# Erzeugt ../content/numpy_2d.ipynb (siehe nbgen.py).
#
# Braucht numpy in derselben Version wie Pyodide in JupyterLite (zurzeit 2.4.6), siehe gen_numpy_grundlagen.py:
#     py -3.13 -W error generator/gen_numpy_2d.py
#
# Fallstricke (zusätzlich zu denen in gen_numpy_grundlagen.py und gen_numpy_filtern.py):
# - np.unravel_index() liefert ein Tupel aus numpy-Zahlen -> (np.int64(1), np.int64(2)). Immer auspacken: z, s = ...
# - Matrizenmultiplikation (@) kommt erst in numpy_mathe.
from nbgen import sec, expl, task, predict, generate


def t(text, given='', body='', kind='normal'):
    """Aufgabe, deren Lösung aus dem vorgegebenen Code plus body besteht."""
    task(text, given=given, solution=(given + '\n' + body) if given else body, kind=kind)


NP = 'import numpy as np'

INTRO = '''Ein **zweidimensionales Array** ist eine Tabelle aus Zeilen und Spalten, wie ein Grid aus Listen von Listen.
Damit kann man Spielfelder, Notentabellen, Messreihen über mehrere Tage oder Bilder (Pixel) darstellen.
numpy macht die Arbeit damit viel bequemer: Ganze Zeilen und Spalten auswählen, Zeilen- und Spaltensummen berechnen,
alle Felder auf einmal ändern, ... geht ohne verschachtelte Schleifen.

Vorausgesetzt werden die Notebooks *numpy: Grundlagen* und *numpy: Filtern und Auswählen*.
Hilfreich ist auch das Notebook *Zweidimensionale Listen (Grids)*.

Jeder Abschnitt beginnt mit kurzen Erklärungen und Beispielen. Führe die Beispiele aus und probiere sie ruhig ein wenig aus.
Danach folgen viele kleine Übungen. Wenn etwas vorgegeben ist, steht es schon in der Codezelle.'''

M = NP + '''
m = np.array([[ 1,  2,  3,  4],
              [ 5,  6,  7,  8],
              [ 9, 10, 11, 12]])'''

# ---------------------------------------------------------------- 1
sec('2D-Arrays erstellen')
expl('''#### Aus einer Liste von Listen

`np.array(liste_von_listen)` macht aus einem Grid ein zweidimensionales Array. Jede innere Liste ist eine **Zeile**.
Alle Zeilen müssen gleich lang sein.

- `a.shape` ist jetzt ein Tupel `(zeilen, spalten)`.
- `a.ndim` ist 2, `a.size` ist die Anzahl aller Elemente.
- `len(a)` ist die Anzahl der **Zeilen**.

`print()` gibt das Array Zeile für Zeile aus.''',
     """import numpy as np

a = np.array([[1, 2, 3],
              [4, 5, 6]])
print(a)
print(a.shape)
print(a.ndim, a.size, len(a))""")
expl('''#### Arrays mit fester Form erzeugen

Bei `zeros()`, `ones()` und `full()` gibt man statt einer Zahl ein Tupel `(zeilen, spalten)` an:

- `np.zeros((3, 4))`: 3 Zeilen, 4 Spalten voller Nullen
- `np.full((2, 5), 7)`: 2 Zeilen, 5 Spalten voller 7
- `np.eye(n)`: eine `n` × `n`-**Einheitsmatrix**, mit 1 auf der Diagonalen und sonst 0

Auf die doppelten Klammern achten: `np.zeros((3, 4))`.''',
     """import numpy as np

print(np.zeros((3, 4)))
print(np.ones((2, 3), dtype=int))
print(np.full((2, 5), 7))
print(np.full((2, 3), '.'))
print(np.eye(3, dtype=int))""")
expl('''#### Mit `reshape()` umformen

`a.reshape(zeilen, spalten)` bringt die Elemente in eine neue Form. Die Anzahl der Elemente muss gleich bleiben.
Zusammen mit `np.arange()` erzeugt man so schnell durchnummerierte Grids. Die Elemente werden Zeile für Zeile verteilt.''',
     """import numpy as np

print(np.arange(12).reshape(3, 4))
print(np.arange(1, 7).reshape(2, 3))""")

t('Erstelle aus `grid` ein Array und gib es aus.',
  NP + '\ngrid = [[3, 1, 4], [1, 5, 9], [2, 6, 5]]',
  """a = np.array(grid)
print(a)""")
t('Gib `shape`, `ndim`, `size` und `len()` von `m` aus, jedes in einer eigenen Zeile.', M,
  """print(m.shape)
print(m.ndim)
print(m.size)
print(len(m))""")
t('Gib die Anzahl der Zeilen und die Anzahl der Spalten von `m` aus. Verwende `m.shape[0]` und `m.shape[1]`.', M,
  """print(m.shape[0])
print(m.shape[1])""")
t('Erstelle ein Array mit 4 Zeilen und 5 Spalten voller Nullen und gib es aus.', NP, """print(np.zeros((4, 5)))""")
t('Erstelle ein Array mit 3 Zeilen und 3 Spalten voller Einsen als ganze Zahlen und gib es aus.', NP, """print(np.ones((3, 3), dtype=int))""")
t('Erstelle ein Spielfeld mit 3 Zeilen und 6 Spalten, in dem überall `.` steht, und gib es aus.', NP, """print(np.full((3, 6), '.'))""")
t('Erstelle eine 4 × 4-Einheitsmatrix mit ganzen Zahlen und gib sie aus.', NP, """print(np.eye(4, dtype=int))""")
t('Erstelle mit `np.arange()` und `reshape()` ein Array mit den Zahlen 1 bis 12 in 3 Zeilen und 4 Spalten.', NP,
  """print(np.arange(1, 13).reshape(3, 4))""")
t('Erstelle mit `np.arange()` und `reshape()` ein Array mit den Zahlen 0 bis 19 in 4 Zeilen und 5 Spalten.', NP,
  """print(np.arange(20).reshape(4, 5))""")
