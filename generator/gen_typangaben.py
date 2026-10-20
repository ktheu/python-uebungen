# Erzeugt ../content/typangaben.ipynb (siehe nbgen.py). Zwischen oop_vererbung und einem Notebook zu dataclasses.
#
# Python prüft Typangaben nicht. Ob sie stimmen, vergleichen die Schüler selbst mit der Lösung (kein Typprüfer):
# Aufgaben, in denen es um die Typangaben geht, bekommen mit th() den Hinweis VERGLEICH angehängt.
# Lokal Python 3.13, in JupyterLite 3.14 (Annotationen werden dort erst bei Bedarf ausgewertet): Verweise auf die eigene
# Klasse deshalb immer in Anführungszeichen ('Punkt'), sonst NameError in 3.13.
from nbgen import sec, expl, predict, generate
from oophilfe import t, tu

VERGLEICH = '\n\n*Python prüft Typangaben nicht. Vergleiche deine Typangaben deshalb mit der Lösung.*'


def th(text, given='', body='', kind='normal', anhaenge=None):
    """Aufgabe, bei der es (auch) um die Typangaben geht."""
    t(text + VERGLEICH, given, body, kind, anhaenge=anhaenge)


def thu(text, name, attribute, methoden, given='', body=''):
    """Wie th(), mit Klassendiagramm."""
    tu(text + VERGLEICH, name, attribute, methoden, given, body)


INTRO = '''Mit **Typangaben** (englisch *type hints*) schreibt man in den Code, welchen Typ eine Variable, ein Parameter oder ein Rückgabewert haben soll:
`def flaeche(breite: float, hoehe: float) -> float:`. Das macht Programme leichter lesbar, und Entwicklungsumgebungen können damit Fehler finden.
Die Schreibweise kennst du schon aus den UML-Klassendiagrammen: `+ einzahlen(betrag: float): void`.

**Wichtig:** Python selbst **prüft Typangaben nicht**. Ein Programm mit falschen Typangaben läuft genauso wie eines mit richtigen.
Bei vielen Aufgaben kann die erwartete Ausgabe deshalb nicht zeigen, ob deine Typangaben stimmen.
**Vergleiche deine Typangaben immer mit der Lösung**, die du unter der Aufgabe aufklappen kannst.

Du solltest Funktionen, Listen, Dictionaries, Tupel und die OOP-Notebooks 1 und 2 schon kennen.

Jeder Abschnitt beginnt mit kurzen Erklärungen und Beispielen. Führe die Beispiele aus und probiere sie ruhig ein wenig aus.
Danach folgen viele kleine Übungen. Wenn etwas vorgegeben ist, steht es schon in der Codezelle.'''

# ---------------------------------------------------------------- 1
sec('Typangaben bei Variablen')
expl('''#### Die Schreibweise

Hinter den Variablennamen schreibt man einen Doppelpunkt und den Typ: `alter: int = 16`. Die wichtigsten Typen:

| Typ | Werte |
|---|---|
| `int` | ganze Zahlen |
| `float` | Kommazahlen |
| `str` | Zeichenketten |
| `bool` | `True`, `False` |

Eine Typangabe ist eine **Information für Menschen und Werkzeuge**. Python merkt sie sich, prüft sie aber nicht.''',
     """alter: int = 16
preis: float = 2.49
name: str = 'Ali'
volljaehrig: bool = alter >= 18
print(alter, preis, name, volljaehrig)""")
expl('''#### Python prüft nicht

Auch mit einer falschen Typangabe läuft das Programm. Ein Fehler kommt erst, wenn mit dem Wert etwas Unpassendes gemacht wird,
genau wie ohne Typangabe.''',
     """anzahl: int = 'drei'
print(anzahl)
print(anzahl * 2)
print(anzahl + 1)""", error=TypeError)
expl('''#### `__annotations__`

Die Typangaben einer Funktion stehen in ihrem Attribut `__annotations__`, einem Dictionary vom Namen zum Typ. Der Rückgabetyp steht unter `'return'`.
Damit kannst du dir ansehen, was Python sich gemerkt hat.''',
     """def doppelt(x: int) -> int:
    return 2 * x

print(doppelt.__annotations__)
print(doppelt.__annotations__['x'])""")

th('Lege die Variablen `titel` (Text `Momo`), `seiten` (304), `preis` (12.0) und `gelesen` (`False`) mit Typangaben an und gib sie in einer Zeile aus.',
   body="""titel: str = 'Momo'
seiten: int = 304
preis: float = 12.0
gelesen: bool = False
print(titel, seiten, preis, gelesen)""")
th('Lege `temperatur` als Kommazahl mit dem Wert 21.5 und `stadt` als Text mit dem Wert `Ulm` an (mit Typangaben). Gib `Ulm: 21.5 °C` aus.',
   body="""temperatur: float = 21.5
stadt: str = 'Ulm'
print(f'{stadt}: {temperatur} °C')""")
predict("""punkte: int = 7
punkte = punkte / 2
print(punkte)""")
predict("""name: int = 'Bea'
print(name.upper())""")
predict("""x: str = 5
print(x + 5)
print(x + '5')""", error=TypeError)

