# Erzeugt ../content/dictionaries.ipynb (siehe nbgen.py).
from nbgen import sec, expl, task, predict, generate

# ---------------------------------------------------------------- 1
sec('Dictionaries erstellen')
expl('''#### Was ist ein Dictionary?

Ein **Dictionary** (deutsch: Wörterbuch, Datentyp `dict`) speichert **Schlüssel-Wert-Paare**.
Es steht in geschweiften Klammern: `{schluessel: wert, ...}`. Über den Schlüssel findet man den Wert,
so wie man in einem Wörterbuch über ein Wort die Übersetzung findet.

- Jeder **Schlüssel** kommt nur **einmal** vor. Schreibt man ihn doppelt, gilt der letzte Wert.
- Schlüssel sind meist Zeichenketten oder Zahlen. Listen dürfen keine Schlüssel sein.
- **Werte** können beliebige Datentypen haben, auch Listen oder andere Dictionaries.
- Dictionaries sind **veränderbar** und behalten die **Reihenfolge**, in der die Paare eingefügt wurden.''',
     """auto = {'marke': 'VW', 'modell': 'Golf', 'baujahr': 2019}
print(auto)
print(len(auto))
print(type(auto))""")
expl('''#### `dict()` und das leere Dictionary

- `{}` oder `dict()` erzeugt ein **leeres** Dictionary.
- Mit `dict(name='Ali', alter=16)` kann man ein Dictionary auch mit Schlüsselwort-Argumenten erzeugen.
  Die Schlüssel sind dann Zeichenketten.''',
     """leer = {}
print(leer, len(leer))
person = dict(name='Ali', alter=16)
print(person)""")

task("Erstelle ein Dictionary `auto` mit den Schlüsseln `marke`, `modell` und `baujahr` und den Werten `'VW'`, `'Golf'` und `2019`. Gib es aus.",
     solution="""auto = {'marke': 'VW', 'modell': 'Golf', 'baujahr': 2019}
print(auto)""")
task('Gib mit `len()` aus, wie viele Paare in `noten` stehen.',
     given="noten = {'Mathe': 2, 'Deutsch': 3, 'Englisch': 1, 'Info': 1}",
     solution="""noten = {'Mathe': 2, 'Deutsch': 3, 'Englisch': 1, 'Info': 1}
print(len(noten))""")
task('Erstelle ein leeres Dictionary. Gib seinen Datentyp und seine Länge aus.',
     solution="""d = {}
print(type(d))
print(len(d))""")
task("Erstelle mit `dict()` und Schlüsselwort-Argumenten ein Dictionary `person` mit `name='Bea'`, `alter=17` und `ort='Hamburg'`. Gib es aus.",
     solution="""person = dict(name='Bea', alter=17, ort='Hamburg')
print(person)""")
task("Erstelle ein Dictionary `telefonbuch`, das den Namen `'Ali'`, `'Bea'` und `'Cem'` die Nummern `'0301234'`, `'0405678'` und `'0899012'` zuordnet. Gib es aus.",
     solution="""telefonbuch = {'Ali': '0301234', 'Bea': '0405678', 'Cem': '0899012'}
print(telefonbuch)""")
task("Erstelle ein Dictionary `englisch`, das die englischen Wörter `'cat'`, `'dog'` und `'house'` ihrer deutschen Übersetzung zuordnet. Gib es aus.",
     solution="""englisch = {'cat': 'Katze', 'dog': 'Hund', 'house': 'Haus'}
print(englisch)""")
task('Erstelle ein Dictionary `quadrat`, das den Zahlen 1 bis 4 ihre Quadratzahlen zuordnet. Schlüssel und Werte sind hier Zahlen. Gib es aus.',
     solution="""quadrat = {1: 1, 2: 4, 3: 9, 4: 16}
print(quadrat)""")
task('Erstelle ein Dictionary `steckbrief` mit den Schlüsseln `name`, `alter` und `hobbys`. Der Wert zu `hobbys` soll eine Liste sein. Gib das Dictionary aus.',
     solution="""steckbrief = {'name': 'Mia', 'alter': 16, 'hobbys': ['Lesen', 'Fußball']}
print(steckbrief)""", kind='free')
predict("""d = {'a': 1, 'b': 2, 'a': 3}
print(d)
print(len(d))
print(type(d))""")
predict("""d = {['a', 'b']: 1}
print(d)""", error=TypeError)

# ---------------------------------------------------------------- 2
sec('Auf Werte zugreifen')
expl('''#### Zugriff mit `[]`

Mit `d[schluessel]` erhält man den Wert zu einem Schlüssel. Gibt es den Schlüssel nicht, gibt es einen `KeyError`.''',
     """auto = {'marke': 'VW', 'modell': 'Golf', 'baujahr': 2019}
print(auto['modell'])
print(auto['baujahr'] + 1)""")
expl('''#### `get()`

`d.get(schluessel)` gibt ebenfalls den Wert zurück. Gibt es den Schlüssel nicht, ist das Ergebnis `None`, es gibt **keinen** Fehler.
Mit `d.get(schluessel, standard)` erhält man statt `None` den Wert `standard`.''',
     """auto = {'marke': 'VW', 'modell': 'Golf'}
print(auto.get('marke'))
print(auto.get('farbe'))
print(auto.get('farbe', 'unbekannt'))""")
expl('''#### `in`

`schluessel in d` prüft, ob es einen **Schlüssel** gibt. Die Werte werden dabei nicht durchsucht.''',
     """auto = {'marke': 'VW', 'modell': 'Golf'}
print('marke' in auto)
print('VW' in auto)""")

