# Erzeugt ../content/grids.ipynb (siehe nbgen.py).
from nbgen import sec, expl, task, predict, generate

# ---------------------------------------------------------------- 1
sec('Zweidimensionale Listen erstellen')
expl('''#### Was ist eine zweidimensionale Liste?

Eine **zweidimensionale Liste** (auch *Grid*, *Tabelle* oder *Matrix*) ist eine **Liste von Listen**.
Jede innere Liste ist eine **Zeile**. Man schreibt sie gern untereinander, dann sieht man die Tabelle.

- `grid[zeile]` ist eine ganze Zeile (eine Liste).
- `grid[zeile][spalte]` ist ein einzelnes Element. Zuerst kommt die **Zeile**, dann die **Spalte**. Beide beginnen bei 0.
- `len(grid)` ist die Anzahl der Zeilen, `len(grid[0])` die Anzahl der Spalten.''',
     """grid = [
    [1, 2, 3],
    [4, 5, 6],
]
print(grid)
print(len(grid))
print(len(grid[0]))
print(grid[1])
print(grid[1][2])""")
expl('''#### Zeilenweise ausgeben

Mit `print(grid)` steht alles in einer Zeile. Übersichtlicher ist es, jede Zeile einzeln auszugeben.''',
     """grid = [[1, 2, 3], [4, 5, 6]]
for zeile in grid:
    print(zeile)""")

task('Erstelle ein Grid `grid` mit 3 Zeilen und 4 Spalten, das zeilenweise die Zahlen von 1 bis 12 enthält. Gib es zeilenweise aus.',
     solution="""grid = [
    [1, 2, 3, 4],
    [5, 6, 7, 8],
    [9, 10, 11, 12],
]
for zeile in grid:
    print(zeile)""")
G = "grid = [[5, 3, 8, 1], [2, 9, 4, 7], [6, 0, 3, 5]]"
task('Gib die Anzahl der Zeilen und die Anzahl der Spalten von `grid` aus wie unten.',
     given=G, solution=G + """
print('Zeilen:', len(grid))
print('Spalten:', len(grid[0]))""")
task("Erstelle ein leeres Tic-Tac-Toe-Feld `feld` mit 3 Zeilen und 3 Spalten, in dem jedes Feld `'.'` enthält. Gib es zeilenweise aus.",
     solution="""feld = [
    ['.', '.', '.'],
    ['.', '.', '.'],
    ['.', '.', '.'],
]
for zeile in feld:
    print(zeile)""")
task("Erstelle ein Grid `plan` mit den Fächern unten: Zeile 0 ist Montag, Zeile 1 ist Dienstag. Gib es zeilenweise aus.\n\nMontag: Mathe, Deutsch, Sport\n\nDienstag: Info, Info, Englisch",
     solution="""plan = [
    ['Mathe', 'Deutsch', 'Sport'],
    ['Info', 'Info', 'Englisch'],
]
for zeile in plan:
    print(zeile)""")
task('Gib aus, wie viele Elemente `grid` insgesamt enthält.',
     given=G, solution=G + """
print(len(grid) * len(grid[0]))""")
task('Gib die erste und die letzte Zeile von `grid` aus.',
     given=G, solution=G + """
print(grid[0])
print(grid[-1])""")
predict("""g = [[1, 2], [3, 4], [5, 6]]
print(len(g))
print(len(g[0]))
print(g[1])
print(g[1][0])
print(g[-1][-2])""")

# ---------------------------------------------------------------- 2
sec('Zugreifen und ändern')
expl('''#### Elemente ändern

- `grid[z][s] = wert` ändert ein einzelnes Element.
- `grid[z] = [...]` ersetzt eine ganze Zeile.
- `grid.append([...])` hängt eine neue Zeile unten an.
- Negative Indizes funktionieren wie bei Listen: `grid[-1][-1]` ist das Element unten rechts.''',
     """grid = [[1, 2, 3], [4, 5, 6]]
grid[0][1] = 20
grid[1] = [7, 8, 9]
grid.append([0, 0, 0])
for zeile in grid:
    print(zeile)
print(grid[-1][-1])""")

task('Gib das Element in Zeile 0 und Spalte 2 aus.',
     given=G, solution=G + """
print(grid[0][2])""")
task('Gib das Element unten rechts aus. Verwende negative Indizes.',
     given=G, solution=G + """
print(grid[-1][-1])""")
task('Gib die mittlere Zeile aus.',
     given=G, solution=G + """
print(grid[1])""")
task('Setze das Element in Zeile 1 und Spalte 1 auf 0. Gib das Grid zeilenweise aus.',
     given=G, solution=G + """
grid[1][1] = 0
for zeile in grid:
    print(zeile)""")
FELD = "feld = [['.', '.', '.'], ['.', '.', '.'], ['.', '.', '.']]"
task("Setze im Tic-Tac-Toe-Feld ein `'X'` in die Mitte und ein `'O'` in die Ecke oben links. Gib das Feld zeilenweise aus.",
     given=FELD, solution=FELD + """
feld[1][1] = 'X'
feld[0][0] = 'O'
for zeile in feld:
    print(zeile)""")
