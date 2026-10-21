# Erzeugt ../content/schleifen.ipynb (siehe nbgen.py).
#
# Bewusst andere Aufgabenformen als in bedingungen/aufgabentex (Klausuraufgaben):
# kein "gib die Zahlen von a bis b aus" mit for/while, keine break/continue-Aufgabe über 1 bis 30,
# keine einfachen while-Herunterzähl-Vorhersagen.
# Auch nicht die Beispiele aus bedingungen/inhalte (Unterricht): kein Verdoppeln/Verdreifachen bis zu einer Grenze im Beispiel,
# kein Guthaben mit 5 % bis zur Verdopplung, keine Summe 1 bis 100 oder Summe der (un)geraden Zahlen, kein Countdown,
# kein continue bei i % 2 bzw. i % 3 == 0 mit anschließendem break.
# Kein Collatz (einfuehrung/inhalte), keine lineare Suche nach Minimum/Maximum (kommt später im Unterricht).
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
     """x = 2
while x < 50:
    print(x)
    x = x + 9
print('Ende:', x)""")

t('Gib mit einer `while`-Schleife die Quadratzahlen 1, 4, 9, 16, ... aus, solange sie kleiner als 100 sind. Verwende eine Variable `n`, die bei 1 beginnt.',
  body="""n = 1
while n * n < 100:
    print(n * n)
    n = n + 1""")
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
t('Berechne mit einer `while`-Schleife die Quersumme von `n`. Tipp: `n % 10` ist die letzte Ziffer, `n // 10` entfernt die letzte Ziffer.',
  'n = 4711',
  """summe = 0
while n > 0:
    summe = summe + n % 10
    n = n // 10
print(summe)""")
t('Ein Ball fällt aus 10 m Höhe und springt jedes Mal auf 60 % der vorherigen Höhe zurück. Wie oft springt er, bis er weniger als 1 m hoch springt? Gib die Anzahl aus.',
  body="""hoehe = 10
spruenge = 0
while hoehe >= 1:
    hoehe = hoehe * 0.6
    spruenge = spruenge + 1
print(spruenge)""")
predict("""x = 0
summe = 0
while summe < 20:
    x = x + 3
    summe = summe + x
print(x, summe)""", erklaerung='''| Durchlauf | `x` | `summe` |
|---|---|---|
| 1 | 3 | 3 |
| 2 | 6 | 9 |
| 3 | 9 | 18 |
| 4 | 12 | 30 |

Nach dem 4. Durchlauf ist `summe < 20` falsch. Ausgegeben werden die Werte nach diesem Durchlauf.''')

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
for i in range(20, 5, -4):
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
t('Gib die Quadratzahlen von 1 bis 100 in einer Zeile aus.',
  body="""for i in range(1, 11):
    print(i * i, end=' ')
print()""")
t('Gib die Neunerreihe aus wie unten.',
  body="""for i in range(1, 11):
    print(f'{i} x 9 = {i * 9}')""")
t('Gib mit `for` und `*` die Treppe unten aus.',
  body="""for i in range(1, 6):
    print('#' * i)""")
t('Gib eine Umrechnungstabelle von Grad Celsius in Grad Fahrenheit aus: von 0 bis 100 Grad in Zwanzigerschritten. Es gilt `f = c * 9 / 5 + 32`.',
  body="""for c in range(0, 101, 20):
    print(f'{c} Grad Celsius = {c * 9 / 5 + 32} Grad Fahrenheit')""")
