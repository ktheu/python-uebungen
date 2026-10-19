# Erzeugt ../content/funktionen.ipynb (siehe nbgen.py).
from nbgen import sec, expl, task, predict, generate

# ---------------------------------------------------------------- 1
sec('Funktionen definieren und aufrufen')
expl('''#### Was ist eine Funktion?

Eine **Funktion** ist ein Stück Code mit einem Namen. Man **definiert** sie einmal mit `def` und kann sie dann
beliebig oft **aufrufen**. So muss man Code nicht mehrfach schreiben.

- Die erste Zeile heißt **Kopf**: `def name():`. Danach folgt ein Doppelpunkt.
- Der eingerückte Code darunter ist der **Rumpf**. Er wird erst ausgeführt, wenn die Funktion aufgerufen wird.
- Aufgerufen wird die Funktion mit ihrem Namen und runden Klammern: `name()`.
- Eine Funktion muss **definiert** sein, bevor sie aufgerufen wird.''',
     """def begruessung():
    print('Hallo!')
    print('Schön, dass du da bist.')

begruessung()
begruessung()""")
expl('''#### `pass` und Docstrings

- Ein Rumpf darf nicht leer sein. Will man eine Funktion erst später ausfüllen, schreibt man `pass` hinein.
- Ein **Docstring** ist ein Text in drei Anführungszeichen direkt unter dem Kopf. Er beschreibt, was die Funktion macht.''',
     '''def spaeter():
    pass

def linie():
    """Gibt eine Linie aus 20 Minuszeichen aus."""
    print('-' * 20)

spaeter()
linie()''')

task("Schreibe eine Funktion `hallo()`, die `Hallo!` ausgibt. Rufe sie zweimal auf.",
     solution="""def hallo():
    print('Hallo!')

hallo()
hallo()""")
task("Schreibe eine Funktion `linie()`, die eine Linie aus 20 Minuszeichen ausgibt. Gib damit die Ausgabe unten aus: Linie, das Wort `Titel`, Linie.",
     solution="""def linie():
    print('-' * 20)

linie()
print('Titel')
linie()""")
task('Schreibe eine Funktion `dreieck()`, die das Dreieck unten ausgibt. Rufe sie auf.',
     solution="""def dreieck():
    print('*')
    print('**')
    print('***')

dreieck()""")
task('Schreibe eine Funktion `countdown()`, die mit einer Schleife die Zahlen 3, 2, 1 und danach `Los!` ausgibt. Rufe sie auf.',
     solution="""def countdown():
    for i in range(3, 0, -1):
        print(i)
    print('Los!')

countdown()""")
task("Schreibe eine Funktion `noch_leer()`, deren Rumpf nur `pass` enthält. Rufe sie auf und gib danach `fertig` aus.",
     solution="""def noch_leer():
    pass

noch_leer()
print('fertig')""")
task('Schreibe eine Funktion `stern_linie()`, die 10 Sterne ausgibt. Rufe sie in einer Schleife dreimal auf.',
     solution="""def stern_linie():
    print('*' * 10)

for i in range(3):
    stern_linie()""")
task('Schreibe eine Funktion `rahmen()`, die die Ausgabe unten erzeugt. Verwende darin die Funktion `linie()` aus Aufgabe 1.2.',
     solution="""def linie():
    print('-' * 20)

def rahmen():
    linie()
    print('|' + ' ' * 18 + '|')
    linie()

rahmen()""")
predict("""def a():
    print('A')

def b():
    print('B')
    a()

b()
a()""")
predict("""hallo()

def hallo():
    print('Hallo')""", error=NameError)

# ---------------------------------------------------------------- 2
sec('Parameter und Argumente')
expl('''#### Parameter

In den Klammern des Kopfs kann man **Parameter** angeben. Das sind Variablen, die beim Aufruf einen Wert bekommen.
Die Werte beim Aufruf heißen **Argumente**.

Bei mehreren Parametern werden die Argumente der Reihe nach zugeordnet: das erste Argument zum ersten Parameter usw.
Die Anzahl muss passen, sonst gibt es einen `TypeError`.''',
     """def begruesse(name):
    print(f'Hallo, {name}!')

def vorstellen(name, alter):
    print(f'{name} ist {alter} Jahre alt.')

begruesse('Ali')
begruesse('Bea')
vorstellen('Cem', 15)""")