task('Ersetze die letzte Zeile von `grid` durch `[0, 0, 0, 0]`. Gib das Grid zeilenweise aus.',
     given=G, solution=G + """
grid[-1] = [0, 0, 0, 0]
for zeile in grid:
    print(zeile)""")
task('Hänge die Zeile `[1, 1, 1, 1]` unten an `grid` an. Gib das Grid zeilenweise und danach die Anzahl der Zeilen aus.',
     given=G, solution=G + """
grid.append([1, 1, 1, 1])
for zeile in grid:
    print(zeile)
print(len(grid))""")
task('Hänge an jede Zeile von `grid` am Ende eine 0 an, sodass eine neue Spalte entsteht. Gib das Grid zeilenweise aus.',
     given=G, solution=G + """
for zeile in grid:
    zeile.append(0)
for zeile in grid:
    print(zeile)""")
task('Vertausche die erste und die letzte Zeile von `grid`. Gib das Grid zeilenweise aus.',
     given=G, solution=G + """
grid[0], grid[-1] = grid[-1], grid[0]
for zeile in grid:
    print(zeile)""")
task('Berechne die Summe der vier Eckelemente von `grid` und gib sie aus.',
     given=G, solution=G + """
print(grid[0][0] + grid[0][-1] + grid[-1][0] + grid[-1][-1])""")
predict("""g = [[1, 2, 3], [4, 5, 6]]
g[0][1] = 9
g[1] = [7, 8]
print(g)
print(g[-1][-1])""")
predict("""g = [[1, 2, 3], [4, 5, 6]]
print(g[0][3])""", error=IndexError)

# ---------------------------------------------------------------- 3
sec('Grids schön ausgeben')
expl('''#### `print()` mit `end`

Normalerweise beginnt nach jedem `print()` eine neue Zeile. Mit `print(wert, end=' ')` wird am Ende stattdessen
ein Leerzeichen ausgegeben, und die nächste Ausgabe steht in derselben Zeile. Ein leeres `print()` beendet die Zeile.''',
     """grid = [[1, 2, 3], [4, 5, 6]]
for zeile in grid:
    for x in zeile:
        print(x, end=' ')
    print()""")
expl('''#### Ausgabe mit `join()` und mit Formatangaben

- Enthält das Grid **Zeichenketten**, kann man jede Zeile mit `' '.join(zeile)` zu einer Zeichenkette verbinden.
- Bei **Zahlen** sorgt eine Formatangabe wie `{x:3}` dafür, dass jede Zahl 3 Zeichen breit ist. So stehen die Spalten genau untereinander.''',
     """feld = [['X', '.', 'O'], ['.', 'X', '.']]
for zeile in feld:
    print(' '.join(zeile))
grid = [[1, 20, 3], [400, 5, 60]]
for zeile in grid:
    for x in zeile:
        print(f'{x:4}', end='')
    print()""")

task('Gib `grid` zeilenweise ohne Klammern und Kommas aus. Die Zahlen einer Zeile sind durch Leerzeichen getrennt. Verwende `end`.',
     given=G, solution=G + """
for zeile in grid:
    for x in zeile:
        print(x, end=' ')
    print()""")
task("Gib das Feld zeilenweise mit `join()` aus. Die Zeichen einer Zeile sind durch Leerzeichen getrennt.",
     given="feld = [['X', 'O', 'X'], ['.', 'X', 'O'], ['O', '.', 'X']]",
     solution="""feld = [['X', 'O', 'X'], ['.', 'X', 'O'], ['O', '.', 'X']]
for zeile in feld:
    print(' '.join(zeile))""")
task("Gib das Feld so aus wie unten: Zwischen den Feldern steht `|`, zwischen den Zeilen eine Linie aus Minuszeichen.",
     given="feld = [['X', 'O', 'X'], ['.', 'X', 'O'], ['O', '.', 'X']]",
     solution="""feld = [['X', 'O', 'X'], ['.', 'X', 'O'], ['O', '.', 'X']]
for i in range(len(feld)):
    print('|'.join(feld[i]))
    if i < len(feld) - 1:
        print('-----')""")
task('Gib das Grid so aus, dass jede Zahl 5 Zeichen breit ist und die Spalten genau untereinander stehen.',
     given="zahlen = [[1, 25, 300], [42, 7, 1000], [5, 60, 8]]",
     solution="""zahlen = [[1, 25, 300], [42, 7, 1000], [5, 60, 8]]
for zeile in zahlen:
    for x in zeile:
        print(f'{x:5}', end='')
    print()""")
task('Gib `grid` mit Zeilennummern aus wie unten.',
     given=G, solution=G + """
for i in range(len(grid)):
    print(f'Zeile {i}:', end=' ')
    for x in grid[i]:
        print(x, end=' ')
    print()""")
