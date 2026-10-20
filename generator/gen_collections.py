# Erzeugt ../content/collections.ipynb (siehe nbgen.py).
#
# Reihenfolge: nach itertools (lambda ist dort erklärt). Sets aus Zeichenketten nie direkt ausgeben (sorted),
# die Ausgabe von Counter ist nach Häufigkeit geordnet, bei gleicher Anzahl nach dem ersten Auftreten (deterministisch).
from nbgen import sec, expl, task, predict, generate


def t(text, given='', body='', kind='normal'):
    """Aufgabe, deren Lösung aus dem vorgegebenen Code plus body besteht."""
    task(text, given=given, solution=(given + '\n' + body) if given else body, kind=kind)


INTRO = '''Das Modul `collections` enthält **besondere Datentypen**, die Listen, Tupel und Dictionaries ergänzen:

- `Counter` zählt, wie oft etwas vorkommt.
- `defaultdict` ist ein Dictionary, das fehlende Schlüssel selbst anlegt.
- `namedtuple` ist ein Tupel, dessen Elemente Namen haben.
- `deque` ist eine Art Liste, an der man vorne **und** hinten schnell anfügen und entfernen kann.
- `OrderedDict` und `ChainMap` sind zwei weitere Arten von Dictionaries.

Du solltest Listen, Tupel, Dictionaries, Sets und Funktionen schon kennen. `lambda` kennst du aus dem Notebook zu `itertools`.

Jeder Abschnitt beginnt mit kurzen Erklärungen und Beispielen. Führe die Beispiele aus und probiere sie ruhig ein wenig aus.
Danach folgen viele kleine Übungen. Wenn etwas vorgegeben ist, steht es schon in der Codezelle.'''

# ---------------------------------------------------------------- 1
sec('Zählen mit Counter')
expl('''#### `Counter` erstellen

Ein `Counter` zählt, wie oft jedes Element vorkommt. Man importiert ihn mit `from collections import Counter`.

- `Counter(liste)` zählt die Elemente einer Liste, `Counter(text)` die Zeichen einer Zeichenkette.
- Bei der Ausgabe mit `print()` stehen die **häufigsten Elemente zuerst**. Kommen zwei Elemente gleich oft vor,
  steht das zuerst, das auch im Text oder in der Liste zuerst vorkommt.''',
     """from collections import Counter

c = Counter(['rot', 'blau', 'rot', 'grün', 'rot', 'blau'])
print(c)
print(Counter('banane'))""")
expl('''#### Auf die Anzahlen zugreifen

Ein `Counter` ist ein **Dictionary**: Die Elemente sind die Schlüssel, die Anzahlen die Werte.

- `c[element]` gibt die Anzahl zurück. Kommt das Element gar nicht vor, ist das Ergebnis `0`, es gibt **keinen** `KeyError`.
- `len(c)` ist die Anzahl der **verschiedenen** Elemente, `c.total()` die Summe aller Anzahlen.
- `element in c` prüft, ob das Element vorkommt.''',
     """from collections import Counter

c = Counter('mississippi')
print(c['s'])
print(c['x'])
print(len(c))
print(c.total())
print('p' in c, 'x' in c)""")
expl('''#### Schleifen über einen Counter

Wie bei einem Dictionary gibt es `keys()`, `values()` und `items()`. Eine Schleife durchläuft die Elemente in der Reihenfolge,
in der sie **zuerst vorkommen** (nicht nach Häufigkeit). Mit `sorted(c)` erhält man die Elemente sortiert.

Mit `dict(c)` wird aus dem Counter ein gewöhnliches Dictionary.''',
     """from collections import Counter

c = Counter('abracadabra')
for buchstabe, anzahl in c.items():
    print(buchstabe, anzahl)
print(sorted(c))
print(dict(c))""")
expl('''#### Wörter zählen und Counter von Hand angeben

- Wörter zählt man mit `Counter(text.split())`.
- Einen Counter kann man auch direkt angeben: `Counter({'a': 2, 'b': 1})` oder `Counter(a=2, b=1)`.
- Mit `==` vergleicht man einen Counter wie ein Dictionary: `Counter('ab') == {'a': 1, 'b': 1}` ist `True`.''',
     """from collections import Counter

satz = 'der Hund und der Hase und die Katze'
print(Counter(satz.split()))
print(Counter(a=2, b=1))
print(Counter('ab') == {'a': 1, 'b': 1})""")

t('Zähle mit `Counter` die Buchstaben im Wort `wort` und gib den Counter aus.',
  "from collections import Counter\nwort = 'ananas'",
  "print(Counter(wort))")
t('Gib aus, wie oft der Buchstabe `e` in `text` vorkommt. Verwende einen `Counter`.',
  "from collections import Counter\ntext = 'beethovens erste sinfonie'",
  """c = Counter(text)
print(c['e'])""")
t('Gib aus, wie oft der Buchstabe `z` in `text` vorkommt (auch wenn er gar nicht vorkommt).',
  "from collections import Counter\ntext = 'beethovens erste sinfonie'",
  """c = Counter(text)
print(c['z'])""")
t('Zähle die Noten in `noten`. Gib aus, wie viele Einsen und wie viele Sechsen es gibt.',
  "from collections import Counter\nnoten = [2, 3, 1, 2, 4, 1, 2, 3, 5, 1, 2]",
  """c = Counter(noten)
print('Einsen:', c[1])
print('Sechsen:', c[6])""")
t('Zähle die Wörter in `satz` und gib aus, wie oft `die` vorkommt.',
  "from collections import Counter\nsatz = 'die Katze und die Maus und die Ente'",
  """c = Counter(satz.split())
print(c['die'])""")
t('Gib aus, wie viele **verschiedene** Zahlen in `wuerfe` vorkommen.',
  "from collections import Counter\nwuerfe = [3, 6, 2, 6, 6, 1, 3, 2, 6]",
  """c = Counter(wuerfe)
print(len(c))""")
t('Zähle die Tiere in `tiere`. Gib die Gesamtzahl der Tiere mit `total()` aus und danach die Anzahl der verschiedenen Tierarten.',
  "from collections import Counter\ntiere = ['Kuh', 'Huhn', 'Huhn', 'Schwein', 'Huhn', 'Kuh']",
  """c = Counter(tiere)
print(c.total())
print(len(c))""")
t('Gib jede Farbe mit ihrer Anzahl in der Form `rot: 3` aus, in der Reihenfolge, in der die Farben zuerst vorkommen.',
  "from collections import Counter\nfarben = ['rot', 'gelb', 'rot', 'blau', 'gelb', 'rot']",
  """c = Counter(farben)
for farbe, anzahl in c.items():
    print(f'{farbe}: {anzahl}')""")
t('Gib die Buchstaben von `wort` mit ihrer Anzahl **alphabetisch sortiert** aus, jeweils in der Form `a 2`.',
  "from collections import Counter\nwort = 'banane'",
  """c = Counter(wort)
for b in sorted(c):
    print(b, c[b])""")
t('Prüfe mit `in`, ob in `text` ein `q` vorkommt und ob ein `x` vorkommt. Gib jeweils `True` oder `False` aus.',
  "from collections import Counter\ntext = 'quadratische gleichung'",
  """c = Counter(text)
print('q' in c)
print('x' in c)""")
t('Gib alle Buchstaben von `wort`, die **mindestens zweimal** vorkommen, als alphabetisch sortierte Liste aus.',
  "from collections import Counter\nwort = 'abrakadabra'",
  """c = Counter(wort)
mehrfach = []
for b in c:
    if c[b] >= 2:
        mehrfach.append(b)
print(sorted(mehrfach))""")
t('''Zähle die Buchstaben in `name`, ohne Groß- und Kleinschreibung zu unterscheiden (wandle vorher mit `lower()` um).
Gib aus, wie oft `a` vorkommt.''',
  "from collections import Counter\nname = 'Anna Aaronson'",
  """c = Counter(name.lower())
print(c['a'])""")
t('Gib für jede Augenzahl von 1 bis 6 aus, wie oft sie in `wuerfe` vorkommt, auch wenn sie gar nicht vorkommt. Form: `1: 2`.',
  "from collections import Counter\nwuerfe = [3, 6, 2, 6, 6, 1, 3, 2, 6, 1]",
  """c = Counter(wuerfe)
for augen in range(1, 7):
    print(f'{augen}: {c[augen]}')""")
t('''Zähle die Buchstaben in `wort` einmal mit einem `Counter` und einmal „von Hand“ mit einem gewöhnlichen Dictionary
und `get()`. Gib das Dictionary aus und danach, ob beide mit `==` gleich sind.''',
  "from collections import Counter\nwort = 'kokosnuss'",
  """d = {}
for b in wort:
    d[b] = d.get(b, 0) + 1
print(d)
print(Counter(wort) == d)""")
t('''Gib für jede Stimme in `stimmen` aus, wie viel Prozent der Stimmen sie bekommen hat, mit einer Nachkommastelle
und in der Reihenfolge, in der die Namen zuerst vorkommen. Form: `Ali: 40.0 %`.''',
  "from collections import Counter\nstimmen = ['Ali', 'Bea', 'Ali', 'Cem', 'Bea', 'Ali', 'Bea', 'Bea', 'Ali', 'Cem']",
  """c = Counter(stimmen)
for name, anzahl in c.items():
    print(f'{name}: {anzahl / c.total() * 100:.1f} %')""")
