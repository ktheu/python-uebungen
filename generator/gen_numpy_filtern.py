# Erzeugt ../content/numpy_filtern.ipynb (siehe nbgen.py).
#
# Braucht numpy in derselben Version wie Pyodide in JupyterLite (zurzeit 2.4.6), siehe gen_numpy_grundlagen.py:
#     py -3.13 -W error generator/gen_numpy_filtern.py
#
# Fallstricke (zusätzlich zu denen in gen_numpy_grundlagen.py):
# - argsort() ist bei gleichen Werten nicht stabil; lokal (SIMD-Sortierung) kann eine andere Reihenfolge herauskommen
#   als im Browser. In Aufgaben mit argsort() deshalb keine doppelten Werte.
# - mean() eines leeren Arrays gibt eine Warnung (mit -W error ein Fehler). Filter in Aufgaben nie leer mitteln.
from nbgen import sec, expl, task, predict, generate


def t(text, given='', body='', kind='normal'):
    """Aufgabe, deren Lösung aus dem vorgegebenen Code plus body besteht."""
    task(text, given=given, solution=(given + '\n' + body) if given else body, kind=kind)


NP = 'import numpy as np'

INTRO = '''In diesem Notebook geht es darum, aus einem numpy-Array **bestimmte Werte auszuwählen**: alle Werte über 10,
alle Personen mit mehr als 80 Punkten, die drei besten Zeiten, ... Das Werkzeug dafür sind **Masken**:
Arrays aus `True` und `False`, die angeben, welche Elemente man haben will. Mit ihnen braucht man dafür keine Schleife.

Vorausgesetzt wird das Notebook *numpy: Grundlagen*.

Jeder Abschnitt beginnt mit kurzen Erklärungen und Beispielen. Führe die Beispiele aus und probiere sie ruhig ein wenig aus.
Danach folgen viele kleine Übungen. Wenn etwas vorgegeben ist, steht es schon in der Codezelle.'''

# ---------------------------------------------------------------- 1
sec('Vergleiche und Bool-Arrays')
expl('''#### Vergleiche ergeben Bool-Arrays

Vergleicht man ein Array mit einer Zahl, wird **jedes** Element verglichen. Das Ergebnis ist ein Array aus
`True` und `False` (Datentyp `bool`), ein **Bool-Array**. Das geht mit `<`, `>`, `<=`, `>=`, `==` und `!=`.

Auch zwei gleich lange Arrays kann man elementweise vergleichen.''',
     """import numpy as np

a = np.array([3, 8, 1, 6, 10])
print(a > 5)
print(a == 1)
print(a % 2 == 0)
b = np.array([3, 7, 1, 9, 10])
print(a == b)""")
expl('''#### Zählen mit `sum()` und Anteile mit `mean()`

Beim Rechnen zählt `True` als 1 und `False` als 0. Deshalb gilt:

- `(a > 5).sum()` ist die **Anzahl** der Elemente, die größer als 5 sind.
- `(a > 5).mean()` ist der **Anteil** dieser Elemente (zwischen 0 und 1).

`np.array_equal(a, b)` prüft, ob zwei Arrays genau gleich sind, und gibt **ein** `True` oder `False` zurück.''',
     """import numpy as np

a = np.array([3, 8, 1, 6, 10])
print((a > 5).sum())
print((a > 5).mean())
print(np.array_equal(a, np.array([3, 8, 1, 6, 10])))
print(np.array_equal(a, np.array([3, 8, 1])))""")

A = NP + '\na = np.array([4, 15, 8, 23, 16, 42, 7])'
t('Gib ein Bool-Array aus, das angibt, welche Elemente von `a` größer als 10 sind.', A, """print(a > 10)""")
t('Gib ein Bool-Array aus, das angibt, welche Elemente von `a` gerade sind. Verwende den Modulo-Operator.', A, """print(a % 2 == 0)""")
t('Gib ein Bool-Array aus, das angibt, welche Elemente von `a` **nicht** gleich 8 sind.', A, """print(a != 8)""")
t('Gib aus, wie viele Elemente von `a` größer als 10 sind.', A, """print((a > 10).sum())""")
t('Gib aus, wie viele Elemente von `a` ungerade sind.', A, """print((a % 2 == 1).sum())""")
t('Gib den Anteil der Noten aus, die besser (kleiner) als 3 sind.',
  NP + '\nnoten = np.array([2, 3, 1, 4, 2, 5, 3, 2])',
  """print((noten < 3).mean())""")
t('Gib aus, an wie vielen Tagen es mindestens 20 Grad warm war.',
  NP + '\ntemperaturen = np.array([18, 21, 20, 25, 19, 17, 22])',
  """print((temperaturen >= 20).sum())""")
t('Vergleiche die Lösungen mit den richtigen Antworten. Gib das Bool-Array und die Anzahl der richtigen Antworten aus.',
  NP + "\nrichtig = np.array(['a', 'c', 'b', 'b', 'd', 'a'])\nantworten = np.array(['a', 'b', 'b', 'b', 'd', 'c'])",
  """print(antworten == richtig)
print((antworten == richtig).sum())""")
t('Gib aus, in wie vielen Spielen Team A mehr Tore geschossen hat als Team B.',
  NP + '\ntore_a = np.array([2, 0, 3, 1, 1, 4])\ntore_b = np.array([1, 0, 2, 3, 1, 2])',
  """print((tore_a > tore_b).sum())""")
t('Prüfe mit `np.array_equal()`, ob `a` sortiert gleich `b` ist. Verwende `np.sort(a)` (sortiert ein Array).',
  NP + '\na = np.array([3, 1, 2])\nb = np.array([1, 2, 3])',
  """print(np.array_equal(np.sort(a), b))""")
