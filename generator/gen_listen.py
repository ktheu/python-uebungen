# Erzeugt ../content/listen.ipynb (siehe nbgen.py).
from nbgen import sec, expl, task, predict, generate

# ---------------------------------------------------------------- 1
sec('Listen erstellen')
expl('''#### Was ist eine Liste?

Eine **Liste** speichert mehrere Werte in einer einzigen Variablen. Die Werte stehen in eckigen Klammern
und werden durch Kommas getrennt. Die Werte in einer Liste heißen **Elemente**.

- Listen sind **geordnet**: Die Elemente haben eine feste Reihenfolge.
- Listen sind **veränderbar**: Man kann Elemente ändern, hinzufügen und entfernen.
- Listen dürfen **Duplikate** enthalten, also denselben Wert mehrmals.
- Eine Liste kann Elemente **verschiedener Datentypen** enthalten.
- `[]` ist eine **leere Liste**.''',
     '''zahlen = [3, 7, 1, 7]
gemischt = [42, 'Hallo', 3.5, True]
leer = []
print(zahlen)
print(gemischt)
print(leer)''')
expl('''#### `len()`

`len(liste)` gibt die **Anzahl der Elemente** einer Liste zurück.
`len()` funktioniert auch bei Zeichenketten. Dann ist das Ergebnis die Anzahl der Zeichen.''',
     '''farben = ['rot', 'grün', 'blau']
print(len(farben))
print(len([]))
print(len('Hallo'))''')
expl('''#### `type()`

`type(wert)` gibt den **Datentyp** eines Wertes zurück. Bei einer Liste ist das `list`.''',
     '''farben = ['rot', 'grün', 'blau']
print(type(farben))
print(type(42))''')
expl('''#### `list()`

`list(...)` erzeugt eine **neue Liste**.

- `list(range(...))` macht aus einem Zahlenbereich eine Liste. Zur Erinnerung: `range(start, stop, schritt)`
  erzeugt die Zahlen von `start` bis **ausschließlich** `stop` mit der Schrittweite `schritt`.
- `list('Text')` macht aus einer Zeichenkette eine Liste mit den einzelnen Zeichen.
- `list()` ohne Argument ergibt eine leere Liste.''',
     '''print(list(range(5)))
print(list(range(2, 12, 3)))
print(list('Hallo'))
print(list())''')

task('Erstelle eine Liste `farben` mit den Elementen `\'rot\'`, `\'grün\'` und `\'blau\'`. Gib die Liste aus.',
     solution='''farben = ['rot', 'grün', 'blau']
print(farben)''')
task('Erstelle eine Liste `primzahlen` mit den ersten fünf Primzahlen. Gib die Liste und danach ihre Länge aus.',
     solution='''primzahlen = [2, 3, 5, 7, 11]
print(primzahlen)
print(len(primzahlen))''')
task('Erstelle eine leere Liste `einkauf`. Gib die Liste und ihre Länge aus.',
     solution='''einkauf = []
print(einkauf)
print(len(einkauf))''')
task('Gib mit `len()` aus, wie viele Tiere in der Liste `tiere` stehen. Die Ausgabe soll so aussehen wie unten.',
     given="tiere = ['Hund', 'Katze', 'Maus', 'Pferd', 'Esel', 'Kuh']",
     solution='''tiere = ['Hund', 'Katze', 'Maus', 'Pferd', 'Esel', 'Kuh']
print(f'Es sind {len(tiere)} Tiere.')''')
task('Erstelle mit `list()` und `range()` eine Liste mit den Zahlen von 0 bis 9. Gib die Liste aus.',
     solution='''zahlen = list(range(10))
print(zahlen)''')
task('Erstelle mit `list()` und `range()` eine Liste mit den Zahlen 10, 20, 30, ..., 100. Gib die Liste aus.',
     solution='''zehner = list(range(10, 101, 10))
print(zehner)''')
task('Erstelle mit `list()` eine Liste mit den Buchstaben des Wortes `\'Python\'`. Gib die Liste aus.',
     solution='''buchstaben = list('Python')
print(buchstaben)''')
task('Erstelle mit `list()` und `range()` eine Liste mit den Zahlen 20, 18, 16, ..., 2. Gib die Liste aus.',
     solution='''zahlen = list(range(20, 0, -2))
print(zahlen)''')
task('''Erstelle eine Liste `steckbrief` mit vier Elementen: deinem Vornamen (Zeichenkette), deinem Alter (ganze Zahl),
deiner Größe in Metern (Kommazahl) und ob du ein Haustier hast (`True` oder `False`).
Gib die Liste und danach mit `type()` ihren Datentyp aus.''',
     solution='''steckbrief = ['Mia', 16, 1.68, True]
print(steckbrief)
print(type(steckbrief))''', kind='free')
predict('''a = [1, 'zwei', 3.0, [4, 5]]
b = []
c = list('abc')
print(len(a))
print(len(b))
print(len(c))
print(type(c))''')

# ---------------------------------------------------------------- 2
sec('Auf Elemente zugreifen')
expl('''#### Zugriff über den Index

Jedes Element hat eine Position, den **Index**. Das erste Element hat den Index **0**,
das zweite den Index 1 usw. Mit `liste[index]` greift man auf ein Element zu.

Das letzte Element hat den Index `len(liste) - 1`. Ist der Index zu groß, gibt es einen `IndexError`.

Auch bei Zeichenketten kann man so auf einzelne Zeichen zugreifen: `'Hallo'[0]` ist `'H'`.''',
     '''tiere = ['Hund', 'Katze', 'Maus', 'Pferd']
print(tiere[0])
print(tiere[2])
print(tiere[len(tiere) - 1])
print(tiere[1][0])''')
expl('''#### Negativer Index

Ein negativer Index zählt **von hinten**: `liste[-1]` ist das letzte Element, `liste[-2]` das vorletzte usw.''',
     '''tiere = ['Hund', 'Katze', 'Maus', 'Pferd']
print(tiere[-1])
print(tiere[-2])''')
expl('''#### Bereiche (Slicing)

Mit `liste[start:stop]` erhält man eine **neue Liste** mit den Elementen von Index `start` bis
**ausschließlich** Index `stop`.

- Fehlt `start`, beginnt der Bereich am Anfang: `liste[:3]`.
- Fehlt `stop`, geht der Bereich bis zum Ende: `liste[2:]`.
- Negative Indizes sind auch erlaubt: `liste[-3:]` sind die letzten drei Elemente.
- Ein Bereich darf über das Ende hinausgehen. Das führt nicht zu einem Fehler.''',
     '''zahlen = [10, 20, 30, 40, 50, 60]
print(zahlen[1:4])
print(zahlen[:3])
print(zahlen[2:])
print(zahlen[-3:])
print(zahlen[-4:-1])
print(zahlen[4:100])''')
expl('''#### `in` und `not in`

Mit `wert in liste` prüft man, ob ein Wert in der Liste vorkommt. Das Ergebnis ist `True` oder `False`.
`wert not in liste` ist das Gegenteil.''',
     '''obst = ['Apfel', 'Birne', 'Kirsche']
print('Birne' in obst)
print('Mango' in obst)
print('Mango' not in obst)
if 'Apfel' in obst:
    print('Es gibt Äpfel.')''')

