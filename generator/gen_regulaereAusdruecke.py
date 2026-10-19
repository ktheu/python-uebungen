# Erzeugt ../content/regulaereAusdruecke.ipynb (siehe nbgen.py).
#
# Alle Muster stehen als Raw-Strings r'...' im Code, sonst gibt es ab Python 3.12 Warnungen wegen \d usw.
# Prüfen am besten mit:  py -3.13 -W error generator/gen_regulaereAusdruecke.py
# (macht ungültige Escape-Sequenzen und veraltete Aufrufe wie re.sub(..., 1) zu Fehlern)
from nbgen import sec, expl, task, predict, generate


def t(text, given='', body='', kind='normal'):
    """Aufgabe, deren Lösung aus dem vorgegebenen Code plus body besteht."""
    task(text, given=given, solution=(given + '\n' + body) if given else body, kind=kind)


TEST = """for text in texte:
    print(text, bool(re.search(muster, text)))"""
FULL = """for text in texte:
    print(text, bool(re.fullmatch(muster, text)))"""
NUR = """for text in texte:
    if re.search(muster, text):
        print(text)"""


def tm(text, texte, muster, schleife=TEST):
    """Aufgabe: ein Muster schreiben und mit einer Schleife an den vorgegebenen Texten prüfen."""
    q = '"' if "'" in muster else "'"
    t(text, 'import re\ntexte = ' + texte, f'muster = r{q}{muster}{q}\n' + schleife)


INTRO = '''Ein **regulärer Ausdruck** (englisch *regular expression*, kurz *Regex*) ist ein **Suchmuster** für Zeichenketten.
Damit kann man prüfen, ob ein Text eine bestimmte Form hat (zum Beispiel eine Postleitzahl oder eine Uhrzeit),
Teile aus einem Text herausholen, ersetzen oder den Text zerlegen.
Reguläre Ausdrücke sind sehr mächtig, aber anfangs schwer zu lesen: eine Art „kompaktes Programmieren mit Zeichen“.

Jeder Abschnitt beginnt mit kurzen Erklärungen und Beispielen. Führe die Beispiele aus und probiere sie ruhig ein wenig aus.
Danach folgen viele kleine Übungen. Wenn etwas vorgegeben ist, steht es schon in der Codezelle.

Videos zum Thema: [Playlist reguläre Ausdrücke](https://www.youtube.com/playlist?list=PLWeMgMhRDsIFk8RPO6C3DzcQfBf8mTGn7).
Muster ausprobieren kannst du auch auf [regex101.com](https://regex101.com) (links *Python* einstellen).'''

# ---------------------------------------------------------------- 1
sec('Suchen mit re.search()')
expl('''#### Das Modul `re` und `re.search()`

Die Funktionen für reguläre Ausdrücke stehen im Modul `re`. Man importiert es mit `import re`.

`re.search(muster, text)` sucht das Muster **irgendwo** im Text.

- Findet es eine passende Stelle, gibt es ein **Match-Objekt** zurück (englisch *match* = Treffer).
- Findet es nichts, gibt es `None` zurück („nichts“).
- Ein Treffer liegt auch dann vor, wenn nur ein **Teil** des Textes zum Muster passt.
- Groß- und Kleinschreibung werden unterschieden.

Die einfachsten Muster bestehen nur aus normalen Buchstaben. Sie passen genau auf diese Buchstabenfolge.''',
     r"""import re

print(re.search('aus', 'Haus'))
print(re.search('aus', 'Hut'))
print(re.search('aus', 'AUS'))""")
expl('''#### Treffer prüfen mit `bool()` und `if`

`bool(re.search(muster, text))` ergibt `True`, wenn es einen Treffer gibt, sonst `False`.

In einer `if`-Bedingung kann man das Ergebnis von `re.search()` direkt verwenden:
Ein Match-Objekt zählt als wahr, `None` als falsch.''',
     r"""import re

print(bool(re.search('aus', 'Haus')))
print(bool(re.search('aus', 'Hut')))
if re.search('Hund', 'Der Hund bellt.'):
    print('Hund gefunden')
if not re.search('Katze', 'Der Hund bellt.'):
    print('keine Katze')""")
expl('''#### Die Testschleife

Um ein Muster an mehreren Texten auszuprobieren, verwenden wir in vielen Aufgaben diese Schleife.
Sie gibt jeden Text aus und dahinter, ob das Muster darin vorkommt.
Das Muster steht in der Variablen `muster`. Das `r` davor erklären wir im nächsten Abschnitt.''',
     r"""import re

texte = ['Haus', 'Maus', 'Hut', 'Ausflug', 'raus']
muster = r'aus'
for text in texte:
    print(text, bool(re.search(muster, text)))""")
expl('''#### Was wurde gefunden? `group()`, `start()`, `end()` und `span()`

`re.search()` liefert nur den **ersten** Treffer. Das Match-Objekt `m` weiß, was und wo gefunden wurde:

| Methode | Ergebnis |
|---|---|
| `m.group()` | der gefundene Text |
| `m.start()` | Index des ersten Zeichens des Treffers |
| `m.end()` | Index **hinter** dem letzten Zeichen (wie beim Slicing) |
| `m.span()` | das Tupel `(start, end)` |

Ist das Ergebnis `None`, gibt es diese Methoden nicht. Dann entsteht ein `AttributeError`.
Deshalb prüft man vorher mit `if m:`.''',
     r"""import re

text = 'Hund und Katze'
m = re.search('und', text)
print(m.group())
print(m.start(), m.end())
print(m.span())
print(text[m.start():m.end()])""")

t('Prüfe mit `re.search()` und `bool()`, ob in `satz` das Wort `Python` vorkommt. Gib das Ergebnis aus.',
  "import re\nsatz = 'Ich lerne Python.'",
  "print(bool(re.search('Python', satz)))")
tm("Prüfe mit der Testschleife, welche Texte `ei` enthalten.",
   "['Eis', 'Brei', 'Seil', 'Bein', 'Ast']", 'ei')
tm("Gib mit einer Schleife und `if` nur die Texte aus, die `en` enthalten.",
   "['lernen', 'Hund', 'Ente', 'Tenne', 'Ball']", 'en', NUR)
t('Gib den Startindex und den Endindex des **ersten** Treffers von `Ball` in `satz` aus.',
  "import re\nsatz = 'Der Ball rollt zum Ballspieler.'",
  """m = re.search('Ball', satz)
print(m.start(), m.end())""")
t("""Suche `x` in `wort`. Gib `gefunden an Position ...` aus, wenn es vorkommt, sonst `nicht gefunden`.
Teste auch mit `wort = 'Tag'`.""",
  "import re\nwort = 'Taxi'",
  """m = re.search('x', wort)
if m:
    print('gefunden an Position', m.start())
else:
    print('nicht gefunden')""")
t('Zähle mit einer Schleife, wie viele Wörter in `woerter` die Buchstabenfolge `ch` enthalten. Gib die Anzahl aus.',
  "import re\nwoerter = ['ich', 'Buch', 'Haus', 'Chor', 'lachen', 'Tisch', 'Ball']",
  """anzahl = 0
for wort in woerter:
    if re.search('ch', wort):
        anzahl += 1
print(anzahl)""")
t('''Suche `und` in `satz`. Gib mit Slicing, `m.start()` und `m.end()` den Text **vor** und den Text **nach** dem Treffer aus,
jeweils in eckigen Klammern wie unten.''',
  "import re\nsatz = 'Heute ist Montag und morgen ist Dienstag.'",
  """m = re.search('und', satz)
print(f'[{satz[:m.start()]}]')
print(f'[{satz[m.end():]}]')""")
t('Gib mit `m.span()` die Position des ersten Treffers von `ana` in `wort` aus.',
  "import re\nwort = 'Bananenschale'",
  """m = re.search('ana', wort)
print(m.span())""")
predict(r"""import re
print(re.search('a', 'Banane').span())
print(re.search('na', 'Banane').group())
print(bool(re.search('B', 'banane')))
print(re.search('x', 'abc'))""")
predict(r"""import re
m = re.search('z', 'Haus')
print(m)
print(m.group())""", error=AttributeError)

# ---------------------------------------------------------------- 2
sec('Der Punkt, Sonderzeichen und Raw-Strings')
expl('''#### Der Punkt `.`

Im Muster steht der Punkt `.` für **genau ein beliebiges Zeichen** (Buchstabe, Ziffer, Leerzeichen, Satzzeichen, ...).
Nur einen Zeilenumbruch `\\n` erfasst er nicht.

`.a` passt also auf „irgendein Zeichen, danach ein `a`“.''',
     r"""import re

texte = ['ba', 'bb', 'cca', 'a', 'Xa', ' a']
for text in texte:
    print(text, bool(re.search('.a', text)))""")
expl(r'''#### Sonderzeichen escapen

Einige Zeichen haben in regulären Ausdrücken eine besondere Bedeutung. Du lernst sie in den nächsten Abschnitten kennen:

`.` `^` `$` `*` `+` `?` `{` `}` `[` `]` `\` `|` `(` `)`

Will man so ein Zeichen **wörtlich** suchen, schreibt man einen Backslash davor: `\.` passt nur auf einen Punkt,
`\?` auf ein Fragezeichen, `\(` auf eine runde Klammer und `\\` auf einen Backslash.''',
     r"""import re

texte = ['ccb.a', 'ccb.ad', 'bab', 'b.a?c']
muster = r'b\.a.'
for text in texte:
    print(text, bool(re.search(muster, text)))""")
expl(r'''#### Raw-Strings `r'...'`

Auch Python selbst benutzt den Backslash in Zeichenketten, zum Beispiel ist `'\n'` ein Zeilenumbruch und `'\b'` ein
Steuerzeichen (*backspace*). Damit Python den Backslash unverändert an das Modul `re` weitergibt, schreibt man vor das
Muster ein `r`. Das ist ein **Raw-String** (englisch *raw* = roh): Darin ist `\` ein ganz normales Zeichen.

**Schreibe Muster immer als Raw-String**, also `r'...'`. Ohne `r` meldet Python bei Mustern wie `'\d'` eine Warnung,
und bei `'\b'` funktioniert das Muster nicht.''',
     r"""print(len('a\nb'), len(r'a\nb'))
print('C:\neu')
print(r'C:\neu')""")

