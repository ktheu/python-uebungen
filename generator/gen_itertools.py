# Erzeugt ../content/itertools.ipynb (siehe nbgen.py).
from nbgen import sec, expl, task, predict, generate


def t(text, given='', body='', kind='normal'):
    """Aufgabe, deren Lösung aus dem vorgegebenen Code plus body besteht."""
    task(text, given=given, solution=(given + '\n' + body) if given else body, kind=kind)


# ---------------------------------------------------------------- 1
sec('Iteratoren, enumerate() und zip()')
expl('''#### Was ist ein Iterator?

Ein **Iterator** liefert seine Werte **einen nach dem anderen**, erst dann, wenn man sie braucht.
Die Funktionen aus dem Modul `itertools` geben fast alle Iteratoren zurück.

- Gibt man einen Iterator mit `print()` aus, sieht man nur ein Objekt, nicht die Werte.
- Mit `list(iterator)` erhält man alle Werte als Liste. Mit einer `for`-Schleife kann man sie durchlaufen.
- `next(iterator)` liefert den **nächsten** Wert. Gibt es keinen mehr, entsteht ein `StopIteration`-Fehler.
- Ein Iterator ist nach einem Durchlauf **verbraucht**. Ein zweites `list()` ergibt eine leere Liste.
- `iter(liste)` macht aus einer Liste (oder einer Zeichenkette) einen Iterator.''',
     """it = iter(['a', 'b', 'c'])
print(it)
print(next(it))
print(list(it))
print(list(it))""")
expl('''#### Module importieren

Die Funktionen aus `itertools` muss man erst **importieren**:

- `import itertools` und dann `itertools.count(...)`, oder
- `from itertools import count, cycle` und dann direkt `count(...)`.''',
     """import itertools
from itertools import repeat

print(list(itertools.repeat('ha', 3)))
print(list(repeat(0, 4)))""")
expl('''#### `enumerate()` und `zip()`

Zwei eingebaute Funktionen liefern ebenfalls Iteratoren und werden oft zusammen mit `itertools` benutzt:

- `enumerate(liste)` liefert Paare `(index, element)`. Mit `enumerate(liste, 1)` beginnt die Zählung bei 1.
- `zip(a, b)` liefert Paare aus den Elementen von `a` und `b` mit demselben Index. Es hört auf, sobald **eine** der Listen zu Ende ist.''',
     """namen = ['Ali', 'Bea', 'Cem']
for i, name in enumerate(namen, 1):
    print(i, name)
noten = [2, 1, 3]
for name, note in zip(namen, noten):
    print(name, note)
print(list(zip('abc', [1, 2])))""")

t('Erzeuge mit `iter()` einen Iterator aus `tiere`. Gib mit `next()` nacheinander die ersten beiden Elemente aus und danach mit `list()` den Rest.',
  "tiere = ['Hund', 'Katze', 'Maus', 'Pferd']",
  """it = iter(tiere)
print(next(it))
print(next(it))
print(list(it))""")
t("Importiere `itertools` mit `import itertools`. Gib mit `itertools.repeat()` eine Liste aus, die fünfmal `'ja'` enthält.",
  body="""import itertools
print(list(itertools.repeat('ja', 5)))""")
t('Gib die Namen mit `enumerate()` nummeriert aus wie unten. Die Zählung soll bei 1 beginnen.',
  "namen = ['Ali', 'Bea', 'Cem', 'Dana']",
  """for i, name in enumerate(namen, 1):
    print(f'{i}. {name}')""")
t('Gib mit `enumerate()` die Indizes aller Elemente von `zahlen` aus, die größer als 10 sind.',
  'zahlen = [5, 12, 8, 31, 2, 17]',
  """for i, z in enumerate(zahlen):
    if z > 10:
        print(i)""")
t('Gib mit `zip()` jeden Namen mit seiner Note aus wie unten.',
  """namen = ['Ali', 'Bea', 'Cem']
noten = [2, 1, 3]""",
  """for name, note in zip(namen, noten):
    print(f'{name}: {note}')""")
t('Erstelle mit `zip()` und `dict()` ein Dictionary, das jedem Land seine Hauptstadt zuordnet. Gib es aus.',
  """laender = ['Deutschland', 'Frankreich', 'Italien']
staedte = ['Berlin', 'Paris', 'Rom']""",
  """print(dict(zip(laender, staedte)))""")
t('Berechne mit `zip()` die Summe der Produkte `preise[i] * anzahl[i]` und gib sie aus.',
  """preise = [2, 3, 5]
anzahl = [4, 1, 2]""",
  """summe = 0
for p, a in zip(preise, anzahl):
    summe += p * a
print(summe)""")
predict("""it = iter([1, 2, 3])
print(next(it))
print(list(it))
print(list(it))
print(list(zip([1, 2, 3], 'ab')))""")
predict("""it = iter([1])
print(next(it))
print(next(it))""", error=StopIteration)

