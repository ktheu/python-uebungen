# Erzeugt ../content/tupel.ipynb (siehe nbgen.py).
from nbgen import sec, expl, task, predict, generate

# ---------------------------------------------------------------- 1
sec('Tupel erstellen')
expl('''#### Was ist ein Tupel?

Ein **Tupel** speichert wie eine Liste mehrere Werte in einer Variablen. Die Elemente stehen in **runden** Klammern.

- Tupel sind **geordnet**: Die Elemente haben eine feste Reihenfolge.
- Tupel sind **unveränderlich**: Nach dem Erstellen kann man keine Elemente ändern, hinzufügen oder entfernen.
- Tupel dürfen **Duplikate** und Elemente **verschiedener Datentypen** enthalten.
- Die Klammern darf man auch weglassen: `t = 1, 2, 3` ist ebenfalls ein Tupel.

Man nimmt Tupel für Daten, die zusammengehören und sich nicht ändern sollen, z. B. Koordinaten `(3, 4)` oder ein Datum `(17, 10, 2026)`.''',
     """punkt = (3, 4)
person = ('Ali', 16, 'Berlin')
farbe = 255, 128, 0
print(punkt)
print(person)
print(farbe)""")
expl('''#### Tupel mit einem Element

Bei einem Tupel mit **nur einem** Element muss nach dem Element ein **Komma** stehen.
Ohne Komma sind die Klammern nur normale Klammern wie in einer Rechnung. `()` ist ein leeres Tupel.''',
     """a = ('Hallo',)
b = ('Hallo')
print(type(a))
print(type(b))
print(())""")
expl('''#### `len()` und `type()`

`len(tupel)` gibt die Anzahl der Elemente zurück. `type(tupel)` gibt den Datentyp `tuple` zurück.''',
     """punkt = (3, 4)
print(len(punkt))
print(type(punkt))""")
expl('''#### `tuple()`

`tuple(...)` erzeugt ein neues Tupel, z. B. aus einer Liste, einer Zeichenkette oder einem `range()`.''',
     """print(tuple([1, 2, 3]))
print(tuple('abc'))
print(tuple(range(5)))""")

task('Erstelle ein Tupel `wochentage` mit den Kürzeln `Mo` bis `So`. Gib das Tupel aus.',
     solution="""wochentage = ('Mo', 'Di', 'Mi', 'Do', 'Fr', 'Sa', 'So')
print(wochentage)""")
task('Erstelle ein Tupel `punkt` mit den Koordinaten 3 und 4. Gib das Tupel und seine Länge aus.',
     solution="""punkt = (3, 4)
print(punkt)
print(len(punkt))""")
task("Erstelle ein Tupel mit dem einzigen Element `'Hallo'`. Gib das Tupel und seinen Datentyp aus.",
     solution="""t = ('Hallo',)
print(t)
print(type(t))""")
task('Erstelle mit `tuple()` aus der Liste `zahlen` ein Tupel. Gib es aus.',
     given='zahlen = [4, 8, 15, 16, 23, 42]',
     solution="""zahlen = [4, 8, 15, 16, 23, 42]
t = tuple(zahlen)
print(t)""")
task('Erstelle mit `tuple()` und `range()` ein Tupel mit den Zahlen von 1 bis 10. Gib es aus.',
     solution="""t = tuple(range(1, 11))
print(t)""")
task("Erstelle mit `tuple()` ein Tupel aus den Buchstaben von `'Python'`. Gib es aus.",
     solution="""t = tuple('Python')
print(t)""")
task('Erstelle **ohne Klammern** ein Tupel `orange` mit den Farbwerten 255, 128 und 0. Gib es aus.',
     solution="""orange = 255, 128, 0
print(orange)""")
task('Gib mit einem f-String und `len()` aus, wie viele Monate in `monate` stehen. Die Ausgabe soll so aussehen wie unten.',
     given="monate = ('Jan', 'Feb', 'Mär', 'Apr', 'Mai', 'Jun', 'Jul', 'Aug', 'Sep', 'Okt', 'Nov', 'Dez')",
     solution="""monate = ('Jan', 'Feb', 'Mär', 'Apr', 'Mai', 'Jun', 'Jul', 'Aug', 'Sep', 'Okt', 'Nov', 'Dez')
print(f'Ein Jahr hat {len(monate)} Monate.')""")
task('Erstelle ein Tupel `geburtstag` mit Tag, Monat und Jahr deines Geburtstags. Gib das Tupel aus.',
     solution="""geburtstag = (3, 5, 2010)
print(geburtstag)""", kind='free')
predict("""a = (5)
b = (5,)
c = ()
d = 1, 2
print(type(a))
print(type(b))
print(len(c))
print(d)""")