tm("Schreibe ein Muster für: `H`, ein beliebiges Zeichen, `nd`. Prüfe es mit der Testschleife.",
   "['Hand', 'Hund', 'Hemd', 'Hnd', 'Hindernis']", 'H.nd')
tm("Schreibe ein Muster für: `b`, zwei beliebige Zeichen, `t`. Prüfe es mit der Testschleife.",
   "['bist', 'beet', 'bot', 'bunt', 'Brot']", 'b..t')
tm("""Gib nur die Texte aus, die `.de` enthalten (mit einem echten Punkt).
Ohne Backslash würden auch `code` und `xde.com` passen.""",
   "['schule.de', 'web.de', 'code', 'gmx.net', 'xde.com']", r'\.de', NUR)
tm("Gib nur die Sätze aus, die ein Fragezeichen enthalten.",
   "['Wie geht es dir?', 'Gut.', 'Echt?', 'Ja!']", r'\?', NUR)
tm("Prüfe mit der Testschleife, welche Texte `(1)` enthalten (mit Klammern).",
   "['Punkt (1)', 'Punkt 1', 'Punkt (2)', '(1) Anfang']", r'\(1\)')
tm("Prüfe mit der Testschleife, welche Texte den Preis `3.50` mit einem echten Punkt enthalten.",
   "['3.50 Euro', '3,50 Euro', '3550 Euro', '13.50 Euro']", r'3\.50')
t("Suche in `satz` nach `B`, zwei beliebigen Zeichen und `n`. Gib den gefundenen Text aus. Suche danach genauso nach `B..m`.",
  "import re\nsatz = 'Am Bahnhof steht ein Baum.'",
  """print(re.search(r'B..n', satz).group())
print(re.search(r'B..m', satz).group())""")
tm("Gib nur die Pfade aus, die einen Backslash enthalten.",
   r"[r'C:\Daten', 'C:/Daten', r'D:\Bilder', 'home/anna']", r'\\', NUR)
tm("Gib nur die Texte aus, die einen Stern `*` enthalten.",
   "['3 * 4', '3 x 4', '**fett**', 'a+b']", r'\*', NUR)
predict(r"""import re
print(len(r'\n'), len('\n'))
print(bool(re.search(r'.', '')))
print(bool(re.search(r'...', 'ab')))
print(re.search(r'\.', 'a.b.c').start())
print(re.search(r'a.c', 'abc a.c').group())""")

# ---------------------------------------------------------------- 3
sec('Zeichenklassen')
expl('''#### Zeichenklassen `[...]`

In eckigen Klammern gibt man an, welche Zeichen an **einer** Stelle erlaubt sind.

| Muster | passt auf |
|---|---|
| `[aeiou]` | einen der Buchstaben a, e, i, o, u |
| `[0-5]` | eine Ziffer von 0 bis 5 |
| `[a-z]` | einen Kleinbuchstaben von a bis z (ohne ä, ö, ü, ß) |
| `[a-zA-Z0-9]` | einen englischen Buchstaben oder eine Ziffer |
| `[a-zäöüß]` | einen deutschen Kleinbuchstaben |

Ein Bereich wie `a-z` wird mit einem Bindestrich geschrieben.''',
     r"""import re

texte = ['Hund', 'Hand', 'Hind', 'Hemd']
for text in texte:
    print(text, bool(re.search(r'H[au]nd', text)))
print(re.search(r'[0-9]', 'Raum B12').group())
print(re.search(r'[A-Z]', 'ein Satz mit Großbuchstaben').group())""")
expl('''#### Verneinte Zeichenklassen `[^...]` und Sonderzeichen in Klassen

- Steht `^` **direkt** nach `[`, passt die Klasse auf jedes Zeichen, das **nicht** darin steht: `[^0-9]` ist „keine Ziffer“.
- In eckigen Klammern verlieren die meisten Sonderzeichen ihre Bedeutung: `[.?*]` passt auf einen Punkt, ein Fragezeichen oder einen Stern.
- Ein Bindestrich ganz am Anfang oder am Ende der Klasse ist ein normales Zeichen: `[-+]` passt auf Minus oder Plus.''',
     r"""import re

print(re.search(r'[^0-9]', '123x45').group())
print(re.search(r'[^aeiou]', 'aua!').group())
print(bool(re.search(r'[.,]', '3,5')))
print(re.search(r'[-+]', 'a+b-c').group())""")

tm("Schreibe ein Muster, das auf `Maier` und `Meier` passt. Prüfe es mit der Testschleife.",
   "['Maier', 'Meier', 'Mayer', 'Meyer', 'Mier']", r'M[ae]ier')
tm("Schreibe ein Muster, das auf `Maier`, `Meier`, `Mayer` und `Meyer` passt.",
   "['Maier', 'Meier', 'Mayer', 'Meyer', 'Moier']", r'M[ae][iy]er')
tm("Gib nur die Texte aus, die eine Ziffer enthalten.",
   "['Raum 12', 'Aula', 'B2', 'Turnhalle', '3. Stock']", r'[0-9]', NUR)
t('Gib den ersten Großbuchstaben (A bis Z) in `satz` aus.',
  "import re\nsatz = 'das ist ein kleiner Satz mit Großbuchstaben'",
  "print(re.search(r'[A-Z]', satz).group())")
tm("""Eine kurze Farbangabe besteht aus `#` und drei Hexadezimalziffern (`0`-`9`, `a`-`f`, `A`-`F`).
Schreibe ein Muster dafür und prüfe es.""",
   "['#fff', '#A0c', '#xyz', 'fff', '#12G']", r'#[0-9a-fA-F][0-9a-fA-F][0-9a-fA-F]')
tm("Gib nur die Texte aus, die mindestens ein Zeichen enthalten, das **keine** Ziffer ist.",
   "['12345', '12a45', '0815', '3.14', '']", r'[^0-9]', NUR)
tm("Prüfe, welche Wörter zwei Vokale (a, e, i, o, u) direkt hintereinander enthalten.",
   "['Boot', 'Haus', 'Bett', 'Seele', 'Kind']", r'[aeiou][aeiou]')
t('''Suche in jedem Text nach „Ziffer, Punkt oder Komma, Ziffer“. Gib den Treffer aus oder `kein Treffer`, wenn es keinen gibt.''',
  "import re\ntexte = ['Preis 3,5', 'Note 2.7', 'Seite 12', 'a.b']",
  """for text in texte:
    m = re.search(r'[0-9][.,][0-9]', text)
    if m:
        print(m.group())
    else:
        print('kein Treffer')""")
tm("Gib nur die Wörter aus, die einen Umlaut (klein oder groß) oder ein `ß` enthalten.",
   "['Käse', 'Brot', 'Öl', 'Fuß', 'Müsli', 'Ei']", r'[äöüßÄÖÜ]', NUR)
tm("Prüfe, welche Texte einen Großbuchstaben direkt gefolgt von einer Ziffer enthalten.",
   "['B12', 'b12', 'Raum A3', 'A-3', 'XY9']", r'[A-Z][0-9]')
predict(r"""import re
print(re.search(r'[abc]', 'xyzcba').group())
print(re.search(r'[^abc]', 'abcabcd').group())
print(bool(re.search(r'[A-Z][a-z]', 'aBC')))
print(re.search(r'[.]', 'a.b').start())
print(re.search(r'[0-9][0-9]', 'a1b23c').group())""")

# ---------------------------------------------------------------- 4
sec('Vordefinierte Zeichenklassen')
expl(r'''#### `\d`, `\w`, `\s` und ihre Gegenteile

Für häufige Zeichenklassen gibt es Abkürzungen:

| Muster | passt auf |
|---|---|
| `\d` | eine Ziffer, wie `[0-9]` (englisch *digit*) |
| `\w` | ein Wortzeichen: Buchstabe (auch ä, ö, ü, ß und Buchstaben anderer Sprachen), Ziffer oder Unterstrich `_` |
| `\s` | Leerraum (*whitespace*): Leerzeichen, Tabulator `\t` oder Zeilenumbruch `\n` |
| `\D` | alles außer Ziffern |
| `\W` | alles außer Wortzeichen, z. B. Leerzeichen und Satzzeichen |
| `\S` | alles außer Leerraum |

Die Abkürzungen kann man auch in eckigen Klammern verwenden: `[\d.]` ist „Ziffer oder Punkt“.''',
     r"""import re

texte = ['4ab9', '0ab1', '6ab9', '0bb5']
muster = r'[0-5]ab\d'
for text in texte:
    print(text, bool(re.search(muster, text)))

print(re.search(r'\w\w', '!!Öl!!').group())
print(re.search(r'\s', 'ab cd').start())
print(re.search(r'\W', 'Hallo, Welt').group())""")

tm(r"Prüfe mit `\d`, welche Texte zwei Ziffern direkt hintereinander enthalten.",
   "['7', '42', 'a1b2', 'Bus 101', 'x9']", r'\d\d')
t(r'Gib mit `\s` aus, an welcher Position in `satz` das erste Leerraum-Zeichen steht.',
  "import re\nsatz = 'Python\\tist toll'",
  r"print(re.search(r'\s', satz).start())")
t(r'Suche in `satz` eine Uhrzeit der Form „zwei Ziffern, Doppelpunkt, zwei Ziffern“ und gib sie aus.',
  "import re\nsatz = 'Treffpunkt um 14:30 am Kino.'",
  r"print(re.search(r'\d\d:\d\d', satz).group())")
tm(r"Schreibe mit `\d` und `\.` ein Muster für ein Datum wie `01.02.2024` (immer zwei Ziffern für Tag und Monat, vier für das Jahr).",
   "['01.02.2024', '1.2.2024', '31.12.1999', '12-05-2020']", r'\d\d\.\d\d\.\d\d\d\d')
tm(r"Gib nur die Texte aus, die ein Zeichen enthalten, das weder ein Wortzeichen noch Leerraum ist. Tipp: `[^\w\s]`.",
   "['Hallo Welt', 'Hallo!', 'a_b', 'x-y', 'Größe 12']", r'[^\w\s]', NUR)