task('Gib `bild` aus. Für jede 1 soll `#` erscheinen, für jede 0 ein Punkt `.`. Die Zeichen einer Zeile stehen ohne Leerzeichen nebeneinander.',
     given="bild = [[0, 1, 1, 0], [1, 0, 0, 1], [1, 1, 1, 1], [1, 0, 0, 1]]",
     solution="""bild = [[0, 1, 1, 0], [1, 0, 0, 1], [1, 1, 1, 1], [1, 0, 0, 1]]
for zeile in bild:
    for x in zeile:
        if x == 1:
            print('#', end='')
        else:
            print('.', end='')
    print()""")
predict("""for zeile in [[1, 2], [3, 4]]:
    for x in zeile:
        print(x * 10, end=' ')
    print()
print('fertig')""")

# ---------------------------------------------------------------- 4
sec('Grids erzeugen')
expl('''#### Mit Schleifen erzeugen

Man beginnt mit einer leeren Liste. Für jede Zeile baut man eine neue Liste und hängt sie an.''',
     """zeilen = 2
spalten = 3
grid = []
for z in range(zeilen):
    zeile = []
    for s in range(spalten):
        zeile.append(0)
    grid.append(zeile)
print(grid)""")
expl('''#### Mit List Comprehension erzeugen

Kürzer geht es mit einer List Comprehension: `[[0] * spalten for z in range(zeilen)]`.

**Achtung:** `[[0] * spalten] * zeilen` sieht ähnlich aus, ist aber falsch. Dabei entsteht **eine** Zeile,
die mehrfach in der Liste steht. Ändert man ein Element, ändert es sich in allen Zeilen.''',
     """grid = [[0] * 3 for z in range(2)]
grid[0][0] = 1
print(grid)
falsch = [[0] * 3] * 2
falsch[0][0] = 1
print(falsch)""")

task('Erzeuge mit Schleifen ein Grid mit 3 Zeilen und 5 Spalten, das nur Nullen enthält. Gib es zeilenweise aus.',
     solution="""grid = []
for z in range(3):
    zeile = []
    for s in range(5):
        zeile.append(0)
    grid.append(zeile)
for zeile in grid:
    print(zeile)""")
task('Erzeuge dasselbe Grid wie in der vorigen Aufgabe mit einer List Comprehension. Gib es zeilenweise aus.',
     solution="""grid = [[0] * 5 for z in range(3)]
for zeile in grid:
    print(zeile)""")
task("Erzeuge ein Grid mit 4 Zeilen und 4 Spalten, das in jedem Feld `'.'` enthält. Gib es mit `join()` zeilenweise aus.",
     solution="""feld = [['.'] * 4 for z in range(4)]
for zeile in feld:
    print(' '.join(zeile))""")
task('Erzeuge ein Grid für das kleine Einmaleins von 1 bis 5: Das Element in Zeile `z` und Spalte `s` ist `(z + 1) * (s + 1)`. Gib es aus, jede Zahl 3 Zeichen breit.',
     solution="""tabelle = []
for z in range(5):
    zeile = []
    for s in range(5):
        zeile.append((z + 1) * (s + 1))
    tabelle.append(zeile)
for zeile in tabelle:
    for x in zeile:
        print(f'{x:3}', end='')
    print()""")
task('Erzeuge ein Grid mit 3 Zeilen und 4 Spalten, in dem jedes Element die Summe aus Zeilen- und Spaltenindex ist. Gib es zeilenweise aus.',
     solution="""grid = []
for z in range(3):
    zeile = []
    for s in range(4):
        zeile.append(z + s)
    grid.append(zeile)
for zeile in grid:
    print(zeile)""")
task("Erzeuge ein Schachbrett mit 4 Zeilen und 4 Spalten. Oben links steht `'W'`, danach wechseln `'W'` und `'S'` sich ab. Tipp: `(z + s) % 2`. Gib es mit `join()` aus.",
     solution="""brett = []
for z in range(4):
    zeile = []
    for s in range(4):
        if (z + s) % 2 == 0:
            zeile.append('W')
        else:
            zeile.append('S')
    brett.append(zeile)
for zeile in brett:
    print(' '.join(zeile))""")
task('Erzeuge eine 4×4-Einheitsmatrix: Auf der Diagonalen von oben links nach unten rechts steht 1, sonst 0. Gib sie zeilenweise aus.',
     solution="""matrix = [[0] * 4 for z in range(4)]
for i in range(4):
    matrix[i][i] = 1
for zeile in matrix:
    print(zeile)""")
task('Mache aus der Liste `zahlen` ein Grid mit 3 Zeilen und 4 Spalten. Verwende Slicing. Gib es zeilenweise aus.',
     given='zahlen = [5, 3, 8, 1, 2, 9, 4, 7, 6, 0, 3, 5]',
     solution="""zahlen = [5, 3, 8, 1, 2, 9, 4, 7, 6, 0, 3, 5]
grid = []
for z in range(3):
    grid.append(zahlen[z * 4:(z + 1) * 4])
for zeile in grid:
    print(zeile)""")
