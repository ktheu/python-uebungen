"""Erzeugt ein Übungsnotebook mit aufklappbaren Lösungen.

Ein Generator-Skript (z. B. gen_listen.py) beschreibt mit sec(), expl(), task() und predict()
die Abschnitte, Erklärungen und Aufgaben und ruft am Ende generate() auf.
Dabei werden alle Beispiele und Musterlösungen ausgeführt. Die erwarteten Ausgaben in den
Aufgaben stammen aus diesen Läufen. Geschrieben wird nur, wenn alles fehlerfrei läuft.

Das Notebook landet in ../content/ (neben dem Ordner generator/) oder im als Argument angegebenen Ordner.
"""
import contextlib
import io
import json
import os
import shutil
import sys
import tempfile

sys.stdout.reconfigure(encoding='utf-8')

sections = []
setup_cell = None


def setup(md, code):
    """Zelle, die am Anfang beider Notebooks steht (z. B. zum Anlegen von Beispieldateien).
    Sie wird vor allen Aufgaben ausgeführt; alles läuft dabei in einem temporären Ordner."""
    global setup_cell
    setup_cell = {'md': md, 'code': code}


def sec(title, intro=None):
    sections.append({'title': title, 'intro': intro, 'items': []})


def expl(md, code):
    sections[-1]['items'].append({'type': 'expl', 'md': md, 'code': code})


def task(text, given='', solution='', kind='normal', error=None):
    """kind: 'normal' (mit erwarteter Ausgabe), 'free' (ohne erwartete Ausgabe), 'predict'."""
    sections[-1]['items'].append({'type': 'task', 'text': text, 'given': given.strip('\n'),
                                  'solution': solution.strip('\n'), 'kind': kind, 'error': error})


def predict(code, error=None):
    task('Was wird ausgegeben? Überlege zuerst, was ausgegeben wird. Führe dann die Zelle aus und vergleiche.',
         given=code, solution=code, kind='predict', error=error)


# ---------------------------------------------------------------- run solutions
def run(code):
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        try:
            exec(code, {})
            err = None
        except Exception as e:  # noqa
            err = e
    return buf.getvalue(), err


def check():
    alt = os.getcwd()
    tmp = tempfile.mkdtemp()
    os.chdir(tmp)
    try:
        return _check()
    finally:
        os.chdir(alt)
        shutil.rmtree(tmp)


def _check():
    problems = 0
    if setup_cell:
        out, err = run(setup_cell['code'])
        if err:
            print('SETUP ERROR', err); problems += 1
    for s_i, s in enumerate(sections, 1):
        n = 0
        for it in s['items']:
            if it['type'] == 'expl':
                out, err = run(it['code'])
                if err:
                    print('EXPL ERROR', s['title'], err); problems += 1
                continue
            n += 1
            it['nr'] = f'{s_i}.{n}'
            out, err = run(it['solution'])
            if it['error']:
                if not isinstance(err, it['error']):
                    print('EXPECTED ERROR MISSING', it['nr']); problems += 1
            elif err:
                print('ERROR', it['nr'], err); problems += 1
            if it['given'] and not it['solution'].startswith(it['given']):
                print('GIVEN MISMATCH', it['nr']); problems += 1
            it['out'] = out
            print(f'--- {it["nr"]} ({it["kind"]})\n{out}', end='')
    print('PROBLEMS:', problems)
    return problems


# ---------------------------------------------------------------- notebooks
def md(src):
    return {'cell_type': 'markdown', 'metadata': {}, 'source': src}


def code(src):
    return {'cell_type': 'code', 'execution_count': None, 'metadata': {}, 'outputs': [], 'source': src}


def task_md(it):
    text = f'#### Aufgabe {it["nr"]}\n\n'
    if it['kind'] == 'predict':
        text += it['text'] + f'\n```python\n{it["given"]}\n```'
    else:
        text += it['text']
        if it['kind'] == 'normal':
            text += f'\n\n**Erwartete Ausgabe:**\n```\n{it["out"].rstrip()}\n```'
    return text


