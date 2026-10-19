# Erzeugt ../content/numpy_zufall_statistik.ipynb (siehe nbgen.py).
#
# Braucht numpy in derselben Version wie Pyodide in JupyterLite (zurzeit 2.4.6), siehe gen_numpy_grundlagen.py:
#     py -3.13 -W error generator/gen_numpy_zufall_statistik.py
#
# Zufall: Aufgaben ohne festen Seed sind 'free'. Aufgaben mit erwarteter Ausgabe geben
# rng = np.random.default_rng(...) vor und nennen im Text genau die Aufrufe (Reihenfolge und Argumente),
# sonst entstehen andere Zahlen. Die Ausgaben wurden mit echtem Pyodide 314.0.6 (numpy 2.4.6) verglichen.
from nbgen import sec, expl, task, predict, generate


def t(text, given='', body='', kind='normal'):
    """Aufgabe, deren Lösung aus dem vorgegebenen Code plus body besteht."""
    task(text, given=given, solution=(given + '\n' + body) if given else body, kind=kind)


NP = 'import numpy as np'


def rng(seed):
    return NP + f'\nrng = np.random.default_rng({seed})'


INTRO = '''numpy kann sehr schnell **viele Zufallszahlen auf einmal** erzeugen und große Datenmengen **statistisch auswerten**:
Mittelwert, Median, Streuung, Häufigkeiten, ... Zusammen erlaubt das **Simulationen**: Statt eine Münze tausendmal in einer
Schleife zu werfen, erzeugt man ein Array mit tausend Würfen und zählt mit einer Maske.

Vorausgesetzt werden die Notebooks *numpy: Grundlagen*, *numpy: Filtern und Auswählen* und *numpy: Zweidimensionale Arrays*.
Das Notebook *Zufallszahlen mit random* ist hilfreich, aber nicht nötig.

Jeder Abschnitt beginnt mit kurzen Erklärungen und Beispielen. Führe die Beispiele aus und probiere sie ruhig ein wenig aus.
Danach folgen viele kleine Übungen. Wenn etwas vorgegeben ist, steht es schon in der Codezelle.

Zufallszahlen sind bei jedem Lauf anders. Deshalb steht nur bei Aufgaben mit einem festen **Seed**
(`np.random.default_rng(42)`) eine erwartete Ausgabe. Damit du genau diese Ausgabe bekommst, musst du die Funktionen
genau so und in genau der Reihenfolge aufrufen, wie es in der Aufgabe steht.'''

# ---------------------------------------------------------------- 1
sec('Der Zufallsgenerator')
expl('''#### `np.random.default_rng()`

Für Zufallszahlen erzeugt man zuerst einen **Zufallsgenerator**: `rng = np.random.default_rng()`.
(*rng* steht für *random number generator*.) Alle Zufallszahlen holt man sich dann mit Methoden von `rng`.

- `rng.random()` liefert eine zufällige Kommazahl von 0 (einschließlich) bis 1 (ausschließlich).
- `rng.random(5)` liefert ein Array mit 5 solchen Zahlen.
- `rng.integers(a, b)` liefert eine zufällige ganze Zahl von `a` bis **ausschließlich** `b`. Ein Würfel ist also `rng.integers(1, 7)`.
  Achtung: Bei `random.randint(1, 6)` aus dem Modul `random` gehört die 6 dazu, bei `rng.integers(1, 6)` nicht!
- `rng.integers(a, b, size=10)` liefert ein Array mit 10 Zahlen.''',
     """import numpy as np

rng = np.random.default_rng()
print(rng.random())
print(rng.random(5))
print(rng.integers(1, 7))
print(rng.integers(1, 7, size=10))""")
expl('''#### Ein fester Seed

Gibt man beim Erstellen eine Zahl an, den **Seed** (englisch für Samenkorn), liefert der Generator bei jedem Lauf
**dieselben** Zufallszahlen: `rng = np.random.default_rng(42)`.
Das ist praktisch zum Testen und damit andere ein Ergebnis nachprüfen können.

Die Zahlen hängen aber von der Reihenfolge der Aufrufe ab: Ein zusätzlicher Aufruf dazwischen verschiebt alles danach.''',
     """import numpy as np

rng = np.random.default_rng(42)
print(rng.integers(1, 7, size=5))
rng = np.random.default_rng(42)
print(rng.integers(1, 7, size=5))
print(rng.integers(1, 7, size=5))""")
expl('''#### Ältere Schreibweise

In älteren Programmen und im Internet sieht man oft `np.random.seed(42)` und `np.random.randint(1, 7, size=10)`.
Das funktioniert auch noch, empfohlen ist heute aber der Generator mit `default_rng()`. Wir verwenden nur diesen.''',
     """import numpy as np

np.random.seed(1)
print(np.random.randint(1, 7, size=5))""")

t('Erstelle einen Zufallsgenerator ohne Seed und gib eine zufällige Kommazahl zwischen 0 und 1 aus. Führe die Zelle mehrmals aus.',
  NP, """rng = np.random.default_rng()
print(rng.random())""", kind='free')
t('Gib einen zufälligen Würfelwurf (1 bis 6) aus.',
  NP, """rng = np.random.default_rng()
print(rng.integers(1, 7))""", kind='free')
t('Gib ein Array mit 20 Würfelwürfen aus.',
  NP, """rng = np.random.default_rng()
print(rng.integers(1, 7, size=20))""", kind='free')
t('Gib ein Array mit 10 zufälligen ganzen Zahlen von 0 bis einschließlich 100 aus.',
  NP, """rng = np.random.default_rng()
print(rng.integers(0, 101, size=10))""", kind='free')
t('Gib mit `rng.integers(1, 7, size=10)` zehn Würfelwürfe aus.',
  rng(42), """print(rng.integers(1, 7, size=10))""")