predict("""from collections import Counter
c = Counter('abba')
print(c['a'], c['c'])
print(len(c), c.total())""")
predict("""from collections import Counter
print(Counter('mississippi'))""")
predict("""from collections import Counter
c = Counter([1, 2, 2, 3, 3, 3])
print(sorted(c.values()))
print(c[4] + c[3])""")

# ---------------------------------------------------------------- 2
sec('most_common() und elements()')
expl('''#### Die häufigsten Elemente: `most_common()`

`c.most_common(n)` gibt eine **Liste von Tupeln** `(element, anzahl)` zurück, die häufigsten zuerst, höchstens `n` Stück.
Ohne `n` erhält man alle Elemente. Bei gleicher Anzahl gilt wieder: Was zuerst vorkommt, steht vorne.

Das häufigste Element mit seiner Anzahl erhält man mit `c.most_common(1)[0]`. Das Tupel kann man gleich **entpacken**.''',
     """from collections import Counter

c = Counter('abracadabra')
print(c.most_common(2))
print(c.most_common())
buchstabe, anzahl = c.most_common(1)[0]
print(buchstabe, anzahl)""")
expl('''#### Die einzelnen Elemente: `elements()`

`c.elements()` liefert jedes Element **so oft, wie es gezählt wurde**. Das Ergebnis ist ein Iterator,
deshalb wandelt man es mit `list()` oder `sorted()` um oder verbindet es mit `''.join()`. Elemente mit Anzahl 0 fallen weg.''',
     """from collections import Counter

c = Counter({'x': 3, 'y': 1, 'z': 0})
print(list(c.elements()))
print(''.join(c.elements()))
print(sorted(Counter('banane').elements()))""")

t('Gib die drei häufigsten Wörter in `text` mit ihrer Anzahl aus (als Liste von Tupeln).',
  "from collections import Counter\ntext = 'ich weiß dass ich nichts weiß und ich weiß dass das so ist'",
  """c = Counter(text.split())
print(c.most_common(3))""")
t('Gib den häufigsten Buchstaben in `wort` und seine Anzahl in der Form `s kommt 4-mal vor` aus.',
  "from collections import Counter\nwort = 'mississippi'",
  """c = Counter(wort)
b, anzahl = c.most_common(1)[0]
print(f'{b} kommt {anzahl}-mal vor')""")
t('Gib die häufigste Note in `noten` aus.',
  "from collections import Counter\nnoten = [3, 2, 2, 4, 1, 3, 2, 5, 3, 2]",
  """c = Counter(noten)
print(c.most_common(1)[0][0])""")
t('Gib eine Rangliste der Lieblingsfächer aus, die häufigsten zuerst, in der Form `1. Sport (4)`.',
  "from collections import Counter\nfaecher = ['Sport', 'Kunst', 'Mathe', 'Sport', 'Kunst', 'Sport', 'Informatik', 'Sport', 'Mathe', 'Informatik', 'Informatik']",
  """c = Counter(faecher)
for platz, (fach, anzahl) in enumerate(c.most_common(), 1):
    print(f'{platz}. {fach} ({anzahl})')""")
t('Gib die drei häufigsten Buchstaben in `satz` aus, **ohne** die Leerzeichen mitzuzählen (entferne sie vorher mit `replace()`).',
  "from collections import Counter\nsatz = 'alle meine entchen schwimmen auf dem see'",
  """c = Counter(satz.replace(' ', ''))
print(c.most_common(3))""")
t('Gib das **seltenste** Element von `zahlen` mit seiner Anzahl aus. Es steht in `most_common()` ganz hinten.',
  "from collections import Counter\nzahlen = [4, 7, 4, 1, 7, 4, 7, 1, 9, 4]",
  """c = Counter(zahlen)
print(c.most_common()[-1])""")
t('Wer hat die Wahl gewonnen? Gib den Namen und die Anzahl der Stimmen aus, in der Form `Gewinner: Bea mit 5 Stimmen`.',
  "from collections import Counter\nstimmen = ['Ali', 'Bea', 'Ali', 'Cem', 'Bea', 'Ali', 'Bea', 'Bea', 'Cem', 'Bea']",
  """c = Counter(stimmen)
name, anzahl = c.most_common(1)[0]
print(f'Gewinner: {name} mit {anzahl} Stimmen')""")
t('Gib die Elemente von `c` mit `elements()` als Liste aus.',
  "from collections import Counter\nc = Counter({'Apfel': 2, 'Birne': 1, 'Kiwi': 3})",
  "print(list(c.elements()))")
t("Bilde aus dem Counter `c` mit `elements()` und `''.join()` die Zeichenkette `aaabbc` und gib sie aus.",
  "from collections import Counter\nc = Counter(a=3, b=2, c=1)",
  "print(''.join(c.elements()))")
t('Gib die Buchstaben von `wort` alphabetisch sortiert als Zeichenkette aus. Verwende `elements()`, `sorted()` und `join()`.',
  "from collections import Counter\nwort = 'informatik'",
  """c = Counter(wort)
print(''.join(sorted(c.elements())))""")
t('''Zwei Wörter sind **Anagramme**, wenn sie aus denselben Buchstaben bestehen (z. B. `lager` und `regal`).
Gib für jedes Paar in `paare` aus, ob die beiden Wörter Anagramme sind. Vergleiche dazu zwei Counter mit `==`.''',
  "from collections import Counter\npaare = [('lager', 'regal'), ('ampel', 'lampe'), ('rasen', 'sahne'), ('esel', 'seele')]",
  """for a, b in paare:
    print(a, b, Counter(a) == Counter(b))""")
t('Gib das häufigste Wort in `text` aus, das **mindestens vier Buchstaben** hat. Sammle diese Wörter zuerst in einer Liste.',
  "from collections import Counter\ntext = 'der Ball rollt und der Ball springt und der Hund holt den Ball und rollt ihn zurück'",
  """lange = []
for w in text.split():
    if len(w) >= 4:
        lange.append(w)
print(Counter(lange).most_common(1)[0][0])""")
t('Gib alle Zahlen aus `zahlen` aus, die genau so oft vorkommen wie die häufigste Zahl, als sortierte Liste.',
  "from collections import Counter\nzahlen = [5, 3, 5, 8, 3, 1, 8, 5, 3, 8]",
  """c = Counter(zahlen)
hoechste = c.most_common(1)[0][1]
haeufigste = []
for z in c:
    if c[z] == hoechste:
        haeufigste.append(z)
print(sorted(haeufigste))""")
predict("""from collections import Counter
c = Counter('hallo welt')
print(c.most_common(2))""")
predict("""from collections import Counter
c = Counter({'b': 2, 'a': 1, 'c': 0})
print(list(c.elements()))
print(len(c))""")

# ---------------------------------------------------------------- 3
sec('Counter ändern und verrechnen')
expl('''#### Anzahlen ändern

- `c[element] += 1` erhöht eine Anzahl. Das geht auch, wenn das Element noch nicht vorkommt (es startet bei 0).
  Deshalb kann man mit einem leeren `Counter()` und einer Schleife selbst zählen.
- `c.update(liste)` zählt die Elemente der Liste **dazu**. `c.update(anderer_counter)` addiert die Anzahlen.
- `c.subtract(...)` zieht ab. Dabei können Anzahlen 0 oder **negativ** werden.
- `del c[element]` entfernt ein Element ganz.''',
     """from collections import Counter

c = Counter()
for w in ['ja', 'nein', 'ja']:
    c[w] += 1
print(c)
c.update(['ja', 'vielleicht'])
print(c)
c.subtract({'nein': 3})
print(c)
del c['vielleicht']
print(c)""")
expl('''#### Counter verrechnen: `+`, `-`, `&`, `|`

Zwei Counter kann man miteinander verrechnen. Im Ergebnis bleiben nur Elemente mit einer Anzahl **größer als 0**.

| Rechnung | Ergebnis |
|---|---|
| `a + b` | Anzahlen addieren |
| `a - b` | Anzahlen abziehen, was 0 oder kleiner wird, fällt weg |
| `a & b` | jeweils das **Minimum** (was in beiden vorkommt) |
| <code>a &#124; b</code> | jeweils das **Maximum** |

Der Unterschied: `a.subtract(b)` ändert `a` selbst und behält negative Anzahlen, `a - b` erzeugt einen neuen Counter.''',
     """from collections import Counter

a = Counter('aabbbc')
b = Counter('abd')
print(a + b)
print(a - b)
print(a & b)
print(a | b)""")

