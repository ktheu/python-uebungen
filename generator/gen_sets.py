# Erzeugt ../content/sets.ipynb (siehe nbgen.py).
#
# Achtung: Die Reihenfolge, in der ein Set aus Zeichenketten ausgegeben wird, ändert sich von Lauf zu Lauf.
# Bei Aufgaben mit erwarteter Ausgabe werden solche Sets deshalb immer mit sorted() ausgegeben.
from nbgen import sec, expl, task, predict, generate

# ---------------------------------------------------------------- 1
sec('Sets erstellen')
expl('''#### Was ist ein Set?

Ein **Set** (deutsch: Menge) speichert mehrere Werte in einer Variablen. Die Elemente stehen in **geschweiften** Klammern.

- Sets sind **ungeordnet**: Die Elemente haben keine feste Reihenfolge und keinen Index.
  Die Reihenfolge bei der Ausgabe kann anders sein als beim Erstellen.
- Sets enthalten **keine Duplikate**: Jeder Wert kommt höchstens einmal vor.
- Man kann Elemente hinzufügen und entfernen, aber ein einzelnes Element nicht ändern.
- `True` und `1` gelten in einem Set als derselbe Wert, ebenso `False` und `0`.''',
     """farben = {'rot', 'grün', 'blau', 'rot'}
print(farben)
print(len(farben))
print(type(farben))""")
expl('''#### `set()` und das leere Set

`set(...)` erzeugt ein Set, z. B. aus einer Liste, einer Zeichenkette oder einem `range()`. Duplikate fallen dabei weg.

Achtung: `{}` ist **kein** leeres Set, sondern ein leeres Dictionary. Ein leeres Set erzeugt man mit `set()`.''',
     """print(set([3, 1, 3, 2, 1]))
print(set(range(5)))
leer = set()
print(len(leer))
print(type({}))""")
expl('''#### `sorted()`

`sorted(menge)` gibt die Elemente eines Sets als **sortierte Liste** zurück.
So erhält man immer dieselbe Ausgabe, egal in welcher Reihenfolge das Set seine Elemente speichert.''',
     """farben = {'rot', 'grün', 'blau'}
print(sorted(farben))
print(sorted(set('Banane')))""")

task('Erstelle ein Set `farben` mit den Elementen `rot`, `grün` und `blau`. Gib die Anzahl der Elemente aus.',
     solution="""farben = {'rot', 'grün', 'blau'}
print(len(farben))""")
task('Erstelle mit `set()` aus der Liste `zahlen` ein Set ohne Duplikate. Gib es mit `sorted()` aus.',
     given='zahlen = [4, 2, 4, 7, 2, 9, 7, 4]',
     solution="""zahlen = [4, 2, 4, 7, 2, 9, 7, 4]
menge = set(zahlen)
print(sorted(menge))""")
task('Gib aus, wie viele **verschiedene** Augenzahlen in `wuerfe` vorkommen.',
     given='wuerfe = [6, 2, 6, 3, 1, 6, 4, 2, 3, 2]',
     solution="""wuerfe = [6, 2, 6, 3, 1, 6, 4, 2, 3, 2]
print(len(set(wuerfe)))""")
task('Erstelle ein leeres Set. Gib seinen Datentyp und seine Länge aus.',
     solution="""leer = set()
print(type(leer))
print(len(leer))""")
task("Gib aus, wie viele verschiedene Buchstaben im Wort `'Mississippi'` vorkommen.",
     solution="""print(len(set('Mississippi')))""")
task("Gib die verschiedenen Buchstaben von `'Banane'` als sortierte Liste aus.",
     solution="""print(sorted(set('Banane')))""")
task('Erstelle mit `set()` und `range()` ein Set mit den Zahlen von 1 bis 5. Gib es aus.',
     solution="""print(set(range(1, 6)))""")
