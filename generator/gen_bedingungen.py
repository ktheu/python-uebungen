# Erzeugt ../content/bedingungen.ipynb (siehe nbgen.py).
#
# Bewusst andere Aufgabenformen als in bedingungen/aufgabentex (Klausuraufgaben):
# kein input(), keine "Ausdruck, der genau dann wahr ist, wenn x ... und durch n teilbar"-Aufgaben,
# keine Wahrheitstafeln, keine positiv/null/negativ- oder bestanden/nicht-bestanden-Aufgaben.
# Auch nicht die Beispiele aus bedingungen/inhalte (Unterricht): kein volljaehrig = alter >= 18, kein gerade/ungerade
# bzw. durch-3-teilbar, keine Altersgrenzen mit 65, kein Wochenende/Werktag, keine and/or/not-Tabellen mit a, b, c.
from nbgen import sec, expl, task, predict, generate


def t(text, given='', body='', kind='normal'):
    """Aufgabe, deren Lösung aus dem vorgegebenen Code plus body besteht."""
    task(text, given=given, solution=(given + '\n' + body) if given else body, kind=kind)


# ---------------------------------------------------------------- 1
sec('Wahrheitswerte und Vergleiche')
expl('''#### `True` und `False`

Ein **Wahrheitswert** (Datentyp `bool`) ist entweder `True` (wahr) oder `False` (falsch).
Vergleiche liefern immer einen Wahrheitswert:

| Operator | Bedeutung |
|---|---|
| `==` | gleich |
| `!=` | ungleich |
| `<`, `>` | kleiner, größer |
| `<=`, `>=` | kleiner oder gleich, größer oder gleich |

Achtung: `=` ist eine **Zuweisung**, `==` ist ein **Vergleich**.''',
     """a = 7
b = 12
print(a < b)
print(a == b)
ergebnis = a != b
print(ergebnis)
print(type(ergebnis))""")
expl('''#### Vergleichsketten und Zeichenketten

- Mehrere Vergleiche kann man verketten: `0 <= x <= 10` bedeutet „x liegt zwischen 0 und 10 (einschließlich)“.
- Zeichenketten vergleicht man mit `==` und `!=`. Groß- und Kleinschreibung werden unterschieden.
- Mit `<` und `>` werden Zeichenketten **alphabetisch** verglichen. Dabei kommen alle Großbuchstaben vor allen Kleinbuchstaben.''',
     """x = 7
print(0 <= x <= 10)
print('Hallo' == 'hallo')
print('Apfel' < 'Birne')
print('Zebra' < 'apfel')""")

t('Gib für `a` und `b` die Ergebnisse von `a > b`, `a <= b` und `a != b` aus, jeweils in einer eigenen Zeile.',
  'a = 15\nb = 9',
  """print(a > b)
print(a <= b)
print(a != b)""")
t('Im Flugzeug sind 23 kg Gepäck frei. Speichere in der Variablen `passt`, ob `gewicht` höchstens 23 ist. Gib `passt` aus. Teste auch mit `gewicht = 23`.',
  'gewicht = 24.5',
  """passt = gewicht <= 23
print(passt)""")
t('Prüfe mit **einer** Vergleichskette, ob `temperatur` zwischen 18 und 24 Grad liegt (einschließlich). Gib das Ergebnis aus. Teste auch mit `25`.',
  'temperatur = 21',
  "print(18 <= temperatur <= 24)")
t('Gib aus, ob die Zahl `n` mit der Ziffer 0 endet. Verwende den Modulo-Operator `%`. Teste auch mit `n = 205`.',
  'n = 230',
  "print(n % 10 == 0)")
t('Gib aus, ob `name1` im Alphabet vor `name2` steht.',
  "name1 = 'Lena'\nname2 = 'Ben'",
  "print(name1 < name2)")
t('Gib aus, ob `a` und `b` dasselbe Vorzeichen haben. Tipp: Das Produkt zweier Zahlen mit demselben Vorzeichen ist positiv.',
  'a = -3\nb = -8',
  "print(a * b > 0)")
