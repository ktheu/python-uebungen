"""Ausführung von Zellen für die pandas-Notebooks, so wie JupyterLab sie anzeigt.

- Text von print() erscheint als Textblock (```).
- Ist die letzte Zeile ein Ausdruck, wird sein Wert angezeigt (wie "Out[ ]"); ebenso alles, was mit display() ausgegeben wird.
  DataFrames werden als HTML-Tabelle angezeigt, Pillow-Bilder als Bild (Anhang, verkleinert, siehe pillow_anhang()),
  alles andere (auch Series) als Text mit repr().
- Die Reihenfolge von print() und display() bleibt erhalten.

nbgen.generate(..., ausfuehren=pandasnb.ausfuehrung(), ausgabe_markdown=True) benutzt das für die erwarteten Ausgaben.
Der Pyodide-Check (pyodide_check/pruefen.py) führt zelle_ausfuehren() und als_markdown() in Pyodide aus und vergleicht.
Dieses Modul darf deshalb außer der Standardbibliothek nichts importieren (pandas nur innerhalb der Funktionen).
"""
import ast
import re


class _Sammler:
    """Ersatz für sys.stdout: sammelt Text in die gemeinsame Liste der Ausgabeteile."""

    def __init__(self, teile):
        self.teile = teile

    def write(self, s):
        if s:
            self.teile.append(('text', s))
        return len(s)

    def flush(self):
        pass


def html_tabelle(df):
    """DataFrame als HTML-Tabelle wie in JupyterLab: links stehend, Zellen rechtsbündig, höchstens 60 Zeilen (sonst gekürzt)."""
    h = df.to_html(max_rows=60, show_dimensions=len(df) > 60)
    h = h.replace('<table border="1" class="dataframe">', '<table style="margin-left: 0">')
    h = re.sub(r'<(th|td)(\s[^>]*)?>', lambda m: f'<{m.group(1)}{m.group(2) or ""} style="text-align: right">', h)
    h = h.replace('<tr style="text-align: right;">', '<tr>')
    return h


def _darstellen(wert, teile):
    if wert is None:
        return
    if type(wert).__name__ == 'DataFrame':
        teile.append(('html', html_tabelle(wert)))
    elif type(wert).__module__.startswith('PIL.') and hasattr(wert, '_repr_png_'):
        teile.append(('bild', wert))   # Pillow-Bild: JupyterLab zeigt es als Bild an (in als_markdown nicht enthalten)
    else:
        teile.append(('text', repr(wert) + '\n'))


def zelle_ausfuehren(code, namensraum=None):
    """Führt code aus wie eine Notebook-Zelle. Gibt (teile, fehler) zurück; teile ist eine Liste von ('text'|'html', inhalt)."""
    import contextlib
    teile = []
    ns = {} if namensraum is None else namensraum
    ns['display'] = lambda *werte: [_darstellen(w, teile) for w in werte] and None
    fehler = None
    with contextlib.redirect_stdout(_Sammler(teile)):
        try:
            baum = ast.parse(code)
            letzter = None
            if baum.body and isinstance(baum.body[-1], ast.Expr):
                letzter = ast.Expression(baum.body.pop().value)
            exec(compile(baum, '<zelle>', 'exec'), ns)
            if letzter is not None:
                _darstellen(eval(compile(letzter, '<zelle>', 'eval'), ns), teile)
        except Exception as e:  # noqa
            fehler = e
    return teile, fehler


def als_markdown(teile):
    """Fasst aufeinanderfolgenden Text zu Codeblöcken zusammen; HTML-Tabellen stehen dazwischen."""
    bloecke = []
    text = ''
    for art, inhalt in teile:
        if art == 'bild':
            continue
        if art == 'text':
            text += inhalt
        else:
            if text:
                bloecke.append('```\n' + text.rstrip('\n') + '\n```')
                text = ''
            bloecke.append(inhalt.rstrip('\n'))
    if text:
        bloecke.append('```\n' + text.rstrip('\n') + '\n```')
    return '\n\n'.join(bloecke) + ('\n' if bloecke else '')


BILD_MAX = 320  # erwartete Pillow-Bilder höchstens so breit/hoch (Pixel), damit die Notebooks klein bleiben


def pillow_anhang(bild):
    """Pillow-Bild als Daten für den Anhang: verkleinert auf BILD_MAX; Fotos (viele Farben) als JPEG, sonst PNG."""
    import io
    foto = bild.mode in ('RGB', 'L') and bild.getcolors(256) is None  # am Original zählen: Verkleinern erzeugt Zwischenfarben
    kopie = bild.copy()
    kopie.thumbnail((BILD_MAX, BILD_MAX))
    if kopie.mode not in ('RGB', 'RGBA', 'L', '1'):
        kopie = kopie.convert('RGBA')
    buf = io.BytesIO()
    if foto:
        kopie.save(buf, 'JPEG', quality=85)
    else:
        kopie.save(buf, 'PNG', optimize=True)
    return buf.getvalue()


def ausfuehrung():
    """Funktion code -> (markdown, fehler, bilder) für nbgen. Sammelt matplotlib-Diagramme wie nbgen.run_mit_bildern()."""
    def ausfuehren(code):
        import io
        plt = None
        if 'matplotlib' in code or '.plot' in code or '.hist(' in code:
            import matplotlib
            matplotlib.use('Agg')
            import matplotlib.pyplot as plt
            plt.close('all')
            matplotlib.rcdefaults()
            plt.show = lambda *args, **kwargs: None
        teile, fehler = zelle_ausfuehren(code)
        bilder = [pillow_anhang(inhalt) for art, inhalt in teile if art == 'bild']
        if plt is not None:
            for nr in plt.get_fignums():
                buf = io.BytesIO()
                plt.figure(nr).savefig(buf, format='png', dpi=72, bbox_inches='tight', metadata={'Software': None})
                bilder.append(buf.getvalue())
            plt.close('all')
        return als_markdown(teile), fehler, bilder

    ausfuehren.pandas = True  # Kennzeichen für den Pyodide-Check
    return ausfuehren
