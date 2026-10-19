# Erzeugt ../content/strings.ipynb (siehe nbgen.py).
from nbgen import sec, expl, task, predict, generate

# ---------------------------------------------------------------- 1
sec('Zeichenketten erstellen und ausgeben')
expl('''#### Was ist eine Zeichenkette?

Eine **Zeichenkette** (englisch *string*, Datentyp `str`) ist ein Text. Sie steht in einfachen `'...'`
oder doppelten `"..."` Anführungszeichen. Beides bedeutet dasselbe.

- Will man einfache Anführungszeichen im Text haben, nimmt man außen doppelte, und umgekehrt.
- Mit drei Anführungszeichen `\'\'\'...\'\'\'` kann eine Zeichenkette über **mehrere Zeilen** gehen.
- `''` ist eine **leere Zeichenkette**.''',
     """a = 'Hallo'
b = "Welt"
c = "Ich heiße 'Max'."
d = '''Zeile 1
Zeile 2'''
print(a, b)
print(c)
print(d)
print(type(a))""")
expl(r'''#### Escape-Zeichen

Mit einem Backslash `\` kann man besondere Zeichen in eine Zeichenkette schreiben:

| Schreibweise | Bedeutung |
|---|---|
| `\n` | neue Zeile |
| `\t` | Tabulator |
| `\'` | einfaches Anführungszeichen |
| `\"` | doppeltes Anführungszeichen |
| `\\` | ein Backslash |''',
     r"""print('Zeile 1\nZeile 2')
print('Name\tAlter')
print('It\'s')
print("Er sagte: \"Hi\"")
print('C:\\Daten')""")
expl('''#### `len()`

`len(text)` gibt die **Anzahl der Zeichen** einer Zeichenkette zurück. Leerzeichen zählen mit.''',
     """print(len('Hallo'))
print(len('Hallo Welt'))
print(len(''))""")
expl('''#### f-Strings

Steht vor der Zeichenkette ein `f`, kann man in geschweiften Klammern `{...}` Variablen und Ausdrücke einsetzen.
Ihr Wert wird dann in den Text geschrieben.''',
     """name = 'Ali'
alter = 16
print(f'{name} ist {alter} Jahre alt.')
print(f'In 10 Jahren ist {name} {alter + 10}.')
print(f'{name} hat {len(name)} Buchstaben.')""")

task('Speichere den Titel deines Lieblingsfilms in der Variablen `film` und gib ihn aus.',
     solution="""film = 'Zurück in die Zukunft'
print(film)""", kind='free')
task(r'Gib mit **einem** `print()` und `\n` die drei Zeilen unten aus.',
     solution=r"""print('Eins\nZwei\nDrei')""")
task('Gib den Satz unten aus. Achte auf die Anführungszeichen.',
     solution="""print('Er sagte: "Hallo!"')""")
task(r'''Gib den Satz unten aus. Verwende außen **einfache** Anführungszeichen und `\'`.''',
     solution=r"""print('It\'s fun.')""")
task(r'Gib den Pfad unten aus. Verwende `\\`.',
     solution=r"""print('C:\\Users\\Schule')""")
task(r'Gib mit `\t` die kleine Tabelle unten aus. Verwende pro Zeile ein `print()`.',
     solution=r"""print('Name\tAlter')
print('Ali\t16')
print('Bea\t17')""")
task('Gib die Länge von `wort` aus.',
     given="wort = 'Donaudampfschifffahrt'",
     solution="""wort = 'Donaudampfschifffahrt'
print(len(wort))""")
task('Gib mit einem f-String und `len()` den Satz unten aus.',
     given="wort = 'Informatik'",
     solution="""wort = 'Informatik'
print(f'Das Wort {wort} hat {len(wort)} Buchstaben.')""")
task("""Speichere mit drei Anführungszeichen `'''...'''` die drei Zeilen unten in der Variablen `gedicht` und gib sie aus.""",
     solution="""gedicht = '''Rosen sind rot,
Veilchen sind blau,
Python ist toll.'''
print(gedicht)""")
task('Gib mit einem f-String aus, wie lang die Zeichenketten `a` und `b` zusammen sind.',
     given="""a = 'Haus'
b = 'Schlüssel'""",
     solution="""a = 'Haus'
b = 'Schlüssel'
print(f'Zusammen: {len(a) + len(b)} Zeichen')""")
predict(r"""a = 'Hallo'
b = ''
c = 'a b'
print(len(a), len(b), len(c))
print(len('Zeile\nZeile'))
print(type(a))""")

# ---------------------------------------------------------------- 2
sec('Verbinden, wiederholen und umwandeln')
expl('''#### Verbinden mit `+`

Mit `+` hängt man Zeichenketten aneinander. Leerzeichen werden **nicht** automatisch eingefügt.
Mit `+=` hängt man etwas an eine Variable an.''',
     """a = 'Haus'
b = 'tür'
print(a + b)
print(a + ' ' + b)
text = 'A'
text += 'B'
text += 'C'
print(text)""")
expl('''#### Wiederholen mit `*`

`text * n` ergibt eine Zeichenkette, in der `text` `n`-mal hintereinander steht.''',
     """print('ab' * 3)
print('-' * 20)""")
expl('''#### `str()`, `int()` und `float()`

- `str(wert)` wandelt einen Wert, z. B. eine Zahl, in eine Zeichenkette um.
- `int(text)` wandelt eine Zeichenkette in eine ganze Zahl um, `float(text)` in eine Kommazahl.

Eine Zeichenkette und eine Zahl kann man nicht mit `+` verbinden. Das gibt einen `TypeError`.
Man muss die Zahl vorher mit `str()` umwandeln.''',
     """alter = 16
print('Ich bin ' + str(alter) + ' Jahre alt.')
print(int('12') + 1)
print(float('2.5') * 2)""")

task('Verbinde `vorname` und `nachname` mit einem Leerzeichen dazwischen zur Variablen `name`. Gib `name` aus.',
     given="""vorname = 'Max'
nachname = 'Mustermann'""",
     solution="""vorname = 'Max'
nachname = 'Mustermann'
name = vorname + ' ' + nachname
print(name)""")
task("Gib mit `*` eine Linie aus 30 Minuszeichen aus.",
     solution="""print('-' * 30)""")
task("Gib mit `*` und `+` die Zeichenkette unten aus.",
     given="wort = 'Ha'",
     solution="""wort = 'Ha'
print(wort * 3 + '!')""")
task('Gib mit `+` und `str()` den Satz unten aus.',
     given='alter = 16',
     solution="""alter = 16
print('Ich bin ' + str(alter) + ' Jahre alt.')""")
task('Gib zuerst `a + b` aus. Wandle dann beide mit `int()` in Zahlen um und gib ihre Summe aus.',
     given="""a = '12'
b = '30'""",
     solution="""a = '12'
b = '30'
print(a + b)
print(int(a) + int(b))""")
task('Wandle `preis` mit `float()` in eine Zahl um und gib den Preis für 4 Stück aus.',
     given="preis = '3.50'",
     solution="""preis = '3.50'
print(float(preis) * 4)""")
task('Gib mit einer `for`-Schleife und `*` die Treppe unten aus.',
     solution="""for i in range(1, 6):
    print('*' * i)""")