task("Schreibe eine Funktion `begruesse(name)`, die `Hallo, ...!` mit dem Namen ausgibt. Rufe sie mit `'Ali'` und mit `'Bea'` auf.",
     solution="""def begruesse(name):
    print(f'Hallo, {name}!')

begruesse('Ali')
begruesse('Bea')""")
task('Schreibe eine Funktion `quadrat_ausgeben(n)`, die das Quadrat von `n` ausgibt. Rufe sie mit 3 und mit 7 auf.',
     solution="""def quadrat_ausgeben(n):
    print(n * n)

quadrat_ausgeben(3)
quadrat_ausgeben(7)""")
task('Schreibe eine Funktion `linie(n)`, die eine Linie aus `n` Minuszeichen ausgibt. Rufe sie mit 5 und mit 10 auf.',
     solution="""def linie(n):
    print('-' * n)

linie(5)
linie(10)""")
task("Schreibe eine Funktion `rechteck(breite, hoehe)`, die ein Rechteck aus `#` ausgibt. Rufe sie mit 5 und 3 auf.",
     solution="""def rechteck(breite, hoehe):
    for i in range(hoehe):
        print('#' * breite)

rechteck(5, 3)""")
task("Schreibe eine Funktion `vorstellen(name, alter)`, die den Satz unten ausgibt. Rufe sie mit `'Ali'` und `16` auf.",
     solution="""def vorstellen(name, alter):
    print(f'Ich heiße {name} und bin {alter} Jahre alt.')

vorstellen('Ali', 16)""")
task('Schreibe eine Funktion `reihe(n)`, die die ersten fünf Aufgaben der Einmaleins-Reihe von `n` ausgibt wie unten. Rufe sie mit 7 auf.',
     solution="""def reihe(n):
    for i in range(1, 6):
        print(f'{i} x {n} = {i * n}')

reihe(7)""")
task("Schreibe eine Funktion `wiederhole(text, anzahl)`, die `text` `anzahl`-mal ausgibt, jedes Mal in einer neuen Zeile. Rufe sie mit `'Hip hip hurra!'` und `3` auf.",
     solution="""def wiederhole(text, anzahl):
    for i in range(anzahl):
        print(text)

wiederhole('Hip hip hurra!', 3)""")
task("Schreibe eine Funktion `buchstabieren(wort)`, die jeden Buchstaben von `wort` in einer eigenen Zeile ausgibt. Rufe sie mit `'Code'` auf.",
     solution="""def buchstabieren(wort):
    for c in wort:
        print(c)

buchstabieren('Code')""")
predict("""def f(a, b):
    print(a - b)

f(5, 3)
f(3, 5)
x = 10
f(x, x // 2)""")
predict("""def f(a, b):
    print(a - b)

f(1)""", error=TypeError)

# ---------------------------------------------------------------- 3
sec('Rückgabewerte')
expl('''#### `return`

Mit `return wert` gibt eine Funktion einen **Wert zurück**. Den Rückgabewert kann man speichern, ausgeben
oder weiterrechnen. Bei `return` ist die Funktion sofort zu Ende. Code danach wird nicht mehr ausgeführt.

**Unterschied:** `print()` zeigt einen Wert nur auf dem Bildschirm an. Mit `return` bekommt das Programm den Wert
und kann damit weiterarbeiten. Hat eine Funktion kein `return`, gibt sie `None` zurück.''',
     """def quadrat(n):
    return n * n

ergebnis = quadrat(4)
print(ergebnis)
print(quadrat(3) + quadrat(4))
print(quadrat(quadrat(2)))""")
expl('''#### Mehrere `return`-Anweisungen

Eine Funktion kann mehrere `return`-Anweisungen haben, z. B. in verschiedenen Zweigen eines `if`.
Funktionen, die `True` oder `False` zurückgeben, kann man direkt in Bedingungen verwenden.''',
     """def ist_positiv(x):
    if x > 0:
        return True
    return False

print(ist_positiv(5))
if ist_positiv(-3):
    print('positiv')
else:
    print('nicht positiv')""")