t('Erstelle mit `np.arange()` und `reshape()` ein Array mit den Vielfachen von 10 von 10 bis 90 in 3 Zeilen und 3 Spalten.', NP,
  """print(np.arange(10, 100, 10).reshape(3, 3))""")
t('Erstelle aus den Zeichenketten mit `list()` ein Grid aus einzelnen Zeichen und gib es und seine Form aus.',
  NP + "\nzeilen = ['#..#', '.##.', '#..#']",
  """g = np.array([list(z) for z in zeilen])
print(g)
print(g.shape)""")
predict("""import numpy as np
a = np.arange(6).reshape(2, 3)
print(a)
print(a.shape)
print(len(a))
print(np.zeros((1, 2)))""")
predict("""import numpy as np
a = np.array([[1, 2, 3], [4, 5]])""", error=ValueError)

# ---------------------------------------------------------------- 2
sec('Elemente, Zeilen und Spalten')
expl('''#### Zugriff mit `a[z, s]`

- `a[z, s]` ist das Element in Zeile `z` und Spalte `s`. (`a[z][s]` wie bei Listen geht auch, ist aber langsamer.)
- `a[z]` ist die ganze **Zeile** `z` (ein eindimensionales Array).
- `a[:, s]` ist die ganze **Spalte** `s`. Der Doppelpunkt bedeutet „alle Zeilen“.
- Negative Indizes zählen von hinten: `a[-1]` ist die letzte Zeile, `a[:, -1]` die letzte Spalte.

Mit `=` kann man ein Element, eine ganze Zeile oder eine ganze Spalte ändern.''',
     """import numpy as np

m = np.array([[1, 2, 3, 4],
              [5, 6, 7, 8],
              [9, 10, 11, 12]])
print(m[1, 2])
print(m[1])
print(m[:, 2])
print(m[-1, -1])
m[0, 0] = 99
m[2] = 0
m[:, 1] = -1
print(m)""")

t('Gib das Element in Zeile 2, Spalte 1 von `m` aus.', M, """print(m[2, 1])""")
t('Gib das Element unten rechts von `m` aus. Verwende negative Indizes.', M, """print(m[-1, -1])""")
t('Gib die erste Zeile von `m` aus.', M, """print(m[0])""")
t('Gib die letzte Zeile von `m` aus.', M, """print(m[-1])""")
t('Gib die erste Spalte von `m` aus.', M, """print(m[:, 0])""")
t('Gib die dritte Spalte (Index 2) von `m` aus.', M, """print(m[:, 2])""")
t('Gib die Summe der zweiten Zeile (Index 1) von `m` aus.', M, """print(m[1].sum())""")
t('Gib den Mittelwert der letzten Spalte von `m` aus.', M, """print(m[:, -1].mean())""")
t('Setze das Element in der Mitte des Spielfelds auf `X` und gib das Feld aus.',
  NP + "\nfeld = np.full((3, 3), '.')",
  """feld[1, 1] = 'X'
print(feld)""")
t('Setze die erste Zeile von `m` auf 0 und gib `m` aus.', M, """m[0] = 0
print(m)""")
t('Setze die letzte Spalte von `m` auf 100 und gib `m` aus.', M, """m[:, -1] = 100
print(m)""")
t('Setze die zweite Spalte (Index 1) von `m` auf die Werte 7, 8 und 9 und gib `m` aus.', M,
  """m[:, 1] = [7, 8, 9]
print(m)""")
t('Verdopple alle Werte der ersten Zeile von `m` mit `*=` und gib `m` aus.', M, """m[0] *= 2
print(m)""")
t('Vertausche die erste und die letzte Zeile von `m`. Tipp: `m[[0, -1]] = m[[-1, 0]]`.', M,
  """m[[0, -1]] = m[[-1, 0]]
print(m)""")
t('Gib mit einer `for`-Schleife jede Zeile von `m` und ihre Summe aus wie unten.', M,
  """for zeile in m:
    print(zeile, zeile.sum())""")
predict("""import numpy as np
a = np.arange(9).reshape(3, 3)
print(a[1, 1])
print(a[2])
print(a[:, 0])
print(a[0][2])
print(a[-1, 0] + a[0, -1])""")

# ---------------------------------------------------------------- 3
sec('Teilbereiche ausschneiden')
expl('''#### Slicing in zwei Richtungen

In `a[zeilen, spalten]` kann man für Zeilen und Spalten jeweils ein Slice angeben:

- `a[0:2, 1:3]`: Zeilen 0 und 1, Spalten 1 und 2
- `a[:, :2]`: alle Zeilen, die ersten beiden Spalten
- `a[::2, ::2]`: jede zweite Zeile und jede zweite Spalte
- `a[::-1]`: die Zeilen in umgekehrter Reihenfolge, `a[:, ::-1]`: die Spalten umgekehrt

Einem Teilbereich kann man auch einen Wert zuweisen: `a[1:3, 1:3] = 0`.
Wie bei eindimensionalen Arrays ist ein Slice nur eine **Ansicht**. Für eine unabhängige Kopie braucht man `copy()`.''',
     """import numpy as np

a = np.arange(1, 17).reshape(4, 4)
print(a)
print(a[0:2, 1:3])
print(a[:, :2])
print(a[::2, ::2])
print(a[::-1])
a[1:3, 1:3] = 0
print(a)""")