# ---------------------------------------------------------------- 2
sec('Typangaben bei Funktionen')
expl('''#### Parameter und Rückgabewert

- Hinter jeden Parameter kommt `: Typ`.
- Hinter die Klammer kommt `-> Typ` für den **Rückgabewert**, dann der Doppelpunkt.
- Gibt die Funktion nichts zurück, schreibt man `-> None` (im UML-Diagramm steht dafür `void`).
- Bei Standardwerten steht die Typangabe vor dem `=`: `anzahl: int = 1`.''',
     """def flaeche(breite: float, hoehe: float) -> float:
    return breite * hoehe

def begruessen(name: str, mal: int = 1) -> None:
    for i in range(mal):
        print('Hallo', name)

def ist_gerade(n: int) -> bool:
    return n % 2 == 0

print(flaeche(2.5, 4))
begruessen('Mia', 2)
print(ist_gerade(7))""")
expl('''#### Lesbarer Code

Typangaben ersetzen oft einen Kommentar. Am Kopf der Funktion sieht man sofort, was hineingeht und was herauskommt:

```python
def preis_mit_rabatt(preis, rabatt):              # Rabatt in Prozent? als 0.2? Ergebnis gerundet?
def preis_mit_rabatt(preis: float, rabatt: int) -> float:
```

Bei der zweiten Zeile ist klar: Der Rabatt ist eine ganze Zahl (also Prozent), das Ergebnis eine Kommazahl.''',
     """def preis_mit_rabatt(preis: float, rabatt: int) -> float:
    return preis * (100 - rabatt) / 100

print(preis_mit_rabatt(80.0, 25))""")

th('Schreibe eine Funktion `quadrat(x)` für ganze Zahlen mit Typangaben. Gib `quadrat(12)` aus.',
   body="""def quadrat(x: int) -> int:
    return x * x

print(quadrat(12))""")
th('Schreibe eine Funktion `kreisflaeche(r)` mit Typangaben, die die Fläche mit `3.14` berechnet. Gib `kreisflaeche(10.0)` aus.',
   body="""def kreisflaeche(r: float) -> float:
    return 3.14 * r * r

print(kreisflaeche(10.0))""")
th('Schreibe eine Funktion `initialen(vorname, nachname)` mit Typangaben, die z. B. `A. B.` zurückgibt. Gib `initialen(\'Ada\', \'Byron\')` aus.',
   body="""def initialen(vorname: str, nachname: str) -> str:
    return f'{vorname[0]}. {nachname[0]}.'

print(initialen('Ada', 'Byron'))""")
th('Schreibe eine Funktion `ist_teiler(a, b)` mit Typangaben, die zurückgibt, ob `a` ein Teiler von `b` ist. Gib das Ergebnis für (3, 12) und (5, 12) aus.',
   body="""def ist_teiler(a: int, b: int) -> bool:
    return b % a == 0

print(ist_teiler(3, 12))
print(ist_teiler(5, 12))""")
th('Schreibe eine Funktion `linie(laenge, zeichen)` mit Typangaben, die eine Linie aus `laenge` Zeichen **ausgibt** und nichts zurückgibt. `zeichen` hat den Standardwert `\'-\'`. Rufe sie mit 10 und mit (5, `\'*\'`) auf.',
   body="""def linie(laenge: int, zeichen: str = '-') -> None:
    print(zeichen * laenge)

linie(10)
linie(5, '*')""")
th('''Ergänze die Typangaben in dieser Funktion. Schreibe dazu die ganze Funktion mit Typangaben in die Zelle und gib `note_in_text(2)` aus.
```python
def note_in_text(note):
    texte = ['sehr gut', 'gut', 'befriedigend', 'ausreichend', 'mangelhaft', 'ungenügend']
    return texte[note - 1]
```''',
   body="""def note_in_text(note: int) -> str:
    texte = ['sehr gut', 'gut', 'befriedigend', 'ausreichend', 'mangelhaft', 'ungenügend']
    return texte[note - 1]

print(note_in_text(2))""")
th('''Schreibe eine Funktion `brutto(netto, steuersatz)` mit Typangaben. `steuersatz` ist eine ganze Zahl in Prozent mit dem Standardwert 19. Gib `brutto(100.0)` und `brutto(100.0, 7)` aus.''',
   body="""def brutto(netto: float, steuersatz: int = 19) -> float:
    return netto * (100 + steuersatz) / 100

print(brutto(100.0))
print(brutto(100.0, 7))""")
t('Gib die Typangaben der Funktion `brutto` mit `__annotations__` aus.',
  "def brutto(netto: float, steuersatz: int = 19) -> float:\n    return netto * (100 + steuersatz) / 100",
  "print(brutto.__annotations__)")