# ---------------------------------------------------------------- 2
sec('Auf Elemente zugreifen')
expl('''#### Index, negativer Index und Slicing

Der Zugriff funktioniert genau wie bei Listen:

- `t[0]` ist das erste Element, `t[-1]` das letzte.
- `t[start:stop]` ergibt ein **neues Tupel** mit den Elementen von `start` bis ausschließlich `stop`.
- `wert in t` prüft, ob ein Wert im Tupel vorkommt.''',
     """t = ('a', 'b', 'c', 'd', 'e')
print(t[0])
print(t[-1])
print(t[1:3])
print(t[:2])
print('c' in t)""")

MONATE = "monate = ('Jan', 'Feb', 'Mär', 'Apr', 'Mai', 'Jun', 'Jul', 'Aug', 'Sep', 'Okt', 'Nov', 'Dez')"
task('Gib den ersten und den letzten Monat aus, jeweils in einer eigenen Zeile.',
     given=MONATE, solution=MONATE + """
print(monate[0])
print(monate[-1])""")
task('Gib den fünften Monat aus.',
     given=MONATE, solution=MONATE + """
print(monate[4])""")
task('Gib mit Slicing die ersten drei Monate aus.',
     given=MONATE, solution=MONATE + """
print(monate[:3])""")
task('Gib mit Slicing und negativen Indizes die letzten drei Monate aus.',
     given=MONATE, solution=MONATE + """
print(monate[-3:])""")
task('Gib mit Slicing die Sommermonate Juni, Juli und August aus.',
     given=MONATE, solution=MONATE + """
print(monate[5:8])""")
task("Prüfe mit `in`, ob `'Mai'` in `monate` vorkommt, und gib das Ergebnis (`True` oder `False`) aus. Prüfe danach `'May'`.",
     given=MONATE, solution=MONATE + """
print('Mai' in monate)
print('May' in monate)""")
task('Gib die beiden Koordinaten von `punkt` aus wie unten.',
     given='punkt = (3, 7)',
     solution="""punkt = (3, 7)
print(f'x = {punkt[0]}, y = {punkt[1]}')""")
task('Berechne den Mittelwert der drei Farbwerte in `rgb` und gib ihn aus.',
     given='rgb = (255, 128, 0)',
     solution="""rgb = (255, 128, 0)
print((rgb[0] + rgb[1] + rgb[2]) / 3)""")
task('Gib mit den Elementen von `person` den Satz unten aus.',
     given="person = ('Ali', 16, 'Berlin')",
     solution="""person = ('Ali', 16, 'Berlin')
print(f'{person[0]} ist {person[1]} Jahre alt und wohnt in {person[2]}.')""")
task('Gib den Monat mit der Nummer `nr` aus (Januar hat die Nummer 1).',
     given=MONATE + '\nnr = 10',
     solution=MONATE + """
nr = 10
print(monate[nr - 1])""")
predict("""t = (10, 20, 30, 40, 50)
print(t[1])
print(t[-1])
print(t[1:3])
print(t[:1])
print(40 in t)""")
predict("""t = (1, 2, 3)
print(t[3])""", error=IndexError)

# ---------------------------------------------------------------- 3
sec('Tupel sind unveränderlich')
expl('''#### Kein Ändern, Hinzufügen oder Entfernen

Bei einem Tupel gibt es **kein** `t[0] = ...`, kein `append()` und kein `remove()`. Das führt zu einem Fehler.
Mit `del t` kann man aber das ganze Tupel löschen.''',
     """t = (1, 2, 3)
try:
    t[0] = 9
except TypeError as fehler:
    print('Fehler:', fehler)""")
