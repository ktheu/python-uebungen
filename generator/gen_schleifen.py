# Erzeugt ../content/schleifen.ipynb (siehe nbgen.py).
#
# Bewusst andere Aufgabenformen als in bedingungen/aufgabentex (Klausuraufgaben):
# kein "gib die Zahlen von a bis b aus" mit for/while, keine break/continue-Aufgabe über 1 bis 30,
# keine einfachen while-Herunterzähl-Vorhersagen.
from nbgen import sec, expl, task, predict, generate


def t(text, given='', body='', kind='normal'):
    """Aufgabe, deren Lösung aus dem vorgegebenen Code plus body besteht."""
    task(text, given=given, solution=(given + '\n' + body) if given else body, kind=kind)


# ---------------------------------------------------------------- 1
sec('while-Schleifen')
expl('''#### Die `while`-Schleife

Eine `while`-Schleife wiederholt ihren Block, **solange** die Bedingung wahr ist.

- Vor jedem Durchlauf wird die Bedingung neu geprüft. Ist sie falsch, geht es nach der Schleife weiter.
- Im Block muss sich etwas ändern, das die Bedingung irgendwann falsch macht. Sonst läuft die Schleife **endlos**.
  (In Jupyter stoppt man eine endlose Schleife mit dem Stopp-Knopf ■.)''',
     """x = 1
while x < 100:
    print(x)
    x = x * 3
print('Ende:', x)""")

t('Gib mit einer `while`-Schleife die Zahlen 1, 2, 4, 8, ... aus, solange sie höchstens 128 sind. Jede Zahl ist doppelt so groß wie die vorige.',
  body="""x = 1
while x <= 128:
    print(x)
    x = x * 2""")
t('Gib mit einer `while`-Schleife einen Countdown von 5 bis 1 aus und danach `Abheben!`.',
  body="""n = 5
while n > 0:
    print(n)
    n = n - 1
print('Abheben!')""")
t('Lea spart jede Woche 7 Euro. Wie viele Wochen dauert es, bis sie mindestens 100 Euro hat? Gib die Anzahl der Wochen und den gesparten Betrag aus wie unten.',
  body="""betrag = 0
wochen = 0
while betrag < 100:
    betrag = betrag + 7
    wochen = wochen + 1
print('Wochen:', wochen)
print('Betrag:', betrag)""")
t('Halbiere `zahl` mit ganzzahliger Division `//` so lange, bis sie 1 ist. Gib jede Zahl aus, auch die 1.',
  'zahl = 1000',
  """print(zahl)
while zahl > 1:
    zahl = zahl // 2
    print(zahl)""")
t('1000 Euro werden mit 5 % pro Jahr verzinst. Nach wie vielen Jahren hat sich das Geld mindestens verdoppelt? Gib die Anzahl der Jahre aus.',
  body="""kapital = 1000
jahre = 0
while kapital < 2000:
    kapital = kapital * 1.05
    jahre = jahre + 1
print(jahre)""")
t('Berechne mit einer `while`-Schleife die Quersumme von `n`. Tipp: `n % 10` ist die letzte Ziffer, `n // 10` entfernt die letzte Ziffer.',
  'n = 4711',
  """summe = 0
while n > 0:
    summe = summe + n % 10
    n = n // 10
print(summe)""")
t('Zähle mit einer `while`-Schleife, wie viele Stellen `n` hat. Gib die Anzahl aus.',
  'n = 2026105',
  """stellen = 0
while n > 0:
    n = n // 10
    stellen = stellen + 1
print(stellen)""")
t('Ein Ball fällt aus 10 m Höhe und springt jedes Mal auf 60 % der vorherigen Höhe zurück. Wie oft springt er, bis er weniger als 1 m hoch springt? Gib die Anzahl aus.',
  body="""hoehe = 10
spruenge = 0
while hoehe >= 1:
    hoehe = hoehe * 0.6
    spruenge = spruenge + 1
print(spruenge)""")
predict("""n = 20
schritte = 0
while n != 1:
    if n % 2 == 0:
        n = n // 2
    else:
        n = 3 * n + 1
    schritte = schritte + 1
print(schritte)""")
predict("""x = 0
summe = 0
while summe < 20:
    x = x + 3
    summe = summe + x
print(x, summe)""")