t('Gib für jeden Parameter der Funktion `termin` den Namen des Typs aus, in der Form `tag: int`. Lass `\'return\'` weg. (`typ.__name__` gibt den Namen eines Typs.)',
  "def termin(tag: int, monat: int, titel: str, ganztags: bool) -> str:\n    return f'{tag}.{monat}. {titel}'",
  """for name, typ in termin.__annotations__.items():
    if name != 'return':
        print(f'{name}: {typ.__name__}')""")
predict("""def verdoppeln(x: int) -> int:
    return x * 2

print(verdoppeln(4))
print(verdoppeln('ha'))
print(verdoppeln(1.5))""")
predict("""def hallo(name: str) -> None:
    print('Hallo', name)

ergebnis = hallo('Ida')
print(ergebnis)""")

# ---------------------------------------------------------------- 3
sec('Listen, Dictionaries und Tupel')
expl('''#### Was steht in der Liste?

Bei Listen, Mengen und Dictionaries gibt man in eckigen Klammern an, welchen Typ die **Elemente** haben:

| Typangabe | bedeutet |
|---|---|
| `list[int]` | Liste mit ganzen Zahlen |
| `set[str]` | Menge von Zeichenketten |
| `dict[str, float]` | Dictionary: Schlüssel `str`, Werte `float` |
| `tuple[int, int]` | Tupel aus genau zwei ganzen Zahlen |
| `tuple[str, int, bool]` | Tupel aus Text, Zahl und Wahrheitswert |
| `tuple[int, ...]` | Tupel beliebiger Länge mit ganzen Zahlen |

Im UML-Diagramm stand bisher nur `list`. Mit Typangaben sieht man auch, was in der Liste steht.''',
     """def summe(zahlen: list[int]) -> int:
    s = 0
    for z in zahlen:
        s += z
    return s

def mittelpunkt(a: tuple[float, float], b: tuple[float, float]) -> tuple[float, float]:
    return ((a[0] + b[0]) / 2, (a[1] + b[1]) / 2)

preise: dict[str, float] = {'Brot': 2.49, 'Milch': 1.19}
print(summe([3, 4, 5]))
print(mittelpunkt((0, 0), (4, 2)))
print(preise['Brot'])""")

th('Schreibe eine Funktion `laengstes(woerter)` mit Typangaben, die das längste Wort einer Liste von Wörtern zurückgibt. Gib `laengstes([\'Hund\', \'Elefant\', \'Maus\'])` aus.',
   body="""def laengstes(woerter: list[str]) -> str:
    return max(woerter, key=len)

print(laengstes(['Hund', 'Elefant', 'Maus']))""")
th('Schreibe eine Funktion `gerade_zahlen(zahlen)` mit Typangaben, die eine neue Liste mit den geraden Zahlen zurückgibt. Gib das Ergebnis für `[3, 8, 5, 12, 7, 4]` aus.',
   body="""def gerade_zahlen(zahlen: list[int]) -> list[int]:
    ergebnis = []
    for z in zahlen:
        if z % 2 == 0:
            ergebnis.append(z)
    return ergebnis

print(gerade_zahlen([3, 8, 5, 12, 7, 4]))""")
th('Schreibe eine Funktion `buchstaben_zaehlen(text)` mit Typangaben, die ein Dictionary vom Buchstaben zur Anzahl zurückgibt. Gib das Ergebnis für `\'banane\'` aus.',
   body="""def buchstaben_zaehlen(text: str) -> dict[str, int]:
    d = {}
    for b in text:
        d[b] = d.get(b, 0) + 1
    return d

print(buchstaben_zaehlen('banane'))""")
th('Schreibe eine Funktion `min_max(zahlen)` mit Typangaben, die das kleinste und das größte Element als Tupel zurückgibt. Gib das Ergebnis für `[7, 2, 9, 4]` aus.',
   body="""def min_max(zahlen: list[int]) -> tuple[int, int]:
    return (min(zahlen), max(zahlen))

print(min_max([7, 2, 9, 4]))""")
th('''Schreibe eine Funktion `durchschnitte(noten)` mit Typangaben. Sie bekommt ein Dictionary vom Namen zu einer Liste von Noten und gibt ein Dictionary vom Namen zum
Durchschnitt zurück. Gib das Ergebnis für `{'Ali': [2, 3, 1], 'Bea': [1, 2]}` aus.''',
   body="""def durchschnitte(noten: dict[str, list[int]]) -> dict[str, float]:
    ergebnis = {}
    for name, liste in noten.items():
        ergebnis[name] = sum(liste) / len(liste)
    return ergebnis

print(durchschnitte({'Ali': [2, 3, 1], 'Bea': [1, 2]}))""")
th('''Schreibe eine Funktion `woerter_mit(woerter, buchstabe)` mit Typangaben, die die **Menge** der Wörter zurückgibt, in denen der Buchstabe vorkommt.
Gib das Ergebnis sortiert aus für `['Apfel', 'Birne', 'Pflaume', 'Kiwi']` und `'e'`.''',
   body="""def woerter_mit(woerter: list[str], buchstabe: str) -> set[str]:
    ergebnis = set()
    for w in woerter:
        if buchstabe in w:
            ergebnis.add(w)
    return ergebnis

print(sorted(woerter_mit(['Apfel', 'Birne', 'Pflaume', 'Kiwi'], 'e')))""")
th('''Ergänze die Typangaben. Schreibe die Funktion mit Typangaben in die Zelle und gib `bester([('Ali', 17), ('Bea', 23), ('Cem', 19)])` aus.
```python
def bester(ergebnisse):
    name, punkte = ergebnisse[0]
    for n, p in ergebnisse:
        if p > punkte:
            name, punkte = n, p
    return name
```''',
   body="""def bester(ergebnisse: list[tuple[str, int]]) -> str:
    name, punkte = ergebnisse[0]
    for n, p in ergebnisse:
        if p > punkte:
            name, punkte = n, p
    return name

print(bester([('Ali', 17), ('Bea', 23), ('Cem', 19)]))""")
th('''Lege eine Variable `stundenplan` mit Typangabe an: ein Dictionary vom Wochentag zu einer Liste von Fächern, mit Mo: Mathe, Deutsch und Di: Sport.
Gib die Anzahl der Fächer am Montag aus.''',
   body="""stundenplan: dict[str, list[str]] = {'Mo': ['Mathe', 'Deutsch'], 'Di': ['Sport']}
print(len(stundenplan['Mo']))""")
t('Gib die Typangaben der Funktion `mittelpunkt` mit `__annotations__` aus.',
  "def mittelpunkt(a: tuple[float, float], b: tuple[float, float]) -> tuple[float, float]:\n    return ((a[0] + b[0]) / 2, (a[1] + b[1]) / 2)",
  "print(mittelpunkt.__annotations__)")