G = NP + '\ng = np.arange(1, 26).reshape(5, 5)'
t('Gib die ersten beiden Zeilen von `g` aus.', G, """print(g[:2])""")
t('Gib die letzten beiden Spalten von `g` aus.', G, """print(g[:, -2:])""")
t('Gib den 2 × 2-Bereich oben links von `g` aus.', G, """print(g[:2, :2])""")
t('Gib den 3 × 3-Bereich in der Mitte von `g` aus (ohne den Rand).', G, """print(g[1:-1, 1:-1])""")
t('Gib jede zweite Zeile und jede zweite Spalte von `g` aus, beginnend oben links.', G, """print(g[::2, ::2])""")
t('Gib `g` mit umgekehrter Reihenfolge der Zeilen aus (oben und unten vertauscht).', G, """print(g[::-1])""")
t('Gib `g` gespiegelt aus: Die Spalten sollen in umgekehrter Reihenfolge stehen.', G, """print(g[:, ::-1])""")
t('Gib `g` um 180 Grad gedreht aus.', G, """print(g[::-1, ::-1])""")
t('Setze den Rand von `g` auf 0, das Innere bleibt. Setze dazu die erste und letzte Zeile und die erste und letzte Spalte einzeln.', G,
  """g[0] = 0
g[-1] = 0
g[:, 0] = 0
g[:, -1] = 0
print(g)""")
t('Setze den 3 × 3-Bereich in der Mitte von `g` auf -1 und gib `g` aus.', G, """g[1:-1, 1:-1] = -1
print(g)""")
t('Gib die Summe des 2 × 2-Bereichs unten rechts von `g` aus.', G, """print(g[-2:, -2:].sum())""")
t('Erstelle mit `np.zeros()` ein 8 × 8-Schachbrett aus 0 und 1: Setze mit zwei Slicing-Zuweisungen die Felder auf 1, bei denen Zeile und Spalte nicht beide gerade oder beide ungerade sind.', NP,
  """brett = np.zeros((8, 8), dtype=int)
brett[::2, 1::2] = 1
brett[1::2, ::2] = 1
print(brett)""")
t('Schneide aus `g` mit `copy()` den Bereich der ersten zwei Zeilen aus. Setze ihn auf 0. Gib den Bereich und danach `g` aus.', G,
  """teil = g[:2].copy()
teil[:] = 0
print(teil)
print(g)""")
predict("""import numpy as np
a = np.arange(1, 10).reshape(3, 3)
b = a[:2, :2]
b[:] = 0
print(a)
print(a[1:, 1:].sum())
print(a[::-1, 0])""")

# ---------------------------------------------------------------- 4
sec('Form ändern: reshape(), flatten() und T')
expl('''#### `reshape()`, `flatten()` und `T`

- `a.reshape(z, s)` gibt die Elemente in einer neuen Form zurück. Eine der Zahlen darf `-1` sein: Sie wird dann ausgerechnet.
  `a.reshape(-1, 2)` heißt also „zwei Spalten, so viele Zeilen wie nötig“.
- `a.flatten()` macht aus einem 2D-Array wieder ein eindimensionales Array (Zeile für Zeile).
- `a.T` ist das **transponierte** Array: Aus Zeilen werden Spalten und umgekehrt. Ein 2 × 3-Array wird zu einem 3 × 2-Array.

Passt die Anzahl der Elemente nicht zur neuen Form, gibt `reshape()` einen `ValueError`.''',
     """import numpy as np

a = np.arange(6).reshape(2, 3)
print(a)
print(a.reshape(3, 2))
print(a.reshape(-1, 2))
print(a.flatten())
print(a.T)
print(a.T.shape)""")

t('Forme `m` in ein Array mit 4 Zeilen und 3 Spalten um und gib es aus.', M, """print(m.reshape(4, 3))""")
t('Forme `m` in ein Array mit 2 Spalten um. Lass die Anzahl der Zeilen mit `-1` ausrechnen.', M, """print(m.reshape(-1, 2))""")
t('Forme `m` in ein Array mit einer einzigen Zeile um. Gib es und seine Form aus.', M,
  """z = m.reshape(1, -1)
print(z)
print(z.shape)""")
t('Mache aus `m` mit `flatten()` ein eindimensionales Array und gib es aus.', M, """print(m.flatten())""")
t('Gib `m` transponiert aus und darunter die Form des transponierten Arrays.', M, """print(m.T)
print(m.T.shape)""")
t('Die Messwerte stehen hintereinander, jeweils 3 pro Tag. Forme sie in ein Array mit einer Zeile pro Tag um und gib die Tagessummen aus (mit einer Schleife über die Zeilen).',
  NP + '\nwerte = np.array([4, 5, 3, 6, 6, 7, 2, 3, 2, 8, 7, 9])',
  """tage = werte.reshape(-1, 3)
print(tage)
for tag in tage:
    print(tag.sum())""")
t('Gib die Namen in einer Tabelle mit 3 Spalten aus: Forme dazu das Array um.',
  NP + "\nnamen = np.array(['Ali', 'Bea', 'Cem', 'Dana', 'Eli', 'Fia', 'Gus', 'Hana', 'Ida'])",
  """print(namen.reshape(-1, 3))""")
t('Prüfe, ob die Matrix symmetrisch ist, also gleich ihrer Transponierten. Verwende `==` und `all()`.',
  NP + '\na = np.array([[1, 7, 3],\n              [7, 4, 5],\n              [3, 5, 6]])',
  """print((a == a.T).all())""")
t('Drehe `m` um 90 Grad im Uhrzeigersinn: Kehre zuerst die Reihenfolge der Zeilen um und transponiere dann.', M,
  """print(m[::-1].T)""")
predict("""import numpy as np
a = np.arange(8)
print(a.reshape(2, -1))
print(a.reshape(2, 4).T)
print(a.reshape(4, 2).flatten())
print(a.reshape(-1, 4).shape)""")
predict("""import numpy as np
a = np.arange(10)
print(a.reshape(3, 3))""", error=ValueError)

# ---------------------------------------------------------------- 5
sec('Rechnen und Broadcasting')
expl('''#### Elementweise rechnen

Rechnen mit einer Zahl und mit einem Array **derselben Form** funktioniert wie bei eindimensionalen Arrays:
Jedes Element wird mit dem passenden Element gerechnet. Auch `np.sqrt()`, `np.round()` usw. funktionieren.''',
     """import numpy as np

a = np.array([[1, 2], [3, 4]])
b = np.array([[10, 20], [30, 40]])
print(a * 10)
print(a + b)
print(b / a)
print(a ** 2)""")
expl('''#### Broadcasting

Rechnet man ein 2D-Array mit einem eindimensionalen Array, das so lang ist wie eine **Zeile**, wird das eindimensionale Array
für **jede Zeile** verwendet. Das nennt man **Broadcasting**.

Will man stattdessen mit jeder **Spalte** rechnen, braucht man eine Spalte: ein Array der Form `(zeilen, 1)`.
Das bekommt man mit `reshape(-1, 1)`.

Rechnet man eine Spalte (Form `(n, 1)`) mit einer Zeile (Form `(k,)`), entsteht eine ganze Tabelle der Form `(n, k)`.''',
     """import numpy as np

a = np.array([[1, 2, 3],
              [4, 5, 6]])
print(a + np.array([10, 20, 30]))
print(a * np.array([10, 100]).reshape(-1, 1))

zeile = np.arange(1, 4)
spalte = np.arange(1, 5).reshape(-1, 1)
print(spalte)
print(spalte * zeile)""")