# ---------------------------------------------------------------- 2
sec('for-Schleifen mit range()')
expl('''#### `for` und `range()`

Mit `for i in range(...):` wird der Block für jede Zahl aus dem Bereich einmal ausgeführt.
Die Variable `i` enthält dabei nacheinander die Zahlen.

- `range(stop)`: 0, 1, ..., `stop - 1`
- `range(start, stop)`: `start`, ..., `stop - 1`. Der Wert `stop` gehört **nicht** dazu.
- `range(start, stop, schritt)`: mit Schrittweite. Mit negativer Schrittweite zählt man rückwärts.''',
     """for i in range(3):
    print('Durchlauf', i)
for i in range(10, 0, -3):
    print(i)""")
expl('''#### Ausgabe in einer Zeile und Wiederholen von Text

- `print(wert, end=' ')` schreibt am Ende ein Leerzeichen statt einer neuen Zeile. So stehen mehrere Ausgaben in einer Zeile.
  Ein leeres `print()` beendet die Zeile.
- `text * n` wiederholt eine Zeichenkette `n`-mal, z. B. `'ab' * 3` ergibt `'ababab'`.''',
     """for i in range(1, 6):
    print(i, end=' ')
print()
print('-' * 20)""")

t('Gib die Vielfachen von 7 von 7 bis 70 in einer Zeile aus.',
  body="""for i in range(7, 71, 7):
    print(i, end=' ')
print()""")
t('Gib die Zahlen von 100 bis 0 rückwärts in Zehnerschritten in einer Zeile aus.',
  body="""for i in range(100, -1, -10):
    print(i, end=' ')
print()""")
t('Gib fünfmal `Hallo` mit einer laufenden Nummer aus wie unten.',
  body="""for i in range(1, 6):
    print('Hallo', i)""")
t('Gib die Quadratzahlen von 1 bis 100 in einer Zeile aus.',
  body="""for i in range(1, 11):
    print(i * i, end=' ')
print()""")
t('Gib die Neunerreihe aus wie unten.',
  body="""for i in range(1, 11):
    print(i, 'x 9 =', i * 9)""")
t('Gib mit `for` und `*` die Treppe unten aus.',
  body="""for i in range(1, 6):
    print('#' * i)""")
t('Gib die Treppe umgekehrt aus: oben 5 Rauten, unten eine.',
  body="""for i in range(5, 0, -1):
    print('#' * i)""")
t('Gib die Zahlen von -5 bis 5 in einer Zeile aus.',
  body="""for i in range(-5, 6):
    print(i, end=' ')
print()""")
t('Gib eine Umrechnungstabelle von Grad Celsius in Grad Fahrenheit aus: von 0 bis 100 Grad in Zwanzigerschritten. Es gilt `f = c * 9 / 5 + 32`.',
  body="""for c in range(0, 101, 20):
    print(c, 'Grad Celsius =', c * 9 / 5 + 32, 'Grad Fahrenheit')""")
predict("""for i in range(3, 12, 4):
    print(i, end=' ')
print()
for i in range(5, 0, -2):
    print(i, end=' ')
print()
for i in range(4, 4):
    print('X')
print('Ende')""")
predict("""for k in range(4):
    pass
print(k)
summe = 0
for k in range(1, 4):
    summe = summe + k * k
print(summe)""")

# ---------------------------------------------------------------- 3
sec('Summen, Zähler und Produkte')
expl('''#### Werte in einer Schleife sammeln

Ein häufiges Muster: Vor der Schleife setzt man eine Variable auf einen **Startwert**, in der Schleife wird sie verändert,
nach der Schleife gibt man sie aus.

- **Summe:** Startwert 0, in der Schleife `summe = summe + x` (kurz: `summe += x`)
- **Zähler:** Startwert 0, in der Schleife `anzahl += 1`, oft nur, wenn eine Bedingung erfüllt ist
- **Produkt:** Startwert 1, in der Schleife `produkt *= x`''',
     """summe = 0
anzahl = 0
for i in range(1, 11):
    summe += i
    if i % 3 == 0:
        anzahl += 1
print(summe)
print(anzahl)""")