task('Entferne mit einem Set die doppelten Namen aus `namen`. Gib die Namen als sortierte Liste aus.',
     given="namen = ['Tom', 'Lisa', 'Tom', 'Max', 'Lisa', 'Anna']",
     solution="""namen = ['Tom', 'Lisa', 'Tom', 'Max', 'Lisa', 'Anna']
print(sorted(set(namen)))""")
task('Gib aus, wie viele Werte in `liste` doppelt vorkommen. Vergleiche dazu die Länge der Liste mit der Länge des Sets.',
     given='liste = [1, 2, 2, 3, 3, 3, 4]',
     solution="""liste = [1, 2, 2, 3, 3, 3, 4]
print(len(liste) - len(set(liste)))""")
predict("""a = {1, 2, 2, 3, 3, 3}
b = {}
c = set()
print(len(a))
print(type(b))
print(type(c))
print(len({True, 1, 2}))""")
predict("""s = {'Banane', 'Apfel', 'Kirsche'}
print(s)
print(sorted(s))""")
predict("""s = {1, 2, 3}
print(s[0])""", error=TypeError)

# ---------------------------------------------------------------- 2
sec('Auf Elemente zugreifen')
expl('''#### Schleife und `in`

Weil Sets keinen Index haben, gibt es kein `s[0]`. Man kann aber

- mit `for element in s:` über alle Elemente laufen (in einer beliebigen Reihenfolge),
- mit `wert in s` prüfen, ob ein Wert im Set ist.

Die Prüfung mit `in` ist bei Sets **sehr schnell**, auch bei vielen Elementen.''',
     """obst = {'Apfel', 'Birne', 'Kirsche'}
for o in sorted(obst):
    print(o)
print('Birne' in obst)
print('Mango' not in obst)""")

OBST = "obst = {'Apfel', 'Birne', 'Kirsche', 'Banane'}"
task("Prüfe mit `in`, ob `'Mango'` in `obst` ist. Gib einen passenden Satz aus.",
     given=OBST, solution=OBST + """
if 'Mango' in obst:
    print('Mango ist da.')
else:
    print('Mango ist nicht da.')""")
task('Gib die Elemente von `obst` alphabetisch sortiert aus, jedes in einer eigenen Zeile.',
     given=OBST, solution=OBST + """
for o in sorted(obst):
    print(o)""")
ZS = 'zahlen = {12, 5, 18, 3, 25, 9}'
task('Berechne mit einer Schleife die Summe der Zahlen in `zahlen`. Gib sie aus.',
     given=ZS, solution=ZS + """
summe = 0
for z in zahlen:
    summe += z
print(summe)""")
task('Zähle, wie viele Zahlen in `zahlen` größer als 10 sind. Gib die Anzahl aus.',
     given=ZS, solution=ZS + """
anzahl = 0
for z in zahlen:
    if z > 10:
        anzahl += 1
print(anzahl)""")
task('Prüfe für jedes Wort in `woerter`, ob es in `erlaubt` vorkommt. Gib das Wort mit `ok` oder `verboten` aus wie unten.',
     given="""erlaubt = {'ja', 'nein', 'vielleicht'}
woerter = ['ja', 'nö', 'vielleicht', 'jein']""",
     solution="""erlaubt = {'ja', 'nein', 'vielleicht'}
woerter = ['ja', 'nö', 'vielleicht', 'jein']
for w in woerter:
    if w in erlaubt:
        print(w, 'ok')
    else:
        print(w, 'verboten')""")
task('Zähle, wie viele Wörter in `satz` **keine** Füllwörter sind, also nicht in `fuellwoerter` vorkommen. Gib die Anzahl aus.',
     given="""fuellwoerter = {'der', 'die', 'das', 'und', 'ein', 'eine'}
satz = 'der Hund und die Katze spielen mit einem Ball und einer Maus'""",
     solution="""fuellwoerter = {'der', 'die', 'das', 'und', 'ein', 'eine'}
satz = 'der Hund und die Katze spielen mit einem Ball und einer Maus'
anzahl = 0
for w in satz.split():
    if w not in fuellwoerter:
        anzahl += 1
print(anzahl)""")
task('Gib das größte und das kleinste Element von `zahlen` aus. Verwende `max()` und `min()`.',
     given=ZS, solution=ZS + """
print(max(zahlen))
print(min(zahlen))""")
predict("""s = {3, 1, 2}
summe = 0
for x in s:
    summe += x
print(summe)
print(2 in s, 5 not in s)""")

# ---------------------------------------------------------------- 3
sec('Elemente hinzufügen')
expl('''#### `add()`

`s.add(wert)` fügt einen Wert zum Set hinzu. Ist der Wert schon im Set, passiert nichts.''',
     """farben = {'rot', 'blau'}
farben.add('gelb')
farben.add('rot')
print(sorted(farben))""")
expl('''#### `update()`

`s.update(...)` fügt **alle Elemente** einer Liste, eines Tupels, eines anderen Sets oder einer Zeichenkette hinzu.''',
     """s = {1, 2}
s.update([2, 3, 4])
print(s)
s.update({5, 6})
print(s)""")