STAEDTE = "staedte = ['Berlin', 'Hamburg', 'München', 'Köln', 'Frankfurt', 'Stuttgart', 'Düsseldorf']"
ZAHLEN8 = 'zahlen = [5, 12, 8, 3, 19, 7, 14, 2]'
task('Gib das erste und das dritte Element der Liste `staedte` aus, jeweils in einer eigenen Zeile.',
     given=STAEDTE, solution=STAEDTE + '''
print(staedte[0])
print(staedte[2])''')
task('Gib das letzte Element von `staedte` zweimal aus: einmal mit einem negativen Index und einmal mit `len()`.',
     given=STAEDTE, solution=STAEDTE + '''
print(staedte[-1])
print(staedte[len(staedte) - 1])''')
task('Gib das vorletzte Element von `staedte` aus.',
     given=STAEDTE, solution=STAEDTE + '''
print(staedte[-2])''')
task('Gib mit Slicing eine Liste mit den ersten drei Elementen von `zahlen` aus.',
     given=ZAHLEN8, solution=ZAHLEN8 + '''
print(zahlen[:3])''')
task('Gib mit Slicing alle Elemente von `zahlen` ab Index 4 aus.',
     given=ZAHLEN8, solution=ZAHLEN8 + '''
print(zahlen[4:])''')
task('Gib mit Slicing und negativen Indizes die letzten drei Elemente von `zahlen` aus.',
     given=ZAHLEN8, solution=ZAHLEN8 + '''
print(zahlen[-3:])''')
task('Gib die Elemente von `zahlen` von Index 2 bis **einschließlich** Index 5 aus.',
     given=ZAHLEN8, solution=ZAHLEN8 + '''
print(zahlen[2:6])''')
task('Gib alle Elemente von `zahlen` außer dem ersten und dem letzten aus.',
     given=ZAHLEN8, solution=ZAHLEN8 + '''
print(zahlen[1:-1])''')
task('Berechne die Summe aus dem ersten und dem letzten Element von `zahlen` und gib sie aus.',
     given=ZAHLEN8, solution=ZAHLEN8 + '''
print(zahlen[0] + zahlen[-1])''')
task('''Speichere mit Slicing die Werktage (Montag bis Freitag) in der Liste `werktage`
und das Wochenende in der Liste `wochenende`. Gib beide Listen aus.''',
     given="woche = ['Mo', 'Di', 'Mi', 'Do', 'Fr', 'Sa', 'So']",
     solution='''woche = ['Mo', 'Di', 'Mi', 'Do', 'Fr', 'Sa', 'So']
werktage = woche[:5]
wochenende = woche[5:]
print(werktage)
print(wochenende)''')
task("Gib mit Slicing die Liste `['f', 'o', 'r', 'm']` aus der Liste `buchstaben` aus.",
     given="buchstaben = list('Informatik')",
     solution='''buchstaben = list('Informatik')
print(buchstaben[2:6])''')
task('''Prüfe mit `in`, ob die Variable `frucht` in der Liste `obst` vorkommt, und gib einen passenden Satz aus.
Teste dein Programm auch mit `frucht = 'Mango'`. Dann soll `Mango ist nicht in der Liste.` ausgegeben werden.''',
     given='''obst = ['Apfel', 'Birne', 'Kirsche', 'Banane']
frucht = 'Kirsche\'''',
     solution='''obst = ['Apfel', 'Birne', 'Kirsche', 'Banane']
frucht = 'Kirsche'
if frucht in obst:
    print(f'{frucht} ist in der Liste.')
else:
    print(f'{frucht} ist nicht in der Liste.')''')
task('Gib das mittlere Element der Liste `noten` aus. Berechne dazu den Index mit `len()` und `//`.',
     given='noten = [2, 3, 1, 4, 2, 5, 3]',
     solution='''noten = [2, 3, 1, 4, 2, 5, 3]
print(noten[len(noten) // 2])''')
predict('''a = [10, 20, 30, 40, 50, 60]
print(a[1])
print(a[-2])
print(a[1:4])
print(a[:2])
print(a[4:])
print(a[-3:-1])
print(25 in a)''')
predict('''b = ['x', 'y', 'z']
print(b[len(b) - 1])
print(b[0:10])
print(b[3])''', error=IndexError)

# ---------------------------------------------------------------- 3
sec('Elemente ändern')
expl('''#### Ein Element ändern

Mit `liste[index] = wert` ersetzt man das Element an der Stelle `index` durch einen neuen Wert.
Auch negative Indizes sind erlaubt.''',
     '''tiere = ['Hund', 'Katze', 'Maus']
tiere[1] = 'Pferd'
tiere[-1] = 'Esel'
print(tiere)''')
expl('''#### Einen Bereich ändern

Mit `liste[start:stop] = [...]` ersetzt man einen ganzen Bereich durch die Elemente einer anderen Liste.
Hat die neue Liste mehr oder weniger Elemente als der Bereich, wird die Liste länger oder kürzer.''',
     '''a = [1, 2, 3, 4, 5]
a[1:3] = [20, 30]
print(a)
a[1:3] = [0]
print(a)
a[1:2] = [7, 8, 9]
print(a)''')

task("Ändere das zweite Element von `farben` in `'gelb'`. Gib die Liste aus.",
     given="farben = ['rot', 'grün', 'blau']",
     solution='''farben = ['rot', 'grün', 'blau']
farben[1] = 'gelb'
print(farben)''')
task('Der letzte Messwert in `temperaturen` ist falsch, er muss 18 heißen. Ändere ihn mit einem negativen Index. Gib die Liste aus.',
     given='temperaturen = [12, 15, 9, 17, 14]',
     solution='''temperaturen = [12, 15, 9, 17, 14]
temperaturen[-1] = 18
print(temperaturen)''')
task('Ändere das erste Element von `a` in 100 und das dritte Element in 300. Gib die Liste aus.',
     given='a = [1, 2, 3, 4]',
     solution='''a = [1, 2, 3, 4]
a[0] = 100
a[2] = 300
print(a)''')
task('Ersetze in `zahlen` mit **einer** Anweisung die Elemente an Index 1 und 2 durch 20 und 30. Gib die Liste aus.',
     given='zahlen = [1, 2, 3, 4, 5, 6]',
     solution='''zahlen = [1, 2, 3, 4, 5, 6]
zahlen[1:3] = [20, 30]
print(zahlen)''')
task('Ersetze in `zahlen` die Elemente 2, 3 und 4 mit **einer** Anweisung durch die einzelne Zahl 0. Gib die Liste aus.',
     given='zahlen = [1, 2, 3, 4, 5, 6]',
     solution='''zahlen = [1, 2, 3, 4, 5, 6]
zahlen[1:4] = [0]
print(zahlen)''')
task('Verdopple das erste Element von `a` und verringere das letzte Element um 5. Gib die Liste aus.',
     given='a = [4, 8, 15, 16]',
     solution='''a = [4, 8, 15, 16]
a[0] = a[0] * 2
a[-1] = a[-1] - 5
print(a)''')
task('Vertausche das erste und das letzte Element von `punkte`. Verwende dazu eine Hilfsvariable. Gib die Liste aus.',
     given='punkte = [3, 5, 2, 7]',
     solution='''punkte = [3, 5, 2, 7]
hilf = punkte[0]
punkte[0] = punkte[-1]
punkte[-1] = hilf
print(punkte)''')
task("""Die Sportstunde fällt aus. Ersetze `'Sport'` mit **einer** Anweisung durch die beiden Fächer `'Physik'` und `'Chemie'`.
Gib den Stundenplan aus.""",
     given="stundenplan = ['Mathe', 'Deutsch', 'Sport', 'Englisch', 'Info']",
     solution='''stundenplan = ['Mathe', 'Deutsch', 'Sport', 'Englisch', 'Info']
stundenplan[2:3] = ['Physik', 'Chemie']
print(stundenplan)''')
task("Ersetze die ersten beiden Elemente von `woerter` durch `'eins'` und `'zwei'`. Gib die Liste aus.",
     given="woerter = ['a', 'b', 'c', 'd']",
     solution='''woerter = ['a', 'b', 'c', 'd']
woerter[:2] = ['eins', 'zwei']
print(woerter)''')
predict('''a = ['A', 'B', 'C', 'D']
a[1] = 'X'
a[-1] = a[0]
a[1:3] = ['Y']
print(a)
print(len(a))''')