t('Gib aus, wie viele der Zahlen von 1 bis 100 durch 3 oder durch 5 teilbar sind. Tipp: Zähle die durch 3 teilbaren, die durch 5 teilbaren und ziehe die durch 15 teilbaren ab.',
  NP + '\nz = np.arange(1, 101)',
  """print((z % 3 == 0).sum() + (z % 5 == 0).sum() - (z % 15 == 0).sum())""")
predict("""import numpy as np
a = np.array([1, 2, 3, 4])
print(a >= 3)
print((a >= 3).sum())
print((a > 10).sum())
print((a == a).mean())
print(np.array([True, True, False]).sum())""")

# ---------------------------------------------------------------- 2
sec('Filtern mit Masken')
expl('''#### Masken

Gibt man ein Bool-Array gleicher Länge in eckigen Klammern an, erhält man nur die Elemente, bei denen `True` steht.
So ein Bool-Array heißt **Maske**. Meist schreibt man die Bedingung direkt in die Klammern:

`a[a > 5]` heißt „alle Elemente von `a`, die größer als 5 sind“.

Mit dem Ergebnis kann man weiterrechnen: `a[a > 5].sum()`, `a[a > 5].mean()`, `len(a[a > 5])`, ...
Erfüllt kein Element die Bedingung, entsteht ein leeres Array `[]`.''',
     """import numpy as np

a = np.array([3, 8, 1, 6, 10])
maske = a > 5
print(maske)
print(a[maske])
print(a[a > 5])
print(a[a % 2 == 0])
print(a[a > 5].sum())
print(a[a > 100])""")
expl('''#### Eine Maske für ein anderes Array

Gehören mehrere Arrays zusammen (gleiche Länge, gleiche Reihenfolge), kann man die Maske aus einem Array bilden
und auf ein anderes anwenden. `namen[punkte > 80]` sind die Namen der Personen mit mehr als 80 Punkten.
Dazu muss `namen` ein numpy-Array sein, keine Liste.''',
     """import numpy as np

namen = np.array(['Anna', 'Ben', 'Cem', 'Dana'])
punkte = np.array([78, 91, 85, 64])
print(namen[punkte > 80])
print(punkte[namen == 'Cem'])""")

t('Gib alle Elemente von `a` aus, die größer als 10 sind.', A, """print(a[a > 10])""")
t('Gib alle geraden Elemente von `a` aus.', A, """print(a[a % 2 == 0])""")
t('Gib alle Elemente von `a` aus, die kleiner oder gleich 8 sind.', A, """print(a[a <= 8])""")
t('Erstelle zuerst eine Maske `gross` für die Elemente größer als 15. Gib die Maske aus und danach die Elemente.', A,
  """gross = a > 15
print(gross)
print(a[gross])""")
t('Gib die Summe aller positiven Werte aus.',
  NP + '\nwerte = np.array([5, -3, 12, -8, 0, 7, -1])',
  """print(werte[werte > 0].sum())""")
t('Gib den Mittelwert der Noten aus, die besser (kleiner) als 4 sind, gerundet auf zwei Nachkommastellen.',
  NP + '\nnoten = np.array([2, 3, 1, 4, 2, 5, 3, 2])',
  """print(np.round(noten[noten < 4].mean(), 2))""")
t('Gib alle Zahlen von 1 bis 50 aus, die durch 7 teilbar sind. Verwende `np.arange()` und eine Maske.',
  NP, """z = np.arange(1, 51)
print(z[z % 7 == 0])""")
t('Gib alle Quadratzahlen von 1 bis 400 aus, die gerade sind.',
  NP, """q = np.arange(1, 21) ** 2
print(q[q % 2 == 0])""")
t('Gib alle Temperaturen unter dem Mittelwert aus.',
  NP + '\ntemperaturen = np.array([18, 21, 20, 25, 19, 17, 22])',
  """print(temperaturen[temperaturen < temperaturen.mean()])""")
t('Gib die Namen der Personen aus, die mehr als 80 Punkte haben.',
  NP + "\nnamen = np.array(['Anna', 'Ben', 'Cem', 'Dana', 'Emil'])\npunkte = np.array([78, 91, 85, 64, 80])",
  """print(namen[punkte > 80])""")
t('Gib die Punkte von `Dana` aus.',
  NP + "\nnamen = np.array(['Anna', 'Ben', 'Cem', 'Dana', 'Emil'])\npunkte = np.array([78, 91, 85, 64, 80])",
  """print(punkte[namen == 'Dana'])""")
t('Gib die Tage aus, an denen es geregnet hat (Regenmenge größer als 0), und darunter die gesamte Regenmenge.',
  NP + "\ntage = np.array(['Mo', 'Di', 'Mi', 'Do', 'Fr', 'Sa', 'So'])\nregen = np.array([0, 2.5, 0, 0, 8.0, 1.5, 0])",
  """print(tage[regen > 0])
print(regen[regen > 0].sum())""")
t('Gib die Artikel aus, die weniger als 2 Euro kosten.',
  NP + "\nartikel = np.array(['Brot', 'Milch', 'Käse', 'Apfel', 'Saft'])\npreise = np.array([2.49, 1.19, 3.99, 0.6, 1.79])",
  """print(artikel[preise < 2])""")
t('Gib alle Wörter aus, die länger als 4 Zeichen sind. Erstelle dazu mit einer List Comprehension ein Array der Längen.',
  NP + "\nwoerter = np.array(['Haus', 'Baum', 'Garten', 'Ei', 'Fenster', 'Tor'])",
  """laengen = np.array([len(w) for w in woerter])
print(woerter[laengen > 4])""")
t('Gib alle Messwerte aus, die mehr als 2 vom Mittelwert abweichen (nach oben oder unten). Verwende `np.abs()`.',
  NP + '\nmesswerte = np.array([10.2, 9.8, 13.5, 10.1, 6.9, 10.4])',
  """print(messwerte[np.abs(messwerte - messwerte.mean()) > 2])""")
