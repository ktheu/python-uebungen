# Erzeugt ../content/random.ipynb (siehe nbgen.py).
#
# Zufallsergebnisse ändern sich bei jedem Lauf. Aufgaben ohne random.seed() sind deshalb 'free'
# (ohne erwartete Ausgabe). Nur Aufgaben mit festem seed() zeigen eine erwartete Ausgabe.
from nbgen import sec, expl, task, predict, generate


def t(text, given='', body='', kind='free'):
    """Aufgabe, deren Lösung aus dem vorgegebenen Code plus body besteht. Standard: ohne erwartete Ausgabe."""
    task(text, given=given, solution=(given + '\n' + body) if given else body, kind=kind)


INTRO = '''Jeder Abschnitt beginnt mit kurzen Erklärungen und Beispielen. Führe die Beispiele aus und probiere sie ruhig ein wenig aus.
Danach folgen viele kleine Übungen. Wenn etwas vorgegeben ist, steht es schon in der Codezelle.

Weil Zufallszahlen bei jedem Lauf anders sind, steht bei den meisten Aufgaben **keine** erwartete Ausgabe.
Führe deine Lösung ruhig mehrmals aus. Nur bei Aufgaben mit `random.seed()` ist das Ergebnis immer gleich und deshalb angegeben.'''

# ---------------------------------------------------------------- 1
sec('Zufallszahlen erzeugen')
expl('''#### Das Modul `random`

Mit `import random` lädt man das Modul `random`. Seine Funktionen ruft man mit `random.name(...)` auf.

- `random.random()` liefert eine zufällige Kommazahl von 0 bis **ausschließlich** 1.
- `random.randint(a, b)` liefert eine zufällige ganze Zahl von `a` bis **einschließlich** `b`.
- `random.randrange(start, stop, schritt)` liefert eine zufällige Zahl aus `range(start, stop, schritt)`, also **ohne** `stop`.
- `random.uniform(a, b)` liefert eine zufällige Kommazahl zwischen `a` und `b`.

Bei jedem Ausführen kommen andere Zahlen heraus.''',
     """import random

print(random.random())
print(random.randint(1, 6))
print(random.randrange(0, 100, 10))
print(random.uniform(1.5, 2.5))""")

t('Gib drei Zufallszahlen von 0 bis 1 aus, jede in einer eigenen Zeile.',
  'import random',
  """for i in range(3):
    print(random.random())""")
t('Erzeuge mit einer List Comprehension eine Liste mit 10 Zufallszahlen von 10 bis 20 (einschließlich). Gib die Liste, die kleinste und die größte Zahl aus.',
  'import random',
  """zahlen = [random.randint(10, 20) for i in range(10)]
print(zahlen)
print(min(zahlen))
print(max(zahlen))""")
t('Gib mit `randrange()` eine zufällige **gerade** Zahl von 0 bis 100 aus.',
  'import random',
  "print(random.randrange(0, 101, 2))")
t('Gib mit `randrange()` eine zufällige Zahl aus 5, 10, 15, ..., 50 aus.',
  'import random',
  "print(random.randrange(5, 51, 5))")
t('Gib mit `uniform()` eine zufällige Temperatur zwischen -5 und 30 Grad mit einer Nachkommastelle aus wie `Heute: 17.3 Grad`.',
  'import random',
  """temp = random.uniform(-5, 30)
print(f'Heute: {temp:.1f} Grad')""")
t('Erzeuge mit `random()` eine zufällige Kommazahl von 0 bis 100 und gib sie mit zwei Nachkommastellen aus.',
  'import random',
  "print(f'{random.random() * 100:.2f}')")