predict("""def erstes(liste: list[int]) -> int:
    return liste[0]

print(erstes(['a', 'b']))
print(erstes('xyz'))""")

# ---------------------------------------------------------------- 4
sec('Mehrere mögliche Typen und None')
expl('''#### `|` heißt „oder“

- `int | float` bedeutet: eine ganze Zahl **oder** eine Kommazahl.
- `str | None` bedeutet: ein Text **oder** `None`. So schreibt man Funktionen, die manchmal nichts finden.

In älterem Code liest man dafür `Optional[str]` (aus dem Modul `typing`). Das bedeutet dasselbe wie `str | None`.''',
     """def suche(namen: list[str], anfang: str) -> str | None:
    for n in namen:
        if n.startswith(anfang):
            return n
    return None

def halbe(x: int | float) -> float:
    return x / 2

print(suche(['Ali', 'Bea', 'Cem'], 'B'))
print(suche(['Ali', 'Bea', 'Cem'], 'D'))
print(halbe(5), halbe(2.5))""")
expl('''#### `startswith()`

`text.startswith(anfang)` gibt `True` zurück, wenn der Text mit `anfang` beginnt (`endswith()` entsprechend für das Ende).''',
     """print('Banane'.startswith('Ba'), 'Banane'.endswith('ne'), 'Banane'.startswith('b'))""")

th('''Schreibe eine Funktion `als_zahl(text)` mit Typangaben, die den Text als ganze Zahl zurückgibt oder `None`, wenn er keine ganze Zahl ist (fange den `ValueError` ab).
Gib das Ergebnis für `'42'` und für `'zweiundvierzig'` aus.''',
   body="""def als_zahl(text: str) -> int | None:
    try:
        return int(text)
    except ValueError:
        return None

print(als_zahl('42'))
print(als_zahl('zweiundvierzig'))""")
th('''Schreibe eine Funktion `telefonnummer(buch, name)` mit Typangaben: `buch` ist ein Dictionary vom Namen zur Nummer (Text). Die Funktion gibt die Nummer zurück oder `None`.
Gib das Ergebnis für `Ali` und `Ida` aus.''',
   given="buch = {'Ali': '0711 123', 'Bea': '0151 999'}",
   body="""def telefonnummer(buch: dict[str, str], name: str) -> str | None:
    return buch.get(name)

print(telefonnummer(buch, 'Ali'))
print(telefonnummer(buch, 'Ida'))""")
th('Schreibe eine Funktion `betrag(x)` mit Typangaben, die für ganze Zahlen und Kommazahlen den Betrag zurückgibt (ohne `abs()`). Gib `betrag(-3)` und `betrag(-2.5)` aus.',
   body="""def betrag(x: int | float) -> int | float:
    if x < 0:
        return -x
    return x

print(betrag(-3))
print(betrag(-2.5))""")
th('''Schreibe eine Funktion `erste_negative(zahlen)` mit Typangaben, die die erste negative Zahl der Liste zurückgibt oder `None`.
Gib für jede Liste in `listen` das Ergebnis aus oder, wenn es `None` ist, `keine`.''',
   given="listen = [[3, -1, -5], [2, 4], [-7]]",
   body="""def erste_negative(zahlen: list[int]) -> int | None:
    for z in zahlen:
        if z < 0:
            return z
    return None

for liste in listen:
    ergebnis = erste_negative(liste)
    if ergebnis is None:
        print('keine')
    else:
        print(ergebnis)""")