predict("""import numpy as np
a = np.array([5, 2, 9, 4, 7])
print(a[a > 4])
print(a[a > 4].sum())
print(len(a[a > 100]))
print(a[[True, False, True, False, True]])
print(a[a % 2 == 1].max())""")

# ---------------------------------------------------------------- 3
sec('Bedingungen verknüpfen')
expl('''#### `&`, `|` und `~`

Bei Masken verknüpft man Bedingungen **nicht** mit `and`, `or` und `not`, sondern mit:

| Zeichen | Bedeutung |
|---|---|
| `&` | und |
| `\\|` | oder |
| `~` | nicht |

**Wichtig:** Um jede Bedingung gehören **Klammern**: `(a > 2) & (a < 8)`.
Ohne Klammern rechnet Python zuerst `2 & a` aus und es gibt einen Fehler.
Mit `and` gibt es ebenfalls einen Fehler, weil `and` nur ein einzelnes `True` oder `False` verarbeiten kann.''',
     """import numpy as np

a = np.arange(1, 11)
print(a[(a > 2) & (a < 8)])
print(a[(a < 3) | (a > 8)])
print(a[~(a % 2 == 0)])""")
expl('''#### `np.isin()`

`np.isin(a, werte)` gibt eine Maske zurück, die angibt, welche Elemente von `a` in `werte` vorkommen.
Das ist kürzer als viele Bedingungen mit `|`.''',
     """import numpy as np

a = np.array([3, 8, 1, 6, 10, 3])
print(np.isin(a, [1, 3, 5]))
print(a[np.isin(a, [1, 3, 5])])
print(a[~np.isin(a, [1, 3, 5])])
tiere = np.array(['Hund', 'Katze', 'Maus', 'Pferd'])
print(tiere[np.isin(tiere, ['Katze', 'Pferd'])])""")

Z = NP + '\nz = np.arange(1, 31)'
t('Gib alle Zahlen von `z` aus, die größer als 10 und kleiner als 20 sind.', Z, """print(z[(z > 10) & (z < 20)])""")
t('Gib alle Zahlen von `z` aus, die kleiner als 5 oder größer als 25 sind.', Z, """print(z[(z < 5) | (z > 25)])""")
t('Gib alle Zahlen von `z` aus, die durch 3 teilbar, aber **nicht** durch 2 teilbar sind.', Z,
  """print(z[(z % 3 == 0) & (z % 2 != 0)])""")
t('Gib mit `~` alle Zahlen von `z` aus, die **nicht** durch 5 teilbar sind und kleiner als 15 sind.', Z,
  """print(z[~(z % 5 == 0) & (z < 15)])""")
t('Gib alle Zahlen von `z` aus, die durch 4 oder durch 6 teilbar sind.', Z, """print(z[(z % 4 == 0) | (z % 6 == 0)])""")
t('Gib die Temperaturen aus, die zwischen 18 und 22 Grad liegen (beide Grenzen gehören dazu).',
  NP + '\ntemperaturen = np.array([15, 18, 24, 22, 19, 26, 21, 17])',
  """print(temperaturen[(temperaturen >= 18) & (temperaturen <= 22)])""")
t('Gib die Namen der Personen aus, die älter als 15 sind **und** mehr als 80 Punkte haben.',
  NP + "\nnamen = np.array(['Anna', 'Ben', 'Cem', 'Dana', 'Emil'])\nalter = np.array([16, 14, 17, 15, 16])\npunkte = np.array([78, 91, 85, 64, 88])",
  """print(namen[(alter > 15) & (punkte > 80)])""")
t('Gib die Namen der Personen aus, die jünger als 15 sind **oder** weniger als 70 Punkte haben.',
  NP + "\nnamen = np.array(['Anna', 'Ben', 'Cem', 'Dana', 'Emil'])\nalter = np.array([16, 14, 17, 15, 16])\npunkte = np.array([78, 91, 85, 64, 88])",
  """print(namen[(alter < 15) | (punkte < 70)])""")
t('Gib mit `np.isin()` alle Würfe aus, die eine 1 oder eine 6 sind, und danach ihre Anzahl.',
  NP + '\nwuerfe = np.array([3, 6, 1, 4, 6, 2, 5, 1, 6])',
  """treffer = wuerfe[np.isin(wuerfe, [1, 6])]
print(treffer)
print(len(treffer))""")
t('Gib mit `np.isin()` und `~` alle Buchstaben aus, die keine Vokale sind.',
  NP + "\nbuchstaben = np.array(list('informatik'))",
  """print(buchstaben[~np.isin(buchstaben, ['a', 'e', 'i', 'o', 'u'])])""")
t('Gib die Artikel aus, die zur Kategorie Obst oder Gemüse gehören und weniger als 2 Euro kosten.',
  NP + "\nartikel = np.array(['Apfel', 'Käse', 'Möhre', 'Banane', 'Brot', 'Paprika'])\nkategorie = np.array(['Obst', 'Milch', 'Gemüse', 'Obst', 'Back', 'Gemüse'])\npreise = np.array([0.6, 3.99, 0.4, 1.2, 2.49, 2.2])",
  """print(artikel[np.isin(kategorie, ['Obst', 'Gemüse']) & (preise < 2)])""")
t('Gib aus, wie viele Zahlen von 1 bis 1000 durch 7 teilbar sind, aber nicht durch 11.',
  NP, """z = np.arange(1, 1001)
print(((z % 7 == 0) & (z % 11 != 0)).sum())""")
predict("""import numpy as np
a = np.array([1, 2, 3, 4, 5, 6])
print(a[(a > 1) & (a < 5)])
print(a[(a == 1) | (a == 6)])
print(a[~(a > 2)])
print(np.isin(a, [2, 4]).sum())""")
predict("""import numpy as np
a = np.array([1, 2, 3, 4, 5, 6])
print(a[a > 1 & a < 5])""", error=ValueError)
predict("""import numpy as np
a = np.array([1, 2, 3, 4, 5, 6])
print(a[(a > 1) and (a < 5)])""", error=ValueError)