expl('''#### Umweg über eine Liste

Will man ein Tupel trotzdem „ändern“, wandelt man es mit `list()` in eine Liste um, ändert die Liste
und wandelt sie mit `tuple()` wieder zurück. Dabei entsteht ein **neues** Tupel.''',
     """farben = ('rot', 'grün', 'blau')
liste = list(farben)
liste[1] = 'gelb'
liste.append('lila')
farben = tuple(liste)
print(farben)""")
expl('''#### Neues Tupel mit `+`

Mit `+` kann man zwei Tupel zu einem **neuen** Tupel verbinden. So kann man auch ein Element „anhängen“:
`t + ('neu',)`. Das Komma ist wichtig.''',
     """t = (1, 2, 3)
t = t + (4,)
print(t)""")

FARBEN = "farben = ('rot', 'grün', 'blau')"
task("Ändere über eine Liste das zweite Element von `farben` in `'gelb'`. Speichere das Ergebnis wieder als Tupel in `farben` und gib es aus.",
     given=FARBEN, solution=FARBEN + """
liste = list(farben)
liste[1] = 'gelb'
farben = tuple(liste)
print(farben)""")
task("Füge über eine Liste und `append()` das Element `'lila'` am Ende von `farben` hinzu. Gib das neue Tupel aus.",
     given=FARBEN, solution=FARBEN + """
liste = list(farben)
liste.append('lila')
farben = tuple(liste)
print(farben)""")
task("Füge mit `+` das Element `'lila'` am Ende von `farben` hinzu. Gib das neue Tupel aus.",
     given=FARBEN, solution=FARBEN + """
farben = farben + ('lila',)
print(farben)""")
task("Füge mit `+` das Element `'weiß'` am **Anfang** von `farben` hinzu. Gib das neue Tupel aus.",
     given=FARBEN, solution=FARBEN + """
farben = ('weiß',) + farben
print(farben)""")
task("Entferne über eine Liste das Element `'grün'` aus `farben`. Gib das neue Tupel aus.",
     given=FARBEN, solution=FARBEN + """
liste = list(farben)
liste.remove('grün')
farben = tuple(liste)
print(farben)""")
task('Erzeuge mit Slicing und `+` ein neues Tupel, in dem das mittlere Element von `zahlen` durch 0 ersetzt ist. Gib es aus.',
     given='zahlen = (1, 2, 3, 4, 5)',
     solution="""zahlen = (1, 2, 3, 4, 5)
neu = zahlen[:2] + (0,) + zahlen[3:]
print(neu)""")
task('Sortiere die Zahlen in `t` über eine Liste. Speichere das Ergebnis wieder als Tupel in `t` und gib es aus.',
     given='t = (5, 2, 8, 1, 9)',
     solution="""t = (5, 2, 8, 1, 9)
liste = list(t)
liste.sort()
t = tuple(liste)
print(t)""")
predict("""t = (1, 2, 3)
u = t + (4,)
print(t)
print(u)
liste = list(t)
liste.append(5)
print(tuple(liste))
print(t)""")
predict("""t = (1, 2, 3)
t[0] = 9""", error=TypeError)
predict("""t = (1, 2, 3)
t.append(4)""", error=AttributeError)

# ---------------------------------------------------------------- 4
sec('Tupel entpacken')
expl('''#### Entpacken

Man kann die Elemente eines Tupels in einer Zeile auf mehrere Variablen verteilen:
`x, y = punkt`. Die Anzahl der Variablen muss zur Anzahl der Elemente passen, sonst gibt es einen `ValueError`.''',
     """punkt = (3, 7)
x, y = punkt
print(x)
print(y)""")
expl('''#### Entpacken mit `*`

Steht vor einer Variablen ein `*`, sammelt sie **alle übrigen** Elemente in einer **Liste**.''',
     """zahlen = (1, 2, 3, 4, 5)
erste, *rest = zahlen
print(erste)
print(rest)
anfang, *mitte, ende = zahlen
print(anfang, mitte, ende)""")
expl('''#### Werte tauschen

Mit `a, b = b, a` tauscht man die Werte zweier Variablen in einer Zeile.
Rechts entsteht dabei ein Tupel, das links wieder entpackt wird.''',
     """a = 1
b = 2
a, b = b, a
print(a, b)""")