t('Gib aus, ob der Preis mit 19 % Mehrwertsteuer höchstens 20 Euro beträgt.',
  'netto = 16.5',
  "print(netto * 1.19 <= 20)")
predict("""a = 3
b = 3.0
print(a == b)
print('3' == 3)
print(10 > 9 > 8)
print('Zebra' < 'apfel')
print(type(a > b))""", erklaerung='''- `a == b` ist `True`: `3` und `3.0` haben denselben Wert, auch wenn die eine Zahl ganzzahlig ist und die andere eine Kommazahl.
- `'3' == 3` ist `False`: Eine Zeichenkette ist nie gleich einer Zahl.
- `10 > 9 > 8` ist eine Vergleichskette: `10 > 9` und `9 > 8` stimmen beide.
- `'Zebra' < 'apfel'` ist `True`: Alle Großbuchstaben kommen vor allen Kleinbuchstaben.
- `a > b` ist ein Vergleich (hier mit dem Wert `False`). Jeder Vergleich hat den Datentyp `bool`.''')
predict("""x = 5
if x = 5:
    print('fünf')""", error=SyntaxError, erklaerung='''In der Bedingung steht `=` (Zuweisung) statt `==` (Vergleich).
Das ist ein Syntaxfehler: Python führt dann **gar nichts** aus, auch nicht die erste Zeile. Richtig wäre `if x == 5:`.''')

# ---------------------------------------------------------------- 2
sec('if')
expl('''#### Die `if`-Anweisung

Mit `if` wird Code nur dann ausgeführt, wenn eine **Bedingung** wahr ist.

- Nach der Bedingung steht ein **Doppelpunkt**.
- Der Code, der zur Bedingung gehört, ist **eingerückt** (meist 4 Leerzeichen). Er heißt **Block**.
- Danach geht das Programm ganz normal weiter, egal ob die Bedingung wahr war oder nicht.''',
     """temperatur = 33
if temperatur > 30:
    print('Es ist heiß!')
    print('Trink genug Wasser.')
print('Schönen Tag noch.')""")

t("Gib `Akku fast leer!` aus, wenn `akku` (in Prozent) unter 15 liegt. Teste auch mit `40`: Dann soll nichts ausgegeben werden.",
  'akku = 8',
  """if akku < 15:
    print('Akku fast leer!')""")
t("Ist `kontostand` negativ, gib `Konto überzogen!` aus. Danach soll **immer** der Kontostand ausgegeben werden wie unten.",
  'kontostand = -50',
  """if kontostand < 0:
    print('Konto überzogen!')
print('Kontostand:', kontostand)""")
t('Ist `a` größer als `b`, vertausche die Werte der beiden Variablen. Verwende eine Hilfsvariable. Gib danach `a` und `b` aus.',
  'a = 9\nb = 4',
  """if a > b:
    hilf = a
    a = b
    b = hilf
print(a, b)""")
t("Gib `Super!` aus, wenn `punkte` mindestens 90 ist. Gib **zusätzlich** `Volle Punktzahl!` aus, wenn `punkte` genau 100 ist. Verwende zwei `if`-Anweisungen. Teste auch mit `95` und `80`.",
  'punkte = 100',
  """if punkte >= 90:
    print('Super!')
if punkte == 100:
    print('Volle Punktzahl!')""")
t("Ein Getränk kostet 2 Euro. Ist `guthaben` groß genug, ziehe 2 Euro ab und gib `Getränk ausgegeben` aus. Gib danach immer das Guthaben aus.",
  'guthaben = 5',
  """if guthaben >= 2:
    guthaben = guthaben - 2
    print('Getränk ausgegeben')
print('Guthaben:', guthaben)""")
predict("""x = 10
if x > 5:
    x = x - 5
if x > 5:
    x = x - 5
print(x)""", erklaerung='''Die erste Bedingung `10 > 5` ist wahr, also wird `x` zu `5`.
Die zweite Bedingung wird mit dem **neuen** Wert geprüft: `5 > 5` ist falsch. Deshalb bleibt `x` bei `5`.''')
predict("""x = 3
if x > 2:
print('groß')""", error=IndentationError, erklaerung='''Nach dem Doppelpunkt muss ein **eingerückter** Block folgen. Hier ist `print('groß')` nicht eingerückt.
Python meldet einen Einrückungsfehler und führt nichts aus.''')