# ---------------------------------------------------------------- 2
sec('islice()')
expl('''#### `islice()`

`islice(iterable, stop)` liefert die ersten `stop` Werte, so wie `liste[:stop]`.
Mit `islice(iterable, start, stop)` oder `islice(iterable, start, stop, schritt)` geht es wie beim Slicing.

Der Vorteil: `islice()` funktioniert auch mit Iteratoren, die man nicht mit `[...]` zerschneiden kann,
zum Beispiel mit **unendlichen** Iteratoren (siehe nächster Abschnitt).''',
     """from itertools import islice

zahlen = [10, 20, 30, 40, 50, 60]
print(list(islice(zahlen, 3)))
print(list(islice(zahlen, 2, 5)))
print(list(islice(zahlen, 0, None, 2)))""")

IS = 'from itertools import islice\nzahlen = [5, 12, 8, 3, 19, 7, 14, 2]'
t('Gib mit `islice()` die ersten drei Elemente von `zahlen` als Liste aus.',
  IS, "print(list(islice(zahlen, 3)))")
t('Gib mit `islice()` die Elemente von Index 2 bis ausschließlich Index 6 als Liste aus.',
  IS, "print(list(islice(zahlen, 2, 6)))")
t('Gib mit `islice()` jedes zweite Element von `zahlen` als Liste aus, beginnend beim ersten. Als `stop` kannst du `None` angeben.',
  IS, "print(list(islice(zahlen, 0, None, 2)))")
t("Gib mit `islice()` und `''.join()` die ersten vier Buchstaben von `wort` aus.",
  "from itertools import islice\nwort = 'Informatik'",
  "print(''.join(islice(wort, 4)))")
t('Gib mit einer `for`-Schleife über `islice()` die ersten drei Zeilen von `text` aus. `text.splitlines()` liefert die Zeilen.',
  """from itertools import islice
text = '''Zeile eins
Zeile zwei
Zeile drei
Zeile vier'''""",
  """for zeile in islice(text.splitlines(), 3):
    print(zeile)""")
predict("""from itertools import islice
it = iter(range(10))
print(list(islice(it, 3)))
print(list(islice(it, 3)))
print(list(islice('abcdef', 1, None, 2)))""")

# ---------------------------------------------------------------- 3
sec('Unendliche Iteratoren: count(), cycle() und repeat()')
expl('''#### `count()`

`count(start, schritt)` zählt **ohne Ende**: `start`, `start + schritt`, `start + 2 * schritt`, ...
Ohne Angaben beginnt es bei 0 mit Schritt 1. Weil `count()` nie aufhört, braucht man `break` oder `islice()`.
**Niemals** `list(count())` schreiben, das läuft endlos.''',
     """from itertools import count, islice

for i in count(1):
    if i > 3:
        break
    print(i)
print(list(islice(count(10, 5), 4)))""")
expl('''#### `cycle()` und `repeat()`

- `cycle(iterable)` wiederholt die Elemente **immer wieder** von vorne: A, B, C, A, B, C, ...
- `repeat(wert, n)` liefert `n`-mal denselben Wert. Ohne `n` wiederholt es ihn unendlich oft.

Mit `zip()` hört die Schleife auf, sobald die **endliche** Liste zu Ende ist.''',
     """from itertools import cycle, repeat, islice

print(list(islice(cycle('ABC'), 7)))
print(list(repeat('x', 3)))
for name, team in zip(['Ali', 'Bea', 'Cem'], cycle(['rot', 'blau'])):
    print(name, team)""")

t('Gib mit `count(1)` und `break` die Zahlen von 1 bis 5 aus, jede in einer eigenen Zeile.',
  'from itertools import count',
  """for i in count(1):
    if i > 5:
        break
    print(i)""")
t('Gib mit `count()` und `islice()` die ersten vier Werte der Folge 10, 15, 20, ... als Liste aus.',
  'from itertools import count, islice',
  "print(list(islice(count(10, 5), 4)))")
t('Gib mit `count()` und `islice()` die ersten fünf Werte der Folge 0.5, 1.0, 1.5, ... als Liste aus.',
  'from itertools import count, islice',
  "print(list(islice(count(0.5, 0.5), 5)))")
t('Finde mit `count()` die kleinste Zahl ab 1, deren Quadrat größer als 500 ist. Gib sie aus.',
  'from itertools import count',
  """for i in count(1):
    if i * i > 500:
        print(i)
        break""")
t('Nummeriere die Namen mit `zip()` und `count(1)` wie unten.',
  "from itertools import count\nnamen = ['Ali', 'Bea', 'Cem']",
  """for nr, name in zip(count(1), namen):
    print(nr, name)""")
t('Die drei Spieler sind abwechselnd an der Reihe. Gib mit `cycle()` und `islice()` als Liste aus, wer bei den ersten 7 Zügen dran ist.',
  "from itertools import cycle, islice\nspieler = ['Ali', 'Bea', 'Cem']",
  "print(list(islice(cycle(spieler), 7)))")
t('Gib mit `cycle()` und `zip()` für 10 aufeinanderfolgende Tage den Wochentag aus wie unten. Der erste Tag ist ein Montag.',
  "from itertools import cycle\ntage = ['Mo', 'Di', 'Mi', 'Do', 'Fr', 'Sa', 'So']",
  """for nr, tag in zip(range(1, 11), cycle(tage)):
    print(f'Tag {nr}: {tag}')""")