# ---------------------------------------------------------------- 4
sec('Elemente hinzufügen')
expl('''#### `append()`

`liste.append(wert)` hängt einen Wert **am Ende** der Liste an.''',
     '''einkauf = ['Milch', 'Brot']
einkauf.append('Eier')
print(einkauf)''')
expl('''#### `insert()`

`liste.insert(index, wert)` fügt einen Wert **an der Stelle** `index` ein.
Die Elemente ab dieser Stelle rücken eine Position nach hinten.''',
     '''einkauf = ['Milch', 'Brot']
einkauf.insert(0, 'Kaffee')
einkauf.insert(2, 'Zucker')
print(einkauf)''')
expl('''#### `extend()`

`liste.extend(andere_liste)` hängt **alle Elemente** einer anderen Liste am Ende an.''',
     '''a = [1, 2, 3]
b = [4, 5]
a.extend(b)
print(a)
print(b)''')

task("Füge mit `append()` das Element `'Eier'` am Ende von `einkauf` an. Gib die Liste aus.",
     given="einkauf = ['Milch', 'Brot']",
     solution='''einkauf = ['Milch', 'Brot']
einkauf.append('Eier')
print(einkauf)''')
task("Füge mit `append()` nacheinander `'Butter'`, `'Käse'` und `'Äpfel'` an `einkauf` an. Gib die Liste aus.",
     given="einkauf = ['Milch', 'Brot']",
     solution='''einkauf = ['Milch', 'Brot']
einkauf.append('Butter')
einkauf.append('Käse')
einkauf.append('Äpfel')
print(einkauf)''')
task("Füge mit `insert()` das Element `'Kaffee'` am Anfang von `einkauf` ein. Gib die Liste aus.",
     given="einkauf = ['Milch', 'Brot']",
     solution='''einkauf = ['Milch', 'Brot']
einkauf.insert(0, 'Kaffee')
print(einkauf)''')
task('Füge mit `insert()` die Zahl 3 an der richtigen Stelle in `zahlen` ein. Gib die Liste aus.',
     given='zahlen = [1, 2, 4, 5]',
     solution='''zahlen = [1, 2, 4, 5]
zahlen.insert(2, 3)
print(zahlen)''')
task('Hänge mit `extend()` die Liste `b` an die Liste `a` an. Gib danach `a` und `b` aus.',
     given='''a = [1, 2, 3]
b = [4, 5, 6]''',
     solution='''a = [1, 2, 3]
b = [4, 5, 6]
a.extend(b)
print(a)
print(b)''')
task("Erstelle eine leere Liste `tage`. Füge mit `append()` die Elemente `'Mo'`, `'Di'` und `'Mi'` hinzu. Gib die Liste und ihre Länge aus.",
     solution='''tage = []
tage.append('Mo')
tage.append('Di')
tage.append('Mi')
print(tage)
print(len(tage))''')
task("""In der Warteschlange stehen Tom und Lisa. Danach passiert Folgendes:
`'Max'` stellt sich hinten an. `'Oma Erna'` darf ganz nach vorne. `'Jan'` drängelt sich an die zweite Stelle.
Ändere die Liste entsprechend und gib sie aus.""",
     given="warteschlange = ['Tom', 'Lisa']",
     solution='''warteschlange = ['Tom', 'Lisa']
warteschlange.append('Max')
warteschlange.insert(0, 'Oma Erna')
warteschlange.insert(1, 'Jan')
print(warteschlange)''')
task('Füge mit `extend()` die Zahlen 7, 8 und 9 an `zahlen` an. Füge danach mit `insert()` die Zahl 0 am Anfang ein. Gib die Liste aus.',
     given='zahlen = [4, 5, 6]',
     solution='''zahlen = [4, 5, 6]
zahlen.extend([7, 8, 9])
zahlen.insert(0, 0)
print(zahlen)''')
task('Füge mit `insert()` und `len()` die Zahl 99 so in `a` ein, dass sie das vorletzte Element wird. Gib die Liste aus.',
     given='a = [1, 2, 3, 4, 5]',
     solution='''a = [1, 2, 3, 4, 5]
a.insert(len(a) - 1, 99)
print(a)''')
predict('''a = [1, 2]
a.append([3, 4])
print(a)
print(len(a))
b = [1, 2]
b.extend([3, 4])
print(b)
print(len(b))''')
predict('''a = ['x', 'y', 'z']
a.insert(1, 'A')
a.insert(-1, 'B')
a.insert(100, 'C')
print(a)''')

# ---------------------------------------------------------------- 5
sec('Elemente entfernen')
expl('''#### `remove()`

`liste.remove(wert)` entfernt das **erste Vorkommen** eines Wertes.
Kommt der Wert nicht in der Liste vor, gibt es einen `ValueError`.''',
     '''zahlen = [3, 7, 3, 9]
zahlen.remove(3)
print(zahlen)''')
expl('''#### `pop()`

`liste.pop(index)` entfernt das Element an der Stelle `index` und **gibt es zurück**.
Ohne Index entfernt `pop()` das **letzte** Element.''',
     '''tiere = ['Hund', 'Katze', 'Maus', 'Pferd']
letztes = tiere.pop()
zweites = tiere.pop(1)
print(letztes)
print(zweites)
print(tiere)''')
expl('''#### `del`

`del liste[index]` löscht das Element an der Stelle `index`.
Mit `del liste[start:stop]` löscht man einen ganzen Bereich.
`del liste` löscht die ganze Variable. Danach gibt es die Liste nicht mehr.''',
     '''a = [10, 20, 30, 40, 50, 60]
del a[0]
print(a)
del a[1:3]
print(a)''')
expl('''#### `clear()`

`liste.clear()` entfernt **alle** Elemente. Die Liste ist danach leer, existiert aber noch.''',
     '''a = [1, 2, 3]
a.clear()
print(a)''')