tm("Prüfe, welche Texte ein Wortzeichen, ein Leerzeichen und eine Ziffer direkt hintereinander enthalten.",
   "['Raum 4', 'Raum4', 'Seite 12', '1 2']", r'\w\s\d')
tm(r"Gib nur die Texte aus, die **keine** Ziffer enthalten. Verwende `if not ...`.",
   "['Haus', 'Haus 2', 'B52', 'Garten']", r'\d', """for text in texte:
    if not re.search(muster, text):
        print(text)""")
tm(r"Prüfe, welche Texte eine Ziffer direkt gefolgt von etwas enthalten, das keine Ziffer ist. Verwende `\d` und `\D`.",
   "['123', '12a', 'a12', '1 2']", r'\d\D')
t('Gib das erste Zeichen von `text` aus, das kein Leerraum ist, und seine Position.',
  "import re\ntext = '   \\t  Hallo'",
  r"""m = re.search(r'\S', text)
print(m.group(), m.start())""")
predict(r"""import re
print(bool(re.search(r'\d', 'zwei')))
print(re.search(r'\w', '  _x').group())
print(re.search(r'\S', '   ab').start())
print(re.search(r'\D\d', '12a34').group())
print(bool(re.search(r'\w', 'ß')))""")

# ---------------------------------------------------------------- 5
sec('Quantoren')
expl(r'''#### Wie oft? Quantoren

Ein **Quantor** gibt an, wie oft das Zeichen (oder die Zeichenklasse) **direkt davor** vorkommen darf.

| Quantor | Bedeutung |
|---|---|
| `?` | null- oder einmal (also: optional) |
| `*` | beliebig oft, auch null-mal |
| `+` | mindestens einmal |
| `{k}` | genau k-mal |
| `{k,}` | mindestens k-mal |
| `{,k}` | höchstens k-mal (auch null-mal) |
| `{k,l}` | zwischen k- und l-mal |

In den geschweiften Klammern darf **kein Leerzeichen** stehen: `{2,4}`, nicht `{2, 4}`.

`\d+` ist also „eine oder mehrere Ziffern“, `colou?r` passt auf `color` und `colour`.''',
     r"""import re

print(re.search(r'\d+', 'Raum 1204 B').group())
print(re.search(r'ab*c', 'xacx').group())
print(re.search(r'ab*c', 'xabbbcx').group())
print(re.search(r'colou?r', 'my colour').group())
print(re.search(r'\d{3}', '12 345 6789').group())""")
expl(r'''#### Ein längeres Beispiel

`\d\w{4}\s9` bedeutet: eine Ziffer, genau vier Wortzeichen, ein Leerraum-Zeichen, eine 9.''',
     r"""import re

texte = ['8acDa 9', '8abcd_9', '7xxx 9', '0_a6b 9']
muster = r'\d\w{4}\s9'
for text in texte:
    print(text, bool(re.search(muster, text)))""")

tm("Schreibe ein Muster, das auf `color` und `colour` passt.",
   "['color', 'colour', 'colouur', 'colr']", r'colou?r')
t(r'Gib die erste Zahl (eine oder mehrere Ziffern) in `satz` aus.',
  "import re\nsatz = 'Ich habe 125 Euro und 30 Cent.'",
  r"print(re.search(r'\d+', satz).group())")
tm(r"Prüfe mit `\d{5}`, welche Texte fünf Ziffern hintereinander enthalten.",
   "['48143', '4814', 'PLZ 10115 Berlin', '1234a']", r'\d{5}')
tm("Schreibe ein Muster für ein Datum, bei dem Tag und Monat ein- oder zweistellig sein dürfen und das Jahr vierstellig ist.",
   "['01.02.2024', '1.2.2024', '31.12.99', '5.11.2023']", r'\d{1,2}\.\d{1,2}\.\d{4}')
tm("Prüfe, welche Texte ein `G`, mindestens drei `o` und ein `l` enthalten.",
   "['Gol', 'Gool', 'Goool', 'Gooooool']", r'Go{3,}l')
tm("""Ein Kfz-Kennzeichen besteht hier aus 1 bis 3 Großbuchstaben, einem Leerzeichen, 1 bis 2 Großbuchstaben, einem Leerzeichen
und 1 bis 4 Ziffern. Schreibe ein Muster und prüfe es. Dass `K L 12345` passt, liegt daran, dass ein **Teil** davon passt.
Wie man das verhindert, lernst du im nächsten Abschnitt.""",
   "['MS AB 123', 'B X 1', 'MS AB123', 'ms ab 12', 'K L 12345']", r'[A-Z]{1,3} [A-Z]{1,2} \d{1,4}')
t(r'Suche in `satz` ein Wort mit Bindestrich (Wortzeichen, Bindestrich, Wortzeichen) und gib es aus.',
  "import re\nsatz = 'Der Fußball-Verein spielt heute.'",
  r"print(re.search(r'\w+-\w+', satz).group())")
tm(r"""Prüfe, welche Texte die Form „`a`, beliebig viele Leerzeichen, `=`, beliebig viele Leerzeichen, mindestens eine Ziffer“ haben.
Verwende `\s*`.""",
   "['a=5', 'a = 5', 'a  =   12', 'a == 5', 'a = x']", r'a\s*=\s*\d+')
t('Suche in jedem Text eine ganze Zahl mit optionalem Vorzeichen `+` oder `-`. Gib den Treffer aus oder `kein Treffer`.',
  "import re\ntexte = ['-17', '+3', '42', 'x-y']",
  r"""for text in texte:
    m = re.search(r'[-+]?\d+', text)
    if m:
        print(m.group())
    else:
        print('kein Treffer')""")
tm("Gib nur die Wörter aus, die mindestens 8 Wortzeichen hintereinander enthalten.",
   "['Schule', 'Informatik', 'Bleistift', 'Heft', 'Taschenrechner']", r'\w{8}', NUR)
tm("Prüfe, welche Texte ein Wort aus einem Großbuchstaben und danach mindestens zwei Kleinbuchstaben enthalten.",
   "['Anna', 'ANNA', 'An', 'die Oma', 'Ok']", r'[A-Z][a-z]{2,}')
predict(r"""import re
print(re.search(r'a+', 'baaad').group())
print(re.search(r'\d{2,3}', '12345').group())
print(re.search(r'x?y', 'xxy').group())
print(re.search(r'[ab]+', 'cabbac').group())
print(re.search(r'a*', 'baaad').span())""")

# ---------------------------------------------------------------- 6
sec('Anfang, Ende und Wortgrenzen')
expl(r'''#### Anfang `^` und Ende `$`

| Zeichen | Bedeutung |
|---|---|
| `^` oder `\A` | Anfang des Textes |
| `$` oder `\Z` | Ende des Textes |

Sie passen auf eine **Stelle**, nicht auf ein Zeichen. Mit `^...$` muss der **ganze** Text zum Muster passen.''',
     r"""import re

texte = ['04', '10', '99', '110', '112']
for text in texte:
    print(text, bool(re.search(r'[1-9][0-9]', text)), bool(re.search(r'^[1-9][0-9]$', text)))""")
expl(r'''#### `re.fullmatch()` und `re.match()`

- `re.fullmatch(muster, text)` gibt nur dann einen Treffer, wenn der **ganze** Text passt, wie `^...$`.
- `re.match(muster, text)` sucht nur am **Anfang** des Textes, wie ein Muster mit `^`.

Zum Prüfen von Eingaben (Postleitzahl, Uhrzeit, ...) ist `re.fullmatch()` meist die beste Wahl.''',
     r"""import re

print(bool(re.fullmatch(r'\d{5}', '48143')))
print(bool(re.fullmatch(r'\d{5}', '481431')))
print(bool(re.match(r'\d+', '12 Äpfel')))
print(bool(re.match(r'\d+', 'Äpfel: 12')))""")
expl(r'''#### Wortgrenzen `\b` und `\B`

`\b` passt auf eine **Wortgrenze**: eine Stelle zwischen einem Wortzeichen und einem Nicht-Wortzeichen
(oder dem Anfang/Ende des Textes). `\B` passt auf eine Stelle, die **keine** Wortgrenze ist.

- `\bich\b` findet `ich` nur als ganzes Wort,
- `\bich` nur am Wortanfang, `ich\b` nur am Wortende.

Hier ist der Raw-String besonders wichtig, denn ohne `r` wäre `'\b'` ein Steuerzeichen.''',
     r"""import re

for text in ['ich gehe', 'nicht', 'ichbezogen', 'mich']:
    print(text, bool(re.search(r'\bich\b', text)), bool(re.search(r'\bich', text)),
          bool(re.search(r'ich\b', text)), bool(re.search(r'\Bich\B', text)))""")

tm(r"Prüfe mit `re.fullmatch()`, welche Texte genau eine fünfstellige Postleitzahl sind.",
   "['48143', '4814', 'PLZ 10115', '123456']", r'\d{5}', FULL)
tm("Schreibe ein Muster mit `^` und `$` für Texte, die nur aus Kleinbuchstaben `a` bis `z` bestehen (mindestens einer).",
   "['hallo', 'Hallo', 'hallo welt', 'abc1', 'x']", r'^[a-z]+$')
tm("Gib nur die Sätze aus, die mit `Ich` beginnen.",
   "['Ich bin da.', 'Bin ich da?', 'Ichthyologie ist toll.', 'ich auch.']", r'^Ich', NUR)
tm(r"Gib nur die Sätze aus, die mit dem **Wort** `Ich` beginnen. Verwende `^` und `\b`.",
   "['Ich bin da.', 'Bin ich da?', 'Ichthyologie ist toll.', 'Ich!']", r'^Ich\b', NUR)
tm("Gib nur die Sätze aus, die mit einem Fragezeichen enden.",
   "['Wie geht es?', 'Gut?!', 'Echt? Ja.', 'Wer?']", r'\?$', NUR)
tm("Prüfe die Kfz-Kennzeichen aus Abschnitt 5 jetzt mit `re.fullmatch()`.",
   "['MS AB 123', 'B X 1', 'MS AB123', 'ms ab 12', 'K L 12345']", r'[A-Z]{1,3} [A-Z]{1,2} \d{1,4}', FULL)