t('Gib die Typangaben der Funktion `suche` mit `__annotations__` aus.',
  "def suche(namen: list[str], anfang: str) -> str | None:\n    for n in namen:\n        if n.startswith(anfang):\n            return n\n    return None",
  "print(suche.__annotations__)")

# ---------------------------------------------------------------- 5
sec('Typen selbst prüfen')
expl('''#### `isinstance()` und `raise TypeError`

Soll eine Funktion falsche Typen wirklich **ablehnen**, muss sie selbst prüfen: mit `isinstance(wert, typ)` und `raise TypeError(...)`.
`isinstance()` versteht auch `|`: `isinstance(x, int | float)`.

**Achtung:** `True` und `False` zählen in Python auch als `int` (`True` ist 1). Will man Wahrheitswerte ausschließen, prüft man das extra.''',
     """def wurzel(x: int | float) -> float:
    if not isinstance(x, int | float) or isinstance(x, bool):
        raise TypeError('Zahl erwartet')
    return x ** 0.5

print(wurzel(16))
print(isinstance(True, int))
for wert in ['16', True]:
    try:
        wurzel(wert)
    except TypeError as e:
        print(repr(wert), e)""")

th('''Schreibe eine Funktion `wiederhole(text, n)` mit Typangaben, die `text` `n`-mal hintereinander zurückgibt. Ist `text` kein `str` oder `n` kein `int`, löst sie
`TypeError('falscher Typ')` aus. Teste mit allen Paaren in `tests` und gib das Ergebnis oder die Fehlermeldung aus.''',
   given="tests = [('ha', 3), (3, 'ha'), ('ab', 2.0), ('-', 5)]",
   body="""def wiederhole(text: str, n: int) -> str:
    if not isinstance(text, str) or not isinstance(n, int):
        raise TypeError('falscher Typ')
    return text * n

for text, n in tests:
    try:
        print(wiederhole(text, n))
    except TypeError as e:
        print(e)""")
th('''Schreibe eine Funktion `summe(zahlen)` mit Typangaben für eine Liste aus ganzen Zahlen und Kommazahlen. Sie prüft jedes Element und löst bei einem anderen Typ
`TypeError` mit der Meldung `kein Zahlwert: '3'` aus (mit `repr()`). Teste mit `[1, 2.5, 3]` und `[1, '3', 4]`.''',
   body="""def summe(zahlen: list[int | float]) -> float:
    s = 0
    for z in zahlen:
        if not isinstance(z, int | float):
            raise TypeError(f'kein Zahlwert: {repr(z)}')
        s += z
    return s

print(summe([1, 2.5, 3]))
try:
    print(summe([1, '3', 4]))
except TypeError as e:
    print(e)""")
t('Gib für jeden Wert in `werte` aus, ob er mit `isinstance(w, int)` eine ganze Zahl ist und ob er ein `bool` ist, in der Form `5 True False`.',
  "werte = [5, 5.0, True, '5', 0]",
  """for w in werte:
    print(repr(w), isinstance(w, int), isinstance(w, bool))""")
predict("""def f(x: int) -> int:
    if not isinstance(x, int):
        raise TypeError('int erwartet')
    return x + 1

print(f(True))
print(f(2))
print(f(2.0))""", error=TypeError)

# ---------------------------------------------------------------- 6
sec('Typangaben in Klassen')
expl('''#### Attribute und Methoden

In Klassen gelten dieselben Regeln:

- Bei Methoden bekommt `self` **keine** Typangabe.
- Der Konstruktor gibt nichts zurück: `def __init__(self, name: str) -> None:`.
- Attribute kann man bei der ersten Zuweisung mit Typ angeben: `self.__kontostand: float = 0`.

So entspricht der Code fast Wort für Wort dem UML-Diagramm. `void` im Diagramm wird zu `-> None`.''',
     """class Konto:
    def __init__(self, inhaber: str) -> None:
        self.__inhaber: str = inhaber
        self.__kontostand: float = 0

    def einzahlen(self, betrag: float) -> None:
        self.__kontostand += betrag

    def get_kontostand(self) -> float:
        return self.__kontostand

k = Konto('Ali')
k.einzahlen(50)
print(k.get_kontostand())""")
expl('''#### Klassen als Typ

Eine eigene Klasse ist auch ein Typ: `def vorstellen(hund: Hund) -> str:` oder `list[Hund]`.

Innerhalb einer Klasse kann man ihren eigenen Namen noch nicht direkt benutzen, weil die Klasse erst am Ende der Definition fertig ist.
Dann schreibt man den Namen in **Anführungszeichen**: `def abstand(self, other: 'Punkt') -> float:`.''',
     """class Punkt:
    def __init__(self, x: float, y: float) -> None:
        self.x = x
        self.y = y

    def abstand(self, other: 'Punkt') -> float:
        return ((self.x - other.x) ** 2 + (self.y - other.y) ** 2) ** 0.5

    def verschoben(self, dx: float, dy: float) -> 'Punkt':
        return Punkt(self.x + dx, self.y + dy)

def am_weitesten(start: Punkt, punkte: list[Punkt]) -> Punkt:
    return max(punkte, key=lambda p: start.abstand(p))

p = Punkt(0, 0)
q = p.verschoben(3, 4)
print(p.abstand(q))
print(am_weitesten(p, [Punkt(1, 1), Punkt(-5, 0), q]).x)""")