t('Teile die Schüler mit `cycle()` abwechselnd den Teams A und B zu. Gib jeden Namen mit seinem Team aus.',
  "from itertools import cycle\nnamen = ['Ali', 'Bea', 'Cem', 'Dana', 'Eli']",
  """for name, team in zip(namen, cycle(['A', 'B'])):
    print(name, team)""")
t("Erzeuge mit `repeat()` und `''.join()` eine Linie aus 15 Gleichheitszeichen und gib sie aus.",
  'from itertools import repeat',
  "print(''.join(repeat('=', 15)))")
t('Erzeuge mit `repeat()` eine Liste mit vier Nullen und gib sie aus.',
  'from itertools import repeat',
  "print(list(repeat(0, 4)))")
t('Erzeuge mit `cycle()` eine Zeichenkette der Länge 12, die abwechselnd `#` und `.` enthält. Gib sie aus.',
  'from itertools import cycle, islice',
  "print(''.join(islice(cycle('#.'), 12)))")
predict("""from itertools import count, cycle, islice
c = count(3, 2)
print(next(c), next(c), next(c))
print(list(islice(cycle([1, 2]), 5)))
print(list(zip('abc', count(100))))""")

# ---------------------------------------------------------------- 4
sec('Verbinden und Paare bilden')
expl('''#### `chain()` und `chain.from_iterable()`

- `chain(a, b, c)` liefert erst alle Elemente von `a`, dann alle von `b`, dann alle von `c`.
- `chain.from_iterable(liste_von_listen)` macht dasselbe für eine Liste von Listen. So macht man z. B.
  aus einem Grid eine einfache Liste („flach machen“).''',
     """from itertools import chain

print(list(chain([1, 2], [3], [4, 5])))
grid = [[1, 2, 3], [4, 5, 6]]
print(list(chain.from_iterable(grid)))""")
expl('''#### `zip_longest()` und `pairwise()`

- `zip_longest(a, b, fillvalue=...)` arbeitet wie `zip()`, hört aber erst auf, wenn die **längste** Liste zu Ende ist.
  Fehlende Werte werden durch `fillvalue` ersetzt (sonst `None`).
- `pairwise(liste)` liefert alle **benachbarten Paare**: `(a[0], a[1])`, `(a[1], a[2])`, ...''',
     """from itertools import zip_longest, pairwise

print(list(zip_longest('abc', [1], fillvalue='-')))
print(list(pairwise([1, 4, 9, 16])))""")

t('Verbinde die drei Listen mit `chain()` und gib das Ergebnis als Liste aus.',
  """from itertools import chain
a = [1, 2]
b = [3, 4, 5]
c = [6]""",
  "print(list(chain(a, b, c)))")
t("Verbinde mit `chain()` die Zeichenkette `'ab'` und die Liste `[1, 2]`. Gib das Ergebnis als Liste aus.",
  'from itertools import chain',
  "print(list(chain('ab', [1, 2])))")
t('Mache das Grid mit `chain.from_iterable()` zu einer einfachen Liste. Gib sie aus.',
  'from itertools import chain\ngrid = [[5, 3, 8], [2, 9, 4], [6, 0, 3]]',
  "print(list(chain.from_iterable(grid)))")
t('Berechne mit `chain.from_iterable()` und `sum()` die Summe aller Elemente des Grids. Gib auch das Maximum aus.',
  'from itertools import chain\ngrid = [[5, 3, 8], [2, 9, 4], [6, 0, 3]]',
  """print(sum(chain.from_iterable(grid)))
print(max(chain.from_iterable(grid)))""")
t("Gib alle Fächer, die in mindestens einer Klasse unterrichtet werden, alphabetisch sortiert und ohne Duplikate aus. Verwende `chain.from_iterable()`, `set()` und `sorted()`.",
  "from itertools import chain\nfaecher = [['Mathe', 'Info'], ['Deutsch', 'Mathe'], ['Info', 'Kunst']]",
  "print(sorted(set(chain.from_iterable(faecher))))")
t("Gib mit `zip_longest()` jeden Namen mit seiner Note aus. Fehlt eine Note, soll `-` ausgegeben werden.",
  """from itertools import zip_longest
namen = ['Ali', 'Bea', 'Cem', 'Dana']
noten = [2, 1]""",
  """for name, note in zip_longest(namen, noten, fillvalue='-'):
    print(name, note)""")
t('Gib die beiden Spalten mit `zip_longest()` nebeneinander aus wie unten. Die erste Spalte ist 8 Zeichen breit, fehlende Einträge werden durch leere Zeichenketten ersetzt.',
  """from itertools import zip_longest
links = ['Milch', 'Brot', 'Eier']
rechts = ['Käse', 'Wurst', 'Saft', 'Tee']""",
  """for a, b in zip_longest(links, rechts, fillvalue=''):
    print(f'{a:8}{b}')""")
t('Berechne mit `pairwise()` die Differenzen zwischen benachbarten Werten von `werte`. Gib sie als Liste aus.',
  'from itertools import pairwise\nwerte = [2, 5, 9, 10, 16]',
  """diffs = []
for a, b in pairwise(werte):
    diffs.append(b - a)
print(diffs)""")
t('Prüfe mit `pairwise()`, ob `a` aufsteigend sortiert ist. Gib `sortiert` oder `nicht sortiert` aus.',
  'from itertools import pairwise\na = [1, 3, 5, 4, 9]',
  """ok = True
for x, y in pairwise(a):
    if x > y:
        ok = False
if ok:
    print('sortiert')
else:
    print('nicht sortiert')""")
