"""Erzeugt ein Übungsnotebook mit aufklappbaren Lösungen.

Ein Generator-Skript (z. B. gen_listen.py) beschreibt mit sec(), expl(), task() und predict()
die Abschnitte, Erklärungen und Aufgaben und ruft am Ende generate() auf.
Dabei werden alle Beispiele und Musterlösungen ausgeführt. Die erwarteten Ausgaben in den
Aufgaben stammen aus diesen Läufen. Geschrieben wird nur, wenn alles fehlerfrei läuft.
Zeichnet eine Musterlösung matplotlib-Diagramme, werden sie als PNG an die Aufgabenzelle angehängt
und als erwartete Ausgabe angezeigt (siehe run_mit_bildern()).

Das Notebook landet in ../content/ (neben dem Ordner generator/) oder im als Argument angegebenen Ordner.
"""
import base64
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

# Sprache des Notebooks, gesetzt von generate(..., sprache=...): Kernel, Platzhalter in den Aufgabenzellen,
# Sprache der Codeblöcke in Markdown. Bei 'python' werden erwartete Ausgaben als Codeblock gezeigt,
# sonst liefert die Ausführungsfunktion fertiges Markdown (z. B. eine Tabelle bei SQL).
SPRACHEN = {
    'python': {
        'kernelspec': {'display_name': 'Python 3 (ipykernel)', 'language': 'python', 'name': 'python3'},
        'language_info': {'codemirror_mode': {'name': 'ipython', 'version': 3}, 'file_extension': '.py',
                          'mimetype': 'text/x-python', 'name': 'python', 'nbconvert_exporter': 'python',
                          'pygments_lexer': 'ipython3', 'version': '3.12.8'},
        'platzhalter': '# your code',
        'codeblock': 'python'},
    'sqlite': {
        'kernelspec': {'display_name': 'SQLite (xsqlite)', 'language': 'sqlite', 'name': 'xsqlite'},
        'language_info': {'name': 'sqlite'},
        'platzhalter': '',  # leere Zelle: wird nicht ausgeführt (eine Zelle nur mit Kommentar gibt im Kernel einen Fehler)
        'codeblock': 'sql'},
}
aktuelle_sprache = 'python'
ausfuehrung = None  # Funktion code -> (ausgabe, fehler, bilder); None bedeutet run_mit_bildern


def setup(md, code):
    """Zelle, die am Anfang beider Notebooks steht (z. B. zum Anlegen von Beispieldateien).
    Sie wird vor allen Aufgaben ausgeführt; alles läuft dabei in einem temporären Ordner."""
    global setup_cell
    setup_cell = {'md': md, 'code': code}


def sec(title, intro=None):
    sections.append({'title': title, 'intro': intro, 'items': []})


def expl(md, code, anhaenge=None):
    """anhaenge: {name: PNG-Daten}, im Markdown als ![...](attachment:name) eingebunden (z. B. ER-Diagramme)."""
    sections[-1]['items'].append({'type': 'expl', 'md': md, 'code': code, 'anhaenge': anhaenge or {}})


def task(text, given='', solution='', kind='normal', error=None, anhaenge=None):
    """kind: 'normal' (mit erwarteter Ausgabe), 'free' (ohne erwartete Ausgabe), 'predict'.
    anhaenge: {name: PNG-Daten} für Bilder im Aufgabentext (![...](attachment:name))."""
    sections[-1]['items'].append({'type': 'task', 'text': text, 'given': given.strip('\n'),
                                  'solution': solution.strip('\n'), 'kind': kind, 'error': error,
                                  'anhaenge': anhaenge or {}})


def predict(code, error=None, anhaenge=None, text=''):
    """text: steht vor der Frage (z. B. ein Diagramm der beteiligten Tabellen)."""
    task(text + 'Was wird ausgegeben? Überlege zuerst, was ausgegeben wird. Führe dann die Zelle aus und vergleiche.',
         given=code, solution=code, kind='predict', error=error, anhaenge=anhaenge)


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


BILD_DPI = 72  # Auflösung der erwarteten Diagramme (klein halten, die Bilder stehen im Notebook)


def run_mit_bildern(code):
    """Wie run(), sammelt aber zusätzlich alle matplotlib-Diagramme als PNG-Daten ein.
    matplotlib wird nur angefasst, wenn der Code es verwendet."""
    plt = None
    if 'matplotlib' in code:
        import matplotlib
        matplotlib.use('Agg')
        import matplotlib.pyplot as plt
        plt.close('all')
        matplotlib.rcdefaults()  # Stiländerungen einer Zelle sollen nicht in die nächste durchschlagen
        plt.show = lambda *args, **kwargs: None  # im Notebook zeigt plt.show() das Bild, hier wird es danach eingesammelt
    out, err = run(code)
    bilder = []
    if plt is not None:
        for nr in plt.get_fignums():
            buf = io.BytesIO()
            plt.figure(nr).savefig(buf, format='png', dpi=BILD_DPI, bbox_inches='tight', metadata={'Software': None})
            bilder.append(buf.getvalue())
        plt.close('all')
    return out, err, bilder


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
    ausf = ausfuehrung or run_mit_bildern  # bei SQL usw. die eigene Ausführungsfunktion
    if setup_cell:
        out, err, bilder = ausf(setup_cell['code'])
        if err:
            print('SETUP ERROR', err); problems += 1
    for s_i, s in enumerate(sections, 1):
        n = 0
        for it in s['items']:
            if it['type'] == 'expl':
                out, err, bilder = ausf(it['code'])
                if err:
                    print('EXPL ERROR', s['title'], err); problems += 1
                continue
            n += 1
            it['nr'] = f'{s_i}.{n}'
            out, err, it['bilder'] = ausf(it['solution'])
            if it['error']:
                if not isinstance(err, it['error']):
                    print('EXPECTED ERROR MISSING', it['nr']); problems += 1
            elif err:
                print('ERROR', it['nr'], err); problems += 1
            if it['given'] and not it['solution'].startswith(it['given']):
                print('GIVEN MISMATCH', it['nr']); problems += 1
            it['out'] = out
            print(f'--- {it["nr"]} ({it["kind"]})\n{out}', end='')
            for b in it['bilder']:
                print(f'[Bild, {len(b) // 1024} KB]')
    print('PROBLEMS:', problems)
    return problems