t('Multipliziere alle Elemente von `m` mit 3 und gib das Ergebnis aus.', M, """print(m * 3)""")
t('Addiere die beiden Arrays elementweise.',
  NP + '\na = np.array([[1, 2], [3, 4]])\nb = np.array([[5, 6], [7, 8]])',
  """print(a + b)""")
t('Ein Graustufenbild hat Helligkeitswerte von 0 bis 255. Erzeuge das Negativ (`255 - bild`) und gib es aus.',
  NP + '\nbild = np.array([[0, 50, 100], [150, 200, 255]])',
  """print(255 - bild)""")
t('Teile alle Werte von `m` durch den größten Wert von `m` und runde auf zwei Nachkommastellen.', M,
  """print(np.round(m / m.max(), 2))""")
t('Addiere zu jeder Zeile von `m` die Werte `[100, 200, 300, 400]` (Broadcasting).', M,
  """print(m + np.array([100, 200, 300, 400]))""")
t('Multipliziere die erste Zeile von `m` mit 1, die zweite mit 10 und die dritte mit 100. Verwende eine Spalte mit `reshape(-1, 1)`.', M,
  """print(m * np.array([1, 10, 100]).reshape(-1, 1))""")
t('''Die Tabelle enthält für jede Woche (Zeile) die verkauften Mengen von drei Produkten (Spalten).
Berechne mit Broadcasting die Umsätze, indem du jede Spalte mit dem Preis des Produkts multiplizierst.''',
  NP + '\nmengen = np.array([[3, 5, 2],\n                   [4, 1, 6],\n                   [2, 2, 2]])\npreise = np.array([1.5, 2.0, 4.0])',
  """print(mengen * preise)""")
t('Erzeuge mit Broadcasting das kleine Einmaleins als 10 × 10-Tabelle (eine Spalte 1 bis 10 mal eine Zeile 1 bis 10).', NP,
  """z = np.arange(1, 11)
print(z.reshape(-1, 1) * z)""")
t('Erzeuge mit Broadcasting eine 4 × 5-Tabelle, in der jedes Feld die Summe aus Zeilenindex und Spaltenindex enthält.', NP,
  """print(np.arange(4).reshape(-1, 1) + np.arange(5))""")
t('Erzeuge mit Broadcasting und dem Modulo-Operator ein 6 × 6-Schachbrett aus 0 und 1: `(zeile + spalte) % 2`.', NP,
  """print((np.arange(6).reshape(-1, 1) + np.arange(6)) % 2)""")
t('Ziehe von jeder Spalte von `m` ihren Mittelwert ab. Die Spaltenmittelwerte bekommst du mit `m.mean(axis=0)` (mehr dazu im nächsten Abschnitt).', M,
  """print(m - m.mean(axis=0))""")
predict("""import numpy as np
a = np.ones((2, 3), dtype=int)
print(a + np.array([1, 2, 3]))
print(a * np.array([5, 7]).reshape(-1, 1))
print(np.arange(3).reshape(-1, 1) * np.arange(3))""")
predict("""import numpy as np
a = np.ones((2, 3), dtype=int)
print(a + np.array([1, 2]))""", error=ValueError)

# ---------------------------------------------------------------- 6
sec('Auswerten mit axis')
expl('''#### Der Parameter `axis`

`sum()`, `mean()`, `min()`, `max()`, `argmin()` und `argmax()` rechnen ohne Angabe über **alle** Elemente.
Mit `axis` legt man fest, in welche Richtung zusammengefasst wird:

| Aufruf | Ergebnis |
|---|---|
| `a.sum()` | eine Zahl: Summe aller Elemente |
| `a.sum(axis=0)` | für jede **Spalte** eine Summe (es wird über die Zeilen hinweg addiert, also nach unten) |
| `a.sum(axis=1)` | für jede **Zeile** eine Summe (es wird über die Spalten hinweg addiert, also nach rechts) |

Merkhilfe: `axis=0` lässt die Zeilen verschwinden, `axis=1` die Spalten.''',
     """import numpy as np

a = np.array([[1, 2, 3],
              [4, 5, 6]])
print(a.sum())
print(a.sum(axis=0))
print(a.sum(axis=1))
print(a.max(axis=0))
print(a.mean(axis=1))
print(a.argmax(axis=1))""")
expl('''#### Wo liegt das Maximum? `np.unravel_index()`

`a.argmax()` ohne `axis` zählt die Elemente Zeile für Zeile durch und gibt **einen** Index zurück.
`np.unravel_index(index, a.shape)` rechnet ihn in Zeile und Spalte um. Man verteilt das Ergebnis auf zwei Variablen.''',
     """import numpy as np

a = np.array([[3, 8, 1],
              [9, 2, 7]])
print(a.argmax())
z, s = np.unravel_index(a.argmax(), a.shape)
print(z, s)""")