t('Zähle die Wörter in `woerter` selbst mit einem leeren `Counter()` und `+= 1` in einer Schleife. Gib den Counter aus.',
  "from collections import Counter\nwoerter = ['eins', 'zwei', 'eins', 'drei', 'eins', 'zwei']",
  """c = Counter()
for w in woerter:
    c[w] += 1
print(c)""")
t('Zähle die **Längen** der Wörter in `woerter` mit einem `Counter` (Schlüssel ist die Länge). Gib den Counter aus.',
  "from collections import Counter\nwoerter = ['Hut', 'Hose', 'Mantel', 'Schal', 'Rock', 'Bluse', 'Kleid', 'Top']",
  """c = Counter()
for w in woerter:
    c[len(w)] += 1
print(c)""")
t('Im Lager liegt der Bestand `lager`. Es kommt eine Lieferung `lieferung` dazu. Aktualisiere das Lager mit `update()` und gib es aus.',
  "from collections import Counter\nlager = Counter({'Stifte': 20, 'Hefte': 5, 'Lineale': 3})\nlieferung = {'Hefte': 30, 'Radierer': 10}",
  """lager.update(lieferung)
print(lager)""")
t('Im Laden wurde `verkauft`. Ziehe die verkauften Teile mit `subtract()` vom Lager ab und gib das Lager aus.',
  "from collections import Counter\nlager = Counter({'Stifte': 20, 'Hefte': 35, 'Radierer': 10})\nverkauft = ['Stifte', 'Hefte', 'Stifte', 'Radierer', 'Stifte']",
  """lager.subtract(verkauft)
print(lager)""")
t('''Es wurden mehr Teile bestellt als im Lager sind. Ziehe die Bestellung mit `subtract()` ab und gib danach
alle Artikel mit negativem Bestand in der Form `Hefte fehlen: 5` aus.''',
  "from collections import Counter\nlager = Counter({'Stifte': 4, 'Hefte': 10, 'Mappen': 2})\nbestellung = {'Stifte': 3, 'Hefte': 15, 'Mappen': 6}",
  """lager.subtract(bestellung)
for artikel, anzahl in lager.items():
    if anzahl < 0:
        print(f'{artikel} fehlen: {-anzahl}')""")
t('Im Zoo wurden an zwei Tagen Besucher gezählt. Gib mit `+` aus, wie viele es an beiden Tagen zusammen waren.',
  "from collections import Counter\nmontag = Counter({'Kinder': 120, 'Erwachsene': 80})\ndienstag = Counter({'Kinder': 95, 'Erwachsene': 110, 'Gruppen': 3})",
  "print(montag + dienstag)")
t('''Für ein Rezept braucht man `rezept`, zu Hause ist `vorrat`. Gib mit `-` aus, was man noch einkaufen muss.''',
  "from collections import Counter\nrezept = Counter({'Eier': 4, 'Mehl': 2, 'Milch': 1, 'Zucker': 1})\nvorrat = Counter({'Eier': 2, 'Mehl': 3, 'Zucker': 1})",
  "print(rezept - vorrat)")
t('''Kann man das Wort `wort` aus den Buchstabenplättchen `plaettchen` legen? Das geht genau dann, wenn
`Counter(wort) - Counter(plaettchen)` leer ist, also die Länge 0 hat. Gib für jedes Wort in `woerter` aus, ob es geht.''',
  "from collections import Counter\nplaettchen = 'eanrtsel'\nwoerter = ['rest', 'tanne', 'leser', 'traen', 'salter']",
  """for wort in woerter:
    fehlt = Counter(wort) - Counter(plaettchen)
    print(wort, len(fehlt) == 0)""")
t('''Welche Buchstaben haben die beiden Wörter gemeinsam (mit Vielfachheit)? Bilde `Counter(a) & Counter(b)` und gib
die Buchstaben mit `elements()` als sortierte Liste aus.''',
  "from collections import Counter\na = 'banane'\nb = 'ananas'",
  """gemeinsam = Counter(a) & Counter(b)
print(sorted(gemeinsam.elements()))""")
t('''Zwei Personen packen für dieselbe Reise. Die gemeinsame Packliste soll von jedem Gegenstand so viele enthalten,
wie die Person braucht, die am meisten davon braucht. Gib die Liste mit `|` aus.''',
  "from collections import Counter\nmia = Counter({'T-Shirt': 5, 'Hose': 2, 'Pulli': 1})\nnoah = Counter({'T-Shirt': 3, 'Hose': 3, 'Mütze': 1})",
  "print(mia | noah)")
t('Gib aus, wie viele Buchstaben man aus `a` streichen muss, damit nur noch Buchstaben übrig bleiben, die auch in `b` vorkommen (mit Vielfachheit). Verwende `-` und `total()`.',
  "from collections import Counter\na = 'programmieren'\nb = 'regen'",
  """rest = Counter(a) - Counter(b)
print(rest.total())""")
t('Entferne mit `del` das Leerzeichen (den Schlüssel `\' \'`) aus dem Counter `c`. Gib danach die zwei häufigsten Zeichen aus.',
  "from collections import Counter\nc = Counter('ab ab ab a c')",
  """del c[' ']
print(c.most_common(2))""")
t('''Simuliere 600 Würfe mit einem Würfel: `random.seed(5)`, dann in einer Schleife 600-mal `random.randint(1, 6)`.
Zähle die Ergebnisse mit einem `Counter` und gib für jede Augenzahl von 1 bis 6 die Anzahl aus, in der Form `1: 98`.''',
  "import random\nfrom collections import Counter\nrandom.seed(5)",
  """c = Counter()
for i in range(600):
    c[random.randint(1, 6)] += 1
for augen in range(1, 7):
    print(f'{augen}: {c[augen]}')""")
predict("""from collections import Counter
a = Counter('aab')
b = Counter('bc')
print(a + b)
print(a - b)""")
predict("""from collections import Counter
c = Counter('aab')
c.subtract('abb')
print(c['a'], c['b'], c['c'])""")
predict("""from collections import Counter
c = Counter()
c['x'] += 2
c['y'] -= 1
c.update(['x', 'z'])
print(c['x'], c['y'], c['z'], len(c))""")

# ---------------------------------------------------------------- 4
sec('defaultdict')
expl('''#### Das Problem mit fehlenden Schlüsseln

Bei einem gewöhnlichen Dictionary gibt `d[schluessel] += 1` einen `KeyError`, wenn es den Schlüssel noch nicht gibt.
Deshalb braucht man `get()` oder eine `if`-Abfrage.

Ein `defaultdict` legt einen fehlenden Schlüssel **automatisch** an, mit einem Startwert. Dafür gibt man ihm eine Funktion,
die den Startwert erzeugt:

| Aufruf | Startwert |
|---|---|
| `defaultdict(int)` | `int()` ist `0` |
| `defaultdict(list)` | `list()` ist `[]` |
| `defaultdict(set)` | `set()` ist eine leere Menge |
| `defaultdict(str)` | `str()` ist `''` |

Man gibt nur den **Namen** an, ohne Klammern (wie bei `key=`).''',
     """from collections import defaultdict

print(int(), list(), str())
d = defaultdict(int)
for b in 'hallo':
    d[b] += 1
print(d)
print(dict(d))""")
expl('''#### Ausgabe und Lesen

- `print(d)` zeigt `defaultdict(<class 'int'>, {...})`. Mit `print(dict(d))` sieht die Ausgabe aus wie bei einem Dictionary.
- **Achtung:** Schon das **Lesen** eines fehlenden Schlüssels mit `d[schluessel]` legt ihn an!
  Ob ein Schlüssel vorhanden ist, prüft man deshalb mit `in` (oder mit `get()`): Das legt nichts an.''',
     """from collections import defaultdict

d = defaultdict(int)
d['a'] += 5
print('b' in d)
print(d['b'])
print('b' in d)
print(dict(d))""")
expl('''#### Gruppieren mit `defaultdict(list)` und `defaultdict(set)`

Mit `defaultdict(list)` kann man Elemente in Gruppen sammeln: `d[gruppe].append(element)`.
Gibt es die Gruppe noch nicht, beginnt sie mit einer leeren Liste. `defaultdict(set)` sammelt ohne Doppelte mit `add()`.

Sets aus Zeichenketten werden in zufälliger Reihenfolge ausgegeben, deshalb gibt man sie mit `sorted()` aus.''',
     """from collections import defaultdict

tiere = ['Hund', 'Hase', 'Katze', 'Huhn', 'Kuh']
gruppen = defaultdict(list)
for tier in tiere:
    gruppen[tier[0]].append(tier)
print(dict(gruppen))

besuche = defaultdict(set)
for name, tag in [('Ali', 'Mo'), ('Bea', 'Mo'), ('Ali', 'Di'), ('Ali', 'Mo')]:
    besuche[name].add(tag)
print(sorted(besuche['Ali']))""")
expl('''#### Eigene Startwerte mit `lambda`

Statt `int` oder `list` kann man jede Funktion ohne Parameter angeben, zum Beispiel eine `lambda`-Funktion:
`defaultdict(lambda: 'unbekannt')` gibt für fehlende Schlüssel `'unbekannt'` zurück.''',
     """from collections import defaultdict

farbe = defaultdict(lambda: 'unbekannt')
farbe['Banane'] = 'gelb'
print(farbe['Banane'])
print(farbe['Kiwi'])""")