FARBEN = "farben = {'rot', 'grün', 'blau'}"
task("Füge mit `add()` das Element `'gelb'` zu `farben` hinzu. Gib das Set sortiert aus.",
     given=FARBEN, solution=FARBEN + """
farben.add('gelb')
print(sorted(farben))""")
task("Füge `'rot'` mit `add()` zu `farben` hinzu und gib danach die Länge aus.",
     given=FARBEN, solution=FARBEN + """
farben.add('rot')
print(len(farben))""")
task("Füge mit `update()` alle Farben aus `neue` zu `farben` hinzu. Gib das Set sortiert aus.",
     given=FARBEN + "\nneue = ['lila', 'rot', 'weiß']",
     solution=FARBEN + """
neue = ['lila', 'rot', 'weiß']
farben.update(neue)
print(sorted(farben))""")
task('Erstelle ein leeres Set `quadrate`. Füge mit einer Schleife und `add()` die Quadratzahlen von 1 bis 25 hinzu. Gib das Set sortiert aus.',
     solution="""quadrate = set()
for i in range(1, 6):
    quadrate.add(i * i)
print(sorted(quadrate))""")
task('Sammle mit einer Schleife und `add()` alle Buchstaben von `wort` in einem Set. Gib das Set sortiert aus.',
     given="wort = 'Informatik'",
     solution="""wort = 'Informatik'
buchstaben = set()
for c in wort:
    buchstaben.add(c)
print(sorted(buchstaben))""")
task('In `besuche` steht für jeden Besuch der Name des Besuchers. Sammle die Namen mit `add()` in einem Set und gib aus, wie viele verschiedene Personen da waren.',
     given="besuche = ['Ali', 'Bea', 'Ali', 'Cem', 'Bea', 'Ali', 'Dana']",
     solution="""besuche = ['Ali', 'Bea', 'Ali', 'Cem', 'Bea', 'Ali', 'Dana']
personen = set()
for name in besuche:
    personen.add(name)
print(len(personen))""")
task("Füge mit `update()` die Buchstaben von `'abc'` zu `s` hinzu. Gib `s` sortiert aus.",
     given="s = {'x', 'y'}",
     solution="""s = {'x', 'y'}
s.update('abc')
print(sorted(s))""")
task('Füge mit **einem** `update()` alle geraden Zahlen von 2 bis 10 zu `s` hinzu. Verwende `range()`. Gib `s` sortiert aus.',
     given='s = {1, 3}',
     solution="""s = {1, 3}
s.update(range(2, 11, 2))
print(sorted(s))""")
predict("""s = {1, 2}
s.add(2)
s.add(3)
s.update([3, 4, 5])
print(len(s))
s.update('ab')
print(len(s))""")

# ---------------------------------------------------------------- 4
sec('Elemente entfernen')
expl('''#### `remove()` und `discard()`

- `s.remove(wert)` entfernt einen Wert. Ist er nicht im Set, gibt es einen `KeyError`.
- `s.discard(wert)` entfernt einen Wert ebenfalls, gibt aber **keinen Fehler**, wenn er fehlt.''',
     """s = {1, 2, 3}
s.remove(2)
s.discard(7)
print(s)""")
expl('''#### `pop()`, `clear()` und `del`

- `s.pop()` entfernt ein **beliebiges** Element und gibt es zurück. Welches, kann man nicht vorhersagen.
- `s.clear()` entfernt alle Elemente.
- `del s` löscht die ganze Variable.''',
     """s = {'a', 'b', 'c'}
x = s.pop()
print(x, len(s))
s.clear()
print(s)""")