task("Erzeuge mit einer `for`-Schleife und `+=` die Zeichenkette `'12345'`. Beginne mit einer leeren Zeichenkette. Gib das Ergebnis aus.",
     solution="""text = ''
for i in range(1, 6):
    text += str(i)
print(text)""")
task('Gib mit einer `for`-Schleife, `*` und `+` das Dreieck unten aus. Jede Zeile beginnt mit Leerzeichen.',
     solution="""for i in range(1, 5):
    print(' ' * (4 - i) + '#' * (2 * i - 1))""")
predict("""a = '3'
b = 4
print(a * b)
print(int(a) * b)
print(a + str(b))
print(float(a) + b)""")
predict("""alter = 16
print('Alter: ' + alter)""", error=TypeError)

# ---------------------------------------------------------------- 3
sec('Auf Zeichen zugreifen (Index und Slicing)')
expl('''#### Index

Jedes Zeichen einer Zeichenkette hat einen **Index**. Das erste Zeichen hat den Index **0**.
Mit `text[index]` erhält man das Zeichen an dieser Stelle. Ein negativer Index zählt von hinten:
`text[-1]` ist das letzte Zeichen.''',
     """wort = 'Python'
print(wort[0])
print(wort[3])
print(wort[-1])
print(wort[len(wort) - 1])""")
expl('''#### Slicing

`text[start:stop]` ergibt die Zeichen von Index `start` bis **ausschließlich** `stop`.
Fehlt `start`, beginnt der Bereich am Anfang. Fehlt `stop`, geht er bis zum Ende.
Auch negative Indizes sind erlaubt.''',
     """wort = 'Python'
print(wort[1:4])
print(wort[:2])
print(wort[2:])
print(wort[-3:])""")
expl('''#### Zeichenketten sind unveränderlich

Man kann ein einzelnes Zeichen **nicht** ändern. `text[0] = 'X'` gibt einen `TypeError`.
Stattdessen baut man eine neue Zeichenkette, z. B. mit Slicing und `+`.''',
     """wort = 'Haus'
neu = 'M' + wort[1:]
print(neu)""")

WORT = "wort = 'Programmieren'"
task('Gib das erste und das letzte Zeichen von `wort` aus, jeweils in einer eigenen Zeile.',
     given=WORT, solution=WORT + """
print(wort[0])
print(wort[-1])""")
task('Gib das dritte Zeichen von `wort` aus.',
     given=WORT, solution=WORT + """
print(wort[2])""")
task('Gib die ersten 7 Zeichen von `wort` aus.',
     given=WORT, solution=WORT + """
print(wort[:7])""")
task('Gib die letzten 3 Zeichen von `wort` aus.',
     given=WORT, solution=WORT + """
print(wort[-3:])""")
task('Gib alle Zeichen von `wort` ab Index 3 aus.',
     given=WORT, solution=WORT + """
print(wort[3:])""")
task("Gib mit Slicing `'gramm'` aus `wort` aus.",
     given=WORT, solution=WORT + """
print(wort[3:8])""")
task('Speichere mit Slicing Tag, Monat und Jahr aus `datum` in drei Variablen. Gib sie aus wie unten.',
     given="datum = '17.10.2026'",
     solution="""datum = '17.10.2026'
tag = datum[:2]
monat = datum[3:5]
jahr = datum[6:]
print('Tag:', tag)
print('Monat:', monat)
print('Jahr:', jahr)""")
task("Erzeuge aus `wort` mit Slicing und `+` die Zeichenkette `'Maus'`. Gib sie aus.",
     given="wort = 'Haus'",
     solution="""wort = 'Haus'
print('M' + wort[1:])""")
task('Gib `text` ohne das erste und das letzte Zeichen aus.',
     given="""text = '"Hallo"'""",
     solution="""text = '"Hallo"'
print(text[1:-1])""")
task('Gib den Ländercode (die ersten beiden Zeichen) und die Prüfziffer (Index 2 und 3) von `iban` aus.',
     given="iban = 'DE89370400440532013000'",
     solution="""iban = 'DE89370400440532013000'
print(iban[:2])
print(iban[2:4])""")
task('Gib das mittlere Zeichen von `wort` aus. Berechne den Index mit `len()` und `//`.',
     given="wort = 'Stuhl'",
     solution="""wort = 'Stuhl'
print(wort[len(wort) // 2])""")
task('Vertausche die erste und die zweite Hälfte von `wort` und gib das Ergebnis aus.',
     given="wort = 'Fußball'",
     solution="""wort = 'Fußball'
mitte = len(wort) // 2
print(wort[mitte:] + wort[:mitte])""")
predict("""s = 'Python'
print(s[0], s[-1])
print(s[1:4])
print(s[:2] + s[-2:])
print(s[10:])
print(len(s[2:]))""")
predict("""s = 'Haus'
s[0] = 'M'
print(s)""", error=TypeError)

# ---------------------------------------------------------------- 4
sec('Schleifen über Zeichenketten und in')
expl('''#### `for`-Schleife über die Zeichen

Mit `for zeichen in text:` durchläuft man eine Zeichenkette **Zeichen für Zeichen**.
Mit `for i in range(len(text)):` durchläuft man die Indizes.''',
     """for c in 'Hallo':
    print(c)
wort = 'Eis'
for i in range(len(wort)):
    print(i, wort[i])""")
expl('''#### `in` und `not in`

`teil in text` prüft, ob `teil` irgendwo in `text` vorkommt. `teil` kann ein einzelnes Zeichen oder ein längerer Text sein.
Groß- und Kleinschreibung werden unterschieden.''',
     """satz = 'Ich lerne Python.'
print('Python' in satz)
print('python' in satz)
print('x' not in satz)
print('e' in 'aeiou')""")

task('Gib jedes Zeichen von `wort` in einer eigenen Zeile aus.',
     given="wort = 'Hallo'",
     solution="""wort = 'Hallo'
for c in wort:
    print(c)""")