t('Berechne die Summe der Zahlen von 1 bis 100 und gib sie aus.',
  body="""summe = 0
for i in range(1, 101):
    summe += i
print(summe)""")
t('Berechne die Summe aller geraden Zahlen von 2 bis 50 und gib sie aus.',
  body="""summe = 0
for i in range(2, 51, 2):
    summe += i
print(summe)""")
t('Berechne das Produkt `1 * 2 * 3 * ... * 10` und gib es aus.',
  body="""produkt = 1
for i in range(1, 11):
    produkt *= i
print(produkt)""")
t('Zähle, wie viele Zahlen von 1 bis 100 durch 3 **oder** durch 5 teilbar sind. Gib die Anzahl aus.',
  body="""anzahl = 0
for i in range(1, 101):
    if i % 3 == 0 or i % 5 == 0:
        anzahl += 1
print(anzahl)""")
t('Berechne die Summe `1/1 + 1/2 + 1/3 + ... + 1/10` und gib sie mit vier Nachkommastellen aus. Das geht mit der Formatangabe `{summe:.4f}` in einem f-String.',
  body="""summe = 0
for i in range(1, 11):
    summe += 1 / i
print(f'{summe:.4f}')""")
t('Berechne den Durchschnitt der Zahlen von 1 bis 20. Bestimme dazu in einer Schleife Summe und Anzahl.',
  body="""summe = 0
anzahl = 0
for i in range(1, 21):
    summe += i
    anzahl += 1
print(summe / anzahl)""")
t('Berechne die Summe der Quadratzahlen `1*1 + 2*2 + ... + 10*10` und gib sie aus.',
  body="""summe = 0
for i in range(1, 11):
    summe += i * i
print(summe)""")
t('Finde für `n` von 0 bis 20 den kleinsten Wert von `n * n - 10 * n`. Gib das `n` und den Wert aus.',
  body="""bestes_n = 0
kleinster = 0
for n in range(21):
    wert = n * n - 10 * n
    if wert < kleinster:
        kleinster = wert
        bestes_n = n
print(bestes_n, kleinster)""")
t('Gib die Zweierpotenzen von `2**0` bis `2**10` in einer Zeile aus und danach ihre Summe.',
  body="""summe = 0
for i in range(11):
    print(2 ** i, end=' ')
    summe += 2 ** i
print()
print(summe)""")
predict("""s = 0
p = 1
for i in range(1, 5):
    s += i
    p *= i
print(s, p)
z = 0
for i in range(20):
    if i % 4 == 1:
        z += 1
print(z)""")

# ---------------------------------------------------------------- 4
sec('Schleifen über Zeichenketten')
expl('''#### Zeichen für Zeichen

Mit `for zeichen in text:` durchläuft man eine Zeichenkette Zeichen für Zeichen.
So kann man Zeichen zählen oder eine neue Zeichenkette aufbauen: Man beginnt mit `''` und hängt mit `+=` an.

Braucht man auch die **Position**, hilft das: `len(text)` ist die Anzahl der Zeichen, und `text[i]` ist das Zeichen
an Position `i`. Die Zählung beginnt bei 0. Mit `for i in range(len(text)):` durchläuft man also alle Positionen.''',
     """for c in 'Hallo':
    print(c)
neu = ''
for c in 'abc':
    neu += c + c
print(neu)
wort = 'Eis'
for i in range(len(wort)):
    print(i, wort[i])""")