t("Gib mit `pairwise()` alle Buchstabenpaare von `wort` aus, jeweils als zusammengesetzte Zeichenkette.",
  "from itertools import pairwise\nwort = 'Tisch'",
  """for a, b in pairwise(wort):
    print(a + b)""")
t('Zähle mit `pairwise()`, an wie vielen Tagen die Temperatur höher war als am Vortag. Gib die Anzahl aus.',
  'from itertools import pairwise\ntemperaturen = [14, 16, 15, 18, 21, 19, 22]',
  """anzahl = 0
for gestern, heute in pairwise(temperaturen):
    if heute > gestern:
        anzahl += 1
print(anzahl)""")
predict("""from itertools import chain, zip_longest, pairwise
print(list(chain('ab', 'cd')))
print(list(zip([1, 2, 3], 'xy')))
print(list(zip_longest([1, 2, 3], 'xy')))
print(len(list(pairwise('Hallo'))))""")

# ---------------------------------------------------------------- 5
sec('Filtern')
expl('''#### `lambda`

Viele `itertools`-Funktionen bekommen eine **Funktion** als Argument. Für kurze Funktionen gibt es `lambda`:

`lambda x: x > 3` ist eine Funktion mit dem Parameter `x`, die `x > 3` zurückgibt. Sie entspricht

```python
def groesser_drei(x):
    return x > 3
```

Statt `lambda` kann man immer auch eine mit `def` geschriebene Funktion verwenden. Man gibt dann nur ihren Namen an, ohne Klammern.''',
     """quadrat = lambda x: x * x
print(quadrat(5))

def ist_gerade(n):
    return n % 2 == 0

print(list(filter(ist_gerade, [1, 2, 3, 4])))
print(list(filter(lambda x: x > 2, [1, 2, 3, 4])))""")
expl('''#### `compress()`, `takewhile()`, `dropwhile()` und `filterfalse()`

- `compress(daten, auswahl)` liefert die Elemente von `daten`, bei denen in `auswahl` an derselben Stelle `True` (oder 1) steht.
- `takewhile(f, liste)` liefert Elemente, **solange** `f` wahr ist, und hört beim ersten falschen Element auf.
- `dropwhile(f, liste)` überspringt Elemente, solange `f` wahr ist, und liefert dann **alle** übrigen.
- `filterfalse(f, liste)` liefert alle Elemente, für die `f` **falsch** ist. Das eingebaute `filter(f, liste)` liefert die, für die `f` wahr ist.''',
     """from itertools import compress, takewhile, dropwhile, filterfalse

print(list(compress('ABCD', [1, 0, 1, 0])))
z = [1, 3, 5, 8, 2, 4]
print(list(takewhile(lambda x: x < 6, z)))
print(list(dropwhile(lambda x: x < 6, z)))
print(list(filterfalse(lambda x: x < 6, z)))""")

t('Schreibe eine `lambda`-Funktion `doppelt`, die eine Zahl verdoppelt. Gib `doppelt(21)` aus.',
  body="""doppelt = lambda x: 2 * x
print(doppelt(21))""")
t('Gib mit `compress()` die Namen der Schüler aus, die anwesend sind. Gib das Ergebnis als Liste aus.',
  """from itertools import compress
namen = ['Ali', 'Bea', 'Cem', 'Dana', 'Eli']
anwesend = [True, False, True, True, False]""",
  "print(list(compress(namen, anwesend)))")
t('Gib mit `compress()` die Buchstaben von `wort` aus, bei denen in `maske` eine 1 steht, und setze sie zu einer Zeichenkette zusammen.',
  """from itertools import compress
wort = 'Programmieren'
maske = [1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0]""",
  "print(''.join(compress(wort, maske)))")
t('Die Liste `zahlen` ist sortiert. Gib mit `takewhile()` alle Zahlen kleiner als 10 als Liste aus.',
  'from itertools import takewhile\nzahlen = [1, 4, 7, 9, 12, 15, 20]',
  "print(list(takewhile(lambda x: x < 10, zahlen)))")
t("Entferne mit `dropwhile()` die Leerzeichen am Anfang von `text`. Setze das Ergebnis mit `''.join()` zusammen und gib es zwischen `|` aus.",
  "from itertools import dropwhile\ntext = '   Hallo Welt  '",
  "print('|' + ''.join(dropwhile(lambda c: c == ' ', text)) + '|')")
t('Gib mit `dropwhile()` alle Messwerte ab dem ersten Wert über 20 als Liste aus.',
  'from itertools import dropwhile\nmesswerte = [12, 15, 19, 23, 18, 25, 17]',
  "print(list(dropwhile(lambda x: x <= 20, messwerte)))")