task('Entpacke `punkt` in die Variablen `x` und `y`. Gib beide aus wie unten.',
     given='punkt = (3, 7)',
     solution="""punkt = (3, 7)
x, y = punkt
print(f'x = {x}, y = {y}')""")
task('Entpacke `person` in die Variablen `name`, `alter` und `ort`. Gib den Satz unten aus.',
     given="person = ('Ali', 16, 'Berlin')",
     solution="""person = ('Ali', 16, 'Berlin')
name, alter, ort = person
print(f'{name} ist {alter} Jahre alt und wohnt in {ort}.')""")
task('Entpacke `datum` in drei Variablen und gib das Datum in der Form unten aus.',
     given='datum = (17, 10, 2026)',
     solution="""datum = (17, 10, 2026)
tag, monat, jahr = datum
print(f'{tag}.{monat}.{jahr}')""")
task('Vertausche die Werte von `a` und `b` in **einer** Zeile. Gib danach `a` und `b` aus.',
     given="""a = 'links'
b = 'rechts'""",
     solution="""a = 'links'
b = 'rechts'
a, b = b, a
print(a, b)""")
task('Entpacke `noten` mit `*` so, dass `erste` die erste Note enthält und `rest` alle anderen. Gib beide aus.',
     given='noten = (1, 2, 3, 2, 4)',
     solution="""noten = (1, 2, 3, 2, 4)
erste, *rest = noten
print(erste)
print(rest)""")
task('Entpacke `platzierung` mit `*` in `erster`, `mittelfeld` und `letzter`. Gib die drei Variablen aus.',
     given="platzierung = ('Ida', 'Tom', 'Lea', 'Jan', 'Mia')",
     solution="""platzierung = ('Ida', 'Tom', 'Lea', 'Jan', 'Mia')
erster, *mittelfeld, letzter = platzierung
print(erster)
print(mittelfeld)
print(letzter)""")
task('Verschiebe die Werte von `x`, `y` und `z` in einer Zeile im Kreis: `x` bekommt den Wert von `y`, `y` den von `z` und `z` den von `x`. Gib danach alle drei aus.',
     given="""x = 1
y = 2
z = 3""",
     solution="""x = 1
y = 2
z = 3
x, y, z = y, z, x
print(x, y, z)""")
task('Gib die ersten 10 Fibonacci-Zahlen aus, jede in einer eigenen Zeile. Beginne mit `a, b = 1, 1` und berechne die nächste Zahl mit `a, b = b, a + b`.',
     solution="""a, b = 1, 1
for i in range(10):
    print(a)
    a, b = b, a + b""")
predict("""a, b = 1, 2
a, b = b, a + b
print(a, b)
x, *y = (5, 6, 7, 8)
print(x)
print(y)
*p, q = 'abc'
print(p, q)""")
predict("""a, b = (1, 2, 3)
print(a, b)""", error=ValueError)

# ---------------------------------------------------------------- 5
sec('Schleifen über Tupel')
expl('''#### Schleifen

Über ein Tupel läuft man genau wie über eine Liste: mit `for element in t:`,
mit `for i in range(len(t)):` oder mit einer `while`-Schleife.''',
     """farben = ('rot', 'grün', 'blau')
for f in farben:
    print(f)
for i in range(len(farben)):
    print(i, farben[i])""")
expl('''#### Tupel in Listen und Entpacken in der Schleife

Oft stehen Tupel in einer Liste, z. B. `[('Ali', 2), ('Bea', 1)]`.
In der `for`-Schleife kann man jedes Tupel direkt entpacken: `for name, note in liste:`.''',
     """noten = [('Ali', 2), ('Bea', 1), ('Cem', 3)]
for name, note in noten:
    print(name, 'hat die Note', note)""")

ZT = 'zahlen = (7, 12, 3, 18, 5, 11)'
task('Gib jede Farbe aus `farben` in einer eigenen Zeile aus.',
     given="farben = ('rot', 'grün', 'blau', 'gelb')",
     solution="""farben = ('rot', 'grün', 'blau', 'gelb')
for f in farben:
    print(f)""")
task('Berechne mit einer Schleife die Summe der Zahlen in `zahlen` und gib sie aus.',
     given=ZT, solution=ZT + """
summe = 0
for z in zahlen:
    summe += z
print(summe)""")
task('Gib die Wochentage nummeriert aus wie unten. Verwende `range()` und `len()`.',
     given="tage = ('Mo', 'Di', 'Mi', 'Do', 'Fr')",
     solution="""tage = ('Mo', 'Di', 'Mi', 'Do', 'Fr')
for i in range(len(tage)):
    print(f'{i + 1}. {tage[i]}')""")