t("Simuliere 10 Münzwürfe mit `random()`: Ist die Zahl kleiner als 0.5, ist es `Kopf`, sonst `Zahl`. Gib alle Ergebnisse in einer Zeile aus.",
  'import random',
  """for i in range(10):
    if random.random() < 0.5:
        print('Kopf', end=' ')
    else:
        print('Zahl', end=' ')
print()""")
t("Wähle mit `randint()` und einem Index einen zufälligen Buchstaben aus `alphabet` aus. Verwende nicht `choice()`.",
  "import random\nalphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'",
  "print(alphabet[random.randint(0, len(alphabet) - 1)])")
t("Ein Basketballspieler trifft mit einer Wahrscheinlichkeit von 30 %. Simuliere 10 Würfe: Gib für jeden Wurf `Treffer` oder `daneben` aus und am Ende die Anzahl der Treffer.",
  'import random',
  """treffer = 0
for i in range(10):
    if random.random() < 0.3:
        print('Treffer')
        treffer += 1
    else:
        print('daneben')
print(treffer)""")
t('Würfle mit `randint()` so lange, bis eine 6 kommt. Gib jeden Wurf aus und am Ende die Anzahl der Würfe.',
  'import random',
  """anzahl = 0
while True:
    wurf = random.randint(1, 6)
    anzahl += 1
    print(wurf)
    if wurf == 6:
        break
print('Würfe:', anzahl)""")
predict("""import random
x = random.randint(1, 6)
print(1 <= x <= 6)
y = random.random()
print(0 <= y < 1)
z = random.randrange(0, 10, 5)
print(z in [0, 5])""")
predict("""import random
print(random.randint(6, 1))""", error=ValueError)

# ---------------------------------------------------------------- 2
sec('Zufällig auswählen und mischen')
expl('''#### `choice()`, `choices()` und `sample()`

- `random.choice(liste)` wählt **ein** zufälliges Element aus.
- `random.choices(liste, k=n)` wählt `n` Elemente **mit Zurücklegen** aus. Ein Element kann also mehrfach vorkommen.
  Mit `weights=[...]` kann man jedem Element ein Gewicht geben: Elemente mit größerem Gewicht werden häufiger gewählt.
- `random.sample(liste, n)` wählt `n` **verschiedene** Elemente aus, also **ohne Zurücklegen**.

Statt einer Liste geht auch eine Zeichenkette oder ein `range()`.''',
     """import random

farben = ['rot', 'grün', 'blau']
print(random.choice(farben))
print(random.choices(farben, k=5))
print(random.choices(farben, weights=[8, 1, 1], k=5))
print(random.sample(range(1, 50), 6))""")
expl('''#### `shuffle()`

`random.shuffle(liste)` **mischt** die Liste. Die Liste selbst wird verändert, die Funktion gibt `None` zurück.
Zeichenketten und Tupel kann man nicht mischen. Man wandelt sie vorher mit `list()` in eine Liste um.''',
     """import random

karten = ['A', 'K', 'D', 'B', '10']
random.shuffle(karten)
print(karten)""")

t("Wähle mit `choice()` zufällig ein Essen aus und gib den Satz `Heute gibt es ...` aus.",
  "import random\nessen = ['Pizza', 'Nudeln', 'Suppe', 'Salat', 'Curry']",
  "print(f'Heute gibt es {random.choice(essen)}.')")
t('Gib mit `choice()` einen zufälligen Buchstaben aus `wort` aus.',
  "import random\nwort = 'Informatik'",
  "print(random.choice(wort))")
t('In der Lostrommel liegen die Lose unten. Ziehe mit `choices()` dreimal **mit Zurücklegen** und gib die gezogenen Lose aus.',
  "import random\nlose = ['Niete', 'Niete', 'Niete', 'Gewinn', 'Hauptgewinn']",
  "print(random.choices(lose, k=3))")
t('Ziehe mit `sample()` die Lottozahlen „6 aus 49“ und gib sie sortiert aus.',
  'import random',
  "print(sorted(random.sample(range(1, 50), 6)))")