NT = NP + """
# Zeilen: Anna, Ben, Cem, Dana; Spalten: Mathe, Deutsch, Englisch, Informatik
noten = np.array([[2, 3, 1, 1],
                  [4, 2, 3, 2],
                  [1, 2, 2, 1],
                  [3, 4, 3, 2]])
namen = ['Anna', 'Ben', 'Cem', 'Dana']
faecher = ['Mathe', 'Deutsch', 'Englisch', 'Informatik']"""
t('Gib die Summe aller Elemente von `m` aus, darunter die Spaltensummen und darunter die Zeilensummen.', M,
  """print(m.sum())
print(m.sum(axis=0))
print(m.sum(axis=1))""")
t('Gib das größte Element jeder Zeile von `m` aus.', M, """print(m.max(axis=1))""")
t('Gib das kleinste Element jeder Spalte von `m` aus.', M, """print(m.min(axis=0))""")
t('Gib für jede Person den Notendurchschnitt aus.', NT, """print(noten.mean(axis=1))""")
t('Gib für jedes Fach den Notendurchschnitt aus.', NT, """print(noten.mean(axis=0))""")
t('Gib den Namen der Person mit dem besten (kleinsten) Durchschnitt aus.', NT, """print(namen[noten.mean(axis=1).argmin()])""")
t('Gib das Fach mit dem schlechtesten (größten) Durchschnitt aus.', NT, """print(faecher[noten.mean(axis=0).argmax()])""")
t('Gib für jede Person ihr bestes Fach aus (das erste mit der kleinsten Note), wie unten.', NT,
  """beste = noten.argmin(axis=1)
for i in range(len(namen)):
    print(namen[i], faecher[beste[i]])""")
t('Gib die schlechteste Note jeder Person aus.', NT, """print(noten.max(axis=1))""")
t('''Die Tabelle enthält für eine Woche (Zeilen Mo bis So) die Temperaturen um 8, 12, 16 und 20 Uhr (Spalten).
Gib die Tageshöchstwerte und den Mittelwert jeder Uhrzeit über die Woche aus (eine Nachkommastelle).''',
  NP + """
temp = np.array([[ 8, 14, 16, 11],
                 [ 7, 12, 15, 10],
                 [10, 17, 19, 13],
                 [ 9, 16, 18, 12],
                 [11, 18, 21, 15],
                 [12, 20, 22, 16],
                 [ 9, 13, 14, 10]])""",
  """print(temp.max(axis=1))
print(np.round(temp.mean(axis=0), 1))""")
t('Gib aus, in welcher Zeile und Spalte das größte Element von `a` steht. Verwende `np.unravel_index()`.',
  NP + '\na = np.array([[4, 9, 2],\n              [8, 1, 12],\n              [7, 3, 5]])',
  """z, s = np.unravel_index(a.argmax(), a.shape)
print(z, s)""")
t('Prüfe, ob `q` ein magisches Quadrat ist: Alle Zeilensummen, alle Spaltensummen und beide Diagonalsummen sind gleich. `np.diag(q)` ist die Hauptdiagonale, `np.diag(q[::-1])` die Nebendiagonale.',
  NP + '\nq = np.array([[2, 7, 6],\n              [9, 5, 1],\n              [4, 3, 8]])',
  """summe = q[0].sum()
zeilen_ok = (q.sum(axis=1) == summe).all()
spalten_ok = (q.sum(axis=0) == summe).all()
diag_ok = np.diag(q).sum() == summe and np.diag(q[::-1]).sum() == summe
print(zeilen_ok and spalten_ok and diag_ok)""")
t('Gib die Zeilensummen von `m` als Spalte aus (Form `(3, 1)`). Verwende `keepdims=True`: `m.sum(axis=1, keepdims=True)`.', M,
  """print(m.sum(axis=1, keepdims=True))""")
t('Berechne für jede Zeile von `m` die Anteile der Elemente an der Zeilensumme in Prozent, gerundet auf eine Nachkommastelle.', M,
  """print(np.round(m / m.sum(axis=1, keepdims=True) * 100, 1))""")
predict("""import numpy as np
a = np.array([[1, 5],
              [4, 2],
              [3, 6]])
print(a.sum(axis=0))
print(a.sum(axis=1))
print(a.argmax(axis=0))
print(a.argmax())
print(a.max(axis=1).min())""")

# ---------------------------------------------------------------- 7
sec('Masken und Bedingungen in 2D')
expl('''#### Masken in 2D

Vergleiche ergeben auch bei 2D-Arrays ein Bool-Array derselben Form. Damit kann man:

- zählen: `(a > 5).sum()`, auch pro Zeile oder Spalte mit `axis`
- filtern: `a[a > 5]` liefert die passenden Elemente als **eindimensionales** Array
- ändern: `a[a > 5] = 0`
- mit `np.where(a > 5, 'x', '.')` ein neues Array derselben Form bauen
- mit `np.argwhere(a > 5)` die Positionen `[zeile, spalte]` aller passenden Elemente bekommen''',
     """import numpy as np

a = np.array([[3, 8, 1],
              [9, 2, 7]])
print(a > 5)
print((a > 5).sum(axis=1))
print(a[a > 5])
print(np.where(a > 5, 'x', '.'))
print(np.argwhere(a > 5))""")
expl('''#### Ganze Zeilen auswählen

Eine Maske aus **einer Spalte** kann man verwenden, um ganze **Zeilen** auszuwählen:
`a[a[:, 0] > 5]` sind alle Zeilen, bei denen in der ersten Spalte ein Wert größer als 5 steht.

Mit `(a > 5).any(axis=1)` und `(a > 5).all(axis=1)` prüft man für jede Zeile, ob mindestens ein bzw. jedes Element passt.''',
     """import numpy as np

a = np.array([[3, 8, 1],
              [9, 2, 7],
              [6, 6, 6]])
print(a[a[:, 0] > 5])
print((a > 5).any(axis=1))
print(a[(a > 5).all(axis=1)])""")

t('Gib aus, wie viele Elemente von `m` gerade sind.', M, """print((m % 2 == 0).sum())""")
t('Gib alle Elemente von `m` aus, die größer als 6 sind.', M, """print(m[m > 6])""")
t('Gib für jede Zeile von `m` aus, wie viele Elemente größer als 6 sind.', M, """print((m > 6).sum(axis=1))""")
t('Setze alle ungeraden Elemente von `m` auf 0 und gib `m` aus.', M, """m[m % 2 == 1] = 0
print(m)""")
t('Gib mit `np.where()` ein Array aus, in dem bei geraden Zahlen von `m` ein `g` und bei ungeraden ein `u` steht.', M,
  """print(np.where(m % 2 == 0, 'g', 'u'))""")
