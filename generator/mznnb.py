"""Ausführung und Darstellung von MiniZinc-Modellen für die Arbeitsblätter in extern/ (gen_minizinc_*.py).

Die Notebooks (nbgen-Sprache 'minizinc') zeigen Modelle in Codezellen, die man nicht ausführt (nur zum Lesen und Kopieren),
die Ausgaben als Markdown darunter; unter jeder Aufgabe eine Codezelle für die eigene Lösung; Musterlösungen als Markdown-Block. Gerechnet wird in der MiniZinc IDE oder im Playground. Beim Erzeugen führt dieses Modul jedes Modell mit dem lokal
installierten MiniZinc aus (Solver Gecode, wie in der IDE voreingestellt) und liefert die Ausgabe als Markdown.

Steuerzeilen im Code (erscheinen nicht im Notebook):
    %! alle           alle Lösungen ausgeben (-a)
    %! anzahl         nur die Anzahl aller Lösungen zeigen
    %! mehrdeutig     es gibt mehrere (optimale) Lösungen: Ausgabe mit Hinweis, keine Eindeutigkeitsprüfung
    %! solver=highs   anderen Solver benutzen (Standard gecode)
Eine Zeile  % --- Daten (name.dzn) ---  trennt Modell und Daten (im Notebook zwei Blöcke, beim Lösen eine .dzn-Datei).

Eindeutigkeit: Ohne 'alle', 'anzahl' und 'mehrdeutig' muss die Lösung eindeutig sein, sonst ist die erwartete Ausgabe
nicht verlässlich (ein anderer Solver oder eine andere Version findet eine andere). Bei 'solve satisfy' wird mit -n 2 gezählt,
bei Optimierung wird der Zielwert festgehalten und dann gezählt (nur bei ganzzahligem Zielwert).
"""
import os
import re
import shutil
import subprocess
import tempfile

from nbgen import task

# ---------------------------------------------------------------- gemeinsame Bausteine der Generatoren gen_minizinc_*.py
REIHE = '''Die Reihe hat drei Notebooks:

1. Grundlagen: Modelle, Variablen, Bedingungen, Optimieren
2. Daten: Aufzählungen, Arrays, Datendateien, Mengen
3. Zuordnen und Planen: Zuordnungen, Sitz- und Dienstpläne, Gruppen'''


def reihe(nr):
    """Liste der Notebooks, das aktuelle fett und mit dem Zusatz (dieses Notebook)."""
    zeilen = REIHE.split('\n')
    i = 1 + nr
    name, rest = zeilen[i][3:].split(':', 1)
    zeilen[i] = f'{nr}. **{name}**:{rest} (dieses Notebook)'
    return '\n'.join(zeilen)


ARBEITSBLATT = '''**Dieses Notebook ist ein Arbeitsblatt.** MiniZinc läuft weder im Browser-Python der Übungsseite noch in Colab. Die Codezellen enthalten
MiniZinc-Code, keinen Python-Code: **Führe sie hier nicht aus**, sondern kopiere sie. Lies die Erklärungen hier und schreibe und starte die Modelle in der **MiniZinc IDE**
(kostenlos für Windows, macOS und Linux: [minizinc.org](https://www.minizinc.org/)). Ohne Installation geht es auch im Browser im
[MiniZinc Playground](https://play.minizinc.org/).

Jeder Abschnitt beginnt mit kurzen Erklärungen und Beispielen. Tippe die Beispiele in der IDE ab (oder kopiere sie) und probiere sie aus.
Danach folgen kleine Übungen mit der erwarteten Ausgabe. Unter jeder Aufgabe steht eine Codezelle für deine Lösung: Schreib sie dort hinein,
damit du sie später nachlesen kannst, und führe sie in der MiniZinc IDE aus.'''


def t(text, loesung, kind='normal'):
    """Aufgabe: Text (Markdown) und Musterlösung (MiniZinc). Darunter eine Codezelle für die eigene Lösung (ausgeführt wird in der IDE)."""
    task(text, solution=loesung, kind=kind)


def vorhersage(code, erklaerung):
    task('Was gibt das Modell in der Zelle unten aus? Überlege zuerst, führe es dann in der MiniZinc IDE aus und vergleiche.',
         solution=code, kind='predict', erklaerung=erklaerung)


MINIZINC = shutil.which('minizinc') or r'C:\Program Files\MiniZinc\minizinc.exe'
TRENNER = re.compile(r'^% --- Daten(?: \((?P<name>[^)]+)\))? ---\s*$', re.M)
ZEITLIMIT_MS = 60000


class MehrdeutigError(Exception):
    pass


class MiniZincFehler(Exception):
    pass