t('Gib mit `takewhile()` und `count(1)` alle Quadratzahlen kleiner als 100 als Liste aus. Tipp: Nimm die Zahlen `i`, solange `i * i < 100` ist, und quadriere sie danach in einer List Comprehension.',
  'from itertools import takewhile, count',
  """zahlen = takewhile(lambda i: i * i < 100, count(1))
print([i * i for i in zahlen])""")
t('Schreibe eine Funktion `ist_gerade(n)` mit `def`. Gib mit `filterfalse()` und dieser Funktion alle ungeraden Zahlen aus `zahlen` als Liste aus.',
  'from itertools import filterfalse\nzahlen = [3, 8, 12, 5, 6, 7, 10]',
  """
def ist_gerade(n):
    return n % 2 == 0

print(list(filterfalse(ist_gerade, zahlen)))""")
t('Teile `woerter` mit `filter()` und `filterfalse()` in die Wörter mit mehr als 4 Buchstaben und den Rest auf. Gib beide Listen aus.',
  "from itertools import filterfalse\nwoerter = ['Haus', 'Elefant', 'Ei', 'Computer', 'Baum']",
  """lang = lambda w: len(w) > 4
print(list(filter(lang, woerter)))
print(list(filterfalse(lang, woerter)))""")
predict("""from itertools import takewhile, filterfalse
z = [1, 4, 6, 3, 8]
print(list(takewhile(lambda x: x < 5, z)))
print(list(filter(lambda x: x < 5, z)))
print(list(filterfalse(lambda x: x < 5, z)))""")

# ---------------------------------------------------------------- 6
sec('accumulate() und starmap()')
expl('''#### `accumulate()`

`accumulate(liste)` liefert die **laufenden Summen**: das erste Element, die Summe der ersten beiden, der ersten drei usw.

- Mit `accumulate(liste, funktion)` wird statt `+` die Funktion verwendet, z. B. `max` für das laufende Maximum.
  Die Funktion bekommt das bisherige Ergebnis und das nächste Element.
- Mit `initial=wert` beginnt die Rechnung mit einem Startwert.''',
     """from itertools import accumulate

print(list(accumulate([1, 2, 3, 4])))
print(list(accumulate([3, 1, 5, 2], max)))
print(list(accumulate([1, 2, 3], lambda a, b: a * b)))
print(list(accumulate([5, -2], initial=10)))""")
expl('''#### `starmap()`

`starmap(funktion, liste_von_tupeln)` ruft die Funktion für jedes Tupel auf und übergibt die Elemente des Tupels
als einzelne Argumente. Aus `(2, 3)` wird also `funktion(2, 3)`.''',
     """from itertools import starmap

def flaeche(breite, hoehe):
    return breite * hoehe

print(list(starmap(flaeche, [(2, 3), (4, 5)])))
print(list(starmap(pow, [(2, 3), (10, 2)])))""")

t('Gib mit `accumulate()` die laufenden Summen von `zahlen` als Liste aus.',
  'from itertools import accumulate\nzahlen = [3, 1, 4, 1, 5, 9]',
  "print(list(accumulate(zahlen)))")
t('Das Konto startet mit 100 Euro. Gib mit `accumulate()` und `initial` den Kontostand nach jeder Buchung als Liste aus.',
  'from itertools import accumulate\nbuchungen = [-20, 50, -35, -10, 80]',
  "print(list(accumulate(buchungen, initial=100)))")
t('Gib mit `accumulate()` und `max` das laufende Maximum der Temperaturen als Liste aus.',
  'from itertools import accumulate\ntemperaturen = [14, 16, 15, 18, 21, 19, 22]',
  "print(list(accumulate(temperaturen, max)))")
t('Gib mit `accumulate()` und `min` das laufende Minimum von `zahlen` als Liste aus.',
  'from itertools import accumulate\nzahlen = [8, 9, 5, 7, 3, 6]',
  "print(list(accumulate(zahlen, min)))")
t('Gib mit `accumulate()` und einer `lambda`-Funktion die Fakultäten 1!, 2!, ..., 6! als Liste aus.',
  'from itertools import accumulate',
  "print(list(accumulate(range(1, 7), lambda a, b: a * b)))")
t('Gib mit `accumulate()` alle Anfänge von `wort` aus, jeden in einer eigenen Zeile.',
  "from itertools import accumulate\nwort = 'Haus'",
  """for anfang in accumulate(wort):
    print(anfang)""")
t('Gib mit `starmap()` und `pow` die Potenzen zu den Paaren in `paare` als Liste aus.',
  'from itertools import starmap\npaare = [(2, 3), (3, 2), (10, 2), (5, 0)]',
  "print(list(starmap(pow, paare)))")
t('Schreibe eine Funktion `flaeche(breite, hoehe)`. Berechne mit `starmap()` die Flächen aller Rechtecke und gib sie als Liste aus.',
  'from itertools import starmap\nrechtecke = [(2, 3), (4, 5), (1, 10)]',
  """
def flaeche(breite, hoehe):
    return breite * hoehe

print(list(starmap(flaeche, rechtecke)))""")
t('Jedes Tupel in `korb` enthält Preis und Anzahl. Berechne mit `starmap()`, einer `lambda`-Funktion und `sum()` den Gesamtpreis.',
  'from itertools import starmap\nkorb = [(2, 3), (4, 1), (5, 2)]',
  "print(sum(starmap(lambda preis, anzahl: preis * anzahl, korb)))")
predict("""from itertools import accumulate, starmap
print(list(accumulate([1, 1, 1, 1])))
print(list(accumulate('abc')))
print(list(accumulate([2, 3], initial=1)))
print(list(starmap(max, [(1, 5), (7, 2)])))""")