NOTEN = "noten = {'Mathe': 2, 'Deutsch': 3, 'Englisch': 1, 'Info': 1}"
task('Gib die Note in Mathe aus.',
     given=NOTEN, solution=NOTEN + """
print(noten['Mathe'])""")
task('Gib mit einem f-String den Satz unten aus.',
     given=NOTEN, solution=NOTEN + """
print(f"In Englisch hast du eine {noten['Englisch']}.")""")
task("Prüfe mit `in`, ob es in `noten` eine Note für `'Physik'` gibt. Gib `True` oder `False` aus.",
     given=NOTEN, solution=NOTEN + """
print('Physik' in noten)""")
task("Gib mit `get()` die Note für `'Physik'` aus. Es soll kein Fehler entstehen.",
     given=NOTEN, solution=NOTEN + """
print(noten.get('Physik'))""")
task("Gib mit `get()` die Note für `'Physik'` aus. Gibt es keine, soll `keine Note` ausgegeben werden.",
     given=NOTEN, solution=NOTEN + """
print(noten.get('Physik', 'keine Note'))""")
task('Berechne den Durchschnitt der Noten in Mathe und Deutsch und gib ihn aus.',
     given=NOTEN, solution=NOTEN + """
print((noten['Mathe'] + noten['Deutsch']) / 2)""")
task("Übersetze `wort` mit dem Dictionary `englisch`. Gibt es das Wort nicht, soll `unbekannt` ausgegeben werden. Teste auch mit `wort = 'mouse'`.",
     given="""englisch = {'cat': 'Katze', 'dog': 'Hund', 'house': 'Haus'}
wort = 'dog'""",
     solution="""englisch = {'cat': 'Katze', 'dog': 'Hund', 'house': 'Haus'}
wort = 'dog'
print(englisch.get(wort, 'unbekannt'))""")
task('Berechne mit einer Schleife über `einkauf` den Gesamtpreis. Die Preise stehen in `preise`. Gib ihn aus.',
     given="""preise = {'Milch': 2, 'Brot': 3, 'Käse': 5, 'Äpfel': 4}
einkauf = ['Brot', 'Käse', 'Milch', 'Brot']""",
     solution="""preise = {'Milch': 2, 'Brot': 3, 'Käse': 5, 'Äpfel': 4}
einkauf = ['Brot', 'Käse', 'Milch', 'Brot']
summe = 0
for produkt in einkauf:
    summe += preise[produkt]
print(summe)""")
task("""Gib die Telefonnummer von `name` aus. Gibt es den Namen nicht im Telefonbuch, gib `Name nicht gefunden` aus.
Verwende `in`. Teste auch mit `name = 'Dana'`.""",
     given="""telefonbuch = {'Ali': '0301234', 'Bea': '0405678', 'Cem': '0899012'}
name = 'Bea'""",
     solution="""telefonbuch = {'Ali': '0301234', 'Bea': '0405678', 'Cem': '0899012'}
name = 'Bea'
if name in telefonbuch:
    print(telefonbuch[name])
else:
    print('Name nicht gefunden')""")
predict("""d = {'x': 10, 'y': 20}
print(d['x'])
print(d.get('z'))
print(d.get('z', 0))
print('y' in d)
print(20 in d)""")
predict("""d = {'x': 10, 'y': 20}
print(d['z'])""", error=KeyError)

# ---------------------------------------------------------------- 3
sec('keys(), values() und items()')
expl('''#### `keys()`, `values()` und `items()`

- `d.keys()` liefert alle **Schlüssel**,
- `d.values()` alle **Werte**,
- `d.items()` alle **Paare** als Tupel `(schluessel, wert)`.

Mit `list(...)` kann man das Ergebnis in eine Liste umwandeln. Funktionen wie `sum()`, `min()`, `max()` und `sorted()`
kann man direkt darauf anwenden. `sorted(d)` gibt die Schlüssel sortiert als Liste zurück.''',
     """noten = {'Mathe': 2, 'Deutsch': 3, 'Info': 1}
print(list(noten.keys()))
print(list(noten.values()))
print(list(noten.items()))
print(sum(noten.values()))
print(sorted(noten))""")

task('Gib alle Fächer aus `noten` als Liste aus.',
     given=NOTEN, solution=NOTEN + """
print(list(noten.keys()))""")
task('Gib alle Noten aus `noten` als Liste aus.',
     given=NOTEN, solution=NOTEN + """
print(list(noten.values()))""")
task('Gib die Summe aller Noten aus.',
     given=NOTEN, solution=NOTEN + """
print(sum(noten.values()))""")
task('Berechne den Notendurchschnitt und gib ihn aus.',
     given=NOTEN, solution=NOTEN + """
print(sum(noten.values()) / len(noten))""")
task('Gib die beste (kleinste) und die schlechteste (größte) Note aus.',
     given=NOTEN, solution=NOTEN + """
print(min(noten.values()))
print(max(noten.values()))""")
task('Gib alle Paare aus `noten` als Liste von Tupeln aus.',
     given=NOTEN, solution=NOTEN + """
print(list(noten.items()))""")
task('Gib die Fächer alphabetisch sortiert als Liste aus.',
     given=NOTEN, solution=NOTEN + """
print(sorted(noten))""")
task('Prüfe mit `in` und `values()`, ob irgendwo eine 1 als Note vorkommt. Gib `True` oder `False` aus.',
     given=NOTEN, solution=NOTEN + """
print(1 in noten.values())""")
task('Gib aus, in wie vielen Fächern die Note 1 ist. Wandle dazu die Werte in eine Liste um und verwende `count()`.',
     given=NOTEN, solution=NOTEN + """
print(list(noten.values()).count(1))""")
predict("""d = {'b': 2, 'a': 1}
print(list(d.keys()))
print(list(d.values()))
print(list(d.items()))
print(sorted(d))
print(len(d.items()))""")