task('Erzeuge ein Dreieck: Zeile 0 enthält eine 1, Zeile 1 zwei Einsen usw. bis Zeile 4. Gib es zeilenweise aus.',
     solution="""dreieck = []
for z in range(5):
    dreieck.append([1] * (z + 1))
for zeile in dreieck:
    print(zeile)""")
predict("""a = [[0] * 3] * 2
a[0][0] = 1
print(a)
b = [[0] * 3 for i in range(2)]
b[0][0] = 1
print(b)""")

# ---------------------------------------------------------------- 5
sec('Grids durchlaufen')
expl('''#### Verschachtelte Schleifen

Um alle Elemente zu bearbeiten, braucht man **zwei** Schleifen: eine äußere für die Zeilen und eine innere für die Spalten.

- `for zeile in grid:` / `for x in zeile:` reicht, wenn man nur die Werte braucht.
- `for z in range(len(grid)):` / `for s in range(len(grid[z])):` braucht man, wenn man die **Position** kennen
  oder Elemente **ändern** will.''',
     """grid = [[1, 2, 3], [4, 5, 6]]
summe = 0
for zeile in grid:
    for x in zeile:
        summe += x
print(summe)
for z in range(len(grid)):
    for s in range(len(grid[z])):
        if grid[z][s] % 2 == 0:
            print('gerade Zahl bei', z, s)""")

task('Berechne die Summe aller Elemente von `grid` und gib sie aus.',
     given=G, solution=G + """
summe = 0
for zeile in grid:
    for x in zeile:
        summe += x
print(summe)""")
task('Finde mit Schleifen das größte Element von `grid` und gib es aus.',
     given=G, solution=G + """
groesstes = grid[0][0]
for zeile in grid:
    for x in zeile:
        if x > groesstes:
            groesstes = x
print(groesstes)""")
task('Zähle, wie viele Elemente von `grid` größer als 4 sind. Gib die Anzahl aus.',
     given=G, solution=G + """
anzahl = 0
for zeile in grid:
    for x in zeile:
        if x > 4:
            anzahl += 1
print(anzahl)""")
task('Gib für jede Zeile von `grid` die Summe aus. Du darfst `sum()` verwenden.',
     given=G, solution=G + """
for zeile in grid:
    print(sum(zeile))""")
task('Gib für jede Spalte von `grid` die Summe aus.',
     given=G, solution=G + """
for s in range(len(grid[0])):
    summe = 0
    for z in range(len(grid)):
        summe += grid[z][s]
    print(summe)""")
task('Finde die Position (Zeile und Spalte) des größten Elements von `grid`. Gib sie aus wie unten.',
     given=G, solution=G + """
bz, bs = 0, 0
for z in range(len(grid)):
    for s in range(len(grid[z])):
        if grid[z][s] > grid[bz][bs]:
            bz, bs = z, s
print(f'Zeile {bz}, Spalte {bs}')""")
task('Verdopple jedes Element von `grid`. Das Grid selbst soll geändert werden. Gib es danach zeilenweise aus.',
     given=G, solution=G + """
for z in range(len(grid)):
    for s in range(len(grid[z])):
        grid[z][s] = 2 * grid[z][s]
for zeile in grid:
    print(zeile)""")
task("Zähle, wie viele `'X'` im Feld stehen. Gib die Anzahl aus.",
     given="feld = [['X', 'O', 'X'], ['.', 'X', 'O'], ['O', '.', 'X']]",
     solution="""feld = [['X', 'O', 'X'], ['.', 'X', 'O'], ['O', '.', 'X']]
anzahl = 0
for zeile in feld:
    anzahl += zeile.count('X')
print(anzahl)""")
task("Gib die Positionen aller leeren Felder (`'.'`) aus, jeweils als Zeile und Spalte.",
     given="feld = [['X', 'O', 'X'], ['.', 'X', 'O'], ['O', '.', 'X']]",
     solution="""feld = [['X', 'O', 'X'], ['.', 'X', 'O'], ['O', '.', 'X']]
for z in range(len(feld)):
    for s in range(len(feld[z])):
        if feld[z][s] == '.':
            print(z, s)""")
task('Berechne den Durchschnitt aller Elemente von `grid` und gib ihn aus.',
     given=G, solution=G + """
summe = 0
anzahl = 0
for zeile in grid:
    for x in zeile:
        summe += x
        anzahl += 1
print(summe / anzahl)""")
task('Gib die Nummer der Zeile aus, deren Summe am größten ist.',
     given=G, solution=G + """
beste = 0
for z in range(len(grid)):
    if sum(grid[z]) > sum(grid[beste]):
        beste = z
print(beste)""")
predict("""g = [[1, 2], [3, 4], [5, 6]]
a = 0
b = 0
for zeile in g:
    a += zeile[0]
    b += zeile[-1]
print(a, b)
print(g[2][0] * g[0][1])""")