task("Entferne mit `remove()` das Element `'grün'` aus `farben`. Gib die Liste aus.",
     given="farben = ['rot', 'grün', 'blau', 'gelb']",
     solution='''farben = ['rot', 'grün', 'blau', 'gelb']
farben.remove('grün')
print(farben)''')
task('Entferne mit `remove()` die erste 3 aus `zahlen`. Gib die Liste aus.',
     given='zahlen = [3, 7, 3, 9, 3]',
     solution='''zahlen = [3, 7, 3, 9, 3]
zahlen.remove(3)
print(zahlen)''')
task('Entferne **alle** Dreien aus `zahlen`. Verwende eine `while`-Schleife, `in` und `remove()`. Gib die Liste aus.',
     given='zahlen = [3, 7, 3, 9, 3]',
     solution='''zahlen = [3, 7, 3, 9, 3]
while 3 in zahlen:
    zahlen.remove(3)
print(zahlen)''')
task('Entferne mit `pop()` das letzte Buch vom `stapel` und speichere es in der Variablen `buch`. Gib `buch` und `stapel` aus.',
     given="stapel = ['Buch1', 'Buch2', 'Buch3', 'Buch4']",
     solution='''stapel = ['Buch1', 'Buch2', 'Buch3', 'Buch4']
buch = stapel.pop()
print(buch)
print(stapel)''')
task('Entferne mit `pop()` das Element an Index 1 aus `noten`. Gib das entfernte Element und danach die Liste aus.',
     given='noten = [2, 5, 1, 3]',
     solution='''noten = [2, 5, 1, 3]
x = noten.pop(1)
print(x)
print(noten)''')
task('Lösche mit `del` das erste Element von `a`. Gib die Liste aus.',
     given='a = [10, 20, 30, 40, 50]',
     solution='''a = [10, 20, 30, 40, 50]
del a[0]
print(a)''')
task('Lösche mit `del` die Elemente an Index 2 bis einschließlich Index 4 aus `a`. Gib die Liste aus.',
     given='a = [10, 20, 30, 40, 50, 60, 70]',
     solution='''a = [10, 20, 30, 40, 50, 60, 70]
del a[2:5]
print(a)''')
task('Leere die Liste `a` mit `clear()`. Gib danach die Liste und ihre Länge aus.',
     given='a = [1, 2, 3]',
     solution='''a = [1, 2, 3]
a.clear()
print(a)
print(len(a))''')
task('''Wenn `produkt` in `einkauf` vorkommt, soll es entfernt werden. Sonst soll ausgegeben werden, dass das Produkt nicht
auf der Liste steht. Gib am Ende die Liste aus. Teste dein Programm auch mit `produkt = 'Brot'`.''',
     given="""einkauf = ['Milch', 'Brot', 'Eier', 'Butter']
produkt = 'Käse'""",
     solution="""einkauf = ['Milch', 'Brot', 'Eier', 'Butter']
produkt = 'Käse'
if produkt in einkauf:
    einkauf.remove(produkt)
else:
    print(f'{produkt} steht nicht auf der Liste.')
print(einkauf)""")
task('''Entferne mit `pop()` das erste und das letzte Element von `zahlen`. Addiere die beiden entfernten Zahlen.
Gib die Summe und danach die Liste aus.''',
     given='zahlen = [8, 3, 6, 1, 12]',
     solution='''zahlen = [8, 3, 6, 1, 12]
erstes = zahlen.pop(0)
letztes = zahlen.pop()
print(erstes + letztes)
print(zahlen)''')
predict('''a = [5, 6, 7, 8, 9]
x = a.pop()
y = a.pop(0)
a.remove(7)
print(x, y)
print(a)''')
predict('''a = ['a', 'b', 'c']
a.remove('d')
print(a)''', error=ValueError)

# ---------------------------------------------------------------- 6
sec('Schleifen über Listen')
expl('''#### `for`-Schleife über die Elemente

Mit `for element in liste:` wird der Schleifenrumpf für **jedes Element** der Liste einmal ausgeführt.
Die Variable `element` enthält nacheinander die einzelnen Elemente.''',
     '''tiere = ['Hund', 'Katze', 'Maus']
for tier in tiere:
    print(tier)''')
expl('''#### `for`-Schleife über die Indizes

Mit `for i in range(len(liste)):` durchläuft man alle Indizes 0, 1, ..., `len(liste) - 1`.
Das braucht man, wenn man die Position kennen oder die Elemente in der Liste **ändern** möchte.''',
     '''tiere = ['Hund', 'Katze', 'Maus']
for i in range(len(tiere)):
    print(i, tiere[i])''')
expl('''#### `while`-Schleife

Mit einer `while`-Schleife und einer Zählvariablen kann man eine Liste ebenfalls durchlaufen.
Die Zählvariable darf man dabei nicht vergessen zu erhöhen.''',
     '''tiere = ['Hund', 'Katze', 'Maus']
i = 0
while i < len(tiere):
    print(tiere[i])
    i += 1''')

TIERE = "tiere = ['Hund', 'Katze', 'Maus', 'Pferd', 'Esel']"
Z5 = 'zahlen = [4, 7, 1, 9, 3]'
task('Gib jedes Tier aus `tiere` in einer eigenen Zeile aus. Verwende eine `for`-Schleife.',
     given=TIERE, solution=TIERE + '''
for tier in tiere:
    print(tier)''')
task('Gib jede Zahl aus `zahlen` verdoppelt aus.',
     given=Z5, solution=Z5 + '''
for z in zahlen:
    print(2 * z)''')
task('Gib die Namen nummeriert aus wie unten. Verwende `range()` und `len()`.',
     given="namen = ['Ali', 'Bea', 'Cem', 'Dana']",
     solution='''namen = ['Ali', 'Bea', 'Cem', 'Dana']
for i in range(len(namen)):
    print(f'{i + 1}. {namen[i]}')''')
task('Berechne mit einer `for`-Schleife die Summe aller Zahlen in `zahlen`. Gib die Summe aus.',
     given=Z5, solution=Z5 + '''
summe = 0
for z in zahlen:
    summe += z
print(summe)''')
task('Gib nur die geraden Zahlen aus `zahlen` aus.',
     given='zahlen = [3, 8, 12, 5, 6, 7, 10]',
     solution='''zahlen = [3, 8, 12, 5, 6, 7, 10]
for z in zahlen:
    if z % 2 == 0:
        print(z)''')
task('Zähle, wie viele Zahlen in `zahlen` größer als 5 sind. Gib die Anzahl aus.',
     given='zahlen = [3, 8, 12, 5, 6, 7, 10]',
     solution='''zahlen = [3, 8, 12, 5, 6, 7, 10]
anzahl = 0
for z in zahlen:
    if z > 5:
        anzahl += 1
print(anzahl)''')
task('Gib jedes Wort aus `woerter` zusammen mit seiner Länge aus wie unten.',
     given="woerter = ['Haus', 'Baum', 'Elefant', 'Ei', 'Computer']",
     solution='''woerter = ['Haus', 'Baum', 'Elefant', 'Ei', 'Computer']
for w in woerter:
    print(w, len(w))''')
task('Gib alle Tiere aus `tiere` mit einer `while`-Schleife aus.',
     given=TIERE, solution=TIERE + '''
i = 0
while i < len(tiere):
    print(tiere[i])
    i += 1''')
task('Erhöhe jedes Element in `a` um 1. Die Liste selbst soll geändert werden. Gib danach die Liste aus.',
     given='a = [2, 4, 6, 8]',
     solution='''a = [2, 4, 6, 8]
for i in range(len(a)):
    a[i] = a[i] + 1
print(a)''')
task('Erstelle eine neue Liste `positive` mit allen Zahlen aus `zahlen`, die größer als 0 sind. Verwende eine Schleife und `append()`. Gib die neue Liste aus.',
     given='zahlen = [5, -3, 8, -1, 0, 7]',
     solution='''zahlen = [5, -3, 8, -1, 0, 7]
positive = []
for z in zahlen:
    if z > 0:
        positive.append(z)
print(positive)''')
task('Gib die Elemente von `tiere` in umgekehrter Reihenfolge aus, jedes in einer eigenen Zeile. Verwende eine `while`-Schleife, die beim letzten Index beginnt.',
     given=TIERE, solution=TIERE + '''
i = len(tiere) - 1
while i >= 0:
    print(tiere[i])
    i -= 1''')
task('Finde mit einer Schleife die kleinste Zahl in `zahlen` und gib sie aus. Benutze dafür keine fertige Funktion.',
     given='zahlen = [17, 4, 22, 9, 3, 15]',
     solution='''zahlen = [17, 4, 22, 9, 3, 15]
kleinste = zahlen[0]
for z in zahlen:
    if z < kleinste:
        kleinste = z
print(kleinste)''')
task('Gib nur die Elemente von `buchstaben` aus, die an einer geraden Indexposition (0, 2, 4, ...) stehen.',
     given="buchstaben = ['P', 'x', 'y', 'y', 't', 'z', 'h', 'q', 'o', 'w', 'n']",
     solution='''buchstaben = ['P', 'x', 'y', 'y', 't', 'z', 'h', 'q', 'o', 'w', 'n']
for i in range(len(buchstaben)):
    if i % 2 == 0:
        print(buchstaben[i])''')