t('Gib mit `rng.random(3)` drei Zufallszahlen aus, gerundet auf zwei Nachkommastellen.',
  rng(7), """print(np.round(rng.random(3), 2))""")
t('Rufe zweimal hintereinander `rng.integers(1, 101, size=4)` auf und gib beide Arrays aus.',
  rng(3), """print(rng.integers(1, 101, size=4))
print(rng.integers(1, 101, size=4))""")
t('Erstelle den Generator zweimal mit dem Seed 5 und rufe danach jeweils `rng.integers(0, 10, size=6)` auf. Gib beide Ergebnisse aus.',
  NP, """rng = np.random.default_rng(5)
print(rng.integers(0, 10, size=6))
rng = np.random.default_rng(5)
print(rng.integers(0, 10, size=6))""")
t('Erzeuge mit `rng.integers(0, 2, size=10)` zehn Münzwürfe (0 = Zahl, 1 = Kopf) und gib sie und die Anzahl der Köpfe aus.',
  rng(11), """muenzen = rng.integers(0, 2, size=10)
print(muenzen)
print(muenzen.sum())""")
predict("""import numpy as np
rng = np.random.default_rng()
w = rng.integers(1, 3, size=8)
print(w)
print(w.min(), w.max())
print(rng.integers(5, 6, size=3))""")

# ---------------------------------------------------------------- 2
sec('Zufallszahlen erzeugen')
expl('''#### Gleichverteilte Zahlen und 2D-Arrays

- `rng.uniform(a, b, size=n)`: `n` Kommazahlen, gleichmäßig verteilt von `a` bis `b`.
- `rng.integers(a, b, size=(z, s))` und `rng.random((z, s))`: Mit einem Tupel als `size` entsteht ein 2D-Array.
- `rng.integers(a, b, size=n, endpoint=True)`: Mit `endpoint=True` gehört `b` dazu.''',
     """import numpy as np

rng = np.random.default_rng(1)
print(np.round(rng.uniform(10, 20, size=4), 2))
print(rng.integers(1, 7, size=(3, 5)))
print(rng.integers(1, 6, size=8, endpoint=True))""")
expl('''#### Normalverteilte Zahlen

Viele Größen aus der Natur (Körpergröße, Messfehler, ...) sind **normalverteilt**: Die meisten Werte liegen nahe am Mittelwert,
große Abweichungen sind selten. Die Häufigkeiten bilden eine Glockenkurve.

`rng.normal(mittelwert, standardabweichung, size=n)` erzeugt `n` normalverteilte Zahlen.
Die **Standardabweichung** gibt an, wie stark die Werte streuen (mehr dazu in Abschnitt 4).
Etwa 68 % der Werte liegen höchstens eine Standardabweichung vom Mittelwert entfernt, etwa 95 % höchstens zwei.''',
     """import numpy as np

rng = np.random.default_rng(1)
groessen = rng.normal(170, 8, size=10)
print(np.round(groessen))
viele = rng.normal(170, 8, size=100000)
print(np.round(viele.mean(), 1))
print(np.round((np.abs(viele - 170) <= 8).mean(), 3))""")

t('Erzeuge 5 zufällige Kommazahlen von 1.5 bis 2.0 (Körpergrößen in Metern) und gib sie mit zwei Nachkommastellen aus.',
  NP, """rng = np.random.default_rng()
print(np.round(rng.uniform(1.5, 2.0, size=5), 2))""", kind='free')
t('Gib mit `rng.uniform(-10, 30, size=7)` die Temperaturen einer Woche aus, gerundet auf eine Nachkommastelle.',
  rng(21), """print(np.round(rng.uniform(-10, 30, size=7), 1))""")
t('Erzeuge mit `rng.integers(0, 2, size=(4, 6))` ein 4 × 6-Grid aus Nullen und Einsen und gib es aus.',
  rng(8), """print(rng.integers(0, 2, size=(4, 6)))""")
t('Erzeuge mit `rng.integers(1, 6, size=12, endpoint=True)` zwölf Noten von 1 bis 5 und gib sie aus.',
  rng(4), """print(rng.integers(1, 6, size=12, endpoint=True))""")
t('''Erzeuge mit `rng.integers(1, 7, size=(5, 3))` fünf Würfe mit je drei Würfeln (eine Zeile pro Wurf).
Gib das Array und die Augensumme jedes Wurfs aus.''',
  rng(2), """w = rng.integers(1, 7, size=(5, 3))
print(w)
print(w.sum(axis=1))""")
t('Erzeuge mit `rng.normal(170, 8, size=8)` acht Körpergrößen in cm und gib sie auf ganze Zentimeter gerundet als ganze Zahlen aus.',
  rng(9), """print(np.round(rng.normal(170, 8, size=8)).astype(int))""")
t('Erzeuge 100000 normalverteilte Werte mit Mittelwert 50 und Standardabweichung 10. Gib den Mittelwert der Werte und den Anteil der Werte zwischen 30 und 70 aus.',
  NP, """rng = np.random.default_rng()
w = rng.normal(50, 10, size=100000)
print(w.mean())
print(((w >= 30) & (w <= 70)).mean())""", kind='free')
t('''Ein Messgerät misst eine Länge von 20 cm mit einem Fehler (Standardabweichung 0.3 cm). Erzeuge mit `rng.normal(20, 0.3, size=6)`
sechs Messungen und gib sie mit zwei Nachkommastellen aus und darunter ihren Mittelwert (zwei Nachkommastellen).''',
  rng(12), """m = rng.normal(20, 0.3, size=6)
print(np.round(m, 2))
print(np.round(m.mean(), 2))""")
t('Erzeuge mit `rng.random((3, 3))` ein 3 × 3-Array und gib es mit einer Nachkommastelle aus. Gib darunter aus, wie viele Werte größer als 0.5 sind.',
  rng(6), """a = rng.random((3, 3))
print(np.round(a, 1))
print((a > 0.5).sum())""")
predict("""import numpy as np
rng = np.random.default_rng()
a = rng.integers(0, 10, size=(2, 4))
print(a.shape)
print(rng.uniform(5, 5.001, size=3).round())
print(rng.normal(0, 0, size=2))""")