# ---------------------------------------------------------------- 4
sec('any(), all() und Indizes finden')
expl('''#### `any()`, `all()` und `np.count_nonzero()`

- `maske.any()`: Ist **mindestens ein** Element `True`?
- `maske.all()`: Sind **alle** Elemente `True`?
- `np.count_nonzero(maske)`: die Anzahl der `True`-Werte (wie `maske.sum()`).

Statt `maske.any()` kann man auch `np.any(maske)` schreiben.''',
     """import numpy as np

noten = np.array([2, 3, 1, 4, 2])
print((noten == 1).any())
print((noten == 6).any())
print((noten <= 4).all())
print(np.count_nonzero(noten == 2))""")
expl('''#### An welchen Stellen? `np.flatnonzero()`

`np.flatnonzero(maske)` gibt die **Indizes** zurück, an denen die Maske `True` ist.
Das erste davon ist die erste Stelle, an der die Bedingung erfüllt ist.''',
     """import numpy as np

a = np.array([3, 8, 1, 6, 10])
print(np.flatnonzero(a > 5))
print(np.flatnonzero(a > 5)[0])
tage = np.array(['Mo', 'Di', 'Mi', 'Do', 'Fr'])
print(tage[np.flatnonzero(a > 5)])""")

N = NP + '\nnoten = np.array([2, 3, 1, 4, 2, 5, 3, 2])'
t('Prüfe, ob es mindestens eine 1 gibt.', N, """print((noten == 1).any())""")
t('Prüfe, ob es eine 6 gibt.', N, """print((noten == 6).any())""")
t('Prüfe, ob alle bestanden haben (Note 4 oder besser).', N, """print((noten <= 4).all())""")
t('Gib mit `np.count_nonzero()` aus, wie oft die Note 2 vorkommt.', N, """print(np.count_nonzero(noten == 2))""")
t('Gib die Indizes aller Noten aus, die schlechter als 3 sind.', N, """print(np.flatnonzero(noten > 3))""")
t('Gib den Index der ersten Note aus, die schlechter als 3 ist.', N, """print(np.flatnonzero(noten > 3)[0])""")
t('Gib `alle positiv` aus, wenn alle Werte größer als 0 sind, sonst `nicht alle positiv`.',
  NP + '\nwerte = np.array([3, 7, 1, 9, 0, 4])',
  """if (werte > 0).all():
    print('alle positiv')
else:
    print('nicht alle positiv')""")
t('Gib `Frost` aus, wenn es an mindestens einem Tag unter 0 Grad war, sonst `kein Frost`.',
  NP + '\ntemperaturen = np.array([3, 1, -2, 0, 4, 5, -1])',
  """if (temperaturen < 0).any():
    print('Frost')
else:
    print('kein Frost')""")
t('Gib aus, an welchen Tagen es Frost gab (unter 0 Grad). Verwende `np.flatnonzero()` oder eine Maske.',
  NP + "\ntage = np.array(['Mo', 'Di', 'Mi', 'Do', 'Fr', 'Sa', 'So'])\ntemperaturen = np.array([3, 1, -2, 0, 4, 5, -1])",
  """print(tage[temperaturen < 0])""")
t('Das Sparschwein enthält nach jeder Woche die angegebene Summe. Gib aus, in welcher Woche (Index + 1) zum ersten Mal mindestens 100 Euro drin waren.',
  NP + '\nstand = np.array([15, 32, 48, 70, 95, 101, 120, 140])',
  """print(np.flatnonzero(stand >= 100)[0] + 1)""")
t('Prüfe, ob die Zahlen aufsteigend sortiert sind: Alle Differenzen benachbarter Zahlen müssen größer oder gleich 0 sein.',
  NP + '\na = np.array([1, 3, 3, 7, 12, 15])',
  """print((np.diff(a) >= 0).all())""")
t('Gib die Indizes aller Stellen aus, an denen der Wert größer ist als der vorherige. Tipp: `np.flatnonzero(np.diff(a) > 0) + 1`.',
  NP + '\na = np.array([5, 7, 6, 6, 9, 3, 4])',
  """print(np.flatnonzero(np.diff(a) > 0) + 1)""")
predict("""import numpy as np
a = np.array([0, 2, 0, 5])
print((a > 0).any())
print((a > 0).all())
print(np.count_nonzero(a > 0))
print(np.flatnonzero(a == 0))
print(np.flatnonzero(a > 10))""")

# ---------------------------------------------------------------- 5
sec('Werte ersetzen und np.where()')
expl('''#### Werte über eine Maske ändern

Mit einer Maske kann man auch **zuweisen**: `a[a < 0] = 0` setzt alle negativen Werte auf 0.
Auch `a[a > 10] *= 2` usw. funktioniert. Dabei wird `a` selbst verändert.

Achtung: Anders als ein Slice ist `a[maske]` (ohne Zuweisung) eine **Kopie**.
Ändert man `b = a[a > 5]`, ändert sich `a` nicht.''',
     """import numpy as np

a = np.array([5, -3, 12, -8, 0, 7])
a[a < 0] = 0
print(a)
a[a > 6] *= 10
print(a)
b = a[a > 0]
b[0] = 999
print(a)
print(b)""")
expl('''#### `np.where()`

`np.where(bedingung, wert_wenn_wahr, wert_wenn_falsch)` erzeugt ein **neues** Array:
An jeder Stelle steht der erste Wert, wenn die Bedingung dort `True` ist, sonst der zweite.
Die Werte können Zahlen, Zeichenketten oder Arrays gleicher Länge sein.

Mehrere Fälle schachtelt man: `np.where(a < 0, 'negativ', np.where(a == 0, 'null', 'positiv'))`.''',
     """import numpy as np

a = np.array([5, -3, 12, -8, 0, 7])
print(np.where(a < 0, 0, a))
print(np.where(a % 2 == 0, 'gerade', 'ungerade'))
print(np.where(a < 0, 'negativ', np.where(a == 0, 'null', 'positiv')))
print(a)""")