task('Erstelle mit einer Schleife und `append()` eine Liste mit den Quadratzahlen 1, 4, 9, ..., 100. Gib die Liste aus.',
     solution='''quadrate = []
for i in range(1, 11):
    quadrate.append(i * i)
print(quadrate)''')
predict('''a = [1, 2, 3, 4]
for i in range(len(a)):
    a[i] = a[i] * i
print(a)''')
predict('''zahlen = [3, 1, 4, 1, 5]
ergebnis = []
for z in zahlen:
    if z > 2:
        ergebnis.append(z * 10)
print(ergebnis)''')

# ---------------------------------------------------------------- 7
sec('List Comprehension')
expl('''#### List Comprehension

Mit einer **List Comprehension** erzeugt man eine neue Liste in einer einzigen Zeile:

`neue_liste = [ausdruck for element in liste]`

Für jedes Element wird der Ausdruck berechnet und in die neue Liste geschrieben.
Statt einer Liste kann man auch `range()` verwenden.''',
     '''zahlen = [1, 2, 3, 4]
doppelt = [2 * z for z in zahlen]
print(doppelt)
print([i for i in range(5)])''')
expl('''#### List Comprehension mit Bedingung

Mit `if` am Ende kommen nur die Elemente in die neue Liste, für die die Bedingung wahr ist:

`neue_liste = [ausdruck for element in liste if bedingung]`''',
     '''zahlen = [5, 12, 8, 3, 19]
gross = [z for z in zahlen if z > 7]
print(gross)''')
expl('''#### `if`-`else` im Ausdruck

Der Ausdruck vorne darf selbst eine Auswahl enthalten: `wert1 if bedingung else wert2`.
Dann kommt **jedes** Element in die neue Liste, aber je nach Bedingung mit einem anderen Wert.''',
     '''zahlen = [5, 12, 8, 3, 19]
markiert = ['groß' if z > 7 else 'klein' for z in zahlen]
print(markiert)''')
expl('''#### `upper()` und `lower()`

`text.upper()` gibt eine Zeichenkette in **Großbuchstaben** zurück, `text.lower()` in **Kleinbuchstaben**.
Die ursprüngliche Zeichenkette bleibt dabei unverändert.''',
     '''name = 'Anna'
print(name.upper())
print(name.lower())
print([w.upper() for w in ['ja', 'nein']])''')

task('Erstelle mit einer List Comprehension eine Liste mit den Quadratzahlen von 1 bis 100. Gib sie aus.',
     solution='''quadrate = [i * i for i in range(1, 11)]
print(quadrate)''')
task('Erstelle mit einer List Comprehension eine neue Liste, in der jede Zahl aus `zahlen` verdreifacht ist. Gib sie aus.',
     given=Z5, solution=Z5 + '''
dreifach = [3 * z for z in zahlen]
print(dreifach)''')
task('Erstelle mit einer List Comprehension eine Liste mit allen ungeraden Zahlen aus `zahlen`. Gib sie aus.',
     given='zahlen = [3, 8, 12, 5, 6, 7, 10]',
     solution='''zahlen = [3, 8, 12, 5, 6, 7, 10]
ungerade = [z for z in zahlen if z % 2 == 1]
print(ungerade)''')
task('Erstelle mit einer List Comprehension eine Liste mit den Längen der Wörter in `woerter`. Gib sie aus.',
     given="woerter = ['Haus', 'Baum', 'Elefant', 'Ei', 'Computer']",
     solution='''woerter = ['Haus', 'Baum', 'Elefant', 'Ei', 'Computer']
laengen = [len(w) for w in woerter]
print(laengen)''')
task('Erstelle mit einer List Comprehension eine Liste mit allen Wörtern aus `woerter`, die mehr als 4 Buchstaben haben. Gib sie aus.',
     given="woerter = ['Haus', 'Baum', 'Elefant', 'Ei', 'Computer']",
     solution='''woerter = ['Haus', 'Baum', 'Elefant', 'Ei', 'Computer']
lang = [w for w in woerter if len(w) > 4]
print(lang)''')
task('Erstelle mit einer List Comprehension eine Liste, in der alle Namen in Großbuchstaben stehen. Gib sie aus.',
     given="namen = ['anna', 'ben', 'carla']",
     solution='''namen = ['anna', 'ben', 'carla']
gross = [n.upper() for n in namen]
print(gross)''')
task('Rechne die Temperaturen mit einer List Comprehension von Grad Celsius in Grad Fahrenheit um. Es gilt: `f = c * 9 / 5 + 32`. Gib die neue Liste aus.',
     given='celsius = [0, 10, 20, 30, 37]',
     solution='''celsius = [0, 10, 20, 30, 37]
fahrenheit = [c * 9 / 5 + 32 for c in celsius]
print(fahrenheit)''')
task('Erstelle mit einer List Comprehension und `range()` eine Liste mit allen Vielfachen von 7 zwischen 1 und 50. Verwende dabei `if`. Gib die Liste aus.',
     solution='''vielfache = [z for z in range(1, 51) if z % 7 == 0]
print(vielfache)''')
task('Erstelle mit einer List Comprehension eine neue Liste, in der alle negativen Zahlen aus `zahlen` durch 0 ersetzt sind. Gib sie aus.',
     given='zahlen = [4, -2, 7, -5, 0, 3]',
     solution='''zahlen = [4, -2, 7, -5, 0, 3]
ohne_negative = [z if z >= 0 else 0 for z in zahlen]
print(ohne_negative)''')
task('''Schreibe den folgenden Code als List Comprehension in einer Zeile. Gib das Ergebnis aus.
```python
ergebnis = []
for x in range(1, 6):
    ergebnis.append(x * 2)
```''',
     solution='''ergebnis = [x * 2 for x in range(1, 6)]
print(ergebnis)''')
task('''Schreibe die folgende Zeile als `for`-Schleife mit `append()`. Gib das Ergebnis aus.
```python
b = [x + 1 for x in a if x % 3 == 0]
```''',
     given='a = [3, 4, 6, 7, 9, 10, 12]',
     solution='''a = [3, 4, 6, 7, 9, 10, 12]
b = []
for x in a:
    if x % 3 == 0:
        b.append(x + 1)
print(b)''')
task("Erstelle mit einer List Comprehension eine Liste, die für jede Note aus `noten` `'bestanden'` enthält, wenn die Note höchstens 4 ist, und sonst `'nicht bestanden'`. Gib die Liste aus.",
     given='noten = [2, 5, 3, 6, 4, 1]',
     solution='''noten = [2, 5, 3, 6, 4, 1]
ergebnis = ['bestanden' if n <= 4 else 'nicht bestanden' for n in noten]
print(ergebnis)''')
task('Erstelle mit einer List Comprehension eine Liste mit allen Namen aus `namen`, die mehr als 3 Buchstaben haben, in Kleinbuchstaben. Gib sie aus.',
     given="namen = ['TIM', 'Lena', 'JONAS', 'Eva', 'Paul']",
     solution='''namen = ['TIM', 'Lena', 'JONAS', 'Eva', 'Paul']
ergebnis = [n.lower() for n in namen if len(n) > 3]
print(ergebnis)''')
predict('''a = [x * x for x in range(5) if x % 2 == 1]
b = ['ja' if x > 2 else 'nein' for x in [1, 3, 2, 5]]
print(a)
print(b)''')