task("Zähle mit einer Schleife, wie oft `'e'` in `satz` vorkommt. Gib die Anzahl aus.",
     given="satz = 'Wenn hinter Fliegen Fliegen fliegen'",
     solution="""satz = 'Wenn hinter Fliegen Fliegen fliegen'
anzahl = 0
for c in satz:
    if c == 'e':
        anzahl += 1
print(anzahl)""")
task("Zähle mit einer Schleife die Vokale (a, e, i, o, u) in `satz`. Verwende `in 'aeiou'`. Gib die Anzahl aus.",
     given="satz = 'informatik macht spass'",
     solution="""satz = 'informatik macht spass'
anzahl = 0
for c in satz:
    if c in 'aeiou':
        anzahl += 1
print(anzahl)""")
task('Erzeuge mit einer Schleife eine neue Zeichenkette, in der jedes Zeichen von `wort` doppelt vorkommt. Gib sie aus.',
     given="wort = 'Hallo'",
     solution="""wort = 'Hallo'
neu = ''
for c in wort:
    neu += c + c
print(neu)""")
task('Erzeuge mit einer Schleife eine Zeichenkette, die `wort` rückwärts enthält. Gib sie aus.',
     given="wort = 'Hallo'",
     solution="""wort = 'Hallo'
rueckwaerts = ''
for c in wort:
    rueckwaerts = c + rueckwaerts
print(rueckwaerts)""")
task('Gib jedes Zeichen von `wort` zusammen mit seinem Index aus wie unten.',
     given="wort = 'Code'",
     solution="""wort = 'Code'
for i in range(len(wort)):
    print(i, wort[i])""")
task("Prüfe mit `in`, ob `'Python'` in `satz` vorkommt. Gib `gefunden` oder `nicht gefunden` aus.",
     given="satz = 'Wir programmieren heute mit Python.'",
     solution="""satz = 'Wir programmieren heute mit Python.'
if 'Python' in satz:
    print('gefunden')
else:
    print('nicht gefunden')""")
task("""Eine E-Mail-Adresse muss ein `'@'` enthalten. Gib `gültig` oder `ungültig` aus.
Teste dein Programm auch mit `email = 'max.schule.de'`.""",
     given="email = 'max@schule.de'",
     solution="""email = 'max@schule.de'
if '@' in email:
    print('gültig')
else:
    print('ungültig')""")
task('Erzeuge mit einer Schleife eine neue Zeichenkette ohne die Leerzeichen aus `satz`. Gib sie aus.',
     given="satz = 'Das ist ein Test'",
     solution="""satz = 'Das ist ein Test'
neu = ''
for c in satz:
    if c != ' ':
        neu += c
print(neu)""")
task("Zähle mit einer Schleife und `in '0123456789'`, wie viele Ziffern in `text` vorkommen. Gib die Anzahl aus.",
     given="text = 'Raum 204, Haus 7, Tel. 0301234'",
     solution="""text = 'Raum 204, Haus 7, Tel. 0301234'
anzahl = 0
for c in text:
    if c in '0123456789':
        anzahl += 1
print(anzahl)""")
task('Gib nur die Zeichen von `text` aus, die an einem geraden Index stehen, alle zusammen in einer Zeile.',
     given="text = 'Pxyytzhqown'",
     solution="""text = 'Pxyytzhqown'
neu = ''
for i in range(len(text)):
    if i % 2 == 0:
        neu += text[i]
print(neu)""")
predict("""s = 'Banane'
z = 0
for c in s:
    if c == 'a':
        z += 1
print(z)
print('nan' in s)
print('Ban' not in s)""")

# ---------------------------------------------------------------- 5
sec('Groß- und Kleinschreibung')
expl('''#### `upper()` und `lower()`

`text.upper()` gibt den Text in **Großbuchstaben** zurück, `text.lower()` in **Kleinbuchstaben**.

Alle String-Methoden geben eine **neue** Zeichenkette zurück. Die ursprüngliche Zeichenkette bleibt unverändert.
Will man das Ergebnis behalten, muss man es speichern, z. B. `text = text.upper()`.''',
     """text = 'Hallo Welt'
print(text.upper())
print(text.lower())
print(text)""")
expl('''#### `capitalize()`, `title()` und `swapcase()`

- `text.capitalize()`: erster Buchstabe groß, alle anderen klein.
- `text.title()`: in **jedem Wort** der erste Buchstabe groß, die anderen klein.
- `text.swapcase()`: große Buchstaben werden klein und kleine groß.''',
     """text = 'hallo WELT'
print(text.capitalize())
print(text.title())
print(text.swapcase())""")

task('Gib `name` in Großbuchstaben aus.',
     given="name = 'Lena'",
     solution="""name = 'Lena'
print(name.upper())""")
task('Gib `satz` in Kleinbuchstaben aus.',
     given="satz = 'Heute ist MONTAG.'",
     solution="""satz = 'Heute ist MONTAG.'
print(satz.lower())""")
task('Gib `text` so aus, dass nur der erste Buchstabe groß ist.',
     given="text = 'hallo welt'",
     solution="""text = 'hallo welt'
print(text.capitalize())""")
task('Gib `titel` so aus, dass jedes Wort mit einem Großbuchstaben beginnt.',
     given="titel = 'der herr der ringe'",
     solution="""titel = 'der herr der ringe'
print(titel.title())""")
task('Tausche in `text` Groß- und Kleinbuchstaben und gib das Ergebnis aus.',
     given="text = 'pYTHON'",
     solution="""text = 'pYTHON'
print(text.swapcase())""")
task("""Gib `Zustimmung` aus, wenn `antwort` `ja` lautet, egal in welcher Schreibweise. Sonst gib `Ablehnung` aus.
Teste dein Programm auch mit `'Ja'`, `'jA'` und `'nein'`.""",
     given="antwort = 'JA'",
     solution="""antwort = 'JA'
if antwort.lower() == 'ja':
    print('Zustimmung')
else:
    print('Ablehnung')""")
task('Korrigiere die Schreibweise von `name` mit einer Methode und gib den Namen aus.',
     given="name = 'mAX mUSTERMANN'",
     solution="""name = 'mAX mUSTERMANN'
print(name.title())""")
task('Erzeuge aus `wort` eine Zeichenkette, bei der der erste Buchstabe klein und der Rest groß ist. Verwende Slicing. Gib sie aus.',
     given="wort = 'python'",
     solution="""wort = 'python'
print(wort[0].lower() + wort[1:].upper())""")
task('Erzeuge mit einer Schleife eine Zeichenkette, in der die Buchstaben von `wort` abwechselnd groß und klein sind, beginnend mit groß. Gib sie aus.',
     given="wort = 'informatik'",
     solution="""wort = 'informatik'
neu = ''
for i in range(len(wort)):
    if i % 2 == 0:
        neu += wort[i].upper()
    else:
        neu += wort[i].lower()
print(neu)""")
task('Speichere `text` in Großbuchstaben wieder in der Variablen `text`. Gib danach `text` aus.',
     given="text = 'achtung'",
     solution="""text = 'achtung'
text = text.upper()
print(text)""")
predict("""s = 'hallo Welt'
t = s.upper()
print(s)
print(t)
print(s.capitalize())
print(s.title())
print(s.swapcase())""")