task('Zähle, wie viele Zahlen in `zahlen` größer als 10 sind. Gib die Anzahl aus.',
     given=ZT, solution=ZT + """
anzahl = 0
for z in zahlen:
    if z > 10:
        anzahl += 1
print(anzahl)""")
task('Gib die Elemente von `zahlen` mit einer `while`-Schleife rückwärts aus, jedes in einer eigenen Zeile.',
     given=ZT, solution=ZT + """
i = len(zahlen) - 1
while i >= 0:
    print(zahlen[i])
    i -= 1""")
task('Erzeuge ein neues Tupel, in dem jede Zahl aus `zahlen` verdoppelt ist. Sammle die Werte zuerst in einer Liste. Gib das Tupel aus.',
     given=ZT, solution=ZT + """
liste = []
for z in zahlen:
    liste.append(2 * z)
doppelt = tuple(liste)
print(doppelt)""")
task('Gib jeden Punkt aus `punkte` aus wie unten. Entpacke die Punkte dazu in der `for`-Schleife.',
     given='punkte = [(1, 2), (3, 4), (5, 6)]',
     solution="""punkte = [(1, 2), (3, 4), (5, 6)]
for x, y in punkte:
    print(f'x = {x}, y = {y}')""")
SCH = "schueler = [('Ali', 2), ('Bea', 1), ('Cem', 3), ('Dana', 2)]"
task('Gib jeden Namen mit seiner Note aus wie unten.',
     given=SCH, solution=SCH + """
for name, note in schueler:
    print(f'{name}: {note}')""")
task('Berechne den Notendurchschnitt der Schüler und gib ihn aus.',
     given=SCH, solution=SCH + """
summe = 0
for name, note in schueler:
    summe += note
print(summe / len(schueler))""")
task('Finde mit einer Schleife den Namen des Schülers mit der besten (kleinsten) Note und gib ihn aus.',
     given=SCH, solution=SCH + """
bester_name, beste_note = schueler[0]
for name, note in schueler:
    if note < beste_note:
        bester_name = name
        beste_note = note
print(bester_name)""")
task('Gib alle Namen aus, deren Note besser als 3 ist.',
     given=SCH, solution=SCH + """
for name, note in schueler:
    if note < 3:
        print(name)""")
predict("""paare = [(1, 'a'), (2, 'b'), (3, 'c')]
for zahl, buchstabe in paare:
    print(buchstabe * zahl)""")

# ---------------------------------------------------------------- 6
sec('Verbinden, wiederholen und vergleichen')
expl('''#### `+` und `*`

- `a + b` verbindet zwei Tupel zu einem neuen Tupel.
- `t * n` erzeugt ein neues Tupel, in dem die Elemente von `t` `n`-mal hintereinander stehen.''',
     """a = (1, 2)
b = (3, 4)
print(a + b)
print(a * 3)
print((0,) * 5)""")
expl('''#### Vergleichen mit `==`

`a == b` ist `True`, wenn beide Tupel dieselben Elemente in derselben Reihenfolge haben.''',
     """print((1, 2) == (1, 2))
print((1, 2) == (2, 1))""")

task('Verbinde `a` und `b` mit `+` zu einem neuen Tupel `c`. Gib `c` aus.',
     given="""a = ('x', 'y')
b = ('z',)""",
     solution="""a = ('x', 'y')
b = ('z',)
c = a + b
print(c)""")
task('Erzeuge mit `*` ein Tupel aus fünf Nullen. Gib es aus.',
     solution="""print((0,) * 5)""")