# ---------------------------------------------------------------- 3
sec('if und else')
expl('''#### `else`

Mit `else` gibt man an, was passieren soll, wenn die Bedingung **falsch** ist.
Es wird also immer **genau einer** der beiden Blöcke ausgeführt. `else` steht ohne Bedingung und auf derselben Höhe wie `if`.''',
     """stunde = 14
if stunde < 12:
    print('Guten Morgen')
else:
    print('Guten Tag')""")
expl('''#### Ausgaben mit f-Strings

Bei einem **f-String** steht ein `f` vor dem Anführungszeichen. In geschweiften Klammern `{...}` kann man Variablen
oder Rechnungen einsetzen. Ihr Wert wird an dieser Stelle in den Text geschrieben.''',
     """preis = 12
anzahl = 3
print(f'{anzahl} Karten kosten {anzahl * preis} Euro.')""")

t("Ein Bus fährt zu jeder Viertelstunde (Minute 0, 15, 30, 45). Gib `Bus kommt` aus, wenn `minute` durch 15 teilbar ist, sonst `kein Bus`. Teste auch mit `20`.",
  'minute = 45',
  """if minute % 15 == 0:
    print('Bus kommt')
else:
    print('kein Bus')""")
t('Speichere die größere der beiden Zahlen in der Variablen `groesser` und gib sie aus. Verwende nicht `max()`.',
  'a = 23\nb = 31',
  """if a > b:
    groesser = a
else:
    groesser = b
print(groesser)""")
t('Ab einem Bestellwert von 100 Euro ist der Versand kostenlos, sonst kostet er 5 Euro. Gib den Gesamtpreis mit einem f-String aus wie unten. Teste auch mit `60`.',
  'bestellwert = 120',
  """if bestellwert >= 100:
    versand = 0
else:
    versand = 5
print(f'Gesamtpreis: {bestellwert + versand} Euro')""")
t("Gib `Weiter geht's!` aus, wenn `antwort` gleich `'ja'` ist, sonst `Abbruch`. Teste auch mit `'nein'` und `'Ja'`.",
  "antwort = 'ja'",
  """if antwort == 'ja':
    print("Weiter geht's!")
else:
    print('Abbruch')""")
t('Speichere den Betrag (die Zahl ohne Vorzeichen) von `x` in der Variablen `betrag`. Verwende `if` und `else`, nicht `abs()`. Gib `betrag` aus.',
  'x = -12',
  """if x < 0:
    betrag = -x
else:
    betrag = x
print(betrag)""")
t("Ein Aufzug darf höchstens 630 kg tragen. Gib `OK` aus, wenn das Gesamtgewicht von `personen` Personen mit je 75 kg passt, sonst `zu schwer`. Teste auch mit `9`.",
  'personen = 8',
  """if personen * 75 <= 630:
    print('OK')
else:
    print('zu schwer')""")
predict("""a = 4
b = 7
if a > b:
    groesser = a
else:
    groesser = b
print(groesser)
if a % 2 == 0:
    print('a gerade')
else:
    print('a ungerade')
print('fertig')""", erklaerung='''- `4 > 7` ist falsch, also wird der `else`-Block ausgeführt: `groesser` wird `7`.
- `4 % 2` ist `0`, also ist die zweite Bedingung wahr und es wird `a gerade` ausgegeben. Der `else`-Block wird übersprungen.
- `print('fertig')` ist nicht eingerückt und wird immer ausgeführt.''')

# ---------------------------------------------------------------- 4
sec('elif')
expl('''#### Mehrere Fälle mit `elif`

Mit `elif` (kurz für „else if“) prüft man weitere Bedingungen, wenn die vorherigen **falsch** waren.

- Die Bedingungen werden **von oben nach unten** geprüft.
- Nur der Block der **ersten** wahren Bedingung wird ausgeführt. Alle weiteren werden übersprungen.
- Das `else` am Ende ist optional. Es greift, wenn keine Bedingung wahr war.

Deshalb ist die **Reihenfolge** wichtig.''',
     """wind = 45
if wind < 20:
    print('leichter Wind')
elif wind < 50:
    print('frischer Wind')
elif wind < 75:
    print('Sturm')
else:
    print('Orkan')""")