# ---------------------------------------------------------------- 6
sec('Leerzeichen und Zeichen am Rand entfernen')
expl('''#### `strip()`, `lstrip()` und `rstrip()`

- `text.strip()` entfernt Leerzeichen (auch Tabulatoren und Zeilenumbrüche) am **Anfang und Ende**.
- `text.lstrip()` entfernt sie nur **links** (am Anfang), `text.rstrip()` nur **rechts** (am Ende).
- Gibt man Zeichen an, z. B. `text.strip('*')`, werden diese Zeichen statt der Leerzeichen entfernt.

Leerzeichen in der Mitte bleiben immer erhalten. In den Beispielen zeigen die Striche `|`, wo der Text anfängt und aufhört.''',
     """text = '   Hallo Welt   '
print('|' + text.strip() + '|')
print('|' + text.lstrip() + '|')
print('|' + text.rstrip() + '|')
print('**Wichtig**'.strip('*'))""")

EIN = "eingabe = '   Hallo Welt   '"
task('Entferne die Leerzeichen am Anfang und am Ende von `eingabe`. Gib das Ergebnis mit `|` davor und dahinter aus.',
     given=EIN, solution=EIN + """
print('|' + eingabe.strip() + '|')""")
task('Entferne nur die Leerzeichen am Anfang von `eingabe`. Gib das Ergebnis mit `|` davor und dahinter aus.',
     given=EIN, solution=EIN + """
print('|' + eingabe.lstrip() + '|')""")
task('Entferne nur die Leerzeichen am Ende von `eingabe`. Gib das Ergebnis mit `|` davor und dahinter aus.',
     given=EIN, solution=EIN + """
print('|' + eingabe.rstrip() + '|')""")
task('Entferne die Sternchen am Anfang und Ende von `text` und gib das Ergebnis aus.',
     given="text = '***Achtung***'",
     solution="""text = '***Achtung***'
print(text.strip('*'))""")
task('Entferne alle Ausrufezeichen und Punkte am Ende von `text` und gib das Ergebnis aus.',
     given="text = 'Hallo!!!...'",
     solution="""text = 'Hallo!!!...'
print(text.rstrip('!.'))""")
task("""Gib `Zustimmung` aus, wenn `antwort` nach dem Entfernen der Leerzeichen und in Kleinbuchstaben `ja` ist. Sonst gib `Ablehnung` aus.""",
     given="antwort = '  JA  '",
     solution="""antwort = '  JA  '
if antwort.strip().lower() == 'ja':
    print('Zustimmung')
else:
    print('Ablehnung')""")
task('Entferne die führenden Nullen von `nummer` und gib das Ergebnis aus.',
     given="nummer = '000420'",
     solution="""nummer = '000420'
print(nummer.lstrip('0'))""")
task('Vergleiche die Länge von `eingabe` vor und nach `strip()`. Gib aus, wie viele Zeichen entfernt wurden.',
     given=EIN, solution=EIN + """
print(len(eingabe) - len(eingabe.strip()))""")
predict("""s = '  ab  cd  '
print(len(s))
print(len(s.strip()))
print('|' + s.lstrip() + '|')
print('|' + s.rstrip() + '|')""")

# ---------------------------------------------------------------- 7
sec('Suchen und Zählen')
expl('''#### `find()` und `index()`

- `text.find(teil)` gibt den Index zurück, an dem `teil` **zum ersten Mal** vorkommt. Kommt `teil` nicht vor, ist das Ergebnis `-1`.
- `text.find(teil, start)` sucht erst ab dem Index `start`.
- `text.index(teil)` macht dasselbe wie `find()`, gibt aber einen `ValueError`, wenn `teil` nicht vorkommt.''',
     """satz = 'Ich mag Eis und Eis mag mich.'
print(satz.find('Eis'))
print(satz.find('Eis', 9))
print(satz.find('Kuchen'))
print(satz.index('mag'))""")
expl('''#### `count()`

`text.count(teil)` gibt zurück, **wie oft** `teil` in `text` vorkommt.''',
     """print('Banane'.count('a'))
print('Banane'.count('an'))""")
expl('''#### `startswith()` und `endswith()`

`text.startswith(teil)` prüft, ob `text` mit `teil` **beginnt**, `text.endswith(teil)`, ob er damit **endet**.
Das Ergebnis ist `True` oder `False`.''',
     """datei = 'bild.png'
print(datei.endswith('.png'))
print(datei.startswith('foto'))""")

SATZ = "satz = 'Der Hund bellt und der Hund rennt.'"
task("Gib mit `find()` aus, an welchem Index `'Hund'` in `satz` zum ersten Mal vorkommt.",
     given=SATZ, solution=SATZ + """
print(satz.find('Hund'))""")
task("Gib mit `find()` aus, an welchem Index `'Katze'` in `satz` vorkommt.",
     given=SATZ, solution=SATZ + """
print(satz.find('Katze'))""")
task("Gib aus, wie oft `'Hund'` in `satz` vorkommt.",
     given=SATZ, solution=SATZ + """
print(satz.count('Hund'))""")
task("Gib aus, wie oft der Buchstabe `'e'` in `satz` vorkommt.",
     given=SATZ, solution=SATZ + """
print(satz.count('e'))""")
task("Finde den Index des **zweiten** Vorkommens von `'Hund'` in `satz`. Verwende `find()` zweimal, beim zweiten Mal mit Startindex.",
     given=SATZ, solution=SATZ + """
erstes = satz.find('Hund')
zweites = satz.find('Hund', erstes + 1)
print(zweites)""")
task("""Gib `PDF-Datei` aus, wenn `dateiname` mit `'.pdf'` endet, sonst `keine PDF-Datei`.
Teste dein Programm auch mit `'bild.jpg'`.""",
     given="dateiname = 'bericht.pdf'",
     solution="""dateiname = 'bericht.pdf'
if dateiname.endswith('.pdf'):
    print('PDF-Datei')
else:
    print('keine PDF-Datei')""")
task("Gib `deutsche Nummer` aus, wenn `telefon` mit `'+49'` beginnt, sonst `ausländische Nummer`.",
     given="telefon = '+49 30 123456'",
     solution="""telefon = '+49 30 123456'
if telefon.startswith('+49'):
    print('deutsche Nummer')
else:
    print('ausländische Nummer')""")