# ---------------------------------------------------------------- 8
sec('Listen sortieren')
expl('''#### `sort()`

`liste.sort()` sortiert die Liste **aufsteigend**. Zahlen werden der Größe nach sortiert,
Zeichenketten alphabetisch. Die Liste selbst wird dabei verändert.

Achtung: `sort()` gibt **nichts** zurück (genauer: `None`). Schreibe also nicht `a = a.sort()`.

Mit `liste.sort(reverse=True)` wird **absteigend** sortiert.''',
     '''zahlen = [5, 2, 9, 1]
zahlen.sort()
print(zahlen)
zahlen.sort(reverse=True)
print(zahlen)
namen = ['Tom', 'Anna', 'Max']
namen.sort()
print(namen)''')
expl('''#### Sortieren mit `key`

Mit `liste.sort(key=funktion)` wird nach dem Ergebnis der Funktion sortiert, nicht nach den Elementen selbst.

- `key=len` sortiert nach der Länge.
- Großbuchstaben kommen beim Sortieren **vor** Kleinbuchstaben. Mit `key=str.lower` wird so sortiert,
  als wären alle Buchstaben klein.
- Man kann auch eine **eigene Funktion** angeben. Hinter `key=` steht dabei nur der Name der Funktion, ohne Klammern.''',
     '''woerter = ['banane', 'Apfel', 'Kiwi', 'birne']
woerter.sort()
print(woerter)
woerter.sort(key=str.lower)
print(woerter)
woerter.sort(key=len)
print(woerter)

def letzte_ziffer(n):
    return n % 10

zahlen = [23, 41, 18, 5]
zahlen.sort(key=letzte_ziffer)
print(zahlen)''')
expl('''#### `abs()`

`abs(zahl)` gibt den **Betrag** einer Zahl zurück, also die Zahl ohne Vorzeichen.''',
     '''print(abs(-7))
print(abs(7))
print(abs(3 - 10))''')
expl('''#### `reverse()`

`liste.reverse()` kehrt die **Reihenfolge** der Elemente um. Dabei wird nicht sortiert.''',
     '''a = [3, 1, 2]
a.reverse()
print(a)''')

ZS = 'zahlen = [42, 7, 19, 3, 25, 11, 8]'
task('Sortiere `zahlen` aufsteigend. Gib die Liste aus.',
     given=ZS, solution=ZS + '''
zahlen.sort()
print(zahlen)''')
task('Sortiere `zahlen` absteigend. Gib die Liste aus.',
     given=ZS, solution=ZS + '''
zahlen.sort(reverse=True)
print(zahlen)''')
task('Sortiere `namen` alphabetisch. Gib die Liste aus.',
     given="namen = ['Lukas', 'Emma', 'Noah', 'Mia', 'Ben']",
     solution='''namen = ['Lukas', 'Emma', 'Noah', 'Mia', 'Ben']
namen.sort()
print(namen)''')
task('Sortiere `namen` in umgekehrter alphabetischer Reihenfolge (von Z nach A). Gib die Liste aus.',
     given="namen = ['Lukas', 'Emma', 'Noah', 'Mia', 'Ben']",
     solution='''namen = ['Lukas', 'Emma', 'Noah', 'Mia', 'Ben']
namen.sort(reverse=True)
print(namen)''')
task('Sortiere `obst` alphabetisch, ohne dass Groß- und Kleinschreibung eine Rolle spielt. Gib die Liste aus.',
     given="obst = ['banane', 'Apfel', 'kirsche', 'Birne']",
     solution='''obst = ['banane', 'Apfel', 'kirsche', 'Birne']
obst.sort(key=str.lower)
print(obst)''')
task('Sortiere `woerter` nach der Länge der Wörter, das kürzeste zuerst. Gib die Liste aus.',
     given="woerter = ['Haus', 'Elefant', 'Ei', 'Computer', 'Maus']",
     solution='''woerter = ['Haus', 'Elefant', 'Ei', 'Computer', 'Maus']
woerter.sort(key=len)
print(woerter)''')
task('Kehre die Reihenfolge von `tage` mit `reverse()` um. Gib die Liste aus.',
     given="tage = ['Mo', 'Di', 'Mi', 'Do', 'Fr']",
     solution='''tage = ['Mo', 'Di', 'Mi', 'Do', 'Fr']
tage.reverse()
print(tage)''')
task('Gib die drei größten Zahlen aus `zahlen` als Liste aus, die größte zuerst. Verwende `sort()` und Slicing.',
     given=ZS, solution=ZS + '''
zahlen.sort(reverse=True)
print(zahlen[:3])''')
task('''Sortiere `zahlen` danach, wie weit die Zahlen von 10 entfernt sind. Die Zahl, die am nächsten an 10 liegt, soll zuerst kommen.
Schreibe dazu eine Funktion `abstand(n)`, die mit `abs()` den Abstand zu 10 zurückgibt, und verwende sie als `key`.''',
     given='zahlen = [3, 14, 9, 25, 10, 1]',
     solution='''zahlen = [3, 14, 9, 25, 10, 1]

def abstand(n):
    return abs(n - 10)

zahlen.sort(key=abstand)
print(zahlen)''')
task('Sortiere `woerter` absteigend nach ihrer Länge, das längste Wort zuerst. Gib die Liste aus.',
     given="woerter = ['Haus', 'Elefant', 'Ei', 'Computer', 'Maus']",
     solution='''woerter = ['Haus', 'Elefant', 'Ei', 'Computer', 'Maus']
woerter.sort(key=len, reverse=True)
print(woerter)''')
predict('''a = [3, 1, 2]
b = a.sort()
print(a)
print(b)''')
predict('''a = ['b', 'C', 'a', 'D']
a.sort()
print(a)
a.reverse()
print(a)''')

# ---------------------------------------------------------------- 9
sec('Listen kopieren')
expl('''#### `b = a` ist keine Kopie

Nach `b = a` gibt es **nur eine** Liste, die zwei Namen hat. Ändert man die Liste über `b`,
ist die Änderung auch über `a` zu sehen.''',
     '''a = [1, 2, 3]
b = a
b.append(4)
print(a)''')
expl('''#### `copy()`, `list()` und `[:]`

Eine echte Kopie erhält man auf drei Arten:

- `b = a.copy()`
- `b = list(a)`
- `b = a[:]` (Slicing ohne Start und Stopp)

Danach sind `a` und `b` zwei verschiedene Listen.''',
     '''a = [1, 2, 3]
b = a.copy()
c = list(a)
d = a[:]
b.append(4)
c.append(5)
d.append(6)
print(a, b, c, d)''')

task('Erstelle mit `copy()` eine Kopie von `original` und sortiere die Kopie. `original` soll unverändert bleiben. Gib beide Listen aus.',
     given='original = [5, 3, 8, 1]',
     solution='''original = [5, 3, 8, 1]
sortiert = original.copy()
sortiert.sort()
print(original)
print(sortiert)''')
task('Erstelle mit `[:]` eine Kopie `noten_ohne` von `noten` und entferne aus der Kopie die Note 5. Gib beide Listen aus.',
     given='noten = [2, 5, 1, 3]',
     solution='''noten = [2, 5, 1, 3]
noten_ohne = noten[:]
noten_ohne.remove(5)
print(noten)
print(noten_ohne)''')
task('Erstelle mit `list()` eine Kopie `rueckwaerts` von `tage` und kehre die Kopie um. Gib beide Listen aus.',
     given="tage = ['Mo', 'Di', 'Mi']",
     solution='''tage = ['Mo', 'Di', 'Mi']
rueckwaerts = list(tage)
rueckwaerts.reverse()
print(tage)
print(rueckwaerts)''')
task('Erstelle eine Kopie `neu` von `preise`, in der jeder Preis um 1 erhöht ist. `preise` soll unverändert bleiben. Gib beide Listen aus.',
     given='preise = [3, 5, 2]',
     solution='''preise = [3, 5, 2]
neu = preise.copy()
for i in range(len(neu)):
    neu[i] = neu[i] + 1
print(preise)
print(neu)''')
predict('''a = [1, 2, 3]
b = a
b.append(4)
print(a)
print(b)''')
predict('''a = [1, 2, 3]
b = a.copy()
b.append(4)
print(a)
print(b)''')
predict('''a = [1, 2, 3]
b = list(a)
c = a
a[0] = 99
print(a, b, c)''')

