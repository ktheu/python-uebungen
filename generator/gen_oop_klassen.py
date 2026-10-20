# Erzeugt ../content/oop_klassen.ipynb (siehe nbgen.py). Erstes Notebook der OOP-Reihe:
# oop_klassen, oop_kapselung, oop_beziehungen, oop_vererbung.
#
# Konventionen wie im Unterricht: private Attribute __name, geschützte _name (ab oop_kapselung),
# Zugriffsmethoden get_x()/set_x(), UML mit Sichtbarkeit und Typen, Konstruktor mit Klassennamen, void ohne Rückgabe.
# In diesem Notebook sind alle Attribute noch öffentlich (+).
# Nie die Standardausgabe eines Objekts (<__main__.X object at 0x...>) in erwarteten Ausgaben: Die Adresse ändert sich.
from nbgen import sec, expl, task, predict, generate
from umlnb import uml_bild


def t(text, given='', body='', kind='normal', anhaenge=None):
    """Aufgabe, deren Lösung aus dem vorgegebenen Code plus body besteht."""
    task(text, given=given, solution=(given + '\n' + body) if given else body, kind=kind, anhaenge=anhaenge)


def uml(name, attribute, methoden):
    """Markdown mit Klassendiagramm und die Anhänge dazu."""
    datei = name.lower() + '.png'
    return f'\n\n![Klassendiagramm {name}](attachment:{datei})\n\n', {datei: uml_bild({name: (attribute, methoden)})}


def tu(text, name, attribute, methoden, given='', body='', kind='normal'):
    """Aufgabe mit Klassendiagramm unter dem Text."""
    md, anh = uml(name, attribute, methoden)
    t(text + md, given, body, kind, anhaenge=anh)


INTRO = '''In der **objektorientierten Programmierung** (OOP) beschreibt man Dinge aus der wirklichen Welt (ein Konto, einen Hund,
einen Würfel) als **Objekte**. Jedes Objekt hat **Attribute** (was es hat, z. B. einen Namen) und **Methoden** (was es kann,
z. B. bellen). Den Bauplan für Objekte nennt man **Klasse**.

Dieses Notebook ist das erste einer Reihe:

1. **Klassen und Objekte** (dieses Notebook)
2. Datenkapselung: private Attribute, Zugriffsmethoden, Klassenattribute
3. Beziehungen zwischen Klassen (Assoziation)
4. Vererbung

Klassen werden mit **UML-Klassendiagrammen** beschrieben. Du lernst sie hier zu lesen und in Python umzusetzen.

Du solltest Funktionen, Listen, Dictionaries und `lambda` schon kennen.

Jeder Abschnitt beginnt mit kurzen Erklärungen und Beispielen. Führe die Beispiele aus und probiere sie ruhig ein wenig aus.
Danach folgen viele kleine Übungen. Wenn etwas vorgegeben ist, steht es schon in der Codezelle.'''

# ---------------------------------------------------------------- 1
sec('Klassen und Objekte')
expl('''#### Klasse und Objekt

Eine **Klasse** ist ein Bauplan. Nach diesem Bauplan kann man beliebig viele **Objekte** erzeugen.
Ein Objekt nennt man auch eine **Instanz** der Klasse.

- `class Hund:` beginnt eine Klasse. Klassennamen schreibt man mit großem Anfangsbuchstaben.
- `pass` steht für einen leeren Klassenkörper.
- `Hund()` erzeugt ein neues Objekt der Klasse `Hund`. Mit `bello = Hund()` merkt man es sich in einer Variablen.

Gibt man ein Objekt mit `print()` aus, sieht man nur die Klasse und eine Speicheradresse. Wie man das ändert, lernst du später.''',
     """class Hund:
    pass

bello = Hund()
luna = Hund()
print(bello)
print(type(bello).__name__)""")
expl('''#### Attribute

Ein Objekt kann **Attribute** haben: Variablen, die zum Objekt gehören. Man schreibt sie mit einem Punkt:
`bello.name = 'Bello'` legt das Attribut `name` an, `print(bello.name)` liest es.

Jedes Objekt hat **eigene** Attribute: Ändert man `bello.name`, bleibt `luna.name` unverändert.''',
     """class Hund:
    pass

bello = Hund()
bello.name = 'Bello'
bello.alter = 3
luna = Hund()
luna.name = 'Luna'
luna.alter = 5
print(bello.name, bello.alter)
print(luna.name, luna.alter)
bello.alter += 1
print(bello.alter, luna.alter)""")
expl('''#### `isinstance()`

`isinstance(objekt, Klasse)` prüft, ob ein Objekt eine Instanz der Klasse ist.''',
     """class Hund:
    pass

class Katze:
    pass

bello = Hund()
print(isinstance(bello, Hund))
print(isinstance(bello, Katze))""")

t('Lege eine leere Klasse `Auto` an. Erzeuge ein Objekt `a`, gib ihm die Attribute `marke` (`\'VW\'`) und `ps` (`110`) und gib beide aus.',
  body="""class Auto:
    pass

a = Auto()
a.marke = 'VW'
a.ps = 110
print(a.marke, a.ps)""")
t('Erzeuge zwei Objekte der Klasse `Stadt` mit den Attributen `name` und `einwohner`: Tübingen mit 91877 und Ulm mit 128928 Einwohnern. Gib aus, welche Stadt mehr Einwohner hat.',
  "class Stadt:\n    pass",
  """s1 = Stadt()
s1.name = 'Tübingen'
s1.einwohner = 91877
s2 = Stadt()
s2.name = 'Ulm'
s2.einwohner = 128928
if s1.einwohner > s2.einwohner:
    print(s1.name)
else:
    print(s2.name)""")
t('Erhöhe das Attribut `punkte` des Objekts `spieler` dreimal hintereinander um 10 und gib es danach aus.',
  "class Spieler:\n    pass\n\nspieler = Spieler()\nspieler.name = 'Mia'\nspieler.punkte = 5",
  """for i in range(3):
    spieler.punkte += 10
print(spieler.punkte)""")
t('Prüfe mit `isinstance()`, ob `x` ein `Buch` ist und ob `x` ein `Film` ist. Gib beide Ergebnisse aus.',
  "class Buch:\n    pass\n\nclass Film:\n    pass\n\nx = Film()",
  """print(isinstance(x, Buch))
print(isinstance(x, Film))""")
t('Gib mit `type(...).__name__` aus, von welcher Klasse die Objekte in `dinge` sind, jeweils in einer eigenen Zeile.',
  "class Apfel:\n    pass\n\nclass Birne:\n    pass\n\ndinge = [Apfel(), Birne(), Apfel()]",
  """for d in dinge:
    print(type(d).__name__)""")
predict("""class Box:
    pass

a = Box()
b = Box()
a.inhalt = 'Ball'
b.inhalt = 'Buch'
a.inhalt = b.inhalt
b.inhalt = 'Stift'
print(a.inhalt, b.inhalt)""")
predict("""class Box:
    pass

a = Box()
a.inhalt = 'Ball'
b = Box()
print(b.inhalt)""", error=AttributeError)