task("Gib den Teil von `email` vor dem `'@'` und den Teil danach aus. Verwende `find()` und Slicing.",
     given="email = 'max.mustermann@schule.de'",
     solution="""email = 'max.mustermann@schule.de'
at = email.find('@')
print(email[:at])
print(email[at + 1:])""")
task("Zähle, wie viele Dateien in `dateien` mit `'.py'` enden. Gib die Anzahl aus.",
     given="dateien = ['spiel.py', 'notizen.txt', 'test.py', 'bild.png', 'main.py']",
     solution="""dateien = ['spiel.py', 'notizen.txt', 'test.py', 'bild.png', 'main.py']
anzahl = 0
for d in dateien:
    if d.endswith('.py'):
        anzahl += 1
print(anzahl)""")
task("Gib alles aus, was in `satz` nach dem ersten Komma steht, ohne das Leerzeichen am Anfang.",
     given="satz = 'Ja, ich komme morgen, vielleicht.'",
     solution="""satz = 'Ja, ich komme morgen, vielleicht.'
k = satz.find(',')
print(satz[k + 1:].strip())""")
task("Gib den Dateinamen ohne Endung aus, also alles vor dem letzten Punkt. Tipp: Die Endung hat hier immer 3 Buchstaben. Prüfe vorher mit `endswith()`, ob es eine `.txt`-Datei ist.",
     given="datei = 'aufsatz.txt'",
     solution="""datei = 'aufsatz.txt'
if datei.endswith('.txt'):
    print(datei[:-4])""")
predict("""s = 'Mississippi'
print(s.find('ss'))
print(s.find('ss', 3))
print(s.count('s'))
print(s.count('ss'))
print(s.find('x'))
print(s.startswith('miss'))""")
predict("""s = 'Hallo'
print(s.index('l'))
print(s.index('x'))""", error=ValueError)

# ---------------------------------------------------------------- 8
sec('Ersetzen')
expl('''#### `replace()`

`text.replace(alt, neu)` ersetzt **jedes** Vorkommen von `alt` durch `neu`.
Mit `text.replace(alt, neu, anzahl)` werden nur die ersten `anzahl` Vorkommen ersetzt.
Ersetzt man durch `''`, wird `alt` gelöscht.''',
     """text = 'Ich mag Katzen. Katzen sind toll.'
print(text.replace('Katzen', 'Hunde'))
print(text.replace('Katzen', 'Hunde', 1))
print('a-b-c'.replace('-', ''))""")

task("Ersetze in `satz` das Wort `'Katze'` durch `'Maus'` und gib den Satz aus.",
     given="satz = 'Die Katze schläft auf dem Sofa.'",
     solution="""satz = 'Die Katze schläft auf dem Sofa.'
print(satz.replace('Katze', 'Maus'))""")
task("Ersetze in `dateiname` alle Leerzeichen durch Unterstriche `_` und gib das Ergebnis aus.",
     given="dateiname = 'mein erstes Programm.py'",
     solution="""dateiname = 'mein erstes Programm.py'
print(dateiname.replace(' ', '_'))""")
task("Entferne mit `replace()` alle Leerzeichen aus `nummer` und gib das Ergebnis aus.",
     given="nummer = 'DE89 3704 0044 0532 0130 00'",
     solution="""nummer = 'DE89 3704 0044 0532 0130 00'
print(nummer.replace(' ', ''))""")
task("Ersetze nur das **erste** `'a'` in `wort` durch `'o'` und gib das Ergebnis aus.",
     given="wort = 'Banane'",
     solution="""wort = 'Banane'
print(wort.replace('a', 'o', 1))""")
task("Ersetze in `preis` das Komma durch einen Punkt, wandle das Ergebnis mit `float()` in eine Zahl um und gib den doppelten Preis aus.",
     given="preis = '3,75'",
     solution="""preis = '3,75'
print(float(preis.replace(',', '.')) * 2)""")
task("Ersetze in `text` ä, ö, ü und ß durch ae, oe, ue und ss. Verwende `replace()` mehrmals und gib das Ergebnis aus.",
     given="text = 'Grüße aus Köln, schön hier, Bär'",
     solution="""text = 'Grüße aus Köln, schön hier, Bär'
text = text.replace('ä', 'ae')
text = text.replace('ö', 'oe')
text = text.replace('ü', 'ue')
text = text.replace('ß', 'ss')
print(text)""")
task("Ersetze das Wort in `verboten` in `satz` durch genauso viele Sternchen, wie es Buchstaben hat. Verwende `len()` und `*`.",
     given="""satz = 'Das ist doof und nochmal doof.'
verboten = 'doof'""",
     solution="""satz = 'Das ist doof und nochmal doof.'
verboten = 'doof'
print(satz.replace(verboten, '*' * len(verboten)))""")
task("Wandle `datum` mit `replace()` in die Schreibweise `17.10.2026` um.",
     given="datum = '17/10/2026'",
     solution="""datum = '17/10/2026'
print(datum.replace('/', '.'))""")
task("In `text` stehen manchmal mehrere Leerzeichen hintereinander. Ersetze mit einer `while`-Schleife so lange zwei Leerzeichen durch eines, bis keine doppelten Leerzeichen mehr vorkommen. Gib den Text aus.",
     given="text = 'Das   ist    zu  viel   Platz.'",
     solution="""text = 'Das   ist    zu  viel   Platz.'
while '  ' in text:
    text = text.replace('  ', ' ')
print(text)""")
task("Tausche in `text` alle `'a'` und `'e'` gegeneinander aus. Verwende ein Hilfszeichen, z. B. `'#'`. Gib das Ergebnis aus.",
     given="text = 'Pelle Abend Ameise'",
     solution="""text = 'Pelle Abend Ameise'
text = text.replace('a', '#')
text = text.replace('e', 'a')
text = text.replace('#', 'e')
print(text)""")
predict("""s = 'banane'
t = s.replace('an', 'AN')
print(s)
print(t)
print(s.replace('a', '', 1))
print(s.replace('x', 'y'))""")

# ---------------------------------------------------------------- 9
sec('Zerlegen und zusammensetzen')
expl('''#### `split()`

`text.split()` zerlegt eine Zeichenkette an den Leerzeichen und gibt eine **Liste** der Teile zurück.
Mehrere Leerzeichen hintereinander zählen dabei wie eines.

Mit `text.split(trenner)` wird an einem anderen Zeichen zerlegt, z. B. `text.split(',')`.''',
     """satz = 'Ich  lerne Python'
print(satz.split())
print('Apfel,Birne,Kirsche'.split(','))""")
expl('''#### `join()`

`trenner.join(liste)` setzt die Zeichenketten einer Liste zu **einer** Zeichenkette zusammen.
Zwischen die Teile wird `trenner` gesetzt. Achtung: Die Methode gehört zum Trenner, nicht zur Liste.''',
     """woerter = ['Ich', 'lerne', 'Python']
print(' '.join(woerter))
print('-'.join(woerter))
print(''.join(woerter))""")