t(r'Zähle, in wie vielen Sätzen `die` als **ganzes Wort** vorkommt. Gib die Anzahl aus.',
  "import re\nsaetze = ['die Katze', 'Dieb', 'Melodie', 'Ich sehe die Sonne.', 'Diesel']",
  r"""anzahl = 0
for satz in saetze:
    if re.search(r'\bdie\b', satz):
        anzahl += 1
print(anzahl)""")
tm("Prüfe mit `re.fullmatch()`, welche Texte eine Uhrzeit mit ein- oder zweistelliger Stunde und zweistelliger Minute sind.",
   "['9:30', '14:05', '14:5', 'um 14:05', '123:45']", r'\d{1,2}:\d{2}', FULL)
tm("""Ein Benutzername beginnt mit einem Kleinbuchstaben `a`-`z`. Danach folgen 2 bis 11 Zeichen aus Kleinbuchstaben, Ziffern und `_`.
Prüfe mit `re.fullmatch()`.""",
   "['max_1', 'm1', '1max', 'super_mario_2024', 'anna']", r'[a-z][a-z0-9_]{2,11}', FULL)
tm("""Eine Kommazahl besteht hier aus einem optionalen Vorzeichen, beliebig vielen Ziffern, einem optionalen Punkt und mindestens einer Ziffer.
Schreibe ein Muster mit `^` und `$`.""",
   "['-3.14', '2', '+000.62', '4.-62', '.5', '5.']", r'^[-+]?[0-9]*\.?[0-9]+$')
t('Gib mit `re.match()` für jede Zeile die Zahl am Anfang aus. Zeilen, die nicht mit einer Zahl beginnen, werden übersprungen.',
  "import re\nzeilen = ['3 Äpfel', 'Äpfel: 3', '12 Birnen', ' 7 Kiwis']",
  r"""for zeile in zeilen:
    m = re.match(r'\d+', zeile)
    if m:
        print(m.group())""")
tm(r"Gib nur die Wörter aus, die `ball` **nicht** am Anfang, aber irgendwo im Wort enthalten. Verwende `\B`.",
   "['ballern', 'Fußball', 'Handballer', 'ball', 'Ballon']", r'\Bball', NUR)
predict(r"""import re
print(bool(re.search(r'^a', 'banane')))
print(bool(re.search(r'e$', 'banane')))
print(bool(re.fullmatch(r'b.*e', 'banane')))
print(bool(re.match(r'an', 'banane')))
print(bool(re.search(r'\Ban\B', 'banane')))""")
predict(r"""print('\b' == r'\b')
print(len('\b'), len(r'\b'))""")

# ---------------------------------------------------------------- 7
sec('Alternativen und Gruppen')
expl(r'''#### Alternativen mit `|`

`Hund|Katze` passt auf `Hund` **oder** `Katze`.

Achtung: `|` trennt das **ganze** Muster in zwei Teile. `^1\d\d|2\d\d$` bedeutet „`^1\d\d` oder `2\d\d$`“.
Deshalb passt es auch auf `1234` und `5299`.''',
     r"""import re

texte = ['99', '100', '299', '310', '1234', '5299']
muster = r'^1[0-9][0-9]|2[0-9][0-9]$'
for text in texte:
    print(text, bool(re.search(muster, text)))""")
expl(r'''#### Gruppen `(...)`

Mit runden Klammern fasst man einen Teil des Musters zu einer **Gruppe** zusammen:

- `^(1|2)\d\d$` : Die Alternative gilt nur innerhalb der Klammern.
- `(ab)+` : Der Quantor gilt für die ganze Gruppe, also `ab`, `abab`, `ababab`, ...

Python merkt sich außerdem, was zu jeder Gruppe gepasst hat (Abschnitte 8 und 9).
Mit `(?:...)` gruppiert man, **ohne** dass sich Python den Inhalt merkt.''',
     r"""import re

texte = ['99', '100', '299', '310', '1234', '5299']
for text in texte:
    print(text, bool(re.search(r'^(1|2)[0-9][0-9]$', text)))

print(re.search(r'(ab)+', 'xxababab!').group())
print(bool(re.fullmatch(r'(Mo|Di|Mi|Do|Fr)\.?', 'Mi.')))""")

tm("Prüfe, welche Texte `Hund` oder `Katze` enthalten.",
   "['Hund', 'Katze', 'Maus', 'Hundekatze']", r'Hund|Katze')
tm("Prüfe mit `re.fullmatch()`, welche Texte eine Wochentags-Abkürzung `Mo`, `Di`, `Mi`, `Do`, `Fr`, `Sa` oder `So` sind.",
   "['Mo', 'Mi', 'Mx', 'Montag', 'So']", r'Mo|Di|Mi|Do|Fr|Sa|So', FULL)
tm("Prüfe mit `re.fullmatch()`, welche Dateinamen auf `.jpg`, `.png` oder `.gif` enden. Vor dem Punkt stehen Wortzeichen.",
   "['bild.jpg', 'foto.png', 'text.txt', 'bild.jpeg', 'logo.gif']", r'\w+\.(jpg|png|gif)', FULL)
tm("Prüfe mit `re.fullmatch()`: ein- oder mehrmals `ha`, danach beliebig viele Ausrufezeichen.",
   "['ha', 'hahaha!!', 'hah', 'ha!ha', 'hahaha']", r'(ha)+!*', FULL)
tm(r"""Prüfe mit `re.fullmatch()`, welche Texte eine gültige Uhrzeit von `00:00` bis `23:59` sind (immer zweistellig).
Tipp: Die Stunde ist `[01]\d` oder `2[0-3]`.""",
   "['09:30', '23:59', '24:00', '12:60', '7:15']", r'([01]\d|2[0-3]):[0-5]\d', FULL)
tm("Prüfe mit `^` und `$`, welche Texte eine Monatszahl von `1` bis `12` ohne führende Null sind. Ohne Klammern geht es hier nicht.",
   "['1', '9', '10', '12', '13', '0', '05']", r'^([1-9]|1[0-2])$')
tm(r"""Prüfe mit `re.fullmatch()`, welche Texte die Form einer IP-Adresse haben: viermal 1 bis 3 Ziffern, getrennt durch Punkte.
Verwende `(\d{1,3}\.){3}`. Ob die Zahlen höchstens 255 sind, prüft das Muster nicht.""",
   "['192.168.0.1', '10.0.0', '1.2.3.4', '256.1.1.1', 'a.b.c.d']", r'(\d{1,3}\.){3}\d{1,3}', FULL)
tm("Gib nur die Sätze aus, die mit dem Wort `Hallo` oder dem Wort `Hi` beginnen.",
   "['Hallo Anna', 'Hi Tom', 'Hilfe!', 'Na, hallo', 'Hallo!']", r'^(Hallo|Hi)\b', NUR)
tm("Prüfe mit `re.fullmatch()`, welche Texte `ja`, `nein` oder `vielleicht` sind, jeweils groß oder klein geschrieben am Anfang.",
   "['ja', 'Nein', 'vielleicht', 'jein', 'Ja!', 'Vielleicht']", r'[Jj]a|[Nn]ein|[Vv]ielleicht', FULL)
tm(r"Prüfe mit `re.fullmatch()`, welche Texte eine Zahl mit optionalem Nachkommateil sind: Ziffern, danach optional ein Komma und genau zwei Ziffern. Verwende `(,\d{2})?`.",
   "['12', '12,50', '0,99', '12,5', ',50']", r'\d+(,\d{2})?', FULL)
predict(r"""import re
print(re.search(r'ab|cd', 'xxcdab').group())
print(re.search(r'a(b|c)+', 'abcbcd').group())
print(bool(re.fullmatch(r'ja|nein', 'jein')))
print(bool(re.search(r'^ja|nein$', 'ja oder vielleicht')))
print(re.search(r'(na)+', 'Banana').group())""")

# ---------------------------------------------------------------- 8
sec('Alle Treffer finden mit re.findall()')
expl(r'''#### `re.findall()`

`re.findall(muster, text)` sammelt **alle** Treffer in einer Liste. Die Treffer überlappen sich nicht:
Nach einem Treffer wird dahinter weitergesucht. Gibt es keinen Treffer, ist die Liste leer.

Mit `len()` kann man die Treffer zählen.''',
     r"""import re

s = 'abe 12 aa 43 4ab 113 01 99 5j'
zahlen = re.findall(r'\b[1-9][0-9]\b', s)
print(zahlen)
print(len(zahlen))
print(re.findall(r'x', s))""")
expl(r'''#### `re.findall()` mit Gruppen

Enthält das Muster Gruppen `(...)`, liefert `re.findall()` nicht den ganzen Treffer, sondern nur den **Inhalt der Gruppen**:

- bei **einer** Gruppe eine Liste von Zeichenketten,
- bei **mehreren** Gruppen eine Liste von Tupeln.

Gruppen mit `(?:...)` zählen dabei nicht mit.''',
     r"""import re

text = 'abab665  ab91 ababab42  abc809'
print(re.findall(r'\b(ab)+(\d+)', text))
print(re.findall(r'\b(?:ab)+(\d+)', text))
print(re.findall(r'\b(?:ab)+\d+', text))""")
expl(r'''#### Daten herausholen

Mit einer Gruppe holt man genau den Teil heraus, der einen interessiert.
Hier sollen die Vornamen gesammelt werden. Um das `=` dürfen beliebig viele Leerzeichen stehen.''',
     r"""import re

zeilen = ['Nachname = Schulte, Vorname = Anna-Lena, Alter = 21',
          'Vorname= Malte, Nachname= Riedberg,  Alter = 22']
muster = r'Vorname\s*=\s*([A-Za-z-]+)'
for zeile in zeilen:
    print(re.findall(muster, zeile)[0])""")

t(r'Gib mit `re.findall()` eine Liste aller Zahlen in `text` aus.',
  "import re\ntext = 'Ich habe 3 Hunde, 12 Katzen und 150 Fische.'",
  r"print(re.findall(r'\d+', text))")