# ---------------------------------------------------------------- 4
sec('Ändern und hinzufügen')
expl('''#### Wert ändern oder Paar hinzufügen

Mit `d[schluessel] = wert` **ändert** man den Wert, wenn es den Schlüssel schon gibt.
Gibt es ihn noch nicht, wird ein **neues Paar** am Ende hinzugefügt.''',
     """noten = {'Mathe': 2, 'Deutsch': 3}
noten['Deutsch'] = 2
noten['Info'] = 1
print(noten)""")
expl('''#### `update()`

`d.update(anderes_dict)` übernimmt alle Paare aus einem anderen Dictionary.
Vorhandene Schlüssel bekommen den neuen Wert, neue Schlüssel werden hinzugefügt.''',
     """noten = {'Mathe': 2, 'Deutsch': 3}
noten.update({'Mathe': 1, 'Kunst': 2})
print(noten)""")

task('Ändere die Note in Deutsch auf 2. Gib `noten` aus.',
     given=NOTEN, solution=NOTEN + """
noten['Deutsch'] = 2
print(noten)""")
task("Füge das Fach `'Physik'` mit der Note 3 hinzu. Gib `noten` aus.",
     given=NOTEN, solution=NOTEN + """
noten['Physik'] = 3
print(noten)""")
task("Übernimm mit `update()` die Noten `{'Mathe': 1, 'Kunst': 2}` in `noten`. Gib `noten` aus.",
     given=NOTEN, solution=NOTEN + """
noten.update({'Mathe': 1, 'Kunst': 2})
print(noten)""")
task("Es wurden 10 Äpfel geliefert. Erhöhe den Bestand an Äpfeln in `lager` um 10. Gib `lager` aus.",
     given="lager = {'Äpfel': 25, 'Birnen': 12, 'Kiwis': 0}",
     solution="""lager = {'Äpfel': 25, 'Birnen': 12, 'Kiwis': 0}
lager['Äpfel'] += 10
print(lager)""")
task('Erstelle ein leeres Dictionary `quadrat`. Füge mit einer Schleife für die Zahlen 1 bis 6 jeweils die Zahl als Schlüssel und ihr Quadrat als Wert hinzu. Gib es aus.',
     solution="""quadrat = {}
for i in range(1, 7):
    quadrat[i] = i * i
print(quadrat)""")
task("""`spieler` bekommt 5 Punkte dazu. Ist `spieler` noch nicht im Dictionary, beginnt er bei 0. Verwende `get()` mit Standardwert.
Gib `punkte` aus. Teste auch mit `spieler = 'Bea'`.""",
     given="""punkte = {'Ali': 12, 'Bea': 7}
spieler = 'Finn'""",
     solution="""punkte = {'Ali': 12, 'Bea': 7}
spieler = 'Finn'
punkte[spieler] = punkte.get(spieler, 0) + 5
print(punkte)""")
task('Erstelle mit einer Schleife aus den Listen `namen` und `alter` ein Dictionary, das jedem Namen sein Alter zuordnet. Gib es aus.',
     given="""namen = ['Ali', 'Bea', 'Cem']
alter = [16, 17, 15]""",
     solution="""namen = ['Ali', 'Bea', 'Cem']
alter = [16, 17, 15]
d = {}
for i in range(len(namen)):
    d[namen[i]] = alter[i]
print(d)""")
task('Erstelle ein Dictionary, das jedem Wort aus `woerter` seine Länge zuordnet. Gib es aus.',
     given="woerter = ['Haus', 'Elefant', 'Ei', 'Computer']",
     solution="""woerter = ['Haus', 'Elefant', 'Ei', 'Computer']
laengen = {}
for w in woerter:
    laengen[w] = len(w)
print(laengen)""")
predict("""d = {'a': 1}
d['b'] = 2
d['a'] = d['a'] + 10
d.update({'c': 3, 'b': 20})
print(d)""")