task('Schreibe eine Funktion `quadrat(n)`, die das Quadrat von `n` zurückgibt. Gib damit `quadrat(4) + quadrat(3)` aus.',
     solution="""def quadrat(n):
    return n * n

print(quadrat(4) + quadrat(3))""")
task('Schreibe eine Funktion `summe(a, b)`, die die Summe zurückgibt. Speichere `summe(12, 30)` in einer Variablen und gib sie aus.',
     solution="""def summe(a, b):
    return a + b

s = summe(12, 30)
print(s)""")
task('Schreibe eine Funktion `kreisflaeche(r)`, die die Fläche eines Kreises mit Radius `r` zurückgibt. Verwende `3.14` für π. Gib die Fläche für `r = 10` aus.',
     solution="""def kreisflaeche(r):
    return 3.14 * r * r

print(kreisflaeche(10))""")
task('Schreibe eine Funktion `ist_gerade(n)`, die `True` zurückgibt, wenn `n` gerade ist, sonst `False`. Gib das Ergebnis für 4 und für 7 aus.',
     solution="""def ist_gerade(n):
    return n % 2 == 0

print(ist_gerade(4))
print(ist_gerade(7))""")
task('Schreibe eine Funktion `maximum(a, b)`, die die größere der beiden Zahlen zurückgibt. Verwende nicht `max()`. Gib `maximum(3, 8)` und `maximum(9, 2)` aus.',
     solution="""def maximum(a, b):
    if a > b:
        return a
    return b

print(maximum(3, 8))
print(maximum(9, 2))""")
task('Schreibe eine Funktion `maximum3(a, b, c)`, die die größte von drei Zahlen zurückgibt. Verwende darin die Funktion `maximum(a, b)` aus der vorigen Aufgabe. Gib `maximum3(4, 11, 7)` aus.',
     solution="""def maximum(a, b):
    if a > b:
        return a
    return b

def maximum3(a, b, c):
    return maximum(maximum(a, b), c)

print(maximum3(4, 11, 7))""")
task('Schreibe eine Funktion `betrag(x)`, die den Betrag von `x` zurückgibt. Verwende nicht `abs()`. Gib `betrag(-5)` und `betrag(3)` aus.',
     solution="""def betrag(x):
    if x < 0:
        return -x
    return x

print(betrag(-5))
print(betrag(3))""")
task('''Schreibe eine Funktion `note(punkte)`, die zu einer Punktzahl von 0 bis 100 die Note zurückgibt:
ab 90 die 1, ab 75 die 2, ab 60 die 3, ab 45 die 4, ab 20 die 5, sonst die 6. Gib die Noten für 95, 74, 45 und 10 aus.''',
     solution="""def note(punkte):
    if punkte >= 90:
        return 1
    if punkte >= 75:
        return 2
    if punkte >= 60:
        return 3
    if punkte >= 45:
        return 4
    if punkte >= 20:
        return 5
    return 6

print(note(95))
print(note(74))
print(note(45))
print(note(10))""")
task('Schreibe eine Funktion `fahrenheit(c)`, die eine Temperatur von Grad Celsius in Grad Fahrenheit umrechnet: `c * 9 / 5 + 32`. Gib die Werte für 0, 100 und 37 aus.',
     solution="""def fahrenheit(c):
    return c * 9 / 5 + 32

print(fahrenheit(0))
print(fahrenheit(100))
print(fahrenheit(37))""")
task('Schreibe eine Funktion `ist_teiler(a, b)`, die `True` zurückgibt, wenn `a` ein Teiler von `b` ist. Gib mit einer Schleife alle Teiler von 36 aus.',
     solution="""def ist_teiler(a, b):
    return b % a == 0

for i in range(1, 37):
    if ist_teiler(i, 36):
        print(i)""")
task("Schreibe eine Funktion `anzahl_vokale(text)`, die die Anzahl der Vokale (a, e, i, o, u) in `text` zurückgibt. Groß- und Kleinschreibung sollen keine Rolle spielen. Gib das Ergebnis für `'Informatik ist toll'` aus.",
     solution="""def anzahl_vokale(text):
    anzahl = 0
    for c in text.lower():
        if c in 'aeiou':
            anzahl += 1
    return anzahl

print(anzahl_vokale('Informatik ist toll'))""")
task('Schreibe eine Funktion `vorzeichen(x)`, die `positiv`, `negativ` oder `null` zurückgibt. Gib das Ergebnis für 5, -2 und 0 aus.',
     solution="""def vorzeichen(x):
    if x > 0:
        return 'positiv'
    if x < 0:
        return 'negativ'
    return 'null'

print(vorzeichen(5))
print(vorzeichen(-2))
print(vorzeichen(0))""")
predict("""def f(x):
    print(x * 2)

def g(x):
    return x * 2

a = f(3)
b = g(3)
print(a, b)""")
predict("""def h(n):
    return n + 1
    print('Ende')

x = h(h(1))
print(x)""")

# ---------------------------------------------------------------- 4
sec('Standardwerte und Schlüsselwort-Argumente')
expl('''#### Standardwerte

Ein Parameter kann einen **Standardwert** haben: `def f(a, b=2):`. Lässt man das Argument beim Aufruf weg,
wird der Standardwert verwendet. Parameter mit Standardwert müssen **hinter** den Parametern ohne Standardwert stehen.''',
     """def begruesse(name, gruss='Hallo'):
    print(f'{gruss}, {name}!')

begruesse('Ali')
begruesse('Bea', 'Guten Morgen')""")
expl('''#### Schlüsselwort-Argumente

Beim Aufruf kann man den Namen des Parameters angeben: `f(b=5, a=1)`. Dann ist die Reihenfolge egal.
So kann man auch einzelne Standardwerte überspringen.

Auch `print()` hat solche Parameter: `sep` legt fest, was zwischen den Werten steht (Standard: ein Leerzeichen),
`end`, was am Ende steht (Standard: eine neue Zeile).''',
     """def vorstellen(name, alter, ort='Berlin'):
    print(f'{name}, {alter}, {ort}')

vorstellen(alter=16, name='Ali')
vorstellen('Bea', 17, ort='Köln')
print('Mo', 'Di', 'Mi', sep=' | ')""")