# ---------------------------------------------------------------- 2
sec('Der Konstruktor __init__')
expl('''#### Attribute im Konstruktor anlegen

Attribute einzeln von außen anzulegen ist umständlich und fehleranfällig. Besser legt die Klasse sie selbst an, und zwar im
**Konstruktor**: einer besonderen Methode mit dem Namen `__init__` (zwei Unterstriche vorne und hinten).

- Der Konstruktor wird **automatisch** aufgerufen, wenn ein Objekt erzeugt wird.
- Sein erster Parameter heißt `self`: Das ist das **neue Objekt selbst**. Mit `self.name = name` bekommt das Objekt das Attribut `name`.
- Die anderen Parameter gibt man beim Erzeugen an: `Hund('Bello', 3)`. Für `self` gibt man nichts an.''',
     """class Hund:
    def __init__(self, name, alter):
        self.name = name
        self.alter = alter

bello = Hund('Bello', 3)
luna = Hund('Luna', 5)
print(bello.name, bello.alter)
print(luna.name, luna.alter)""")
expl('''#### Startwerte und berechnete Attribute

Nicht jedes Attribut muss ein Parameter sein. Der Konstruktor kann Attributen auch einen festen Startwert geben
oder sie aus den Parametern berechnen. Parameter können Standardwerte haben, wie bei Funktionen.''',
     """class Konto:
    def __init__(self, inhaber, kontostand=0):
        self.inhaber = inhaber
        self.kontostand = kontostand
        self.buchungen = []

class Rechteck:
    def __init__(self, breite, hoehe):
        self.breite = breite
        self.hoehe = hoehe
        self.flaeche = breite * hoehe

k = Konto('Ali')
print(k.inhaber, k.kontostand, k.buchungen)
print(Konto('Bea', 50).kontostand)
print(Rechteck(3, 4).flaeche)""")
md, anh = uml('Hund', ['+ name: str', '+ alter: int'], ['+ Hund(name: str, alter: int)'])
expl('''#### UML-Klassendiagramm

Ein **Klassendiagramm** beschreibt eine Klasse in einem Kasten mit drei Teilen:

1. oben der **Name** der Klasse,
2. in der Mitte die **Attribute** mit ihrem Typ, z. B. `name: str`,
3. unten die **Methoden** mit ihren Parametern. Der **Konstruktor** steht dort mit dem Namen der Klasse: `Hund(name: str, alter: int)`.

Das `+` vor einem Eintrag bedeutet **öffentlich**: Man darf von außen darauf zugreifen. (Was `-` bedeutet, kommt im nächsten Notebook.)
Die Typen schreibt man in Python **nicht** mit, sie sagen nur, welche Art von Werten gemeint ist.
Zur Klasse im Diagramm passt der Code im Beispiel.''' + md,
     """class Hund:
    def __init__(self, name, alter):
        self.name = name
        self.alter = alter""", anhaenge=anh)

t('Schreibe eine Klasse `Buch` mit einem Konstruktor, der die Attribute `titel`, `autor` und `seiten` anlegt. Erzeuge das Buch „Momo“ von Michael Ende mit 304 Seiten und gib alle drei Attribute aus.',
  body="""class Buch:
    def __init__(self, titel, autor, seiten):
        self.titel = titel
        self.autor = autor
        self.seiten = seiten

b = Buch('Momo', 'Michael Ende', 304)
print(b.titel, b.autor, b.seiten)""")
tu('Setze die Klasse aus dem Diagramm in Python um. Erzeuge den Schüler Ali, 16 Jahre, Klasse `10b`, und gib aus: `Ali (16) aus der 10b`.',
   'Schueler', ['+ name: str', '+ alter: int', '+ klasse: str'], ['+ Schueler(name: str, alter: int, klasse: str)'],
   body="""class Schueler:
    def __init__(self, name, alter, klasse):
        self.name = name
        self.alter = alter
        self.klasse = klasse

s = Schueler('Ali', 16, '10b')
print(f'{s.name} ({s.alter}) aus der {s.klasse}')""")
tu('''Setze die Klasse aus dem Diagramm um. `punkte` ist kein Parameter, sondern beginnt immer bei 0, `leben` immer bei 3.
Erzeuge den Spieler `Luna` und gib Name, Punkte und Leben aus.''',
   'Spieler', ['+ name: str', '+ punkte: int', '+ leben: int'], ['+ Spieler(name: str)'],
   body="""class Spieler:
    def __init__(self, name):
        self.name = name
        self.punkte = 0
        self.leben = 3

s = Spieler('Luna')
print(s.name, s.punkte, s.leben)""")
t('''Schreibe eine Klasse `Rechteck`, deren Konstruktor `breite` und `hoehe` speichert und daraus die Attribute `flaeche`
und `umfang` berechnet. Gib Fläche und Umfang eines Rechtecks mit Breite 5 und Höhe 3 aus.''',
  body="""class Rechteck:
    def __init__(self, breite, hoehe):
        self.breite = breite
        self.hoehe = hoehe
        self.flaeche = breite * hoehe
        self.umfang = 2 * (breite + hoehe)

r = Rechteck(5, 3)
print(r.flaeche, r.umfang)""")
t('''Schreibe eine Klasse `Artikel` mit den Attributen `name`, `preis` und `anzahl`. `anzahl` soll den Standardwert 1 haben.
Erzeuge eine Packung Milch für 1.19 (ohne Anzahl) und 6 Brötchen für 0.45 und gib jeweils `preis * anzahl` mit zwei Nachkommastellen aus.''',
  body="""class Artikel:
    def __init__(self, name, preis, anzahl=1):
        self.name = name
        self.preis = preis
        self.anzahl = anzahl

milch = Artikel('Milch', 1.19)
broetchen = Artikel('Brötchen', 0.45, 6)
print(f'{milch.preis * milch.anzahl:.2f}')
print(f'{broetchen.preis * broetchen.anzahl:.2f}')""")
tu('Setze die Klasse um. `email` hat den Standardwert `None`. Erzeuge zwei Kontakte, einen mit und einen ohne E-Mail-Adresse, und gib bei beiden Name und E-Mail aus.',
   'Kontakt', ['+ name: str', '+ telefon: str', '+ email: str'], ['+ Kontakt(name: str, telefon: str, email: str = None)'],
   body="""class Kontakt:
    def __init__(self, name, telefon, email=None):
        self.name = name
        self.telefon = telefon
        self.email = email

k1 = Kontakt('Bea', '0711 123', 'bea@example.org')
k2 = Kontakt('Cem', '0151 999')
print(k1.name, k1.email)
print(k2.name, k2.email)""")
t('''Schreibe eine Klasse `Termin` mit den Attributen `tag`, `stunde` und `fach`. Der Konstruktor soll zusätzlich das Attribut
`nachmittag` anlegen: `True`, wenn `stunde` 13 oder größer ist, sonst `False`. Gib für die Termine in `daten` jeweils Fach und `nachmittag` aus.''',
  "daten = [('Mo', 8, 'Mathe'), ('Mo', 14, 'Sport'), ('Di', 13, 'Chor')]",
  """class Termin:
    def __init__(self, tag, stunde, fach):
        self.tag = tag
        self.stunde = stunde
        self.fach = fach
        self.nachmittag = stunde >= 13

for tag, stunde, fach in daten:
    termin = Termin(tag, stunde, fach)
    print(termin.fach, termin.nachmittag)""")