t('Gib mit `np.argwhere()` die Positionen aller Zahlen in `m` aus, die durch 5 teilbar sind.', M, """print(np.argwhere(m % 5 == 0))""")
t('Gib die Positionen aller Schätze `S` auf der Karte aus, jede als `Zeile Spalte` in einer eigenen Zeile.',
  NP + "\nkarte = np.array([list('..S.'), list('S...'), list('...S')])",
  """for z, s in np.argwhere(karte == 'S'):
    print(z, s)""")
t('Gib aus, wie viele Personen in jedem Fach eine 1 haben.', NT, """print((noten == 1).sum(axis=0))""")
t('Gib die Namen der Personen aus, die in **keinem** Fach schlechter als 3 sind. Mache dazu aus `namen` ein Array.', NT,
  """print(np.array(namen)[(noten <= 3).all(axis=1)])""")
t('Gib die Zeilen der Notentabelle aus, bei denen in Mathe (Spalte 0) eine 1 oder 2 steht.', NT,
  """print(noten[noten[:, 0] <= 2])""")
t('Zähle die Wände `#` im Labyrinth: insgesamt und pro Zeile.',
  NP + "\nlabyrinth = np.array([list('#####'), list('#..##'), list('#.#.#'), list('#...#'), list('#####')])",
  """print((labyrinth == '#').sum())
print((labyrinth == '#').sum(axis=1))""")
t('''Ein Graustufenbild soll in Schwarz-Weiß umgewandelt werden: Werte ab 128 werden 255, alle anderen 0.
Gib das Ergebnis aus und darunter, wie viele Pixel weiß sind.''',
  NP + '\nbild = np.array([[ 12, 200, 130],\n                 [128,  90, 255],\n                 [ 60, 127, 180]])',
  """sw = np.where(bild >= 128, 255, 0)
print(sw)
print((sw == 255).sum())""")
predict("""import numpy as np
a = np.arange(6).reshape(2, 3)
print(a[a > 2])
print((a > 2).any(axis=1))
print((a > 2).all(axis=0))
print(np.where(a % 2 == 0, a, -1))""")

# ---------------------------------------------------------------- 8
sec('Arrays verbinden')
expl('''#### `np.vstack()`, `np.hstack()` und `np.concatenate()`

- `np.vstack([a, b])` stapelt Arrays **untereinander** (vertikal). Die Spaltenzahl muss passen.
- `np.hstack([a, b])` setzt Arrays **nebeneinander** (horizontal). Die Zeilenzahl muss passen.
- `np.concatenate([a, b], axis=0)` entspricht `vstack`, mit `axis=1` entspricht es `hstack`.

Mit `vstack` kann man auch eine einzelne Zeile (ein eindimensionales Array) unten anhängen.
Eine Spalte hängt man mit `hstack` an, nachdem man sie mit `reshape(-1, 1)` in eine Spalte verwandelt hat.''',
     """import numpy as np

a = np.array([[1, 2], [3, 4]])
b = np.array([[5, 6], [7, 8]])
print(np.vstack([a, b]))
print(np.hstack([a, b]))
print(np.vstack([a, np.array([9, 9])]))
print(np.hstack([a, np.array([0, 0]).reshape(-1, 1)]))""")

AB = NP + '\na = np.array([[1, 2, 3], [4, 5, 6]])\nb = np.array([[7, 8, 9], [10, 11, 12]])'
t('Stapele `a` und `b` untereinander und gib das Ergebnis und seine Form aus.', AB,
  """c = np.vstack([a, b])
print(c)
print(c.shape)""")
t('Setze `a` und `b` nebeneinander und gib das Ergebnis und seine Form aus.', AB,
  """c = np.hstack([a, b])
print(c)
print(c.shape)""")
t('Verbinde `a` und `b` mit `np.concatenate()` untereinander.', AB, """print(np.concatenate([a, b], axis=0))""")
t('Hänge an `a` unten die Zeile `[0, 0, 0]` an.', AB, """print(np.vstack([a, np.array([0, 0, 0])]))""")
t('Hänge an `a` rechts eine Spalte mit den Zeilensummen an.', AB,
  """print(np.hstack([a, a.sum(axis=1).reshape(-1, 1)]))""")
t('Hänge an `a` unten eine Zeile mit den Spaltensummen an.', AB, """print(np.vstack([a, a.sum(axis=0)]))""")
t('Baue aus den drei Messreihen (je ein Array) eine Tabelle mit einer Zeile pro Messreihe.',
  NP + '\nmo = np.array([3, 5, 4])\ndi = np.array([6, 2, 7])\nmi = np.array([4, 4, 5])',
  """print(np.vstack([mo, di, mi]))""")
t('Setze das Bild `b` zweimal nebeneinander und das Ergebnis zweimal untereinander (ein Kachelmuster).',
  NP + "\nb = np.array([list('#.'), list('.#')])",
  """zeile = np.hstack([b, b])
print(np.vstack([zeile, zeile]))""")
predict("""import numpy as np
a = np.zeros((1, 2), dtype=int)
b = np.ones((2, 2), dtype=int)
print(np.vstack([a, b]))
print(np.vstack([a, b]).shape)
print(np.hstack([b, b]).shape)""")

# ---------------------------------------------------------------- 9
sec('Spielfelder und Nachbarn')
expl('''#### Spielfelder ausgeben

Ein Spielfeld aus einzelnen Zeichen gibt man am schönsten Zeile für Zeile mit `''.join(zeile)` aus.

#### Diagonalen

`np.diag(a)` liefert die **Hauptdiagonale** (von oben links nach unten rechts).
Die **Nebendiagonale** (von oben rechts nach unten links) bekommt man mit `np.diag(a[:, ::-1])`.''',
     """import numpy as np

feld = np.array([list('X.O'),
                 list('.X.'),
                 list('O.X')])
for zeile in feld:
    print(''.join(zeile))
print(np.diag(feld))
print(np.diag(feld[:, ::-1]))""")
expl('''#### Nachbarn zählen mit `np.pad()`

Im Grids-Notebook hast du die Nachbarn eines Feldes mit einer Schleife und einer Randprüfung gezählt.
Mit numpy geht das für **alle Felder auf einmal**:

1. `np.pad(a, 1)` legt einen Rand aus Nullen um das Array. Dann hat jedes Feld acht Nachbarn.
2. Für jede der acht Richtungen schneidet man das verschobene Array aus und addiert alles.

Bei einem Feld der Größe `z` × `s` ist `p[0:z, 0:s]` das Array der Nachbarn oben links, `p[1:z+1, 2:s+2]` das der rechten
Nachbarn usw. In der Mitte `p[1:z+1, 1:s+1]` steht das ursprüngliche Array.''',
     """import numpy as np

a = np.array([[1, 0, 0],
              [0, 1, 1],
              [0, 0, 1]])
z, s = a.shape
p = np.pad(a, 1)
print(p)
nachbarn = np.zeros((z, s), dtype=int)
for dz in range(3):
    for ds in range(3):
        if dz != 1 or ds != 1:
            nachbarn += p[dz:dz + z, ds:ds + s]
print(nachbarn)""")

