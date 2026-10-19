# Läuft in Pyodide (von check.mjs gestartet). Erwartet die Variable zellen_json und setzt die Variable ergebnis.
import contextlib
import io
import json
import os
import sys
import tempfile

zellen = json.loads(zellen_json)
os.chdir(tempfile.mkdtemp())

ERWARTET = {'beispiel', 'free', 'predict'}  # dort steht keine erwartete Ausgabe im Notebook (z. B. Zufall ohne Seed)
echt = []
andere = []
for z in zellen:
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        try:
            exec(z['code'], {})
        except Exception:
            pass  # Fehler-Beispiele (predict mit error=...) brechen ab wie lokal
    if buf.getvalue() != z['out']:
        text = f"{z['nr']} ({z['art']})\n--- lokal:\n{z['out']}--- pyodide:\n{buf.getvalue()}"
        (andere if z['art'] in ERWARTET else echt).append(text)

versionen = f'Python {sys.version.split()[0]}'
try:
    import numpy
    versionen += f', numpy {numpy.__version__} (Ganzzahltyp {numpy.arange(1).dtype})'
except ImportError:
    pass

zeilen = [f'{versionen}, {len(zellen)} Zellen',
          f'ECHTE FEHLER: {len(echt)} (Aufgaben mit erwarteter Ausgabe, die in Pyodide anders herauskommen)',
          f'Andere Unterschiede: {len(andere)} (Beispiele, free und predict, z. B. Zufall ohne Seed; nur zur Info)']
if echt:
    zeilen += ['', '##### Echte Fehler'] + echt
if andere:
    zeilen += ['', '##### Andere Unterschiede: ' + ', '.join(t.split('\n')[0] for t in andere)]
ergebnis = '\n'.join(zeilen)