# ---------------------------------------------------------------- 7
sec('groupby()')
expl('''#### `groupby()`

`groupby(liste)` fasst **direkt aufeinanderfolgende** gleiche Elemente zu Gruppen zusammen.
Es liefert Paare `(schluessel, gruppe)`. Die Gruppe ist selbst ein Iterator, den man z. B. mit `list()` ausliest.

- Mit `groupby(liste, key=funktion)` wird nach dem Ergebnis der Funktion gruppiert.
- Weil nur **benachbarte** Elemente zusammengefasst werden, muss man die Liste meist vorher mit **demselben** `key` sortieren.''',
     """from itertools import groupby

for k, g in groupby('aaabbca'):
    print(k, list(g))
woerter = ['Ast', 'Bus', 'Affe', 'Bahn']
woerter.sort()
for k, g in groupby(woerter, key=lambda w: w[0]):
    print(k, list(g))""")

t("Gib mit `groupby()` für jede Gruppe gleicher Buchstaben in `text` den Buchstaben und die Länge der Gruppe aus.",
  "from itertools import groupby\ntext = 'aaabbcaa'",
  """for k, g in groupby(text):
    print(k, len(list(g)))""")
t("Erzeuge mit `groupby()` die Lauflängenkodierung von `text`: Jede Gruppe wird durch den Buchstaben und die Anzahl ersetzt. Gib das Ergebnis aus.",
  "from itertools import groupby\ntext = 'WWWWBBBWWBBBBBB'",
  """ergebnis = ''
for k, g in groupby(text):
    ergebnis += k + str(len(list(g)))
print(ergebnis)""")
t('Gruppiere die Wörter mit `groupby()` nach ihrem Anfangsbuchstaben. Sortiere die Liste vorher. Gib jeden Buchstaben mit der Liste seiner Wörter aus.',
  "from itertools import groupby\nwoerter = ['Birne', 'Apfel', 'Kiwi', 'Banane', 'Ananas', 'Aprikose']",
  """woerter.sort()
for k, g in groupby(woerter, key=lambda w: w[0]):
    print(k, list(g))""")
t('Gruppiere die Wörter nach ihrer Länge. Sortiere vorher mit `key=len` und gruppiere mit `key=len`. Gib jede Länge mit der Liste ihrer Wörter aus.',
  "from itertools import groupby\nwoerter = ['Haus', 'Ei', 'Baum', 'Elefant', 'Eis', 'Kuh', 'Maus']",
  """woerter.sort(key=len)
for k, g in groupby(woerter, key=len):
    print(k, list(g))""")
t('''Jedes Tupel in `schueler` enthält Name und Klasse. Schreibe eine Funktion `klasse(eintrag)`, die die Klasse zurückgibt.
Sortiere und gruppiere damit und gib für jede Klasse die Namen aus wie unten.''',
  "from itertools import groupby\nschueler = [('Ali', '10a'), ('Bea', '10b'), ('Cem', '10a'), ('Dana', '10c'), ('Eli', '10b')]",
  """
def klasse(eintrag):
    return eintrag[1]

schueler.sort(key=klasse)
for k, g in groupby(schueler, key=klasse):
    namen = [name for name, kl in g]
    print(k, namen)""")
t('Finde mit `groupby()` die längste Serie gleicher Augenzahlen in `wuerfe`. Gib die Augenzahl und die Länge der Serie aus.',
  'from itertools import groupby\nwuerfe = [3, 6, 6, 2, 5, 5, 5, 1, 6, 6]',
  """beste_zahl = 0
beste_laenge = 0
for k, g in groupby(wuerfe):
    laenge = len(list(g))
    if laenge > beste_laenge:
        beste_zahl = k
        beste_laenge = laenge
print(beste_zahl, beste_laenge)""")
t('Gib mit `sorted()` und `groupby()` die Notenverteilung aus: für jede vorkommende Note, wie oft sie vorkommt.',
  'from itertools import groupby\nnoten = [2, 3, 1, 2, 4, 2, 3, 1, 2]',
  """for note, g in groupby(sorted(noten)):
    print(note, len(list(g)))""")
predict("""from itertools import groupby
z = [1, 1, 2, 1, 1]
print([k for k, g in groupby(z)])
print([k for k, g in groupby(sorted(z))])
print([len(list(g)) for k, g in groupby(sorted(z))])""")

# ---------------------------------------------------------------- 8
sec('Kombinatorik')
expl('''#### `product()`

`product(a, b)` liefert **alle Kombinationen** aus einem Element von `a` und einem Element von `b`, als Tupel.
Das ist dasselbe wie zwei verschachtelte Schleifen. `product(a, repeat=3)` entspricht `product(a, a, a)`.''',
     """from itertools import product

print(list(product('AB', [1, 2])))
print(len(list(product('01', repeat=3))))""")
expl('''#### `permutations()`, `combinations()` und `combinations_with_replacement()`

- `permutations(liste, r)` liefert alle **Anordnungen** von `r` Elementen. Die Reihenfolge zählt: `(A, B)` und `(B, A)` sind verschieden.
  Ohne `r` werden alle Elemente angeordnet.
- `combinations(liste, r)` liefert alle **Auswahlen** von `r` Elementen ohne Wiederholung. Die Reihenfolge zählt nicht.
- `combinations_with_replacement(liste, r)` ist wie `combinations()`, aber ein Element darf mehrfach gewählt werden.''',
     """from itertools import permutations, combinations, combinations_with_replacement

print(list(permutations('ABC', 2)))
print(list(combinations('ABC', 2)))
print(list(combinations_with_replacement('ABC', 2)))""")