t('Berechne die Summe aller Zahlen in `text` und gib sie aus.',
  "import re\ntext = 'Ich habe 3 Hunde, 12 Katzen und 150 Fische.'",
  r"""summe = 0
for z in re.findall(r'\d+', text):
    summe += int(z)
print(summe)""")
t('Gib eine Liste aller Wörter in `satz` aus, die mit einem Großbuchstaben (auch Ä, Ö, Ü) beginnen.',
  "import re\nsatz = 'Am Montag fährt Anna mit dem Bus nach Köln.'",
  r"print(re.findall(r'\b[A-ZÄÖÜ]\w*', satz))")
t('Zähle mit `re.findall()` und `len()` die Vokale (groß und klein) in `satz`.',
  "import re\nsatz = 'Informatik macht Spaß'",
  r"print(len(re.findall(r'[aeiouAEIOU]', satz)))")
t('Gib eine Liste aller Hashtags (`#` und danach Wortzeichen) in `text` aus.',
  "import re\ntext = 'Toller Tag! #sommer #sonne und #urlaub2024'",
  r"print(re.findall(r'#\w+', text))")
t('Gib eine Liste der Hashtags **ohne** `#` aus. Verwende eine Gruppe.',
  "import re\ntext = 'Toller Tag! #sommer #sonne und #urlaub2024'",
  r"print(re.findall(r'#(\w+)', text))")
t(r'''Gib eine Liste aller E-Mail-Adressen in `text` aus. Eine Adresse besteht hier aus Wortzeichen, Punkten und Bindestrichen,
dann `@`, dann Wortzeichen und Bindestrichen, einem Punkt und Wortzeichen. Tipp: `[\w.-]+`.''',
  "import re\ntext = 'Schreib an anna.m@schule.de oder info@web-shop.com, nicht an @foo.'",
  r"print(re.findall(r'[\w.-]+@[\w-]+\.\w+', text))")
t('Gib eine Liste aller Preise der Form `2,49 €` in `text` aus (Ziffern, Komma, zwei Ziffern, Leerzeichen, €).',
  "import re\ntext = 'Brot 2,49 €, Milch 1,19 €, Butter 3 €'",
  r"print(re.findall(r'\d+,\d{2} €', text))")
t('Gib eine Liste aller Wörter in `satz` aus, die genau vier Wortzeichen lang sind.',
  "import re\nsatz = 'Der Hund kann sehr laut bellen'",
  r"print(re.findall(r'\b\w{4}\b', satz))")
t('Gib mit `re.findall()` und zwei Gruppen eine Liste der Paare aus Name und Zahl aus.',
  "import re\ntext = 'a=1, b=22, c=x, d=4'",
  r"print(re.findall(r'(\w+)=(\d+)', text))")
t('Erstelle aus den Paaren ein Dictionary, das jedem Namen die Zahl als `int` zuordnet. Gib es aus.',
  "import re\ntext = 'a=1, b=22, c=x, d=4'",
  r"""werte = {}
for name, zahl in re.findall(r'(\w+)=(\d+)', text):
    werte[name] = int(zahl)
print(werte)""")
t(r'Gib für jede Zeile den Nachnamen aus. Er kann wie der Vorname einen Bindestrich enthalten.',
  """import re
zeilen = ['Nachname = Schulte, Vorname = Anna-Lena, Alter = 21',
          'Vorname= Malte, Nachname= Riedberg,  Alter = 22']""",
  r"""for zeile in zeilen:
    print(re.findall(r'Nachname\s*=\s*([A-Za-z-]+)', zeile)[0])""")
t(r'Berechne das Durchschnittsalter aller Personen in `zeilen` und gib es aus.',
  """import re
zeilen = ['Nachname = Schulte, Vorname = Anna-Lena, Alter = 21',
          'Vorname= Malte, Nachname= Riedberg,  Alter = 22']""",
  r"""summe = 0
for zeile in zeilen:
    summe += int(re.findall(r'Alter\s*=\s*(\d+)', zeile)[0])
print(summe / len(zeilen))""")
t(r'''Gib eine Liste der Telefon- und Faxnummern (nicht der Handynummer) aus. Verwende `(?:Tel|Fax)` und eine Gruppe für die Nummer.''',
  "import re\ntext = 'Tel: 0251-12345, Fax: 0251-12346, Handy: 0170-987654'",
  r"print(re.findall(r'(?:Tel|Fax): (\d+-\d+)', text))")
t('Gib eine Liste aller Uhrzeiten (Stunde ein- oder zweistellig, Minute zweistellig) in `text` aus.',
  "import re\ntext = 'Bus um 7:15, Schule ab 8:00, Ende 13:30, Training 17:45.'",
  r"print(re.findall(r'\d{1,2}:\d{2}', text))")
predict(r"""import re
print(re.findall(r'a', 'Banana'))
print(re.findall(r'an', 'Banana'))
print(re.findall(r'ana', 'Banana'))
print(re.findall(r'x', 'Banana'))
print(re.findall(r'(a)(n)', 'Banana'))""")
predict(r"""import re
print(re.findall(r'\d+', 'a12b3'))
print(re.findall(r'\d', 'a12b3'))
print(re.findall(r'\d*', 'a12b'))""")

# ---------------------------------------------------------------- 9
sec('Gruppen auslesen und re.finditer()')
expl(r'''#### Gruppen im Match-Objekt

Die Gruppen werden nach ihrer **öffnenden Klammer** von links nach rechts nummeriert, beginnend bei 1.

| Methode | Ergebnis |
|---|---|
| `m.group()` oder `m.group(0)` | der ganze Treffer |
| `m.group(1)`, `m.group(2)`, ... | der Inhalt der 1., 2., ... Gruppe |
| `m.groups()` | ein Tupel mit dem Inhalt aller Gruppen |
| `m.span(1)` | Start und Ende der 1. Gruppe |''',
     r"""import re

m = re.search(r'(\d{1,2})\.(\d{1,2})\.(\d{4})', 'Am 24.12.2024 ist Heiligabend.')
print(m.group())
print(m.group(1), m.group(2), m.group(3))
print(m.groups())
tag, monat, jahr = m.groups()
print(jahr)""")
expl(r'''#### Benannte Gruppen `(?P<name>...)`

Man kann Gruppen auch einen **Namen** geben: `(?P<stunde>\d+)`.
Dann bekommt man ihren Inhalt mit `m.group('stunde')`.
`m.groupdict()` liefert ein Dictionary mit allen benannten Gruppen.''',
     r"""import re

m = re.search(r'(?P<stunde>\d{1,2}):(?P<minute>\d{2})', 'Beginn um 8:45 Uhr')
print(m.group('stunde'))
print(m.group('minute'))
print(m.groupdict())""")
expl(r'''#### `re.finditer()`

`re.finditer(muster, text)` liefert wie `re.findall()` alle Treffer, aber als **Match-Objekte**, einen nach dem anderen.
Man durchläuft sie mit einer `for`-Schleife. Das ist praktisch, wenn man zu jedem Treffer die Position
oder mehrere Gruppen braucht.''',
     r"""import re

for m in re.finditer(r'\d+', 'a1 b22 c333'):
    print(m.group(), m.start())""")
expl(r'''#### Rückverweise `\1`

Im Muster selbst bedeutet `\1`: „genau derselbe Text, der zur 1. Gruppe gepasst hat“.
`(\w)\1` passt also auf zwei **gleiche** Wortzeichen hintereinander.''',
     r"""import re

for wort in ['Ball', 'Hund', 'Kaffee']:
    m = re.search(r'(\w)\1', wort)
    if m:
        print(wort, m.group())""")

t('Gib Tag, Monat und Jahr aus dem Datum in `satz` aus wie unten. Verwende drei Gruppen.',
  "import re\nsatz = 'Abgabe bis 15.03.2025.'",
  r"""m = re.search(r'(\d{2})\.(\d{2})\.(\d{4})', satz)
print(f'Tag: {m.group(1)}, Monat: {m.group(2)}, Jahr: {m.group(3)}')""")
t('Gib das Datum aus `satz` in der Form `Jahr-Monat-Tag` aus.',
  "import re\nsatz = 'Abgabe bis 15.03.2025.'",
  r"""m = re.search(r'(\d{2})\.(\d{2})\.(\d{4})', satz)
tag, monat, jahr = m.groups()
print(f'{jahr}-{monat}-{tag}')""")
t('Die Namen stehen in der Form `Nachname, Vorname`. Gib sie mit zwei Gruppen in der Form `Vorname Nachname` aus.',
  "import re\nnamen = ['Müller, Anna', 'Schmidt, Tom', 'Yılmaz, Cem']",
  r"""for name in namen:
    m = re.fullmatch(r'(\w+), (\w+)', name)
    print(m.group(2), m.group(1))""")
t('''Suche die Uhrzeit in `text` mit den benannten Gruppen `stunde` und `minute`.
Gib aus, wie viele Minuten seit Mitternacht vergangen sind.''',
  "import re\ntext = 'Der Film beginnt um 20:15 Uhr.'",
  r"""m = re.search(r'(?P<stunde>\d{1,2}):(?P<minute>\d{2})', text)
print(int(m.group('stunde')) * 60 + int(m.group('minute')))""")
t(r'''Zerlege `text` mit den benannten Gruppen `name`, `alter` und `stadt` und gib `m.groupdict()` aus.
Die Klammern um das Alter musst du escapen: `\(` und `\)`.''',
  "import re\ntext = 'Mia (16) aus Köln'",
  r"""m = re.fullmatch(r'(?P<name>\w+) \((?P<alter>\d+)\) aus (?P<stadt>\w+)', text)
print(m.groupdict())""")
t('Gib mit `re.finditer()` jede Zahl in `text` zusammen mit ihrer Startposition aus.',
  "import re\ntext = 'x7 y42 z5'",
  r"""for m in re.finditer(r'\d+', text):
    print(m.group(), m.start())""")
t('Gib mit `re.finditer()` die Positionen aller kleinen `e` in `wort` aus, jede in einer Zeile.',
  "import re\nwort = 'Erdbeere'",
  r"""for m in re.finditer(r'e', wort):
    print(m.start())""")