t('Setze alle negativen Werte auf 0 und gib das Array aus.',
  NP + '\nwerte = np.array([4, -2, 7, -9, 3, -1])',
  """werte[werte < 0] = 0
print(werte)""")
t('Begrenze alle Werte über 100 auf 100 (mit einer Maske, nicht mit `np.clip()`). Gib das Array aus.',
  NP + '\npunkte = np.array([95, 102, 87, 130, 100, 64])',
  """punkte[punkte > 100] = 100
print(punkte)""")
t('Verdopple alle geraden Zahlen in `a`. Gib `a` aus.',
  NP + '\na = np.arange(1, 11)',
  """a[a % 2 == 0] *= 2
print(a)""")
t('Ersetze alle fehlenden Messwerte (`-1`) durch den Mittelwert der übrigen Werte. Gib das Array aus.',
  NP + '\nmesswerte = np.array([12.0, -1, 14.0, 13.0, -1, 11.0])',
  """mittel = messwerte[messwerte != -1].mean()
messwerte[messwerte == -1] = mittel
print(messwerte)""")
t('Gib mit `np.where()` für jede Note `bestanden` oder `nicht bestanden` aus (bestanden bis Note 4).',
  NP + '\nnoten = np.array([2, 5, 4, 1, 6, 3])',
  """print(np.where(noten <= 4, 'bestanden', 'nicht bestanden'))""")
t('Gib mit `np.where()` ein Array aus, in dem alle negativen Werte durch 0 ersetzt sind. `werte` selbst soll unverändert bleiben. Gib danach `werte` aus.',
  NP + '\nwerte = np.array([4, -2, 7, -9, 3, -1])',
  """print(np.where(werte < 0, 0, werte))
print(werte)""")
t('Gib mit `np.where()` die Beträge aller Werte aus, ohne `np.abs()` zu verwenden.',
  NP + '\nwerte = np.array([4, -2, 7, -9, 3, -1])',
  """print(np.where(werte < 0, -werte, werte))""")
t('Gib mit `np.where()` für jede Temperatur `kalt` (unter 10), `mild` (10 bis 19) oder `warm` (ab 20) aus.',
  NP + '\ntemperaturen = np.array([5, 12, 20, 9, 25, 18])',
  """print(np.where(temperaturen < 10, 'kalt', np.where(temperaturen < 20, 'mild', 'warm')))""")
t('Ab einem Einkaufswert von 50 Euro gibt es 10 % Rabatt. Gib mit `np.where()` die Endbeträge aus, gerundet auf zwei Nachkommastellen.',
  NP + '\nbetraege = np.array([30.0, 55.0, 49.99, 120.0, 50.0])',
  """print(np.round(np.where(betraege >= 50, betraege * 0.9, betraege), 2))""")
t('Erstelle mit `np.where()` aus den Zahlen 1 bis 15 ein Array für das Spiel Fizz Buzz: durch 3 teilbar → `Fizz`, durch 5 → `Buzz`, durch beide → `FizzBuzz`, sonst die Zahl als Zeichenkette.',
  NP + '\nz = np.arange(1, 16)',
  """print(np.where(z % 15 == 0, 'FizzBuzz',
               np.where(z % 3 == 0, 'Fizz',
                        np.where(z % 5 == 0, 'Buzz', z.astype(str)))))""")
t('Gib mit `np.where()` für jedes Spiel `S`, `U` oder `N` aus (Sieg, Unentschieden, Niederlage für Team A).',
  NP + '\ntore_a = np.array([2, 0, 3, 1, 1, 4])\ntore_b = np.array([1, 0, 2, 3, 1, 2])',
  """print(np.where(tore_a > tore_b, 'S', np.where(tore_a == tore_b, 'U', 'N')))""")
t('Berechne die Punkte aus Aufgabe 5.11: Sieg 3, Unentschieden 1, Niederlage 0. Gib die Punkte und die Summe aus.',
  NP + '\ntore_a = np.array([2, 0, 3, 1, 1, 4])\ntore_b = np.array([1, 0, 2, 3, 1, 2])',
  """punkte = np.where(tore_a > tore_b, 3, np.where(tore_a == tore_b, 1, 0))
print(punkte)
print(punkte.sum())""")
predict("""import numpy as np
a = np.array([1, 2, 3, 4])
b = a[a > 2]
b[:] = 0
print(a)
a[a > 2] = 0
print(a)
print(np.where(a == 0, 9, a))
print(a)""")

# ---------------------------------------------------------------- 6
sec('Auswahl mit Indexlisten')
expl('''#### Mehrere Elemente auf einmal auswählen

Gibt man eine **Liste von Indizes** (oder ein Array mit Indizes) in eckigen Klammern an, erhält man genau diese Elemente
in dieser Reihenfolge. Indizes dürfen negativ sein und sich wiederholen.
Auch zuweisen geht: `a[[0, 2]] = 0`.

Wie bei Masken ist das Ergebnis eine **Kopie**.''',
     """import numpy as np

a = np.array([10, 20, 30, 40, 50])
print(a[[0, 2, 4]])
print(a[[4, 0, -2]])
print(a[[1, 1, 1]])
idx = np.array([3, 1])
print(a[idx])
a[[0, 2]] = 0
print(a)""")