t("Gib für die Ampelfarbe aus, was zu tun ist: `rot` → `Stehen`, `gelb` → `Achtung`, `grün` → `Fahren`. Bei jeder anderen Farbe gib `Ampel kaputt` aus. Teste auch mit `'blau'`.",
  "farbe = 'gelb'",
  """if farbe == 'rot':
    print('Stehen')
elif farbe == 'gelb':
    print('Achtung')
elif farbe == 'grün':
    print('Fahren')
else:
    print('Ampel kaputt')""")
t('Ein Händler gibt Mengenrabatt: ab 50 Stück 20 %, ab 20 Stück 10 %, ab 10 Stück 5 %, sonst keinen. Gib den Rabatt aus wie unten. Teste auch mit 50, 9 und 10.',
  'anzahl = 25',
  """if anzahl >= 50:
    rabatt = 20
elif anzahl >= 20:
    rabatt = 10
elif anzahl >= 10:
    rabatt = 5
else:
    rabatt = 0
print(f'Rabatt: {rabatt} %')""")
task('''Der folgende Code soll für 95 Punkte die Note 1 ausgeben, gibt aber die Note 4 aus.
Schreibe ihn in die Codezelle und ändere die Reihenfolge der Bedingungen so, dass er richtig arbeitet. Teste auch mit 75 und 55.
```python
punkte = 95
if punkte >= 50:
    note = 4
elif punkte >= 70:
    note = 3
elif punkte >= 80:
    note = 2
elif punkte >= 90:
    note = 1
else:
    note = 5
print(note)
```''',
     solution="""punkte = 95
if punkte >= 90:
    note = 1
elif punkte >= 80:
    note = 2
elif punkte >= 70:
    note = 3
elif punkte >= 50:
    note = 4
else:
    note = 5
print(note)""")
t("Ein kleiner Taschenrechner: Berechne je nach `op` (`'+'`, `'-'`, `'*'`, `'/'`) das Ergebnis von `a op b` und gib es aus. Bei einem anderen Zeichen gib `unbekannter Operator` aus.",
  "a = 12\nb = 4\nop = '/'",
  """if op == '+':
    print(a + b)
elif op == '-':
    print(a - b)
elif op == '*':
    print(a * b)
elif op == '/':
    print(a / b)
else:
    print('unbekannter Operator')""")
predict("""x = 15
if x > 10:
    print('A')
elif x > 5:
    print('B')
else:
    print('C')
if x > 20:
    print('D')
elif x % 5 == 0:
    print('E')""", erklaerung='''- Erste `if`-Anweisung: `15 > 10` ist wahr, also wird `A` ausgegeben. `15 > 5` wäre auch wahr, wird aber
  gar nicht mehr geprüft, weil nur der Block der **ersten** wahren Bedingung ausgeführt wird.
- Die zweite `if`-Anweisung ist unabhängig von der ersten: `15 > 20` ist falsch, `15 % 5 == 0` ist wahr. Also wird `E` ausgegeben.''')

# ---------------------------------------------------------------- 5
sec('and, or und not')
expl('''#### Logische Operatoren

Mit logischen Operatoren verbindet man Bedingungen:

- `a and b` ist wahr, wenn **beide** wahr sind.
- `a or b` ist wahr, wenn **mindestens eine** wahr ist.
- `not a` kehrt den Wahrheitswert um.

Rangfolge: Zuerst wird `not` ausgewertet, dann `and`, dann `or`. Im Zweifel setzt man **Klammern**.''',
     """stunde = 23
feiertag = False
print(stunde < 6 or stunde >= 22)
print(stunde >= 8 and not feiertag)
regen = False
if not regen:
    print('Wir gehen raus.')""")

