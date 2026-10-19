# Läuft in Pyodide (von check.mjs gestartet). Erwartet die Variable zellen_json und setzt die Variable ergebnis.
import contextlib
import io
import json
import os
import sys
import tempfile

os.environ['MPLBACKEND'] = 'Agg'  # in Node gibt es kein Browserfenster; Diagramme werden nur gezeichnet, nicht angezeigt

zellen = json.loads(zellen_json)
os.chdir(tempfile.mkdtemp())

ERWARTET = {'beispiel', 'free', 'predict'}  # dort steht keine erwartete Ausgabe im Notebook (z. B. Zufall ohne Seed)
echt = []
andere = []
for z in zellen:
    plt = None
    if 'matplotlib' in z['code']:
        import matplotlib
        import matplotlib.pyplot as plt
        plt.close('all')
        matplotlib.rcdefaults()
    buf = io.StringIO()
    fehler = None
    with contextlib.redirect_stdout(buf):
        try:
            exec(z['code'], {})
        except Exception as e:
            fehler = type(e).__name__
    if plt is not None:
        plt.close('all')
    if fehler != z.get('fehler'):
        erwartet = z.get('fehler') or 'kein Fehler'
        echt.append(f"{z['nr']} ({z['art']})\n--- Laufzeitfehler: {fehler or 'keiner'}, erwartet: {erwartet}\n")
    elif buf.getvalue() != z['out']:
        text = f"{z['nr']} ({z['art']})\n--- lokal:\n{z['out']}--- pyodide:\n{buf.getvalue()}"
        (andere if z['art'] in ERWARTET else echt).append(text)

versionen = f'Python {sys.version.split()[0]}'
for paket in ['numpy', 'matplotlib']:
    if paket in sys.modules:
        versionen += f', {paket} {sys.modules[paket].__version__}'
if 'numpy' in sys.modules:
    versionen += f' (Ganzzahltyp {sys.modules["numpy"].arange(1).dtype})'

zeilen = [f'{versionen}, {len(zellen)} Zellen',
          f'ECHTE FEHLER: {len(echt)} (Laufzeitfehler oder Aufgaben mit erwarteter Ausgabe, die in Pyodide anders herauskommen)',
          f'Andere Unterschiede: {len(andere)} (Beispiele, free und predict, z. B. Zufall ohne Seed; nur zur Info)']
if echt:
    zeilen += ['', '##### Echte Fehler'] + echt
if andere:
    zeilen += ['', '##### Andere Unterschiede: ' + ', '.join(t.split('\n')[0] for t in andere)]
ergebnis = '\n'.join(zeilen)