t('Ein T-Shirt gibt es in den Farben und Größen unten. Gib mit `product()` alle Varianten aus wie unten.',
  """from itertools import product
farben = ['rot', 'blau']
groessen = ['S', 'M', 'L']""",
  """for farbe, groesse in product(farben, groessen):
    print(farbe, groesse)""")
t("Gib mit `product()` und `repeat=3` alle dreistelligen Binärzahlen aus, jeweils als Zeichenkette wie `010`.",
  'from itertools import product',
  """for t in product('01', repeat=3):
    print(''.join(t))""")
t('Mit zwei Würfeln gibt es 36 mögliche Würfe. Zähle mit `product()`, bei wie vielen die Augensumme 7 ist. Gib die Anzahl aus.',
  'from itertools import product',
  """anzahl = 0
for a, b in product(range(1, 7), repeat=2):
    if a + b == 7:
        anzahl += 1
print(anzahl)""")
t("Gib mit `permutations()` alle Anordnungen der Buchstaben von `'ABC'` aus, jeweils als zusammengesetzte Zeichenkette.",
  'from itertools import permutations',
  """for p in permutations('ABC'):
    print(''.join(p))""")
t('Gib aus, wie viele Anordnungen es für 5 verschiedene Elemente gibt. Verwende `permutations()`, `list()` und `len()`.',
  'from itertools import permutations',
  "print(len(list(permutations(range(5)))))")
t('Beim Rennen gibt es Gold, Silber und Bronze. Gib aus, wie viele verschiedene Siegerpodeste mit den Läufern in `laeufer` möglich sind.',
  "from itertools import permutations\nlaeufer = ['Ali', 'Bea', 'Cem', 'Dana', 'Eli']",
  "print(len(list(permutations(laeufer, 3))))")
t('Im Turnier spielt jeder einmal gegen jeden. Gib mit `combinations()` alle Spiele aus wie unten.',
  "from itertools import combinations\nteams = ['Rot', 'Blau', 'Grün', 'Gelb']",
  """for a, b in combinations(teams, 2):
    print(f'{a} gegen {b}')""")
t('Gib aus, wie viele Möglichkeiten es gibt, aus 20 Schülern 3 für einen Ausflug auszuwählen.',
  'from itertools import combinations',
  "print(len(list(combinations(range(20), 3))))")
t('Gib mit `combinations()` alle Paare von Zahlen aus `zahlen` aus, deren Summe 10 ist.',
  'from itertools import combinations\nzahlen = [2, 8, 5, 3, 7, 1, 9]',
  """for a, b in combinations(zahlen, 2):
    if a + b == 10:
        print(a, b)""")
t("Ein Eisbecher hat 2 Kugeln, die Sorten dürfen sich wiederholen und die Reihenfolge spielt keine Rolle. Gib mit `combinations_with_replacement()` alle möglichen Becher aus.",
  "from itertools import combinations_with_replacement\nsorten = ['Vanille', 'Schoko', 'Erdbeere']",
  """for a, b in combinations_with_replacement(sorten, 2):
    print(a, b)""")
t('Gib alle Teilmengen von `menge` aus, also alle Auswahlen mit 0, 1, 2 und 3 Elementen. Verwende `combinations()` in einer Schleife über `r`.',
  "from itertools import combinations\nmenge = ['a', 'b', 'c']",
  """for r in range(len(menge) + 1):
    for teil in combinations(menge, r):
        print(teil)""")
t('Zähle mit `product()`, wie viele Ziffernfolgen von `000` bis `999` die Quersumme 10 haben. Gib die Anzahl aus.',
  'from itertools import product',
  """anzahl = 0
for a, b, c in product(range(10), repeat=3):
    if a + b + c == 10:
        anzahl += 1
print(anzahl)""")
predict("""from itertools import product, permutations, combinations, combinations_with_replacement
s = 'abc'
print(len(list(product(s, repeat=2))))
print(len(list(permutations(s, 2))))
print(len(list(combinations(s, 2))))
print(len(list(combinations_with_replacement(s, 2))))""")

# ---------------------------------------------------------------- 9
sec('batched()')
expl('''#### `batched()`

`batched(liste, n)` teilt eine Liste in **Gruppen von `n` Elementen** auf. Die letzte Gruppe kann kleiner sein.
Die Gruppen sind Tupel. `batched()` gibt es erst ab **Python 3.12**.''',
     """from itertools import batched

print(list(batched([1, 2, 3, 4, 5, 6, 7], 3)))
print(list(batched('abcdef', 2)))""")

t('Teile `zahlen` mit `batched()` in Dreiergruppen auf. Gib die Gruppen als Liste aus.',
  'from itertools import batched\nzahlen = list(range(1, 11))',
  "print(list(batched(zahlen, 3)))")