t('''Schreibe eine Klasse `Klasse` (für eine Schulklasse) mit den Attributen `name` und `schueler`. `schueler` beginnt als leere Liste.
Erzeuge die Klasse `9a`, hänge `Ali` und `Bea` an die Liste an und gib den Namen und die Anzahl der Schüler aus.''',
  body="""class Klasse:
    def __init__(self, name):
        self.name = name
        self.schueler = []

k = Klasse('9a')
k.schueler.append('Ali')
k.schueler.append('Bea')
print(k.name, len(k.schueler))""")
t('''Schreibe eine Klasse `Uhrzeit` mit den Attributen `stunde` und `minute`. Der Konstruktor bekommt eine Zeichenkette wie
`'14:05'` und zerlegt sie mit `split(':')`. Gib für `Uhrzeit('14:05')` die Stunde und die Minute als Zahlen aus und danach
die Minuten seit Mitternacht.''',
  body="""class Uhrzeit:
    def __init__(self, text):
        h, m = text.split(':')
        self.stunde = int(h)
        self.minute = int(m)

u = Uhrzeit('14:05')
print(u.stunde, u.minute)
print(u.stunde * 60 + u.minute)""")
predict("""class Punkt:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.summe = x + y

p = Punkt(2, 3)
p.x = 10
print(p.x, p.y, p.summe)""")
predict("""class Punkt:
    def __init__(self, x, y=0):
        self.x = x
        self.y = y

a = Punkt(4)
b = Punkt(y=1, x=2)
print(a.x, a.y, b.x, b.y)""")
predict("""class Punkt:
    def __init__(self, x, y):
        self.x = x
        self.y = y

p = Punkt(1)""", error=TypeError)

# ---------------------------------------------------------------- 3
sec('Methoden')
expl('''#### Methoden definieren und aufrufen

Eine **Methode** ist eine Funktion, die in der Klasse steht und zu einem Objekt gehört.

- Ihr erster Parameter ist immer `self`. Darüber kommt sie an die Attribute des Objekts: `self.name`.
- Aufgerufen wird sie mit einem Punkt am Objekt: `bello.bellen()`. Für `self` gibt man wieder nichts an.

Im Klassendiagramm steht hinter der Methode ihr **Rückgabetyp**. `void` bedeutet: Die Methode gibt nichts zurück.''',
     """class Hund:
    def __init__(self, name):
        self.name = name

    def bellen(self):
        print(self.name, 'sagt: Wuff!')

bello = Hund('Bello')
luna = Hund('Luna')
bello.bellen()
luna.bellen()""")
expl('''#### Methoden mit Parametern und Rückgabewert

Methoden können weitere Parameter haben und mit `return` einen Wert zurückgeben, wie Funktionen.
Methoden können auch **Attribute ändern**, z. B. `self.kontostand += betrag`.''',
     """class Konto:
    def __init__(self, inhaber):
        self.inhaber = inhaber
        self.kontostand = 0

    def einzahlen(self, betrag):
        self.kontostand += betrag

    def ist_im_plus(self):
        return self.kontostand > 0

k = Konto('Ali')
print(k.ist_im_plus())
k.einzahlen(50)
k.einzahlen(25)
print(k.kontostand, k.ist_im_plus())""")
md, anh = uml('Konto', ['+ inhaber: str', '+ kontostand: float'],
              ['+ Konto(inhaber: str)', '+ einzahlen(betrag: float): void', '+ ist_im_plus(): bool'])
expl('''Das Klassendiagramm zur Klasse `Konto` aus dem Beispiel darüber. Hinter `einzahlen` steht `void`, weil die Methode nichts zurückgibt.''' + md,
     None, anhaenge=anh)
expl('''#### Methoden rufen Methoden auf

Innerhalb der Klasse ruft man eine andere Methode desselben Objekts mit `self.methode()` auf.

Bekommt eine Methode ein **zweites Objekt derselben Klasse** als Parameter, nennt man es meist `other`: `self` ist das eigene Objekt,
`other` das andere. Mit `other.flaeche()` ruft man dessen Methode auf.''',
     """class Rechteck:
    def __init__(self, breite, hoehe):
        self.breite = breite
        self.hoehe = hoehe

    def flaeche(self):
        return self.breite * self.hoehe

    def ist_groesser_als(self, other):
        return self.flaeche() > other.flaeche()

a = Rechteck(3, 4)
b = Rechteck(2, 5)
print(a.flaeche(), b.flaeche())
print(a.ist_groesser_als(b))""")

t('Ergänze die Klasse `Katze` um eine Methode `miauen()`, die `Minka sagt: Miau!` (mit dem Namen der Katze) ausgibt. Rufe sie für `minka` und für `felix` auf.',
  "class Katze:\n    def __init__(self, name):\n        self.name = name",
  """
    def miauen(self):
        print(self.name, 'sagt: Miau!')

minka = Katze('Minka')
felix = Katze('Felix')
minka.miauen()
felix.miauen()""")
t('Ergänze die Klasse `Kreis` um die Methoden `flaeche()` und `umfang()` (mit `pi = 3.14`, Ergebnis zurückgeben). Gib beide für einen Kreis mit Radius 10 mit zwei Nachkommastellen aus.',
  "class Kreis:\n    def __init__(self, radius):\n        self.radius = radius",
  """
    def flaeche(self):
        return 3.14 * self.radius * self.radius

    def umfang(self):
        return 2 * 3.14 * self.radius

k = Kreis(10)
print(f'{k.flaeche():.2f}')
print(f'{k.umfang():.2f}')""")
tu('Setze die Klasse aus dem Diagramm um. `geburtstag()` erhöht das Alter um 1. Erzeuge Ida, 12 Jahre, feiere zweimal Geburtstag und gib danach ihr Alter aus.',
   'Person', ['+ name: str', '+ alter: int'], ['+ Person(name: str, alter: int)', '+ geburtstag(): void'],
   body="""class Person:
    def __init__(self, name, alter):
        self.name = name
        self.alter = alter

    def geburtstag(self):
        self.alter += 1

ida = Person('Ida', 12)
ida.geburtstag()
ida.geburtstag()
print(ida.alter)""")
tu('''Setze die Klasse um. `zaehlen()` erhöht `stand` um 1, `zuruecksetzen()` setzt ihn auf 0, `get_stand()` gibt ihn zurück.
Klicke 5-mal, gib den Stand aus, setze zurück, klicke 2-mal und gib den Stand wieder aus.''',
   'Klickzaehler', ['+ stand: int'], ['+ Klickzaehler()', '+ zaehlen(): void', '+ zuruecksetzen(): void', '+ get_stand(): int'],
   body="""class Klickzaehler:
    def __init__(self):
        self.stand = 0

    def zaehlen(self):
        self.stand += 1

    def zuruecksetzen(self):
        self.stand = 0

    def get_stand(self):
        return self.stand

z = Klickzaehler()
for i in range(5):
    z.zaehlen()
print(z.get_stand())
z.zuruecksetzen()
z.zaehlen()
z.zaehlen()
print(z.get_stand())""")
t('''Ergänze die Klasse `Konto` um eine Methode `abheben(betrag)`. Ist genug Geld da, wird der Betrag abgezogen und `True`
zurückgegeben, sonst bleibt der Kontostand gleich und die Methode gibt `False` zurück. Hebe nacheinander 30, 50 und 20 ab und gib jeweils
das Ergebnis und den Kontostand aus.''',
  "class Konto:\n    def __init__(self, inhaber, kontostand):\n        self.inhaber = inhaber\n        self.kontostand = kontostand",
  """
    def abheben(self, betrag):
        if betrag > self.kontostand:
            return False
        self.kontostand -= betrag
        return True

k = Konto('Ali', 60)
for betrag in [30, 50, 20]:
    print(k.abheben(betrag), k.kontostand)""")