t("Für die Achterbahn muss man mindestens 1.40 m groß **und** mindestens 8 Jahre alt sein. Gib `darf fahren` oder `darf nicht fahren` aus. Teste auch mit `groesse = 1.45`.",
  'groesse = 1.35\nalter = 9',
  """if groesse >= 1.40 and alter >= 8:
    print('darf fahren')
else:
    print('darf nicht fahren')""")
t("Eine Wetterstation misst die Temperatur. Werte unter -40 **oder** über 50 Grad sind vermutlich Messfehler. Gib `Messfehler?` oder `ok` aus. Teste auch mit 20 und -45.",
  'temperatur = 57',
  """if temperatur < -40 or temperatur > 50:
    print('Messfehler?')
else:
    print('ok')""")
t("Gib `Feiertag` aus, wenn `datum` gleich `'01.01.'`, `'01.05.'` oder `'03.10.'` ist, sonst `kein Feiertag`. Teste auch mit `'24.12.'`.",
  "datum = '03.10.'",
  """if datum == '01.01.' or datum == '01.05.' or datum == '03.10.':
    print('Feiertag')
else:
    print('kein Feiertag')""")
t('''Ein Jahr ist ein Schaltjahr, wenn es durch 4, aber nicht durch 100 teilbar ist, **oder** wenn es durch 400 teilbar ist.
Speichere das Ergebnis in `schaltjahr` und gib es aus. Teste auch mit 2024, 2000 und 2026.''',
  'jahr = 1900',
  """schaltjahr = (jahr % 4 == 0 and jahr % 100 != 0) or jahr % 400 == 0
print(schaltjahr)""")
t("Aus drei Seitenlängen kann man nur dann ein Dreieck bauen, wenn jeweils zwei Seiten zusammen länger sind als die dritte. Gib `Dreieck` oder `kein Dreieck` aus. Teste auch mit 3, 4, 5.",
  'a = 3\nb = 4\nc = 8',
  """if a + b > c and a + c > b and b + c > a:
    print('Dreieck')
else:
    print('kein Dreieck')""")
t('Prüfe auf zwei Arten, ob `x` **außerhalb** des Bereichs von 1 bis 10 liegt: einmal mit `not` und einer Vergleichskette, einmal mit `or`. Gib beide Ergebnisse aus.',
  'x = 5',
  """print(not (1 <= x <= 10))
print(x < 1 or x > 10)""")
t("Beim Würfeln mit zwei Würfeln gilt: Zwei Sechsen sind ein `Hauptgewinn`, zwei gleiche Zahlen sonst ein `Pasch`, alles andere `nichts`. Achte auf die Reihenfolge der Bedingungen. Teste auch mit 4 und 4 und mit 2 und 5.",
  'w1 = 6\nw2 = 6',
  """if w1 == 6 and w2 == 6:
    print('Hauptgewinn')
elif w1 == w2:
    print('Pasch')
else:
    print('nichts')""")
predict("""sonne = False
wind = True
print(sonne or wind)
print(sonne and wind)
print(not sonne and wind)
print(not (sonne and wind))
print(sonne or not wind)""", erklaerung='''- `sonne or wind`: `wind` ist wahr, das reicht für `or`. Ergebnis `True`.
- `sonne and wind`: `sonne` ist falsch, also ist `and` falsch. Ergebnis `False`.
- `not sonne and wind`: Zuerst `not sonne`, das ist `True`. `True and True` ergibt `True`.
- `not (sonne and wind)`: Die Klammer ergibt `False`, `not False` ergibt `True`.
- `sonne or not wind`: `not wind` ist `False`. `False or False` ergibt `False`.''')
predict("""x = 4
print(x > 3 or x < 2 and x == 0)
print((x > 3 or x < 2) and x == 0)""", erklaerung='''Die einzelnen Vergleiche: `x > 3` ist `True`, `x < 2` ist `False`, `x == 0` ist `False`.

- Ohne Klammern wird `and` vor `or` ausgewertet: `x < 2 and x == 0` ergibt `False`. Dann `True or False`, also `True`.
- Mit Klammern wird zuerst die Klammer ausgewertet: `True or False` ergibt `True`. Dann `True and False`, also `False`.''')