# ---------------------------------------------------------------- 3
sec('Auswählen und mischen')
expl('''#### `rng.choice()`

`rng.choice(werte)` wählt ein zufälliges Element aus einer Liste oder einem Array.

- `rng.choice(werte, size=5)`: 5 Elemente **mit Zurücklegen** (es kann sich etwas wiederholen).
- `rng.choice(werte, size=5, replace=False)`: 5 **verschiedene** Elemente (ohne Zurücklegen), wie beim Lotto.
- `rng.choice(werte, size=n, p=[...])`: mit **Wahrscheinlichkeiten** `p` für die einzelnen Elemente. Sie müssen zusammen 1 ergeben.
- Ist `werte` eine ganze Zahl `n`, wird aus `0, 1, ..., n - 1` gewählt.''',
     """import numpy as np

rng = np.random.default_rng(3)
farben = ['rot', 'grün', 'blau']
print(rng.choice(farben))
print(rng.choice(farben, size=5))
print(rng.choice(10, size=4, replace=False))
print(rng.choice(['Gewinn', 'Niete'], size=6, p=[0.1, 0.9]))""")
expl('''#### Mischen: `permutation()` und `shuffle()`

- `rng.permutation(a)` gibt ein **neues**, zufällig gemischtes Array zurück. `a` bleibt unverändert.
  `rng.permutation(n)` mischt die Zahlen `0` bis `n - 1`.
- `rng.shuffle(a)` mischt das Array `a` selbst und gibt nichts zurück.''',
     """import numpy as np

rng = np.random.default_rng(5)
a = np.arange(1, 9)
print(rng.permutation(a))
print(a)
rng.shuffle(a)
print(a)
print(rng.permutation(5))""")

N = "\nnamen = ['Anna', 'Ben', 'Cem', 'Dana', 'Emil', 'Fia']"
t('Wähle zufällig eine Person aus `namen` aus, die heute die Tafel putzt.',
  NP + N, """rng = np.random.default_rng()
print(rng.choice(namen))""", kind='free')
t('Wähle mit `rng.choice(namen, size=3, replace=False)` drei verschiedene Personen für eine Gruppe aus.',
  rng(1) + N, """print(rng.choice(namen, size=3, replace=False))""")
t('Wähle mit `rng.choice(namen, size=8)` acht Personen **mit Zurücklegen** aus (z. B. wer an acht Tagen anfängt) und gib aus, wie oft jede Person vorkommt. Verwende `np.unique()` mit `return_counts=True`.',
  rng(2) + N, """auswahl = rng.choice(namen, size=8)
print(auswahl)
werte, anzahl = np.unique(auswahl, return_counts=True)
for w, n in zip(werte, anzahl):
    print(w, n)""")
t('Ziehe mit `rng.choice(np.arange(1, 50), size=6, replace=False)` die Lottozahlen 6 aus 49 und gib sie sortiert aus.',
  rng(49), """lotto = rng.choice(np.arange(1, 50), size=6, replace=False)
print(np.sort(lotto))""")
t('''Ein Glücksrad hat die Felder `Hauptgewinn` (Wahrscheinlichkeit 0.05), `Trostpreis` (0.25) und `Niete` (0.7).
Drehe es mit `rng.choice(felder, size=20, p=wahrscheinlichkeiten)` zwanzigmal und gib aus, wie oft es auf `Niete` stehen blieb.''',
  rng(13) + "\nfelder = ['Hauptgewinn', 'Trostpreis', 'Niete']\nwahrscheinlichkeiten = [0.05, 0.25, 0.7]",
  """drehungen = rng.choice(felder, size=20, p=wahrscheinlichkeiten)
print((drehungen == 'Niete').sum())""")
t('Mische die Reihenfolge der Vorträge mit `rng.permutation(namen)` und gib sie nummeriert aus.',
  rng(30) + N, """for i, name in enumerate(rng.permutation(namen), 1):
    print(i, name)""")
t('Mische das Array `karten` mit `rng.shuffle()` und gib es aus.',
  rng(4) + "\nkarten = np.array(['7', '8', '9', '10', 'B', 'D', 'K', 'A'])",
  """rng.shuffle(karten)
print(karten)""")
t('''Teile die sechs Personen zufällig in drei Zweiergruppen ein: Mische sie mit `rng.permutation(namen)` und forme das Ergebnis
mit `reshape(3, 2)` um. Gib die Gruppen Zeile für Zeile aus.''',
  rng(8) + N, """gruppen = rng.permutation(namen).reshape(3, 2)
for g in gruppen:
    print(g)""")
t('''Erzeuge ein zufälliges Passwort aus 10 Zeichen: Wähle sie mit `rng.choice(zeichen, size=10)` und verbinde sie mit `''.join()`.''',
  rng(99) + "\nzeichen = list('abcdefghijkmnpqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ23456789')",
  """print(''.join(rng.choice(zeichen, size=10)))""")
t('Erzeuge 10000 Würfe eines gezinkten Würfels, bei dem die 6 mit Wahrscheinlichkeit 0.5 fällt und jede andere Zahl mit 0.1. Gib den Anteil der Sechsen aus.',
  NP, """rng = np.random.default_rng()
w = rng.choice([1, 2, 3, 4, 5, 6], size=10000, p=[0.1, 0.1, 0.1, 0.1, 0.1, 0.5])
print((w == 6).mean())""", kind='free')
predict("""import numpy as np
rng = np.random.default_rng()
a = np.array([1, 2, 3])
b = rng.permutation(a)
print(np.sort(b))
print(a)
print(rng.shuffle(a))
print(len(rng.choice(10, size=10, replace=False)))
print(len(np.unique(rng.choice(10, size=10, replace=False))))""")
predict("""import numpy as np
rng = np.random.default_rng()
print(rng.choice(5, size=6, replace=False))""", error=ValueError)