task("Entferne mit `remove()` das Element `'grün'` aus `farben`. Gib das Set sortiert aus.",
     given=FARBEN, solution=FARBEN + """
farben.remove('grün')
print(sorted(farben))""")
task("Entferne mit `discard()` das Element `'lila'` aus `farben`, obwohl es gar nicht drin ist. Gib das Set sortiert aus.",
     given=FARBEN, solution=FARBEN + """
farben.discard('lila')
print(sorted(farben))""")
task("""Entferne `farbe` mit `remove()` aus `farben`, aber nur, wenn sie drin ist. Sonst gib `nicht vorhanden` aus.
Gib am Ende das Set sortiert aus. Teste auch mit `farbe = 'blau'`.""",
     given=FARBEN + "\nfarbe = 'lila'",
     solution=FARBEN + """
farbe = 'lila'
if farbe in farben:
    farben.remove(farbe)
else:
    print('nicht vorhanden')
print(sorted(farben))""")
task('Entferne mit einer Schleife und `discard()` die Zahlen 2, 4, 6, 8 und 10 aus `zahlen`. Gib `zahlen` aus.',
     given='zahlen = set(range(1, 10))',
     solution="""zahlen = set(range(1, 10))
for z in range(2, 11, 2):
    zahlen.discard(z)
print(zahlen)""")
task('Entferne mit `pop()` in einer `while`-Schleife so lange Elemente aus `s`, bis das Set leer ist. Zähle mit, wie oft `pop()` aufgerufen wurde, und gib die Anzahl aus.',
     given="s = {'a', 'b', 'c', 'd', 'e'}",
     solution="""s = {'a', 'b', 'c', 'd', 'e'}
anzahl = 0
while len(s) > 0:
    s.pop()
    anzahl += 1
print(anzahl)""")
task('Leere `farben` mit `clear()`. Gib danach das Set und seine Länge aus.',
     given=FARBEN, solution=FARBEN + """
farben.clear()
print(farben)
print(len(farben))""")
task('In `vorrat` stehen die Lebensmittel im Kühlschrank. Entferne alle, die in der Liste `gegessen` stehen. Verwende `discard()`. Gib den Vorrat sortiert aus.',
     given="""vorrat = {'Milch', 'Käse', 'Eier', 'Butter', 'Joghurt'}
gegessen = ['Eier', 'Joghurt', 'Wurst']""",
     solution="""vorrat = {'Milch', 'Käse', 'Eier', 'Butter', 'Joghurt'}
gegessen = ['Eier', 'Joghurt', 'Wurst']
for g in gegessen:
    vorrat.discard(g)
print(sorted(vorrat))""")
predict("""s = {1, 2, 3, 4}
s.discard(5)
s.remove(4)
s.discard(1)
print(s)
print(len(s))""")
predict("""s = {1, 2, 3}
s.remove(5)
print(s)""", error=KeyError)

# ---------------------------------------------------------------- 5
sec('Mengenoperationen')
expl('''#### Vereinigung, Schnittmenge, Differenz

Für zwei Sets `a` und `b` gibt es diese Operationen. Jede erzeugt ein **neues** Set:

| Operation | Methode | Operator | Ergebnis |
|---|---|---|---|
| Vereinigung | `a.union(b)` | `a \\| b` | alle Elemente, die in `a` **oder** in `b` sind |
| Schnittmenge | `a.intersection(b)` | `a & b` | alle Elemente, die in `a` **und** in `b` sind |
| Differenz | `a.difference(b)` | `a - b` | alle Elemente von `a`, die **nicht** in `b` sind |
| symmetrische Differenz | `a.symmetric_difference(b)` | `a ^ b` | alle Elemente, die in **genau einem** der beiden Sets sind |

Die Methoden funktionieren auch, wenn `b` eine Liste ist. Die Operatoren funktionieren nur mit zwei Sets.''',
     """a = {1, 2, 3, 4}
b = {3, 4, 5, 6}
print(a | b)
print(a & b)
print(a - b)
print(a ^ b)
print(a.union([7, 8]))""")
expl('''#### Die `_update`-Methoden

`a.update(b)`, `a.intersection_update(b)`, `a.difference_update(b)` und `a.symmetric_difference_update(b)`
erzeugen **kein** neues Set, sondern ändern `a` direkt.''',
     """a = {1, 2, 3, 4}
a.intersection_update({3, 4, 5})
print(a)
b = {1, 2, 3, 4}
b.difference_update({1, 2})
print(b)""")

