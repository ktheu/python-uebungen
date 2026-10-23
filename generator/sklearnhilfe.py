"""Gemeinsames für die scikit-learn-Notebooks (gen_sklearn_*.py)."""
import re

from nbgen import task


def t(text, given='', body='', kind='normal'):
    """Aufgabe, deren Lösung aus dem vorgegebenen Code plus body besteht."""
    loesung = (given + '\n' + body) if given else body
    task(text, given=given, solution=re.sub(r'\n{3,}', '\n\n', loesung), kind=kind)  # höchstens eine Leerzeile


# Erste Zeilen jeder Setup-Zelle: Pyodide meldet beim ersten fit() eines k-NN-Modells eine RuntimeWarning
# (JsProxy.as_object_map, aus threadpoolctl).
WARNUNG = """import warnings
warnings.filterwarnings('ignore', message='JsProxy')   # harmlose Meldung des Browser-Pythons ausblenden"""

WARNUNG_MD = 'Die erste Zeile blendet eine harmlose Meldung aus, die das Python im Browser sonst beim ersten Training anzeigt.'

# Legt iris.csv mit deutschen Spaltennamen an.
IRIS_CSV = """from sklearn.datasets import load_iris

iris = load_iris(as_frame=True).frame
iris.columns = ['kelch_laenge', 'kelch_breite', 'bluete_laenge', 'bluete_breite', 'art']
iris['art'] = iris['art'].map({0: 'setosa', 1: 'versicolor', 2: 'virginica'})
iris.to_csv('iris.csv', index=False)"""

IRIS_MD = '''`iris.csv`: die berühmten Iris-Daten von 1936, 150 vermessene Schwertlilien von drei Arten (*setosa*, *versicolor*, *virginica*).
  Gemessen sind Länge und Breite des **Kelchblatts** und des **Blütenblatts** in cm.'''

REIHE = '''Die Reihe hat vier Notebooks:

1. Grundlagen: Merkmale und Zielwerte, das erste Modell, Trainings- und Testdaten, Skalieren
2. Klassifikation: k-nächste Nachbarn, Entscheidungsbäume, logistische Regression, neuronale Netze, Kreuzvalidierung
3. Regression: Zahlen vorhersagen, Überanpassung
4. Unüberwachtes Lernen: Clustering, Dimensionen reduzieren, Ziffernerkennung'''


def reihe(nr):
    """Liste der Notebooks, das aktuelle fett und mit dem Zusatz (dieses Notebook)."""
    zeilen = REIHE.split('\n')
    i = 1 + nr
    name, rest = zeilen[i][3:].split(':', 1)
    zeilen[i] = f'{nr}. **{name}**:{rest} (dieses Notebook)'
    return '\n'.join(zeilen)


SCHLUSS = '''**Tabellen anzeigen:** Steht eine Tabelle (ein DataFrame) in der **letzten Zeile** einer Zelle, zeigt JupyterLab sie als Tabelle an. Mehrere Tabellen
in einer Zelle zeigt man mit `display(df)` an. Einzelne Werte gibt man wie gewohnt mit `print()` aus. Die erwarteten Ausgaben in den Aufgaben sehen genauso aus.

Jeder Abschnitt beginnt mit kurzen Erklärungen und Beispielen. Führe die Beispiele aus und probiere sie ruhig ein wenig aus.
Danach folgen viele kleine Übungen. Wenn etwas vorgegeben ist, steht es schon in der Codezelle.

Beim ersten `import sklearn` lädt der Browser die Pakete nach. Das dauert einige Sekunden.'''