# ---------------------------------------------------------------- 4
sec('Kennzahlen der Statistik')
expl('''#### Lage: Mittelwert und Median

- `np.mean(a)` oder `a.mean()`: der **Mittelwert** (Durchschnitt).
- `np.median(a)`: der **Median**, also der Wert in der Mitte, wenn man die Werte sortiert. Bei einer geraden Anzahl ist es der
  Mittelwert der beiden mittleren Werte. Der Median wird von einzelnen Ausreißern kaum beeinflusst, der Mittelwert stark.''',
     """import numpy as np

gehalt = np.array([2100, 2300, 2500, 2400, 2200, 15000])
print(gehalt.mean())
print(np.median(gehalt))
print(np.median(np.array([3, 1, 2])))""")
expl('''#### Streuung: Spannweite, Varianz und Standardabweichung

- `np.ptp(a)`: die **Spannweite** (größter minus kleinster Wert, englisch *peak to peak*).
- `a.var()`: die **Varianz**, der Mittelwert der quadrierten Abweichungen vom Mittelwert.
- `a.std()`: die **Standardabweichung**, die Wurzel aus der Varianz. Sie hat dieselbe Einheit wie die Werte und
  gibt an, wie weit die Werte typischerweise vom Mittelwert entfernt sind.

numpy teilt bei der Varianz durch die Anzahl `n`. Für eine Stichprobe teilt man in der Statistik oft durch `n - 1`.
Das geht mit `a.std(ddof=1)`.''',
     """import numpy as np

a = np.array([2, 4, 4, 4, 5, 5, 7, 9])
print(np.ptp(a))
print(a.var())
print(a.std())
print(np.sqrt(((a - a.mean()) ** 2).mean()))
print(np.round(a.std(ddof=1), 3))""")
expl('''#### Quantile

`np.percentile(a, p)` ist der Wert, unter dem `p` Prozent der Werte liegen. `np.percentile(a, 50)` ist der Median.
Das **untere Quartil** ist `np.percentile(a, 25)`, das **obere Quartil** `np.percentile(a, 75)`.
Zwischen ihnen liegt die mittlere Hälfte der Werte. Mit einer Liste bekommt man mehrere auf einmal.
Liegt ein Quantil zwischen zwei Werten, rechnet numpy einen Zwischenwert aus.''',
     """import numpy as np

a = np.array([1, 3, 4, 6, 7, 8, 9, 12, 15])
print(np.percentile(a, 50))
print(np.percentile(a, 25), np.percentile(a, 75))
print(np.percentile(a, [10, 90]))""")

D = NP + '\nzeiten = np.array([12.4, 11.9, 13.1, 12.0, 12.7, 14.8, 12.2, 11.6])'
t('Gib den Mittelwert und den Median der Laufzeiten aus (zwei Nachkommastellen).', D,
  """print(np.round(zeiten.mean(), 2))
print(np.round(np.median(zeiten), 2))""")
t('Gib die Spannweite der Laufzeiten aus (eine Nachkommastelle).', D, """print(np.round(np.ptp(zeiten), 1))""")
t('Gib die Varianz und die Standardabweichung der Laufzeiten aus (drei Nachkommastellen).', D,
  """print(np.round(zeiten.var(), 3))
print(np.round(zeiten.std(), 3))""")
t('Berechne die Standardabweichung ohne `std()`: Wurzel aus dem Mittelwert der quadrierten Abweichungen. Gib sie mit drei Nachkommastellen aus.', D,
  """print(np.round(np.sqrt(((zeiten - zeiten.mean()) ** 2).mean()), 3))""")
t('Gib das untere Quartil, den Median und das obere Quartil der Laufzeiten aus. Verwende `np.percentile()` mit einer Liste.', D,
  """print(np.percentile(zeiten, [25, 50, 75]))""")
t('Gib alle Laufzeiten aus, die mehr als eine Standardabweichung über dem Mittelwert liegen.', D,
  """print(zeiten[zeiten > zeiten.mean() + zeiten.std()])""")
t('Vergleiche Mittelwert und Median der Taschengelder. Gib beide aus und darunter die Differenz.',
  NP + '\ntaschengeld = np.array([20, 25, 15, 30, 20, 25, 200])',
  """m = taschengeld.mean()
med = np.median(taschengeld)
print(np.round(m, 2))
print(med)
print(np.round(m - med, 2))""")
t('''Zwei Klassen haben denselben Notendurchschnitt. Gib für beide den Mittelwert und die Standardabweichung (zwei Nachkommastellen) aus.''',
  NP + '\nklasse_a = np.array([3, 3, 2, 3, 4, 3, 3, 3])\nklasse_b = np.array([1, 5, 1, 4, 5, 1, 2, 5])',
  """print(klasse_a.mean(), np.round(klasse_a.std(), 2))
print(klasse_b.mean(), np.round(klasse_b.std(), 2))""")
t('Gib für jedes Fach (Spalte) den Median und die Standardabweichung (zwei Nachkommastellen) aus. Verwende `axis=0`.',
  NP + '\nnoten = np.array([[2, 3, 1],\n                  [4, 2, 3],\n                  [1, 2, 2],\n                  [3, 4, 3],\n                  [2, 1, 5]])',
  """print(np.median(noten, axis=0))
print(np.round(noten.std(axis=0), 2))""")
t('''Standardisiere die Laufzeiten: Ziehe den Mittelwert ab und teile durch die Standardabweichung (**z-Werte**).
Gib die z-Werte mit zwei Nachkommastellen aus und darunter, welche Laufzeit am stärksten abweicht (größter Betrag).''', D,
  """z = (zeiten - zeiten.mean()) / zeiten.std()
print(np.round(z, 2))
print(zeiten[np.abs(z).argmax()])""")
t('Gib den Interquartilsabstand der Laufzeiten aus (oberes minus unteres Quartil), gerundet auf drei Nachkommastellen.', D,
  """q1, q3 = np.percentile(zeiten, [25, 75])
print(np.round(q3 - q1, 3))""")
predict("""import numpy as np
a = np.array([1, 2, 3, 4, 100])
print(a.mean())
print(np.median(a))
print(np.median(np.array([1, 2, 3, 4])))
print(np.ptp(a))
print(np.array([5, 5, 5]).std())""")