t('''Gib mit `re.finditer()` und zwei Gruppen für jede Person aus, wie viele Punkte sie hat.
Gib danach die Summe aller Punkte aus.''',
  "import re\ntext = 'Anna: 3, Ben: 17, Cem: 8'",
  r"""summe = 0
for m in re.finditer(r'(\w+): (\d+)', text):
    print(f'{m.group(1)} hat {m.group(2)} Punkte')
    summe += int(m.group(2))
print(summe)""")
tm(r"Gib mit einem Rückverweis nur die Wörter aus, die zwei gleiche Buchstaben direkt hintereinander enthalten.",
   "['Ball', 'Hund', 'Kaffee', 'Boot', 'Tisch']", r'(\w)\1', NUR)
t(r'Gib mit `re.findall()` und einem Rückverweis eine Liste der Wörter aus, die in `satz` doppelt hintereinander stehen.',
  "import re\nsatz = 'Das ist ist ein Test Test für dich.'",
  r"print(re.findall(r'\b(\w+) \1\b', satz))")
tm(r"""Prüfe mit `re.fullmatch()`, welche Wörter Palindrome aus fünf Buchstaben sind (vorwärts und rückwärts gleich).
Tipp: `(\w)(\w)\w\2\1`.""",
   "['Rotor', 'rotor', 'level', 'hallo', 'kayak']", r'(\w)(\w)\w\2\1', FULL)
predict(r"""import re
m = re.search(r'(a+)(b*)', 'xaabbby')
print(m.group())
print(m.group(1))
print(m.group(2))
print(m.groups())
print(m.span(2))""")
predict(r"""import re
m = re.search(r'(\d+)', 'abc 12')
print(m.group(1))
print(m.group(2))""", error=IndexError)

# ---------------------------------------------------------------- 10
sec('Gierig und genügsam')
expl(r'''#### Gierige Quantoren

Die Quantoren `?`, `*`, `+` und `{k,l}` sind **gierig** (englisch *greedy*): Sie nehmen so viele Zeichen wie möglich.

Hängt man ein `?` an, werden sie **genügsam** (englisch *lazy*): `*?`, `+?`, `??`, `{k,l}?` nehmen so **wenige** Zeichen
wie möglich, sodass das Muster gerade noch passt.''',
     r"""import re

print(re.findall(r'Py.*on', 'Python Python Python'))
print(re.findall(r'Py.*?on', 'Python Python Python'))""")
expl(r'''#### Beispiel: HTML-Tags

Ein HTML-Tag steht in spitzen Klammern, z. B. `<b>`. `<.+>` nimmt alles bis zum **letzten** `>`.
Richtig wird es genügsam mit `<.+?>` oder mit einer verneinten Klasse: `<[^>]+>` heißt
„`<`, dann mindestens ein Zeichen, das kein `>` ist, dann `>`“.''',
     r"""import re

html = '<b>fett</b>'
print(re.findall(r'<.+>', html))
print(re.findall(r'<.+?>', html))
print(re.findall(r'<[^>]+>', html))""")

t('Gib mit einem genügsamen Quantor eine Liste aller HTML-Tags in `html` aus.',
  "import re\nhtml = '<p>Hallo <b>Welt</b></p>'",
  r"print(re.findall(r'<.+?>', html))")
t('Gib wieder eine Liste aller HTML-Tags aus. Verwende diesmal `[^>]+`.',
  "import re\nhtml = '<p>Hallo <b>Welt</b></p>'",
  r"print(re.findall(r'<[^>]+>', html))")
t('Gib eine Liste aller Texte aus, die in `satz` in doppelten Anführungszeichen stehen (ohne die Anführungszeichen).',
  "import re\nsatz = 'Sie sagte \"Hallo\" und er sagte \"Tschüss\".'",
  r"""print(re.findall(r'"(.*?)"', satz))""")
t('Gib eine Liste der Texte aus, die in `text` in runden Klammern stehen (ohne die Klammern).',
  "import re\ntext = 'Python (Sprache), Java (auch Sprache) und HTML (keine).'",
  r"print(re.findall(r'\((.*?)\)', text))")
t('Gib mit `re.search()` und einem genügsamen Quantor nur den ersten Satz (bis einschließlich zum ersten Punkt) aus.',
  "import re\ntext = 'Das ist Satz eins. Das ist Satz zwei.'",
  r"print(re.search(r'.+?\.', text).group())")
t(r'Gib eine Liste aller Textstellen aus, die in Markdown fett geschrieben sind, also zwischen `**` und `**` stehen (ohne die Sterne).',
  "import re\ntext = 'Das ist **wichtig** und das ist **sehr wichtig**.'",
  r"print(re.findall(r'\*\*(.+?)\*\*', text))")
t('Gib eine Liste aller Werte aus, die in `zeile` zwischen `[` und `]` stehen.',
  "import re\nzeile = 'Werte: [3] [17] [x] [42]'",
  r"print(re.findall(r'\[(.*?)\]', zeile))")
predict(r"""import re
print(re.findall(r'a.*b', 'a1b a2b'))
print(re.findall(r'a.*?b', 'a1b a2b'))
print(re.search(r'\d+?', '2024').group())
print(re.search(r'\d{2,4}?', '2024').group())
print(re.findall(r'\d{2,4}', '1234567'))
print(re.findall(r'\d{2,4}?', '1234567'))""")

# ---------------------------------------------------------------- 11
sec('Ersetzen mit re.sub()')
expl(r'''#### `re.sub()`

`re.sub(muster, ersatz, text)` ersetzt **jeden** Treffer im `text` durch `ersatz` und gibt den neuen Text zurück.
Der alte Text bleibt unverändert.

Mit `count=1` wird nur der erste Treffer ersetzt (allgemein höchstens `count` Treffer).''',
     r"""import re

print(re.sub(r'[Jj]a[Vv]a', 'Python', 'Java oder java und jaVa'))
print(re.sub(r'\d', '#', 'PIN 4711'))
print(re.sub(r'a', 'o', 'Banane', count=1))""")
expl(r'''#### Gruppen im Ersatztext

Im Ersatztext steht `\1` für den Inhalt der 1. Gruppe, `\2` für die 2. Gruppe usw.
Bei benannten Gruppen schreibt man `\g<name>`. Auch den Ersatztext schreibt man deshalb als Raw-String.

Beispiel: Beim Umstellen von Processing-Programmen auf p5.js muss aus `fill(#AB02F9);` der Code `fill('#AB02F9');` werden.''',
     r"""import re

zeile = 'fill(#AB02F9);  // Farbe setzen'
zeile = re.sub(r"fill\((#[A-Fa-f0-9]{6})\);", r"fill('\1');", zeile)
print(zeile)

print(re.sub(r'(?P<tag>\d+)\.(?P<monat>\d+)\.', r'\g<monat>/\g<tag>/', '24.12.2024'))""")
expl(r'''#### Eine Funktion als Ersatz

Statt eines Ersatztextes kann man auch eine **Funktion** angeben. Sie wird für jeden Treffer mit dem Match-Objekt
aufgerufen und gibt den Ersatztext zurück. Dann kann man mit dem Treffer rechnen.''',
     r"""import re

def doppelt(m):
    return str(int(m.group()) * 2)

print(re.sub(r'\d+', doppelt, 'a1 b22 c5'))""")

t("Ersetze jede Ziffer in `text` durch `*` und gib das Ergebnis aus.",
  "import re\ntext = 'PIN: 4711, Code: 0815'",
  r"print(re.sub(r'\d', '*', text))")
t("Ersetze in `satz` jede Folge von Leerzeichen durch ein einziges Leerzeichen.",
  "import re\nsatz = 'Das   ist    zu  viel    Platz.'",
  r"print(re.sub(r' +', ' ', satz))")
t("Ersetze in `satz` nur das **erste** `eins` durch `drei`.",
  "import re\nsatz = 'eins, zwei, eins, zwei'",
  r"print(re.sub(r'eins', 'drei', satz, count=1))")
t(r"Entferne alle Zeichen aus `satz`, die weder Wortzeichen noch Leerraum sind. Ersetze sie dazu durch `''`.",
  "import re\nsatz = \"Hallo, Welt! Wie geht's?\"",
  r"print(re.sub(r'[^\w\s]', '', satz))")
t("Entferne alle HTML-Tags aus `html`.",
  "import re\nhtml = '<p>Das ist <b>fett</b> und <i>kursiv</i>.</p>'",
  r"print(re.sub(r'<[^>]+>', '', html))")
t(r"Schreibe alle Daten in `text` in die Form `Jahr-Monat-Tag` um. Verwende drei Gruppen und `\3-\2-\1`.",
  "import re\ntext = 'Ferien vom 23.06.2025 bis 05.08.2025.'",
  r"print(re.sub(r'(\d{2})\.(\d{2})\.(\d{4})', r'\3-\2-\1', text))")
t("Die Namen stehen in der Form `Nachname, Vorname`. Gib sie mit `re.sub()` in der Form `Vorname Nachname` aus.",
  "import re\nnamen = ['Müller, Anna', 'Schmidt, Tom', 'Yılmaz, Cem']",
  r"""for name in namen:
    print(re.sub(r'(\w+), (\w+)', r'\2 \1', name))""")
t(r"Schreibe die Telefonnummern in die Form `(0251) 12345` um. Verwende die benannten Gruppen `vorwahl` und `nummer` und `\g<...>`.",
  "import re\ntext = 'Büro: 0251-12345, Sekretariat: 0251-12399'",
  r"print(re.sub(r'(?P<vorwahl>\d+)-(?P<nummer>\d+)', r'(\g<vorwahl>) \g<nummer>', text))")
t(r"""Stelle die Zeilen von Processing auf p5.js um: Aus `fill(#00FF00)` wird `fill('#00FF00')`, aus `stroke(#000000)` wird `stroke('#000000')`.
Verwende eine Gruppe für den Befehl (`fill|stroke`) und eine für die Farbe.""",
  "import re\nzeilen = ['stroke(#00FF00);', 'fill(#ab02f9); stroke(#000000);', 'rect(10, 10, 50, 50);']",
  r"""for zeile in zeilen:
    print(re.sub(r'(fill|stroke)\((#[A-Fa-f0-9]{6})\)', r"\1('\2')", zeile))""")
