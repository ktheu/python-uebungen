"""Prüft, ob die erwarteten Ausgaben eines Notebooks auch in JupyterLite (Pyodide) herauskommen.

Aufruf (aus dem Repo-Ordner, mit einem Python, das die Generatoren ausführen kann, z. B. mit numpy 2.4.6):

    py -3.13 generator/pyodide_check/pruefen.py generator/gen_numpy_2d.py [weitere Generatoren ...]

Ablauf:
1. Der Generator wird lokal ausgeführt (das Notebook landet in einem temporären Ordner, content/ bleibt unverändert).
   Alle Codezellen (Setup, Beispiele, Musterlösungen) werden mit ihrer lokalen Ausgabe als JSON gespeichert.
2. check.mjs startet Pyodide (dieselbe Version wie JupyterLite, siehe package.json), lädt die importierten Pakete
   und führt inner.py aus: Jede Zelle wird dort noch einmal ausgeführt und die Ausgabe mit der lokalen verglichen.

Einmalig vorher in diesem Ordner: npm install
"""
import glob
import json
import os
import shutil
import subprocess
import sys
import tempfile

HIER = os.path.dirname(os.path.abspath(__file__))


def zellen(generator, ordner):
    """Führt den Generator aus und gibt alle Codezellen mit lokaler Ausgabe zurück."""
    sys.path.insert(0, os.path.dirname(os.path.abspath(generator)))
    import nbgen  # vor dem Umleiten der Ausgabe importieren (nbgen stellt stdout auf UTF-8 um)
    import contextlib
    import io
    import runpy
    nbgen.sections.clear()
    nbgen.setup_cell = None
    alt = sys.argv
    sys.argv = [generator, ordner]
    try:
        with contextlib.redirect_stdout(io.StringIO()):
            runpy.run_path(generator, run_name='__main__')
    finally:
        sys.argv = alt
    if not os.listdir(ordner):
        sys.exit(f'{generator}: Der Generator hat nichts geschrieben (PROBLEMS > 0?). Erst lokal fehlerfrei machen.')

    items = []
    alt_dir = os.getcwd()
    tmp = tempfile.mkdtemp()
    os.chdir(tmp)  # wie in nbgen.check(): Setup und Zellen laufen in einem temporären Ordner
    try:
        if nbgen.setup_cell:
            out, err, bilder = nbgen.run_mit_bildern(nbgen.setup_cell['code'])
            items.append({'nr': 'Setup', 'art': 'setup', 'code': nbgen.setup_cell['code'], 'out': out, 'fehler': None})
        for s_i, s in enumerate(nbgen.sections, 1):
            b = 0
            for it in s['items']:
                if it['type'] == 'expl':
                    b += 1
                    out, err, bilder = nbgen.run_mit_bildern(it['code'])
                    items.append({'nr': f'{s_i}. Beispiel {b}', 'art': 'beispiel', 'code': it['code'], 'out': out,
                                  'fehler': None})
                else:
                    items.append({'nr': it['nr'], 'art': it['kind'], 'code': it['solution'], 'out': it['out'],
                                  'fehler': it['error'].__name__ if it['error'] else None})
    finally:
        os.chdir(alt_dir)
        shutil.rmtree(tmp)
    return items


def node_programm():
    for name in ('node.exe', 'node'):
        pfad = os.path.join(HIER, 'node_modules', 'node', 'bin', name)
        if os.path.isfile(pfad) and os.path.getsize(pfad) > 1000:
            return pfad
    sys.exit(f'Node/Pyodide fehlen. Einmalig ausführen:  cd {HIER}  und dann  npm install')


def main():
    if len(sys.argv) < 2:
        sys.exit('Bitte einen oder mehrere Generatoren angeben, zum Beispiel:\n'
                 '    py -3.13 generator/pyodide_check/pruefen.py generator/gen_numpy_2d.py\n'
                 '    py -3.13 generator/pyodide_check/pruefen.py generator/gen_*.py')
    node = node_programm()
    generatoren = []
    for muster in sys.argv[1:]:  # Muster wie gen_*.py selbst auflösen (PowerShell tut das nicht)
        generatoren += sorted(glob.glob(muster)) or [muster]
    fehler = 0
    for generator in generatoren:
        ordner = tempfile.mkdtemp()
        try:
            items = zellen(generator, ordner)
            datei = os.path.join(ordner, 'zellen.json')
            with open(datei, 'w', encoding='utf-8') as f:
                json.dump(items, f, ensure_ascii=False)
            print(f'=== {os.path.basename(generator)}', flush=True)
            r = subprocess.run([node, os.path.join(HIER, 'check.mjs'), datei],
                               capture_output=True, text=True, encoding='utf-8')
            if r.returncode != 0:
                print(r.stderr[-3000:])
                fehler += 1
                continue
            print(r.stdout)
            if 'ECHTE FEHLER: 0' not in r.stdout:
                fehler += 1
        finally:
            shutil.rmtree(ordner)
    sys.exit(1 if fehler else 0)


if __name__ == '__main__':
    main()