# ---------------------------------------------------------------- 5
sec('Entfernen')
expl('''#### `pop()`, `popitem()`, `del` und `clear()`

- `d.pop(schluessel)` entfernt das Paar mit diesem Schlüssel und **gibt den Wert zurück**. Fehlt der Schlüssel, gibt es einen `KeyError`.
  Mit `d.pop(schluessel, standard)` gibt es keinen Fehler, sondern den Wert `standard`.
- `d.popitem()` entfernt das **zuletzt hinzugefügte** Paar und gibt es als Tupel zurück.
- `del d[schluessel]` löscht das Paar mit diesem Schlüssel.
- `d.clear()` entfernt alle Paare.''',
     """d = {'a': 1, 'b': 2, 'c': 3, 'd': 4}
x = d.pop('a')
print(x, d)
paar = d.popitem()
print(paar, d)
del d['b']
print(d)
d.clear()
print(d)""")
expl('''#### Entfernen in einer Schleife

Während man mit einer Schleife über ein Dictionary läuft, darf man keine Paare entfernen. Das gibt einen Fehler.
Man läuft deshalb über eine **Liste** der Schlüssel: `for k in list(d):`.''',
     """lager = {'Äpfel': 25, 'Birnen': 0, 'Kiwis': 0}
for k in list(lager):
    if lager[k] == 0:
        del lager[k]
print(lager)""")

task("Entferne mit `pop()` das Fach `'Info'` aus `noten`. Gib die entfernte Note und danach `noten` aus.",
     given=NOTEN, solution=NOTEN + """
x = noten.pop('Info')
print(x)
print(noten)""")
task("Lösche mit `del` das Fach `'Deutsch'`. Gib `noten` aus.",
     given=NOTEN, solution=NOTEN + """
del noten['Deutsch']
print(noten)""")
task('Entferne mit `popitem()` das zuletzt hinzugefügte Paar. Gib das entfernte Paar und danach `noten` aus.',
     given=NOTEN, solution=NOTEN + """
paar = noten.popitem()
print(paar)
print(noten)""")
task('Leere `noten` mit `clear()`. Gib danach `noten` und seine Länge aus.',
     given=NOTEN, solution=NOTEN + """
noten.clear()
print(noten)
print(len(noten))""")
task("Entferne mit `pop()` das Fach `'Physik'`, ohne dass ein Fehler entsteht, obwohl es nicht vorhanden ist. Gib `noten` aus.",
     given=NOTEN, solution=NOTEN + """
noten.pop('Physik', None)
print(noten)""")
task('Entferne alle Artikel aus `lager`, deren Bestand 0 ist. Gib `lager` aus.',
     given="lager = {'Äpfel': 25, 'Birnen': 0, 'Kiwis': 8, 'Mangos': 0}",
     solution="""lager = {'Äpfel': 25, 'Birnen': 0, 'Kiwis': 8, 'Mangos': 0}
for k in list(lager):
    if lager[k] == 0:
        del lager[k]
print(lager)""")
task('Entferne alle Fächer aus `noten`, deren Note schlechter als 2 ist. Gib `noten` aus.',
     given=NOTEN, solution=NOTEN + """
for fach in list(noten):
    if noten[fach] > 2:
        del noten[fach]
print(noten)""")
predict("""d = {'a': 1, 'b': 2, 'c': 3}
x = d.pop('a')
y = d.popitem()
print(x)
print(y)
print(d)""")
predict("""d = {'a': 1}
del d['b']""", error=KeyError)

# ---------------------------------------------------------------- 6
sec('Schleifen über Dictionaries')
expl('''#### Drei Arten von Schleifen

- `for k in d:` durchläuft die **Schlüssel**. Den Wert erhält man mit `d[k]`.
- `for v in d.values():` durchläuft die **Werte**.
- `for k, v in d.items():` durchläuft die **Paare**. Jedes Paar wird direkt in `k` und `v` entpackt.''',
     """noten = {'Mathe': 2, 'Deutsch': 3}
for fach in noten:
    print(fach, noten[fach])
for note in noten.values():
    print(note)
for fach, note in noten.items():
    print(f'{fach}: {note}')""")

HS = "hauptstaedte = {'Deutschland': 'Berlin', 'Frankreich': 'Paris', 'Italien': 'Rom', 'Spanien': 'Madrid'}"
task('Gib alle Länder aus, jedes in einer eigenen Zeile.',
     given=HS, solution=HS + """
for land in hauptstaedte:
    print(land)""")
task('Gib alle Hauptstädte aus, jede in einer eigenen Zeile.',
     given=HS, solution=HS + """
for stadt in hauptstaedte.values():
    print(stadt)""")
task('Gib für jedes Land den Satz unten aus. Verwende `items()`.',
     given=HS, solution=HS + """
for land, stadt in hauptstaedte.items():
    print(f'Die Hauptstadt von {land} ist {stadt}.')""")
task('Gib jedes Fach mit seiner Note aus wie unten.',
     given=NOTEN, solution=NOTEN + """
for fach, note in noten.items():
    print(f'{fach}: {note}')""")
task('Gib alle Fächer aus, in denen die Note 1 ist.',
     given=NOTEN, solution=NOTEN + """
for fach, note in noten.items():
    if note == 1:
        print(fach)""")