# ---------------------------------------------------------------- 6
sec('Zeilen, Spalten und Diagonalen')
expl('''#### Spalten

Eine Zeile ist einfach `grid[z]`. Eine **Spalte** muss man sich aus allen Zeilen zusammensuchen:
`[zeile[s] for zeile in grid]`.''',
     """m = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
print(m[1])
print([zeile[1] for zeile in m])""")
expl('''#### Diagonalen und Transponieren

Bei einem **quadratischen** Grid mit `n` Zeilen und Spalten gilt:

- Die **Hauptdiagonale** (oben links nach unten rechts) besteht aus `m[i][i]`.
- Die **Nebendiagonale** (oben rechts nach unten links) besteht aus `m[i][n - 1 - i]`.
- Beim **Transponieren** werden Zeilen zu Spalten: Das neue Element `[z][s]` ist das alte `[s][z]`.''',
     """m = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
n = len(m)
print([m[i][i] for i in range(n)])
print([m[i][n - 1 - i] for i in range(n)])
t = [[m[s][z] for s in range(n)] for z in range(n)]
print(t)""")

M = "m = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]"
task('Gib die Spalte mit Index 1 von `m` als Liste aus.',
     given=M, solution=M + """
spalte = []
for zeile in m:
    spalte.append(zeile[1])
print(spalte)""")
task('Gib die letzte Spalte von `m` als Liste aus. Verwende eine List Comprehension.',
     given=M, solution=M + """
print([zeile[-1] for zeile in m])""")
task('Gib die Hauptdiagonale von `m` als Liste aus.',
     given=M, solution=M + """
print([m[i][i] for i in range(len(m))])""")
task('Gib die Nebendiagonale von `m` als Liste aus.',
     given=M, solution=M + """
n = len(m)
print([m[i][n - 1 - i] for i in range(n)])""")
task('Berechne die Summe der Hauptdiagonale von `m` und gib sie aus.',
     given=M, solution=M + """
summe = 0
for i in range(len(m)):
    summe += m[i][i]
print(summe)""")
task('Erzeuge mit Schleifen die transponierte Matrix von `t`. Aus den Zeilen werden Spalten. Gib sie zeilenweise aus.',
     given="t = [[1, 2, 3], [4, 5, 6]]",
     solution="""t = [[1, 2, 3], [4, 5, 6]]
neu = []
for s in range(len(t[0])):
    zeile = []
    for z in range(len(t)):
        zeile.append(t[z][s])
    neu.append(zeile)
for zeile in neu:
    print(zeile)""")
task('Spiegele `m` an der senkrechten Achse: Jede Zeile wird umgedreht. Erzeuge ein neues Grid und gib es zeilenweise aus.',
     given=M, solution=M + """
neu = []
for zeile in m:
    umgedreht = zeile.copy()
    umgedreht.reverse()
    neu.append(umgedreht)
for zeile in neu:
    print(zeile)""")
task('Spiegele `m` an der waagerechten Achse: Die Reihenfolge der Zeilen wird umgedreht. Erzeuge ein neues Grid und gib es zeilenweise aus.',
     given=M, solution=M + """
neu = []
for i in range(len(m) - 1, -1, -1):
    neu.append(m[i].copy())
for zeile in neu:
    print(zeile)""")
task('Drehe `m` um 90 Grad im Uhrzeigersinn. Für das neue Element gilt `neu[z][s] = m[n - 1 - s][z]`. Gib das neue Grid zeilenweise aus.',
     given=M, solution=M + """
n = len(m)
neu = [[0] * n for z in range(n)]
for z in range(n):
    for s in range(n):
        neu[z][s] = m[n - 1 - s][z]
for zeile in neu:
    print(zeile)""")
task('Prüfe, ob `m` symmetrisch ist, also ob für alle `z` und `s` gilt: `m[z][s] == m[s][z]`. Gib `symmetrisch` oder `nicht symmetrisch` aus.',
     given="m = [[1, 7, 3], [7, 4, 5], [3, 5, 6]]",
     solution="""m = [[1, 7, 3], [7, 4, 5], [3, 5, 6]]
sym = True
for z in range(len(m)):
    for s in range(len(m)):
        if m[z][s] != m[s][z]:
            sym = False
if sym:
    print('symmetrisch')
else:
    print('nicht symmetrisch')""")
predict("""m = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
print([z[0] for z in m])
print(m[1][-1])
print(m[0][0] + m[1][1] + m[2][2] - m[1][1])""")

# ---------------------------------------------------------------- 7
sec('Nachbarn')
expl('''#### Nachbarfelder und der Rand

Das Feld in Zeile `z` und Spalte `s` hat bis zu vier **direkte Nachbarn**: oben `(z - 1, s)`, unten `(z + 1, s)`,
links `(z, s - 1)` und rechts `(z, s + 1)`. Mit den vier diagonalen Feldern sind es acht.

Am Rand gibt es manche Nachbarn nicht. Vor dem Zugriff prüft man deshalb, ob die Position im Grid liegt:
`0 <= z < len(grid)` und `0 <= s < len(grid[0])`. Vorsicht: Ein negativer Index gibt keinen Fehler, sondern zählt von hinten.''',
     """grid = [[1, 2, 3], [4, 5, 6]]
z, s = 0, 0
for dz, ds in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
    nz = z + dz
    ns = s + ds
    if 0 <= nz < len(grid) and 0 <= ns < len(grid[0]):
        print('Nachbar:', grid[nz][ns])""")