t('Gib die Buchstaben von `wort` in einer Zeile aus, getrennt durch Leerzeichen.',
  "wort = 'Python'",
  """for c in wort:
    print(c, end=' ')
print()""")
t("Zähle mit einer Schleife, wie oft `'a'` in `text` vorkommt. Gib die Anzahl aus.",
  "text = 'Anna fahrt mit dem Bananenboot'",
  """anzahl = 0
for c in text:
    if c == 'a':
        anzahl += 1
print(anzahl)""")
t("Zähle die Vokale (a, e, i, o, u) in `text`. Verwende `in 'aeiou'`.",
  "text = 'schleifen sind praktisch'",
  """anzahl = 0
for c in text:
    if c in 'aeiou':
        anzahl += 1
print(anzahl)""")
t('Baue mit einer Schleife das Wort rückwärts auf und gib es aus.',
  "wort = 'Regal'",
  """neu = ''
for c in wort:
    neu = c + neu
print(neu)""")
t("Baue mit einer Schleife eine neue Zeichenkette, in der jedes Leerzeichen durch `_` ersetzt ist. Gib sie aus.",
  "text = 'mein erstes Programm'",
  """neu = ''
for c in text:
    if c == ' ':
        neu += '_'
    else:
        neu += c
print(neu)""")
t("Zähle die Großbuchstaben in `text`. Ein Zeichen `c` ist ein Großbuchstabe, wenn `'A' <= c <= 'Z'` gilt (Umlaute brauchst du nicht zu beachten).",
  "text = 'Heute Lernen Wir Python'",
  """anzahl = 0
for c in text:
    if 'A' <= c <= 'Z':
        anzahl += 1
print(anzahl)""")
predict("""s = ''
for c in 'Code':
    s = s + c * 2
print(s)
n = 0
for c in 'a b c':
    if c != ' ':
        n += 1
print(n)""")

# ---------------------------------------------------------------- 5
sec('break, continue und while True')
expl('''#### `break` und `continue`

- `break` beendet die Schleife **sofort**. Das Programm macht nach der Schleife weiter.
- `continue` springt sofort zum **nächsten Durchlauf**. Der Rest des Blocks wird übersprungen.
- Eine Schleife `while True:` läuft endlos weiter und wird mit `break` beendet. Das ist praktisch, wenn man erst im Block weiß, wann Schluss ist.''',
     """for i in range(1, 10):
    if i == 3:
        continue
    if i == 6:
        break
    print(i)
n = 1
while True:
    n = n * 3
    if n > 50:
        break
print(n)""")

t('Finde mit `while True` und `break` die kleinste Zahl ab 1, deren Quadrat größer als 1000 ist. Gib sie aus.',
  body="""n = 1
while True:
    if n * n > 1000:
        break
    n += 1
print(n)""")
t('Finde mit einer `for`-Schleife und `break` den kleinsten Teiler von 391, der größer als 1 ist. Gib ihn aus.',
  body="""for t in range(2, 392):
    if 391 % t == 0:
        print(t)
        break""")
t("Gib alle Zeichen von `text` in einer Zeile aus, aber überspringe mit `continue` Leerzeichen und Kommas.",
  "text = 'Hallo, liebe Welt'",
  """for c in text:
    if c == ' ' or c == ',':
        continue
    print(c, end='')
print()""")
t("Finde die Position des ersten `'x'` in `text`. Verwende `range(len(text))` und `break`. Gibt es kein `'x'`, gib `nicht gefunden` aus. Tipp: Merke dir in einer Variablen, ob etwas gefunden wurde. Teste auch mit einem Text ohne `x`.",
  "text = 'Hexe und Axt'",
  """gefunden = False
for i in range(len(text)):
    if text[i] == 'x':
        print(i)
        gefunden = True
        break
if not gefunden:
    print('nicht gefunden')""")
t('Addiere die Zahlen 1, 2, 3, ... so lange, bis die Summe größer als 500 ist. Gib die zuletzt addierte Zahl und die Summe aus.',
  body="""summe = 0
n = 0
while summe <= 500:
    n += 1
    summe += n
print(n, summe)""")
t('Berechne mit `continue` die Summe aller Zahlen von 1 bis 50, die **nicht** durch 4 teilbar sind.',
  body="""summe = 0
for i in range(1, 51):
    if i % 4 == 0:
        continue
    summe += i
print(summe)""")
t('''Ein Würfelspiel ohne Zufall: Die Würfe stehen als Ziffern in `wuerfe`. Addiere die Augen, bis eine 1 kommt.
Dann ist das Spiel sofort vorbei und alle Punkte sind verloren. Gib die Punkte aus. `int(c)` wandelt eine Ziffer in eine Zahl um.
Teste auch mit `'4635'`.''',
  "wuerfe = '463156'",
  """punkte = 0
for c in wuerfe:
    w = int(c)
    if w == 1:
        punkte = 0
        break
    punkte += w
print(punkte)""")
predict("""for i in range(10):
    if i % 3 == 0:
        continue
    if i > 7:
        break
    print(i, end=' ')
print()""")
predict("""n = 100
while True:
    n = n - 30
    if n < 0:
        break
    print(n)
print('Ende', n)""")