tu('''Setze die Klasse um. `hinzufuegen(note)` hängt eine Note an die Liste `noten` an, `durchschnitt()` gibt den Durchschnitt zurück
(bei leerer Liste 0). Füge die Noten 2, 3, 1 und 2 hinzu und gib den Durchschnitt aus.''',
   'Zeugnis', ['+ fach: str', '+ noten: list'], ['+ Zeugnis(fach: str)', '+ hinzufuegen(note: int): void', '+ durchschnitt(): float'],
   body="""class Zeugnis:
    def __init__(self, fach):
        self.fach = fach
        self.noten = []

    def hinzufuegen(self, note):
        self.noten.append(note)

    def durchschnitt(self):
        if len(self.noten) == 0:
            return 0
        return sum(self.noten) / len(self.noten)

z = Zeugnis('Mathe')
for n in [2, 3, 1, 2]:
    z.hinzufuegen(n)
print(z.durchschnitt())""")
t('''Schreibe eine Klasse `Lampe` mit dem Attribut `an` (Start: `False`) und den Methoden `schalten()` (wechselt zwischen an und aus)
und `zustand()` (gibt `'an'` oder `'aus'` zurück). Schalte die Lampe viermal und gib nach jedem Schalten den Zustand aus.''',
  body="""class Lampe:
    def __init__(self):
        self.an = False

    def schalten(self):
        self.an = not self.an

    def zustand(self):
        if self.an:
            return 'an'
        return 'aus'

lampe = Lampe()
for i in range(4):
    lampe.schalten()
    print(lampe.zustand())""")
t('''Ergänze die Klasse `Rechteck` um die Methoden `flaeche()`, `ist_quadrat()` (gibt `True` oder `False` zurück) und
`skalieren(faktor)` (multipliziert Breite und Höhe mit dem Faktor). Teste: Gib für ein 3×3-Rechteck `ist_quadrat()` aus,
skaliere es mit 2 und gib die Fläche aus.''',
  "class Rechteck:\n    def __init__(self, breite, hoehe):\n        self.breite = breite\n        self.hoehe = hoehe",
  """
    def flaeche(self):
        return self.breite * self.hoehe

    def ist_quadrat(self):
        return self.breite == self.hoehe

    def skalieren(self, faktor):
        self.breite *= faktor
        self.hoehe *= faktor

r = Rechteck(3, 3)
print(r.ist_quadrat())
r.skalieren(2)
print(r.flaeche())""")
tu('''Setze die Klasse um. `tanken(liter)` erhöht den Tankinhalt, aber höchstens bis `tankgroesse`. `fahren(km)` verbraucht
`km * verbrauch / 100` Liter; reicht der Tank nicht, wird nicht gefahren und die Methode gibt `False` zurück, sonst `True`.
Teste mit Tankgröße 50 und Verbrauch 6: tanke 40 Liter, fahre 500 km, fahre 300 km, tanke 100 Liter. Gib nach jedem Schritt den Tankinhalt aus
(bei `fahren` vorher das Ergebnis).''',
   'Auto', ['+ tankgroesse: float', '+ verbrauch: float', '+ tank: float'],
   ['+ Auto(tankgroesse: float, verbrauch: float)', '+ tanken(liter: float): void', '+ fahren(km: float): bool'],
   body="""class Auto:
    def __init__(self, tankgroesse, verbrauch):
        self.tankgroesse = tankgroesse
        self.verbrauch = verbrauch
        self.tank = 0

    def tanken(self, liter):
        self.tank = min(self.tank + liter, self.tankgroesse)

    def fahren(self, km):
        benoetigt = km * self.verbrauch / 100
        if benoetigt > self.tank:
            return False
        self.tank -= benoetigt
        return True

a = Auto(50, 6)
a.tanken(40)
print(a.tank)
print(a.fahren(500), a.tank)
print(a.fahren(300), a.tank)
a.tanken(100)
print(a.tank)""")
t('''Ergänze die Klasse `Punkt` um eine Methode `abstand(other)`, die den Abstand zu einem anderen Punkt zurückgibt
(Wurzel mit `** 0.5`), und eine Methode `verschieben(dx, dy)`. Gib den Abstand von `p` zu `q` aus, verschiebe `p` um (3, 4)
und gib den Abstand erneut aus.''',
  "class Punkt:\n    def __init__(self, x, y):\n        self.x = x\n        self.y = y",
  """
    def abstand(self, other):
        return ((self.x - other.x) ** 2 + (self.y - other.y) ** 2) ** 0.5

    def verschieben(self, dx, dy):
        self.x += dx
        self.y += dy

p = Punkt(0, 0)
q = Punkt(6, 8)
print(p.abstand(q))
p.verschieben(3, 4)
print(p.abstand(q))""")
t('''Ergänze die Klasse `Wort` um die Methoden `ist_palindrom()` (Groß- und Kleinschreibung egal) und `vokale()` (Anzahl der Vokale
a, e, i, o, u). `ist_palindrom()` soll dabei `self.normal()` verwenden. Gib beide Ergebnisse für `Anna` und für `Python` aus.''',
  "class Wort:\n    def __init__(self, text):\n        self.text = text\n\n    def normal(self):\n        return self.text.lower()",
  """
    def ist_palindrom(self):
        return self.normal() == self.normal()[::-1]

    def vokale(self):
        anzahl = 0
        for b in self.normal():
            if b in 'aeiou':
                anzahl += 1
        return anzahl

for w in [Wort('Anna'), Wort('Python')]:
    print(w.text, w.ist_palindrom(), w.vokale())""")
predict("""class Zaehler:
    def __init__(self, start):
        self.wert = start

    def plus(self, n):
        self.wert += n
        return self.wert

z = Zaehler(10)
print(z.plus(5))
z.plus(1)
print(z.wert)""")
predict("""class Konto:
    def __init__(self):
        self.stand = 0

    def einzahlen(self, betrag):
        self.stand += betrag

k = Konto()
print(k.einzahlen(10))
print(k.stand)""")
# ---------------------------------------------------------------- 4
sec('Objekte ausgeben mit __str__')
expl('''#### Die Methode `__str__`

`print(objekt)` zeigt normalerweise nur `<__main__.Hund object at 0x...>`. Schreibt man in die Klasse eine Methode `__str__(self)`,
die eine **Zeichenkette zurückgibt**, verwendet `print()` diese Zeichenkette. Auch `str(objekt)` und f-Strings benutzen `__str__`.

`__str__` gibt den Text mit `return` zurück. Sie gibt nichts mit `print()` aus.''',
     """class Hund:
    def __init__(self, name, alter):
        self.name = name
        self.alter = alter

    def __str__(self):
        return f'{self.name} ({self.alter} Jahre)'

bello = Hund('Bello', 3)
print(bello)
print('Mein Hund: ' + str(bello))
print(f'Das ist {bello}.')""")