predict("""for i in range(2, 9, 3):
    print(i * i, end=' ')
print()
for i in range(3, -4, -3):
    print(i, end=' ')
print()
for i in range(6, 2):
    print('X')
print('Ende')""", erklaerung='''- `range(2, 9, 3)` liefert 2, 5, 8 (die 11 wäre schon zu groß). Ausgegeben werden die Quadrate 4, 25, 64.
- `range(3, -4, -3)` zählt rückwärts: 3, 0, -3. Die -6 liegt schon jenseits von -4.
- `range(6, 2)` ist leer, weil der Start schon größer als das Ende ist und die Schrittweite 1 ist. `X` wird nie ausgegeben.''')
predict("""for k in range(4):
    x = k * 2
print(k, x)
summe = 0
for k in range(1, 4):
    summe = summe + k * k
print(summe)""", erklaerung='''- Nach der Schleife behält `k` den letzten Wert aus `range(4)`, also 3. Entsprechend ist `x` gleich `3 * 2 = 6`.
- `range(1, 4)` liefert 1, 2, 3. Die Summe der Quadrate ist `1 + 4 + 9 = 14`.''')

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
t('Berechne die Summe der Quadratzahlen `1*1 + 2*2 + ... + 10*10` und gib sie aus.',
  body="""summe = 0
for i in range(1, 11):
    summe += i * i
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
print(z)""", erklaerung='''- Für `i` = 1, 2, 3, 4 wird `s` zur Summe `1 + 2 + 3 + 4 = 10` und `p` zum Produkt `1 * 2 * 3 * 4 = 24`.
- Von 0 bis 19 haben die Zahlen 1, 5, 9, 13, 17 beim Teilen durch 4 den Rest 1. Das sind 5 Zahlen.''')

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
print(n)""", erklaerung='''- Jedes Zeichen von `'Code'` wird verdoppelt (`c * 2`) und angehängt: `CC`, `oo`, `dd`, `ee`.
- `'a b c'` hat 5 Zeichen, davon 2 Leerzeichen. Gezählt werden die anderen 3.''')

# ---------------------------------------------------------------- 5
sec('break, continue und while True')
expl('''#### `break` und `continue`

- `break` beendet die Schleife **sofort**. Das Programm macht nach der Schleife weiter.
- `continue` springt sofort zum **nächsten Durchlauf**. Der Rest des Blocks wird übersprungen.
- Eine Schleife `while True:` läuft endlos weiter und wird mit `break` beendet. Das ist praktisch, wenn man erst im Block weiß, wann Schluss ist.''',
     """for zahl in range(1, 20):
    if zahl % 5 == 0:
        continue
    if zahl * zahl > 50:
        break
    print(zahl, end=' ')
print()
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
predict("""wort = 'Banane'
for c in wort:
    if c == 'a':
        continue
    if c == 'e':
        break
    print(c, end='')
print()""", erklaerung='''Die Zeichen werden der Reihe nach geprüft:
`B` wird ausgegeben, `a` übersprungen (`continue`), `n` ausgegeben, `a` übersprungen, `n` ausgegeben.
Bei `e` beendet `break` die Schleife. Das `e` wird also nicht mehr ausgegeben.''')
predict("""n = 100
while True:
    n = n - 30
    if n < 0:
        break
    print(n)
print('Ende', n)""", erklaerung='''Bei jedem Durchlauf wird zuerst 30 abgezogen: 70, 40, 10 werden ausgegeben.
Danach ist `n` gleich -20. Jetzt ist `n < 0` wahr, `break` beendet die Schleife vor dem `print(n)`.
Nach der Schleife hat `n` noch den Wert -20.''')

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
print(z)""", erklaerung='''Die innere Schleife läuft `range(i)` durch, also bei `i = 0` gar nicht, bei `i = 1` einmal, bei `i = 2` zweimal.
Zusammen: `0 + 1 + 2 = 3`.''')
predict("""for i in range(1, 4):
    for j in range(1, 4):
        if j > i:
            break
        print(i * j, end=' ')
    print()""", erklaerung='''Die innere Schleife bricht ab, sobald `j > i` ist. In Zeile `i` laufen also nur `j = 1, ..., i`.
Ausgegeben wird jeweils `i * j`. Das `break` beendet nur die innere Schleife, `print()` am Ende der Zeile wird immer ausgeführt.''')

generate('schleifen', 'Schleifen')