thu('Setze die Klasse aus dem Diagramm mit allen Typangaben um. Erzeuge einen Spieler, gib ihm zweimal 10 Punkte und gib die Punkte aus.',
    'Spieler', ['- name: str', '- punkte: int'],
    ['+ Spieler(name: str)', '+ punkte_dazu(anzahl: int): void', '+ get_punkte(): int', '+ get_name(): str'],
    body="""class Spieler:
    def __init__(self, name: str) -> None:
        self.__name: str = name
        self.__punkte: int = 0

    def punkte_dazu(self, anzahl: int) -> None:
        self.__punkte += anzahl

    def get_punkte(self) -> int:
        return self.__punkte

    def get_name(self) -> str:
        return self.__name

s = Spieler('Mia')
s.punkte_dazu(10)
s.punkte_dazu(10)
print(s.get_punkte())""")
thu('''Setze die Klasse mit allen Typangaben um. In UML steht `list[float]`, also eine Liste von Kommazahlen. `durchschnitt()` gibt `None` zurück, wenn es noch keine
Messwerte gibt. Gib den Durchschnitt vor und nach dem Hinzufügen von 12.5, 14.0, 13.0 und 14.5 aus.''',
    'Messreihe', ['- name: str', '- werte: list[float]'],
    ['+ Messreihe(name: str)', '+ hinzufuegen(wert: float): void', '+ durchschnitt(): float | None'],
    body="""class Messreihe:
    def __init__(self, name: str) -> None:
        self.__name: str = name
        self.__werte: list[float] = []

    def hinzufuegen(self, wert: float) -> None:
        self.__werte.append(wert)

    def durchschnitt(self) -> float | None:
        if len(self.__werte) == 0:
            return None
        return sum(self.__werte) / len(self.__werte)

m = Messreihe('Temperatur')
print(m.durchschnitt())
for w in [12.5, 14.0, 13.0, 14.5]:
    m.hinzufuegen(w)
print(m.durchschnitt())""")
th('''Ergänze die Klasse `Bruch` um eine Methode `mal(other)`, die einen neuen Bruch zurückgibt, und eine Methode `ist_gleich(other)`, die `True` zurückgibt, wenn beide Brüche
denselben Wert haben (über Kreuz multiplizieren). Schreibe alle Typangaben, auch für die vorgegebenen Methoden. Gib `Bruch(1, 2).mal(Bruch(2, 3))` aus und ob `Bruch(1, 2)` gleich `Bruch(2, 4)` ist.''',
   body="""class Bruch:
    def __init__(self, zaehler: int, nenner: int) -> None:
        self.zaehler: int = zaehler
        self.nenner: int = nenner

    def __str__(self) -> str:
        return f'{self.zaehler}/{self.nenner}'

    def mal(self, other: 'Bruch') -> 'Bruch':
        return Bruch(self.zaehler * other.zaehler, self.nenner * other.nenner)

    def ist_gleich(self, other: 'Bruch') -> bool:
        return self.zaehler * other.nenner == other.zaehler * self.nenner

print(Bruch(1, 2).mal(Bruch(2, 3)))
print(Bruch(1, 2).ist_gleich(Bruch(2, 4)))""")
th('''Ergänze die Typangaben. Schreibe beide Klassen mit Typangaben in die Zelle, erzeuge eine Klasse mit drei Schülern und gib die Namen der Schüler mit Note 1 aus.
```python
class Schueler:
    def __init__(self, name, note):
        self.name = name
        self.note = note

class Klasse:
    def __init__(self, bezeichnung):
        self.bezeichnung = bezeichnung
        self.schueler = []

    def aufnehmen(self, s):
        self.schueler.append(s)

    def beste(self):
        namen = []
        for s in self.schueler:
            if s.note == 1:
                namen.append(s.name)
        return namen
```''',
   body="""class Schueler:
    def __init__(self, name: str, note: int) -> None:
        self.name: str = name
        self.note: int = note

class Klasse:
    def __init__(self, bezeichnung: str) -> None:
        self.bezeichnung: str = bezeichnung
        self.schueler: list[Schueler] = []

    def aufnehmen(self, s: Schueler) -> None:
        self.schueler.append(s)

    def beste(self) -> list[str]:
        namen = []
        for s in self.schueler:
            if s.note == 1:
                namen.append(s.name)
        return namen

k = Klasse('9a')
for name, note in [('Ali', 1), ('Bea', 2), ('Cem', 1)]:
    k.aufnehmen(Schueler(name, note))
print(k.beste())""")
th('''Schreibe eine Klasse `Mitarbeiter` mit Typangaben: Name (Text) und Chef (ein Mitarbeiter oder `None`, Standardwert `None`). Die Methode `get_chef()` gibt den Chef zurück,
`kette()` eine Liste der Namen bis nach oben. Gib die Kette für `ali` aus.''',
   body="""class Mitarbeiter:
    def __init__(self, name: str, chef: 'Mitarbeiter | None' = None) -> None:
        self.__name: str = name
        self.__chef: Mitarbeiter | None = chef

    def get_name(self) -> str:
        return self.__name

    def get_chef(self) -> 'Mitarbeiter | None':
        return self.__chef

    def kette(self) -> list[str]:
        namen = []
        m = self
        while m is not None:
            namen.append(m.get_name())
            m = m.get_chef()
        return namen

koenig = Mitarbeiter('Frau König')
graf = Mitarbeiter('Herr Graf', koenig)
ali = Mitarbeiter('Ali', graf)
print(ali.kette())""")
predict("""class Box:
    def __init__(self, inhalt: int) -> None:
        self.inhalt = inhalt

    def doppelt(self) -> int:
        return self.inhalt * 2

b = Box('Ei')
print(b.doppelt())
print(Box.doppelt.__annotations__)""")