t('Zähle die Buchstaben in `wort` mit einem `defaultdict(int)`. Gib das Ergebnis mit `dict()` aus.',
  "from collections import defaultdict\nwort = 'erdbeere'",
  """d = defaultdict(int)
for b in wort:
    d[b] += 1
print(dict(d))""")
t('Zähle die Wörter in `text` mit einem `defaultdict(int)` und gib aus, wie oft `und` vorkommt.',
  "from collections import defaultdict\ntext = 'Brot und Butter und Käse und Wurst'",
  """d = defaultdict(int)
for w in text.split():
    d[w] += 1
print(d['und'])""")
t('Gruppiere die Wörter in `woerter` nach ihrem Anfangsbuchstaben in einem `defaultdict(list)`. Gib das Ergebnis mit `dict()` aus.',
  "from collections import defaultdict\nwoerter = ['Apfel', 'Birne', 'Ananas', 'Banane', 'Kirsche', 'Aprikose']",
  """d = defaultdict(list)
for w in woerter:
    d[w[0]].append(w)
print(dict(d))""")
t('Gruppiere die Wörter nach ihrer **Länge**. Gib die Gruppen nach der Länge sortiert aus, in der Form `3: [\'Hut\', \'Top\']`.',
  "from collections import defaultdict\nwoerter = ['Hut', 'Hose', 'Mantel', 'Schal', 'Rock', 'Bluse', 'Kleid', 'Top']",
  """d = defaultdict(list)
for w in woerter:
    d[len(w)].append(w)
for laenge in sorted(d):
    print(f'{laenge}: {d[laenge]}')""")
t('Gruppiere die Schülerinnen und Schüler nach ihrer Klasse. Gib für jede Klasse (alphabetisch sortiert) die Namen aus, in der Form `10a: Ali, Cem`.',
  "from collections import defaultdict\nschueler = [('Ali', '10a'), ('Bea', '10b'), ('Cem', '10a'), ('Dana', '10c'), ('Emil', '10b'), ('Fiona', '10a')]",
  """d = defaultdict(list)
for name, klasse in schueler:
    d[klasse].append(name)
for klasse in sorted(d):
    print(f"{klasse}: {', '.join(d[klasse])}")""")
t('Addiere die Ausgaben (in Euro) pro Kategorie mit einem `defaultdict(int)`. Gib das Ergebnis mit `dict()` aus.',
  "from collections import defaultdict\nausgaben = [('Essen', 12), ('Kino', 9), ('Essen', 7), ('Bücher', 15), ('Kino', 11), ('Essen', 4)]",
  """summe = defaultdict(int)
for kategorie, betrag in ausgaben:
    summe[kategorie] += betrag
print(dict(summe))""")
t('''Sammle mit einem `defaultdict(set)`, wer in welcher AG ist (ohne Doppelte). Gib für jede AG (alphabetisch) die Namen
als sortierte Liste aus, in der Form `Chor: ['Ali', 'Bea']`.''',
  "from collections import defaultdict\nanmeldungen = [('Chor', 'Bea'), ('Robotik', 'Cem'), ('Chor', 'Ali'), ('Theater', 'Bea'), ('Robotik', 'Ali'), ('Chor', 'Bea')]",
  """ags = defaultdict(set)
for ag, name in anmeldungen:
    ags[ag].add(name)
for ag in sorted(ags):
    print(f'{ag}: {sorted(ags[ag])}')""")
t('Lege ein Telefonbuch an, in dem jede Person mehrere Nummern haben kann (`defaultdict(list)`). Gib danach die Nummern von `Bea` aus.',
  "from collections import defaultdict\neintraege = [('Ali', '0711 123'), ('Bea', '0151 999'), ('Ali', '0170 555'), ('Bea', '07071 42'), ('Bea', '0160 31')]",
  """telefon = defaultdict(list)
for name, nummer in eintraege:
    telefon[name].append(nummer)
print(telefon['Bea'])""")
t('''Die Liste `wege` enthält Wege zwischen Orten. Jeder Weg geht in **beide Richtungen**. Speichere für jeden Ort seine
Nachbarorte in einem `defaultdict(list)` und gib die Nachbarn von `B` und von `D` aus.''',
  "from collections import defaultdict\nwege = [('A', 'B'), ('B', 'C'), ('B', 'D'), ('C', 'D'), ('D', 'E')]",
  """nachbarn = defaultdict(list)
for a, b in wege:
    nachbarn[a].append(b)
    nachbarn[b].append(a)
print(nachbarn['B'])
print(nachbarn['D'])""")
t('''Sammle die Noten pro Fach in einem `defaultdict(list)`. Gib danach für jedes Fach (alphabetisch) den Durchschnitt
mit einer Nachkommastelle aus, in der Form `Deutsch: 2.5`.''',
  "from collections import defaultdict\nnoten = [('Mathe', 2), ('Deutsch', 3), ('Mathe', 1), ('Englisch', 2), ('Deutsch', 2), ('Mathe', 3), ('Englisch', 4)]",
  """d = defaultdict(list)
for fach, note in noten:
    d[fach].append(note)
for fach in sorted(d):
    print(f'{fach}: {sum(d[fach]) / len(d[fach]):.1f}')""")
t('''Hänge mit einem `defaultdict(str)` die Anfangsbuchstaben der Wörter zusammen, gruppiert nach der Wortlänge.
Gib das Ergebnis mit `dict()` aus.''',
  "from collections import defaultdict\nwoerter = ['Haus', 'Auto', 'Baum', 'Igel', 'Tor', 'Ast', 'Rad']",
  """d = defaultdict(str)
for w in woerter:
    d[len(w)] += w[0]
print(dict(d))""")
t('''Lege ein Wörterbuch mit `defaultdict(lambda: '???')` an, in dem die Übersetzungen aus `vokabeln` stehen.
Übersetze damit jedes Wort in `satz` und gib die übersetzten Wörter durch Leerzeichen getrennt aus.''',
  "from collections import defaultdict\nvokabeln = {'der': 'the', 'Hund': 'dog', 'ist': 'is', 'groß': 'big'}\nsatz = 'der Hund ist sehr groß'",
  """woerterbuch = defaultdict(lambda: '???')
for de, en in vokabeln.items():
    woerterbuch[de] = en
uebersetzt = []
for w in satz.split():
    uebersetzt.append(woerterbuch[w])
print(' '.join(uebersetzt))""")
t('''Gruppiere die Wörter in `woerter` nach Anagrammen: Der Schlüssel ist das Wort mit **sortierten** Buchstaben,
also `''.join(sorted(wort))`. Gib nur die Gruppen mit mehr als einem Wort aus, jeweils als Liste.''',
  "from collections import defaultdict\nwoerter = ['lager', 'regal', 'ampel', 'lampe', 'palme', 'hund', 'tor', 'rot', 'ort', 'maus']",
  """gruppen = defaultdict(list)
for w in woerter:
    gruppen[''.join(sorted(w))].append(w)
for gruppe in gruppen.values():
    if len(gruppe) > 1:
        print(gruppe)""")
t('''Zähle für jede Klasse, wie oft jede Note vorkommt: Verwende `defaultdict(Counter)`, dann ist jeder Wert ein eigener
`Counter`, und `d[klasse][note] += 1` funktioniert sofort. Gib für jede Klasse (alphabetisch) die häufigste Note aus.''',
  "from collections import defaultdict, Counter\nnoten = [('10a', 2), ('10b', 3), ('10a', 2), ('10a', 1), ('10b', 3), ('10b', 4), ('10a', 3)]",
  """d = defaultdict(Counter)
for klasse, note in noten:
    d[klasse][note] += 1
for klasse in sorted(d):
    print(klasse, d[klasse].most_common(1)[0][0])""")
predict("""from collections import defaultdict
d = defaultdict(int)
d['a'] += 2
print(d['b'])
print(len(d))
print('c' in d, len(d))""")
predict("""from collections import defaultdict
d = defaultdict(list)
for z in [3, 8, 5, 6, 1]:
    d[z % 2].append(z)
print(dict(d))""")
predict("""d = {}
d['a'] += 1
print(d)""", error=KeyError)

# ---------------------------------------------------------------- 5
sec('namedtuple')
expl('''#### Tupel mit Namen

Bei einem Tupel `(3, 4)` muss man sich merken, was an welcher Stelle steht. Ein **namedtuple** gibt den Stellen Namen.

`Punkt = namedtuple('Punkt', ['x', 'y'])` erzeugt einen neuen Datentyp `Punkt`. Danach erstellt man Punkte mit `Punkt(3, 4)`
oder `Punkt(x=3, y=4)`. Auf die Werte greift man mit `p.x` oder wie bei Tupeln mit `p[0]` zu.
Die Namen kann man auch als eine Zeichenkette angeben: `namedtuple('Punkt', 'x y')`.''',
     """from collections import namedtuple

Punkt = namedtuple('Punkt', ['x', 'y'])
p = Punkt(3, 4)
q = Punkt(x=-1, y=2)
print(p)
print(p.x, p.y)
print(q[0], q[1])""")
expl('''#### Ein namedtuple ist ein Tupel

- Man kann es **entpacken**, mit `len()` messen, mit `in` durchsuchen, mit `for` durchlaufen und mit `==` vergleichen.
- Es ist **unveränderlich**: `p.x = 5` gibt einen `AttributeError`.
- `p._replace(x=5)` gibt einen **neuen** Punkt zurück, bei dem `x` geändert ist.''',
     """from collections import namedtuple

Punkt = namedtuple('Punkt', 'x y')
p = Punkt(3, 4)
x, y = p
print(x + y)
print(len(p), 4 in p)
print(p == (3, 4))
p2 = p._replace(x=5)
print(p, p2)""")
expl('''#### `_asdict()`, `_fields` und `_make()`

- `p._asdict()` gibt ein Dictionary mit den Namen als Schlüsseln zurück.
- `Punkt._fields` ist ein Tupel mit den Namen.
- `Punkt._make(liste)` erstellt ein namedtuple aus einer Liste (oder einem anderen Tupel).''',
     """from collections import namedtuple

Buch = namedtuple('Buch', 'titel autor jahr')
b = Buch('Momo', 'Michael Ende', 1973)
print(b._asdict())
print(Buch._fields)
print(Buch._make(['Emil und die Detektive', 'Erich Kästner', 1929]))""")
expl('''#### Listen von namedtuples sortieren

`sorted(liste, key=funktion)` sortiert nach dem Ergebnis der Funktion, genau wie `liste.sort(key=funktion)`,
gibt aber eine **neue** Liste zurück. Auch `max()` und `min()` haben den Parameter `key=`.
Bei namedtuples gibt man den Namen des Feldes mit einer `lambda`-Funktion an.''',
     """from collections import namedtuple

Schueler = namedtuple('Schueler', 'name alter')
klasse = [Schueler('Bea', 16), Schueler('Ali', 15), Schueler('Cem', 17)]
for s in sorted(klasse, key=lambda s: s.alter):
    print(s.name, s.alter)
print(max(klasse, key=lambda s: s.alter).name)""")