B = NP + "\nbuchstaben = np.array(['a', 'b', 'c', 'd', 'e', 'f', 'g'])"
t('Gib das erste, dritte und fünfte Element von `buchstaben` aus.', B, """print(buchstaben[[0, 2, 4]])""")
t('Gib das letzte, das erste und das zweitletzte Element von `buchstaben` aus.', B, """print(buchstaben[[-1, 0, -2]])""")
t("Setze aus `buchstaben` mit einer Indexliste das Wort `fade` zusammen. Verbinde die Buchstaben mit `''.join()`.", B,
  """print(''.join(buchstaben[[5, 0, 3, 4]]))""")
t('Gib das Element mit Index 2 dreimal hintereinander aus (als Array).', B, """print(buchstaben[[2, 2, 2]])""")
t('Setze die Elemente mit Index 1 und 3 auf `x` und gib `buchstaben` aus.', B,
  """buchstaben[[1, 3]] = 'x'
print(buchstaben)""")
t('Gib die Temperaturen von Montag, Mittwoch und Freitag aus (Index 0, 2, 4).',
  NP + '\ntemperaturen = np.array([14, 17, 12, 19, 21, 16, 11])',
  """print(temperaturen[[0, 2, 4]])""")
t('Gib die Namen in der Reihenfolge aus, die in `reihenfolge` steht.',
  NP + "\nnamen = np.array(['Anna', 'Ben', 'Cem', 'Dana'])\nreihenfolge = np.array([2, 0, 3, 1])",
  """print(namen[reihenfolge])""")
t('Übersetze die Zahlen in Wörter: Verwende `zahlen` als Indizes für `woerter`.',
  NP + "\nwoerter = np.array(['null', 'eins', 'zwei', 'drei', 'vier'])\nzahlen = np.array([3, 0, 4, 4, 1])",
  """print(woerter[zahlen])""")
t('Würfelergebnisse 1 bis 6 sollen als Augenzahl-Symbole erscheinen. Verwende `wuerfe - 1` als Indizes.',
  NP + "\nsymbole = np.array(['⚀', '⚁', '⚂', '⚃', '⚄', '⚅'])\nwuerfe = np.array([6, 2, 3, 6, 1])",
  """print(symbole[wuerfe - 1])""")
t('Gib die Summe der Elemente an den Indizes in `idx` aus.',
  NP + '\na = np.array([5, 3, 8, 1, 9, 2])\nidx = [0, 2, 4]',
  """print(a[idx].sum())""")
predict("""import numpy as np
a = np.array([7, 8, 9])
print(a[[2, 1, 0]])
print(a[[0, 0, 2, 2]])
b = a[[0, 1]]
b[0] = 0
print(a)
print(a[np.array([1, 2])].sum())""")
predict("""import numpy as np
a = np.array([7, 8, 9])
print(a[[0, 3]])""", error=IndexError)

# ---------------------------------------------------------------- 7
sec('Sortieren und argsort()')
expl('''#### `np.sort()` und `sort()`

- `np.sort(a)` gibt ein **neues**, aufsteigend sortiertes Array zurück. `a` bleibt unverändert.
- `a.sort()` sortiert `a` selbst und gibt nichts zurück.
- Absteigend sortiert man mit `np.sort(a)[::-1]`.

Zeichenketten werden alphabetisch sortiert (Großbuchstaben vor Kleinbuchstaben, Umlaute ganz hinten).''',
     """import numpy as np

a = np.array([3, 8, 1, 6, 10])
print(np.sort(a))
print(np.sort(a)[::-1])
print(a)
a.sort()
print(a)
print(np.sort(np.array(['Cem', 'anna', 'Ben', 'Özge'])))""")
expl('''#### `argsort()`

`a.argsort()` sortiert nicht die Werte, sondern gibt die **Indizes** in der Reihenfolge zurück, in der man die Werte
lesen müsste, um sie sortiert zu bekommen. Damit kann man ein **anderes** Array in dieselbe Reihenfolge bringen:
`namen[punkte.argsort()]` sind die Namen sortiert nach Punkten.

- `a.argsort()[::-1]` liefert die Indizes absteigend sortiert.
- `a.argsort()[::-1][:3]` sind die Indizes der drei größten Werte.''',
     """import numpy as np

namen = np.array(['Anna', 'Ben', 'Cem', 'Dana'])
punkte = np.array([78, 91, 85, 64])
reihenfolge = punkte.argsort()
print(reihenfolge)
print(punkte[reihenfolge])
print(namen[reihenfolge])
print(namen[punkte.argsort()[::-1]])""")

t('Gib die Zahlen aufsteigend sortiert aus.',
  NP + '\nzahlen = np.array([42, 7, 19, 3, 25, 11])',
  """print(np.sort(zahlen))""")
t('Gib die Zahlen absteigend sortiert aus.',
  NP + '\nzahlen = np.array([42, 7, 19, 3, 25, 11])',
  """print(np.sort(zahlen)[::-1])""")
t('Sortiere `zahlen` mit `sort()` selbst und gib das Array aus.',
  NP + '\nzahlen = np.array([42, 7, 19, 3, 25, 11])',
  """zahlen.sort()
print(zahlen)""")
t('Gib die drei kleinsten Zahlen aus.',
  NP + '\nzahlen = np.array([42, 7, 19, 3, 25, 11])',
  """print(np.sort(zahlen)[:3])""")
t('Gib die drei größten Zahlen aus, die größte zuerst.',
  NP + '\nzahlen = np.array([42, 7, 19, 3, 25, 11])',
  """print(np.sort(zahlen)[::-1][:3])""")
t('Gib die Namen alphabetisch sortiert aus.',
  NP + "\nnamen = np.array(['Mia', 'Leo', 'Emma', 'Ben', 'Lina'])",
  """print(np.sort(namen))""")
t('Gib mit `argsort()` die Indizes aus, mit denen man `zahlen` aufsteigend sortiert.',
  NP + '\nzahlen = np.array([42, 7, 19, 3, 25, 11])',
  """print(zahlen.argsort())""")