task("Erzeuge mit `*` aus `antworten` ein Tupel, in dem `'ja'` und `'nein'` dreimal abwechselnd vorkommen. Gib es aus.",
     given="antworten = ('ja', 'nein')",
     solution="""antworten = ('ja', 'nein')
print(antworten * 3)""")
task('Verbinde die drei Tupel in der Reihenfolge `vorne`, `mitte`, `hinten`. Gib das Ergebnis und seine Länge aus.',
     given="""vorne = (1, 2)
mitte = (3, 4, 5)
hinten = (6,)""",
     solution="""vorne = (1, 2)
mitte = (3, 4, 5)
hinten = (6,)
t = vorne + mitte + hinten
print(t)
print(len(t))""")
task("Gib aus, ob `start` und `ziel` derselbe Punkt sind. Gib `gleich` oder `verschieden` aus.",
     given="""start = (2, 5)
ziel = (5, 2)""",
     solution="""start = (2, 5)
ziel = (5, 2)
if start == ziel:
    print('gleich')
else:
    print('verschieden')""")
predict("""a = (1, 2)
b = a * 2 + (3,)
print(b)
print(len(b))
print(a + a == a * 2)""")

# ---------------------------------------------------------------- 7
sec('Methoden und Funktionen')
expl('''#### `count()` und `index()`

Tupel haben nur zwei Methoden:

- `t.count(wert)` gibt zurück, wie oft `wert` im Tupel vorkommt.
- `t.index(wert)` gibt den Index des ersten Vorkommens zurück (oder einen `ValueError`).''',
     """t = (3, 1, 3, 2)
print(t.count(3))
print(t.index(2))""")
expl('''#### `sum()`, `min()`, `max()` und `sorted()`

- `sum(t)`, `min(t)` und `max(t)` funktionieren wie bei Listen.
- `sorted(t)` gibt eine **sortierte Liste** zurück. Das Tupel selbst bleibt unverändert.
  Mit `sorted(t, reverse=True)` wird absteigend sortiert. Mit `tuple(sorted(t))` erhält man wieder ein Tupel.''',
     """t = (5, 2, 8, 1)
print(sum(t), min(t), max(t))
print(sorted(t))
print(tuple(sorted(t, reverse=True)))
print(t)""")

WT = 'wuerfe = (6, 2, 6, 3, 1, 6, 4, 2, 5, 2)'
task('Gib mit `count()` aus, wie oft eine 6 gewürfelt wurde.',
     given=WT, solution=WT + """
print(wuerfe.count(6))""")
task("Gib mit `index()` aus, an welcher Stelle `'Mär'` in `monate` steht.",
     given=MONATE, solution=MONATE + """
print(monate.index('Mär'))""")
task('Gib Summe, Minimum und Maximum von `wuerfe` aus, jeweils in einer eigenen Zeile.',
     given=WT, solution=WT + """
print(sum(wuerfe))
print(min(wuerfe))
print(max(wuerfe))""")
task('Berechne mit `sum()` und `len()` den Durchschnitt der Würfe und gib ihn aus.',
     given=WT, solution=WT + """
print(sum(wuerfe) / len(wuerfe))""")
task('Gib die Würfe mit `sorted()` aufsteigend sortiert als **Tupel** aus.',
     given=WT, solution=WT + """
print(tuple(sorted(wuerfe)))""")
task('Gib die Namen in `namen` absteigend sortiert als Liste aus.',
     given="namen = ('Lukas', 'Emma', 'Noah', 'Mia')",
     solution="""namen = ('Lukas', 'Emma', 'Noah', 'Mia')
print(sorted(namen, reverse=True))""")
task('Gib für jede Augenzahl von 1 bis 6 aus, wie oft sie gewürfelt wurde.',
     given=WT, solution=WT + """
for augen in range(1, 7):
    print(augen, wuerfe.count(augen))""")
task("""Wenn `tier` in `tiere` vorkommt, gib seinen Index aus, sonst `nicht gefunden`.
Teste dein Programm auch mit `tier = 'Esel'`.""",
     given="""tiere = ('Hund', 'Katze', 'Maus')
tier = 'Maus'""",
     solution="""tiere = ('Hund', 'Katze', 'Maus')
tier = 'Maus'
if tier in tiere:
    print(tiere.index(tier))
else:
    print('nicht gefunden')""")
task('Gib die Differenz zwischen der höchsten und der niedrigsten Temperatur aus.',
     given='temperaturen = (14, 19, 11, 22, 17, 9, 15)',
     solution="""temperaturen = (14, 19, 11, 22, 17, 9, 15)
print(max(temperaturen) - min(temperaturen))""")
predict("""t = (3, 1, 3, 2)
print(t.count(3))
print(t.index(3))
print(sorted(t))
print(t)
print(max(t) + min(t))""")