# ---------------------------------------------------------------- notebooks
def md(src):
    return {'cell_type': 'markdown', 'metadata': {}, 'source': src}


def code(src):
    return {'cell_type': 'code', 'execution_count': None, 'metadata': {}, 'outputs': [], 'source': src}


def bild_name(it, k):
    return f'aufgabe-{it["nr"]}-{k}.png'


def task_md(it):
    text = f'#### Aufgabe {it["nr"]}\n\n'
    if it['kind'] == 'predict':
        text += it['text'] + f'\n```{SPRACHEN[aktuelle_sprache]["codeblock"]}\n{it["given"]}\n```'
    else:
        text += it['text']
        if it['kind'] == 'normal' and aktuelle_sprache != 'python':
            text += '\n\n**Erwartete Ausgabe:**\n\n' + it['out'].rstrip()
        elif it['kind'] == 'normal':
            text += '\n\n**Erwartete Ausgabe:**'
            if it['out'].strip() or not it['bilder']:
                text += f'\n```\n{it["out"].rstrip()}\n```'
            for k in range(len(it['bilder'])):  # Diagramme stehen als Anhang (attachment) in der Markdown-Zelle
                text += f'\n\n![Erwartete Ausgabe](attachment:{bild_name(it, k + 1)})'
    return text


def bilder_anhang(it):
    return {bild_name(it, k + 1): {'image/png': base64.b64encode(b).decode('ascii')}
            for k, b in enumerate(it['bilder'])}


def png_anhang(anhaenge):
    return {name: {'image/png': base64.b64encode(b).decode('ascii')} for name, b in anhaenge.items()}


def loesung_md(it):
    """Aufklappbare Lösung unter der Codezelle (nicht bei Vorhersage-Aufgaben)."""
    titel = 'Beispiellösung anzeigen' if it['kind'] == 'free' else 'Lösung anzeigen'
    return (f'<details>\n<summary>{titel} (erst selbst probieren!)</summary>\n\n'
            f'```{SPRACHEN[aktuelle_sprache]["codeblock"]}\n{it["solution"]}\n```\n\n</details>')


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
                    if it['anhaenge']:
                        cells[-1]['attachments'] = png_anhang(it['anhaenge'])
                    cells.append(code(it['code']))
                continue
            cells.append(md(task_md(it)))
            if it['anhaenge'] or (it['kind'] == 'normal' and it['bilder']):
                cells[-1]['attachments'] = png_anhang(it['anhaenge'])
                if it['kind'] == 'normal':
                    cells[-1]['attachments'].update(bilder_anhang(it))
            if loesung or it['kind'] == 'predict':
                cells.append(code(it['solution']))
            elif it['given']:
                cells.append(code(it['given'] + '\n' + SPRACHEN[aktuelle_sprache]['platzhalter']))
            else:
                cells.append(code(SPRACHEN[aktuelle_sprache]['platzhalter']))
            if aufklappbar and not loesung and it['kind'] != 'predict':
                cells.append(md(loesung_md(it)))
    for i, c in enumerate(cells):
        c['id'] = f'zelle-{i:03d}'  # feste IDs, damit Neugenerieren keine unnötigen Git-Änderungen erzeugt
        lines = c['source'].split('\n')
        c['source'] = [l + '\n' for l in lines[:-1]] + [lines[-1]]
    return {
        'cells': cells,
        'metadata': {
            'kernelspec': SPRACHEN[aktuelle_sprache]['kernelspec'],
            'language_info': SPRACHEN[aktuelle_sprache]['language_info']},
        'nbformat': 4, 'nbformat_minor': 5}


INTRO = '''Jeder Abschnitt beginnt mit kurzen Erklärungen und Beispielen. Führe die Beispiele aus und probiere sie ruhig ein wenig aus.
Danach folgen viele kleine Übungen. Wenn etwas vorgegeben ist, steht es schon in der Codezelle.'''


def generate(name, titel, intro=INTRO, aufklappbar=True, loesungsnotebook=False, sprache='python', ausfuehren=None):
    """Schreibt <name>.ipynb nach ../content/.
    aufklappbar: Lösungen aufklappbar unter jede Aufgabe schreiben.
    loesungsnotebook: zusätzlich ein getrenntes <name>_loesungen.ipynb schreiben (wird normalerweise nicht gebraucht).
    sprache: Schlüssel aus SPRACHEN ('python' oder 'sqlite').
    ausfuehren: Funktion code -> (ausgabe, fehler, bilder) zum Prüfen der Zellen (Standard: Python mit run_mit_bildern)."""
    global aktuelle_sprache, ausfuehrung
    aktuelle_sprache = sprache
    ausfuehrung = ausfuehren
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