t('Mische die Karten mit `shuffle()` und gib die ersten fünf Karten aus.',
  "import random\nkarten = ['7', '8', '9', '10', 'B', 'D', 'K', 'A']",
  """random.shuffle(karten)
print(karten[:5])""")
t('Ein gezinkter Würfel zeigt die 6 fünfmal so oft wie jede andere Zahl. Würfle mit `choices()` und `weights` 20-mal und gib die Würfe und die Anzahl der Sechsen aus.',
  'import random',
  """wuerfe = random.choices([1, 2, 3, 4, 5, 6], weights=[1, 1, 1, 1, 1, 5], k=20)
print(wuerfe)
print(wuerfe.count(6))""")
t('Wähle mit `sample()` zwei verschiedene Schüler für den Tafeldienst aus und gib sie aus.',
  "import random\nklasse = ['Ali', 'Bea', 'Cem', 'Dana', 'Eli', 'Finn', 'Gül', 'Hans']",
  """a, b = random.sample(klasse, 2)
print(f'Tafeldienst: {a} und {b}')""")
t('Teile die Klasse zufällig in zwei gleich große Teams. Mische dazu eine Kopie der Liste und teile sie mit Slicing. Gib beide Teams aus.',
  "import random\nklasse = ['Ali', 'Bea', 'Cem', 'Dana', 'Eli', 'Finn', 'Gül', 'Hans']",
  """gemischt = klasse.copy()
random.shuffle(gemischt)
mitte = len(gemischt) // 2
print(gemischt[:mitte])
print(gemischt[mitte:])""")
t('Lege für ein Referat eine zufällige Reihenfolge fest: Mische die Namen und gib sie nummeriert aus.',
  "import random\nnamen = ['Ali', 'Bea', 'Cem', 'Dana']",
  """random.shuffle(namen)
for i in range(len(namen)):
    print(f'{i + 1}. {namen[i]}')""")
t('Bilde fünf zufällige Sätze: Jeder Satz besteht aus einem zufälligen Subjekt, Verb und Objekt.',
  """import random
subjekte = ['Der Hund', 'Die Lehrerin', 'Mein Bruder', 'Ein Roboter']
verben = ['isst', 'sucht', 'malt', 'repariert']
objekte = ['einen Apfel', 'das Fahrrad', 'den Computer', 'ein Bild']""",
  """for i in range(5):
    print(random.choice(subjekte), random.choice(verben), random.choice(objekte) + '.')""")
t('Mische die Buchstaben von `wort` für ein Rätsel. Wandle das Wort dazu in eine Liste um und setze es danach mit `join()` wieder zusammen.',
  "import random\nwort = 'Schmetterling'",
  """buchstaben = list(wort)
random.shuffle(buchstaben)
print(''.join(buchstaben))""")
predict("""import random
a = [1, 2, 3, 4, 5]
b = random.sample(a, 3)
print(len(b))
print(len(set(b)))
random.shuffle(a)
print(sorted(a))
print(random.shuffle(a))""")
predict("""import random
print(random.sample([1, 2, 3], 5))""", error=ValueError)
predict("""import random
print(random.choice([]))""", error=IndexError)

# ---------------------------------------------------------------- 3
sec('Reproduzierbarer Zufall mit seed()')
expl('''#### `seed()`

Der Computer erzeugt Zufallszahlen mit einer Rechenvorschrift. Sie sehen zufällig aus, sind aber berechnet
(**Pseudozufallszahlen**). Mit `random.seed(zahl)` legt man den **Startwert** fest. Nach demselben `seed()`
kommen immer **dieselben** Zahlen in derselben Reihenfolge heraus.

Das ist nützlich zum Testen: Man kann ein Programm mit Zufall mehrmals laufen lassen und erhält jedes Mal dasselbe Ergebnis.
Damit dein Ergebnis zur erwarteten Ausgabe passt, musst du die Funktionen **genau wie beschrieben** und in derselben Reihenfolge aufrufen.''',
     """import random

random.seed(1)
print(random.randint(1, 100), random.randint(1, 100))
random.seed(1)
print(random.randint(1, 100), random.randint(1, 100))""")

