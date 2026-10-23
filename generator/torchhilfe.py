"""Gemeinsames für die PyTorch-Notebooks (gen_pytorch_*.py). Sie landen in ../extern/ und werden in Google Colab geöffnet."""
import re

from nbgen import task, expl as nbgen_expl, predict as nbgen_predict


def eine_leerzeile(code):
    """Höchstens eine Leerzeile hintereinander (auch zwischen Funktionen und Klassen)."""
    return re.sub(r'\n{3,}', '\n\n', code)


def expl(md, code, **optionen):
    nbgen_expl(md, eine_leerzeile(code) if code else code, **optionen)


def predict(code, **optionen):
    nbgen_predict(eine_leerzeile(code), **optionen)


def t(text, given='', body='', kind='normal'):
    """Aufgabe, deren Lösung aus dem vorgegebenen Code plus body besteht."""
    given = re.sub(r'\n{3,}', '\n\n', given)  # höchstens eine Leerzeile, auch im vorgegebenen Code
    loesung = (given + '\n' + body) if given else body
    task(text, given=given, solution=re.sub(r'\n{3,}', '\n\n', loesung), kind=kind)


REIHE = '''Die Reihe hat vier Notebooks:

1. Tensoren: erzeugen, umformen, auswählen, rechnen
2. Lernen: Gradienten, Gradientenabstieg, die Trainingsschleife
3. Netze: neuronale Netze bauen und trainieren, Mini-Batches, Überanpassung
4. Bilder: Ziffern erkennen mit voll verbundenen Netzen und Faltungsnetzen'''


def reihe(nr):
    """Liste der Notebooks, das aktuelle fett und mit dem Zusatz (dieses Notebook)."""
    zeilen = REIHE.split('\n')
    i = 1 + nr
    name, rest = zeilen[i][3:].split(':', 1)
    zeilen[i] = f'{nr}. **{name}**:{rest} (dieses Notebook)'
    return '\n'.join(zeilen)


COLAB = '''**Dieses Notebook läuft nicht im Browser-Python der Übungsseite**, weil es PyTorch dort nicht gibt. Öffne es über den Link in der
Übersicht in **Google Colab** (dafür brauchst du ein Google-Konto). PyTorch ist in Colab schon installiert. Colab öffnet eine Kopie:
Wer seine Lösungen behalten will, wählt *Datei → Kopie in Drive speichern*.

Bei Zufallszahlen und beim Training können deine Ergebnisse in den letzten Stellen von den Lösungen abweichen, je nach PyTorch-Version und Rechner.
Aufgaben mit Training haben deshalb keine erwartete Ausgabe, sondern eine Beispiellösung und eine Angabe, ungefähr welche Werte herauskommen sollten.'''

SCHLUSS = '''Jeder Abschnitt beginnt mit kurzen Erklärungen und Beispielen. Führe die Beispiele aus und probiere sie ruhig ein wenig aus.
Danach folgen viele kleine Übungen. Wenn etwas vorgegeben ist, steht es schon in der Codezelle.'''