task("Schreibe eine Funktion `begruesse(name, gruss='Hallo')`, die `gruss, name!` ausgibt. Rufe sie einmal nur mit `'Ali'` und einmal mit `'Bea'` und `'Moin'` auf.",
     solution="""def begruesse(name, gruss='Hallo'):
    print(f'{gruss}, {name}!')

begruesse('Ali')
begruesse('Bea', 'Moin')""")
task("Schreibe eine Funktion `linie(n=20, zeichen='-')`. Rufe sie auf: ohne Argumente, mit `5`, und mit `n=8, zeichen='='`.",
     solution="""def linie(n=20, zeichen='-'):
    print(zeichen * n)

linie()
linie(5)
linie(n=8, zeichen='=')""")
task('Schreibe eine Funktion `potenz(basis, exponent=2)`, die `basis ** exponent` zurückgibt. Gib `potenz(5)` und `potenz(2, 10)` aus.',
     solution="""def potenz(basis, exponent=2):
    return basis ** exponent

print(potenz(5))
print(potenz(2, 10))""")
task("Rufe die Funktion `vorstellen` mit Schlüsselwort-Argumenten auf, und zwar in der Reihenfolge `ort`, `alter`, `name`. Verwende Hamburg, 17 und Bea.",
     given="""def vorstellen(name, alter, ort):
    print(f'{name} ({alter}) aus {ort}')""",
     solution="""def vorstellen(name, alter, ort):
    print(f'{name} ({alter}) aus {ort}')

vorstellen(ort='Hamburg', alter=17, name='Bea')""")
task('Schreibe eine Funktion `mit_rabatt(preis, rabatt=10)`, die den Preis nach Abzug von `rabatt` Prozent zurückgibt. Gib die Preise für 50 Euro mit dem Standardrabatt und mit 25 Prozent Rabatt aus.',
     solution="""def mit_rabatt(preis, rabatt=10):
    return preis * (100 - rabatt) / 100

print(mit_rabatt(50))
print(mit_rabatt(50, 25))""")
task("Gib mit **einem** `print()` und dem Parameter `sep` die Ausgabe unten aus.",
     solution="""print('Mo', 'Di', 'Mi', 'Do', 'Fr', sep='-')""")
task("Gib mit einer Schleife und dem Parameter `end` die Zahlen von 1 bis 5 in einer Zeile aus, getrennt durch Kommas wie unten.",
     solution="""for i in range(1, 6):
    if i < 5:
        print(i, end=', ')
    else:
        print(i)""")
predict("""def f(a, b=2, c=3):
    return a + b * c

print(f(1))
print(f(1, 4))
print(f(1, c=10))
print(f(c=0, a=5))""")

# ---------------------------------------------------------------- 5
sec('Listen als Parameter')
expl('''#### Listen übergeben

Man kann einer Funktion auch eine Liste übergeben. Die Funktion arbeitet dann mit **derselben** Liste:
Ändert sie die Liste (z. B. mit `append()`), ist die Änderung auch außerhalb zu sehen.

Oft ist es besser, die übergebene Liste nicht zu ändern, sondern eine **neue** Liste zurückzugeben.''',
     """def summe(liste):
    s = 0
    for x in liste:
        s += x
    return s

def null_anhaengen(liste):
    liste.append(0)

zahlen = [3, 5, 2]
print(summe(zahlen))
null_anhaengen(zahlen)
print(zahlen)""")