t('Setze `random.seed(42)`. Erzeuge dann mit einer Schleife und `randint(1, 6)` eine Liste mit 5 Würfen und gib sie aus.',
  'import random',
  """random.seed(42)
wuerfe = []
for i in range(5):
    wuerfe.append(random.randint(1, 6))
print(wuerfe)""", kind='normal')
t('Setze `random.seed(7)`. Gib dann mit `random()` drei Zufallszahlen mit drei Nachkommastellen aus, jede in einer eigenen Zeile.',
  'import random',
  """random.seed(7)
for i in range(3):
    print(f'{random.random():.3f}')""", kind='normal')
t('Erzeuge zweimal eine Liste mit 5 Zahlen `randint(1, 100)`. Setze vor jeder Liste `random.seed(3)`. Gib aus, ob beide Listen gleich sind.',
  'import random',
  """random.seed(3)
a = [random.randint(1, 100) for i in range(5)]
random.seed(3)
b = [random.randint(1, 100) for i in range(5)]
print(a == b)""", kind='normal')
t('Setze `random.seed(1)` und mische die Liste `zahlen` mit `shuffle()`. Gib die Liste aus.',
  'import random\nzahlen = list(range(1, 11))',
  """random.seed(1)
random.shuffle(zahlen)
print(zahlen)""", kind='normal')
t('Setze `random.seed(2026)` und ziehe mit `sample()` die Lottozahlen „6 aus 49“ aus `range(1, 50)`. Gib sie sortiert aus.',
  'import random',
  """random.seed(2026)
print(sorted(random.sample(range(1, 50), 6)))""", kind='normal')
t('Setze `random.seed(5)` und gib in einer Schleife viermal `random.choice(farben)` aus, jede Farbe in einer eigenen Zeile.',
  "import random\nfarben = ['rot', 'grün', 'blau', 'gelb']",
  """random.seed(5)
for i in range(4):
    print(random.choice(farben))""", kind='normal')
t('Setze `random.seed(10)` und würfle mit `randint(1, 6)` so lange, bis eine 6 kommt. Gib die Anzahl der Würfe aus.',
  'import random',
  """random.seed(10)
anzahl = 0
while True:
    anzahl += 1
    if random.randint(1, 6) == 6:
        break
print(anzahl)""", kind='normal')
predict("""import random
random.seed(10)
a = random.random()
b = random.random()
random.seed(10)
c = random.random()
print(a == b)
print(a == c)""")

# ---------------------------------------------------------------- 4
sec('Zufällige Daten erzeugen')
expl('''#### Das Modul `string`

Das Modul `string` enthält fertige Zeichenketten, z. B.

- `string.ascii_lowercase`: alle Kleinbuchstaben `a` bis `z`
- `string.ascii_uppercase`: alle Großbuchstaben `A` bis `Z`
- `string.ascii_letters`: beides zusammen
- `string.digits`: alle Ziffern `0` bis `9`

Zusammen mit `random.choices()` und `join()` kann man damit zufällige Zeichenketten erzeugen.''',
     """import random
import string

print(string.digits)
print(''.join(random.choices(string.ascii_uppercase, k=5)))""")