# ---------------------------------------------------------------- 7
sec('Funktionen als Typ und Typnamen')
expl('''#### `Callable`

Manche Funktionen bekommen eine **andere Funktion** als Parameter, wie `key=` bei `sorted()`. Dafür gibt es den Typ `Callable` aus dem Modul `collections.abc`:
`Callable[[int], bool]` ist eine Funktion mit einem `int`-Parameter, die einen `bool` zurückgibt.''',
     """from collections.abc import Callable

def filtern(zahlen: list[int], bedingung: Callable[[int], bool]) -> list[int]:
    ergebnis = []
    for z in zahlen:
        if bedingung(z):
            ergebnis.append(z)
    return ergebnis

def ist_gerade(n: int) -> bool:
    return n % 2 == 0

print(filtern([1, 2, 3, 4, 5, 6], ist_gerade))
print(filtern([1, 2, 3, 4, 5, 6], lambda n: n > 4))""")
expl('''#### Eigene Typnamen

Lange Typangaben kann man unter einem eigenen Namen speichern: `type Koordinate = tuple[float, float]`.
Danach schreibt man einfach `Koordinate`. Das macht den Code kürzer und sagt, was gemeint ist.''',
     """type Koordinate = tuple[float, float]
type Notenliste = dict[str, list[int]]

def verschieben(p: Koordinate, dx: float) -> Koordinate:
    return (p[0] + dx, p[1])

noten: Notenliste = {'Ali': [2, 1]}
print(verschieben((1.0, 2.0), 3.0))
print(noten)""")

th('''Schreibe eine Funktion `anwenden(zahlen, f)` mit Typangaben, die `f` auf jede Zahl der Liste anwendet und die Liste der Ergebnisse zurückgibt (Zahlen sind `int`, `f` gibt `int` zurück).
Gib das Ergebnis für `[1, 2, 3]` mit `lambda x: x * x` und mit `abs` für `[-2, 5, -7]` aus.''',
   body="""from collections.abc import Callable

def anwenden(zahlen: list[int], f: Callable[[int], int]) -> list[int]:
    ergebnis = []
    for z in zahlen:
        ergebnis.append(f(z))
    return ergebnis

print(anwenden([1, 2, 3], lambda x: x * x))
print(anwenden([-2, 5, -7], abs))""")
th('''Lege den Typnamen `Rgb` für ein Tupel aus drei ganzen Zahlen an. Schreibe eine Funktion `heller(farbe, wert)` mit Typangaben, die jeden Anteil um `wert` erhöht,
aber höchstens bis 255. Gib `heller((200, 100, 250), 30)` aus.''',
   body="""type Rgb = tuple[int, int, int]

def heller(farbe: Rgb, wert: int) -> Rgb:
    r, g, b = farbe
    return (min(r + wert, 255), min(g + wert, 255), min(b + wert, 255))

print(heller((200, 100, 250), 30))""")
th('''Schreibe eine Funktion `zaehle_wenn(woerter, bedingung)` mit Typangaben, die zählt, für wie viele Wörter die Bedingung `True` ist. Gib für `woerter` aus, wie viele Wörter
länger als 4 Buchstaben sind und wie viele mit `S` beginnen.''',
   given="woerter = ['Sonne', 'Mond', 'Sterne', 'Himmel', 'Sand']",
   body="""from collections.abc import Callable

def zaehle_wenn(woerter: list[str], bedingung: Callable[[str], bool]) -> int:
    anzahl = 0
    for w in woerter:
        if bedingung(w):
            anzahl += 1
    return anzahl

print(zaehle_wenn(woerter, lambda w: len(w) > 4))
print(zaehle_wenn(woerter, lambda w: w.startswith('S')))""")