t('Erstelle einen namedtuple-Typ `Buch` mit den Feldern `titel`, `autor` und `jahr`. Erstelle damit das Buch „Krabat“ von Otfried Preußler aus dem Jahr 1971 und gib es aus.',
  "from collections import namedtuple",
  """Buch = namedtuple('Buch', ['titel', 'autor', 'jahr'])
b = Buch('Krabat', 'Otfried Preußler', 1971)
print(b)""")
t('Gib das Buch `b` in der Form `Krabat (1971) von Otfried Preußler` aus. Greife über die Namen der Felder zu.',
  "from collections import namedtuple\nBuch = namedtuple('Buch', 'titel autor jahr')\nb = Buch('Krabat', 'Otfried Preußler', 1971)",
  "print(f'{b.titel} ({b.jahr}) von {b.autor}')")
t('Erstelle mit dem Typ `Farbe` die Farbe Orange mit `rot=255`, `gruen=165` und `blau=0` (mit Namen beim Erstellen). Gib danach den Grünanteil einmal über den Namen und einmal über den Index aus.',
  "from collections import namedtuple\nFarbe = namedtuple('Farbe', 'rot gruen blau')",
  """orange = Farbe(rot=255, gruen=165, blau=0)
print(orange.gruen)
print(orange[1])""")
t('Berechne den Abstand der Punkte `p` und `q` mit der Formel $\\sqrt{(x_1-x_2)^2 + (y_1-y_2)^2}$ (Wurzel mit `** 0.5`) und gib ihn aus.',
  "from collections import namedtuple\nPunkt = namedtuple('Punkt', 'x y')\np = Punkt(1, 2)\nq = Punkt(7, 10)",
  """abstand = ((p.x - q.x) ** 2 + (p.y - q.y) ** 2) ** 0.5
print(abstand)""")
t('Entpacke den Termin `termin` in die Variablen `tag`, `zeit` und `fach` und gib sie in der Form `Mo, 8:00 Uhr: Mathe` aus.',
  "from collections import namedtuple\nTermin = namedtuple('Termin', 'tag zeit fach')\ntermin = Termin('Mo', '8:00', 'Mathe')",
  """tag, zeit, fach = termin
print(f'{tag}, {zeit} Uhr: {fach}')""")
t('Das Buch `b` hat das falsche Jahr. Erstelle mit `_replace()` ein korrigiertes Buch mit dem Jahr 1979 und gib es aus.',
  "from collections import namedtuple\nBuch = namedtuple('Buch', 'titel autor jahr')\nb = Buch('Die unendliche Geschichte', 'Michael Ende', 1997)",
  """b = b._replace(jahr=1979)
print(b)""")
t('Gib den Spieler `s` mit `_asdict()` als Dictionary aus.',
  "from collections import namedtuple\nSpieler = namedtuple('Spieler', 'name punkte level')\ns = Spieler('Luna', 4200, 7)",
  "print(s._asdict())")
t('Gib alle Felder des Spielers `s` mit ihrem Wert untereinander aus, in der Form `name = Luna`. Verwende `Spieler._fields` und `zip()`.',
  "from collections import namedtuple\nSpieler = namedtuple('Spieler', 'name punkte level')\ns = Spieler('Luna', 4200, 7)",
  """for feld, wert in zip(Spieler._fields, s):
    print(f'{feld} = {wert}')""")
t('''Die Zeile `zeile` stammt aus einer CSV-Datei. Zerlege sie mit `split(',')` und erstelle daraus mit `_make()` ein namedtuple
vom Typ `Stadt`. Gib die Stadt aus und danach die Einwohnerzahl als Zahl (`int()`) plus 1.''',
  "from collections import namedtuple\nStadt = namedtuple('Stadt', 'name land einwohner')\nzeile = 'Tübingen,Baden-Württemberg,91877'",
  """s = Stadt._make(zeile.split(','))
print(s)
print(int(s.einwohner) + 1)""")
t('Gib die Namen der Schülerinnen und Schüler nach ihrer Note sortiert aus (beste Note zuerst), in der Form `Bea 1.3`.',
  "from collections import namedtuple\nSchueler = namedtuple('Schueler', 'name note')\nklasse = [Schueler('Ali', 2.7), Schueler('Bea', 1.3), Schueler('Cem', 3.0), Schueler('Dana', 1.7)]",
  """for s in sorted(klasse, key=lambda s: s.note):
    print(s.name, s.note)""")
t('Gib den Titel des **ältesten** Buches in `buecher` aus. Verwende `min()` mit `key=`.',
  "from collections import namedtuple\nBuch = namedtuple('Buch', 'titel jahr')\nbuecher = [Buch('Momo', 1973), Buch('Krabat', 1971), Buch('Tschick', 2010), Buch('Das kleine Gespenst', 1966)]",
  "print(min(buecher, key=lambda b: b.jahr).titel)")
t('Gib die Titel aller Bücher aus `buecher` aus, die **nach 1970** erschienen sind.',
  "from collections import namedtuple\nBuch = namedtuple('Buch', 'titel jahr')\nbuecher = [Buch('Momo', 1973), Buch('Krabat', 1971), Buch('Tschick', 2010), Buch('Das kleine Gespenst', 1966)]",
  """for b in buecher:
    if b.jahr > 1970:
        print(b.titel)""")
t('Schreibe eine Funktion `mitte(p, q)`, die den Mittelpunkt der Strecke von `p` nach `q` als `Punkt` zurückgibt. Gib `mitte(Punkt(2, 4), Punkt(6, 10))` aus.',
  "from collections import namedtuple\nPunkt = namedtuple('Punkt', 'x y')",
  """def mitte(p, q):
    return Punkt((p.x + q.x) / 2, (p.y + q.y) / 2)

print(mitte(Punkt(2, 4), Punkt(6, 10)))""")
t('Schreibe eine Funktion `verschiebe(p, dx, dy)`, die mit `_replace()` einen um `dx` und `dy` verschobenen Punkt zurückgibt. Verschiebe `p` dreimal hintereinander um `(1, -2)` und gib jedes Mal den Punkt aus.',
  "from collections import namedtuple\nPunkt = namedtuple('Punkt', 'x y')\np = Punkt(0, 0)",
  """def verschiebe(p, dx, dy):
    return p._replace(x=p.x + dx, y=p.y + dy)

for i in range(3):
    p = verschiebe(p, 1, -2)
    print(p)""")
t('''Erstelle mit `product()` aus `itertools` ein Kartenspiel: eine Liste mit einer `Karte` für jede Kombination aus
`farben` und `werte` (erst alle Karten von Kreuz, dann Pik, ...). Gib die Anzahl der Karten und die ersten drei Karten aus.''',
  "from collections import namedtuple\nfrom itertools import product\nKarte = namedtuple('Karte', 'farbe wert')\n"
  "farben = ['Kreuz', 'Pik', 'Herz', 'Karo']\nwerte = ['7', '8', '9', '10', 'Bube', 'Dame', 'König', 'Ass']",
  """deck = []
for f, w in product(farben, werte):
    deck.append(Karte(f, w))
print(len(deck))
print(deck[:3])""")
t('Gib die Gesamtpunktzahl aller Spieler in `spieler` aus und danach den Namen des Spielers mit den meisten Punkten.',
  "from collections import namedtuple\nSpieler = namedtuple('Spieler', 'name punkte')\nspieler = [Spieler('Luna', 4200), Spieler('Max', 5100), Spieler('Ida', 3900)]",
  """summe = 0
for s in spieler:
    summe += s.punkte
print(summe)
print(max(spieler, key=lambda s: s.punkte).name)""")
predict("""from collections import namedtuple
Punkt = namedtuple('Punkt', 'x y')
p = Punkt(2, 5)
print(p[1], p.x)
x, y = p
print(x * y)
print(p == Punkt(5, 2))""")
predict("""from collections import namedtuple
Punkt = namedtuple('Punkt', 'x y')
p = Punkt(2, 5)
p.x = 3""", error=AttributeError)
predict("""from collections import namedtuple
Punkt = namedtuple('Punkt', 'x y')
p = Punkt(2, 5)
q = p._replace(y=0)
print(p)
print(q)
print(q._asdict())""")