S9 = "satz = 'Python ist eine einfache Programmiersprache'"
task('Zerlege `satz` in seine Wörter und gib die Liste aus.',
     given=S9, solution=S9 + """
print(satz.split())""")
task('Gib aus, aus wie vielen Wörtern `satz` besteht.',
     given=S9, solution=S9 + """
print(len(satz.split()))""")
task('Zerlege `obst` an den Kommas und gib jede Obstsorte in einer eigenen Zeile aus.',
     given="obst = 'Apfel,Birne,Kirsche,Banane'",
     solution="""obst = 'Apfel,Birne,Kirsche,Banane'
for o in obst.split(','):
    print(o)""")
task('Zerlege `datum` an den Punkten. Gib Tag, Monat und Jahr aus wie unten.',
     given="datum = '17.10.2026'",
     solution="""datum = '17.10.2026'
teile = datum.split('.')
print('Tag:', teile[0])
print('Monat:', teile[1])
print('Jahr:', teile[2])""")
task('Setze die Wörter aus `woerter` mit `join()` zu einem Satz mit Leerzeichen zusammen. Gib ihn aus.',
     given="woerter = ['Heute', 'scheint', 'die', 'Sonne']",
     solution="""woerter = ['Heute', 'scheint', 'die', 'Sonne']
print(' '.join(woerter))""")
task("Setze die Elemente von `tage` mit `' - '` als Trenner zusammen und gib das Ergebnis aus.",
     given="tage = ['Mo', 'Di', 'Mi', 'Do', 'Fr']",
     solution="""tage = ['Mo', 'Di', 'Mi', 'Do', 'Fr']
print(' - '.join(tage))""")
task("Ersetze die Leerzeichen in `satz` durch Bindestriche. Verwende dafür `split()` und `join()`, nicht `replace()`.",
     given=S9, solution=S9 + """
print('-'.join(satz.split()))""")
task('Berechne die Summe der Zahlen in `zahlen_text`. Zerlege den Text und wandle jeden Teil mit `int()` um.',
     given="zahlen_text = '4 8 15 16 23 42'",
     solution="""zahlen_text = '4 8 15 16 23 42'
summe = 0
for t in zahlen_text.split():
    summe += int(t)
print(summe)""")
task('Gib das längste Wort von `satz` aus.',
     given=S9, solution=S9 + """
laengstes = ''
for w in satz.split():
    if len(w) > len(laengstes):
        laengstes = w
print(laengstes)""")
task('Kehre die Reihenfolge der Wörter in `satz` um. Verwende `split()`, `reverse()` und `join()`. Gib den neuen Satz aus.',
     given="satz = 'eins zwei drei vier'",
     solution="""satz = 'eins zwei drei vier'
woerter = satz.split()
woerter.reverse()
print(' '.join(woerter))""")
task('Bilde aus `name` die Initialen (die Anfangsbuchstaben aller Teile) und gib sie aus.',
     given="name = 'Max Peter Mustermann'",
     solution="""name = 'Max Peter Mustermann'
initialen = ''
for teil in name.split():
    initialen += teil[0]
print(initialen)""")
task("`zeile` enthält einen Namen, ein Alter und einen Ort, getrennt durch `;`. Zerlege die Zeile und gib den Satz unten aus.",
     given="zeile = 'Ali;16;Berlin'",
     solution="""zeile = 'Ali;16;Berlin'
teile = zeile.split(';')
print(f'{teile[0]} ist {teile[1]} Jahre alt und wohnt in {teile[2]}.')""")
predict("""s = 'a,b,,c'
teile = s.split(',')
print(teile)
print(len(teile))
print('+'.join(teile))
print('x y  z'.split())""")

# ---------------------------------------------------------------- 10
sec('Zeichenketten prüfen')
expl('''#### `isdigit()`, `isalpha()`, `isalnum()` und `isspace()`

Diese Methoden prüfen, ob **alle** Zeichen einer Zeichenkette eine Eigenschaft haben. Das Ergebnis ist `True` oder `False`.
Bei einer leeren Zeichenkette ist das Ergebnis immer `False`.

- `text.isdigit()`: nur Ziffern
- `text.isalpha()`: nur Buchstaben (auch ä, ö, ü, ß)
- `text.isalnum()`: nur Buchstaben und Ziffern
- `text.isspace()`: nur Leerzeichen (auch Tabulatoren und Zeilenumbrüche)''',
     """print('2026'.isdigit())
print('20.26'.isdigit())
print('Käse'.isalpha())
print('Raum204'.isalnum())
print('Raum 204'.isalnum())
print('   '.isspace())""")
expl('''#### `isupper()` und `islower()`

`text.isupper()` prüft, ob alle Buchstaben **groß** sind, `text.islower()`, ob alle Buchstaben **klein** sind.
Zeichen, die keine Buchstaben sind, werden dabei nicht beachtet.''',
     """print('ABC'.isupper())
print('USB-3'.isupper())
print('Abc'.isupper())
print('hallo welt'.islower())
print('A'.isupper(), 'a'.isupper())""")

task("""Wenn `eingabe` nur aus Ziffern besteht, wandle sie in eine Zahl um und gib die Zahl plus 1 aus.
Sonst gib `keine Zahl` aus. Teste dein Programm auch mit `'20a6'`.""",
     given="eingabe = '2026'",
     solution="""eingabe = '2026'
if eingabe.isdigit():
    print(int(eingabe) + 1)
else:
    print('keine Zahl')""")
task("Gib `gültiger Name` aus, wenn `name` nur aus Buchstaben besteht, sonst `ungültiger Name`. Teste auch mit `'Lena3'`.",
     given="name = 'Lena'",
     solution="""name = 'Lena'
if name.isalpha():
    print('gültiger Name')
else:
    print('ungültiger Name')""")
task('Zähle mit einer Schleife und `isupper()` die Großbuchstaben in `text`. Gib die Anzahl aus.',
     given="text = 'Heute Lernen Wir Python in der Schule'",
     solution="""text = 'Heute Lernen Wir Python in der Schule'
anzahl = 0
for c in text:
    if c.isupper():
        anzahl += 1
print(anzahl)""")
task('Zähle in `text` die Buchstaben, die Ziffern und die Leerzeichen. Gib die drei Anzahlen aus wie unten.',
     given="text = 'Raum 204 in Haus 7'",
     solution="""text = 'Raum 204 in Haus 7'
buchstaben = 0
ziffern = 0
leer = 0
for c in text:
    if c.isalpha():
        buchstaben += 1
    elif c.isdigit():
        ziffern += 1
    elif c.isspace():
        leer += 1
print('Buchstaben:', buchstaben)
print('Ziffern:', ziffern)
print('Leerzeichen:', leer)""")
task("""Ein Passwort ist sicher, wenn es mindestens 8 Zeichen lang ist, mindestens eine Ziffer und mindestens einen Großbuchstaben enthält.
Gib `sicher` oder `nicht sicher` aus. Teste auch mit `'sommer2026'` und `'Sommer'`.""",
     given="passwort = 'Sommer2026'",
     solution="""passwort = 'Sommer2026'
hat_ziffer = False
hat_gross = False
for c in passwort:
    if c.isdigit():
        hat_ziffer = True
    if c.isupper():
        hat_gross = True
if len(passwort) >= 8 and hat_ziffer and hat_gross:
    print('sicher')
else:
    print('nicht sicher')""")
