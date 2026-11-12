"""Ausführung von Zellen für die asyncio-Notebooks, so wie Jupyter sie ausführt.

In einer Notebook-Zelle läuft schon eine Event-Loop. Deshalb darf man dort `await` direkt hinschreiben (Top-Level-await),
und `asyncio.run()` gibt (in JupyterLab/Colab, nicht in JupyterLite) einen RuntimeError. Genau das macht diese Ausführung nach: Der Code der Zelle wird mit
PyCF_ALLOW_TOP_LEVEL_AWAIT übersetzt und **innerhalb** einer laufenden Loop ausgeführt.
Nach der Zelle werden übrig gebliebene Tasks abgebrochen (asyncio.run() räumt so auf; im Notebook liefen sie weiter,
deshalb dürfen die Beispiele nicht darauf angewiesen sein).

nbgen.generate(..., ausfuehren=asyncnb.ausfuehrung()) benutzt das für die erwarteten Ausgaben.
Der Pyodide-Check führt dort die Zellen mit pyodide.code.eval_code_async aus (wie der Kernel von JupyterLite).
Dieses Modul benutzt nur die Standardbibliothek.
"""
import asyncio
import ast
import contextlib
import gc
import inspect
import io
import warnings


def ausfuehrung():
    """Funktion code -> (ausgabe, fehler, bilder) für nbgen."""
    def ausfuehren(code):
        buf = io.StringIO()
        fehler = None
        ns = {}

        async def zelle():
            r = eval(compile(code, '<zelle>', 'exec', flags=ast.PyCF_ALLOW_TOP_LEVEL_AWAIT), ns)
            if inspect.iscoroutine(r):
                await r

        with contextlib.redirect_stdout(buf), warnings.catch_warnings():
            warnings.simplefilter('ignore')  # "coroutine ... was never awaited" steht im Notebook auf stderr, nicht in der Ausgabe
            try:
                asyncio.run(zelle())
            except Exception as e:  # noqa
                fehler = e
            gc.collect()  # nie erwartete Coroutinen jetzt freigeben, damit die Warnung hier (unterdrückt) und nicht später erscheint
        return buf.getvalue(), fehler, []

    ausfuehren.asyncio = True  # Kennzeichen für den Pyodide-Check
    return ausfuehren