# ---------------------------------------------------------------- 10
sec('Listen verbinden')
expl('''#### Der Operator `+`

`a + b` erzeugt eine **neue Liste** mit allen Elementen von `a` und danach allen Elementen von `b`.
`a` und `b` bleiben unverändert.''',
     '''a = [1, 2]
b = [3, 4]
c = a + b
print(c)
print(a)''')
expl('''#### Verbinden mit `extend()` oder mit einer Schleife

`a.extend(b)` hängt die Elemente von `b` direkt an `a` an (siehe oben).
Dasselbe erreicht man mit einer Schleife und `append()`.''',
     '''a = [1, 2]
b = [3, 4]
for x in b:
    a.append(x)
print(a)''')

task('Verbinde `a` und `b` mit `+` zu einer neuen Liste `c`. Gib `c` aus.',
     given='''a = [1, 2, 3]
b = [4, 5, 6]''',
     solution='''a = [1, 2, 3]
b = [4, 5, 6]
c = a + b
print(c)''')
task('Verbinde die beiden Listen zu einer Liste `alle` und sortiere sie alphabetisch. Gib `alle` aus.',
     given="""klasse_a = ['Tim', 'Ida', 'Ole']
klasse_b = ['Zoe', 'Ben', 'Mia']""",
     solution="""klasse_a = ['Tim', 'Ida', 'Ole']
klasse_b = ['Zoe', 'Ben', 'Mia']
alle = klasse_a + klasse_b
alle.sort()
print(alle)""")
task('Hänge die Elemente von `b` mit einer `for`-Schleife und `append()` an `a` an. Gib `a` aus.',
     given='''a = [1, 2, 3]
b = [4, 5, 6]''',
     solution='''a = [1, 2, 3]
b = [4, 5, 6]
for x in b:
    a.append(x)
print(a)''')
task('Verbinde die drei Listen in der Reihenfolge `c`, `a`, `b` zu einer neuen Liste. Gib sie aus.',
     given="""a = ['x']
b = ['y', 'z']
c = ['w']""",
     solution="""a = ['x']
b = ['y', 'z']
c = ['w']
print(c + a + b)""")
task('Erstelle mit `+` eine neue Liste, die mit 0 beginnt, dann alle Elemente von `zahlen` enthält und mit 100 endet. Gib sie aus.',
     given='zahlen = [10, 20, 30]',
     solution='''zahlen = [10, 20, 30]
neu = [0] + zahlen + [100]
print(neu)''')
predict('''a = [1, 2]
b = [3]
c = a + b
a.append(9)
print(c)
print(a + a)''')

# ---------------------------------------------------------------- 11
sec('Weitere Methoden und Funktionen')
expl('''#### `count()`

`liste.count(wert)` gibt zurück, **wie oft** ein Wert in der Liste vorkommt.''',
     '''wuerfe = [6, 2, 6, 3]
print(wuerfe.count(6))
print(wuerfe.count(5))''')
expl('''#### `index()`

`liste.index(wert)` gibt den Index des **ersten Vorkommens** eines Wertes zurück.
Kommt der Wert nicht vor, gibt es einen `ValueError`.''',
     '''tiere = ['Hund', 'Katze', 'Maus', 'Katze']
print(tiere.index('Katze'))''')
expl('''#### `sum()`, `min()` und `max()`

- `sum(liste)` gibt die **Summe** aller Zahlen einer Liste zurück.
- `min(liste)` gibt das **kleinste** Element zurück.
- `max(liste)` gibt das **größte** Element zurück.''',
     '''zahlen = [4, 9, 1, 7]
print(sum(zahlen))
print(min(zahlen))
print(max(zahlen))''')

WUERFE = 'wuerfe = [6, 2, 6, 3, 1, 6, 4, 2, 5, 2]'
task('Gib mit `count()` aus, wie oft in `wuerfe` eine 6 gewürfelt wurde.',
     given=WUERFE, solution=WUERFE + '''
print(wuerfe.count(6))''')
task("Gib mit `index()` aus, an welcher Stelle `'Cem'` in `namen` steht.",
     given="namen = ['Ali', 'Bea', 'Cem', 'Dana']",
     solution='''namen = ['Ali', 'Bea', 'Cem', 'Dana']
print(namen.index('Cem'))''')
task('Gib die Summe, das Minimum und das Maximum von `zahlen` aus, jeweils in einer eigenen Zeile.',
     given=ZS, solution=ZS + '''
print(sum(zahlen))
print(min(zahlen))
print(max(zahlen))''')
task('Berechne mit `sum()` und `len()` den Durchschnitt der Zahlen in `punkte`. Gib ihn aus.',
     given='punkte = [12, 15, 9, 14, 10]',
     solution='''punkte = [12, 15, 9, 14, 10]
print(sum(punkte) / len(punkte))''')
task('Gib für jede Augenzahl von 1 bis 6 aus, wie oft sie in `wuerfe` vorkommt. Verwende eine Schleife und `count()`.',
     given=WUERFE, solution=WUERFE + '''
for augen in range(1, 7):
    print(augen, wuerfe.count(augen))''')
task('Die schlechteste (kleinste) Punktzahl in `punkte` wird gestrichen. Entferne sie mit `min()` und `remove()`. Berechne dann den Durchschnitt der übrigen Punkte und gib ihn aus.',
     given='punkte = [12, 15, 6, 14, 13]',
     solution='''punkte = [12, 15, 6, 14, 13]
punkte.remove(min(punkte))
print(sum(punkte) / len(punkte))''')
task('Gib die Differenz zwischen der höchsten und der niedrigsten Temperatur in `temperaturen` aus.',
     given='temperaturen = [14, 19, 11, 22, 17, 9, 15]',
     solution='''temperaturen = [14, 19, 11, 22, 17, 9, 15]
print(max(temperaturen) - min(temperaturen))''')
task("Ersetze mit `index()` das Element `'Maus'` in `tiere` durch `'Hamster'`. Gib die Liste aus.",
     given="tiere = ['Hund', 'Katze', 'Maus', 'Pferd']",
     solution='''tiere = ['Hund', 'Katze', 'Maus', 'Pferd']
i = tiere.index('Maus')
tiere[i] = 'Hamster'
print(tiere)''')
task('Gib das alphabetisch erste und das alphabetisch letzte Wort aus `woerter` aus. Verwende `min()` und `max()`.',
     given="woerter = ['Maus', 'Ast', 'Zebra', 'Kino', 'Brot']",
     solution='''woerter = ['Maus', 'Ast', 'Zebra', 'Kino', 'Brot']
print(min(woerter))
print(max(woerter))''')
predict('''a = [4, 2, 4, 1, 4]
print(a.count(4))
print(a.index(4))
print(a.count(7))
print(max(a) - min(a))''')