AG = """info = {'Ali', 'Bea', 'Cem', 'Dana', 'Eli'}
sport = {'Bea', 'Dana', 'Finn', 'Gül'}"""
task('`info` und `sport` sind die Mitglieder zweier AGs. Gib alle Schüler, die in **mindestens einer** AG sind, sortiert aus. Verwende `union()`.',
     given=AG, solution=AG + """
print(sorted(info.union(sport)))""")
task('Gib alle Schüler, die in **beiden** AGs sind, sortiert aus. Verwende `intersection()`.',
     given=AG, solution=AG + """
print(sorted(info.intersection(sport)))""")
task('Gib alle Schüler, die **nur** in der Informatik-AG sind, sortiert aus. Verwende `difference()`.',
     given=AG, solution=AG + """
print(sorted(info.difference(sport)))""")
task('Gib alle Schüler, die in **genau einer** der beiden AGs sind, sortiert aus. Verwende `symmetric_difference()`.',
     given=AG, solution=AG + """
print(sorted(info.symmetric_difference(sport)))""")
task('Berechne die vier Operationen von oben für `a` und `b` noch einmal, diesmal mit den Operatoren `|`, `&`, `-` und `^`. Gib jedes Ergebnis sortiert aus.',
     given="""a = {1, 2, 3, 4, 5, 6}
b = {4, 5, 6, 7, 8, 9}""",
     solution="""a = {1, 2, 3, 4, 5, 6}
b = {4, 5, 6, 7, 8, 9}
print(sorted(a | b))
print(sorted(a & b))
print(sorted(a - b))
print(sorted(a ^ b))""")
task('Gib die Buchstaben, die in **beiden** Wörtern vorkommen, sortiert aus.',
     given="""wort1 = 'programmieren'
wort2 = 'informatik'""",
     solution="""wort1 = 'programmieren'
wort2 = 'informatik'
print(sorted(set(wort1) & set(wort2)))""")
task('Gib die Buchstaben, die in `wort1`, aber nicht in `wort2` vorkommen, sortiert aus.',
     given="""wort1 = 'programmieren'
wort2 = 'informatik'""",
     solution="""wort1 = 'programmieren'
wort2 = 'informatik'
print(sorted(set(wort1) - set(wort2)))""")
task('Gib die Zahlen, die in **allen drei** Sets vorkommen, sortiert aus.',
     given="""a = {1, 2, 3, 4, 5, 6}
b = {2, 4, 6, 8}
c = {4, 5, 6, 7}""",
     solution="""a = {1, 2, 3, 4, 5, 6}
b = {2, 4, 6, 8}
c = {4, 5, 6, 7}
print(sorted(a & b & c))""")
task('Ändere `a` mit `intersection_update()` so, dass nur noch die Elemente übrig bleiben, die auch in `b` sind. Gib `a` sortiert aus.',
     given="""a = {1, 2, 3, 4, 5}
b = {2, 3, 5, 7}""",
     solution="""a = {1, 2, 3, 4, 5}
b = {2, 3, 5, 7}
a.intersection_update(b)
print(sorted(a))""")
task('Entferne mit `difference_update()` alle Zahlen aus `zahlen`, die in `ungueltig` stehen. Gib `zahlen` sortiert aus.',
     given="""zahlen = {10, 20, 30, 40, 50}
ungueltig = [20, 40, 60]""",
     solution="""zahlen = {10, 20, 30, 40, 50}
ungueltig = [20, 40, 60]
zahlen.difference_update(ungueltig)
print(sorted(zahlen))""")
task('Gib aus, wie viele **verschiedene** Wörter in beiden Texten vorkommen. Groß- und Kleinschreibung sollen keine Rolle spielen.',
     given="""text1 = 'Der Hund spielt mit dem Ball im Garten'
text2 = 'Im Garten spielt die Katze mit dem Hund'""",
     solution="""text1 = 'Der Hund spielt mit dem Ball im Garten'
text2 = 'Im Garten spielt die Katze mit dem Hund'
w1 = set(text1.lower().split())
w2 = set(text2.lower().split())
print(len(w1 & w2))""")
predict("""a = {1, 2, 3, 4}
b = {3, 4, 5}
print(a | b)
print(a & b)
print(a - b)
print(b - a)
print(a ^ b)""")
predict("""a = {1, 2, 3}
b = {2, 3, 4}
c = a.union(b)
a.intersection_update(b)
print(a)
print(c)
print(len(a - b))""")