task('Schreibe eine Funktion `summe(liste)`, die die Summe aller Zahlen zurückgibt. Verwende nicht `sum()`. Gib `summe([4, 8, 15, 16])` aus.',
     solution="""def summe(liste):
    s = 0
    for x in liste:
        s += x
    return s

print(summe([4, 8, 15, 16]))""")
task('Schreibe eine Funktion `durchschnitt(liste)`, die den Durchschnitt zurückgibt. Gib `durchschnitt([2, 3, 1, 2])` aus.',
     solution="""def durchschnitt(liste):
    return sum(liste) / len(liste)

print(durchschnitt([2, 3, 1, 2]))""")
task('Schreibe eine Funktion `groesstes(liste)`, die das größte Element zurückgibt. Verwende nicht `max()`. Gib `groesstes([7, 3, 19, 4])` aus.',
     solution="""def groesstes(liste):
    g = liste[0]
    for x in liste:
        if x > g:
            g = x
    return g

print(groesstes([7, 3, 19, 4]))""")
task('Schreibe eine Funktion `zaehle_groesser(liste, grenze)`, die zurückgibt, wie viele Elemente größer als `grenze` sind. Gib `zaehle_groesser([5, 12, 8, 3, 19], 7)` aus.',
     solution="""def zaehle_groesser(liste, grenze):
    anzahl = 0
    for x in liste:
        if x > grenze:
            anzahl += 1
    return anzahl

print(zaehle_groesser([5, 12, 8, 3, 19], 7))""")
task('Schreibe eine Funktion `nur_gerade(liste)`, die eine **neue** Liste mit allen geraden Zahlen zurückgibt. Gib das Ergebnis für `[3, 8, 12, 5, 6]` aus.',
     solution="""def nur_gerade(liste):
    ergebnis = []
    for x in liste:
        if x % 2 == 0:
            ergebnis.append(x)
    return ergebnis

print(nur_gerade([3, 8, 12, 5, 6]))""")
task('Schreibe eine Funktion `verdopple(liste)`, die jedes Element der übergebenen Liste verdoppelt und nichts zurückgibt. Rufe sie für `zahlen` auf und gib danach `zahlen` aus.',
     given='zahlen = [1, 2, 3]',
     solution="""zahlen = [1, 2, 3]

def verdopple(liste):
    for i in range(len(liste)):
        liste[i] = 2 * liste[i]

verdopple(zahlen)
print(zahlen)""")
task("Schreibe eine Funktion `enthaelt(liste, wert)`, die `True` zurückgibt, wenn `wert` in der Liste vorkommt. Verwende nicht `in` für die Liste, sondern eine Schleife. Gib das Ergebnis für `'Maus'` und für `'Esel'` in `['Hund', 'Katze', 'Maus']` aus.",
     solution="""def enthaelt(liste, wert):
    for x in liste:
        if x == wert:
            return True
    return False

tiere = ['Hund', 'Katze', 'Maus']
print(enthaelt(tiere, 'Maus'))
print(enthaelt(tiere, 'Esel'))""")
task('Schreibe eine Funktion `umgekehrt(liste)`, die eine neue Liste mit den Elementen in umgekehrter Reihenfolge zurückgibt. Die übergebene Liste soll unverändert bleiben. Gib beide Listen aus.',
     given='zahlen = [1, 2, 3, 4]',
     solution="""zahlen = [1, 2, 3, 4]

def umgekehrt(liste):
    neu = []
    for x in liste:
        neu.insert(0, x)
    return neu

print(umgekehrt(zahlen))
print(zahlen)""")
predict("""def anhaengen(liste):
    liste.append(0)

a = [1, 2]
anhaengen(a)
anhaengen(a)
print(a)""")
predict("""def neu(liste):
    liste = [9, 9]
    return liste

a = [1, 2]
b = neu(a)
print(a, b)""")

# ---------------------------------------------------------------- 6
sec('Lokale und globale Variablen')
expl('''#### Gültigkeitsbereich

- Variablen, die **in** einer Funktion entstehen, sind **lokal**: Es gibt sie nur in der Funktion, und nur während sie läuft.
  Das gilt auch für die Parameter.
- Variablen, die **außerhalb** aller Funktionen entstehen, sind **global**. Eine Funktion kann sie lesen.
- Weist man in einer Funktion einer Variablen einen Wert zu, entsteht eine neue lokale Variable, auch wenn es
  eine globale mit demselben Namen gibt.
- Mit `global name` am Anfang der Funktion kann man eine globale Variable ändern. Das macht Programme aber schwerer
  verständlich. Besser ist meist, den Wert mit `return` zurückzugeben.''',
     """x = 1

def f():
    x = 5
    print('in f:', x)

f()
print('außen:', x)

zaehler = 0

def erhoehe():
    global zaehler
    zaehler += 1

erhoehe()
print(zaehler)""")

predict("""def f():
    x = 5
    print(x)

x = 1
f()
print(x)""")
predict("""def f():
    y = 3

f()
print(y)""", error=NameError)
task('Schreibe eine Funktion `klick()`, die die globale Variable `anzahl` mit `global` um 1 erhöht. Rufe sie dreimal auf und gib danach `anzahl` aus.',
     given='anzahl = 0',
     solution="""anzahl = 0

def klick():
    global anzahl
    anzahl += 1

klick()
klick()
klick()
print(anzahl)""")
task('Löse die vorige Aufgabe ohne `global`: Die Funktion `klick(n)` gibt `n + 1` zurück, und das Ergebnis wird wieder in `anzahl` gespeichert.',
     given='anzahl = 0',
     solution="""anzahl = 0

def klick(n):
    return n + 1

anzahl = klick(anzahl)
anzahl = klick(anzahl)
anzahl = klick(anzahl)
print(anzahl)""")
task('Schreibe eine Funktion `mwst(preis)`, die den Preis plus Mehrwertsteuer zurückgibt. Der Steuersatz steht in der globalen Variablen `steuersatz` und wird nur gelesen. Gib `mwst(100)` aus.',
     given='steuersatz = 19',
     solution="""steuersatz = 19

def mwst(preis):
    return preis + preis * steuersatz / 100

print(mwst(100))""")
predict("""a = 10

def f(a):
    a = a + 1
    return a

print(f(a))
print(a)""")
predict("""z = 0

def erhoehe():
    global z
    z += 5

erhoehe()
erhoehe()
print(z)""")