# ---------------------------------------------------------------- 5
sec('Häufigkeiten und Histogramme')
expl('''#### `np.bincount()`

`np.bincount(a)` zählt für ganze Zahlen ab 0, wie oft jede vorkommt: An Index `k` steht die Anzahl der `k`.
Mit `minlength=n` ist das Ergebnis mindestens `n` lang, auch wenn große Werte gar nicht vorkommen.

Bei Würfeln steht an Index 0 die Anzahl der Nullen (immer 0). Mit `[1:]` schneidet man sie ab.
Teilt man durch die Anzahl, erhält man die **relativen Häufigkeiten**.''',
     """import numpy as np

wuerfe = np.array([3, 6, 1, 3, 6, 6, 2])
print(np.bincount(wuerfe))
print(np.bincount(wuerfe, minlength=7)[1:])
print(np.round(np.bincount(wuerfe, minlength=7)[1:] / len(wuerfe), 2))""")
expl('''#### `np.histogram()`

Bei Kommazahlen oder großen Bereichen fasst man Werte in **Klassen** zusammen (z. B. 0 bis 10, 10 bis 20, ...).
`np.histogram(a, bins=grenzen)` gibt **zwei** Arrays zurück: die Anzahlen und die Grenzen.
Jede Klasse enthält ihre linke Grenze, aber nicht die rechte. Nur die letzte Klasse enthält auch die rechte Grenze.

Mit `'*' * anzahl` kann man daraus ein einfaches Text-Diagramm zeichnen.''',
     """import numpy as np

punkte = np.array([12, 45, 67, 23, 89, 56, 34, 78, 90, 41, 66, 58])
anzahl, grenzen = np.histogram(punkte, bins=[0, 25, 50, 75, 100])
print(anzahl)
print(grenzen)
for i in range(len(anzahl)):
    print(f'{grenzen[i]:3d} bis {grenzen[i + 1]:3d}: ' + '*' * anzahl[i])""")

W = NP + '\nwuerfe = np.array([3, 6, 1, 4, 6, 2, 5, 1, 6, 3, 6, 4, 2, 6, 5])'
t('Gib mit `np.bincount()` aus, wie oft jede Zahl von 0 bis 6 gewürfelt wurde.', W, """print(np.bincount(wuerfe))""")
t('Gib die Häufigkeiten der Augenzahlen 1 bis 6 aus (ohne die 0).', W, """print(np.bincount(wuerfe, minlength=7)[1:])""")
t('Gib die relativen Häufigkeiten der Augenzahlen 1 bis 6 aus, gerundet auf zwei Nachkommastellen.', W,
  """print(np.round(np.bincount(wuerfe, minlength=7)[1:] / len(wuerfe), 2))""")
t('Gib die Augenzahl aus, die am häufigsten vorkam. Verwende `argmax()` auf dem Ergebnis von `np.bincount()`.', W,
  """print(np.bincount(wuerfe).argmax())""")
t('Gib für jede Augenzahl eine Zeile mit so vielen `*`, wie sie gewürfelt wurde, aus wie unten.', W,
  """h = np.bincount(wuerfe, minlength=7)
for zahl in range(1, 7):
    print(zahl, '*' * h[zahl])""")
t('Teile die Körpergrößen mit `np.histogram()` in die Klassen 150–160, 160–170, 170–180, 180–190 ein und gib die Anzahlen aus.',
  NP + '\ngroessen = np.array([162, 175, 158, 181, 169, 173, 177, 165, 188, 171, 159, 176])',
  """anzahl, grenzen = np.histogram(groessen, bins=[150, 160, 170, 180, 190])
print(anzahl)""")
t('Gib für die Körpergrößen ein Text-Histogramm aus wie unten.',
  NP + '\ngroessen = np.array([162, 175, 158, 181, 169, 173, 177, 165, 188, 171, 159, 176])',
  """anzahl, grenzen = np.histogram(groessen, bins=[150, 160, 170, 180, 190])
for i in range(len(anzahl)):
    print(f'{grenzen[i]}-{grenzen[i + 1]}: ' + '#' * anzahl[i])""")
t('''Erzeuge mit `rng.integers(1, 7, size=600)` sechshundert Würfe und gib die Häufigkeiten der Augenzahlen 1 bis 6 aus.''',
  rng(2024), """w = rng.integers(1, 7, size=600)
print(np.bincount(w, minlength=7)[1:])""")
t('''Erzeuge mit `rng.normal(100, 15, size=1000)` tausend Werte (z. B. IQ-Werte) und teile sie mit `np.histogram()` in die Klassen
40, 55, 70, 85, 100, 115, 130, 145, 160 ein. Gib ein Text-Histogramm mit einem `*` pro 10 Werte aus (ganzzahlige Division).''',
  rng(1), """werte = rng.normal(100, 15, size=1000)
grenzen = [40, 55, 70, 85, 100, 115, 130, 145, 160]
anzahl, g = np.histogram(werte, bins=grenzen)
for i in range(len(anzahl)):
    print(f'{grenzen[i]:3d} bis {grenzen[i + 1]:3d}: ' + '*' * (anzahl[i] // 10))""")
predict("""import numpy as np
a = np.array([0, 2, 2, 5])
print(np.bincount(a))
print(np.bincount(a, minlength=8))
anzahl, grenzen = np.histogram(np.array([1, 2, 3, 4]), bins=[0, 2, 4])
print(anzahl)""")