def zerlegen(code):
    """-> (optionen, modell, daten, datenname). Optionen aus den %!-Zeilen."""
    optionen = {}
    zeilen = []
    for z in code.split('\n'):
        if z.startswith('%!'):
            for teil in z[2:].split():
                schluessel, _, wert = teil.partition('=')
                optionen[schluessel] = wert or True
        else:
            zeilen.append(z)
    text = '\n'.join(zeilen).strip('\n')
    m = TRENNER.search(text)
    if not m:
        return optionen, text, '', None
    return optionen, text[:m.start()].rstrip('\n'), text[m.end():].strip('\n'), m.group('name') or 'daten.dzn'


def darstellung(code):
    """Markdown für das Notebook: Modell als Block, Daten als zweiter Block."""
    optionen, modell, daten, name = zerlegen(code)
    text = f'```minizinc\n{modell}\n```'
    if daten:
        text += f'\n\nDaten (Datei `{name}`):\n\n```minizinc\n{daten}\n```'
    return text


def zellen(code):
    """Codezellen für das Notebook: Modell, bei Bedarf eine Überschrift und die Daten als zweite Zelle."""
    optionen, modell, daten, name = zerlegen(code)
    teile = [('code', modell)]
    if daten:
        teile += [('md', f'Daten (Datei `{name}`):'), ('code', daten)]
    return teile


def loesen(modell, daten, argumente):
    """Führt MiniZinc aus und gibt die Ausgabe (stdout) zurück."""
    ordner = tempfile.mkdtemp()
    try:
        mzn = os.path.join(ordner, 'modell.mzn')
        with open(mzn, 'w', encoding='utf-8') as f:
            f.write(modell + '\n')
        dateien = [mzn]
        if daten:
            dzn = os.path.join(ordner, 'daten.dzn')
            with open(dzn, 'w', encoding='utf-8') as f:
                f.write(daten + '\n')
            dateien.append(dzn)
        r = subprocess.run([MINIZINC, '--time-limit', str(ZEITLIMIT_MS), *argumente, *dateien],
                           capture_output=True, text=True, encoding='utf-8')
        if r.returncode != 0 or '=====ERROR=====' in r.stdout or '=====UNKNOWN=====' in r.stdout:
            raise MiniZincFehler((r.stdout + r.stderr).strip()[-600:])
        return r.stdout
    finally:
        shutil.rmtree(ordner)


def ohne_kommentare(modell):
    return re.sub(r'%[^\n]*', '', modell)


def anzahl_loesungen(modell, daten, solver, grenze=None):
    argumente = ['--solver', solver] + (['-n', str(grenze)] if grenze else ['-a'])
    return loesen(modell, daten, argumente).count('----------')


def pruefe_eindeutig(modell, daten, solver):
    """Wirft MehrdeutigError, wenn es mehr als eine (optimale) Lösung gibt."""
    rein = ohne_kommentare(modell)
    ziel = re.search(r'\bsolve\s+(maximize|minimize)\s+(.*?);', rein, re.S)
    if not ziel:
        if anzahl_loesungen(modell, daten, solver, grenze=2) > 1:
            raise MehrdeutigError('mehrere Lösungen (solve satisfy); %! mehrdeutig oder Modell eindeutig machen')
        return
    out = loesen(modell, daten, ['--solver', solver, '--output-mode', 'dzn', '--output-objective'])
    werte = re.findall(r'_objective = (-?\d+);', out)
    if not werte:
        return  # Kommazahl als Zielwert: keine Prüfung
    fest = (rein[:ziel.start()] + f'constraint ({ziel.group(2)}) = {werte[-1]};\nsolve satisfy;' + rein[ziel.end():])
    if anzahl_loesungen(fest, daten, solver, grenze=2) > 1:
        raise MehrdeutigError(f'mehrere optimale Lösungen (Zielwert {werte[-1]}); %! mehrdeutig oder Modell eindeutig machen')


def ausfuehrung():
    """Funktion code -> (markdown, fehler, bilder) für nbgen.generate(..., ausfuehren=...)."""
    def ausfuehren(code):
        optionen, modell, daten, name = zerlegen(code)
        solver = optionen.get('solver', 'gecode')
        try:
            if 'anzahl' in optionen:
                n = anzahl_loesungen(modell, daten, solver)
                return f'**Anzahl der Lösungen: {n}**', None, []
            argumente = ['--solver', solver] + (['-a'] if 'alle' in optionen else [])
            out = loesen(modell, daten, argumente).rstrip()
            if not ({'alle', 'mehrdeutig'} & set(optionen)):
                pruefe_eindeutig(modell, daten, solver)
        except (MiniZincFehler, MehrdeutigError) as e:
            return '', e, []
        text = f'```\n{out}\n```'
        if 'mehrdeutig' in optionen:
            text += '\n\n*Eine von mehreren möglichen Lösungen: Dein Solver findet vielleicht eine andere.*'
        return text, None, []

    return ausfuehren