task('Zähle die Fächer, in denen die Note besser als 3 ist. Gib die Anzahl aus.',
     given=NOTEN, solution=NOTEN + """
anzahl = 0
for note in noten.values():
    if note < 3:
        anzahl += 1
print(anzahl)""")
task('Erhöhe jeden Preis in `preise` um 1. Gib `preise` aus.',
     given="preise = {'Milch': 2, 'Brot': 3, 'Käse': 5}",
     solution="""preise = {'Milch': 2, 'Brot': 3, 'Käse': 5}
for p in preise:
    preise[p] += 1
print(preise)""")
task('Finde mit einer Schleife das Fach mit der schlechtesten (größten) Note. Gib das Fach aus.',
     given=NOTEN, solution=NOTEN + """
schlechtestes = ''
schlechteste_note = 0
for fach, note in noten.items():
    if note > schlechteste_note:
        schlechtestes = fach
        schlechteste_note = note
print(schlechtestes)""")
task('Erstelle ein neues Dictionary, das umgekehrt jeder Hauptstadt ihr Land zuordnet. Gib es aus.',
     given=HS, solution=HS + """
laender = {}
for land, stadt in hauptstaedte.items():
    laender[stadt] = land
print(laender)""")
task('Gib das Telefonbuch alphabetisch nach Namen sortiert aus wie unten.',
     given="telefonbuch = {'Cem': '0899012', 'Ali': '0301234', 'Dana': '0221111', 'Bea': '0405678'}",
     solution="""telefonbuch = {'Cem': '0899012', 'Ali': '0301234', 'Dana': '0221111', 'Bea': '0405678'}
for name in sorted(telefonbuch):
    print(name, telefonbuch[name])""")
task('In `warenkorb` steht, wie viel man von jedem Produkt kauft, in `preise` der Einzelpreis. Berechne den Gesamtpreis und gib ihn aus.',
     given="""preise = {'Milch': 2, 'Brot': 3, 'Käse': 5}
warenkorb = {'Milch': 3, 'Käse': 2}""",
     solution="""preise = {'Milch': 2, 'Brot': 3, 'Käse': 5}
warenkorb = {'Milch': 3, 'Käse': 2}
summe = 0
for produkt, anzahl in warenkorb.items():
    summe += preise[produkt] * anzahl
print(summe)""")
predict("""d = {'a': 3, 'b': 1, 'c': 2}
for k, v in d.items():
    print(k * v)
s = 0
for k in d:
    s += d[k]
print(s)""")

# ---------------------------------------------------------------- 7
sec('Zählen und Gruppieren')
expl('''#### Zählen mit einem Dictionary

Ein Dictionary eignet sich gut zum **Zählen**: Der Schlüssel ist das, was gezählt wird, der Wert ist die Anzahl.
Kommt ein Schlüssel zum ersten Mal vor, beginnt man bei 0. Das geht mit `if ... in ...` oder kürzer mit `get()`.''',
     """zaehler = {}
for c in 'banane':
    if c in zaehler:
        zaehler[c] += 1
    else:
        zaehler[c] = 1
print(zaehler)

zaehler2 = {}
for c in 'banane':
    zaehler2[c] = zaehler2.get(c, 0) + 1
print(zaehler2)""")
expl('''#### Gruppieren und `setdefault()`

Zum **Gruppieren** nimmt man Listen als Werte. Kommt ein Schlüssel zum ersten Mal vor, legt man eine leere Liste an.

`d.setdefault(schluessel, standard)` gibt den Wert zum Schlüssel zurück. Fehlt der Schlüssel, wird er vorher mit dem Wert `standard` angelegt.
So kann man in einer Zeile gruppieren: `d.setdefault(k, []).append(x)`.''',
     """gruppen = {}
for w in ['Ast', 'Ei', 'Affe', 'Eis']:
    if w[0] not in gruppen:
        gruppen[w[0]] = []
    gruppen[w[0]].append(w)
print(gruppen)

gruppen2 = {}
for w in ['Ast', 'Ei', 'Affe', 'Eis']:
    gruppen2.setdefault(w[0], []).append(w)
print(gruppen2)""")

WURF = 'wuerfe = [6, 2, 6, 3, 1, 6, 4, 2, 3, 2]'
task('Zähle mit einem Dictionary, wie oft jede Augenzahl in `wuerfe` vorkommt. Verwende `if ... in ...`. Gib das Dictionary aus.',
     given=WURF, solution=WURF + """
anzahl = {}
for w in wuerfe:
    if w in anzahl:
        anzahl[w] += 1
    else:
        anzahl[w] = 1
print(anzahl)""")
task('Zähle mit einem Dictionary und `get()`, wie oft jeder Buchstabe in `wort` vorkommt. Gib das Dictionary aus.',
     given="wort = 'mississippi'",
     solution="""wort = 'mississippi'
anzahl = {}
for c in wort:
    anzahl[c] = anzahl.get(c, 0) + 1
print(anzahl)""")
task('Zähle, wie oft jedes Wort in `satz` vorkommt. Groß- und Kleinschreibung sollen keine Rolle spielen. Gib das Dictionary aus.',
     given="satz = 'Der Hund und die Katze und der Hund'",
     solution="""satz = 'Der Hund und die Katze und der Hund'
anzahl = {}
for w in satz.lower().split():
    anzahl[w] = anzahl.get(w, 0) + 1
print(anzahl)""")
task('Zähle die Stimmen in `stimmen` und gib für jeden Kandidaten die Anzahl aus wie unten.',
     given="stimmen = ['Ali', 'Bea', 'Ali', 'Cem', 'Bea', 'Ali', 'Bea', 'Cem', 'Bea']",
     solution="""stimmen = ['Ali', 'Bea', 'Ali', 'Cem', 'Bea', 'Ali', 'Bea', 'Cem', 'Bea']
anzahl = {}
for s in stimmen:
    anzahl[s] = anzahl.get(s, 0) + 1
for name, n in anzahl.items():
    print(f'{name}: {n} Stimmen')""")