# ---------------------------------------------------------------- 6
sec('Simulationen')
expl('''#### Simulieren ohne Schleife

Statt in einer Schleife immer wieder zu würfeln, erzeugt man **alle** Würfe auf einmal als Array und wertet sie mit Masken aus.
Das ist kurz und auch bei einer Million Würfen schnell.

- Wahrscheinlichkeiten schätzt man mit dem Anteil: `(wuerfe == 6).mean()`.
- Mehrere Würfel pro Versuch: ein 2D-Array mit einer Zeile pro Versuch, dann z. B. `sum(axis=1)`.
- Für laufende Werte (Kontostand, Position, ...) verwendet man `cumsum()`.''',
     """import numpy as np

rng = np.random.default_rng(0)
wuerfe = rng.integers(1, 7, size=100000)
print((wuerfe == 6).mean())
zwei = rng.integers(1, 7, size=(100000, 2))
summen = zwei.sum(axis=1)
print((summen == 7).mean())
schritte = rng.choice([-1, 1], size=10)
print(schritte)
print(schritte.cumsum())""")

t('Simuliere 100000 Würfe und gib die relativen Häufigkeiten der Augenzahlen 1 bis 6 aus (drei Nachkommastellen). Sie sollten alle nahe bei 1/6 ≈ 0.167 liegen.',
  NP, """rng = np.random.default_rng()
w = rng.integers(1, 7, size=100000)
print(np.round(np.bincount(w, minlength=7)[1:] / len(w), 3))""", kind='free')
t('Simuliere mit `rng.integers(0, 2, size=100000)` hunderttausend Münzwürfe und gib den Anteil der Einsen aus.',
  rng(1), """m = rng.integers(0, 2, size=100000)
print(m.mean())""")
t('''Simuliere mit `rng.integers(1, 7, size=(100000, 2))` hunderttausend Würfe mit zwei Würfeln. Gib für jede Augensumme von 2 bis 12
die relative Häufigkeit aus (drei Nachkommastellen).''',
  rng(2), """s = rng.integers(1, 7, size=(100000, 2)).sum(axis=1)
print(np.round(np.bincount(s, minlength=13)[2:] / len(s), 3))""")
t('''Wie groß ist die Wahrscheinlichkeit, mit zwei Würfeln einen Pasch (zwei gleiche Zahlen) zu werfen?
Simuliere mit `rng.integers(1, 7, size=(100000, 2))` und gib den Anteil aus.''',
  rng(3), """w = rng.integers(1, 7, size=(100000, 2))
print((w[:, 0] == w[:, 1]).mean())""")
t('''Wie groß ist die Wahrscheinlichkeit, bei vier Würfen mindestens eine Sechs zu werfen?
Simuliere mit `rng.integers(1, 7, size=(100000, 4))` und gib den Anteil aus. (Der genaue Wert ist 1 - (5/6)⁴ ≈ 0.518.)''',
  rng(4), """w = rng.integers(1, 7, size=(100000, 4))
print((w == 6).any(axis=1).mean())""")
t('''**Gesetz der großen Zahlen:** Erzeuge mit `rng.integers(0, 2, size=1000)` tausend Münzwürfe. Berechne nach jedem Wurf den Anteil
der bisherigen Einsen (`cumsum()` geteilt durch `np.arange(1, 1001)`). Gib den Anteil nach 10, 100 und 1000 Würfen aus (drei Nachkommastellen).''',
  rng(5), """m = rng.integers(0, 2, size=1000)
anteil = m.cumsum() / np.arange(1, 1001)
print(np.round(anteil[[9, 99, 999]], 3))""")
t('''**Irrfahrt:** Eine Figur startet bei 0 und geht 20-mal zufällig einen Schritt nach links (-1) oder rechts (+1).
Erzeuge die Schritte mit `rng.choice([-1, 1], size=20)` und gib die Positionen nach jedem Schritt aus, danach die weiteste Entfernung von 0.''',
  rng(6), """pos = rng.choice([-1, 1], size=20).cumsum()
print(pos)
print(np.abs(pos).max())""")
t('''**Monte-Carlo-Schätzung von π:** Erzeuge mit `rng.random((100000, 2))` zufällige Punkte im Quadrat von 0 bis 1.
Der Anteil der Punkte im Viertelkreis (`x² + y² <= 1`) ist etwa π/4. Gib die Schätzung `4 * anteil` aus.''',
  rng(7), """p = rng.random((100000, 2))
im_kreis = (p[:, 0] ** 2 + p[:, 1] ** 2 <= 1)
print(4 * im_kreis.mean())""")
t('''**Geburtstagsproblem:** Wie wahrscheinlich ist es, dass in einer Klasse mit 23 Personen mindestens zwei am selben Tag Geburtstag haben?
Erzeuge mit `rng.integers(0, 365, size=(10000, 23))` 10000 Klassen. Sortiere jede Zeile mit `np.sort(..., axis=1)` und prüfe mit
`np.diff(..., axis=1) == 0`, ob zwei benachbarte Werte gleich sind. Gib den Anteil der Klassen mit doppeltem Geburtstag aus.''',
  rng(8), """g = np.sort(rng.integers(0, 365, size=(10000, 23)), axis=1)
doppelt = (np.diff(g, axis=1) == 0).any(axis=1)
print(doppelt.mean())""")
t('''Ein Basketballspieler trifft mit Wahrscheinlichkeit 0.7. Simuliere mit `rng.random((10000, 10)) < 0.7` 10000 Serien mit je 10 Würfen.
Gib aus, wie viele Treffer im Durchschnitt pro Serie erzielt wurden, und den Anteil der Serien mit mindestens 9 Treffern.''',
  rng(9), """treffer = (rng.random((10000, 10)) < 0.7).sum(axis=1)
print(treffer.mean())
print((treffer >= 9).mean())""")
t('''**Ziegenproblem:** Hinter einer von drei Türen ist ein Auto. Du wählst eine Tür. Der Moderator öffnet eine andere Tür mit einer Ziege.
Wer bei seiner Wahl bleibt, gewinnt genau dann, wenn die erste Wahl richtig war. Wer wechselt, gewinnt genau dann, wenn sie falsch war.
Simuliere mit `auto = rng.integers(0, 3, size=100000)` und danach `wahl = rng.integers(0, 3, size=100000)` und gib die Gewinnanteile
für „bleiben“ und „wechseln“ aus.''',
  rng(10), """auto = rng.integers(0, 3, size=100000)
wahl = rng.integers(0, 3, size=100000)
print((auto == wahl).mean())
print((auto != wahl).mean())""")
t('''Simuliere 10000 Spiele „Mensch ärgere dich nicht“-Start: Man darf bis zu dreimal würfeln und braucht eine Sechs.
Gib den Anteil der Spiele aus, in denen mindestens eine der drei Würfe eine Sechs ist. Vergleiche mit dem genauen Wert 1 - (5/6)³.''',
  NP, """rng = np.random.default_rng()
w = rng.integers(1, 7, size=(10000, 3))
print((w == 6).any(axis=1).mean())
print(1 - (5 / 6) ** 3)""", kind='free')
predict("""import numpy as np
rng = np.random.default_rng()
w = rng.integers(1, 7, size=(1000, 3))
print(w.shape)
print(w.sum(axis=1).min() >= 3)
print(w.sum(axis=1).max() <= 18)
print((w == 7).any())""")