task('Gib die Werte der vier direkten Nachbarn des Feldes in Zeile 1 und Spalte 1 aus: oben, unten, links, rechts.',
     given=G, solution=G + """
print(grid[0][1])
print(grid[2][1])
print(grid[1][0])
print(grid[1][2])""")
task('''Schreibe eine Funktion `im_grid(grid, z, s)`, die `True` zurückgibt, wenn die Position im Grid liegt, sonst `False`.
Teste sie mit den Positionen `(0, 0)`, `(2, 3)`, `(3, 0)` und `(1, -1)`.''',
     given=G, solution=G + """

def im_grid(grid, z, s):
    return 0 <= z < len(grid) and 0 <= s < len(grid[0])

print(im_grid(grid, 0, 0))
print(im_grid(grid, 2, 3))
print(im_grid(grid, 3, 0))
print(im_grid(grid, 1, -1))""")
task('Berechne die Summe der direkten Nachbarn des Feldes in Zeile 0 und Spalte 0. Prüfe dabei für jeden Nachbarn, ob er im Grid liegt.',
     given=G, solution=G + """
z, s = 0, 0
summe = 0
for dz, ds in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
    nz = z + dz
    ns = s + ds
    if 0 <= nz < len(grid) and 0 <= ns < len(grid[0]):
        summe += grid[nz][ns]
print(summe)""")
MINEN = """minen = [
    ['.', '*', '.', '.'],
    ['.', '.', '.', '*'],
    ['*', '.', '.', '.'],
]"""
task("Zähle, wie viele Minen `'*'` in den **acht** Nachbarfeldern des Feldes in Zeile 1 und Spalte 1 liegen. Gib die Anzahl aus.",
     given=MINEN, solution=MINEN + """
z, s = 1, 1
anzahl = 0
for dz in [-1, 0, 1]:
    for ds in [-1, 0, 1]:
        if dz == 0 and ds == 0:
            continue
        nz = z + dz
        ns = s + ds
        if 0 <= nz < len(minen) and 0 <= ns < len(minen[0]):
            if minen[nz][ns] == '*':
                anzahl += 1
print(anzahl)""")
task("Erzeuge wie beim Spiel Minesweeper ein Hinweisfeld: Jede Mine bleibt `'*'`, jedes andere Feld enthält die Anzahl der Minen in den acht Nachbarfeldern. Gib das Ergebnis mit `join()` aus.",
     given=MINEN, solution=MINEN + """
hinweis = []
for z in range(len(minen)):
    zeile = []
    for s in range(len(minen[0])):
        if minen[z][s] == '*':
            zeile.append('*')
        else:
            anzahl = 0
            for dz in [-1, 0, 1]:
                for ds in [-1, 0, 1]:
                    nz = z + dz
                    ns = s + ds
                    if 0 <= nz < len(minen) and 0 <= ns < len(minen[0]):
                        if minen[nz][ns] == '*':
                            anzahl += 1
            zeile.append(str(anzahl))
    hinweis.append(zeile)
for zeile in hinweis:
    print(' '.join(zeile))""")
task('Gib die Positionen aller Felder aus, deren Wert größer ist als der Wert jedes direkten Nachbarn.',
     given=G, solution=G + """
for z in range(len(grid)):
    for s in range(len(grid[0])):
        groesser = True
        for dz, ds in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nz = z + dz
            ns = s + ds
            if 0 <= nz < len(grid) and 0 <= ns < len(grid[0]):
                if grid[nz][ns] >= grid[z][s]:
                    groesser = False
        if groesser:
            print(z, s)""")
predict("""g = [[1, 2, 3], [4, 5, 6]]
print(g[0][-1])
print(g[-1][0])
z, s = 0, 0
print(0 <= z - 1 < len(g))""")

# ---------------------------------------------------------------- 8
sec('Grids aus Zeichenketten')
expl('''#### Eine Liste von Zeichenketten als Grid

Eine Karte oder ein Spielfeld schreibt man oft als **Liste von Zeichenketten**. Auch dann ist `karte[z][s]` ein einzelnes Zeichen.

Zeichenketten kann man aber nicht ändern. Will man das Feld ändern, wandelt man jede Zeile mit `list()` in eine Liste um.
Zur Ausgabe setzt man die Zeile mit `''.join(zeile)` wieder zusammen.''',
     """karte = ['#####',
         '#S..#',
         '#####']
print(karte[1][1])
feld = [list(zeile) for zeile in karte]
feld[1][2] = 'X'
for zeile in feld:
    print(''.join(zeile))""")

KARTE = """karte = ['#######',
         '#S..#.#',
         '#.#...#',
         '#...#Z#',
         '#######']"""