# ---------------------------------------------------------------- 7
sec('Beliebig viele Argumente')
expl('''#### `*args`

Steht vor einem Parameter ein `*`, kann man beliebig viele Argumente übergeben.
In der Funktion ist der Parameter dann ein **Tupel** mit allen Argumenten. Meist nennt man ihn `args`.''',
     """def summe(*zahlen):
    s = 0
    for z in zahlen:
        s += z
    return s

print(summe(1, 2))
print(summe(1, 2, 3, 4))
print(summe())""")
expl('''#### `**kwargs`

Stehen vor einem Parameter zwei Sterne `**`, kann man beliebig viele **Schlüsselwort-Argumente** übergeben.
In der Funktion ist der Parameter dann ein **Dictionary**. Meist nennt man ihn `kwargs`.''',
     """def zeige(**angaben):
    for k, v in angaben.items():
        print(k, '=', v)

zeige(name='Ali', alter=16)""")

task('Schreibe eine Funktion `summe(*zahlen)`, die die Summe beliebig vieler Zahlen zurückgibt. Gib `summe(1, 2)`, `summe(1, 2, 3, 4)` und `summe()` aus.',
     solution="""def summe(*zahlen):
    s = 0
    for z in zahlen:
        s += z
    return s

print(summe(1, 2))
print(summe(1, 2, 3, 4))
print(summe())""")
task('Schreibe eine Funktion `groesste(*zahlen)`, die die größte von beliebig vielen Zahlen zurückgibt. Verwende nicht `max()`. Gib `groesste(4, 9, 2)` und `groesste(7)` aus.',
     solution="""def groesste(*zahlen):
    g = zahlen[0]
    for z in zahlen:
        if z > g:
            g = z
    return g

print(groesste(4, 9, 2))
print(groesste(7))""")
task('Schreibe eine Funktion `durchschnitt(*werte)`, die den Durchschnitt zurückgibt. Gib `durchschnitt(2, 4, 9)` aus.',
     solution="""def durchschnitt(*werte):
    return sum(werte) / len(werte)

print(durchschnitt(2, 4, 9))""")
task("Schreibe eine Funktion `einkauf(*artikel)`, die die Artikel nummeriert ausgibt wie unten. Rufe sie mit `'Milch'`, `'Brot'` und `'Eier'` auf.",
     solution="""def einkauf(*artikel):
    for i in range(len(artikel)):
        print(f'{i + 1}. {artikel[i]}')

einkauf('Milch', 'Brot', 'Eier')""")
task("Schreibe eine Funktion `steckbrief(**angaben)`, die jede Angabe in der Form `schluessel: wert` ausgibt. Rufe sie mit `name='Bea'`, `alter=17` und `hobby='Schach'` auf.",
     solution="""def steckbrief(**angaben):
    for k, v in angaben.items():
        print(f'{k}: {v}')

steckbrief(name='Bea', alter=17, hobby='Schach')""")
predict("""def f(*a):
    return len(a)

def g(**k):
    return list(k)

print(f(1, 2, 3))
print(f())
print(g(x=1, y=2))""")

# ---------------------------------------------------------------- 8
sec('Funktionen kombinieren und Rekursion')
expl('''#### Funktionen rufen Funktionen auf

Eine Funktion kann andere Funktionen aufrufen. So zerlegt man ein großes Problem in kleine, gut prüfbare Teile.''',
     """def ist_gerade(n):
    return n % 2 == 0

def gerade_bis(n):
    ergebnis = []
    for i in range(1, n + 1):
        if ist_gerade(i):
            ergebnis.append(i)
    return ergebnis

print(gerade_bis(10))""")
expl('''#### Rekursion

Eine Funktion kann sich auch **selbst** aufrufen. Das nennt man **Rekursion**. Wichtig ist eine **Abbruchbedingung**,
bei der sich die Funktion nicht mehr selbst aufruft. Sonst läuft sie endlos weiter (bis Python mit einem Fehler abbricht).''',
     """def countdown(n):
    if n == 0:
        print('Los!')
        return
    print(n)
    countdown(n - 1)

countdown(3)""")