t('Ergänze die Klasse `Buch` um eine Methode `__str__`, sodass `print(b)` den Text `Momo von Michael Ende` ausgibt.',
  "class Buch:\n    def __init__(self, titel, autor):\n        self.titel = titel\n        self.autor = autor",
  """
    def __str__(self):
        return f'{self.titel} von {self.autor}'

b = Buch('Momo', 'Michael Ende')
print(b)""")
t('Ergänze die Klasse `Bruch` um `__str__`, sodass ein Bruch als `3/4` ausgegeben wird. Gib die Brüche in `brueche` aus, jeweils in einer Zeile.',
  "class Bruch:\n    def __init__(self, zaehler, nenner):\n        self.zaehler = zaehler\n        self.nenner = nenner",
  """
    def __str__(self):
        return f'{self.zaehler}/{self.nenner}'

brueche = [Bruch(3, 4), Bruch(1, 2), Bruch(5, 8)]
for b in brueche:
    print(b)""")
t('''Ergänze die Klasse `Uhrzeit` um `__str__`: Stunde und Minute immer zweistellig, also `08:05` (Formatangabe `:02d`).
Gib `Uhrzeit(8, 5)` und `Uhrzeit(14, 30)` aus.''',
  "class Uhrzeit:\n    def __init__(self, stunde, minute):\n        self.stunde = stunde\n        self.minute = minute",
  """
    def __str__(self):
        return f'{self.stunde:02d}:{self.minute:02d}'

print(Uhrzeit(8, 5))
print(Uhrzeit(14, 30))""")
t('''Ergänze die Klasse `Konto` um `__str__` in der Form `Konto von Ali: 125.50 Euro` (zwei Nachkommastellen).
Gib das Konto aus, zahle 20 ein und gib es wieder aus.''',
  "class Konto:\n    def __init__(self, inhaber, kontostand):\n        self.inhaber = inhaber\n        self.kontostand = kontostand\n\n"
  "    def einzahlen(self, betrag):\n        self.kontostand += betrag",
  """
    def __str__(self):
        return f'Konto von {self.inhaber}: {self.kontostand:.2f} Euro'

k = Konto('Ali', 125.5)
print(k)
k.einzahlen(20)
print(k)""")
t('''Ergänze die Klasse `Ampel` um `__str__`, die die Farbe in Großbuchstaben zurückgibt, und um eine Methode `weiter()`, die zur nächsten Farbe
schaltet: rot → rotgelb → grün → gelb → rot. Die Reihenfolge steht in der Liste `PHASEN`, das Attribut `nr` ist der Index der aktuellen Phase.
Gib die Ampel aus und schalte dann fünfmal weiter, jeweils mit Ausgabe.''',
  "PHASEN = ['rot', 'rotgelb', 'grün', 'gelb']\n\nclass Ampel:\n    def __init__(self):\n        self.nr = 0",
  """
    def weiter(self):
        self.nr = (self.nr + 1) % len(PHASEN)

    def __str__(self):
        return PHASEN[self.nr].upper()

a = Ampel()
print(a)
for i in range(5):
    a.weiter()
    print(a)""")
t('''Ergänze die Klasse `Rechteck` um `__str__`, die das Rechteck aus `#`-Zeichen „zeichnet“: `hoehe` Zeilen mit je `breite` Zeichen,
getrennt durch `\\n`. Gib `Rechteck(5, 3)` aus.''',
  "class Rechteck:\n    def __init__(self, breite, hoehe):\n        self.breite = breite\n        self.hoehe = hoehe",
  """
    def __str__(self):
        zeilen = []
        for i in range(self.hoehe):
            zeilen.append('#' * self.breite)
        return '\\n'.join(zeilen)

print(Rechteck(5, 3))""")
predict("""class Tier:
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return 'Tier ' + self.name

t = Tier('Igel')
print(t)
print(str(t) + '!')
print(len(str(t)))""")
predict("""class Note:
    def __init__(self, wert):
        self.wert = wert

    def __str__(self):
        print('Note', self.wert)
        return 'fertig'

n = Note(2)
print(n)""")

# ---------------------------------------------------------------- 5
sec('Objekte in Listen und Dictionaries')
expl('''#### Viele Objekte verwalten

Objekte kann man wie andere Werte in Listen und Dictionaries speichern. Mit einer Schleife geht man sie durch und greift auf
ihre Attribute und Methoden zu. Zum Sortieren und für `max()`/`min()` gibt man mit `key=` an, nach welchem Attribut verglichen wird.''',
     """class Schueler:
    def __init__(self, name, note):
        self.name = name
        self.note = note

klasse = [Schueler('Ali', 2), Schueler('Bea', 1), Schueler('Cem', 3)]
for s in klasse:
    print(s.name, s.note)
beste = min(klasse, key=lambda s: s.note)
print('Beste Note:', beste.name)
for s in sorted(klasse, key=lambda s: s.name, reverse=True):
    print(s.name)""")
expl('''#### Objekte nach Namen nachschlagen

In einem Dictionary kann man Objekte unter einem Schlüssel ablegen, z. B. unter ihrem Namen.''',
     """class Schueler:
    def __init__(self, name, note):
        self.name = name
        self.note = note

verzeichnis = {}
for name, note in [('Ali', 2), ('Bea', 1)]:
    verzeichnis[name] = Schueler(name, note)
print(verzeichnis['Bea'].note)""")

PRODUKT = ("class Produkt:\n    def __init__(self, name, preis, bestand):\n        self.name = name\n        self.preis = preis\n        self.bestand = bestand\n\n"
           "lager = [Produkt('Heft', 1.2, 40), Produkt('Stift', 0.8, 0), Produkt('Mappe', 2.5, 12), Produkt('Lineal', 1.5, 5), Produkt('Kleber', 2.1, 0)]")
t('Gib die Namen aller Produkte im `lager` aus, die nicht mehr vorrätig sind (Bestand 0).', PRODUKT,
  """for p in lager:
    if p.bestand == 0:
        print(p.name)""")
t('Gib den Gesamtwert des Lagers aus (Summe von Preis mal Bestand), mit zwei Nachkommastellen.', PRODUKT,
  """summe = 0
for p in lager:
    summe += p.preis * p.bestand
print(f'{summe:.2f}')""")
t('Gib den Namen des teuersten Produkts aus. Verwende `max()` mit `key=`.', PRODUKT,
  "print(max(lager, key=lambda p: p.preis).name)")
t('Gib alle Produkte nach dem Preis sortiert aus (das billigste zuerst), in der Form `Stift: 0.80`.', PRODUKT,
  """for p in sorted(lager, key=lambda p: p.preis):
    print(f'{p.name}: {p.preis:.2f}')""")