task('Gib das Zeichen in Zeile 1 und Spalte 1 und das Zeichen in Zeile 3 und Spalte 5 aus.',
     given=KARTE, solution=KARTE + """
print(karte[1][1])
print(karte[3][5])""")
task("Finde die Position des Starts `'S'` und des Ziels `'Z'`. Gib beide aus wie unten.",
     given=KARTE, solution=KARTE + """
for z in range(len(karte)):
    for s in range(len(karte[z])):
        if karte[z][s] == 'S':
            print('Start:', z, s)
        if karte[z][s] == 'Z':
            print('Ziel:', z, s)""")
task("Zähle die Wände `'#'` in der Karte und gib die Anzahl aus.",
     given=KARTE, solution=KARTE + """
anzahl = 0
for zeile in karte:
    anzahl += zeile.count('#')
print(anzahl)""")
task("Zähle die freien Felder `'.'` in der Karte. Verwende zwei Schleifen. Gib die Anzahl aus.",
     given=KARTE, solution=KARTE + """
anzahl = 0
for zeile in karte:
    for c in zeile:
        if c == '.':
            anzahl += 1
print(anzahl)""")
task("Wandle die Karte in eine Liste von Listen um und setze ein `'X'` in Zeile 2 und Spalte 3. Gib die Karte mit `join()` aus.",
     given=KARTE, solution=KARTE + """
feld = [list(zeile) for zeile in karte]
feld[2][3] = 'X'
for zeile in feld:
    print(''.join(zeile))""")
task("""Die Figur steht auf `'S'` in Zeile 1 und Spalte 1. Sie läuft die Befehle in `befehle` ab: `R` = rechts, `L` = links, `U` = hoch, `D` = runter.
Steht auf dem Zielfeld eine Wand `'#'`, bleibt die Figur stehen. Gib am Ende die Position der Figur aus.""",
     given=KARTE + "\nbefehle = 'RRDDR'",
     solution=KARTE + """
befehle = 'RRDDR'
z, s = 1, 1
richtung = {'R': (0, 1), 'L': (0, -1), 'U': (-1, 0), 'D': (1, 0)}
for b in befehle:
    dz, ds = richtung[b]
    if karte[z + dz][s + ds] != '#':
        z = z + dz
        s = s + ds
print(z, s)""")
task("Zeichne den Weg der Figur aus der vorigen Aufgabe in die Karte ein: Jedes Feld, auf dem die Figur nach einem Schritt steht, wird zu `'o'`. Gib die Karte mit `join()` aus.",
     given=KARTE + "\nbefehle = 'RRDDR'",
     solution=KARTE + """
befehle = 'RRDDR'
feld = [list(zeile) for zeile in karte]
z, s = 1, 1
richtung = {'R': (0, 1), 'L': (0, -1), 'U': (-1, 0), 'D': (1, 0)}
for b in befehle:
    dz, ds = richtung[b]
    if feld[z + dz][s + ds] != '#':
        z = z + dz
        s = s + ds
        feld[z][s] = 'o'
for zeile in feld:
    print(''.join(zeile))""")
predict("""k = ['ab', 'cd']
print(k[1][0])
f = [list(z) for z in k]
f[0][1] = 'X'
print(f)
print(k)
print(''.join(f[0]))""")
predict("""k = ['ab', 'cd']
k[0][0] = 'X'""", error=TypeError)

# ---------------------------------------------------------------- 9
sec('Gemischte Übungen')
task("""Prüfe, ob `'X'` im Tic-Tac-Toe-Feld gewonnen hat. Das ist der Fall, wenn eine ganze Zeile, eine ganze Spalte
oder eine der beiden Diagonalen nur `'X'` enthält. Gib `X gewinnt` oder `kein Gewinner` aus.""",
     given="feld = [['X', 'O', 'O'], ['.', 'X', 'O'], ['O', '.', 'X']]",
     solution="""feld = [['X', 'O', 'O'], ['.', 'X', 'O'], ['O', '.', 'X']]
s = 'X'
gewonnen = False
for i in range(3):
    if feld[i][0] == s and feld[i][1] == s and feld[i][2] == s:
        gewonnen = True
    if feld[0][i] == s and feld[1][i] == s and feld[2][i] == s:
        gewonnen = True
if feld[0][0] == s and feld[1][1] == s and feld[2][2] == s:
    gewonnen = True
if feld[0][2] == s and feld[1][1] == s and feld[2][0] == s:
    gewonnen = True
if gewonnen:
    print('X gewinnt')
else:
    print('kein Gewinner')""")
task("""Ein magisches Quadrat hat in jeder Zeile, jeder Spalte und beiden Diagonalen dieselbe Summe.
Prüfe, ob `q` ein magisches Quadrat ist. Gib `magisch` oder `nicht magisch` aus.""",
     given="q = [[2, 7, 6], [9, 5, 1], [4, 3, 8]]",
     solution="""q = [[2, 7, 6], [9, 5, 1], [4, 3, 8]]
n = len(q)
ziel = sum(q[0])
magisch = True
for i in range(n):
    if sum(q[i]) != ziel:
        magisch = False
    spalte = 0
    for z in range(n):
        spalte += q[z][i]
    if spalte != ziel:
        magisch = False
d1 = 0
d2 = 0
for i in range(n):
    d1 += q[i][i]
    d2 += q[i][n - 1 - i]
if d1 != ziel or d2 != ziel:
    magisch = False
if magisch:
    print('magisch')
else:
    print('nicht magisch')""")