# ---------------------------------------------------------------- 8
sec('Gemischte Übungen')
th('''Schreibe mit Typangaben: eine Funktion `einlesen(zeilen)`, die Zeilen der Form `Name;Punkte` in ein Dictionary vom Namen zu den Punkten (int) umwandelt und fehlerhafte Zeilen
überspringt, und eine Funktion `sieger(punkte)`, die den Namen mit den meisten Punkten zurückgibt oder `None` bei leerem Dictionary. Gib beides für `zeilen` aus und `sieger({})`.''',
   given="zeilen = ['Ali;17', 'Bea;zwanzig', 'Cem;23', 'Dana', 'Emil;9']",
   body="""def einlesen(zeilen: list[str]) -> dict[str, int]:
    ergebnis = {}
    for z in zeilen:
        try:
            name, punkte = z.split(';')
            ergebnis[name] = int(punkte)
        except ValueError:
            pass
    return ergebnis

def sieger(punkte: dict[str, int]) -> str | None:
    if len(punkte) == 0:
        return None
    return max(punkte, key=lambda name: punkte[name])

p = einlesen(zeilen)
print(p)
print(sieger(p))
print(sieger({}))""")
thu('''Setze die Klasse aus dem Diagramm mit allen Typangaben um. `hinzufuegen()` fügt einen Artikel mit Menge hinzu (gibt es ihn schon, wird die Menge erhöht),
`entnehmen()` verringert die Menge und gibt `False` zurück, wenn nicht genug da ist, `bestand()` gibt die Menge zurück (0, wenn es den Artikel nicht gibt).
Teste: 10 Schrauben und 4 Dübel hinzufügen, 3 Schrauben entnehmen, 5 Dübel entnehmen; gib die Ergebnisse und beide Bestände aus.''',
    'Lager', ['- artikel: dict[str, int]'],
    ['+ Lager()', '+ hinzufuegen(name: str, menge: int): void', '+ entnehmen(name: str, menge: int): bool', '+ bestand(name: str): int'],
    body="""class Lager:
    def __init__(self) -> None:
        self.__artikel: dict[str, int] = {}

    def hinzufuegen(self, name: str, menge: int) -> None:
        self.__artikel[name] = self.__artikel.get(name, 0) + menge

    def entnehmen(self, name: str, menge: int) -> bool:
        if self.bestand(name) < menge:
            return False
        self.__artikel[name] -= menge
        return True

    def bestand(self, name: str) -> int:
        return self.__artikel.get(name, 0)

l = Lager()
l.hinzufuegen('Schraube', 10)
l.hinzufuegen('Dübel', 4)
print(l.entnehmen('Schraube', 3))
print(l.entnehmen('Dübel', 5))
print(l.bestand('Schraube'), l.bestand('Dübel'))""")
th('''Schreibe eine Klasse `Rechteck` mit Typangaben (Breite und Höhe als `float`) mit den Methoden `flaeche()` und `passt_in(other)`, die zurückgibt, ob das Rechteck
(ohne Drehen) in ein anderes passt. Schreibe außerdem eine Funktion `groesstes(rechtecke)` mit Typangaben, die das Rechteck mit der größten Fläche zurückgibt.
Teste mit den Rechtecken (2, 3), (4, 1) und (5, 5): gib die Fläche des größten aus und ob (2, 3) in (5, 5) und (4, 1) in (2, 3) passt.''',
   body="""class Rechteck:
    def __init__(self, breite: float, hoehe: float) -> None:
        self.breite: float = breite
        self.hoehe: float = hoehe

    def flaeche(self) -> float:
        return self.breite * self.hoehe

    def passt_in(self, other: 'Rechteck') -> bool:
        return self.breite <= other.breite and self.hoehe <= other.hoehe

def groesstes(rechtecke: list[Rechteck]) -> Rechteck:
    return max(rechtecke, key=lambda r: r.flaeche())

a = Rechteck(2, 3)
b = Rechteck(4, 1)
c = Rechteck(5, 5)
print(groesstes([a, b, c]).flaeche())
print(a.passt_in(c))
print(b.passt_in(a))""")
th('''Schreibe eine Funktion `gruppieren(woerter, schluessel)` mit Typangaben: Sie bildet ein Dictionary, in dem die Wörter nach dem Ergebnis der Funktion `schluessel` gruppiert sind
(Schlüssel `str`, Werte Listen von Wörtern). Gruppiere `woerter` nach dem Anfangsbuchstaben und gib das Ergebnis aus.''',
   given="woerter = ['Apfel', 'Birne', 'Ananas', 'Banane', 'Kiwi']",
   body="""from collections.abc import Callable

def gruppieren(woerter: list[str], schluessel: Callable[[str], str]) -> dict[str, list[str]]:
    gruppen = {}
    for w in woerter:
        k = schluessel(w)
        if k not in gruppen:
            gruppen[k] = []
        gruppen[k].append(w)
    return gruppen

print(gruppieren(woerter, lambda w: w[0]))""")
predict("""def teilen(a: int, b: int) -> int | None:
    if b == 0:
        return None
    return a // b

ergebnisse: list[int | None] = []
for b in [3, 0, 2]:
    ergebnisse.append(teilen(7, b))
print(ergebnisse)
print(teilen.__annotations__['return'])""")

generate('typangaben', 'Typangaben (Type Hints)', INTRO)