# ---------------------------------------------------------------- 8
sec('Tupel als Rückgabewert von Funktionen')
expl('''#### Mehrere Werte zurückgeben

Eine Funktion kann mit `return a, b` **mehrere Werte** zurückgeben. Zurückgegeben wird dann ein Tupel.
Beim Aufruf kann man es direkt entpacken: `x, y = funktion()`.''',
     """def summe_und_produkt(a, b):
    return a + b, a * b

ergebnis = summe_und_produkt(3, 4)
print(ergebnis)
s, p = summe_und_produkt(3, 4)
print(s)
print(p)""")

task('''Schreibe eine Funktion `min_max(zahlen)`, die das Minimum und das Maximum zurückgibt.
Rufe sie mit der Liste `[4, 9, 1, 7]` auf, entpacke das Ergebnis und gib beide Werte aus wie unten.''',
     solution="""def min_max(zahlen):
    return min(zahlen), max(zahlen)

kleinste, groesste = min_max([4, 9, 1, 7])
print(f'Minimum: {kleinste}, Maximum: {groesste}')""")
task('''Schreibe eine Funktion `teile(a, b)`, die das Ergebnis der ganzzahligen Division `a // b` und den Rest `a % b` zurückgibt.
Rufe sie mit 17 und 5 auf und gib beide Werte aus wie unten.''',
     solution="""def teile(a, b):
    return a // b, a % b

ganz, rest = teile(17, 5)
print(f'17 : 5 = {ganz} Rest {rest}')""")
task('''Schreibe eine Funktion `statistik(zahlen)`, die die Summe und den Durchschnitt einer Liste zurückgibt.
Rufe sie mit `[2, 4, 6, 8]` auf und gib beide Werte aus.''',
     solution="""def statistik(zahlen):
    summe = sum(zahlen)
    return summe, summe / len(zahlen)

s, d = statistik([2, 4, 6, 8])
print(s)
print(d)""")
task('''Schreibe eine Funktion `mittelpunkt(p, q)`, die für zwei Punkte (als Tupel) den Mittelpunkt als Tupel zurückgibt.
Rufe sie mit `(1, 2)` und `(5, 8)` auf und gib das Ergebnis aus.''',
     solution="""def mittelpunkt(p, q):
    return (p[0] + q[0]) / 2, (p[1] + q[1]) / 2

print(mittelpunkt((1, 2), (5, 8)))""")
task('''Schreibe eine Funktion `zaehle(text)`, die die Anzahl der Vokale (a, e, i, o, u) und die Anzahl der anderen Zeichen zurückgibt.
Rufe sie mit `'programmieren'` auf und gib beide Werte aus.''',
     solution="""def zaehle(text):
    vokale = 0
    andere = 0
    for c in text:
        if c in 'aeiou':
            vokale += 1
        else:
            andere += 1
    return vokale, andere

v, a = zaehle('programmieren')
print(v, a)""")
predict("""def f(x):
    return x, x * x

a = f(3)
b, c = f(4)
print(a)
print(b, c)""")

# ---------------------------------------------------------------- 9
sec('Gemischte Übungen')
task('Berechne den Abstand der Punkte `p` und `q` mit dem Satz des Pythagoras. Die Wurzel ziehst du mit `** 0.5`. Gib den Abstand aus.',
     given="""p = (1, 2)
q = (4, 6)""",
     solution="""p = (1, 2)
q = (4, 6)
dx = q[0] - p[0]
dy = q[1] - p[1]
print((dx ** 2 + dy ** 2) ** 0.5)""")
ERG = "ergebnisse = [('Ali', 72), ('Bea', 45), ('Cem', 88), ('Dana', 50), ('Eli', 31)]"
task('Gib die Namen aller Personen aus, die mindestens 50 Punkte haben.',
     given=ERG, solution=ERG + """
for name, punkte in ergebnisse:
    if punkte >= 50:
        print(name)""")