t('Erhöhe den Preis jedes Produkts um 10 % und gib danach alle Preise mit zwei Nachkommastellen als Liste von Zeichenketten aus.', PRODUKT,
  """for p in lager:
    p.preis *= 1.1
preise = []
for p in lager:
    preise.append(f'{p.preis:.2f}')
print(preise)""")
t('Lege ein Dictionary an, in dem jedes Produkt unter seinem Namen steht. Gib damit den Bestand der Mappe aus.', PRODUKT,
  """nach_name = {}
for p in lager:
    nach_name[p.name] = p
print(nach_name['Mappe'].bestand)""")
t('''Schreibe eine Funktion `suche(lager, name)`, die das Produkt mit diesem Namen zurückgibt oder `None`, wenn es keins gibt.
Gib für `'Lineal'` den Preis aus und für `'Schere'` das Ergebnis der Suche.''', PRODUKT,
  """def suche(lager, name):
    for p in lager:
        if p.name == name:
            return p
    return None

print(suche(lager, 'Lineal').preis)
print(suche(lager, 'Schere'))""")
t('''Erstelle aus der Liste `daten` eine Liste von `Film`-Objekten (die Klasse musst du schreiben, Attribute `titel`, `jahr`, `minuten`).
Gib die Titel aller Filme aus, die länger als 2 Stunden sind, und danach den ältesten Film.''',
  "daten = [('Titanic', 1997, 194), ('Toy Story', 1995, 81), ('Avatar', 2009, 162), ('Shrek', 2001, 90)]",
  """class Film:
    def __init__(self, titel, jahr, minuten):
        self.titel = titel
        self.jahr = jahr
        self.minuten = minuten

filme = []
for titel, jahr, minuten in daten:
    filme.append(Film(titel, jahr, minuten))
for f in filme:
    if f.minuten > 120:
        print(f.titel)
print(min(filme, key=lambda f: f.jahr).titel)""")
t('''Die Klasse `Wuerfel` ist vorgegeben. Erzeuge eine Liste mit 5 Würfeln, würfle mit jedem einmal und gib die Augenzahlen als Liste
und ihre Summe aus.''',
  "import random\nrandom.seed(3)\n\nclass Wuerfel:\n    def __init__(self):\n        self.augen = 1\n\n    def werfen(self):\n        self.augen = random.randint(1, 6)",
  """wuerfel = []
for i in range(5):
    wuerfel.append(Wuerfel())
augen = []
for w in wuerfel:
    w.werfen()
    augen.append(w.augen)
print(augen)
print(sum(augen))""")
t('''Die Klasse `Schueler` hat `__str__`. Gib die Liste `klasse` mit `print()` aus und dann jedes Element mit `print()` einzeln.
Du wirst sehen: Bei der Liste werden die Objekte **nicht** mit `__str__` ausgegeben. Gib deshalb zum Schluss die Namen mit
`', '.join(...)` aus einer Liste von `str(s)` aus. (Ohne erwartete Ausgabe, weil die Liste Speicheradressen enthält.)''',
  "class Schueler:\n    def __init__(self, name):\n        self.name = name\n\n    def __str__(self):\n        return self.name\n\nklasse = [Schueler('Ali'), Schueler('Bea')]",
  """print(klasse)
for s in klasse:
    print(s)
texte = []
for s in klasse:
    texte.append(str(s))
print(', '.join(texte))""", kind='free')
predict("""class Box:
    def __init__(self, n):
        self.n = n

boxen = [Box(3), Box(1), Box(2)]
boxen.sort(key=lambda b: b.n)
print(boxen[0].n, boxen[-1].n)
summe = 0
for b in boxen:
    b.n *= 2
    summe += b.n
print(summe)""")

# ---------------------------------------------------------------- 6
sec('Referenzen')
expl('''#### Variablen verweisen auf Objekte

Eine Variable enthält nicht das Objekt selbst, sondern einen **Verweis** (eine **Referenz**) darauf.
Nach `b = a` verweisen `a` und `b` auf **dasselbe** Objekt. Ändert man das Objekt über `b`, sieht man die Änderung auch über `a`.

`a is b` prüft, ob zwei Variablen auf dasselbe Objekt verweisen.''',
     """class Konto:
    def __init__(self, stand):
        self.stand = stand

a = Konto(100)
b = a
b.stand = 0
print(a.stand)
print(a is b)
c = Konto(0)
print(a is c)""")
expl('''#### `is` und `==`

Zwei **verschiedene** Objekte mit gleichen Attributen sind für Python zunächst **nicht** gleich: Ohne weitere Angaben bedeutet `==`
bei eigenen Objekten dasselbe wie `is`. Will man Attribute vergleichen, vergleicht man sie einzeln
(oder schreibt eine eigene Methode, z. B. `ist_gleich(other)`).''',
     """class Punkt:
    def __init__(self, x, y):
        self.x = x
        self.y = y

p = Punkt(1, 2)
q = Punkt(1, 2)
print(p == q, p is q)
print(p.x == q.x and p.y == q.y)""")
expl('''#### Zahlen und Zeichenketten verhalten sich anders

Zahlen und Zeichenketten kann man nicht verändern. `x += 1` erzeugt eine **neue** Zahl, auf die `x` dann verweist. Deshalb ändert
sich `y` nach `y = x` nicht mit. Bei Objekten (und Listen), die man über ihre Attribute **verändert**, verweisen dagegen alle
Variablen auf dasselbe veränderte Objekt.''',
     """x = 5
y = x
x += 1
print(x, y)

class Zahl:
    def __init__(self, wert):
        self.wert = wert

a = Zahl(5)
b = a
a.wert += 1
print(a.wert, b.wert)""")
expl('''#### Objekte als Parameter

Übergibt man ein Objekt an eine Funktion oder Methode, bekommt sie einen Verweis auf **dasselbe** Objekt.
Ändert sie seine Attribute, ist die Änderung danach auch außerhalb sichtbar. Eine Zahl als Parameter kann die Funktion dagegen
nicht von außen sichtbar ändern.''',
     """class Spieler:
    def __init__(self, name):
        self.name = name
        self.punkte = 0

def belohnen(spieler, punkte):
    spieler.punkte += punkte

def verdoppeln(zahl):
    zahl = zahl * 2

s = Spieler('Mia')
belohnen(s, 10)
print(s.punkte)
n = 7
verdoppeln(n)
print(n)""")
expl('''#### Eine Kopie anlegen und `None`

Will man ein **unabhängiges** Objekt mit gleichen Werten, erzeugt man ein neues mit dem Konstruktor, z. B. in einer Methode `kopie()`.

`None` bedeutet „kein Objekt“. Eine Variable kann `None` sein, wenn sie (noch) auf kein Objekt verweist. Man prüft das mit `is None`.''',
     """class Punkt:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def kopie(self):
        return Punkt(self.x, self.y)

p = Punkt(1, 2)
q = p.kopie()
q.x = 10
print(p.x, q.x)
leer = None
print(leer is None)""")