def loesung_md(it):
    """Aufklappbare Lösung unter der Codezelle (nicht bei Vorhersage-Aufgaben)."""
    titel = 'Beispiellösung anzeigen' if it['kind'] == 'free' else 'Lösung anzeigen'
    return (f'<details>\n<summary>{titel} (erst selbst probieren!)</summary>\n\n'
            f'```python\n{it["solution"]}\n```\n\n</details>')


AUFKLAPP_HINWEIS = '''Unter den Aufgaben kannst du jeweils die Lösung aufklappen. Versuche es aber immer zuerst selbst!
Bei den Aufgaben „Was wird ausgegeben?“ gibt es keine Lösung zum Aufklappen: Dort führst du einfach die Zelle aus und vergleichst.'''


def build(titel, intro, loesung, aufklappbar):
    cells = []
    if loesung:
        cells.append(md(f'### {titel} - Lösungen'))
    elif aufklappbar:
        cells.append(md(f'### {titel} - Übungen\n\n{intro}\n\n{AUFKLAPP_HINWEIS}'))
    else:
        cells.append(md(f'### {titel} - Übungen\n\n{intro}'))
    if setup_cell:
        cells.append(md(setup_cell['md']))
        cells.append(code(setup_cell['code']))
    for s_i, s in enumerate(sections, 1):
        cells.append(md(f'## {s_i}. {s["title"]}'))
        for it in s['items']:
            if it['type'] == 'expl':
                if not loesung:
                    cells.append(md(it['md']))
                    cells.append(code(it['code']))
                continue
            cells.append(md(task_md(it)))
            if loesung or it['kind'] == 'predict':
                cells.append(code(it['solution']))
            elif it['given']:
                cells.append(code(it['given'] + '\n# your code'))
            else:
                cells.append(code('# your code'))
            if aufklappbar and not loesung and it['kind'] != 'predict':
                cells.append(md(loesung_md(it)))
    for i, c in enumerate(cells):
        c['id'] = f'zelle-{i:03d}'  # feste IDs, damit Neugenerieren keine unnötigen Git-Änderungen erzeugt
        lines = c['source'].split('\n')
        c['source'] = [l + '\n' for l in lines[:-1]] + [lines[-1]]
    return {
        'cells': cells,
        'metadata': {
            'kernelspec': {'display_name': 'Python 3 (ipykernel)', 'language': 'python', 'name': 'python3'},
            'language_info': {'codemirror_mode': {'name': 'ipython', 'version': 3}, 'file_extension': '.py',
                              'mimetype': 'text/x-python', 'name': 'python', 'nbconvert_exporter': 'python',
                              'pygments_lexer': 'ipython3', 'version': '3.12.8'}},
        'nbformat': 4, 'nbformat_minor': 5}


INTRO = '''Jeder Abschnitt beginnt mit kurzen Erklärungen und Beispielen. Führe die Beispiele aus und probiere sie ruhig ein wenig aus.
Danach folgen viele kleine Übungen. Wenn etwas vorgegeben ist, steht es schon in der Codezelle.'''


def generate(name, titel, intro=INTRO, aufklappbar=True, loesungsnotebook=False):
    """Schreibt <name>.ipynb nach ../content/.
    aufklappbar: Lösungen aufklappbar unter jede Aufgabe schreiben.
    loesungsnotebook: zusätzlich ein getrenntes <name>_loesungen.ipynb schreiben (wird normalerweise nicht gebraucht)."""
    standard = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(sys.argv[0]))), 'content')
    out = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else standard)
    if check() != 0:
        print('nichts geschrieben')
        return
    varianten = [(f'{name}.ipynb', False)]
    if loesungsnotebook:
        varianten.append((f'{name}_loesungen.ipynb', True))
    for fname, loesung in varianten:
        nb = build(titel, intro, loesung, aufklappbar)  # erst bauen, dann schreiben: ein Fehler leert keine Datei
        with open(os.path.join(out, fname), 'w', encoding='utf-8') as f:
            json.dump(nb, f, ensure_ascii=False, indent=1)
            f.write('\n')
    print('geschrieben:', os.path.join(out, varianten[0][0]))