task("Ein Benutzername darf nur Buchstaben und Ziffern enthalten. Gib `gültig` oder `ungültig` aus. Teste auch mit `'max_2010'`.",
     given="benutzer = 'max2010'",
     solution="""benutzer = 'max2010'
if benutzer.isalnum():
    print('gültig')
else:
    print('ungültig')""")
task('Erzeuge eine Zeichenkette, die nur die Ziffern aus `text` enthält, und gib sie aus.',
     given="text = 'Tel.: 030 / 12 34 56'",
     solution="""text = 'Tel.: 030 / 12 34 56'
ziffern = ''
for c in text:
    if c.isdigit():
        ziffern += c
print(ziffern)""")
task('Gib nur die Wörter aus `woerter` aus, die komplett in Großbuchstaben geschrieben sind.',
     given="woerter = ['USB', 'Maus', 'PC', 'Tastatur', 'RAM', 'cpu']",
     solution="""woerter = ['USB', 'Maus', 'PC', 'Tastatur', 'RAM', 'cpu']
for w in woerter:
    if w.isupper():
        print(w)""")
task("Prüfe, ob `kennung` genau 6 Zeichen hat, mit zwei Buchstaben beginnt und mit vier Ziffern endet. Gib `ok` oder `falsch` aus. Teste auch mit `'A12345'`.",
     given="kennung = 'AB1234'",
     solution="""kennung = 'AB1234'
if len(kennung) == 6 and kennung[:2].isalpha() and kennung[2:].isdigit():
    print('ok')
else:
    print('falsch')""")
predict("""print('abc'.isalpha())
print('abc1'.isalpha())
print('abc1'.isalnum())
print('12.5'.isdigit())
print('   '.isspace())
print(''.isdigit())
print('Hallo'.islower())""")

# ---------------------------------------------------------------- 11
sec('Formatieren')
expl('''#### Formatangaben in f-Strings

Hinter einem Doppelpunkt in den geschweiften Klammern kann man angeben, **wie** ein Wert geschrieben werden soll:

| Angabe | Bedeutung | Beispiel |
|---|---|---|
| `{x:.2f}` | Kommazahl mit 2 Nachkommastellen | `3.50` |
| `{x:03d}` | ganze Zahl mit mindestens 3 Stellen, vorne mit Nullen aufgefüllt | `007` |
| `{s:<10}` | linksbündig in 10 Zeichen Breite | `Hallo     ` |
| `{s:>10}` | rechtsbündig in 10 Zeichen Breite | `     Hallo` |
| `{s:^10}` | zentriert in 10 Zeichen Breite | `  Hallo   ` |''',
     """preis = 3.5
nummer = 7
wort = 'Hallo'
print(f'{preis:.2f}')
print(f'{nummer:03d}')
print(f'|{wort:<10}|')
print(f'|{wort:>10}|')
print(f'|{wort:^10}|')""")
expl('''#### `ljust()`, `rjust()`, `center()` und `zfill()`

- `text.ljust(n)`, `text.rjust(n)` und `text.center(n)` füllen den Text mit Leerzeichen auf `n` Zeichen auf:
  links-, rechtsbündig oder zentriert. Mit einem zweiten Argument füllt man mit einem anderen Zeichen auf, z. B. `text.center(20, '*')`.
- `text.zfill(n)` füllt vorne mit Nullen auf `n` Zeichen auf.''',
     """wort = 'Hallo'
print('|' + wort.ljust(10) + '|')
print('|' + wort.rjust(10) + '|')
print('|' + wort.center(11) + '|')
print(wort.center(15, '*'))
print('42'.zfill(5))""")

task('Gib den Preis mit zwei Nachkommastellen aus wie unten.',
     given='preis = 3.5',
     solution="""preis = 3.5
print(f'Preis: {preis:.2f} Euro')""")
task('Gib `pi` mit drei Nachkommastellen aus.',
     given='pi = 3.14159265',
     solution="""pi = 3.14159265
print(f'{pi:.3f}')""")
task('Berechne den Durchschnitt der Noten und gib ihn mit zwei Nachkommastellen aus wie unten.',
     given='noten = [2, 3, 1, 2, 4, 2]',
     solution="""noten = [2, 3, 1, 2, 4, 2]
schnitt = sum(noten) / len(noten)
print(f'Durchschnitt: {schnitt:.2f}')""")
task('Gib `nummer` dreistellig mit führenden Nullen aus. Verwende `str()` und `zfill()`.',
     given='nummer = 7',
     solution="""nummer = 7
print(str(nummer).zfill(3))""")
task('Gib `wort` zentriert in einer Breite von 20 Zeichen aus. Fülle mit Sternchen auf.',
     given="wort = 'Python'",
     solution="""wort = 'Python'
print(wort.center(20, '*'))""")
task('Gib die Uhrzeit im Format unten aus. Stunde und Minute sollen immer zweistellig sein.',
     given="""stunde = 9
minute = 5""",
     solution="""stunde = 9
minute = 5
print(f'{stunde:02d}:{minute:02d}')""")
task('Gib jede Zahl aus `zahlen` rechtsbündig in einer Breite von 5 Zeichen zwischen zwei `|` aus. Verwende `rjust()`.',
     given='zahlen = [5, 123, 42, 7]',
     solution="""zahlen = [5, 123, 42, 7]
for z in zahlen:
    print('|' + str(z).rjust(5) + '|')""")
task('Gib die Tabelle unten aus. Die Produktnamen stehen linksbündig in 10 Zeichen Breite, die Preise rechtsbündig in 6 Zeichen mit zwei Nachkommastellen. Verwende einen f-String.',
     given="""produkte = ['Milch', 'Brot', 'Käse']
preise = [1.2, 2.5, 4.99]""",
     solution="""produkte = ['Milch', 'Brot', 'Käse']
preise = [1.2, 2.5, 4.99]
for i in range(len(produkte)):
    print(f'{produkte[i]:<10}{preise[i]:>6.2f}')""")
task('Gib den Titel wie unten in einem Rahmen aus: Linien aus 20 Gleichheitszeichen, dazwischen der Titel zentriert in 20 Zeichen Breite.',
     given="titel = 'Menü'",
     solution="""titel = 'Menü'
print('=' * 20)
print(titel.center(20))
print('=' * 20)""")
task('Gib für die Zahlen von 1 bis 5 die Zahl, ihr Quadrat und ihre Kubikzahl als Tabelle aus wie unten. Jede Spalte ist 5 Zeichen breit und rechtsbündig.',
     solution="""for i in range(1, 6):
    print(f'{i:>5}{i * i:>5}{i * i * i:>5}')""")