task('Finde mit den gezählten Stimmen aus der vorigen Aufgabe den Gewinner und gib ihn aus.',
     given="stimmen = ['Ali', 'Bea', 'Ali', 'Cem', 'Bea', 'Ali', 'Bea', 'Cem', 'Bea']",
     solution="""stimmen = ['Ali', 'Bea', 'Ali', 'Cem', 'Bea', 'Ali', 'Bea', 'Cem', 'Bea']
anzahl = {}
for s in stimmen:
    anzahl[s] = anzahl.get(s, 0) + 1
gewinner = ''
meiste = 0
for name, n in anzahl.items():
    if n > meiste:
        gewinner = name
        meiste = n
print(gewinner)""")
task('Gruppiere die Wörter nach ihrem Anfangsbuchstaben. Gib das Dictionary aus.',
     given="woerter = ['Apfel', 'Birne', 'Ananas', 'Banane', 'Kiwi', 'Aprikose']",
     solution="""woerter = ['Apfel', 'Birne', 'Ananas', 'Banane', 'Kiwi', 'Aprikose']
gruppen = {}
for w in woerter:
    if w[0] not in gruppen:
        gruppen[w[0]] = []
    gruppen[w[0]].append(w)
print(gruppen)""")
task('Gruppiere die Namen nach ihrer Länge. Verwende `setdefault()`. Gib das Dictionary aus.',
     given="namen = ['Ali', 'Bea', 'Dana', 'Finn', 'Gül', 'Hannah']",
     solution="""namen = ['Ali', 'Bea', 'Dana', 'Finn', 'Gül', 'Hannah']
gruppen = {}
for n in namen:
    gruppen.setdefault(len(n), []).append(n)
print(gruppen)""")
task('Jedes Tupel in `belegung` enthält einen Schüler und einen Kurs. Erstelle ein Dictionary, das jedem Kurs die Liste seiner Schüler zuordnet. Gib es aus.',
     given="belegung = [('Ali', 'Info'), ('Bea', 'Kunst'), ('Ali', 'Sport'), ('Cem', 'Info'), ('Bea', 'Info')]",
     solution="""belegung = [('Ali', 'Info'), ('Bea', 'Kunst'), ('Ali', 'Sport'), ('Cem', 'Info'), ('Bea', 'Info')]
kurse = {}
for name, kurs in belegung:
    kurse.setdefault(kurs, []).append(name)
print(kurse)""")
task('Berechne für jedes Fach in `tests` die Summe der Punkte. Gib das Dictionary aus.',
     given="tests = [('Mathe', 12), ('Info', 15), ('Mathe', 9), ('Deutsch', 11), ('Info', 13)]",
     solution="""tests = [('Mathe', 12), ('Info', 15), ('Mathe', 9), ('Deutsch', 11), ('Info', 13)]
summen = {}
for fach, punkte in tests:
    summen[fach] = summen.get(fach, 0) + punkte
print(summen)""")
predict("""z = {}
for c in 'abca':
    z[c] = z.get(c, 0) + 1
print(z)
g = {}
for w in ['Ei', 'Ast', 'Eis']:
    g.setdefault(w[0], []).append(w)
print(g)""")

# ---------------------------------------------------------------- 8
sec('Kopieren und Verschachteln')
expl('''#### `copy()`

Wie bei Listen ist `b = a` **keine** Kopie. Eine echte Kopie erhält man mit `b = a.copy()` oder `b = dict(a)`.''',
     """a = {'x': 1}
b = a
c = a.copy()
b['y'] = 2
print(a)
print(c)""")
expl('''#### Verschachtelte Dictionaries

Ein Wert kann selbst ein Dictionary sein. Dann greift man mit zwei Schlüsseln zu: `d['ali']['alter']`.
Oft hat man auch eine **Liste von Dictionaries**, z. B. eine Liste von Büchern, oder ein Dictionary mit **Listen als Werten**.''',
     """schueler = {
    'ali': {'alter': 16, 'ort': 'Berlin'},
    'bea': {'alter': 17, 'ort': 'Hamburg'},
}
print(schueler['bea']['ort'])
for name, daten in schueler.items():
    print(name, daten['alter'])""")

task("Erstelle mit `copy()` eine Kopie `neu` von `noten`. Ändere in der Kopie die Note in Mathe auf 1. Gib beide Dictionaries aus.",
     given=NOTEN, solution=NOTEN + """
neu = noten.copy()
neu['Mathe'] = 1
print(noten)
print(neu)""")
SCH = """schueler = {
    'ali': {'alter': 16, 'ort': 'Berlin'},
    'bea': {'alter': 17, 'ort': 'Hamburg'},
    'cem': {'alter': 15, 'ort': 'Köln'},
}"""
task("Gib das Alter von `'bea'` aus.",
     given=SCH, solution=SCH + """
print(schueler['bea']['alter'])""")
task("`'ali'` ist nach München gezogen. Ändere seinen Ort. Gib `schueler['ali']` aus.",
     given=SCH, solution=SCH + """
schueler['ali']['ort'] = 'München'
print(schueler['ali'])""")
task("Füge den Schüler `'dana'` mit dem Alter 16 und dem Ort `'Bonn'` hinzu. Gib die Liste der Schlüssel von `schueler` aus.",
     given=SCH, solution=SCH + """
schueler['dana'] = {'alter': 16, 'ort': 'Bonn'}
print(list(schueler))""")
task('Gib für jeden Schüler den Satz unten aus.',
     given=SCH, solution=SCH + """
for name, daten in schueler.items():
    print(f"{name} ({daten['alter']}) wohnt in {daten['ort']}.")""")