# ---------------------------------------------------------------- 6
sec('Teilmengen und Vergleiche')
expl('''#### `issubset()`, `issuperset()` und `isdisjoint()`

- `a.issubset(b)` oder `a <= b`: Ist jedes Element von `a` auch in `b`? (`a` ist **Teilmenge** von `b`.)
- `a.issuperset(b)` oder `a >= b`: Ist jedes Element von `b` auch in `a`? (`a` ist **Obermenge** von `b`.)
- `a.isdisjoint(b)`: Haben `a` und `b` **keine** gemeinsamen Elemente?
- `a == b`: Haben beide Sets genau dieselben Elemente? Die Reihenfolge spielt keine Rolle.''',
     """a = {1, 2}
b = {1, 2, 3}
print(a.issubset(b), a <= b)
print(b.issuperset(a), b >= a)
print(a.isdisjoint({4, 5}))
print({1, 2, 3} == {3, 2, 1})""")

task('Prüfe mit `issubset()`, ob alle Zutaten für das Rezept im Vorrat sind. Gib `alles da` oder `es fehlt etwas` aus.',
     given="""zutaten = {'Mehl', 'Eier', 'Milch', 'Zucker'}
vorrat = {'Mehl', 'Milch', 'Butter', 'Zucker', 'Salz'}""",
     solution="""zutaten = {'Mehl', 'Eier', 'Milch', 'Zucker'}
vorrat = {'Mehl', 'Milch', 'Butter', 'Zucker', 'Salz'}
if zutaten.issubset(vorrat):
    print('alles da')
else:
    print('es fehlt etwas')""")
task('Gib aus, welche Zutaten fehlen (sortiert).',
     given="""zutaten = {'Mehl', 'Eier', 'Milch', 'Zucker'}
vorrat = {'Mehl', 'Milch', 'Butter', 'Zucker', 'Salz'}""",
     solution="""zutaten = {'Mehl', 'Eier', 'Milch', 'Zucker'}
vorrat = {'Mehl', 'Milch', 'Butter', 'Zucker', 'Salz'}
print(sorted(zutaten - vorrat))""")
task('Prüfe mit `isdisjoint()`, ob die beiden Gruppen keine gemeinsamen Mitglieder haben. Gib `keine Überschneidung` oder `Überschneidung` aus.',
     given="""gruppe_a = {'Ali', 'Bea', 'Cem'}
gruppe_b = {'Dana', 'Eli', 'Finn'}""",
     solution="""gruppe_a = {'Ali', 'Bea', 'Cem'}
gruppe_b = {'Dana', 'Eli', 'Finn'}
if gruppe_a.isdisjoint(gruppe_b):
    print('keine Überschneidung')
else:
    print('Überschneidung')""")
task('Prüfe mit `issuperset()`, ob `kenntnisse` alle Kenntnisse aus `anforderungen` enthält. Gib `True` oder `False` aus.',
     given="""anforderungen = {'Python', 'SQL'}
kenntnisse = {'Python', 'HTML', 'SQL', 'Java'}""",
     solution="""anforderungen = {'Python', 'SQL'}
kenntnisse = {'Python', 'HTML', 'SQL', 'Java'}
print(kenntnisse.issuperset(anforderungen))""")
task('Prüfe, ob die beiden Listen dieselben Elemente enthalten, egal in welcher Reihenfolge und wie oft. Wandle sie dazu in Sets um. Gib `True` oder `False` aus.',
     given="""a = [3, 1, 2, 3, 1]
b = [1, 2, 2, 3]""",
     solution="""a = [3, 1, 2, 3, 1]
b = [1, 2, 2, 3]
print(set(a) == set(b))""")
task("Prüfe mit `<=`, ob `zahl` nur aus den Zeichen `0` und `1` besteht, also eine Binärzahl ist. Gib `Binärzahl` oder `keine Binärzahl` aus. Teste auch mit `'10201'`.",
     given="zahl = '1011001'",
     solution="""zahl = '1011001'
if set(zahl) <= {'0', '1'}:
    print('Binärzahl')
else:
    print('keine Binärzahl')""")
task("Ein Pangramm ist ein Satz, der jeden Buchstaben von a bis z enthält. Prüfe mit `issubset()`, ob `satz` ein Pangramm ist. Gib `Pangramm` oder `kein Pangramm` aus.",
     given="satz = 'Franz jagt im komplett verwahrlosten Taxi quer durch Bayern'",
     solution="""satz = 'Franz jagt im komplett verwahrlosten Taxi quer durch Bayern'
alphabet = set('abcdefghijklmnopqrstuvwxyz')
if alphabet.issubset(set(satz.lower())):
    print('Pangramm')
else:
    print('kein Pangramm')""")