task('''Sortiere `ergebnisse` absteigend nach den Punkten. Schreibe dazu eine Funktion `punkte(eintrag)`,
die das zweite Element eines Tupels zurückgibt, und verwende sie als `key`. Gib die Liste aus.''',
     given=ERG, solution=ERG + """

def punkte(eintrag):
    return eintrag[1]

ergebnisse.sort(key=punkte, reverse=True)
print(ergebnisse)""")
task('Erstelle aus den beiden Tupeln eine Liste von Tupeln `(name, alter)`. Gib die Liste aus.',
     given="""namen = ('Ali', 'Bea', 'Cem')
alter = (16, 17, 15)""",
     solution="""namen = ('Ali', 'Bea', 'Cem')
alter = (16, 17, 15)
personen = []
for i in range(len(namen)):
    personen.append((namen[i], alter[i]))
print(personen)""")
task('Verschiebe jeden Punkt in `punkte` um 1 nach rechts und um 2 nach oben. Erstelle dazu eine neue Liste von Tupeln und gib sie aus.',
     given='punkte = [(0, 0), (3, 1), (-2, 4)]',
     solution="""punkte = [(0, 0), (3, 1), (-2, 4)]
neu = []
for x, y in punkte:
    neu.append((x + 1, y + 2))
print(neu)""")
task('Zähle, wie viele Punkte in `punkte` im ersten Quadranten liegen, also bei denen x und y beide größer als 0 sind. Gib die Anzahl aus.',
     given='punkte = [(1, 2), (-3, 4), (5, -1), (2, 2), (0, 3), (7, 8)]',
     solution="""punkte = [(1, 2), (-3, 4), (5, -1), (2, 2), (0, 3), (7, 8)]
anzahl = 0
for x, y in punkte:
    if x > 0 and y > 0:
        anzahl += 1
print(anzahl)""")
task('Entpacke `datum` und gib es in der Form unten aus. Tag und Monat sollen immer zweistellig sein (Formatangabe `:02d`).',
     given='datum = (2026, 3, 5)',
     solution="""datum = (2026, 3, 5)
jahr, monat, tag = datum
print(f'{tag:02d}.{monat:02d}.{jahr}')""")
task("Prüfe, ob das Tupel `noten` aufsteigend sortiert ist. Vergleiche es dazu mit `tuple(sorted(noten))`. Gib `sortiert` oder `nicht sortiert` aus.",
     given='noten = (1, 2, 2, 4, 3)',
     solution="""noten = (1, 2, 2, 4, 3)
if noten == tuple(sorted(noten)):
    print('sortiert')
else:
    print('nicht sortiert')""")
KORB = "korb = [('Milch', 2, 3), ('Brot', 4, 1), ('Käse', 5, 2)]"
task('Jedes Tupel in `korb` enthält Produkt, Einzelpreis und Anzahl. Gib für jedes Produkt den Gesamtpreis aus wie unten und danach die Summe.',
     given=KORB, solution=KORB + """
summe = 0
for produkt, preis, anzahl in korb:
    gesamt = preis * anzahl
    summe += gesamt
    print(f'{produkt}: {gesamt} Euro')
print(f'Summe: {summe} Euro')""")
task('Finde das Produkt mit dem höchsten Einzelpreis in `korb` und gib seinen Namen aus.',
     given=KORB, solution=KORB + """
teuerstes = korb[0]
for eintrag in korb:
    if eintrag[1] > teuerstes[1]:
        teuerstes = eintrag
print(teuerstes[0])""")
task('Berechne mit den Tupeln in `strecken` die gesamte zurückgelegte Strecke. Jedes Tupel enthält Geschwindigkeit in km/h und Fahrzeit in Stunden.',
     given='strecken = [(50, 2), (100, 1), (30, 3)]',
     solution="""strecken = [(50, 2), (100, 1), (30, 3)]
gesamt = 0
for v, t in strecken:
    gesamt += v * t
print(gesamt)""")
task('Erstelle eine Liste mit allen Tupeln `(a, b)`, bei denen `a` und `b` zwischen 1 und 3 liegen und `a < b` ist. Verwende zwei verschachtelte Schleifen.',
     solution="""paare = []
for a in range(1, 4):
    for b in range(1, 4):
        if a < b:
            paare.append((a, b))
print(paare)""")
predict("""daten = [('a', 3), ('b', 1), ('c', 2)]
gesamt = 0
for name, zahl in daten:
    gesamt += zahl
print(gesamt)
print(daten[1][0] * daten[0][1])""")

generate('tupel', 'Tupel')