# ---------------------------------------------------------------- 6
sec('Verschachtelte Schleifen')
expl('''#### Schleifen in Schleifen

Steht eine Schleife im Block einer anderen, läuft die **innere** Schleife bei **jedem** Durchlauf der äußeren komplett durch.
Bei 3 äußeren und 4 inneren Durchläufen wird der innere Block also 12-mal ausgeführt.
Ein `break` in der inneren Schleife beendet nur die innere Schleife.''',
     """for zeile in range(1, 4):
    for spalte in range(1, 5):
        print(zeile * spalte, end=' ')
    print()""")

t('Gib mit zwei verschachtelten Schleifen ein Rechteck aus 4 Zeilen und 6 Spalten aus Rauten `#` aus. Verwende nicht `*` zum Wiederholen.',
  body="""for z in range(4):
    for s in range(6):
        print('#', end='')
    print()""")
t('Gib das Zahlendreieck unten aus.',
  body="""for z in range(1, 6):
    for s in range(1, z + 1):
        print(s, end=' ')
    print()""")
t('Gib das kleine Einmaleins von 1 bis 9 als Tabelle aus. Jede Zahl soll 3 Zeichen breit sein (Formatangabe `{x:3}` in einem f-String).',
  body="""for z in range(1, 10):
    for s in range(1, 10):
        print(f'{z * s:3}', end='')
    print()""")
t('Gib alle Paare `a b` mit `1 <= a < b <= 4` aus.',
  body="""for a in range(1, 5):
    for b in range(a + 1, 5):
        print(a, b)""")
t('Ein pythagoreisches Tripel sind drei ganze Zahlen mit `a*a + b*b == c*c`. Gib alle Tripel mit `a < b < c <= 20` aus.',
  body="""for a in range(1, 21):
    for b in range(a + 1, 21):
        for c in range(b + 1, 21):
            if a * a + b * b == c * c:
                print(a, b, c)""")
t("Gib ein Schachbrett aus 8 mal 8 Feldern aus. Oben links steht `#`, danach wechseln sich `#` und `.` ab. Tipp: `(z + s) % 2`.",
  body="""for z in range(8):
    for s in range(8):
        if (z + s) % 2 == 0:
            print('#', end='')
        else:
            print('.', end='')
    print()""")
t('Zähle mit zwei verschachtelten Schleifen, bei wie vielen Würfen mit zwei Würfeln die Augensumme 8 ist.',
  body="""anzahl = 0
for a in range(1, 7):
    for b in range(1, 7):
        if a + b == 8:
            anzahl += 1
print(anzahl)""")
t('Gib alle Uhrzeiten von `00:00` bis `02:45` im Abstand von 15 Minuten aus. Die Formatangabe `{x:02d}` gibt eine Zahl zweistellig mit führender Null aus.',
  body="""for h in range(3):
    for m in range(0, 60, 15):
        print(f'{h:02d}:{m:02d}')""")
t('Gib den Tannenbaum unten aus. Jede Zeile beginnt mit Leerzeichen. Verwende `*` zum Wiederholen von Text.',
  body="""for i in range(1, 5):
    print(' ' * (4 - i) + '*' * (2 * i - 1))
print(' ' * 3 + '|')""")
predict("""z = 0
for i in range(3):
    for j in range(i):
        z += 1
print(z)""")
predict("""for i in range(1, 4):
    for j in range(1, 4):
        if j > i:
            break
        print(i * j, end=' ')
    print()""")