t('''Es gibt nur **ein** Konto, auf das `konto_ali` und `konto_familie` verweisen. Zahle über `konto_familie` 50 ein und gib den Stand über `konto_ali` aus.
Gib danach aus, ob beide Variablen auf dasselbe Objekt verweisen.''',
  "class Konto:\n    def __init__(self, stand):\n        self.stand = stand\n\nkonto_ali = Konto(100)\nkonto_familie = konto_ali",
  """konto_familie.stand += 50
print(konto_ali.stand)
print(konto_ali is konto_familie)""")
t('Gib aus, welche der Variablen `a`, `b`, `c` auf dasselbe Objekt verweisen: `a is b`, `a is c` und `b is c`, und danach `a == c`.',
  "class Punkt:\n    def __init__(self, x, y):\n        self.x = x\n        self.y = y\n\na = Punkt(1, 1)\nb = Punkt(1, 1)\nc = a",
  """print(a is b, a is c, b is c)
print(a == c)""")
t('''Ergänze die Klasse `Punkt` um eine Methode `ist_gleich(other)`, die `True` zurückgibt, wenn beide Koordinaten übereinstimmen.
Vergleiche `p` mit `q` und `p` mit `r`, jeweils mit `==` und mit `ist_gleich()`.''',
  "class Punkt:\n    def __init__(self, x, y):\n        self.x = x\n        self.y = y",
  """
    def ist_gleich(self, other):
        return self.x == other.x and self.y == other.y

p = Punkt(2, 3)
q = Punkt(2, 3)
r = Punkt(3, 2)
print(p == q, p.ist_gleich(q))
print(p == r, p.ist_gleich(r))""")
t('''Schreibe eine Funktion `alle_belohnen(spieler_liste, punkte)`, die jedem Spieler der Liste `punkte` gutschreibt. Sie gibt nichts zurück.
Rufe sie zweimal mit 5 Punkten auf und gib danach die Punkte aller Spieler aus.''',
  "class Spieler:\n    def __init__(self, name):\n        self.name = name\n        self.punkte = 0\n\nteam = [Spieler('Ali'), Spieler('Bea'), Spieler('Cem')]",
  """def alle_belohnen(spieler_liste, punkte):
    for s in spieler_liste:
        s.punkte += punkte

alle_belohnen(team, 5)
alle_belohnen(team, 5)
for s in team:
    print(s.name, s.punkte)""")
t('''Ergänze die Klasse `Rezept` um eine Methode `kopie()`, die ein neues Rezept mit gleichem Namen und einer **neuen** Liste mit den gleichen
Zutaten zurückgibt (`list(self.zutaten)`). Erstelle eine Kopie, hänge an die Zutaten der Kopie `'Zimt'` an und gib die Zutaten beider Rezepte aus.''',
  "class Rezept:\n    def __init__(self, name, zutaten):\n        self.name = name\n        self.zutaten = zutaten",
  """
    def kopie(self):
        return Rezept(self.name, list(self.zutaten))

original = Rezept('Pfannkuchen', ['Mehl', 'Milch', 'Eier'])
neu = original.kopie()
neu.zutaten.append('Zimt')
print(original.zutaten)
print(neu.zutaten)""")
t('''In `klasse` steht dreimal **dasselbe** Objekt (die Liste wurde mit `*` gebildet). Gib die Namen aus, ändere den Namen von `klasse[0]`
auf `'Bea'` und gib die Namen wieder aus. Erzeuge danach eine Liste mit drei **verschiedenen** Objekten (mit einer Schleife) und wiederhole das.''',
  "class Schueler:\n    def __init__(self, name):\n        self.name = name\n\nklasse = [Schueler('Ali')] * 3",
  """for s in klasse:
    print(s.name, end=' ')
print()
klasse[0].name = 'Bea'
for s in klasse:
    print(s.name, end=' ')
print()
klasse = []
for i in range(3):
    klasse.append(Schueler('Ali'))
klasse[0].name = 'Bea'
for s in klasse:
    print(s.name, end=' ')
print()""")
t('''Ergänze die Klasse `Spieler` um das Attribut `partner` (Start: `None`) und eine Methode `partner_text()`, die `Ali spielt allein`
zurückgibt, wenn `partner` `None` ist, sonst `Ali spielt mit Bea`. Gib den Text für `ali` aus, setze `ali.partner = bea` und gib ihn wieder aus.''',
  "class Spieler:\n    def __init__(self, name):\n        self.name = name",
  """        self.partner = None

    def partner_text(self):
        if self.partner is None:
            return f'{self.name} spielt allein'
        return f'{self.name} spielt mit {self.partner.name}'

ali = Spieler('Ali')
bea = Spieler('Bea')
print(ali.partner_text())
ali.partner = bea
print(ali.partner_text())""")
predict("""class Box:
    def __init__(self, n):
        self.n = n

a = Box(1)
b = a
c = Box(1)
b.n = 2
c.n = 3
print(a.n, b.n, c.n)""")
predict("""class Box:
    def __init__(self, n):
        self.n = n

def aendern(box, zahl):
    box.n += 1
    zahl += 1

b = Box(5)
z = 5
aendern(b, z)
print(b.n, z)""")
predict("""class Box:
    def __init__(self, n):
        self.n = n

boxen = [Box(1), Box(2)]
erste = boxen[0]
boxen[0] = Box(9)
erste.n = 7
print(boxen[0].n, erste.n)""")
predict("""class Box:
    def __init__(self, n):
        self.n = n

a = Box(4)
b = Box(4)
print(a == b, a.n == b.n)
b = a
print(a == b)""")

# ---------------------------------------------------------------- 7
sec('Gemischte Übungen')
tu('''Setze die Klasse aus dem Diagramm um. `zug(feld)` setzt das Zeichen des aktuellen Spielers (`'X'` oder `'O'`) auf das Feld 0 bis 8
und wechselt danach den Spieler. Ist das Feld schon belegt, passiert nichts und die Methode gibt `False` zurück, sonst `True`.
`__str__` gibt das Feld in drei Zeilen aus. Spiele die Züge 4, 0, 4, 8, 2 und gib das Spielfeld aus.''',
   'TicTacToe', ['+ felder: list', '+ spieler: str'],
   ['+ TicTacToe()', '+ zug(feld: int): bool', '+ __str__(): str'],
   body="""class TicTacToe:
    def __init__(self):
        self.felder = ['.'] * 9
        self.spieler = 'X'

    def zug(self, feld):
        if self.felder[feld] != '.':
            return False
        self.felder[feld] = self.spieler
        if self.spieler == 'X':
            self.spieler = 'O'
        else:
            self.spieler = 'X'
        return True

    def __str__(self):
        zeilen = []
        for i in range(0, 9, 3):
            zeilen.append(''.join(self.felder[i:i + 3]))
        return '\\n'.join(zeilen)

spiel = TicTacToe()
for f in [4, 0, 4, 8, 2]:
    spiel.zug(f)
print(spiel)""")
t('''Schreibe eine Klasse `Bruch` mit `zaehler` und `nenner`, `__str__` (Form `3/4`), einer Methode `wert()` (Kommazahl) und einer Methode
`mal(other)`, die einen **neuen** Bruch mit dem Produkt zurückgibt (ohne Kürzen). Gib `Bruch(2, 3).mal(Bruch(3, 4))` und dessen Wert aus.''',
  body="""class Bruch:
    def __init__(self, zaehler, nenner):
        self.zaehler = zaehler
        self.nenner = nenner

    def __str__(self):
        return f'{self.zaehler}/{self.nenner}'

    def wert(self):
        return self.zaehler / self.nenner

    def mal(self, other):
        return Bruch(self.zaehler * other.zaehler, self.nenner * other.nenner)

p = Bruch(2, 3).mal(Bruch(3, 4))
print(p)
print(p.wert())""")
t('''Ergänze die Klasse `Bruch` um eine Methode `kuerzen()`, die Zähler und Nenner durch ihren größten gemeinsamen Teiler teilt.
Den ggT liefert `math.gcd(a, b)`. Kürze die Brüche in `brueche` und gib sie aus.''',
  "import math\n\nclass Bruch:\n    def __init__(self, zaehler, nenner):\n        self.zaehler = zaehler\n        self.nenner = nenner\n\n"
  "    def __str__(self):\n        return f'{self.zaehler}/{self.nenner}'",
  """
    def kuerzen(self):
        g = math.gcd(self.zaehler, self.nenner)
        self.zaehler //= g
        self.nenner //= g

brueche = [Bruch(6, 8), Bruch(10, 25), Bruch(7, 9)]
for b in brueche:
    b.kuerzen()
    print(b)""")