# ---------------------------------------------------------------- 7
sec('Zusammenhänge: Korrelation')
expl('''#### Der Korrelationskoeffizient

Der **Korrelationskoeffizient** gibt an, wie stark zwei Größen zusammenhängen. Er liegt zwischen -1 und 1:

- nahe 1: Je größer die eine Größe, desto größer die andere (z. B. Lernzeit und Punkte).
- nahe -1: Je größer die eine, desto kleiner die andere.
- nahe 0: kein (linearer) Zusammenhang.

`np.corrcoef(x, y)` gibt eine 2 × 2-Tabelle zurück. Der Koeffizient steht an der Stelle `[0, 1]`.

Achtung: Ein Zusammenhang bedeutet nicht, dass das eine das andere **verursacht**.''',
     """import numpy as np

lernzeit = np.array([1, 2, 2, 3, 4, 5, 6])
punkte = np.array([40, 48, 55, 60, 70, 74, 85])
print(np.round(np.corrcoef(lernzeit, punkte), 3))
print(np.round(np.corrcoef(lernzeit, punkte)[0, 1], 3))""")

t('Gib den Korrelationskoeffizienten von Temperatur und verkauften Eisportionen aus (drei Nachkommastellen).',
  NP + '\ntemperatur = np.array([18, 22, 25, 28, 31, 20, 26])\neis = np.array([120, 160, 210, 260, 300, 140, 230])',
  """print(np.round(np.corrcoef(temperatur, eis)[0, 1], 3))""")
t('Gib den Korrelationskoeffizienten von Bildschirmzeit (Stunden) und Schlafdauer (Stunden) aus (drei Nachkommastellen).',
  NP + '\nbildschirm = np.array([1, 3, 5, 2, 6, 4, 7])\nschlaf = np.array([9.0, 8.5, 7.0, 8.0, 6.5, 7.5, 6.5])',
  """print(np.round(np.corrcoef(bildschirm, schlaf)[0, 1], 3))""")
t('Gib den Korrelationskoeffizienten von `x` und `y = 3 * x + 2` aus.',
  NP + '\nx = np.array([1, 4, 2, 8, 5])',
  """y = 3 * x + 2
print(np.round(np.corrcoef(x, y)[0, 1], 3))""")
t('''Erzeuge mit `x = rng.random(1000)` und danach `y = rng.random(1000)` zwei unabhängige Zufallsreihen und gib ihren Korrelationskoeffizienten aus (zwei Nachkommastellen).''',
  rng(11), """x = rng.random(1000)
y = rng.random(1000)
print(np.round(np.corrcoef(x, y)[0, 1], 2))""")
t('''Erzeuge mit `x = rng.normal(0, 1, size=1000)` und `rauschen = rng.normal(0, 1, size=1000)` Werte und setze `y = x + rauschen`.
Gib den Korrelationskoeffizienten von `x` und `y` aus (zwei Nachkommastellen).''',
  rng(12), """x = rng.normal(0, 1, size=1000)
rauschen = rng.normal(0, 1, size=1000)
y = x + rauschen
print(np.round(np.corrcoef(x, y)[0, 1], 2))""")
t('Gib für jedes Fach den Korrelationskoeffizienten zwischen Lernzeit und Note aus (zwei Nachkommastellen). Die Spalten von `noten` sind die Fächer.',
  NP + '\nlernzeit = np.array([2, 5, 1, 4, 3, 6])\nnoten = np.array([[3, 4],\n                  [1, 3],\n                  [4, 2],\n                  [2, 4],\n                  [3, 3],\n                  [1, 2]])',
  """for fach in range(noten.shape[1]):
    print(np.round(np.corrcoef(lernzeit, noten[:, fach])[0, 1], 2))""")
predict("""import numpy as np
x = np.array([1, 2, 3, 4])
print(np.round(np.corrcoef(x, x)[0, 1], 3))
print(np.round(np.corrcoef(x, -x)[0, 1], 3))
print(np.corrcoef(x, x * 10).shape)""")