# ---------------------------------------------------------------- 7
sec('Rechnen mit Schleifen')
expl('''#### Kleine Algorithmen

Viele Rechenverfahren bestehen aus einer Schleife mit Bedingungen darin, z. B. das Suchen von Teilern,
das Prüfen auf Primzahlen oder das schrittweise Annähern an ein Ergebnis.

Praktisch dabei: Mit `a, b = b, a + b` bekommen **beide** Variablen gleichzeitig einen neuen Wert.
Rechts wird zuerst alles mit den **alten** Werten ausgerechnet, erst danach wird zugewiesen.''',
     """n = 12
for t in range(1, n + 1):
    if n % t == 0:
        print(t, end=' ')
print()
a = 1
b = 1
a, b = b, a + b
print(a, b)""")

t('Gib alle Teiler von 60 in einer Zeile aus.',
  body="""for t in range(1, 61):
    if 60 % t == 0:
        print(t, end=' ')
print()""")
t('Zähle, wie viele Teiler 360 hat. Gib die Anzahl aus.',
  body="""anzahl = 0
for t in range(1, 361):
    if 360 % t == 0:
        anzahl += 1
print(anzahl)""")
t("Prüfe, ob `n` eine Primzahl ist, also genau zwei Teiler hat (1 und sich selbst). Gib `Primzahl` oder `keine Primzahl` aus. Teste auch mit 91.",
  'n = 97',
  """teiler = 0
for t in range(1, n + 1):
    if n % t == 0:
        teiler += 1
if teiler == 2:
    print('Primzahl')
else:
    print('keine Primzahl')""")
t('Gib alle Primzahlen bis 50 in einer Zeile aus. Verwende zwei verschachtelte Schleifen.',
  body="""for n in range(2, 51):
    prim = True
    for t in range(2, n):
        if n % t == 0:
            prim = False
            break
    if prim:
        print(n, end=' ')
print()""")
t('Collatz-Folge: Ist `n` gerade, halbiere es, sonst rechne `3 * n + 1`. Wiederhole das, bis `n` gleich 1 ist. Gib alle Zahlen der Folge in einer Zeile aus, beginnend mit `n`.',
  'n = 6',
  """print(n, end=' ')
while n != 1:
    if n % 2 == 0:
        n = n // 2
    else:
        n = 3 * n + 1
    print(n, end=' ')
print()""")
t('Berechne den größten gemeinsamen Teiler von `a` und `b` mit dem Subtraktionsverfahren: Solange `a` und `b` verschieden sind, ziehe die kleinere Zahl von der größeren ab. Am Ende ist `a` der ggT.',
  'a = 48\nb = 18',
  """while a != b:
    if a > b:
        a = a - b
    else:
        b = b - a
print(a)""")
t('Gib alle Fibonacci-Zahlen kleiner als 100 in einer Zeile aus. Die Folge beginnt mit 1, 1, und jede weitere Zahl ist die Summe der beiden vorigen. Verwende `a, b = b, a + b`.',
  body="""a = 1
b = 1
while a < 100:
    print(a, end=' ')
    a, b = b, a + b
print()""")
t('Drehe die Ziffern von `n` um: aus 12345 wird 54321. Verwende `% 10` und `// 10` in einer Schleife.',
  'n = 12345',
  """umgedreht = 0
while n > 0:
    umgedreht = umgedreht * 10 + n % 10
    n = n // 10
print(umgedreht)""")
t('Eine Zahl heißt vollkommen, wenn sie gleich der Summe ihrer Teiler (ohne sich selbst) ist, z. B. 6 = 1 + 2 + 3. Gib alle vollkommenen Zahlen bis 1000 in einer Zeile aus.',
  body="""for n in range(2, 1001):
    summe = 0
    for t in range(1, n):
        if n % t == 0:
            summe += t
    if summe == n:
        print(n, end=' ')
print()""")
t('Heron-Verfahren für die Wurzel aus 2: Beginne mit `x = 2` und rechne sechsmal `x = (x + 2 / x) / 2`. Gib nach jedem Schritt `x` mit sechs Nachkommastellen aus (Formatangabe `{x:.6f}`).',
  body="""x = 2
for i in range(6):
    x = (x + 2 / x) / 2
    print(f'{x:.6f}')""")