t('Erzeuge ein zufälliges Passwort aus 10 Zeichen. Es darf Groß- und Kleinbuchstaben und Ziffern enthalten. Gib es aus.',
  'import random\nimport string',
  """zeichen = string.ascii_letters + string.digits
print(''.join(random.choices(zeichen, k=10)))""")
t('Erzeuge so lange zufällige Passwörter aus 8 Kleinbuchstaben und Ziffern, bis eines mindestens eine Ziffer enthält. Gib die Anzahl der Versuche und das Passwort aus.',
  'import random\nimport string',
  """versuche = 0
while True:
    versuche += 1
    pw = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
    hat_ziffer = False
    for c in pw:
        if c.isdigit():
            hat_ziffer = True
    if hat_ziffer:
        break
print(versuche)
print(pw)""")
t('Erzeuge ein zufälliges Berliner Autokennzeichen wie `B-XY 1234`: zwei zufällige Großbuchstaben und eine Zahl von 1 bis 9999.',
  'import random\nimport string',
  """buchstaben = ''.join(random.choices(string.ascii_uppercase, k=2))
zahl = random.randint(1, 9999)
print(f'B-{buchstaben} {zahl}')""")
t('Erzeuge eine Liste mit 20 Würfen. Gib danach mit `count()` für jede Augenzahl von 1 bis 6 aus, wie oft sie vorkommt.',
  'import random',
  """wuerfe = [random.randint(1, 6) for i in range(20)]
for augen in range(1, 7):
    print(augen, wuerfe.count(augen))""")
t("Erzeuge ein zufälliges Spielfeld mit 5 Zeilen und 8 Spalten. Jedes Feld ist mit einer Wahrscheinlichkeit von 30 % eine Wand `'#'`, sonst frei `'.'`. Gib das Feld zeilenweise aus.",
  'import random',
  """for z in range(5):
    zeile = ''
    for s in range(8):
        if random.random() < 0.3:
            zeile += '#'
        else:
            zeile += '.'
    print(zeile)""")
t('Erzeuge ein Dictionary, das jedem Schüler eine zufällige Note von 1 bis 6 zuordnet. Gib es aus und danach den Notendurchschnitt.',
  "import random\nnamen = ['Ali', 'Bea', 'Cem', 'Dana', 'Eli']",
  """noten = {}
for name in namen:
    noten[name] = random.randint(1, 6)
print(noten)
print(sum(noten.values()) / len(noten))""")
t('Erzeuge eine zufällige Farbe aus drei Werten von 0 bis 255 (rot, grün, blau). Gib sie als Tupel und als Hexadezimal-Farbcode wie `#1FA03C` aus. Die Formatangabe `:02X` gibt eine Zahl zweistellig hexadezimal aus.',
  'import random',
  """r = random.randint(0, 255)
g = random.randint(0, 255)
b = random.randint(0, 255)
print((r, g, b))
print(f'#{r:02X}{g:02X}{b:02X}')""")
t('Erzeuge ein zufälliges Datum im Jahr 2026 im Format `TT.MM.2026`. Der Einfachheit halber hat jeder Monat 28 Tage.',
  'import random',
  """tag = random.randint(1, 28)
monat = random.randint(1, 12)
print(f'{tag:02d}.{monat:02d}.2026')""")
t('Erzeuge eine Liste mit 10 verschiedenen Zufallszahlen von 1 bis 100 und gib sie aufsteigend sortiert aus.',
  'import random',
  "print(sorted(random.sample(range(1, 101), 10)))")
predict("""import random
import string
pw = ''.join(random.choices(string.digits, k=4))
print(len(pw))
print(pw.isdigit())
print(len(string.ascii_lowercase))""")

# ---------------------------------------------------------------- 5
sec('Simulationen')
expl('''#### Wahrscheinlichkeiten durch Ausprobieren

Wiederholt man ein Zufallsexperiment sehr oft, liegt die **relative Häufigkeit** eines Ergebnisses meist nahe an seiner
**Wahrscheinlichkeit**. Je mehr Wiederholungen, desto näher (Gesetz der großen Zahlen).
So kann man Wahrscheinlichkeiten mit dem Computer **schätzen**, auch wenn man sie nicht ausrechnen kann.''',
     """import random

n = 10000
sechsen = 0
for i in range(n):
    if random.randint(1, 6) == 6:
        sechsen += 1
print(f'Anteil der Sechsen: {sechsen / n * 100:.1f} %')""")