# ---------------------------------------------------------------- 6
sec('Verschachtelte Bedingungen')
expl('''#### Bedingungen in Bedingungen

Ein `if` kann im Block eines anderen `if` stehen. Dann wird die innere Bedingung nur geprüft, wenn die äußere wahr ist.
Der innere Block ist **doppelt** eingerückt. Manchmal kann man verschachtelte Bedingungen auch mit `and` zusammenfassen.''',
     """alter = 20
hat_ausweis = False
if alter >= 18:
    if hat_ausweis:
        print('Eintritt')
    else:
        print('Bitte Ausweis zeigen')
else:
    print('Kein Eintritt')""")

t('''Gib aus, in welchem Quadranten der Punkt `(x, y)` liegt: `I` (rechts oben), `II` (links oben), `III` (links unten), `IV` (rechts unten).
Liegt der Punkt auf einer Achse, gib `auf einer Achse` aus. Teste auch mit `(3, -2)` und `(0, 5)`.''',
  'x = -4\ny = 2',
  """if x == 0 or y == 0:
    print('auf einer Achse')
elif x > 0:
    if y > 0:
        print('I')
    else:
        print('IV')
else:
    if y > 0:
        print('II')
    else:
        print('III')""")
t('Finde mit verschachtelten Bedingungen die größte der drei Zahlen und gib sie aus. Verwende nicht `max()`. Teste auch mit anderen Reihenfolgen.',
  'a = 8\nb = 15\nc = 11',
  """if a > b:
    if a > c:
        print(a)
    else:
        print(c)
else:
    if b > c:
        print(b)
    else:
        print(c)""")
task('''Schreibe den folgenden Code so um, dass er nur **ein** `if` mit `and` verwendet und dasselbe ausgibt.
```python
sonne = True
temperatur = 26
if sonne:
    if temperatur > 25:
        print('Ab ins Freibad!')
```''',
     given="sonne = True\ntemperatur = 26",
     solution="""sonne = True
temperatur = 26
if sonne and temperatur > 25:
    print('Ab ins Freibad!')""")
t('''Im Parkhaus kostet die erste Stunde 3 Euro, jede weitere Stunde 2 Euro, höchstens aber 15 Euro am Tag.
Am Wochenende gilt ein Pauschalpreis von 6 Euro. Gib den Preis aus. Teste auch mit 2 und 9 Stunden und mit `wochenende = True`.''',
  'stunden = 5\nwochenende = False',
  """if wochenende:
    preis = 6
else:
    preis = 3 + (stunden - 1) * 2
    if preis > 15:
        preis = 15
print(f'Preis: {preis} Euro')""")
t("Gib `Fieber` aus, wenn `temperatur` über 38 Grad liegt. Liegt sie sogar über 39.5 Grad, gib zusätzlich `Arzt anrufen!` aus. Liegt sie unter 36 Grad, gib `Untertemperatur` aus, sonst `normal`. Teste mit 39.8, 38.5, 35.5 und 37.",
  'temperatur = 39.8',
  """if temperatur > 38:
    print('Fieber')
    if temperatur > 39.5:
        print('Arzt anrufen!')
elif temperatur < 36:
    print('Untertemperatur')
else:
    print('normal')""")
predict("""a = 5
b = 0
if a > 3:
    if b > 3:
        print('X')
    else:
        print('Y')
    print('Z')
else:
    print('W')
print('fertig')""", erklaerung='''- `5 > 3` ist wahr, also wird der äußere Block ausgeführt.
- Darin ist `0 > 3` falsch, also wird `Y` ausgegeben.
- `print('Z')` gehört zum äußeren Block (einfach eingerückt), nicht zum inneren `else`. Es wird deshalb auch ausgegeben.
- Das äußere `else` wird übersprungen, `print('fertig')` wird immer ausgeführt.''')

# ---------------------------------------------------------------- 7
sec('Kurze Bedingungen')
expl('''#### Wahrheitswert von Zahlen und Zeichenketten

Auch Zahlen und Zeichenketten haben einen Wahrheitswert. Mit `bool(...)` kann man ihn sehen.

- Die Zahl `0` und die leere Zeichenkette `''` gelten als **falsch**.
- Alle anderen Zahlen und alle nicht leeren Zeichenketten gelten als **wahr**.

Deshalb kann man z. B. kurz `if name:` schreiben statt `if name != '':`.''',
     """print(bool(0), bool(42), bool(''), bool('Hallo'))
name = ''
if name:
    print('Hallo', name)
else:
    print('Kein Name angegeben')""")