task('Berechne das Durchschnittsalter der Schüler und gib es aus.',
     given=SCH, solution=SCH + """
summe = 0
for daten in schueler.values():
    summe += daten['alter']
print(summe / len(schueler))""")
BUECHER = """buecher = [
    {'titel': 'Momo', 'autor': 'Michael Ende', 'jahr': 1973},
    {'titel': 'Tschick', 'autor': 'Wolfgang Herrndorf', 'jahr': 2010},
    {'titel': 'Der Vorleser', 'autor': 'Bernhard Schlink', 'jahr': 1995},
    {'titel': 'Qualityland', 'autor': 'Marc-Uwe Kling', 'jahr': 2017},
]"""
task('Gib die Titel aller Bücher aus, die vor dem Jahr 2000 erschienen sind.',
     given=BUECHER, solution=BUECHER + """
for b in buecher:
    if b['jahr'] < 2000:
        print(b['titel'])""")
task('Finde das neueste Buch und gib Titel und Autor aus wie unten.',
     given=BUECHER, solution=BUECHER + """
neuestes = buecher[0]
for b in buecher:
    if b['jahr'] > neuestes['jahr']:
        neuestes = b
print(f"{neuestes['titel']} von {neuestes['autor']}")""")
task('Berechne für jede Person in `noten` den Notendurchschnitt und gib ihn mit zwei Nachkommastellen aus wie unten.',
     given="noten = {'Ali': [2, 3, 1], 'Bea': [1, 1, 2], 'Cem': [3, 4, 3, 2]}",
     solution="""noten = {'Ali': [2, 3, 1], 'Bea': [1, 1, 2], 'Cem': [3, 4, 3, 2]}
for name, liste in noten.items():
    print(f'{name}: {sum(liste) / len(liste):.2f}')""")
task("Füge `'Bea'` in `noten` eine weitere Note 3 hinzu. Gib danach `noten['Bea']` aus.",
     given="noten = {'Ali': [2, 3, 1], 'Bea': [1, 1, 2], 'Cem': [3, 4, 3, 2]}",
     solution="""noten = {'Ali': [2, 3, 1], 'Bea': [1, 1, 2], 'Cem': [3, 4, 3, 2]}
noten['Bea'].append(3)
print(noten['Bea'])""")
predict("""a = {'x': 1, 'y': 2}
b = a
b['x'] = 99
c = dict(a)
c['y'] = 0
print(a)
print(c)""")
predict("""d = {'a': {'x': 1}, 'b': {'x': 2}}
d['a']['x'] = 5
print(d['a'])
print(d['b']['x'] + d['a']['x'])
print(len(d))""")

# ---------------------------------------------------------------- 9
sec('Gemischte Übungen')
task('Übersetze `satz` Wort für Wort mit `woerterbuch` ins Englische. Wörter, die nicht im Wörterbuch stehen, bleiben unverändert. Gib den übersetzten Satz aus.',
     given="""woerterbuch = {'ich': 'I', 'mag': 'like', 'katzen': 'cats', 'und': 'and', 'hunde': 'dogs'}
satz = 'ich mag katzen und pizza'""",
     solution="""woerterbuch = {'ich': 'I', 'mag': 'like', 'katzen': 'cats', 'und': 'and', 'hunde': 'dogs'}
satz = 'ich mag katzen und pizza'
ergebnis = []
for w in satz.split():
    ergebnis.append(woerterbuch.get(w, w))
print(' '.join(ergebnis))""")
task('Übersetze `text` mit dem Dictionary `morse` in Morsezeichen. Trenne die Buchstaben durch ein Leerzeichen. Gib das Ergebnis aus.',
     given="""morse = {'S': '...', 'O': '---', 'H': '....', 'E': '.', 'L': '.-..', 'P': '.--.'}
text = 'HELP'""",
     solution="""morse = {'S': '...', 'O': '---', 'H': '....', 'E': '.', 'L': '.-..', 'P': '.--.'}
text = 'HELP'
codes = []
for c in text:
    codes.append(morse[c])
print(' '.join(codes))""")
task('Ziehe die Bestellungen vom Lager ab. Jedes Tupel in `bestellungen` enthält Artikel und Anzahl. Gib danach `lager` aus.',
     given="""lager = {'Stifte': 50, 'Hefte': 30, 'Lineale': 10}
bestellungen = [('Stifte', 12), ('Hefte', 5), ('Stifte', 8), ('Lineale', 10)]""",
     solution="""lager = {'Stifte': 50, 'Hefte': 30, 'Lineale': 10}
bestellungen = [('Stifte', 12), ('Hefte', 5), ('Stifte', 8), ('Lineale', 10)]
for artikel, anzahl in bestellungen:
    lager[artikel] -= anzahl
print(lager)""")
task('Gib jede Note aus `zeugnis` zusammen mit ihrer Bezeichnung aus `bezeichnung` aus wie unten.',
     given="""bezeichnung = {1: 'sehr gut', 2: 'gut', 3: 'befriedigend', 4: 'ausreichend', 5: 'mangelhaft', 6: 'ungenügend'}
zeugnis = {'Mathe': 2, 'Deutsch': 3, 'Info': 1}""",
     solution="""bezeichnung = {1: 'sehr gut', 2: 'gut', 3: 'befriedigend', 4: 'ausreichend', 5: 'mangelhaft', 6: 'ungenügend'}
zeugnis = {'Mathe': 2, 'Deutsch': 3, 'Info': 1}
for fach, note in zeugnis.items():
    print(f'{fach}: {bezeichnung[note]}')""")