t('Gib die Namen sortiert nach der Zeit aus, die schnellste (kleinste) zuerst.',
  NP + "\nnamen = np.array(['Anna', 'Ben', 'Cem', 'Dana', 'Emil'])\nzeiten = np.array([12.4, 11.9, 13.1, 12.0, 12.7])",
  """print(namen[zeiten.argsort()])""")
t('Gib die Namen der drei Personen mit den meisten Punkten aus, die beste zuerst.',
  NP + "\nnamen = np.array(['Anna', 'Ben', 'Cem', 'Dana', 'Emil', 'Fia'])\npunkte = np.array([78, 91, 85, 64, 88, 72])",
  """print(namen[punkte.argsort()[::-1][:3]])""")
t('Gib eine Rangliste aus wie unten: Platz, Name und Punkte, die beste Person zuerst.',
  NP + "\nnamen = np.array(['Anna', 'Ben', 'Cem', 'Dana', 'Emil', 'Fia'])\npunkte = np.array([78, 91, 85, 64, 88, 72])",
  """reihenfolge = punkte.argsort()[::-1]
for platz, i in enumerate(reihenfolge, 1):
    print(platz, namen[i], punkte[i])""")
t('Gib den Median aus: Sortiere die Werte und nimm den mittleren (die Anzahl ist ungerade).',
  NP + '\nwerte = np.array([7, 2, 9, 4, 5, 1, 8])',
  """s = np.sort(werte)
print(s[len(s) // 2])""")
t('Gib die Artikel sortiert nach Preis aus, den teuersten zuerst, und daneben die sortierten Preise.',
  NP + "\nartikel = np.array(['Brot', 'Milch', 'Käse', 'Apfel', 'Saft'])\npreise = np.array([2.49, 1.19, 3.99, 0.6, 1.79])",
  """r = preise.argsort()[::-1]
print(artikel[r])
print(preise[r])""")
predict("""import numpy as np
a = np.array([30, 10, 20])
print(a.argsort())
print(np.sort(a))
print(a)
print(a.sort())
print(a)""")

# ---------------------------------------------------------------- 8
sec('Eindeutige Werte und Häufigkeiten')
expl('''#### `np.unique()`

`np.unique(a)` gibt alle **verschiedenen** Werte von `a` sortiert zurück, jeden nur einmal.

Mit `return_counts=True` bekommt man zusätzlich, wie oft jeder Wert vorkommt. Dann gibt `np.unique()` **zwei** Arrays zurück,
die man auf zwei Variablen verteilt:

`werte, anzahl = np.unique(a, return_counts=True)`''',
     """import numpy as np

wuerfe = np.array([3, 6, 1, 3, 6, 6, 2])
print(np.unique(wuerfe))
werte, anzahl = np.unique(wuerfe, return_counts=True)
print(werte)
print(anzahl)
for w, n in zip(werte, anzahl):
    print(w, 'kommt', n, 'mal vor')""")

W = NP + '\nwuerfe = np.array([3, 6, 1, 4, 6, 2, 5, 1, 6, 3, 6, 4])'
t('Gib alle verschiedenen Augenzahlen aus, die gewürfelt wurden.', W, """print(np.unique(wuerfe))""")
t('Gib aus, wie viele verschiedene Augenzahlen gewürfelt wurden.', W, """print(len(np.unique(wuerfe)))""")
t('Gib für jede Augenzahl aus, wie oft sie gewürfelt wurde, wie unten.', W,
  """werte, anzahl = np.unique(wuerfe, return_counts=True)
for w, n in zip(werte, anzahl):
    print(f'{w}: {n}')""")
t('Gib die Augenzahl aus, die am häufigsten gewürfelt wurde. Verwende `argmax()` auf den Häufigkeiten.', W,
  """werte, anzahl = np.unique(wuerfe, return_counts=True)
print(werte[anzahl.argmax()])""")
t('Gib alle verschiedenen Noten aus und darunter, wie oft sie vorkommen.',
  NP + '\nnoten = np.array([2, 3, 1, 4, 2, 5, 3, 2, 2, 3])',
  """werte, anzahl = np.unique(noten, return_counts=True)
print(werte)
print(anzahl)""")
t('Gib alle Städte aus, aus denen die Personen kommen, jede nur einmal und alphabetisch.',
  NP + "\nstaedte = np.array(['Köln', 'Berlin', 'Münster', 'Köln', 'Berlin', 'Aachen'])",
  """print(np.unique(staedte))""")
t('Gib die Buchstaben des Wortes aus, jeden nur einmal, und darunter, wie oft sie vorkommen.',
  NP + "\nbuchstaben = np.array(list('mississippi'))",
  """werte, anzahl = np.unique(buchstaben, return_counts=True)
print(werte)
print(anzahl)""")
t('Gib alle Werte aus, die mehr als einmal vorkommen.',
  NP + '\na = np.array([4, 7, 4, 1, 9, 7, 7, 3])',
  """werte, anzahl = np.unique(a, return_counts=True)
print(werte[anzahl > 1])""")
t('Gib die Wörter aus, die genau einmal vorkommen.',
  NP + "\nwoerter = np.array('der hund und der ball und die katze'.split())",
  """werte, anzahl = np.unique(woerter, return_counts=True)
print(werte[anzahl == 1])""")
t('Erstelle aus `np.unique()` mit `zip()` und `dict()` ein Dictionary Note → Anzahl. Wandle die Werte vorher mit `tolist()` in normale Zahlen um. Gib das Dictionary aus.',
  NP + '\nnoten = np.array([2, 3, 1, 4, 2, 5, 3, 2, 2, 3])',
  """werte, anzahl = np.unique(noten, return_counts=True)
print(dict(zip(werte.tolist(), anzahl.tolist())))""")
predict("""import numpy as np
a = np.array([5, 1, 5, 5, 2])
print(np.unique(a))
werte, anzahl = np.unique(a, return_counts=True)
print(anzahl)
print(anzahl.sum() == len(a))
print(np.unique(np.array(['b', 'a', 'b'])))""")