tu('''Setze die Klasse um. `hinzufuegen(name, preis)` hängt ein Tupel an `artikel` an, `summe()` gibt die Summe der Preise zurück,
`teuerster()` den Namen des teuersten Artikels (bei leerem Warenkorb `None`). Teste mit Brot 2.49, Käse 4.99 und Milch 1.19:
gib Summe (zwei Nachkommastellen) und teuersten Artikel aus.''',
   'Warenkorb', ['+ artikel: list'],
   ['+ Warenkorb()', '+ hinzufuegen(name: str, preis: float): void', '+ summe(): float', '+ teuerster(): str'],
   body="""class Warenkorb:
    def __init__(self):
        self.artikel = []

    def hinzufuegen(self, name, preis):
        self.artikel.append((name, preis))

    def summe(self):
        s = 0
        for name, preis in self.artikel:
            s += preis
        return s

    def teuerster(self):
        if len(self.artikel) == 0:
            return None
        return max(self.artikel, key=lambda a: a[1])[0]

w = Warenkorb()
w.hinzufuegen('Brot', 2.49)
w.hinzufuegen('Käse', 4.99)
w.hinzufuegen('Milch', 1.19)
print(f'{w.summe():.2f}')
print(w.teuerster())""")
t('''Schreibe eine Klasse `Stoppuhr` mit dem Attribut `sekunden` (Start 0) und den Methoden `ticken(n)` (zählt `n` Sekunden weiter)
und `__str__` in der Form `mm:ss` (zweistellig). Lass die Uhr 59, dann 1, dann 75 Sekunden ticken und gib sie jedes Mal aus.''',
  body="""class Stoppuhr:
    def __init__(self):
        self.sekunden = 0

    def ticken(self, n):
        self.sekunden += n

    def __str__(self):
        return f'{self.sekunden // 60:02d}:{self.sekunden % 60:02d}'

uhr = Stoppuhr()
for n in [59, 1, 75]:
    uhr.ticken(n)
    print(uhr)""")
tu('''Setze die Klasse um. Eine Figur steht auf einem Feld mit den Koordinaten `x` und `y` (Start 0, 0). `bewegen(richtung)` bewegt sie
um ein Feld: `'N'` erhöht `y`, `'S'` verringert `y`, `'O'` erhöht `x`, `'W'` verringert `x`. `weg()` gibt die Anzahl der bisher
gemachten Schritte zurück. Bewege die Figur mit allen Zeichen aus `'NNOOOSW'` und gib Position und Schrittzahl aus.''',
   'Figur', ['+ x: int', '+ y: int', '+ schritte: int'],
   ['+ Figur()', '+ bewegen(richtung: str): void', '+ weg(): int'],
   body="""class Figur:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.schritte = 0

    def bewegen(self, richtung):
        if richtung == 'N':
            self.y += 1
        elif richtung == 'S':
            self.y -= 1
        elif richtung == 'O':
            self.x += 1
        elif richtung == 'W':
            self.x -= 1
        self.schritte += 1

    def weg(self):
        return self.schritte

f = Figur()
for r in 'NNOOOSW':
    f.bewegen(r)
print(f.x, f.y, f.weg())""")
t('''Die Klasse `Wuerfel` hat die Methode `werfen()`, die eine Augenzahl zurückgibt. Schreibe eine Funktion `pasch_versuche(w1, w2)`, die mit beiden
Würfeln so lange wirft, bis beide dieselbe Zahl zeigen, und die Anzahl der Würfe zurückgibt. Gib das Ergebnis dreimal hintereinander aus.''',
  "import random\nrandom.seed(11)\n\nclass Wuerfel:\n    def werfen(self):\n        return random.randint(1, 6)",
  """def pasch_versuche(w1, w2):
    versuche = 1
    while w1.werfen() != w2.werfen():
        versuche += 1
    return versuche

a = Wuerfel()
b = Wuerfel()
for i in range(3):
    print(pasch_versuche(a, b))""")
t('''Schreibe eine Klasse `Klassenarbeit` mit `fach` und einem Dictionary `noten` (Name → Note, Start leer). Methoden:
`eintragen(name, note)`, `schnitt()` (Durchschnitt, auf zwei Stellen gerundet mit `round()`) und `spiegel()`, die eine Liste mit der Anzahl der Noten
1 bis 6 zurückgibt. Trage die Noten aus `ergebnisse` ein und gib Schnitt und Notenspiegel aus.''',
  "ergebnisse = [('Ali', 2), ('Bea', 1), ('Cem', 3), ('Dana', 2), ('Emil', 4), ('Fiona', 2), ('Gus', 5)]",
  """class Klassenarbeit:
    def __init__(self, fach):
        self.fach = fach
        self.noten = {}

    def eintragen(self, name, note):
        self.noten[name] = note

    def schnitt(self):
        return round(sum(self.noten.values()) / len(self.noten), 2)

    def spiegel(self):
        anzahl = [0] * 6
        for note in self.noten.values():
            anzahl[note - 1] += 1
        return anzahl

ka = Klassenarbeit('Mathe')
for name, note in ergebnisse:
    ka.eintragen(name, note)
print(ka.schnitt())
print(ka.spiegel())""")
predict("""class Konto:
    def __init__(self, stand):
        self.stand = stand

    def ueberweisen(self, ziel, betrag):
        self.stand -= betrag
        ziel.stand += betrag

a = Konto(100)
b = Konto(20)
c = b
a.ueberweisen(b, 30)
c.ueberweisen(a, 5)
print(a.stand, b.stand, c.stand)""")
predict("""class Zaehler:
    def __init__(self):
        self.n = 0

    def tick(self):
        self.n += 1
        return self

z = Zaehler()
z.tick().tick().tick()
print(z.n)""")

generate('oop_klassen', 'OOP 1: Klassen und Objekte', INTRO)