task('Addiere die beiden Matrizen `a` und `b` elementweise zu einer neuen Matrix. Gib sie zeilenweise aus.',
     given="""a = [[1, 2, 3], [4, 5, 6]]
b = [[10, 20, 30], [40, 50, 60]]""",
     solution="""a = [[1, 2, 3], [4, 5, 6]]
b = [[10, 20, 30], [40, 50, 60]]
summe = []
for z in range(len(a)):
    zeile = []
    for s in range(len(a[0])):
        zeile.append(a[z][s] + b[z][s])
    summe.append(zeile)
for zeile in summe:
    print(zeile)""")
BILD = "bild = [[0, 2, 5, 9], [1, 7, 8, 3], [9, 6, 2, 0]]"
task('`bild` enthält Helligkeiten von 0 (schwarz) bis 9 (weiß). Erzeuge das Negativ: Jeder Wert `x` wird zu `9 - x`. Gib das neue Bild zeilenweise aus.',
     given=BILD, solution=BILD + """
negativ = []
for zeile in bild:
    neue_zeile = []
    for x in zeile:
        neue_zeile.append(9 - x)
    negativ.append(neue_zeile)
for zeile in negativ:
    print(zeile)""")
task("Gib `bild` als Schwarz-Weiß-Bild aus: Werte größer als 4 werden zu `'#'`, alle anderen zu `'.'`. Die Zeichen einer Zeile stehen direkt nebeneinander.",
     given=BILD, solution=BILD + """
for zeile in bild:
    text = ''
    for x in zeile:
        if x > 4:
            text += '#'
        else:
            text += '.'
    print(text)""")
task("Im Kinosaal steht `'x'` für einen belegten und `'.'` für einen freien Platz. Gib für jede Reihe die Anzahl der freien Plätze aus wie unten.",
     given="saal = ['xx..x', 'xxxxx', '.x...', 'x.x.x']",
     solution="""saal = ['xx..x', 'xxxxx', '.x...', 'x.x.x']
for i in range(len(saal)):
    print(f'Reihe {i + 1}: {saal[i].count(".")} frei')""")
PUNKTE = "punkte = [[12, 15, 9], [8, 11, 14], [15, 13, 10]]"
task('In `punkte` steht jede Zeile für einen Schüler und jede Spalte für einen Test. Gib den Durchschnitt jedes Schülers mit einer Nachkommastelle aus wie unten.',
     given=PUNKTE, solution=PUNKTE + """
for i in range(len(punkte)):
    schnitt = sum(punkte[i]) / len(punkte[i])
    print(f'Schüler {i + 1}: {schnitt:.1f}')""")
task('Gib für jeden Test aus `punkte` die beste Punktzahl aus wie unten.',
     given=PUNKTE, solution=PUNKTE + """
for t in range(len(punkte[0])):
    beste = punkte[0][t]
    for zeile in punkte:
        if zeile[t] > beste:
            beste = zeile[t]
    print(f'Test {t + 1}: {beste}')""")
task("""Berechne beim „Spiel des Lebens“ die nächste Generation. Eine lebende Zelle (1) überlebt mit 2 oder 3 lebenden Nachbarn,
sonst stirbt sie. Eine tote Zelle (0) wird mit genau 3 lebenden Nachbarn lebendig. Es zählen die acht Nachbarfelder.
Gib die neue Generation zeilenweise aus.""",
     given="welt = [[0, 0, 0, 0, 0], [0, 0, 1, 0, 0], [0, 0, 1, 0, 0], [0, 0, 1, 0, 0], [0, 0, 0, 0, 0]]",
     solution="""welt = [[0, 0, 0, 0, 0], [0, 0, 1, 0, 0], [0, 0, 1, 0, 0], [0, 0, 1, 0, 0], [0, 0, 0, 0, 0]]
n = len(welt)
neu = [[0] * n for z in range(n)]
for z in range(n):
    for s in range(n):
        nachbarn = 0
        for dz in [-1, 0, 1]:
            for ds in [-1, 0, 1]:
                if dz == 0 and ds == 0:
                    continue
                nz = z + dz
                ns = s + ds
                if 0 <= nz < n and 0 <= ns < n:
                    nachbarn += welt[nz][ns]
        if welt[z][s] == 1 and nachbarn in (2, 3):
            neu[z][s] = 1
        if welt[z][s] == 0 and nachbarn == 3:
            neu[z][s] = 1
for zeile in neu:
    print(zeile)""")
predict("""g = [[1, 2, 3], [4, 5, 6]]
h = [zeile.copy() for zeile in g]
h[0][0] = 99
k = g
k[1][1] = 0
print(g)
print(h)""")

generate('grids', 'Zweidimensionale Listen (Grids)')