predict("""a = {1, 2}
b = {1, 2, 3}
print(a <= b)
print(b <= a)
print(a.isdisjoint({3, 4}))
print({1, 2, 2} == {2, 1})""")

# ---------------------------------------------------------------- 7
sec('Kopieren und frozenset')
expl('''#### `copy()`

Wie bei Listen ist `b = a` **keine** Kopie. Beide Namen zeigen dann auf dasselbe Set.
Eine echte Kopie erhält man mit `b = a.copy()` oder `b = set(a)`.''',
     """a = {1, 2, 3}
b = a
c = a.copy()
b.add(4)
print(a)
print(c)""")
expl('''#### `frozenset()`

Ein **frozenset** ist ein unveränderliches Set. Man erzeugt es mit `frozenset(...)`.
Es gibt kein `add()`, `remove()` usw., aber `in`, `len()` und die Mengenoperationen funktionieren.''',
     """vokale = frozenset('aeiou')
print(len(vokale))
print('e' in vokale)
print(sorted(vokale & set('Banane')))""")

task("Erstelle mit `copy()` eine Kopie `neu` von `farben`. Füge zur Kopie `'gelb'` hinzu. Gib beide Sets sortiert aus.",
     given=FARBEN, solution=FARBEN + """
neu = farben.copy()
neu.add('gelb')
print(sorted(farben))
print(sorted(neu))""")
task("Erstelle ein frozenset `wochenende` mit `'Sa'` und `'So'`. Prüfe für jeden Tag in `tage`, ob er zum Wochenende gehört, und gib den Tag mit `frei` oder `Schule` aus.",
     given="tage = ['Fr', 'Sa', 'So', 'Mo']",
     solution="""tage = ['Fr', 'Sa', 'So', 'Mo']
wochenende = frozenset(['Sa', 'So'])
for t in tage:
    if t in wochenende:
        print(t, 'frei')
    else:
        print(t, 'Schule')""")
predict("""a = {1, 2, 3}
b = a
b.remove(1)
print(a)
c = set(a)
c.add(9)
print(a)
print(len(c))""")
predict("""fs = frozenset([1, 2])
print(len(fs | {3}))
fs.add(3)""", error=AttributeError)

# ---------------------------------------------------------------- 8
sec('Gemischte Übungen')
task('Gib aus, wie viele verschiedene Wörter in `text` vorkommen. Groß- und Kleinschreibung sollen keine Rolle spielen.',
     given="text = 'Die Sonne scheint und die Vögel singen und die Kinder spielen'",
     solution="""text = 'Die Sonne scheint und die Vögel singen und die Kinder spielen'
print(len(set(text.lower().split())))""")
task('Finde alle Zahlen, die in `liste` mehr als einmal vorkommen. Verwende zwei Sets: `gesehen` und `doppelt`. Gib `doppelt` sortiert aus.',
     given='liste = [4, 7, 1, 4, 9, 7, 3, 4, 8]',
     solution="""liste = [4, 7, 1, 4, 9, 7, 3, 4, 8]
gesehen = set()
doppelt = set()
for z in liste:
    if z in gesehen:
        doppelt.add(z)
    else:
        gesehen.add(z)
print(sorted(doppelt))""")
task('Finde das erste Zeichen in `text`, das zum zweiten Mal vorkommt. Verwende ein Set `gesehen` und `break`. Gib das Zeichen aus.',
     given="text = 'Programmieren'",
     solution="""text = 'Programmieren'
gesehen = set()
for c in text:
    if c in gesehen:
        print(c)
        break
    gesehen.add(c)""")
task("Prüfe, ob in `wort` jeder Buchstabe nur einmal vorkommt. Vergleiche dazu die Längen. Gib `alle verschieden` oder `doppelte Buchstaben` aus. Teste auch mit `'Blume'`.",
     given="wort = 'Tasse'",
     solution="""wort = 'Tasse'
if len(set(wort)) == len(wort):
    print('alle verschieden')
else:
    print('doppelte Buchstaben')""")