expl('''#### `in` bei Zeichenketten

`teil in text` prüft, ob `teil` in `text` vorkommt. Das kann ein einzelnes Zeichen oder ein längerer Text sein.''',
     """print('e' in 'Hallo')
print('all' in 'Hallo')
buchstabe = 'o'
if buchstabe in 'aeiou':
    print('Vokal')""")
expl('''#### Der bedingte Ausdruck

Für einfache Fälle gibt es eine kurze Schreibweise in **einer** Zeile:

`wert1 if bedingung else wert2`

Ist die Bedingung wahr, ist das Ergebnis `wert1`, sonst `wert2`.''',
     """temperatur = 12
kleidung = 'Jacke' if temperatur < 15 else 'T-Shirt'
print(kleidung)""")

t("`kekse` Kekse werden gerecht auf `kinder` Kinder verteilt. Speichere in `rest`, wie viele Kekse übrig bleiben. Gib mit `if rest:` den Satz unten aus, sonst `Geht genau auf`. Teste auch mit `kekse = 24`.",
  'kekse = 26\nkinder = 6',
  """rest = kekse % kinder
if rest:
    print(f'Es bleiben {rest} Kekse übrig')
else:
    print('Geht genau auf')""")
t("Eine E-Mail-Adresse muss ein `@` enthalten. Gib `gültig` oder `ungültig` aus. Teste auch mit `'max@schule.de'`.",
  "email = 'max.schule.de'",
  """if '@' in email:
    print('gültig')
else:
    print('ungültig')""")
t("Gib die Anzahl mit dem passenden Wort aus: `1 Apfel`, aber `3 Äpfel`. Verwende einen bedingten Ausdruck und einen f-String. Teste auch mit `anzahl = 1`.",
  'anzahl = 3',
  """wort = 'Apfel' if anzahl == 1 else 'Äpfel'
print(f'{anzahl} {wort}')""")
t('Speichere mit einem bedingten Ausdruck die kleinere der beiden Zahlen in `kleiner` und gib sie aus.',
  'a = 17\nb = 12',
  """kleiner = a if a < b else b
print(kleiner)""")
t("Gib `Spam?` aus, wenn in `betreff` das Wort `'Gewinn'` **oder** das Wort `'gratis'` vorkommt, sonst `ok`.",
  "betreff = 'Ihr Gewinn wartet'",
  """if 'Gewinn' in betreff or 'gratis' in betreff:
    print('Spam?')
else:
    print('ok')""")
predict("""print(bool(0), bool(7), bool(''), bool('0'))
x = 0
print('ja' if x else 'nein')
print('ha' in 'Hallo', 'Ha' in 'Hallo')""", erklaerung='''- `0` und `''` sind falsch, `7` ist wahr. `'0'` ist eine **nicht leere** Zeichenkette (sie enthält das Zeichen 0) und deshalb wahr.
- `x` ist `0`, gilt also als falsch. Der bedingte Ausdruck liefert deshalb `'nein'`.
- `in` unterscheidet Groß- und Kleinschreibung: `'ha'` kommt in `'Hallo'` nicht vor, `'Ha'` schon.''')