task('''Schreibe eine Funktion `ist_prim(n)`, die `True` zurückgibt, wenn `n` eine Primzahl ist. Schreibe dann eine Funktion
`primzahlen_bis(n)`, die mit `ist_prim()` eine Liste aller Primzahlen bis `n` zurückgibt. Gib `primzahlen_bis(30)` aus.''',
     solution="""def ist_prim(n):
    if n < 2:
        return False
    for t in range(2, n):
        if n % t == 0:
            return False
    return True

def primzahlen_bis(n):
    ergebnis = []
    for i in range(2, n + 1):
        if ist_prim(i):
            ergebnis.append(i)
    return ergebnis

print(primzahlen_bis(30))""")
task('Schreibe eine Funktion `fakultaet(n)`, die `1 * 2 * ... * n` mit einer Schleife berechnet und zurückgibt. Gib `fakultaet(5)` und `fakultaet(10)` aus.',
     solution="""def fakultaet(n):
    ergebnis = 1
    for i in range(1, n + 1):
        ergebnis *= i
    return ergebnis

print(fakultaet(5))
print(fakultaet(10))""")
task('Schreibe die Funktion `fakultaet(n)` rekursiv: `fakultaet(0)` ist 1, sonst ist `fakultaet(n) = n * fakultaet(n - 1)`. Gib `fakultaet(5)` aus.',
     solution="""def fakultaet(n):
    if n == 0:
        return 1
    return n * fakultaet(n - 1)

print(fakultaet(5))""")
task('Schreibe eine rekursive Funktion `summe_bis(n)`, die `1 + 2 + ... + n` zurückgibt. Gib `summe_bis(100)` aus.',
     solution="""def summe_bis(n):
    if n == 0:
        return 0
    return n + summe_bis(n - 1)

print(summe_bis(100))""")
task('Schreibe eine rekursive Funktion `potenz(b, e)`, die `b` hoch `e` berechnet. Es gilt: `b` hoch 0 ist 1. Gib `potenz(2, 8)` aus.',
     solution="""def potenz(b, e):
    if e == 0:
        return 1
    return b * potenz(b, e - 1)

print(potenz(2, 8))""")
task('Schreibe eine rekursive Funktion `fib(n)` für die Fibonacci-Zahlen: `fib(1)` und `fib(2)` sind 1, sonst ist `fib(n) = fib(n - 1) + fib(n - 2)`. Gib `fib(10)` aus.',
     solution="""def fib(n):
    if n <= 2:
        return 1
    return fib(n - 1) + fib(n - 2)

print(fib(10))""")
task('Schreibe eine Funktion `quersumme(n)`, die die Quersumme einer Zahl zurückgibt. Verwende `% 10` und `// 10` in einer Schleife. Gib `quersumme(4711)` aus.',
     solution="""def quersumme(n):
    s = 0
    while n > 0:
        s += n % 10
        n = n // 10
    return s

print(quersumme(4711))""")
task('Schreibe eine rekursive Funktion `umdrehen(text)`, die einen Text umgedreht zurückgibt. Tipp: Ein leerer Text bleibt leer, sonst ist das Ergebnis `umdrehen(text[1:]) + text[0]`. Gib `umdrehen(\'Python\')` aus.',
     solution="""def umdrehen(text):
    if text == '':
        return ''
    return umdrehen(text[1:]) + text[0]

print(umdrehen('Python'))""")
predict("""def f(n):
    if n == 0:
        return 0
    return n + f(n - 1)

print(f(4))""")
predict("""def g(n):
    if n <= 1:
        return 1
    return 2 * g(n - 1)

print(g(5))""")