task('Beim Lotto wird `tipp` mit `gezogen` verglichen. Gib die richtigen Zahlen sortiert und danach ihre Anzahl aus.',
     given="""tipp = {3, 12, 19, 25, 33, 41}
gezogen = {7, 12, 19, 28, 33, 45}""",
     solution="""tipp = {3, 12, 19, 25, 33, 41}
gezogen = {7, 12, 19, 28, 33, 45}
richtige = tipp & gezogen
print(sorted(richtige))
print(len(richtige))""")
task('Gib die Vokale, die in `wort` vorkommen, sortiert aus. Groß- und Kleinschreibung sollen keine Rolle spielen.',
     given="wort = 'Ausnahme'",
     solution="""wort = 'Ausnahme'
print(sorted(set(wort.lower()) & set('aeiou')))""")
task('In `liste` sollten alle Zahlen von 1 bis 15 stehen, aber einige fehlen. Gib die fehlenden Zahlen sortiert aus.',
     given='liste = [3, 1, 7, 15, 2, 9, 11, 4, 13, 6, 10]',
     solution="""liste = [3, 1, 7, 15, 2, 9, 11, 4, 13, 6, 10]
print(sorted(set(range(1, 16)) - set(liste)))""")
task('Gib die gemeinsamen Freunde von Anna und Ben sortiert aus. Gib danach die Freunde aus, die nur Anna hat.',
     given="""anna = {'Cem', 'Dana', 'Eli', 'Finn'}
ben = {'Dana', 'Finn', 'Gül', 'Hans'}""",
     solution="""anna = {'Cem', 'Dana', 'Eli', 'Finn'}
ben = {'Dana', 'Finn', 'Gül', 'Hans'}
print(sorted(anna & ben))
print(sorted(anna - ben))""")
task('Entferne die Duplikate aus `liste`, aber behalte die Reihenfolge des ersten Vorkommens. Verwende ein Set `gesehen` und eine neue Liste. Gib die neue Liste aus.',
     given="liste = ['b', 'a', 'b', 'c', 'a', 'd', 'c']",
     solution="""liste = ['b', 'a', 'b', 'c', 'a', 'd', 'c']
gesehen = set()
ergebnis = []
for x in liste:
    if x not in gesehen:
        gesehen.add(x)
        ergebnis.append(x)
print(ergebnis)""")
task('Jedes Tupel in `belegung` enthält einen Schüler und einen Kurs. Gib alle Kurse sortiert aus, die mindestens einmal belegt sind. Gib danach aus, wie viele verschiedene Schüler es gibt.',
     given="belegung = [('Ali', 'Info'), ('Bea', 'Kunst'), ('Ali', 'Sport'), ('Cem', 'Info'), ('Bea', 'Info')]",
     solution="""belegung = [('Ali', 'Info'), ('Bea', 'Kunst'), ('Ali', 'Sport'), ('Cem', 'Info'), ('Bea', 'Info')]
kurse = set()
schueler = set()
for name, kurs in belegung:
    kurse.add(kurs)
    schueler.add(name)
print(sorted(kurse))
print(len(schueler))""")
task('Gib die Wörter sortiert aus, die in **allen drei** Sätzen vorkommen.',
     given="""s1 = 'heute ist das wetter schön und warm'
s2 = 'das wetter ist heute nicht schön'
s3 = 'ist das wetter morgen auch so schön'""",
     solution="""s1 = 'heute ist das wetter schön und warm'
s2 = 'das wetter ist heute nicht schön'
s3 = 'ist das wetter morgen auch so schön'
print(sorted(set(s1.split()) & set(s2.split()) & set(s3.split())))""")
task('Gib die Buchstaben von a bis z sortiert aus, die in **keinem** der Wörter vorkommen.',
     given="woerter = ['python', 'liste', 'menge', 'tupel', 'schleife']",
     solution="""woerter = ['python', 'liste', 'menge', 'tupel', 'schleife']
benutzt = set()
for w in woerter:
    benutzt.update(w)
print(sorted(set('abcdefghijklmnopqrstuvwxyz') - benutzt))""")
task('Erzeuge ein Set mit allen Zahlen von 1 bis 30, die durch 2 oder durch 3 teilbar sind. Verwende zwei Sets und `|`. Gib die Anzahl aus.',
     solution="""zweier = set(range(2, 31, 2))
dreier = set(range(3, 31, 3))
print(len(zweier | dreier))""")
predict("""a = set('hallo')
b = set('welt')
print(len(a))
print(sorted(a & b))
print(sorted(a - b))
print(len(a | b))""")

generate('sets', 'Sets')