t('Würfle 6000-mal und zähle mit einer Liste oder einem Dictionary, wie oft jede Augenzahl vorkommt. Gib das Ergebnis aus. Jede Zahl sollte ungefähr 1000-mal vorkommen.',
  'import random',
  """anzahl = {}
for i in range(6000):
    w = random.randint(1, 6)
    anzahl[w] = anzahl.get(w, 0) + 1
for augen in range(1, 7):
    print(augen, anzahl[augen])""")
t('Gib den Anteil der Sechsen in Prozent für 100, 1000, 10000 und 100000 Würfe aus. Der richtige Wert ist etwa 16.7 %.',
  'import random',
  """for n in [100, 1000, 10000, 100000]:
    sechsen = 0
    for i in range(n):
        if random.randint(1, 6) == 6:
            sechsen += 1
    print(f'{n}: {sechsen / n * 100:.1f} %')""")
t('Würfle 10000-mal mit zwei Würfeln. Zähle, wie oft jede Augensumme von 2 bis 12 vorkommt, und gib für jede Summe einen Balken aus: ein `#` pro 100 Würfe.',
  'import random',
  """anzahl = {}
for i in range(10000):
    s = random.randint(1, 6) + random.randint(1, 6)
    anzahl[s] = anzahl.get(s, 0) + 1
for s in range(2, 13):
    print(f'{s:2} ' + '#' * (anzahl.get(s, 0) // 100))""")
t('Wie viele Würfe braucht man im Durchschnitt bis zur ersten 6? Simuliere das 10000-mal und gib den Durchschnitt aus. Er sollte ungefähr bei 6 liegen.',
  'import random',
  """gesamt = 0
for i in range(10000):
    anzahl = 1
    while random.randint(1, 6) != 6:
        anzahl += 1
    gesamt += anzahl
print(gesamt / 10000)""")
t("Wirf eine Münze 100-mal und finde die längste Serie gleicher Ergebnisse. Gib ihre Länge aus. Meist ist sie länger, als man denkt.",
  'import random',
  """laengste = 1
aktuell = 1
vorher = random.choice('KZ')
for i in range(99):
    wurf = random.choice('KZ')
    if wurf == vorher:
        aktuell += 1
    else:
        aktuell = 1
    if aktuell > laengste:
        laengste = aktuell
    vorher = wurf
print(laengste)""")
t('Wie groß ist die Wahrscheinlichkeit, mit drei Würfeln **mindestens eine** 6 zu würfeln? Simuliere 100000 Versuche und gib das Ergebnis in Prozent aus. Der richtige Wert ist etwa 42.1 %.',
  'import random',
  """n = 100000
treffer = 0
for i in range(n):
    wuerfe = [random.randint(1, 6) for j in range(3)]
    if 6 in wuerfe:
        treffer += 1
print(f'{treffer / n * 100:.1f} %')""")
t('''Geburtstagsproblem: In einer Klasse sind 23 Personen. Wie wahrscheinlich ist es, dass zwei am selben Tag Geburtstag haben?
Wähle für jede Person einen zufälligen Tag von 1 bis 365 und prüfe mit einem Set, ob ein Tag doppelt vorkommt.
Simuliere 10000 Klassen und gib das Ergebnis in Prozent aus. Es sollte ungefähr bei 50 % liegen.''',
  'import random',
  """n = 10000
treffer = 0
for i in range(n):
    tage = [random.randint(1, 365) for j in range(23)]
    if len(set(tage)) < 23:
        treffer += 1
print(f'{treffer / n * 100:.1f} %')""")
t('''Ziegenproblem: Hinter einer von drei Türen steht ein Auto. Du wählst eine Tür. Der Moderator öffnet eine andere Tür, hinter der kein Auto steht.
Dann darfst du wechseln. Simuliere 10000 Spiele und gib aus, wie oft man gewinnt, wenn man **bleibt**, und wie oft, wenn man **wechselt**.
Tipp: Wer wechselt, gewinnt genau dann, wenn die erste Wahl falsch war.''',
  'import random',
  """n = 10000
bleiben = 0
wechseln = 0
for i in range(n):
    auto = random.randint(1, 3)
    wahl = random.randint(1, 3)
    if wahl == auto:
        bleiben += 1
    else:
        wechseln += 1
print(f'bleiben: {bleiben / n * 100:.1f} %')
print(f'wechseln: {wechseln / n * 100:.1f} %')""")
t('Zufallsspaziergang: Eine Figur startet bei 0 und geht 100-mal zufällig einen Schritt nach links (-1) oder rechts (+1). Gib die Endposition und die größte Entfernung von 0 während des Spaziergangs aus.',
  'import random',
  """pos = 0
weiteste = 0
for i in range(100):
    pos += random.choice([-1, 1])
    if abs(pos) > weiteste:
        weiteste = abs(pos)
print(pos)
print(weiteste)""")
t('''Schätze die Zahl π: Wähle 100000 zufällige Punkte `(x, y)` mit `x` und `y` zwischen 0 und 1. Zähle, wie viele davon im Viertelkreis liegen,
also `x * x + y * y <= 1`. Dann ist π ungefähr `4 * anzahl / 100000`. Gib die Schätzung aus.''',
  'import random',
  """n = 100000
innen = 0
for i in range(n):
    x = random.random()
    y = random.random()
    if x * x + y * y <= 1:
        innen += 1
print(4 * innen / n)""")
t('Sammelbilder: Es gibt 10 verschiedene Bilder, in jeder Packung ist ein zufälliges. Wie viele Packungen muss man im Durchschnitt kaufen, bis man alle 10 hat? Simuliere 1000 Sammler und gib den Durchschnitt aus. Er sollte ungefähr bei 29 liegen.',
  'import random',
  """gesamt = 0
for i in range(1000):
    gesammelt = set()
    packungen = 0
    while len(gesammelt) < 10:
        gesammelt.add(random.randint(1, 10))
        packungen += 1
    gesamt += packungen
print(gesamt / 1000)""")