predict("""x = 2 / 3
print(f'{x:.2f}')
print(f'|{"ab":>5}|')
print(f'|{"ab":<5}|')
print(f'|{"ab":^6}|')
print('5'.zfill(3))""")

# ---------------------------------------------------------------- 12
sec('Gemischte Übungen')
task("""Prüfe, ob `wort` ein Palindrom ist, also vorwärts und rückwärts gelesen gleich, ohne Beachtung von Groß- und Kleinschreibung.
Gib `Palindrom` oder `kein Palindrom` aus. Teste auch mit `'Python'`.""",
     given="wort = 'Rentner'",
     solution="""wort = 'Rentner'
w = wort.lower()
rueckwaerts = ''
for c in w:
    rueckwaerts = c + rueckwaerts
if w == rueckwaerts:
    print('Palindrom')
else:
    print('kein Palindrom')""")
task('Zähle, wie viele Wörter in `satz` mehr als 4 Buchstaben haben. Gib die Anzahl aus.',
     given="satz = 'Am Morgen fliegt der kleine Vogel über das grüne Feld'",
     solution="""satz = 'Am Morgen fliegt der kleine Vogel über das grüne Feld'
anzahl = 0
for w in satz.split():
    if len(w) > 4:
        anzahl += 1
print(anzahl)""")
task('Bereinige `name`: Leerzeichen am Rand entfernen und jedes Wort mit einem Großbuchstaben beginnen lassen. Gib das Ergebnis mit `|` davor und dahinter aus.',
     given="name = '   max MUSTERMANN  '",
     solution="""name = '   max MUSTERMANN  '
print('|' + name.strip().title() + '|')""")
task('Erzeuge einen Benutzernamen aus dem ersten Buchstaben von `vorname` und dem ganzen `nachname`, alles in Kleinbuchstaben. Gib ihn aus.',
     given="""vorname = 'Max'
nachname = 'Mustermann'""",
     solution="""vorname = 'Max'
nachname = 'Mustermann'
print((vorname[0] + nachname).lower())""")
task('Bilde aus `begriff` die Abkürzung aus den Anfangsbuchstaben der Wörter, in Großbuchstaben. Gib sie aus.',
     given="begriff = 'portable document format'",
     solution="""begriff = 'portable document format'
abk = ''
for w in begriff.split():
    abk += w[0].upper()
print(abk)""")
task("Ersetze mit einer Schleife jeden Vokal (a, e, i, o, u, auch groß) in `text` durch `'*'`. Gib das Ergebnis aus.",
     given="text = 'Ein Apfel am Tag'",
     solution="""text = 'Ein Apfel am Tag'
neu = ''
for c in text:
    if c.lower() in 'aeiou':
        neu += '*'
    else:
        neu += c
print(neu)""")
task("Gib für jeden Vokal aus, wie oft er in `satz` vorkommt. Groß- und Kleinschreibung sollen keine Rolle spielen. Verwende eine Schleife über `'aeiou'`, `lower()` und `count()`.",
     given="satz = 'Ein Elefant isst Orangen und Ananas'",
     solution="""satz = 'Ein Elefant isst Orangen und Ananas'
for v in 'aeiou':
    print(v, satz.lower().count(v))""")
task("""Ein Satz ist korrekt, wenn er mit einem Großbuchstaben beginnt und mit einem Punkt endet.
Gib `korrekt` oder `nicht korrekt` aus. Teste auch mit `'heute regnet es.'` und `'Heute regnet es'`.""",
     given="satz = 'Heute regnet es.'",
     solution="""satz = 'Heute regnet es.'
if satz[0].isupper() and satz.endswith('.'):
    print('korrekt')
else:
    print('nicht korrekt')""")
task('Wandle `datum` von der Form Jahr-Monat-Tag in die Form Tag.Monat.Jahr um. Verwende `split()`. Gib das Ergebnis aus.',
     given="datum = '2026-10-17'",
     solution="""datum = '2026-10-17'
teile = datum.split('-')
print(f'{teile[2]}.{teile[1]}.{teile[0]}')""")
task('Drehe jedes Wort in `satz` einzeln um. Die Reihenfolge der Wörter bleibt gleich. Gib den neuen Satz aus.',
     given="satz = 'Hallo schöne Welt'",
     solution="""satz = 'Hallo schöne Welt'
neue_woerter = []
for w in satz.split():
    rueckwaerts = ''
    for c in w:
        rueckwaerts = c + rueckwaerts
    neue_woerter.append(rueckwaerts)
print(' '.join(neue_woerter))""")
task('Verdecke alle Ziffern von `karte` außer den letzten vier mit Sternchen. Verwende `len()`, `*` und Slicing.',
     given="karte = '1234567812345678'",
     solution="""karte = '1234567812345678'
print('*' * (len(karte) - 4) + karte[-4:])""")
task("Zähle, wie oft das Wort `'die'` in `satz` vorkommt, egal ob groß oder klein geschrieben. Zerlege dazu den Satz in Wörter, damit z. B. `'Dieb'` nicht mitzählt.",
     given="satz = 'Die Katze und die Maus jagen den Dieb, die Polizei auch'",
     solution="""satz = 'Die Katze und die Maus jagen den Dieb, die Polizei auch'
woerter = satz.lower().split()
print(woerter.count('die'))""")
task('Gib jedes Wort aus `satz` in Großbuchstaben mit seiner Länge aus wie unten.',
     given="satz = 'Ich mag Pizza'",
     solution="""satz = 'Ich mag Pizza'
for w in satz.split():
    print(f'{w.upper()}: {len(w)}')""")
task("Prüfe, ob `wort` jeden Vokal (a, e, i, o, u) mindestens einmal enthält. Gib `alle Vokale` oder `nicht alle Vokale` aus. Teste auch mit `'Banane'`.",
     given="wort = 'Aufsichtsratsvorsitzender'",
     solution="""wort = 'Aufsichtsratsvorsitzender'
alle = True
for v in 'aeiou':
    if v not in wort.lower():
        alle = False
if alle:
    print('alle Vokale')
else:
    print('nicht alle Vokale')""")
task("Kürze `text` auf höchstens 20 Zeichen. Ist der Text länger, sollen die ersten 17 Zeichen und `'...'` ausgegeben werden. Teste auch mit `'Kurzer Text'`.",
     given="text = 'Dies ist ein ziemlich langer Satz.'",
     solution="""text = 'Dies ist ein ziemlich langer Satz.'
if len(text) > 20:
    print(text[:17] + '...')
else:
    print(text)""")
predict("""s = '  Python ist Toll  '
t = s.strip().lower().split()
print(t)
print('_'.join(t).upper())
print(s.count(' '))""")

generate('strings', 'Strings')