# ---------------------------------------------------------------- 9
sec('Gemischte Übungen')
task("Schreibe eine Funktion `ist_palindrom(wort)`, die `True` zurückgibt, wenn das Wort vorwärts und rückwärts gleich ist. Groß- und Kleinschreibung sollen keine Rolle spielen. Gib das Ergebnis für `'Rentner'` und `'Python'` aus.",
     solution="""def ist_palindrom(wort):
    w = wort.lower()
    rueckwaerts = ''
    for c in w:
        rueckwaerts = c + rueckwaerts
    return w == rueckwaerts

print(ist_palindrom('Rentner'))
print(ist_palindrom('Python'))""")
task('Schreibe eine Funktion `ggt(a, b)`, die den größten gemeinsamen Teiler mit dem Algorithmus von Euklid berechnet: Solange `b` nicht 0 ist, ersetze `a, b` durch `b, a % b`. Dann ist `a` der ggT. Gib `ggt(48, 18)` und `ggt(17, 5)` aus.',
     solution="""def ggt(a, b):
    while b != 0:
        a, b = b, a % b
    return a

print(ggt(48, 18))
print(ggt(17, 5))""")
task('Schreibe eine Funktion `bmi(gewicht, groesse)`, die den Body-Mass-Index `gewicht / groesse ** 2` zurückgibt (Gewicht in kg, Größe in m). Gib den BMI für 70 kg und 1.75 m mit einer Nachkommastelle aus.',
     solution="""def bmi(gewicht, groesse):
    return gewicht / groesse ** 2

print(f'{bmi(70, 1.75):.1f}')""")
task("Schreibe eine Funktion `passwort_ok(pw)`, die `True` zurückgibt, wenn das Passwort mindestens 8 Zeichen hat und mindestens eine Ziffer enthält. Gib das Ergebnis für `'geheim'`, `'geheim123'` und `'geheimnis'` aus.",
     solution="""def passwort_ok(pw):
    if len(pw) < 8:
        return False
    for c in pw:
        if c.isdigit():
            return True
    return False

print(passwort_ok('geheim'))
print(passwort_ok('geheim123'))
print(passwort_ok('geheimnis'))""")
task('''Schreibe eine Funktion `schaltjahr(jahr)`. Ein Jahr ist ein Schaltjahr, wenn es durch 4 teilbar ist, aber nicht durch 100,
außer es ist durch 400 teilbar. Gib das Ergebnis für 2024, 1900, 2000 und 2026 aus.''',
     solution="""def schaltjahr(jahr):
    if jahr % 400 == 0:
        return True
    if jahr % 100 == 0:
        return False
    return jahr % 4 == 0

print(schaltjahr(2024))
print(schaltjahr(1900))
print(schaltjahr(2000))
print(schaltjahr(2026))""")
task('Schreibe eine Funktion `tage_im_monat(monat, jahr)`, die die Anzahl der Tage zurückgibt. Verwende für den Februar die Funktion `schaltjahr()` aus der vorigen Aufgabe. Gib die Tage für Februar 2024, Februar 2026 und April 2026 aus.',
     solution="""def schaltjahr(jahr):
    if jahr % 400 == 0:
        return True
    if jahr % 100 == 0:
        return False
    return jahr % 4 == 0

def tage_im_monat(monat, jahr):
    if monat == 2:
        if schaltjahr(jahr):
            return 29
        return 28
    if monat in [4, 6, 9, 11]:
        return 30
    return 31

print(tage_im_monat(2, 2024))
print(tage_im_monat(2, 2026))
print(tage_im_monat(4, 2026))""")
task("Schreibe eine Funktion `initialen(name)`, die die Anfangsbuchstaben aller Teile eines Namens mit Punkt zurückgibt, z. B. `M. P. M.`. Gib `initialen('Max Peter Mustermann')` aus.",
     solution="""def initialen(name):
    teile = []
    for t in name.split():
        teile.append(t[0] + '.')
    return ' '.join(teile)

print(initialen('Max Peter Mustermann'))""")
task('Schreibe eine Funktion `statistik(noten)`, die die beste Note, die schlechteste Note und den Durchschnitt als Tupel zurückgibt. Entpacke das Ergebnis für `[2, 3, 1, 4, 2]` und gib die drei Werte aus.',
     solution="""def statistik(noten):
    return min(noten), max(noten), sum(noten) / len(noten)

beste, schlechteste, schnitt = statistik([2, 3, 1, 4, 2])
print(beste)
print(schlechteste)
print(schnitt)""")
task('Schreibe eine Funktion `wortanzahl(text)`, die ein Dictionary zurückgibt, das jedem Wort (in Kleinbuchstaben) zuordnet, wie oft es vorkommt. Gib das Ergebnis für den Text unten aus.\n\n`Die Katze und die Maus und der Hund`',
     solution="""def wortanzahl(text):
    d = {}
    for w in text.lower().split():
        d[w] = d.get(w, 0) + 1
    return d

print(wortanzahl('Die Katze und die Maus und der Hund'))""")
task('Schreibe eine Funktion `binaer(n)`, die die Binärdarstellung einer Zahl als Zeichenkette zurückgibt. Teile dazu wiederholt durch 2 und setze die Reste von hinten nach vorne zusammen. Gib `binaer(13)` und `binaer(100)` aus.',
     solution="""def binaer(n):
    if n == 0:
        return '0'
    text = ''
    while n > 0:
        text = str(n % 2) + text
        n = n // 2
    return text

print(binaer(13))
print(binaer(100))""")
task("Schreibe eine Funktion `zensieren(text, wort)`, die jedes Vorkommen von `wort` in `text` durch genauso viele Sternchen ersetzt. Gib das Ergebnis für den Text `'Das ist doof, echt doof.'` und das Wort `'doof'` aus.",
     solution="""def zensieren(text, wort):
    return text.replace(wort, '*' * len(wort))

print(zensieren('Das ist doof, echt doof.', 'doof'))""")
predict("""def a(x):
    return x + 1

def b(x):
    return a(x) * 2

def c(x, y=1):
    return b(x) - a(y)

print(a(1), b(1), c(1))
print(c(y=3, x=2))""")

generate('funktionen', 'Funktionen')