# ---------------------------------------------------------------- 9
sec('Gemischte Übungen')
K = NP + """
namen = np.array(['Anna', 'Ben', 'Cem', 'Dana', 'Emil', 'Fia', 'Gus', 'Hana'])
klasse = np.array(['9a', '9b', '9a', '9b', '9a', '9a', '9b', '9b'])
punkte = np.array([78, 91, 85, 64, 88, 72, 59, 95])"""
t('Gib die Namen aller Personen aus der Klasse 9a aus.', K, """print(namen[klasse == '9a'])""")
t('Gib den Punktedurchschnitt der Klasse 9a und der Klasse 9b aus.', K,
  """print(punkte[klasse == '9a'].mean())
print(punkte[klasse == '9b'].mean())""")
t('Gib den Namen der besten Person aus der Klasse 9b aus.', K,
  """namen_b = namen[klasse == '9b']
punkte_b = punkte[klasse == '9b']
print(namen_b[punkte_b.argmax()])""")
t('''Gib die Note jeder Person aus: ab 90 Punkten 1, ab 80 Punkten 2, ab 70 Punkten 3, ab 60 Punkten 4, sonst 5.
Verwende geschachtelte `np.where()`.''', K,
  """noten = np.where(punkte >= 90, 1, np.where(punkte >= 80, 2, np.where(punkte >= 70, 3, np.where(punkte >= 60, 4, 5))))
print(noten)""")
t('Gib aus, wie viele Personen in jeder Klasse mehr als 75 Punkte haben.', K,
  """print(((klasse == '9a') & (punkte > 75)).sum())
print(((klasse == '9b') & (punkte > 75)).sum())""")
t('Gib die Namen der Personen aus, die über dem Gesamtdurchschnitt liegen, sortiert nach Punkten (die beste zuerst).', K,
  """gut = punkte > punkte.mean()
n = namen[gut]
p = punkte[gut]
print(n[p.argsort()[::-1]])""")
t('''Werte die Messreihe aus: Entferne alle ungültigen Werte (kleiner als 0 oder größer als 50).
Gib die gültigen Werte, ihre Anzahl und ihren Mittelwert aus (eine Nachkommastelle).''',
  NP + '\nmessungen = np.array([21.5, -999, 23.0, 22.4, 87.0, 20.9, -1, 24.2])',
  """gueltig = messungen[(messungen >= 0) & (messungen <= 50)]
print(gueltig)
print(len(gueltig))
print(np.round(gueltig.mean(), 1))""")
t('Gib alle Primzahlen bis 50 aus. Erstelle dazu eine Maske mit einer List Comprehension und einer Funktion `ist_prim(n)`.',
  NP,
  """def ist_prim(n):
    if n < 2:
        return False
    for teiler in range(2, n):
        if n % teiler == 0:
            return False
    return True

z = np.arange(1, 51)
maske = np.array([ist_prim(n) for n in z])
print(z[maske])""")
t('''Siebe die Primzahlen bis 50 mit dem **Sieb des Eratosthenes**: Beginne mit einem Bool-Array `prim` aus 51 Werten `True`.
Setze `prim[0]` und `prim[1]` auf `False`. Setze dann für jedes `i` von 2 bis 7 alle Vielfachen ab `i * i` auf `False`
(mit dem Slice `prim[i * i::i]`). Gib am Ende `np.flatnonzero(prim)` aus.''',
  NP,
  """prim = np.full(51, True)
prim[0] = False
prim[1] = False
for i in range(2, 8):
    if prim[i]:
        prim[i * i::i] = False
print(np.flatnonzero(prim))""")
t('Gib die Längen der Wörter aus und darunter die Wörter, die die größte Länge haben (es können mehrere sein).',
  NP + "\nwoerter = np.array(['Haus', 'Garten', 'Ei', 'Fenster', 'Balkon', 'Treppe', 'Dachboden', 'Kinderzimmer', 'Wohnzimmer', 'Schlafzimmer'])",
  """laengen = np.array([len(w) for w in woerter])
print(laengen)
print(woerter[laengen == laengen.max()])""")
t('''Ein Spiel speichert für jede Runde die Punkte. Gib aus, in wie vielen Runden es mehr Punkte gab als in der Runde davor.
Gib danach die Rundennummern (ab 1 gezählt) aus, in denen ein neuer Rekord (mehr als in allen Runden davor) aufgestellt wurde.
Tipp: `np.maximum.accumulate(a)` ist das laufende Maximum.''',
  NP + '\nrunden = np.array([10, 14, 12, 18, 18, 25, 20, 30])',
  """print((np.diff(runden) > 0).sum())
bisher = np.maximum.accumulate(runden)
print(np.flatnonzero(runden[1:] > bisher[:-1]) + 2)""")
t('Ersetze in den Noten jede 6 durch 5 und jede 0 (nicht teilgenommen) durch den Notendurchschnitt der übrigen Noten (gerundet auf eine ganze Note). Gib das Array aus.',
  NP + '\nnoten = np.array([2, 6, 3, 0, 1, 4, 6, 0])',
  """noten[noten == 6] = 5
schnitt = np.round(noten[noten != 0].mean())
noten[noten == 0] = schnitt
print(noten)""")
predict("""import numpy as np
a = np.array([4, 9, 2, 9, 5])
print(a[a == a.max()])
print(np.flatnonzero(a == a.max()))
print(np.where(a > 4, a, 0).sum())
print(np.unique(a)[::-1])
print(a[a.argsort()[:2]])""")

generate('numpy_filtern', 'numpy: Filtern und Auswählen', INTRO)