t('Teile die Schüler mit `batched()` in Zweierteams ein. Gib jedes Team in einer eigenen Zeile aus wie unten.',
  "from itertools import batched\nnamen = ['Ali', 'Bea', 'Cem', 'Dana', 'Eli', 'Finn']",
  """for nr, team in enumerate(batched(namen, 2), 1):
    print(f'Team {nr}: {team[0]} und {team[1]}')""")
t("Gib die IBAN in Vierergruppen getrennt durch Leerzeichen aus. Verwende `batched()` und `join()`.",
  "from itertools import batched\niban = 'DE89370400440532013000'",
  """gruppen = []
for g in batched(iban, 4):
    gruppen.append(''.join(g))
print(' '.join(gruppen))""")
t('Mache aus `zahlen` mit `batched()` ein Grid mit 4 Spalten. Die Zeilen sollen Listen sein. Gib das Grid zeilenweise aus.',
  'from itertools import batched\nzahlen = [5, 3, 8, 1, 2, 9, 4, 7, 6, 0, 3, 5]',
  """grid = [list(zeile) for zeile in batched(zahlen, 4)]
for zeile in grid:
    print(zeile)""")
predict("""from itertools import batched
b = list(batched(range(5), 2))
print(b)
print(len(b))
print(b[-1])""")

# ---------------------------------------------------------------- 10
sec('Gemischte Übungen')
t("Gib mit `product()` alle Ergebnisse von drei Münzwürfen aus (K = Kopf, Z = Zahl), jeweils als Zeichenkette. Gib danach aus, bei wie vielen genau zweimal Kopf vorkommt.",
  'from itertools import product',
  """anzahl = 0
for wurf in product('KZ', repeat=3):
    w = ''.join(wurf)
    print(w)
    if w.count('K') == 2:
        anzahl += 1
print(anzahl)""")
t('Auf einer Party geben sich alle gegenseitig die Hand. Gib für 2 bis 8 Personen aus, wie oft dabei Hände geschüttelt werden. Verwende `combinations()`.',
  'from itertools import combinations',
  """for n in range(2, 9):
    print(n, len(list(combinations(range(n), 2))))""")
t('Verteile die Aufgaben mit `cycle()` reihum an die Personen. Gib jede Aufgabe mit der zuständigen Person aus.',
  """from itertools import cycle
personen = ['Ali', 'Bea', 'Cem']
aufgaben = ['Tafel', 'Blumen', 'Müll', 'Fenster', 'Fegen']""",
  """for aufgabe, person in zip(aufgaben, cycle(personen)):
    print(f'{aufgabe}: {person}')""")
t('Gib mit `accumulate()` und `enumerate()` nach jedem Test den bisherigen Punktedurchschnitt aus, mit einer Nachkommastelle.',
  'from itertools import accumulate\npunkte = [12, 15, 9, 14]',
  """for i, summe in enumerate(accumulate(punkte), 1):
    print(f'{summe / i:.1f}')""")
t("Finde mit `permutations()` alle Wörter aus `woerter`, die aus genau den Buchstaben von `'tor'` bestehen. Gib sie sortiert aus.",
  "from itertools import permutations\nwoerter = {'tor', 'rot', 'ort', 'tier', 'rat', 'tod'}",
  """gefunden = []
for p in permutations('tor'):
    w = ''.join(p)
    if w in woerter:
        gefunden.append(w)
print(sorted(gefunden))""")
t('Gib mit `combinations()` alle Dreiergruppen von Zahlen aus `zahlen` aus, deren Summe 20 ist.',
  'from itertools import combinations\nzahlen = [3, 5, 7, 8, 10, 12]',
  """for gruppe in combinations(zahlen, 3):
    if sum(gruppe) == 20:
        print(gruppe)""")
t('Gib aus, wie viele verschiedene Wörter in allen Sätzen zusammen vorkommen. Verwende `chain.from_iterable()` und `set()`.',
  "from itertools import chain\nsaetze = ['der Hund bellt', 'die Katze schläft', 'der Hund schläft']",
  """woerter = chain.from_iterable([s.split() for s in saetze])
print(len(set(woerter)))""")
t('''Ein Zahlenschloss hat drei Ringe mit den Ziffern 0 bis 9. Du weißt: Die erste Ziffer ist gerade, die Summe aller Ziffern ist 15
und die letzte Ziffer ist größer als die mittlere. Gib mit `product()` alle möglichen Codes aus und danach ihre Anzahl.''',
  'from itertools import product',
  """anzahl = 0
for a, b, c in product(range(10), repeat=3):
    if a % 2 == 0 and a + b + c == 15 and c > b:
        print(f'{a}{b}{c}')
        anzahl += 1
print(anzahl)""")
t('Gib mit `pairwise()` und `max()` die größte Differenz zwischen zwei benachbarten Messwerten aus.',
  'from itertools import pairwise\nmesswerte = [12, 15, 11, 19, 18, 25, 22]',
  """diffs = []
for a, b in pairwise(messwerte):
    diffs.append(abs(b - a))
print(max(diffs))""")
predict("""from itertools import chain, cycle, islice, accumulate
a = list(islice(cycle('ab'), 5))
print(a)
print(list(accumulate(chain([1], [2, 3]))))
print(''.join(chain('xy', a[:2])))""")

generate('itertools', 'itertools')