# ---------------------------------------------------------------- 6
sec('deque')
expl('''#### Eine Liste mit zwei Enden

Eine `deque` (gesprochen „Deck“, von *double-ended queue*) ist wie eine Liste, an der man **an beiden Enden** schnell
anfügen und entfernen kann:

| hinten (rechts) | vorne (links) |
|---|---|
| `d.append(x)` | `d.appendleft(x)` |
| `d.pop()` | `d.popleft()` |
| `d.extend(liste)` | `d.extendleft(liste)` |

`pop()` und `popleft()` geben das entfernte Element zurück. Bei einer Liste ist `liste.pop(0)` langsam, wenn die Liste lang ist,
bei einer `deque` ist `popleft()` immer schnell. Indizes wie `d[0]` und `d[-1]`, `len(d)`, `in` und `for` gehen wie bei Listen.''',
     """from collections import deque

d = deque([2, 3])
d.append(4)
d.appendleft(1)
print(d)
print(d.popleft(), d.pop())
print(d, d[0], len(d))""")
expl('''#### Warteschlange und Stapel

- **Warteschlange** (wer zuerst kommt, ist zuerst dran): hinten mit `append()` anstellen, vorne mit `popleft()` drankommen.
- **Stapel** (das Letzte kommt zuerst wieder heraus): mit `append()` drauflegen, mit `pop()` wegnehmen.

`while d:` läuft, solange die deque nicht leer ist. `pop()` oder `popleft()` bei einer leeren deque geben einen `IndexError`.''',
     """from collections import deque

schlange = deque(['Ali', 'Bea'])
schlange.append('Cem')
while schlange:
    print(schlange.popleft(), 'ist dran')

stapel = deque()
for teller in ['rot', 'grün', 'blau']:
    stapel.append(teller)
print(stapel.pop())""")
expl('''#### Drehen mit `rotate()`

`d.rotate(n)` dreht die deque um `n` Schritte nach **rechts**: Die letzten `n` Elemente wandern nach vorne.
`d.rotate(-n)` dreht nach **links**: Die ersten `n` Elemente wandern nach hinten.

`extendleft(liste)` fügt die Elemente einzeln vorne an, sie stehen danach also in **umgekehrter** Reihenfolge vorne.''',
     """from collections import deque

d = deque([1, 2, 3, 4, 5])
d.rotate(2)
print(d)
d.rotate(-3)
print(d)
d.extendleft([7, 8])
print(d)""")
expl('''#### Begrenzte Länge mit `maxlen`

`deque(maxlen=3)` kann höchstens 3 Elemente enthalten. Ist sie voll, fällt beim `append()` vorne eines heraus
(und beim `appendleft()` hinten). So behält man zum Beispiel immer nur die **letzten** Werte.''',
     """from collections import deque

letzte = deque(maxlen=3)
for z in [1, 2, 3, 4, 5]:
    letzte.append(z)
    print(list(letzte))
print(letzte)""")

t('Erstelle eine deque mit den Zahlen 2, 3, 4. Füge hinten 5 und vorne 1 an und gib die deque aus.',
  "from collections import deque",
  """d = deque([2, 3, 4])
d.append(5)
d.appendleft(1)
print(d)""")
t('Entferne aus `d` das erste und das letzte Element und gib beide aus. Gib danach die deque aus.',
  "from collections import deque\nd = deque(['a', 'b', 'c', 'd'])",
  """print(d.popleft())
print(d.pop())
print(d)""")
t('An der Kasse stehen die Personen in `schlange`. Dann stellen sich noch `Dana` und `Emil` hinten an. Bediene alle der Reihe nach, in der Form `Ali wird bedient`.',
  "from collections import deque\nschlange = deque(['Ali', 'Bea', 'Cem'])",
  """schlange.append('Dana')
schlange.append('Emil')
while schlange:
    print(schlange.popleft(), 'wird bedient')""")
t('Lege die Bücher aus `buecher` der Reihe nach auf einen Stapel (`append()`). Nimm sie dann alle wieder herunter (`pop()`) und gib sie dabei aus.',
  "from collections import deque\nbuecher = ['Mathe', 'Deutsch', 'Englisch', 'Physik']",
  """stapel = deque()
for b in buecher:
    stapel.append(b)
while stapel:
    print(stapel.pop())""")
t('Füge die Zahlen `[10, 20, 30]` mit `extend()` hinten und die Zahlen `[-1, -2]` mit `extendleft()` vorne an. Gib die deque aus.',
  "from collections import deque\nd = deque([0])",
  """d.extend([10, 20, 30])
d.extendleft([-1, -2])
print(d)""")
t('Drehe `d` um 2 Schritte nach rechts und gib `d` aus. Drehe dann um 3 Schritte nach links und gib `d` wieder aus.',
  "from collections import deque\nd = deque(['Mo', 'Di', 'Mi', 'Do', 'Fr'])",
  """d.rotate(2)
print(d)
d.rotate(-3)
print(d)""")
t("""Gib alle Drehungen des Wortes `wort` aus: In jedem Schritt wird der erste Buchstabe ans Ende gesetzt (`rotate(-1)`).
Gib die Buchstaben jeweils mit `''.join()` als Wort aus, insgesamt so viele Zeilen, wie das Wort Buchstaben hat.""",
  "from collections import deque\nwort = 'Python'",
  """d = deque(wort)
for i in range(len(wort)):
    print(''.join(d))
    d.rotate(-1)""")
t('Die Spieler in `spieler` sind reihum dran. Gib für 7 Züge aus, wer dran ist, in der Form `Zug 1: Ali`. Verwende `d[0]` und `rotate(-1)`.',
  "from collections import deque\nspieler = deque(['Ali', 'Bea', 'Cem'])",
  """for zug in range(1, 8):
    print(f'Zug {zug}: {spieler[0]}')
    spieler.rotate(-1)""")
t('''Abzählreim: Die Kinder stehen im Kreis. Es wird reihum gezählt, und jedes **dritte** Kind scheidet aus; dann wird beim
nächsten Kind weitergezählt. Drehe dafür die deque mit `rotate(-2)` und entferne dann das vorderste Kind mit `popleft()`.
Gib die Kinder in der Reihenfolge aus, in der sie ausscheiden.''',
  "from collections import deque\nkinder = deque(['Ali', 'Bea', 'Cem', 'Dana', 'Emil', 'Fiona', 'Gus'])",
  """while kinder:
    kinder.rotate(-2)
    print(kinder.popleft())""")
t('Gehe die Messwerte durch und speichere sie in einer `deque(maxlen=3)`. Gib am Ende die letzten drei Messwerte als Liste aus.',
  "from collections import deque\nmesswerte = [21, 23, 22, 25, 27, 26, 24]",
  """letzte = deque(maxlen=3)
for m in messwerte:
    letzte.append(m)
print(list(letzte))""")
t('''Berechne den **gleitenden Durchschnitt** der letzten drei Messwerte: Füge jeden Wert in eine `deque(maxlen=3)` ein.
Sobald drei Werte darin sind, gib ihren Durchschnitt mit einer Nachkommastelle aus.''',
  "from collections import deque\nmesswerte = [21, 23, 22, 25, 27, 26, 24]",
  """letzte = deque(maxlen=3)
for m in messwerte:
    letzte.append(m)
    if len(letzte) == 3:
        print(f'{sum(letzte) / 3:.1f}')""")
t('''Der Browser merkt sich nur die letzten 4 besuchten Seiten. Speichere die Seiten in einer `deque(maxlen=4)`, die neueste
jeweils **vorne** (`appendleft()`). Gib am Ende den Verlauf als Liste aus.''',
  "from collections import deque\nbesucht = ['start', 'news', 'sport', 'wetter', 'kino', 'news', 'spiele']",
  """verlauf = deque(maxlen=4)
for seite in besucht:
    verlauf.appendleft(seite)
print(list(verlauf))""")
t('''Prüfe mit einer deque, ob ein Wort ein **Palindrom** ist (vorwärts und rückwärts gleich): Solange mehr als ein Buchstabe
übrig ist, vergleiche `popleft()` mit `pop()`. Gib für jedes Wort in `woerter` aus, ob es ein Palindrom ist.''',
  "from collections import deque\nwoerter = ['rentner', 'anna', 'otto', 'hallo', 'reliefpfeiler', 'kajak', 'paddel']",
  """for wort in woerter:
    d = deque(wort)
    palindrom = True
    while len(d) > 1:
        if d.popleft() != d.pop():
            palindrom = False
    print(wort, palindrom)""")
t('''Ein Zauberer hat die Karten 1 bis 6. Er legt immer die oberste Karte auf den Tisch und die nächste dann unter den Stapel.
Das wiederholt er, bis keine Karte mehr übrig ist. Die oberste Karte ist `d[0]`. Gib die Karten in der Reihenfolge aus,
in der sie auf den Tisch kommen.''',
  "from collections import deque\nd = deque([1, 2, 3, 4, 5, 6])",
  """while d:
    print(d.popleft())
    if d:
        d.rotate(-1)""")