t("Ersetze die ganzen Wörter `doof` und `blöd` (auch mit großem Anfangsbuchstaben) durch `***`.",
  "import re\nsatz = 'Das ist doof. Blöd gelaufen! Aber Doofenshmirtz bleibt.'",
  r"print(re.sub(r'\b([Dd]oof|[Bb]löd)\b', '***', satz))")
t("Ersetze mit einer Funktion jede Zahl in `text` durch die um 1 größere Zahl.",
  "import re\ntext = 'Level 9, Leben 3, Punkte 99'",
  r"""def plus_eins(m):
    return str(int(m.group()) + 1)

print(re.sub(r'\d+', plus_eins, text))""")
t(r"Schreibe mit einer Funktion den ersten Buchstaben jedes Wortes groß. Das Muster `\b\w` findet ihn.",
  "import re\ntitel = 'der herr der ringe'",
  r"""def gross(m):
    return m.group().upper()

print(re.sub(r'\b\w', gross, titel))""")
t(r"Entferne doppelte Wörter, die direkt hintereinander stehen. Verwende einen Rückverweis.",
  "import re\nsatz = 'Das ist ist ein ein Test.'",
  r"print(re.sub(r'\b(\w+) \1\b', r'\1', satz))")
t(r"""Wandle den Variablennamen von *camelCase* in *snake_case* um: Vor jeden Großbuchstaben, der auf einen Kleinbuchstaben folgt,
kommt ein `_`. Danach wird alles kleingeschrieben.""",
  "import re\nname = 'meineLieblingsVariable'",
  r"print(re.sub(r'([a-z])([A-Z])', r'\1_\2', name).lower())")
predict(r"""import re
print(re.sub(r'a', 'o', 'Banane'))
print(re.sub(r'an', '', 'Banane'))
print(re.sub(r'(\w)(\w)', r'\2\1', 'abcdef'))
print(re.sub(r'\s+', '', ' a b  c '))
print(re.sub(r'x', 'y', 'abc'))""")

# ---------------------------------------------------------------- 12
sec('Zerlegen mit re.split()')
expl(r'''#### `re.split()`

`re.split(muster, text)` zerlegt den Text in eine Liste. **Alles, was zum Muster passt, ist ein Trennzeichen.**
Anders als bei `text.split(',')` kann man damit mehrere verschiedene Trennzeichen auf einmal verwenden.

- Stehen zwei Trennzeichen direkt nebeneinander, entsteht dazwischen eine leere Zeichenkette `''`.
  Mit einem Quantor wie `+` zählen mehrere Trennzeichen hintereinander als **ein** Trennzeichen.
- Mit `maxsplit=1` wird nur am ersten Trennzeichen zerlegt.
- Enthält das Muster eine Gruppe, stehen die Trennzeichen ebenfalls in der Liste.''',
     r"""import re

print(re.split(r'[,; ]', 'a-a;bbb,,c; dd'))
print(re.split(r'[,; ]+', 'a-a;bbb,,c; dd'))
print(re.split(r'[,;]', 'a,b;c', maxsplit=1))
print(re.split(r'(\d)', 'a1b2c'))""")

t(r"Zerlege `text` an den Kommas. Die Leerzeichen um die Kommas sollen verschwinden. Tipp: `\s*,\s*`.",
  "import re\ntext = 'Äpfel , Birnen,Kiwis ,  Bananen'",
  r"print(re.split(r'\s*,\s*', text))")
t('Zerlege `text` an jeder Ziffernfolge und gib die Liste aus.',
  "import re\ntext = 'abc12def3ghi'",
  r"print(re.split(r'\d+', text))")
t('Die Daten sind mit verschiedenen Trennzeichen geschrieben. Zerlege jedes an `-`, `.` oder `/` und gib die Liste aus.',
  "import re\ndaten = ['2024-03-15', '15.03.2024', '15/03/2024']",
  r"""for datum in daten:
    print(re.split(r'[-./]', datum))""")
t(r'''Zerlege `satz` an allen Folgen von Nicht-Wortzeichen (`\W+`). Entferne danach mit einer List Comprehension die leeren
Zeichenketten und gib die Liste aus.''',
  "import re\nsatz = 'Hallo! Wie geht es dir? Gut.'",
  r"""teile = re.split(r'\W+', satz)
print([w for w in teile if w != ''])""")
t('Zerlege die Rechnung an `+` und `-`. Die Rechenzeichen sollen mit in der Liste stehen. Verwende eine Gruppe.',
  "import re\nrechnung = '12+7-3+10'",
  r"print(re.split(r'([+-])', rechnung))")
t('''Berechne das Ergebnis der Rechnung. Zerlege sie dazu wie in der vorigen Aufgabe und gehe die Liste durch.
Tipp: Die Zahlen stehen an den geraden Indizes, die Rechenzeichen an den ungeraden.''',
  "import re\nrechnung = '12+7-3+10'",
  r"""teile = re.split(r'([+-])', rechnung)
ergebnis = int(teile[0])
for i in range(1, len(teile), 2):
    if teile[i] == '+':
        ergebnis += int(teile[i + 1])
    else:
        ergebnis -= int(teile[i + 1])
print(ergebnis)""")
t(r'Zerlege `zeile` nur am **ersten** Doppelpunkt (mit den Leerzeichen dahinter).',
  "import re\nzeile = 'Termin: 12.03.2025: Klausur'",
  r"print(re.split(r':\s*', zeile, maxsplit=1))")
t('Zerlege `text` in Sätze (Trennzeichen: `.`, `!` oder `?` mit den Leerzeichen danach). Gib jeden nicht leeren Satz in einer eigenen Zeile aus.',
  "import re\ntext = 'Hallo. Wie geht es? Super! Bis bald.'",
  r"""for satz in re.split(r'[.!?]\s*', text):
    if satz != '':
        print(satz)""")
predict(r"""import re
print(re.split(r',', 'a,b,,c'))
print(re.split(r',+', 'a,b,,c'))
print(re.split(r'x', 'abc'))
print(re.split(r'(-)', 'a-b'))
print(re.split(r'\d', '1a2'))""")

# ---------------------------------------------------------------- 13
sec('Flags und re.compile()')
expl(r'''#### Flags: `re.IGNORECASE` und `re.MULTILINE`

Mit `flags=...` kann man das Verhalten der Suche ändern:

- `flags=re.IGNORECASE` (kurz `re.I`): Groß- und Kleinschreibung werden **nicht** unterschieden.
- `flags=re.MULTILINE` (kurz `re.M`): `^` und `$` passen am Anfang und Ende **jeder Zeile**, nicht nur des ganzen Textes.
- Mehrere Flags verbindet man mit `|`: `flags=re.I | re.M`.

Das geht bei allen Funktionen: `re.search()`, `re.findall()`, `re.sub()`, `re.split()`, ...''',
     r"""import re

print(re.findall(r'python', 'Python oder PYTHON oder python', flags=re.IGNORECASE))

text = '''Erste Zeile
zweite Zeile
Dritte'''
print(re.findall(r'^\w+', text))
print(re.findall(r'^\w+', text, flags=re.MULTILINE))
print(re.findall(r'^[a-z]\w*', text, flags=re.I | re.M))""")
expl(r'''#### `re.compile()`

`re.compile(muster)` macht aus dem Muster ein **Musterobjekt**. Es hat dieselben Funktionen als Methoden:
`p.search(text)`, `p.fullmatch(text)`, `p.findall(text)`, `p.sub(ersatz, text)`, `p.split(text)`, ...

Das lohnt sich, wenn man dasselbe Muster oft benutzt, und man kann ihm einen sprechenden Namen geben.
Flags gibt man schon bei `re.compile()` an.''',
     r"""import re

plz = re.compile(r'\d{5}')
print(bool(plz.fullmatch('48143')))
print(plz.findall('48143 Münster, 10115 Berlin'))

vokal = re.compile(r'[aeiou]', flags=re.IGNORECASE)
print(vokal.sub('_', 'Auto'))""")

tm("Prüfe mit `flags=re.IGNORECASE`, welche Texte `ja` in beliebiger Schreibweise enthalten.",
   "['Ja', 'JA!', 'nein', 'jaja', 'Na jA']", r'ja', """for text in texte:
    print(text, bool(re.search(muster, text, flags=re.IGNORECASE)))""")
t('Zähle, wie oft das Wort `der` (als ganzes Wort, in beliebiger Schreibweise) in `satz` vorkommt.',
  "import re\nsatz = 'Der Hund der Nachbarin und DER Kater oder der Vogel.'",
  r"print(len(re.findall(r'\bder\b', satz, flags=re.IGNORECASE)))")
t('Gib mit `re.MULTILINE` eine Liste aller Zahlen aus, die am Anfang einer Zeile stehen.',
  """import re
einkauf = '''3 Eier
500 g Mehl
Zucker 200 g
2 Liter Milch'''""",
  r"print(re.findall(r'^\d+', einkauf, flags=re.MULTILINE))")
t('Gib mit `re.MULTILINE` eine Liste der Aufzählungspunkte aus: Zeilen, die mit `- ` beginnen, ohne das `- `.',
  """import re
notizen = '''Einkaufen:
- Brot
- Käse
Nicht vergessen - Schlüssel!
- Äpfel'''""",
  r"print(re.findall(r'^- (.*)$', notizen, flags=re.MULTILINE))")
t('Zähle, wie viele Zeilen in `antworten` genau `ja` sind (in beliebiger Schreibweise). Verwende beide Flags.',
  """import re
antworten = '''Ja
nein
JA
ja, gerne
ja'''""",
  r"print(len(re.findall(r'^ja$', antworten, flags=re.I | re.M)))")
t('Gib mit `re.MULTILINE` und `re.sub()` den Text aus, wobei vor jeder Zeile `> ` steht (wie bei einem Zitat in einer E-Mail).',
  """import re
text = '''Hallo Anna,
wie geht es dir?
Viele Grüße'''""",
  r"print(re.sub(r'^', '> ', text, flags=re.MULTILINE))")