predict("""n = 10
teiler = 0
for t in range(1, n + 1):
    if n % t == 0:
        teiler += t
print(teiler)
x = 1
for i in range(5):
    x = x * 2 + 1
print(x)""")

# ---------------------------------------------------------------- 8
sec('Gemischte Übungen')
t('FizzBuzz: Gib die Zahlen von 1 bis 15 aus. Statt Vielfachen von 3 gib `Fizz` aus, statt Vielfachen von 5 `Buzz` und statt Vielfachen von 15 `FizzBuzz`.',
  body="""for i in range(1, 16):
    if i % 15 == 0:
        print('FizzBuzz')
    elif i % 3 == 0:
        print('Fizz')
    elif i % 5 == 0:
        print('Buzz')
    else:
        print(i)""")
t('1000 Euro werden 5 Jahre lang mit 3 % pro Jahr verzinst. Gib für jedes Jahr den Kontostand mit zwei Nachkommastellen aus wie unten (Formatangabe `{kapital:.2f}`).',
  body="""kapital = 1000
for jahr in range(1, 6):
    kapital = kapital * 1.03
    print(f'Jahr {jahr}: {kapital:.2f} Euro')""")
t('Eine Bakterienkultur verdoppelt sich alle 20 Minuten. Am Anfang ist es eine Bakterie. Nach wie vielen Minuten sind es mehr als eine Million? Gib die Minuten aus.',
  body="""anzahl = 1
minuten = 0
while anzahl <= 1000000:
    anzahl = anzahl * 2
    minuten += 20
print(minuten)""")
t('Gib alle dreistelligen Zahlen von 100 bis 200 in einer Zeile aus, die vorwärts und rückwärts gelesen gleich sind. Tipp: Bei einer dreistelligen Zahl muss die erste Ziffer `n // 100` gleich der letzten `n % 10` sein.',
  body="""for n in range(100, 201):
    if n // 100 == n % 10:
        print(n, end=' ')
print()""")
t('Zähle, wie viele Zahlen von 1 bis 1000 die Ziffer 7 enthalten. Tipp: `str(n)` wandelt eine Zahl in eine Zeichenkette um, dann hilft `in`.',
  body="""anzahl = 0
for n in range(1, 1001):
    if '7' in str(n):
        anzahl += 1
print(anzahl)""")
t('Zerlege `n` in Primfaktoren. Teile `n` so lange durch den kleinsten möglichen Teiler, bis 1 übrig bleibt. Gib die Faktoren in einer Zeile aus.',
  'n = 360',
  """t = 2
while n > 1:
    if n % t == 0:
        print(t, end=' ')
        n = n // t
    else:
        t += 1
print()""")
t('Ein Kaninchenpaar bekommt ab dem zweiten Monat jeden Monat ein neues Paar, und jedes neue Paar macht es genauso (Fibonacci). Im ersten und zweiten Monat gibt es 1 Paar. In welchem Monat gibt es zum ersten Mal mehr als 1000 Paare? Gib den Monat und die Anzahl aus.',
  body="""a = 1
b = 1
monat = 2
while b <= 1000:
    a, b = b, a + b
    monat += 1
print(monat, b)""")
t('Gib eine Tabelle der Zahlen von 1 bis 5 mit ihrem Quadrat und ihrer Kubikzahl aus. Jede Spalte ist 5 Zeichen breit.',
  body="""for i in range(1, 6):
    print(f'{i:5}{i * i:5}{i * i * i:5}')""")
t('Gib eine Raute aus Sternen aus wie unten. Verwende zwei Schleifen: eine für die obere Hälfte und eine für die untere.',
  body="""for i in range(1, 4):
    print(' ' * (3 - i) + '*' * (2 * i - 1))
for i in range(2, 0, -1):
    print(' ' * (3 - i) + '*' * (2 * i - 1))""")
predict("""zahl = 0
for i in range(1, 4):
    for j in range(i, 4):
        zahl = zahl * 10 + j
print(zahl)""")

generate('schleifen', 'Schleifen')