task('Berechne den Wert der römischen Zahl `zahl`, indem du die Werte aller Ziffern addierst. Die Subtraktionsregel (z. B. IV = 4) musst du nicht beachten.',
     given="""roemisch = {'I': 1, 'V': 5, 'X': 10, 'L': 50, 'C': 100, 'D': 500, 'M': 1000}
zahl = 'MDCLXVI'""",
     solution="""roemisch = {'I': 1, 'V': 5, 'X': 10, 'L': 50, 'C': 100, 'D': 500, 'M': 1000}
zahl = 'MDCLXVI'
summe = 0
for c in zahl:
    summe += roemisch[c]
print(summe)""")
task("""Zwei Wörter sind Anagramme, wenn sie dieselben Buchstaben gleich oft enthalten. Zähle die Buchstaben beider Wörter in zwei Dictionaries
und vergleiche diese mit `==`. Gib `Anagramm` oder `kein Anagramm` aus. Teste auch mit `'Regal'` und `'Lager'`.""",
     given="""wort1 = 'Ampel'
wort2 = 'Lampe'""",
     solution="""wort1 = 'Ampel'
wort2 = 'Lampe'
z1 = {}
for c in wort1.lower():
    z1[c] = z1.get(c, 0) + 1
z2 = {}
for c in wort2.lower():
    z2[c] = z2.get(c, 0) + 1
if z1 == z2:
    print('Anagramm')
else:
    print('kein Anagramm')""")
task('Gib die Fächer sortiert aus, für die es sowohl in `halbjahr1` als auch in `halbjahr2` eine Note gibt. Verwende Sets.',
     given="""halbjahr1 = {'Mathe': 2, 'Deutsch': 3, 'Kunst': 1, 'Info': 2}
halbjahr2 = {'Mathe': 1, 'Info': 1, 'Physik': 3, 'Deutsch': 2}""",
     solution="""halbjahr1 = {'Mathe': 2, 'Deutsch': 3, 'Kunst': 1, 'Info': 2}
halbjahr2 = {'Mathe': 1, 'Info': 1, 'Physik': 3, 'Deutsch': 2}
print(sorted(set(halbjahr1) & set(halbjahr2)))""")
task('''Gib eine Rangliste aus, sortiert nach Punkten, die meisten zuerst. Sortiere dazu `list(punkte.items())` mit einer eigenen
Funktion als `key`, die das zweite Element eines Paares zurückgibt.''',
     given="punkte = {'Ali': 12, 'Bea': 19, 'Cem': 7, 'Dana': 15}",
     solution="""punkte = {'Ali': 12, 'Bea': 19, 'Cem': 7, 'Dana': 15}

def wert(paar):
    return paar[1]

rangliste = list(punkte.items())
rangliste.sort(key=wert, reverse=True)
for i in range(len(rangliste)):
    name, p = rangliste[i]
    print(f'{i + 1}. {name}: {p}')""")
task('Füge die beiden Lagerbestände zu einem neuen Dictionary zusammen. Kommt ein Artikel in beiden vor, werden die Anzahlen addiert. Gib das Ergebnis aus.',
     given="""laden = {'Stifte': 20, 'Hefte': 15}
keller = {'Hefte': 40, 'Lineale': 8}""",
     solution="""laden = {'Stifte': 20, 'Hefte': 15}
keller = {'Hefte': 40, 'Lineale': 8}
gesamt = laden.copy()
for artikel, anzahl in keller.items():
    gesamt[artikel] = gesamt.get(artikel, 0) + anzahl
print(gesamt)""")
task("Gib alle Namen aus dem Telefonbuch aus, deren Nummer mit der Berliner Vorwahl `'030'` beginnt.",
     given="telefonbuch = {'Ali': '0301234', 'Bea': '0405678', 'Cem': '0309012', 'Dana': '0221111'}",
     solution="""telefonbuch = {'Ali': '0301234', 'Bea': '0405678', 'Cem': '0309012', 'Dana': '0221111'}
for name, nummer in telefonbuch.items():
    if nummer.startswith('030'):
        print(name)""")
task('Erstelle ein Dictionary, das jeder Augenzahl von 1 bis 6 ihren Anteil an allen Würfen in Prozent zuordnet. Gib für jede Augenzahl den Anteil ohne Nachkommastellen aus wie unten.',
     given=WURF, solution=WURF + """
anzahl = {}
for w in wuerfe:
    anzahl[w] = anzahl.get(w, 0) + 1
for augen in range(1, 7):
    anteil = anzahl.get(augen, 0) / len(wuerfe) * 100
    print(f'{augen}: {anteil:.0f} %')""")
predict("""d = {'a': 1, 'b': 2}
e = {}
for k, v in d.items():
    e[v] = k
print(e)
print(e[2] + d['a'] * 3 * e[1])""")

generate('dictionaries', 'Dictionaries')