t(r'''Erstelle mit `re.compile()` ein Musterobjekt `email` für einfache E-Mail-Adressen (wie in Abschnitt 8).
Prüfe damit jede Adresse mit `email.fullmatch()`.''',
  "import re\nadressen = ['anna@schule.de', 'tom@web', 'max.m@gmx.net', '@leer.de']",
  r"""email = re.compile(r'[\w.-]+@[\w-]+\.\w+')
for a in adressen:
    print(a, bool(email.fullmatch(a)))""")
t(r'Erstelle mit `re.compile()` ein Musterobjekt für Leerraum (`\s+`) und ersetze damit in jedem Text jede Folge von Leerraum durch ein Leerzeichen.',
  "import re\ntexte = ['a   b', 'c\\t\\td', 'e \\n f']",
  r"""leer = re.compile(r'\s+')
for text in texte:
    print(leer.sub(' ', text))""")
predict(r"""import re
p = re.compile(r'[aeiou]', flags=re.IGNORECASE)
print(p.findall('Auto'))
print(len(p.findall('INFORMATIK')))
print(p.sub('_', 'Hallo'))
print(bool(p.match('Ball')))""")

# ---------------------------------------------------------------- 14
sec('Gemischte Übungen')
t('''Schreibe eine Funktion `ist_sicher(passwort)`, die `True` zurückgibt, wenn das Passwort mindestens 8 Zeichen lang ist
und mindestens einen Großbuchstaben, einen Kleinbuchstaben, eine Ziffer und ein Sonderzeichen (kein Wortzeichen) enthält.
Verwende für jede Bedingung ein eigenes `re.search()`.''',
  "import re\npasswoerter = ['Hallo123!', 'hallo123!', 'HALLO123!', 'Hallo!!!', 'Ha1!', 'Sommer#2024']",
  r"""def ist_sicher(passwort):
    return (len(passwort) >= 8
            and bool(re.search(r'[A-Z]', passwort))
            and bool(re.search(r'[a-z]', passwort))
            and bool(re.search(r'\d', passwort))
            and bool(re.search(r'\W', passwort)))

for pw in passwoerter:
    print(pw, ist_sicher(pw))""")
tm(r"""Eine Handynummer beginnt hier mit `015`, `016` oder `017`, danach eine weitere Ziffer, dann optional ein Leerzeichen oder `/`
und danach 7 oder 8 Ziffern. Prüfe mit `re.fullmatch()`.""",
   "['0171 1234567', '0151/12345678', '01701234567', '0251 123456', '0171 12345']", r'01[5-7]\d[ /]?\d{7,8}', FULL)
t('''Werte das Log aus: Zähle mit einem Dictionary, wie oft jede Stufe (`INFO`, `WARNUNG`, `FEHLER`) vorkommt.
Verwende eine benannte Gruppe `stufe`.''',
  """import re
log = ['2025-03-01 12:00:01 INFO Start',
       '2025-03-01 12:00:05 WARNUNG Speicher knapp',
       '2025-03-01 12:01:10 INFO Datei gespeichert',
       '2025-03-01 12:02:00 FEHLER Platte voll',
       '2025-03-01 12:02:30 INFO Neustart']""",
  r"""anzahl = {}
for zeile in log:
    m = re.search(r'\d{2}:\d{2}:\d{2} (?P<stufe>[A-Z]+)', zeile)
    stufe = m.group('stufe')
    anzahl[stufe] = anzahl.get(stufe, 0) + 1
print(anzahl)""")
t('Gib aus dem Log oben nur die Uhrzeit und die Meldung der Zeilen mit `FEHLER` oder `WARNUNG` aus, wie unten.',
  """import re
log = ['2025-03-01 12:00:01 INFO Start',
       '2025-03-01 12:00:05 WARNUNG Speicher knapp',
       '2025-03-01 12:01:10 INFO Datei gespeichert',
       '2025-03-01 12:02:00 FEHLER Platte voll',
       '2025-03-01 12:02:30 INFO Neustart']""",
  r"""for zeile in log:
    m = re.search(r'(\d{2}:\d{2}:\d{2}) (?:FEHLER|WARNUNG) (.*)', zeile)
    if m:
        print(m.group(1), m.group(2))""")
t('''Zerlege jede Webadresse in Protokoll, Rechnername und Pfad. Der Pfad beginnt beim ersten `/` nach dem Rechnernamen
und kann fehlen. Gib die drei Teile mit `m.groups()` aus.''',
  "import re\nadressen = ['https://www.schule.de/info/index.html', 'http://example.com']",
  r"""for adresse in adressen:
    m = re.fullmatch(r'(\w+)://([^/]+)(/.*)?', adresse)
    print(m.groups())""")
t('''Zähle mit `re.findall()` und einem Dictionary, wie oft jedes Wort in `text` vorkommt. Groß- und Kleinschreibung sollen
keine Rolle spielen (verwende `text.lower()`). Gib das Dictionary aus.''',
  "import re\ntext = 'Der Ball, der Hund und DER Ball. Ein Hund!'",
  r"""anzahl = {}
for wort in re.findall(r'\w+', text.lower()):
    anzahl[wort] = anzahl.get(wort, 0) + 1
print(anzahl)""")
t('''Fülle die Vorlage aus: Ersetze jedes `{name}` durch den passenden Wert aus `daten`. Verwende `re.sub()` mit einer Funktion.
Die geschweiften Klammern musst du escapen.''',
  """import re
vorlage = 'Hallo {name}, du bist {alter} Jahre alt und wohnst in {stadt}.'
daten = {'name': 'Lea', 'alter': '16', 'stadt': 'Münster'}""",
  r"""def einsetzen(m):
    return daten[m.group(1)]

print(re.sub(r'\{(\w+)\}', einsetzen, vorlage))""")
t(r'''Die Beträge in `text` haben Tausenderpunkte. Finde alle Beträge mit `\d{1,3}(?:\.\d{3})*`, entferne die Punkte mit `re.sub()`
und gib die Summe aus.''',
  "import re\ntext = 'Miete 1.250 €, Auto 30 €, Haus 312.000 €, Lotto 1.000.000 €'",
  r"""summe = 0
for betrag in re.findall(r'\d{1,3}(?:\.\d{3})*', text):
    summe += int(re.sub(r'\.', '', betrag))
print(summe)""")
tm(r"""Gib nur die Dateinamen aus, die die Form `bild_` + drei Ziffern + `.jpg` oder `.png` haben.
Groß- und Kleinschreibung soll keine Rolle spielen.""",
   "['bild_001.jpg', 'bild_12.jpg', 'bild_123.PNG', 'Bild_007.png', 'bild_999.gif', 'bild_042.jpg.zip']",
   r'bild_\d{3}\.(jpg|png)', """for text in texte:
    if re.fullmatch(muster, text, flags=re.IGNORECASE):
        print(text)""")
t(r'''Schreibe den ersten Buchstaben jedes Satzes groß. Ein Satz beginnt am Anfang des Textes oder nach `.`, `!` oder `?`
und einem Leerzeichen. Verwende `(^|[.!?] )(\w)` und eine Funktion.''',
  "import re\ntext = 'hallo. wie geht es dir? gut! danke.'",
  r"""def gross(m):
    return m.group(1) + m.group(2).upper()

print(re.sub(r'(^|[.!?] )(\w)', gross, text))""")
t('Gib mit `re.findall()` die Punkte als Liste von Zahlen-Tupeln aus. Die Zahlen können negativ sein. Gib danach die Summe aller x-Werte aus.',
  "import re\ntext = 'P(3, 4) Q(10, -2) R(-5, 7)'",
  r"""punkte = []
for x, y in re.findall(r'\((-?\d+), (-?\d+)\)', text):
    punkte.append((int(x), int(y)))
print(punkte)
summe = 0
for x, y in punkte:
    summe += x
print(summe)""")
t('In `text` werden Namen und Noten mit `:` oder `=` und verschieden vielen Leerzeichen getrennt. Erstelle ein Dictionary Name → Note (als `int`).',
  "import re\ntext = 'Anna: 2; Ben=1, Cem : 3;Dana   =  2'",
  r"""noten = {}
for name, note in re.findall(r'(\w+)\s*[:=]\s*(\d+)', text):
    noten[name] = int(note)
print(noten)""")
t(r'Entferne mit **einem** `re.sub()` den Leerraum am Anfang und am Ende von `text`. Tipp: `^\s+|\s+$`. Gib das Ergebnis in eckigen Klammern aus.',
  "import re\ntext = '   \\t Hallo Welt  \\n'",
  r"""print('[' + re.sub(r'^\s+|\s+$', '', text) + ']')""")
t(r'''Suche in `text` alle Kfz-Kennzeichen (1 bis 3 Großbuchstaben, Bindestrich, 1 bis 2 Großbuchstaben, Leerzeichen, 1 bis 4 Ziffern)
und gib sie als Liste aus. Verwende `\b` am Anfang und am Ende.''',
  "import re\ntext = 'Gesehen: MS-AB 123, B-X 7, mS-AB 12, K-LM 12345 und HH-Z 9999.'",
  r"print(re.findall(r'\b[A-Z]{1,3}-[A-Z]{1,2} \d{1,4}\b', text))")
t('''Prüfe für jede Zeile, ob sie ein gültiges Datum im Format `TT.MM.JJJJ` ist (Tag `01`-`31`, Monat `01`-`12`).
Gib bei gültigen Daten das Datum im Format `JJJJ-MM-TT` aus, sonst `ungültig`. Ob es den Tag im Monat wirklich gibt, prüfst du nicht.''',
  "import re\ndaten = ['24.12.2024', '32.01.2024', '15.13.2024', '01.01.2000', '1.1.2000']",
  r"""for datum in daten:
    m = re.fullmatch(r'(0[1-9]|[12]\d|3[01])\.(0[1-9]|1[0-2])\.(\d{4})', datum)
    if m:
        print(f'{m.group(3)}-{m.group(2)}-{m.group(1)}')
    else:
        print('ungültig')""")
predict(r"""import re
text = 'a1b22c333'
print(re.findall(r'[a-z]\d+', text))
print(re.findall(r'[a-z](\d+)', text))
print(re.sub(r'\d+', '#', text))
print(re.split(r'\d+', text))
print(re.search(r'\d{2}', text).span())""")

generate('regulaereAusdruecke', 'Reguläre Ausdrücke', INTRO)