# ---------------------------------------------------------------- 6
sec('Spiele')
expl('''#### Zufall in Spielen

In Spielen sorgt der Zufall dafür, dass jede Runde anders verläuft. Oft kombiniert man dafür `randint()`,
`choice()` und `shuffle()` mit Schleifen, Bedingungen und Dictionaries.''',
     """import random

wuerfe = [random.randint(1, 6) for i in range(5)]
print(wuerfe)
if len(set(wuerfe)) == 1:
    print('Kniffel!')""")

t('''Schere, Stein, Papier: Zwei Computerspieler spielen 10 Runden. Jeder wählt zufällig. Gib in jeder Runde die beiden Wahlen und den Gewinner aus,
am Ende den Punktestand. Tipp: Ein Dictionary `schlaegt = {'Schere': 'Papier', ...}` sagt, was was schlägt.''',
  'import random',
  """schlaegt = {'Schere': 'Papier', 'Stein': 'Schere', 'Papier': 'Stein'}
optionen = list(schlaegt)
punkte_a = 0
punkte_b = 0
for runde in range(10):
    a = random.choice(optionen)
    b = random.choice(optionen)
    if schlaegt[a] == b:
        ergebnis = 'A gewinnt'
        punkte_a += 1
    elif schlaegt[b] == a:
        ergebnis = 'B gewinnt'
        punkte_b += 1
    else:
        ergebnis = 'unentschieden'
    print(a, b, ergebnis)
print(f'Stand: {punkte_a} zu {punkte_b}')""")
t('''Zahlenraten: Der Computer denkt sich eine Zahl von 1 bis 100. Ein zweites Programmteil rät mit der Halbierungsmethode:
Es rät immer die Mitte des noch möglichen Bereichs. Gib jeden Versuch mit `zu klein`, `zu groß` oder `richtig` aus und am Ende die Anzahl der Versuche.''',
  'import random',
  """geheim = random.randint(1, 100)
unten = 1
oben = 100
versuche = 0
while True:
    tipp = (unten + oben) // 2
    versuche += 1
    if tipp < geheim:
        print(tipp, 'zu klein')
        unten = tipp + 1
    elif tipp > geheim:
        print(tipp, 'zu groß')
        oben = tipp - 1
    else:
        print(tipp, 'richtig')
        break
print('Versuche:', versuche)""")
t('Kniffel: Wirf 5 Würfel. Bei einem Kniffel zeigen alle die gleiche Zahl. Simuliere 100000 Würfe und gib aus, wie viele Kniffel dabei waren. Erwartet werden etwa 77.',
  'import random',
  """kniffel = 0
for i in range(100000):
    wuerfe = [random.randint(1, 6) for j in range(5)]
    if len(set(wuerfe)) == 1:
        kniffel += 1
print(kniffel)""")
t('Erzeuge ein Kartenspiel aus allen Kombinationen von `farben` und `werte`, zum Beispiel `Herz 7`. Mische es und gib eine Hand aus 5 Karten aus.',
  """import random
farben = ['Kreuz', 'Pik', 'Herz', 'Karo']
werte = ['7', '8', '9', '10', 'B', 'D', 'K', 'A']""",
  """deck = []
for f in farben:
    for w in werte:
        deck.append(f'{f} {w}')
random.shuffle(deck)
print(deck[:5])""")
t('Glücksrad: Die Preise haben unterschiedliche Gewichte. Drehe das Rad 10-mal mit `choices()` und gib danach mit einem Dictionary aus, wie oft jeder Preis kam.',
  """import random
preise = ['Niete', 'Bonbon', 'Gutschein', 'Fahrrad']
gewichte = [60, 30, 9, 1]""",
  """ergebnis = random.choices(preise, weights=gewichte, k=10)
anzahl = {}
for p in ergebnis:
    anzahl[p] = anzahl.get(p, 0) + 1
print(anzahl)""")
t("Schatzsuche: Verstecke einen Schatz an einer zufälligen Position in einem Feld mit 5 Zeilen und 5 Spalten. Gib die Position und das Feld aus. Der Schatz ist `X`, alle anderen Felder sind `.`.",
  'import random',
  """z = random.randint(0, 4)
s = random.randint(0, 4)
print('Schatz bei', z, s)
for i in range(5):
    zeile = ''
    for j in range(5):
        if i == z and j == s:
            zeile += 'X'
        else:
            zeile += '.'
    print(zeile)""")