# ---------------------------------------------------------------- 8
sec('Gemischte Übungen')
t('''Kinopreise: Dienstag (`'Di'`) ist Kinotag, da kostet jede Karte 5 Euro. An anderen Tagen zahlen Kinder unter 12 Jahren 6 Euro,
Studierende 7 Euro und alle anderen 9 Euro. Gib den Preis aus. Teste auch mit verschiedenen Werten.''',
  "alter = 20\ntag = 'Mo'\nstudent = True",
  """if tag == 'Di':
    preis = 5
elif alter < 12:
    preis = 6
elif student:
    preis = 7
else:
    preis = 9
print(f'Preis: {preis} Euro')""")
t('''Gib Tipps zum Wetter aus. Mehrere Tipps können gleichzeitig gelten: unter 5 Grad `Mütze nicht vergessen`,
bei Regen `Schirm mitnehmen`, über 25 Grad `Sonnencreme benutzen`. Gilt keiner, gib `Viel Spaß draußen` aus.''',
  'temperatur = 3\nregen = True',
  """tipp = False
if temperatur < 5:
    print('Mütze nicht vergessen')
    tipp = True
if regen:
    print('Schirm mitnehmen')
    tipp = True
if temperatur > 25:
    print('Sonnencreme benutzen')
    tipp = True
if not tipp:
    print('Viel Spaß draußen')""")
t("Prüfe, ob `stunde` und `minute` eine gültige Uhrzeit ergeben (Stunde 0 bis 23, Minute 0 bis 59). Gib `gültig` oder `ungültig` aus. Teste auch mit 24 und 0.",
  'stunde = 23\nminute = 60',
  """if 0 <= stunde <= 23 and 0 <= minute <= 59:
    print('gültig')
else:
    print('ungültig')""")
t('''Vereinfachte Steuer: Bis 12000 Euro Einkommen zahlt man keine Steuer, bis 60000 Euro zahlt man 20 % des gesamten Einkommens,
darüber 40 %. Gib die Steuer aus. Teste auch mit 10000 und 80000.''',
  'einkommen = 45000',
  """if einkommen <= 12000:
    steuer = 0
elif einkommen <= 60000:
    steuer = einkommen * 0.2
else:
    steuer = einkommen * 0.4
print(f'Steuer: {steuer}')""")
t("Schere, Stein, Papier: Schere schlägt Papier, Stein schlägt Schere, Papier schlägt Stein. Gib `Unentschieden`, `Spieler 1 gewinnt` oder `Spieler 2 gewinnt` aus. Teste verschiedene Kombinationen.",
  "spieler1 = 'Stein'\nspieler2 = 'Schere'",
  """if spieler1 == spieler2:
    print('Unentschieden')
elif (spieler1 == 'Schere' and spieler2 == 'Papier') or (spieler1 == 'Stein' and spieler2 == 'Schere') or (spieler1 == 'Papier' and spieler2 == 'Stein'):
    print('Spieler 1 gewinnt')
else:
    print('Spieler 2 gewinnt')""")
t("Bestimme die Art des Dreiecks: alle Seiten gleich `gleichseitig`, genau zwei gleich `gleichschenklig`, sonst `unregelmäßig`. Teste auch mit 4, 4, 4 und 3, 4, 5.",
  'a = 5\nb = 7\nc = 5',
  """if a == b and b == c:
    print('gleichseitig')
elif a == b or a == c or b == c:
    print('gleichschenklig')
else:
    print('unregelmäßig')""")
t("Ein Rabattcode ist gültig, wenn er genau `'SOMMER'` oder `'WINTER'` lautet und der Einkaufswert mindestens 30 Euro beträgt. Gib den Endpreis mit 10 % Rabatt aus, sonst den normalen Preis. Teste auch mit anderen Werten.",
  "code = 'SOMMER'\nwert = 50",
  """if (code == 'SOMMER' or code == 'WINTER') and wert >= 30:
    print(f'Endpreis: {wert * 0.9}')
else:
    print(f'Endpreis: {wert}')""")
predict("""x = 7
y = 0 if x > 5 else 1
if y:
    print('A')
elif not y and x % 2:
    print('B')
else:
    print('C')
print(x > 5 and y == 0 or x < 0)""", erklaerung='''- `7 > 5` ist wahr, also bekommt `y` den Wert `0`.
- `if y:` ist falsch, weil `0` als falsch gilt.
- `not y` ist `True`. `x % 2` ist `1`, und `1` gilt als wahr. Also ist die `elif`-Bedingung wahr, und es wird `B` ausgegeben.
- Letzte Zeile: Zuerst `and`: `x > 5 and y == 0` ergibt `True`. Dann `True or False`, also `True`.''')

generate('bedingungen', 'Bedingungen')