t('''Ein Drucker arbeitet die Aufträge in `auftraege` der Reihe nach ab: Jede Minute druckt er höchstens 3 Seiten des vordersten
Auftrags. Ist ein Auftrag dann noch nicht fertig, kommt der Rest wieder hinten in die Warteschlange.
Gib für jede Minute aus, an welchem Auftrag er druckt, wie viele Seiten er druckt und wie viele noch übrig sind,
in der Form `Minute 1: Ali druckt 3, Rest 2`.''',
  "from collections import deque\nauftraege = deque([('Ali', 5), ('Bea', 2), ('Cem', 7)])",
  """minute = 0
while auftraege:
    minute += 1
    name, seiten = auftraege.popleft()
    gedruckt = min(seiten, 3)
    rest = seiten - gedruckt
    print(f'Minute {minute}: {name} druckt {gedruckt}, Rest {rest}')
    if rest > 0:
        auftraege.append((name, rest))""")
predict("""from collections import deque
d = deque([1, 2, 3])
d.extendleft([4, 5])
print(d)
print(d[1], d[-1])""")
predict("""from collections import deque
d = deque([1, 2, 3, 4], maxlen=4)
d.append(5)
d.appendleft(0)
print(list(d))""")
predict("""from collections import deque
d = deque(['x'])
d.pop()
d.pop()""", error=IndexError)

# ---------------------------------------------------------------- 7
sec('OrderedDict und ChainMap')
expl('''#### `OrderedDict`

Gewöhnliche Dictionaries behalten die Reihenfolge, in der die Schlüssel eingefügt wurden. Ein `OrderedDict` kann zusätzlich
die **Reihenfolge ändern**:

- `od.move_to_end(schluessel)` schiebt einen Eintrag ans Ende, `od.move_to_end(schluessel, last=False)` an den Anfang.
- `od.popitem()` entfernt den **letzten** Eintrag und gibt ihn als Tupel zurück, `od.popitem(last=False)` den **ersten**.
- Zwei OrderedDicts sind nur dann `==`, wenn auch die Reihenfolge gleich ist. Bei gewöhnlichen Dictionaries zählt die Reihenfolge nicht.''',
     """from collections import OrderedDict

od = OrderedDict([('a', 1), ('b', 2), ('c', 3)])
od.move_to_end('a')
print(list(od))
od.move_to_end('c', last=False)
print(list(od))
print(od.popitem(last=False))
print(od)
print({'x': 1, 'y': 2} == {'y': 2, 'x': 1})
print(OrderedDict(x=1, y=2) == OrderedDict(y=2, x=1))""")
expl('''#### `ChainMap`: mehrere Dictionaries hintereinander

`ChainMap(d1, d2)` verbindet mehrere Dictionaries zu einem, **ohne** sie zu kopieren. Beim Nachschlagen wird zuerst in `d1`
gesucht, dann in `d2`. So kann man zum Beispiel eigene Einstellungen vor die Standardeinstellungen stellen.

- Schreiben (`cm[s] = wert`) und Löschen ändern immer nur das **erste** Dictionary.
- `dict(cm)` erzeugt ein gewöhnliches Dictionary mit allen Schlüsseln (bei doppelten gilt der Wert aus dem ersten).''',
     """from collections import ChainMap

standard = {'farbe': 'weiß', 'sprache': 'de', 'schrift': 12}
eigene = {'farbe': 'dunkel'}
cm = ChainMap(eigene, standard)
print(cm['farbe'], cm['sprache'])
cm['schrift'] = 16
print(eigene)
print(standard)
print(dict(cm))""")

t('Die Aufgabe `Vokabeln` ist erledigt und soll ans Ende der Liste. Verschiebe sie mit `move_to_end()` und gib die Schlüssel als Liste aus.',
  "from collections import OrderedDict\naufgaben = OrderedDict([('Mathe', 'S. 12'), ('Vokabeln', 'Unit 3'), ('Physik', 'Blatt 2')])",
  """aufgaben.move_to_end('Vokabeln')
print(list(aufgaben))""")
t('`Cem` hat einen VIP-Pass und kommt an den Anfang der Gästeliste. Verschiebe ihn und gib die Gästeliste aus.',
  "from collections import OrderedDict\ngaeste = OrderedDict([('Ali', 2), ('Bea', 1), ('Cem', 3)])",
  """gaeste.move_to_end('Cem', last=False)
print(gaeste)""")
t('Entferne mit `popitem()` nacheinander den ersten und den letzten Eintrag von `od` und gib beide aus. Gib danach `od` aus.',
  "from collections import OrderedDict\nod = OrderedDict([('rot', 1), ('gelb', 2), ('grün', 3), ('blau', 4)])",
  """print(od.popitem(last=False))
print(od.popitem())
print(od)""")
t('''Ein Speicher behält höchstens 3 Wörter mit ihrer Länge. Füge die Wörter aus `woerter` der Reihe nach ein. Hat der Speicher
danach mehr als 3 Einträge, entferne den **ältesten** mit `popitem(last=False)` und gib ihn aus. Gib am Ende den Speicher aus.''',
  "from collections import OrderedDict\nwoerter = ['Hund', 'Katze', 'Maus', 'Pferd', 'Esel']",
  """speicher = OrderedDict()
for w in woerter:
    speicher[w] = len(w)
    if len(speicher) > 3:
        print(speicher.popitem(last=False))
print(speicher)""")
t('''Ein **LRU-Speicher** (*least recently used*) hat Platz für 3 Seiten. Wird eine Seite aufgerufen, die schon im Speicher ist,
kommt sie mit `move_to_end()` ans Ende. Sonst wird sie hinten eingefügt (Wert: `True`), und wenn dann mehr als 3 Seiten im
Speicher sind, fliegt die vorderste (am längsten nicht benutzte) heraus. Gib nach jedem Aufruf die Seiten als Liste aus.''',
  "from collections import OrderedDict\naufrufe = ['A', 'B', 'C', 'A', 'D', 'B', 'E']",
  """speicher = OrderedDict()
for seite in aufrufe:
    if seite in speicher:
        speicher.move_to_end(seite)
    else:
        speicher[seite] = True
        if len(speicher) > 3:
            speicher.popitem(last=False)
    print(list(speicher))""")
t('Schlage in der ChainMap aus `schule` und `standard` die Werte für `pause`, `beginn` und `ende` nach und gib sie aus.',
  "from collections import ChainMap\nstandard = {'beginn': '8:00', 'pause': 15, 'ende': '13:00'}\nschule = {'beginn': '7:45', 'pause': 20}",
  """zeiten = ChainMap(schule, standard)
print(zeiten['pause'])
print(zeiten['beginn'])
print(zeiten['ende'])""")
t('''Setze in der ChainMap `cm` die `lautstaerke` auf 3 und gib danach `spieler` und `standard` aus. Nur eines der beiden
Dictionaries ändert sich.''',
  "from collections import ChainMap\nstandard = {'lautstaerke': 7, 'musik': True}\nspieler = {'musik': False}\ncm = ChainMap(spieler, standard)",
  """cm['lautstaerke'] = 3
print(spieler)
print(standard)""")
t('''Python sucht einen Namen zuerst bei den lokalen Variablen, dann bei den globalen, dann bei den eingebauten.
Stelle das mit einer ChainMap aus `lokal`, `global_` und `eingebaut` nach. Gib für jeden Namen in `namen` seinen Wert aus,
in der Form `x = 1`.''',
  "from collections import ChainMap\nlokal = {'x': 1}\nglobal_ = {'x': 10, 'y': 20}\neingebaut = {'x': 100, 'y': 200, 'z': 300}\nnamen = ['x', 'y', 'z']",
  """cm = ChainMap(lokal, global_, eingebaut)
for n in namen:
    print(f'{n} = {cm[n]}')""")
t('Verbinde die Dictionaries `a`, `b` und `c` mit einer ChainMap und gib mit `dict()` das zusammengefasste Dictionary aus, dazu die Anzahl der Schlüssel.',
  "from collections import ChainMap\na = {'Mo': 'Sport'}\nb = {'Mo': 'Kunst', 'Di': 'Chor'}\nc = {'Di': 'Theater', 'Mi': 'Robotik'}",
  """cm = ChainMap(a, b, c)
print(dict(cm))
print(len(cm))""")
predict("""from collections import OrderedDict
od = OrderedDict(a=1, b=2, c=3)
od.move_to_end('b')
od.move_to_end('c', last=False)
print(list(od))
print(od.popitem())""")
predict("""from collections import ChainMap
a = {'x': 1}
b = {'x': 2, 'y': 3}
cm = ChainMap(a, b)
print(cm['x'], cm['y'])
cm['y'] = 4
print(a, b)""")

# ---------------------------------------------------------------- 8
sec('Gemischte Übungen')
t('Gib aus, welche Wortlänge in `text` am häufigsten vorkommt und wie oft, in der Form `Länge 3: 5-mal`.',
  "from collections import Counter\ntext = 'der alte Mann und das Meer ist ein Buch von Ernest Hemingway aus dem Jahr 1952'",
  """c = Counter()
for w in text.split():
    c[len(w)] += 1
laenge, anzahl = c.most_common(1)[0]
print(f'Länge {laenge}: {anzahl}-mal')""")
t('Gib den **ersten** Buchstaben von `wort` aus, der nur ein einziges Mal vorkommt.',
  "from collections import Counter\nwort = 'abrakadabrasimsala'",
  """c = Counter(wort)
for b in wort:
    if c[b] == 1:
        print(b)
        break""")