TTT = NP + "\nfeld = np.array([list('XOX'), list('OXO'), list('OXX')])"
t('Gib das Tic-Tac-Toe-Feld Zeile für Zeile mit `join()` aus.', TTT,
  """for zeile in feld:
    print(''.join(zeile))""")
t('Gib die Hauptdiagonale und die Nebendiagonale des Feldes aus.', TTT,
  """print(np.diag(feld))
print(np.diag(feld[:, ::-1]))""")
t('''Prüfe, ob `X` gewonnen hat: Eine Zeile, eine Spalte oder eine Diagonale besteht nur aus `X`.
Verwende `(feld == 'X').all(axis=1).any()` für die Zeilen und entsprechend für Spalten und Diagonalen.''', TTT,
  """x = feld == 'X'
gewonnen = (x.all(axis=1).any() or x.all(axis=0).any()
            or np.diag(x).all() or np.diag(x[:, ::-1]).all())
print(gewonnen)""")
t('Schreibe eine Funktion `gewinner(feld, spieler)`, die prüft, ob `spieler` gewonnen hat. Teste sie mit `X` und `O` an beiden Feldern.',
  NP + "\nfeld1 = np.array([list('XOX'), list('OXO'), list('OXX')])\nfeld2 = np.array([list('XOX'), list('XOO'), list('OOX')])",
  """def gewinner(feld, spieler):
    x = feld == spieler
    return bool(x.all(axis=1).any() or x.all(axis=0).any()
                or np.diag(x).all() or np.diag(x[:, ::-1]).all())

print(gewinner(feld1, 'X'), gewinner(feld1, 'O'))
print(gewinner(feld2, 'X'), gewinner(feld2, 'O'))""")
t('Lege mit `np.pad()` einen Rand aus Nullen um `a` und gib das Ergebnis aus.',
  NP + '\na = np.arange(1, 7).reshape(2, 3)',
  """print(np.pad(a, 1))""")
t('Lege mit `np.pad(a, 1, constant_values=9)` einen Rand aus Neunen um `a`.',
  NP + '\na = np.arange(1, 7).reshape(2, 3)',
  """print(np.pad(a, 1, constant_values=9))""")
t('''Zähle für jedes Feld, wie viele seiner vier **direkten** Nachbarn (oben, unten, links, rechts) eine 1 enthalten.
Lege dazu einen Rand um das Feld und addiere vier verschobene Ausschnitte.''',
  NP + '\na = np.array([[1, 0, 1],\n              [0, 1, 0],\n              [1, 1, 0]])',
  """z, s = a.shape
p = np.pad(a, 1)
print(p[0:z, 1:s + 1] + p[2:z + 2, 1:s + 1] + p[1:z + 1, 0:s] + p[1:z + 1, 2:s + 2])""")
t('''**Minesweeper:** Die Minen sind mit 1 markiert. Berechne für jedes Feld, wie viele der acht Nachbarfelder eine Mine enthalten.
Gib dann das Spielfeld aus: Minen als `*`, sonst die Anzahl. Verwende `np.where()` und `astype(str)`.''',
  NP + '\nminen = np.array([[0, 1, 0, 0],\n                  [0, 0, 0, 1],\n                  [1, 0, 0, 0]])',
  """z, s = minen.shape
p = np.pad(minen, 1)
anzahl = np.zeros((z, s), dtype=int)
for dz in range(3):
    for ds in range(3):
        if dz != 1 or ds != 1:
            anzahl += p[dz:dz + z, ds:ds + s]
feld = np.where(minen == 1, '*', anzahl.astype(str))
for zeile in feld:
    print(''.join(zeile))""")
t('''**Game of Life:** Berechne einen Schritt. Eine lebende Zelle (1) überlebt mit 2 oder 3 lebenden Nachbarn,
eine tote Zelle (0) wird mit genau 3 lebenden Nachbarn lebendig, alle anderen Zellen sind danach tot.
Gib das neue Feld mit `#` für lebende und `.` für tote Zellen aus.''',
  NP + '\nzellen = np.array([[0, 0, 0, 0, 0],\n                   [0, 0, 1, 0, 0],\n                   [0, 0, 1, 0, 0],\n                   [0, 0, 1, 0, 0],\n                   [0, 0, 0, 0, 0]])',
  """z, s = zellen.shape
p = np.pad(zellen, 1)
n = np.zeros((z, s), dtype=int)
for dz in range(3):
    for ds in range(3):
        if dz != 1 or ds != 1:
            n += p[dz:dz + z, ds:ds + s]
neu = ((zellen == 1) & ((n == 2) | (n == 3))) | ((zellen == 0) & (n == 3))
for zeile in np.where(neu, '#', '.'):
    print(''.join(zeile))""")
t('''Schreibe eine Funktion `schritt(zellen)` für das Game of Life, die das neue Feld als Array aus 0 und 1 zurückgibt.
Berechne damit vier Schritte des Gleiters und gib danach das Feld aus.''',
  NP + '\nzellen = np.zeros((6, 6), dtype=int)\nzellen[0, 1] = 1\nzellen[1, 2] = 1\nzellen[2, 0:3] = 1',
  """def schritt(zellen):
    z, s = zellen.shape
    p = np.pad(zellen, 1)
    n = np.zeros((z, s), dtype=int)
    for dz in range(3):
        for ds in range(3):
            if dz != 1 or ds != 1:
                n += p[dz:dz + z, ds:ds + s]
    neu = ((zellen == 1) & ((n == 2) | (n == 3))) | ((zellen == 0) & (n == 3))
    return neu.astype(int)

for i in range(4):
    zellen = schritt(zellen)
for zeile in np.where(zellen == 1, '#', '.'):
    print(''.join(zeile))""")