# ---------------------------------------------------------------- 12
sec('Gemischte Übungen')
task('Erstelle eine neue Liste mit allen Zahlen aus `zahlen`, die größer als der Durchschnitt sind. Gib sie aus.',
     given='zahlen = [4, 10, 7, 1, 13, 5]',
     solution='''zahlen = [4, 10, 7, 1, 13, 5]
durchschnitt = sum(zahlen) / len(zahlen)
groesser = [z for z in zahlen if z > durchschnitt]
print(groesser)''')
task('Erstelle eine neue Liste `ohne_doppelte`, in der jedes Element von `a` nur einmal vorkommt. Die Reihenfolge soll erhalten bleiben. Verwende `not in`. Gib die neue Liste aus.',
     given='a = [3, 1, 3, 2, 1, 5, 2, 3]',
     solution='''a = [3, 1, 3, 2, 1, 5, 2, 3]
ohne_doppelte = []
for x in a:
    if x not in ohne_doppelte:
        ohne_doppelte.append(x)
print(ohne_doppelte)''')
task('Erstelle eine neue Liste mit den Elementen von `a` in umgekehrter Reihenfolge. Verwende dafür nicht `reverse()`, sondern eine Schleife und `insert()`.',
     given='a = [1, 2, 3, 4, 5]',
     solution='''a = [1, 2, 3, 4, 5]
umgekehrt = []
for x in a:
    umgekehrt.insert(0, x)
print(umgekehrt)''')
task('Erstelle eine Liste mit allen Elementen, die sowohl in `a` als auch in `b` vorkommen. Gib sie aus.',
     given='''a = [1, 4, 7, 9, 12]
b = [3, 4, 9, 10, 12, 15]''',
     solution='''a = [1, 4, 7, 9, 12]
b = [3, 4, 9, 10, 12, 15]
gemeinsam = [x for x in a if x in b]
print(gemeinsam)''')
task('''In `produkte` und `preise` gehören die Elemente mit demselben Index zusammen.
Gib jedes Produkt mit seinem Preis aus wie unten und danach die Gesamtsumme.''',
     given="""produkte = ['Milch', 'Brot', 'Käse']
preise = [2, 3, 5]""",
     solution="""produkte = ['Milch', 'Brot', 'Käse']
preise = [2, 3, 5]
for i in range(len(produkte)):
    print(f'{produkte[i]}: {preise[i]} Euro')
print(f'Gesamt: {sum(preise)} Euro')""")
task('Erstelle eine Liste mit den ersten 10 Fibonacci-Zahlen. Beginne mit `[1, 1]`. Jede weitere Zahl ist die Summe der beiden letzten Zahlen der Liste. Gib die Liste aus.',
     solution='''fib = [1, 1]
while len(fib) < 10:
    fib.append(fib[-1] + fib[-2])
print(fib)''')
task('Teile die Zahlen aus `zahlen` auf zwei Listen `gerade` und `ungerade` auf. Gib beide Listen aus.',
     given='zahlen = [7, 2, 9, 4, 4, 11, 6, 1]',
     solution='''zahlen = [7, 2, 9, 4, 4, 11, 6, 1]
gerade = []
ungerade = []
for z in zahlen:
    if z % 2 == 0:
        gerade.append(z)
    else:
        ungerade.append(z)
print(gerade)
print(ungerade)''')
task('Gib alle Tage aus, an denen es wärmer als 20 Grad war. In `tage` und `temperaturen` gehören die Elemente mit demselben Index zusammen.',
     given="""tage = ['Mo', 'Di', 'Mi', 'Do', 'Fr', 'Sa', 'So']
temperaturen = [18, 22, 25, 19, 21, 17, 23]""",
     solution="""tage = ['Mo', 'Di', 'Mi', 'Do', 'Fr', 'Sa', 'So']
temperaturen = [18, 22, 25, 19, 21, 17, 23]
for i in range(len(tage)):
    if temperaturen[i] > 20:
        print(tage[i])""")
task('''Prüfe mit einer Schleife, ob die Liste `a` aufsteigend sortiert ist. Gib `sortiert` oder `nicht sortiert` aus.
Teste dein Programm auch mit `a = [1, 3, 5, 8, 9]`.''',
     given='a = [1, 3, 5, 4, 9]',
     solution='''a = [1, 3, 5, 4, 9]
ist_sortiert = True
for i in range(len(a) - 1):
    if a[i] > a[i + 1]:
        ist_sortiert = False
if ist_sortiert:
    print('sortiert')
else:
    print('nicht sortiert')''')
task('Verschiebe alle Elemente von `a` um eine Position nach rechts. Das letzte Element soll dabei an den Anfang kommen. Verwende `pop()` und `insert()`. Gib die Liste aus.',
     given='a = [1, 2, 3, 4, 5]',
     solution='''a = [1, 2, 3, 4, 5]
letztes = a.pop()
a.insert(0, letztes)
print(a)''')
task('Finde mit einer Schleife das längste Wort in `woerter` und gib es aus.',
     given="woerter = ['Sonne', 'Mond', 'Sternschnuppe', 'Komet', 'Planet']",
     solution='''woerter = ['Sonne', 'Mond', 'Sternschnuppe', 'Komet', 'Planet']
laengstes = woerter[0]
for w in woerter:
    if len(w) > len(laengstes):
        laengstes = w
print(laengstes)''')
task('Erstelle eine neue Liste, in der jedes Element die Summe aus dem Element von `a` und dem Element von `b` mit demselben Index ist. Gib sie aus.',
     given='''a = [1, 2, 3, 4]
b = [10, 20, 30, 40]''',
     solution='''a = [1, 2, 3, 4]
b = [10, 20, 30, 40]
summen = [a[i] + b[i] for i in range(len(a))]
print(summen)''')
task('''Erstelle eine Liste `laufende_summe`. Ihr Element an Index `i` soll die Summe der Elemente von `zahlen` bis einschließlich Index `i` sein.
Gib die Liste aus.''',
     given='zahlen = [3, 1, 4, 1, 5]',
     solution='''zahlen = [3, 1, 4, 1, 5]
laufende_summe = []
summe = 0
for z in zahlen:
    summe += z
    laufende_summe.append(summe)
print(laufende_summe)''')
task("Entferne aus `einkauf` alle Produkte, die auch in `schon_da` stehen. Gib danach `einkauf` aus.",
     given="""einkauf = ['Milch', 'Brot', 'Eier', 'Butter', 'Käse']
schon_da = ['Eier', 'Käse']""",
     solution="""einkauf = ['Milch', 'Brot', 'Eier', 'Butter', 'Käse']
schon_da = ['Eier', 'Käse']
for p in schon_da:
    if p in einkauf:
        einkauf.remove(p)
print(einkauf)""")
task('Erstelle eine Liste `abstaende` mit den Differenzen zwischen zwei benachbarten Elementen von `a`, also `a[1] - a[0]`, `a[2] - a[1]` usw. Gib sie aus.',
     given='a = [2, 5, 9, 10, 16]',
     solution='''a = [2, 5, 9, 10, 16]
abstaende = []
for i in range(len(a) - 1):
    abstaende.append(a[i + 1] - a[i])
print(abstaende)''')
task('Zähle, wie viele Wörter in `woerter` mit einem großen `A` beginnen. Verwende eine Schleife und den Index `[0]` bei Zeichenketten. Gib die Anzahl aus.',
     given="woerter = ['Apfel', 'Birne', 'Ananas', 'apfelsine', 'Aprikose']",
     solution="""woerter = ['Apfel', 'Birne', 'Ananas', 'apfelsine', 'Aprikose']
anzahl = 0
for w in woerter:
    if w[0] == 'A':
        anzahl += 1
print(anzahl)""")

generate('listen', 'Listen', '''Jeder Abschnitt beginnt mit kurzen Erklärungen und Beispielen. Führe die Beispiele aus und probiere sie ruhig ein wenig aus.
Danach folgen viele kleine Übungen. Wenn eine Liste vorgegeben ist, steht sie schon in der Codezelle.''')