t('Stelle die Quizfragen in einer zufälligen Reihenfolge. Mische dazu die Liste der Fragen und gib jede Frage mit der richtigen Antwort aus.',
  """import random
quiz = {'Hauptstadt von Frankreich?': 'Paris', '3 * 7?': '21', 'Größter Planet?': 'Jupiter', 'Farbe von Chlorophyll?': 'grün'}""",
  """fragen = list(quiz)
random.shuffle(fragen)
for f in fragen:
    print(f, '->', quiz[f])""")
t('Würfelduell: Zwei Spieler würfeln je 10-mal. Wer die höhere Zahl hat, bekommt einen Punkt, bei Gleichstand niemand. Gib die Würfe jeder Runde und am Ende den Sieger aus.',
  'import random',
  """a_punkte = 0
b_punkte = 0
for runde in range(10):
    a = random.randint(1, 6)
    b = random.randint(1, 6)
    print(a, b)
    if a > b:
        a_punkte += 1
    elif b > a:
        b_punkte += 1
if a_punkte > b_punkte:
    print('Spieler A gewinnt')
elif b_punkte > a_punkte:
    print('Spieler B gewinnt')
else:
    print('Unentschieden')""")
predict("""import random
random.seed(0)
a = [random.randint(1, 6) for i in range(3)]
random.seed(0)
b = [random.randint(1, 6) for i in range(3)]
print(a == b)
print(len(set(random.sample(range(10), 10))))
print(sorted(random.sample('abc', 3)))""")

generate('random', 'Zufallszahlen mit random', INTRO)