predict("""import numpy as np
a = np.array([[1, 2], [3, 4]])
print(np.diag(a))
print(np.diag(a[:, ::-1]))
print(np.pad(a, 1).shape)
print(np.pad(a, 1).sum())""")

# ---------------------------------------------------------------- 10
sec('Gemischte Übungen')
V = NP + """
# Zeilen: Filialen Nord, Süd, Ost; Spalten: Jan bis Jun
umsatz = np.array([[120, 135, 150, 160, 155, 170],
                   [ 90, 110, 105, 130, 140, 150],
                   [200, 180, 190, 210, 205, 220]])
filialen = ['Nord', 'Süd', 'Ost']"""
t('Gib den Gesamtumsatz jeder Filiale und den Gesamtumsatz jedes Monats aus.', V,
  """print(umsatz.sum(axis=1))
print(umsatz.sum(axis=0))""")
t('Gib die Filiale mit dem höchsten Gesamtumsatz aus.', V, """print(filialen[umsatz.sum(axis=1).argmax()])""")
t('Gib für jede Filiale die Veränderung von Monat zu Monat aus. Verwende `np.diff(umsatz, axis=1)`.', V,
  """print(np.diff(umsatz, axis=1))""")
t('Gib aus, wie viele Monate jede Filiale mehr als 150 umgesetzt hat.', V, """print((umsatz > 150).sum(axis=1))""")
t('Gib die Umsätze des zweiten Quartals (April bis Juni, Spalten 3 bis 5) aus und die Summe je Filiale.', V,
  """q2 = umsatz[:, 3:6]
print(q2)
print(q2.sum(axis=1))""")
t('Hänge an die Tabelle eine Spalte mit dem Halbjahresumsatz an und gib die Tabelle aus.', V,
  """print(np.hstack([umsatz, umsatz.sum(axis=1).reshape(-1, 1)]))""")
t('Gib aus, in welcher Filiale und welchem Monat (Index) der kleinste Umsatz war.', V,
  """z, s = np.unravel_index(umsatz.argmin(), umsatz.shape)
print(filialen[z], s)""")
t('''Erstelle eine Entfernungstabelle: Für die Punkte auf einer Linie soll das Feld `[i, j]` den Abstand `|x[i] - x[j]|` enthalten.
Verwende Broadcasting mit `x.reshape(-1, 1) - x`.''',
  NP + '\nx = np.array([0, 3, 7, 12])',
  """print(np.abs(x.reshape(-1, 1) - x))""")
t('''Erzeuge ein 5 × 5-Grid, in dem jedes Feld den Abstand zur Mitte in „Schritten“ enthält:
`|zeile - 2| + |spalte - 2|`. Verwende Broadcasting.''', NP,
  """i = np.arange(5)
print(np.abs(i.reshape(-1, 1) - 2) + np.abs(i - 2))""")
t('''Drucke einen Rahmen: Erstelle ein 5 × 9-Feld aus Leerzeichen, setze den Rand auf `#` und schreibe in die Mitte
`numpy` (die Buchstaben in Zeile 2, Spalten 2 bis 6). Gib das Feld Zeile für Zeile aus.''', NP,
  """feld = np.full((5, 9), ' ')
feld[0] = '#'
feld[-1] = '#'
feld[:, 0] = '#'
feld[:, -1] = '#'
feld[2, 2:7] = list('numpy')
for zeile in feld:
    print(''.join(zeile))""")
t('''Ein Bild aus Nullen und Einsen soll doppelt so groß werden: Jedes Pixel wird zu einem 2 × 2-Block.
Verwende `np.repeat(bild, 2, axis=0)` (wiederholt jede Zeile) und danach `np.repeat(..., 2, axis=1)` (jede Spalte).''',
  NP + '\nbild = np.array([[1, 0],\n                 [0, 1]])',
  """gross = np.repeat(np.repeat(bild, 2, axis=0), 2, axis=1)
print(gross)""")
t('''Die Punktetabelle enthält für jede Person (Zeile) die Punkte in vier Aufgaben (Spalten). Die maximal möglichen Punkte stehen in `maximal`.
Gib für jede Person den Prozentsatz der erreichten Punkte aus (eine Nachkommastelle) und die Namen der Personen mit mindestens 75 %.''',
  NP + "\npunkte = np.array([[8, 5, 9, 6],\n                   [4, 3, 7, 2],\n                   [10, 6, 10, 8],\n                   [7, 4, 6, 5]])\nmaximal = np.array([10, 6, 10, 8])\nnamen = np.array(['Ali', 'Bea', 'Cem', 'Dana'])",
  """prozent = punkte.sum(axis=1) / maximal.sum() * 100
print(np.round(prozent, 1))
print(namen[prozent >= 75])""")
t('''Berechne für jede Aufgabe, welcher Anteil der möglichen Punkte im Durchschnitt erreicht wurde (zwei Nachkommastellen).
Gib danach die Nummer (ab 1) der schwierigsten Aufgabe aus.''',
  NP + "\npunkte = np.array([[8, 5, 9, 6],\n                   [4, 3, 7, 2],\n                   [10, 6, 10, 8],\n                   [7, 4, 6, 5]])\nmaximal = np.array([10, 6, 10, 8])",
  """anteil = punkte.mean(axis=0) / maximal
print(np.round(anteil, 2))
print(anteil.argmin() + 1)""")
predict("""import numpy as np
a = np.arange(1, 10).reshape(3, 3)
print(a.T[0])
print(a.sum(axis=0) - a.sum(axis=1))
print(np.diag(a).sum())
print(a[a.sum(axis=1) > 10])
print(np.vstack([a[0], a[-1]]))""")

generate('numpy_2d', 'numpy: Zweidimensionale Arrays', INTRO)