t('Gib alle Elemente von `zahlen` aus, die mehr als einmal vorkommen, in der Reihenfolge, in der sie zuerst vorkommen (jedes nur einmal).',
  "from collections import Counter\nzahlen = [4, 8, 15, 16, 23, 42, 8, 4, 4, 23]",
  """c = Counter(zahlen)
doppelt = []
for z in c:
    if c[z] > 1:
        doppelt.append(z)
print(doppelt)""")
t('''Erstelle einen **Index**: Für jedes Wort im Gedicht sollen die Nummern der Zeilen (ab 1) gespeichert werden, in denen es
vorkommt, jede Nummer nur einmal. Verwende `defaultdict(list)`, `enumerate()` und `splitlines()`. Gib die Zeilen für
`ich`, `du` und `wir` aus.''',
  "from collections import defaultdict\ngedicht = '''ich bin du bist\nwir sind ich und du\nwir lachen\ndu und du'''",
  """index = defaultdict(list)
for nr, zeile in enumerate(gedicht.splitlines(), 1):
    for w in zeile.split():
        if nr not in index[w]:
            index[w].append(nr)
print(index['ich'])
print(index['du'])
print(index['wir'])""")
t('''Zähle mit `product()` und einem `Counter`, wie oft jede Augensumme beim Werfen von zwei Würfeln vorkommen kann
(alle 36 Kombinationen). Gib die Summen von 2 bis 12 mit ihrer Anzahl aus, in der Form `7: 6`.''',
  "from collections import Counter\nfrom itertools import product",
  """c = Counter()
for a, b in product(range(1, 7), repeat=2):
    c[a + b] += 1
for s in range(2, 13):
    print(f'{s}: {c[s]}')""")
t('''Die Ergebnisse der Klassenarbeit stehen als namedtuples in `ergebnisse`. Gib für jede Klasse (alphabetisch sortiert)
den Notendurchschnitt mit zwei Nachkommastellen aus. Sammle die Noten in einem `defaultdict(list)`.''',
  "from collections import namedtuple, defaultdict\nErgebnis = namedtuple('Ergebnis', 'name klasse note')\n"
  "ergebnisse = [Ergebnis('Ali', '9b', 2), Ergebnis('Bea', '9a', 1), Ergebnis('Cem', '9b', 4), Ergebnis('Dana', '9a', 3),\n"
  "              Ergebnis('Emil', '9b', 3), Ergebnis('Fiona', '9a', 2), Ergebnis('Gus', '9c', 5)]",
  """d = defaultdict(list)
for e in ergebnisse:
    d[e.klasse].append(e.note)
for klasse in sorted(d):
    print(f'{klasse}: {sum(d[klasse]) / len(d[klasse]):.2f}')""")
t('''Gib die zwei Artikel aus, die in allen Bestellungen zusammen am häufigsten bestellt wurden, mit der Gesamtmenge.
Jede Bestellung ist ein Dictionary; addiere sie mit `update()` in einem Counter.''',
  "from collections import Counter\nbestellungen = [{'Brezel': 2, 'Brötchen': 6}, {'Croissant': 3, 'Brezel': 1}, {'Brötchen': 4, 'Croissant': 1, 'Brezel': 5}]",
  """gesamt = Counter()
for b in bestellungen:
    gesamt.update(b)
print(gesamt.most_common(2))""")
t('''In einem Spiel braucht man für einen **Trank** die Zutaten `rezept`. Prüfe, ob das Inventar reicht. Wenn ja, ziehe die
Zutaten mit `subtract()` ab und gib `Trank gebraut` und das Inventar aus. Wenn nein, gib aus, was fehlt (mit `-`).
Teste mit beiden Inventaren aus `inventare`.''',
  "from collections import Counter\nrezept = Counter({'Kraut': 2, 'Pilz': 1, 'Wasser': 1})\n"
  "inventare = [Counter({'Kraut': 3, 'Pilz': 2, 'Wasser': 1, 'Stein': 4}), Counter({'Kraut': 1, 'Wasser': 2})]",
  """for inventar in inventare:
    fehlt = rezept - inventar
    if len(fehlt) == 0:
        inventar.subtract(rezept)
        print('Trank gebraut', inventar)
    else:
        print('Es fehlt:', fehlt)""")
t('''Ein Texteditor speichert die letzten 3 Zustände für **Rückgängig**. Gehe `aktionen` durch: Ein Wort wird an `text`
angehängt (vorher kommt der alte Text in eine `deque(maxlen=3)`), bei `'undo'` wird der letzte gespeicherte Text
wiederhergestellt, wenn es einen gibt. Gib nach jeder Aktion den Text in der Form `|...|` aus.''',
  "from collections import deque\naktionen = ['Hallo', ' Welt', '!', 'undo', 'undo', 'undo', 'undo', '?']\ntext = ''",
  """verlauf = deque(maxlen=3)
for a in aktionen:
    if a == 'undo':
        if verlauf:
            text = verlauf.pop()
    else:
        verlauf.append(text)
        text += a
    print(f'|{text}|')""")
t('''**Breitensuche:** Wie viele Schritte braucht man von `A` zu jedem anderen Ort? Die Nachbarn stehen in `nachbarn`.
Starte mit `abstand = {'A': 0}` und einer Warteschlange `deque(['A'])`. Nimm immer den vordersten Ort heraus; jeder Nachbar,
der noch keinen Abstand hat, bekommt den Abstand des Ortes plus 1 und wird hinten angestellt.
Gib am Ende die Orte alphabetisch mit ihrem Abstand aus, in der Form `A: 0`.''',
  "from collections import deque\nnachbarn = {'A': ['B', 'C'], 'B': ['A', 'D'], 'C': ['A', 'D', 'E'], 'D': ['B', 'C', 'F'], 'E': ['C', 'F'], 'F': ['D', 'E', 'G'], 'G': ['F']}",
  """abstand = {'A': 0}
schlange = deque(['A'])
while schlange:
    ort = schlange.popleft()
    for n in nachbarn[ort]:
        if n not in abstand:
            abstand[n] = abstand[ort] + 1
            schlange.append(n)
for ort in sorted(abstand):
    print(f'{ort}: {abstand[ort]}')""")
t('''Erstelle für jede Zeile in `zeilen` ein namedtuple `Wetter` mit den Feldern `tag`, `stadt` und `grad` (`grad` als `int`).
Gib danach für jede Stadt (alphabetisch) die höchste Temperatur aus. Verwende ein `defaultdict(list)`.''',
  "from collections import namedtuple, defaultdict\nWetter = namedtuple('Wetter', 'tag stadt grad')\n"
  "zeilen = ['Mo,Stuttgart,18', 'Mo,Freiburg,21', 'Di,Stuttgart,22', 'Di,Freiburg,19', 'Mi,Stuttgart,17', 'Mi,Freiburg,23']",
  """daten = []
for z in zeilen:
    tag, stadt, grad = z.split(',')
    daten.append(Wetter(tag, stadt, int(grad)))
temperaturen = defaultdict(list)
for w in daten:
    temperaturen[w.stadt].append(w.grad)
for stadt in sorted(temperaturen):
    print(stadt, max(temperaturen[stadt]))""")
t('''Gib für die Wörter in `woerter` aus, welcher Buchstabe in **allen** Wörtern zusammen am häufigsten vorkommt.
Addiere dazu die Counter der einzelnen Wörter mit `+`.''',
  "from collections import Counter\nwoerter = ['Mathematik', 'Informatik', 'Physik', 'Chemie', 'Biologie']",
  """gesamt = Counter()
for w in woerter:
    gesamt = gesamt + Counter(w.lower())
print(gesamt.most_common(1))""")
t('''Simuliere 1000 Münzwürfe mit `random.seed(7)` und `random.choice(['K', 'Z'])`. Speichere immer die letzten
drei Würfe in einer `deque(maxlen=3)` und zähle mit einem `Counter`, wie oft die letzten drei Würfe zusammen
(mit `''.join()`) welches Muster ergeben, sobald drei Würfe darin sind. Gib die Muster alphabetisch mit ihrer Anzahl aus.''',
  "import random\nfrom collections import deque, Counter\nrandom.seed(7)",
  """letzte = deque(maxlen=3)
muster = Counter()
for i in range(1000):
    letzte.append(random.choice(['K', 'Z']))
    if len(letzte) == 3:
        muster[''.join(letzte)] += 1
for m in sorted(muster):
    print(m, muster[m])""")
predict("""from collections import Counter, deque
d = deque('abc')
d.rotate(1)
c = Counter(d)
c.update(['c', 'a'])
print(''.join(d))
print(c.most_common(1))""")
predict("""from collections import defaultdict, namedtuple
P = namedtuple('P', 'name gruppe')
leute = [P('Ali', 1), P('Bea', 2), P('Cem', 1)]
d = defaultdict(list)
for p in leute:
    d[p.gruppe].append(p.name)
print(d[1], d[3])
print(len(d))""")

generate('collections', 'Das Modul collections', INTRO)