# ---------------------------------------------------------------- 8
sec('Gemischte Übungen')
t('''Simuliere eine Klassenarbeit: Erzeuge mit `rng.choice([1, 2, 3, 4, 5, 6], size=28, p=[0.1, 0.25, 0.3, 0.2, 0.1, 0.05])` 28 Noten.
Gib den Notenspiegel (Anzahl jeder Note 1 bis 6), den Durchschnitt (zwei Nachkommastellen) und den Median aus.''',
  rng(28), """noten = rng.choice([1, 2, 3, 4, 5, 6], size=28, p=[0.1, 0.25, 0.3, 0.2, 0.1, 0.05])
print(np.bincount(noten, minlength=7)[1:])
print(np.round(noten.mean(), 2))
print(np.median(noten))""")
t('''**Kniffel:** Erzeuge mit `rng.integers(1, 7, size=(100000, 5))` 100000 Würfe mit fünf Würfeln. Ein Kniffel liegt vor, wenn alle
fünf Würfel gleich sind (Minimum gleich Maximum einer Zeile). Gib den Anteil aus und zum Vergleich den genauen Wert `6 / 6 ** 5`.''',
  rng(5), """w = rng.integers(1, 7, size=(100000, 5))
kniffel = w.min(axis=1) == w.max(axis=1)
print(kniffel.mean())
print(np.round(6 / 6 ** 5, 5))""")
t('''Mische ein Skatblatt mit 32 Karten (`rng.permutation(32)`) und verteile es an drei Personen (je 10 Karten) und den Skat (2 Karten):
Die ersten 30 Karten werden mit `reshape(3, 10)` verteilt, die letzten zwei sind der Skat. Gib die sortierten Hände und den Skat aus.''',
  rng(32), """blatt = rng.permutation(32)
haende = np.sort(blatt[:30].reshape(3, 10), axis=1)
print(haende)
print(np.sort(blatt[30:]))""")
t('''Ein Würfelspiel: Wer eine 6 würfelt, bekommt 5 Euro, sonst muss man 1 Euro zahlen. Lohnt sich das Spiel?
Simuliere mit `rng.integers(1, 7, size=100000)` und `np.where()` den Gewinn pro Spiel und gib den mittleren Gewinn aus (drei Nachkommastellen).''',
  rng(6), """w = rng.integers(1, 7, size=100000)
gewinn = np.where(w == 6, 5, -1)
print(np.round(gewinn.mean(), 3))""")
t('''Simuliere den Kontostand bei 50 Spielen aus der vorigen Aufgabe: Erzeuge die Würfe mit `rng.integers(1, 7, size=50)`.
Gib den Kontostand nach jedem 10. Spiel aus (Start bei 0) und den tiefsten Kontostand.''',
  rng(7), """w = rng.integers(1, 7, size=50)
stand = np.where(w == 6, 5, -1).cumsum()
print(stand[9::10])
print(stand.min())""")
t('''**Qualitätskontrolle:** Eine Maschine füllt Tüten mit 500 g, die Füllmenge ist normalverteilt mit Standardabweichung 4 g.
Erzeuge mit `rng.normal(500, 4, size=1000)` tausend Tüten. Gib den Mittelwert und die Standardabweichung (zwei Nachkommastellen) aus
und den Anteil der Tüten mit weniger als 492 g.''',
  rng(500), """tueten = rng.normal(500, 4, size=1000)
print(np.round(tueten.mean(), 2))
print(np.round(tueten.std(), 2))
print((tueten < 492).mean())""")
t('''Erzeuge mit `rng.integers(0, 2, size=(20, 20))` ein zufälliges 20 × 20-Feld aus Nullen und Einsen und gib es mit `#` für 1 und `.` für 0 aus.
Gib darunter den Anteil der Einsen aus.''',
  NP, """rng = np.random.default_rng()
feld = rng.integers(0, 2, size=(20, 20))
for zeile in np.where(feld == 1, '#', '.'):
    print(''.join(zeile))
print(feld.mean())""", kind='free')
t('''**Längste Serie:** Erzeuge mit `rng.integers(0, 2, size=30)` dreißig Münzwürfe und gib sie als Text aus (`K` für 1, `Z` für 0).
Finde die längste Serie gleicher Ergebnisse mit einer Schleife über die Würfe und gib ihre Länge aus.''',
  rng(30), """m = rng.integers(0, 2, size=30)
print(''.join(np.where(m == 1, 'K', 'Z')))
laengste = 1
aktuell = 1
for i in range(1, len(m)):
    if m[i] == m[i - 1]:
        aktuell += 1
    else:
        aktuell = 1
    if aktuell > laengste:
        laengste = aktuell
print(laengste)""")
t('''**Stichprobe:** In `population` stehen 10000 Körpergrößen. Ziehe mit `rng.choice(population, size=50, replace=False)` eine Stichprobe von 50 Personen.
Gib den Mittelwert der Population und den der Stichprobe aus (eine Nachkommastelle). Die Population wird mit `rng.normal(170, 9, size=10000)` erzeugt.''',
  rng(50), """population = rng.normal(170, 9, size=10000)
stichprobe = rng.choice(population, size=50, replace=False)
print(np.round(population.mean(), 1))
print(np.round(stichprobe.mean(), 1))""")
t('''Ziehe 1000-mal eine Stichprobe von 50 Personen aus der Population der vorigen Aufgabe und berechne jeweils den Mittelwert.
Gib die Standardabweichung dieser 1000 Mittelwerte aus. Sie ist viel kleiner als die der Population (etwa 9 / √50 ≈ 1.27).''',
  NP, """rng = np.random.default_rng()
population = rng.normal(170, 9, size=10000)
mittelwerte = []
for i in range(1000):
    mittelwerte.append(rng.choice(population, size=50, replace=False).mean())
print(np.array(mittelwerte).std())""", kind='free')
predict("""import numpy as np
rng = np.random.default_rng()
a = rng.permutation(np.arange(10))
print(np.sort(a))
print(a.sum())
print(np.median(a))
print(np.bincount(a))""")

generate('numpy_zufall_statistik', 'numpy: Zufall und Statistik', INTRO)
