# Erzeugt ../content/oop_vererbung.ipynb (siehe nbgen.py). Viertes Notebook der OOP-Reihe: Vererbung.
#
# In Oberklassen sind die Attribute geschützt (self._x, im UML #), damit Unterklassen sie benutzen dürfen;
# private Attribute (self.__x) zeigen, dass Unterklassen sie nicht direkt erreichen.
from nbgen import sec, expl, predict, generate
from oophilfe import t, td, ed

INTRO = '''Viele Klassen haben etwas gemeinsam: Hunde und Katzen sind beide Tiere, Girokonten und Sparkonten sind beide Konten.
Mit **Vererbung** schreibt man das Gemeinsame **einmal** in eine Oberklasse, und die Unterklassen übernehmen es und ergänzen nur ihre Besonderheiten.

Dieses Notebook ist das vierte der OOP-Reihe:

1. Klassen und Objekte
2. Datenkapselung
3. Beziehungen zwischen Klassen (Assoziation)
4. **Vererbung** (dieses Notebook)

Jeder Abschnitt beginnt mit kurzen Erklärungen und Beispielen. Führe die Beispiele aus und probiere sie ruhig ein wenig aus.
Manche Beispiele enden absichtlich mit einer Fehlermeldung. Danach folgen viele kleine Übungen.
Wenn etwas vorgegeben ist, steht es schon in der Codezelle.'''

TIER_UML = {'Tier': (['# name: str'], ['+ Tier(name: str)', '+ get_name(): str', '+ fressen(): str']),
            'Hund': ([], ['+ bellen(): str']),
            'Katze': ([], ['+ miauen(): str'])}
TIER_POS = {'Tier': (1.1, 0), 'Hund': (0, 2.3), 'Katze': (2.6, 2.3)}

# ---------------------------------------------------------------- 1
sec('Oberklasse und Unterklasse')
ed('''#### Erben

`class Hund(Tier):` bedeutet: Die Klasse `Hund` **erbt** von der Klasse `Tier`. `Tier` ist die **Oberklasse** (Basisklasse), `Hund` die **Unterklasse**.
Ein Hund hat dann alle Attribute und Methoden eines Tiers, auch den Konstruktor, und kann eigene Methoden dazu haben.

Vererbung passt, wenn man sagen kann: „Ein Hund **ist ein** Tier.“ (Bei einer Assoziation sagt man „hat ein“.)

Im Klassendiagramm zeigt ein Pfeil mit **leerem Dreieck** von der Unterklasse zur Oberklasse. In der Unterklasse stehen nur die **neuen** Attribute und Methoden.
Das `#` vor `name` bedeutet **geschützt**: Auch die Unterklassen dürfen das Attribut benutzen.''',
   """class Tier:
    def __init__(self, name):
        self._name = name

    def get_name(self):
        return self._name

    def fressen(self):
        return self._name + ' frisst.'

class Hund(Tier):
    def bellen(self):
        return self._name + ' bellt: Wuff!'

class Katze(Tier):
    def miauen(self):
        return self._name + ' miaut.'

bello = Hund('Bello')
minka = Katze('Minka')
print(bello.fressen())
print(bello.bellen())
print(minka.fressen())
print(minka.miauen())""",
   'tier.png', TIER_UML, [('Hund', 'Tier', 'vererbung'), ('Katze', 'Tier', 'vererbung')], TIER_POS)
expl('''#### `isinstance()` mit Vererbung

Ein Hund ist auch ein Tier: `isinstance(bello, Tier)` ist `True`. Aber nicht jedes Tier ist ein Hund.
Methoden der Unterklasse hat die Oberklasse nicht: Ein `Tier` kann nicht bellen.''',
     """class Tier:
    def __init__(self, name):
        self._name = name

class Hund(Tier):
    def bellen(self):
        return 'Wuff'

bello = Hund('Bello')
tier = Tier('irgendwas')
print(isinstance(bello, Hund), isinstance(bello, Tier))
print(isinstance(tier, Hund), isinstance(tier, Tier))
print(tier.bellen())""", error=AttributeError)

TIER = ("class Tier:\n    def __init__(self, name):\n        self._name = name\n\n    def get_name(self):\n        return self._name\n\n"
        "    def fressen(self):\n        return self._name + ' frisst.'\n")
t('Schreibe eine Unterklasse `Vogel` von `Tier` mit einer Methode `fliegen()`, die `Hansi fliegt.` zurückgibt. Erzeuge den Vogel Hansi und gib `fressen()` und `fliegen()` aus.',
  TIER, """
class Vogel(Tier):
    def fliegen(self):
        return self._name + ' fliegt.'

hansi = Vogel('Hansi')
print(hansi.fressen())
print(hansi.fliegen())""")
td('Setze die drei Klassen aus dem Diagramm um. `umfang()` gibt bei beiden Unterklassen den Umfang zurück. Gib Name und Umfang eines Quadrats mit Seite 3 und eines Dreiecks mit Seite 5 aus.',
   'vieleck.png',
   {'Vieleck': (['# name: str', '# seite: float'], ['+ Vieleck(name: str, seite: float)', '+ get_name(): str', '+ get_seite(): float']),
    'Quadrat': ([], ['+ umfang(): float']),
    'Dreieck': ([], ['+ umfang(): float'])},
   [('Quadrat', 'Vieleck', 'vererbung'), ('Dreieck', 'Vieleck', 'vererbung')],
   {'Vieleck': (0.8, 0), 'Quadrat': (0, 2.2), 'Dreieck': (2.4, 2.2)},
   body="""class Vieleck:
    def __init__(self, name, seite):
        self._name = name
        self._seite = seite

    def get_name(self):
        return self._name

    def get_seite(self):
        return self._seite

class Quadrat(Vieleck):
    def umfang(self):
        return 4 * self._seite

class Dreieck(Vieleck):
    def umfang(self):
        return 3 * self._seite

for v in [Quadrat('Quadrat', 3), Dreieck('Dreieck', 5)]:
    print(v.get_name(), v.umfang())""")
t('Gib für jedes Objekt in `tiere` aus, ob es ein `Tier`, ein `Hund` und eine `Katze` ist, in der Form `Bello True True False`.',
  TIER + "\nclass Hund(Tier):\n    pass\n\nclass Katze(Tier):\n    pass\n\ntiere = [Hund('Bello'), Katze('Minka'), Tier('Nemo')]",
  """for x in tiere:
    print(x.get_name(), isinstance(x, Tier), isinstance(x, Hund), isinstance(x, Katze))""")
t('''Gib für jedes Tier in `tiere` den passenden Laut aus: Bei Hunden das Ergebnis von `bellen()`, bei Katzen von `miauen()`, sonst `fressen()`.
Prüfe die Klasse mit `isinstance()`.''',
  TIER + "\nclass Hund(Tier):\n    def bellen(self):\n        return self._name + ' bellt.'\n\nclass Katze(Tier):\n    def miauen(self):\n        return self._name + ' miaut.'\n\n"
  "tiere = [Hund('Bello'), Katze('Minka'), Tier('Nemo'), Hund('Rex')]",
  """for x in tiere:
    if isinstance(x, Hund):
        print(x.bellen())
    elif isinstance(x, Katze):
        print(x.miauen())
    else:
        print(x.fressen())""")
t('''Die Klasse `Fahrzeug` hat `fahren(km)`, das den Kilometerstand erhöht. Schreibe die Unterklasse `Fahrrad` mit der Methode `klingeln()` (gibt `Ring ring!` zurück)
und die Unterklasse `Auto` mit `hupen()` (gibt `Tuuut!` zurück). Fahre mit beiden 12 km, lass klingeln und hupen und gib die Kilometerstände aus.''',
  "class Fahrzeug:\n    def __init__(self):\n        self._km = 0\n\n    def fahren(self, km):\n        self._km += km\n\n    def get_km(self):\n        return self._km",
  """
class Fahrrad(Fahrzeug):
    def klingeln(self):
        return 'Ring ring!'

class Auto(Fahrzeug):
    def hupen(self):
        return 'Tuuut!'

f = Fahrrad()
a = Auto()
f.fahren(12)
a.fahren(12)
print(f.klingeln(), a.hupen())
print(f.get_km(), a.get_km())""")
predict("""class A:
    def hallo(self):
        return 'A'

class B(A):
    def tschuess(self):
        return 'B'

b = B()
print(b.hallo(), b.tschuess())
print(isinstance(b, A), isinstance(A(), B))""")
predict("""class A:
    def hallo(self):
        return 'A'

class B(A):
    def tschuess(self):
        return 'B'

a = A()
print(a.tschuess())""", error=AttributeError)

# ---------------------------------------------------------------- 2
sec('Der Konstruktor der Unterklasse')
ed('''#### `super().__init__()`

Hat die Unterklasse **eigene Attribute**, braucht sie einen eigenen Konstruktor. Damit die Attribute der Oberklasse trotzdem angelegt werden,
ruft er zuerst den Konstruktor der Oberklasse auf: `super().__init__(name)`. `super()` steht für „die Oberklasse“.

Im Diagramm steht der Konstruktor der Unterklasse mit allen Parametern, auch denen, die an die Oberklasse weitergegeben werden.''',
   """class Tier:
    def __init__(self, name):
        self._name = name

    def get_name(self):
        return self._name

class Hund(Tier):
    def __init__(self, name, rasse):
        super().__init__(name)
        self._rasse = rasse

    def get_rasse(self):
        return self._rasse

bello = Hund('Bello', 'Dackel')
print(bello.get_name(), bello.get_rasse())""",
   'hund_rasse.png',
   {'Tier': (['# name: str'], ['+ Tier(name: str)', '+ get_name(): str']),
    'Hund': (['# rasse: str'], ['+ Hund(name: str, rasse: str)', '+ get_rasse(): str'])},
   [('Hund', 'Tier', 'vererbung')], {'Tier': (0, 0), 'Hund': (0, 2.0)})
expl('''#### Was passiert ohne `super().__init__()`?

Vergisst man den Aufruf, wird der Konstruktor der Oberklasse **nicht** ausgeführt. Die Attribute der Oberklasse fehlen dann,
und Methoden der Oberklasse brechen mit einem `AttributeError` ab.

Statt `super().__init__(name)` liest man manchmal auch `Tier.__init__(self, name)`. Das bewirkt hier dasselbe.''',
     """class Tier:
    def __init__(self, name):
        self._name = name

    def get_name(self):
        return self._name

class Hund(Tier):
    def __init__(self, name, rasse):
        self._rasse = rasse

bello = Hund('Bello', 'Dackel')
print(bello.get_name())""", error=AttributeError)

PERSON = ("class Person:\n    def __init__(self, name, alter):\n        self._name = name\n        self._alter = alter\n\n"
          "    def get_name(self):\n        return self._name\n\n    def get_alter(self):\n        return self._alter\n")
t('''Schreibe eine Unterklasse `Schueler` von `Person` mit dem zusätzlichen Attribut `klasse` und dem Getter `get_klasse()`. Erzeuge Bea, 15, aus der 9c und gib
`Bea (15), 9c` aus.''',
  PERSON, """
class Schueler(Person):
    def __init__(self, name, alter, klasse):
        super().__init__(name, alter)
        self._klasse = klasse

    def get_klasse(self):
        return self._klasse

s = Schueler('Bea', 15, '9c')
print(f'{s.get_name()} ({s.get_alter()}), {s.get_klasse()}')""")
td('''Setze die Klassen um. Eine Lehrkraft ist eine Person mit einer Liste von Fächern (Start: leer). `neues_fach()` hängt ein Fach an, `get_faecher()` gibt die Fächer
als Text mit Komma zurück. Erzeuge Frau Weber (45) mit Mathe und Informatik und gib Name, Alter und Fächer aus.''',
   'lehrkraft.png',
   {'Person': (['# name: str', '# alter: int'], ['+ Person(name: str, alter: int)', '+ get_name(): str', '+ get_alter(): int']),
    'Lehrkraft': (['# faecher: list'], ['+ Lehrkraft(name: str, alter: int)', '+ neues_fach(fach: str): void', '+ get_faecher(): str'])},
   [('Lehrkraft', 'Person', 'vererbung')], {'Person': (0, 0), 'Lehrkraft': (0, 2.1)},
   given=PERSON,
   body="""
class Lehrkraft(Person):
    def __init__(self, name, alter):
        super().__init__(name, alter)
        self._faecher = []

    def neues_fach(self, fach):
        self._faecher.append(fach)

    def get_faecher(self):
        return ', '.join(self._faecher)

w = Lehrkraft('Frau Weber', 45)
w.neues_fach('Mathe')
w.neues_fach('Informatik')
print(w.get_name(), w.get_alter(), w.get_faecher())""")
t('''Schreibe eine Unterklasse `Sparkonto` von `Konto` mit dem zusätzlichen Attribut `zinssatz` (in Prozent) und einer Methode `zinsen_gutschreiben()`, die die Zinsen
für ein Jahr zum Kontostand addiert. Erzeuge ein Sparkonto mit 1000 Euro und 2 % Zinsen, schreibe zweimal Zinsen gut und gib den Kontostand aus.''',
  "class Konto:\n    def __init__(self, inhaber, stand):\n        self._inhaber = inhaber\n        self._stand = stand\n\n    def get_stand(self):\n        return self._stand",
  """
class Sparkonto(Konto):
    def __init__(self, inhaber, stand, zinssatz):
        super().__init__(inhaber, stand)
        self._zinssatz = zinssatz

    def zinsen_gutschreiben(self):
        self._stand += self._stand * self._zinssatz / 100

s = Sparkonto('Ali', 1000, 2)
s.zinsen_gutschreiben()
s.zinsen_gutschreiben()
print(s.get_stand())""")
t('''Schreibe eine Unterklasse `Farbpunkt` von `Punkt` mit dem zusätzlichen Attribut `farbe` (Standardwert `'schwarz'`). Erzeuge einen roten Farbpunkt (2|3) und einen
Farbpunkt (0|0) ohne Farbe und gib für beide `koordinaten()` und `get_farbe()` aus.''',
  "class Punkt:\n    def __init__(self, x, y):\n        self._x = x\n        self._y = y\n\n    def koordinaten(self):\n        return f'({self._x}|{self._y})'",
  """
class Farbpunkt(Punkt):
    def __init__(self, x, y, farbe='schwarz'):
        super().__init__(x, y)
        self._farbe = farbe

    def get_farbe(self):
        return self._farbe

for p in [Farbpunkt(2, 3, 'rot'), Farbpunkt(0, 0)]:
    print(p.koordinaten(), p.get_farbe())""")
t('''Der Konstruktor der Unterklasse muss nicht alle Werte als Parameter bekommen. Schreibe eine Unterklasse `Quadrat` von `Rechteck`, deren Konstruktor nur `seite` bekommt
und `super().__init__(seite, seite)` aufruft. Gib die Fläche eines Quadrats mit Seite 7 aus.''',
  "class Rechteck:\n    def __init__(self, breite, hoehe):\n        self._breite = breite\n        self._hoehe = hoehe\n\n    def flaeche(self):\n        return self._breite * self._hoehe",
  """
class Quadrat(Rechteck):
    def __init__(self, seite):
        super().__init__(seite, seite)

print(Quadrat(7).flaeche())""")
predict("""class A:
    def __init__(self):
        print('A wird erzeugt')
        self.x = 1

class B(A):
    def __init__(self):
        print('B wird erzeugt')
        super().__init__()
        self.y = 2

b = B()
print(b.x + b.y)""")
predict("""class A:
    def __init__(self, x):
        self.x = x

class B(A):
    pass

b = B(5)
print(b.x)
c = B()""", error=TypeError)

# ---------------------------------------------------------------- 3
sec('Methoden überschreiben und erweitern')
expl('''#### Überschreiben

Hat die Unterklasse eine Methode mit **demselben Namen** wie die Oberklasse, wird für Objekte der Unterklasse **ihre** Methode benutzt.
Man sagt: Sie **überschreibt** die Methode der Oberklasse. Objekte der Oberklasse benutzen weiter die alte Methode.''',
     """class Tier:
    def __init__(self, name):
        self._name = name

    def laut(self):
        return '...'

class Hund(Tier):
    def laut(self):
        return 'Wuff'

class Katze(Tier):
    def laut(self):
        return 'Miau'

class Fisch(Tier):
    pass

for t in [Hund('Bello'), Katze('Minka'), Fisch('Nemo')]:
    print(t._name, t.laut())""")
expl('''#### Erweitern mit `super()`

Will man die Methode der Oberklasse nicht ersetzen, sondern **ergänzen**, ruft man sie in der neuen Methode mit `super().methode()` auf und macht dann noch etwas dazu.
Das geht auch bei `__str__`.''',
     """class Person:
    def __init__(self, name):
        self._name = name

    def __str__(self):
        return self._name

class Schueler(Person):
    def __init__(self, name, klasse):
        super().__init__(name)
        self._klasse = klasse

    def __str__(self):
        return super().__str__() + ' (' + self._klasse + ')'

print(Person('Herr Graf'))
print(Schueler('Ali', '10b'))""")

t('Schreibe eine Unterklasse `Ente` von `Tier`, die `laut()` überschreibt und `Quak` zurückgibt. Gib die Laute von Donald (Ente), Nemo (Tier) und Daisy (Ente) aus, in der Form `Donald: Quak`.',
  """class Tier:
    def __init__(self, name):
        self._name = name

    def laut(self):
        return '...'""",
  """
class Ente(Tier):
    def laut(self):
        return 'Quak'

for x in [Ente('Donald'), Tier('Nemo'), Ente('Daisy')]:
    print(f'{x._name}: {x.laut()}')""")
t('''Schreibe zur Klasse `Mitarbeiter` eine Unterklasse `Chef`, die `gehalt()` überschreibt: Ein Chef bekommt das Grundgehalt plus eine Zulage von 20 %
(rufe dafür `super().gehalt()` auf). Gib die Gehälter von `m` und `c` aus.''',
  "class Mitarbeiter:\n    def __init__(self, name, grundgehalt):\n        self._name = name\n        self._grundgehalt = grundgehalt\n\n    def gehalt(self):\n        return self._grundgehalt\n\n"
  "m = Mitarbeiter('Ali', 3000)",
  """
class Chef(Mitarbeiter):
    def gehalt(self):
        return super().gehalt() * 1.2

c = Chef('Frau König', 4000)
print(m.gehalt())
print(c.gehalt())""")
t('''Schreibe eine Unterklasse `Schueler` von `Person`, die `__str__` erweitert: An den Text der Oberklasse wird `, Klasse 9a` angehängt. Gib eine Person und einen Schüler aus.''',
  "class Person:\n    def __init__(self, name, alter):\n        self._name = name\n        self._alter = alter\n\n    def __str__(self):\n        return f'{self._name} ({self._alter})'",
  """
class Schueler(Person):
    def __init__(self, name, alter, klasse):
        super().__init__(name, alter)
        self._klasse = klasse

    def __str__(self):
        return super().__str__() + f', Klasse {self._klasse}'

print(Person('Frau Weber', 45))
print(Schueler('Ali', 15, '9a'))""")
t('''Ein Girokonto darf bis zu einem Dispo (z. B. 200 Euro) ins Minus gehen. Schreibe die Unterklasse `Girokonto` mit dem Attribut `dispo` und überschreibe `abheben()`:
Abheben ist erlaubt, solange der Kontostand danach nicht unter `-dispo` fällt. Hebe nacheinander 150, 100 und 80 ab (Startstand 100, Dispo 200) und gib jeweils das Ergebnis
und den Stand aus. Zum Vergleich: Ein normales Konto mit 100 darf 150 nicht abheben.''',
  "class Konto:\n    def __init__(self, stand):\n        self._stand = stand\n\n    def abheben(self, betrag):\n        if betrag > self._stand:\n            return False\n"
  "        self._stand -= betrag\n        return True\n\n    def get_stand(self):\n        return self._stand",
  """
class Girokonto(Konto):
    def __init__(self, stand, dispo):
        super().__init__(stand)
        self._dispo = dispo

    def abheben(self, betrag):
        if self._stand - betrag < -self._dispo:
            return False
        self._stand -= betrag
        return True

g = Girokonto(100, 200)
for b in [150, 100, 80]:
    print(g.abheben(b), g.get_stand())
print(Konto(100).abheben(150))""")
t('''Die Klasse `Artikel` berechnet in `preis()` den Preis mit 19 % Mehrwertsteuer. Für Lebensmittel gilt der ermäßigte Satz von 7 %. Schreibe die Unterklasse `Lebensmittel`,
die nur das Klassenattribut `MWST` überschreibt (`MWST = 7`), und ändere dafür in `Artikel.preis()` nichts. Gib die Preise für `artikel` mit zwei Nachkommastellen aus.''',
  "class Artikel:\n    MWST = 19\n\n    def __init__(self, name, netto):\n        self._name = name\n        self._netto = netto\n\n    def preis(self):\n        return self._netto * (100 + self.MWST) / 100",
  """
class Lebensmittel(Artikel):
    MWST = 7

artikel = [Artikel('Heft', 1.00), Lebensmittel('Brot', 2.00), Artikel('Stift', 2.50)]
for a in artikel:
    print(a._name, f'{a.preis():.2f}')""")
t('''Schreibe zur Klasse `Wuerfel` eine Unterklasse `GezinkterWuerfel`, die `werfen()` überschreibt: Mit `super().werfen()` wird normal gewürfelt, aber jede 1 wird zu einer 6.
Würfle mit `random.seed(2)` mit dem gezinkten Würfel 10-mal und gib die Würfe als Liste aus.''',
  "import random\nrandom.seed(2)\n\nclass Wuerfel:\n    def werfen(self):\n        return random.randint(1, 6)",
  """
class GezinkterWuerfel(Wuerfel):
    def werfen(self):
        w = super().werfen()
        if w == 1:
            return 6
        return w

g = GezinkterWuerfel()
wuerfe = []
for i in range(10):
    wuerfe.append(g.werfen())
print(wuerfe)""")
predict("""class A:
    def f(self):
        return 'A.f'

    def g(self):
        return 'A.g'

class B(A):
    def f(self):
        return 'B.f'

    def g(self):
        return super().g() + '+B.g'

b = B()
print(b.f())
print(b.g())
print(A().f())""")
predict("""class A:
    def wert(self):
        return 1

class B(A):
    def wert(self):
        return super().wert() * 10

class C(B):
    def wert(self):
        return super().wert() + 5

print(A().wert(), B().wert(), C().wert())""")

# ---------------------------------------------------------------- 4
sec('Geschützt und privat bei Vererbung')
ed('''#### Was darf die Unterklasse?

- **Öffentlich** (`+`, `name`): alle.
- **Geschützt** (`#`, `_name`): die Klasse selbst und ihre **Unterklassen** (eine Abmachung, Python prüft das nicht).
- **Privat** (`-`, `__name`): **nur** die Klasse selbst. Auch eine Unterklasse kommt nicht direkt heran:
  `self.__stand` in der Unterklasse sucht nach einem *anderen* Namen und gibt einen `AttributeError`.

Braucht eine Unterklasse ein privates Attribut der Oberklasse, benutzt sie die Zugriffsmethoden der Oberklasse (`self.get_stand()`).
Deshalb macht man Attribute, die Unterklassen brauchen, meist **geschützt**.''',
   """class Konto:
    def __init__(self, stand):
        self.__stand = stand

    def get_stand(self):
        return self.__stand

class Sparkonto(Konto):
    def zinsen(self):
        return self.get_stand() * 0.02

    def zinsen_falsch(self):
        return self.__stand * 0.02

s = Sparkonto(500)
print(s.zinsen())
print(s.zinsen_falsch())""",
   'konto_privat.png',
   {'Konto': (['- stand: float'], ['+ Konto(stand: float)', '+ get_stand(): float']),
    'Sparkonto': ([], ['+ zinsen(): float', '+ zinsen_falsch(): float'])},
   [('Sparkonto', 'Konto', 'vererbung')], {'Konto': (0, 0), 'Sparkonto': (0, 1.9)}, error=AttributeError)

t('''In der Oberklasse ist `__punkte` privat. Schreibe die Unterklasse `Profi` mit einer Methode `bonus()`, die `get_punkte()` benutzt und das Doppelte der Punkte zurückgibt.
Gib `bonus()` für einen Profi mit 40 Punkten aus.''',
  "class Spieler:\n    def __init__(self, punkte):\n        self.__punkte = punkte\n\n    def get_punkte(self):\n        return self.__punkte",
  """
class Profi(Spieler):
    def bonus(self):
        return 2 * self.get_punkte()

print(Profi(40).bonus())""")
t('''Versuche in der Unterklasse `Profi`, direkt auf `self.__punkte` zuzugreifen. Fange den Fehler beim Aufruf ab und gib den Namen des Fehlertyps aus.
Ändere danach die Oberklasse so, dass das Attribut geschützt ist (`_punkte`, Klasse `Spieler2`), und gib das Ergebnis von `Profi2(40).bonus()` aus.''',
  "class Spieler:\n    def __init__(self, punkte):\n        self.__punkte = punkte\n\nclass Profi(Spieler):\n    def bonus(self):\n        return 2 * self.__punkte",
  """
try:
    print(Profi(40).bonus())
except Exception as e:
    print(type(e).__name__)

class Spieler2:
    def __init__(self, punkte):
        self._punkte = punkte

class Profi2(Spieler2):
    def bonus(self):
        return 2 * self._punkte

print(Profi2(40).bonus())""")
td('''Setze die Klassen aus dem Diagramm um. `Fahrzeug.fahren(km)` erhöht den geschützten Kilometerstand. `Elektroauto` hat zusätzlich einen privaten Akkustand in Prozent
(Start 100). Es überschreibt `fahren()`: Pro 5 km sinkt der Akku um 1 Prozentpunkt (`km // 5`). Reicht der Akku nicht, fährt es nicht und gibt `False` zurück, sonst
ruft es `super().fahren(km)` auf und gibt `True` zurück. Fahre 200, 300 und 100 km und gib jeweils Ergebnis, Kilometerstand und Akku aus.''',
   'elektroauto.png',
   {'Fahrzeug': (['# km: int'], ['+ Fahrzeug()', '+ fahren(km: int): bool', '+ get_km(): int']),
    'Elektroauto': (['- akku: int'], ['+ Elektroauto()', '+ fahren(km: int): bool', '+ get_akku(): int'])},
   [('Elektroauto', 'Fahrzeug', 'vererbung')], {'Fahrzeug': (0, 0), 'Elektroauto': (0, 1.9)},
   body="""class Fahrzeug:
    def __init__(self):
        self._km = 0

    def fahren(self, km):
        self._km += km
        return True

    def get_km(self):
        return self._km

class Elektroauto(Fahrzeug):
    def __init__(self):
        super().__init__()
        self.__akku = 100

    def fahren(self, km):
        verbrauch = km // 5
        if verbrauch > self.__akku:
            return False
        self.__akku -= verbrauch
        return super().fahren(km)

    def get_akku(self):
        return self.__akku

e = Elektroauto()
for km in [200, 300, 100]:
    print(e.fahren(km), e.get_km(), e.get_akku())""")
predict("""class A:
    def __init__(self):
        self._x = 1
        self.__y = 2

    def get_y(self):
        return self.__y

class B(A):
    def summe(self):
        return self._x + self.get_y()

print(B().summe())""")

# ---------------------------------------------------------------- 5
sec('Polymorphie')
expl('''#### Gleicher Aufruf, verschiedenes Verhalten

In einer Liste können Objekte **verschiedener Unterklassen** stehen. Ruft man für jedes dieselbe Methode auf, führt jedes Objekt **seine eigene** Version aus.
Das nennt man **Polymorphie** („Vielgestaltigkeit“). Man muss dafür nicht mit `isinstance()` nachsehen, welche Klasse ein Objekt hat.''',
     """class Form:
    def flaeche(self):
        return 0

class Rechteck(Form):
    def __init__(self, a, b):
        self._a = a
        self._b = b

    def flaeche(self):
        return self._a * self._b

class Kreis(Form):
    def __init__(self, r):
        self._r = r

    def flaeche(self):
        return 3.14 * self._r ** 2

formen = [Rechteck(2, 3), Kreis(1), Rechteck(4, 4)]
summe = 0
for f in formen:
    summe += f.flaeche()
print(summe)""")
expl('''#### Die Oberklasse ruft die Methode der Unterklasse

Eine Methode der Oberklasse kann eine Methode aufrufen, die erst die Unterklassen festlegen: `self.laut()` ruft die Version der **tatsächlichen** Klasse des Objekts auf.

Soll die Oberklasse selbst keine sinnvolle Version haben, löst sie `NotImplementedError` aus. So merkt man sofort, wenn eine Unterklasse die Methode vergessen hat.
Eine solche Oberklasse, von der man selbst keine Objekte erzeugt, nennt man **abstrakt**. Im Diagramm schreibt man ihren Namen oft *kursiv*.''',
     """class Tier:
    def __init__(self, name):
        self._name = name

    def laut(self):
        raise NotImplementedError('Unterklasse muss laut() festlegen')

    def vorstellen(self):
        return f'Ich bin {self._name} und sage {self.laut()}.'

class Hund(Tier):
    def laut(self):
        return 'Wuff'

class Kuh(Tier):
    def laut(self):
        return 'Muh'

class Fisch(Tier):
    pass

print(Hund('Bello').vorstellen())
print(Kuh('Elsa').vorstellen())
print(Fisch('Nemo').vorstellen())""", error=NotImplementedError)

FORM = ("class Form:\n    def flaeche(self):\n        raise NotImplementedError\n\n    def beschreibung(self):\n        return f'{type(self).__name__} mit Fläche {self.flaeche():.2f}'\n")
t('''Schreibe die Unterklassen `Rechteck` (Breite, Höhe), `Kreis` (Radius, mit 3.14) und `Dreieck` (Grundseite, Höhe) von `Form` mit je einer Methode `flaeche()`.
Gib für jede Form in einer Liste mit Rechteck(3, 4), Kreis(2) und Dreieck(6, 5) `beschreibung()` aus.''',
  FORM, """
class Rechteck(Form):
    def __init__(self, breite, hoehe):
        self._breite = breite
        self._hoehe = hoehe

    def flaeche(self):
        return self._breite * self._hoehe

class Kreis(Form):
    def __init__(self, r):
        self._r = r

    def flaeche(self):
        return 3.14 * self._r ** 2

class Dreieck(Form):
    def __init__(self, g, h):
        self._g = g
        self._h = h

    def flaeche(self):
        return self._g * self._h / 2

for f in [Rechteck(3, 4), Kreis(2), Dreieck(6, 5)]:
    print(f.beschreibung())""")
t('''Gib mit der Klasse `Form` und den Unterklassen aus der Aufgabe davor (hier schon vorgegeben) die Form mit der größten Fläche aus (`max` mit `key=`) und die Summe aller Flächen
mit zwei Nachkommastellen.''',
  FORM + "\nclass Rechteck(Form):\n    def __init__(self, b, h):\n        self._b = b\n        self._h = h\n\n    def flaeche(self):\n        return self._b * self._h\n\n"
  "class Kreis(Form):\n    def __init__(self, r):\n        self._r = r\n\n    def flaeche(self):\n        return 3.14 * self._r ** 2\n\nformen = [Rechteck(3, 4), Kreis(2), Rechteck(1, 10), Kreis(1)]",
  """
print(max(formen, key=lambda f: f.flaeche()).beschreibung())
summe = 0
for f in formen:
    summe += f.flaeche()
print(f'{summe:.2f}')""")
td('''Setze die Klassen um. Die abstrakte Klasse `Mitarbeiter` hat `gehalt()` (löst `NotImplementedError` aus) und `abrechnung()`, die `Ali: 2400.00 Euro` zurückgibt.
Festangestellte bekommen ein festes Monatsgehalt, Aushilfen `stunden * stundenlohn`. Gib die Abrechnungen für `team` aus und danach die Summe aller Gehälter.''',
   'mitarbeiter_vererbung.png',
   {'Mitarbeiter': (['# name: str'], ['+ Mitarbeiter(name: str)', '+ gehalt(): float', '+ abrechnung(): str']),
    'Festangestellter': (['- monatsgehalt: float'], ['+ Festangestellter(name: str, monatsgehalt: float)', '+ gehalt(): float']),
    'Aushilfe': (['- stunden: float', '- stundenlohn: float'], ['+ Aushilfe(name: str, stunden: float, stundenlohn: float)', '+ gehalt(): float'])},
   [('Festangestellter', 'Mitarbeiter', 'vererbung'), ('Aushilfe', 'Mitarbeiter', 'vererbung')],
   {'Mitarbeiter': (2.0, 0), 'Festangestellter': (0, 2.3), 'Aushilfe': (4.6, 2.3)},
   body="""class Mitarbeiter:
    def __init__(self, name):
        self._name = name

    def gehalt(self):
        raise NotImplementedError

    def abrechnung(self):
        return f'{self._name}: {self.gehalt():.2f} Euro'

class Festangestellter(Mitarbeiter):
    def __init__(self, name, monatsgehalt):
        super().__init__(name)
        self.__monatsgehalt = monatsgehalt

    def gehalt(self):
        return self.__monatsgehalt

class Aushilfe(Mitarbeiter):
    def __init__(self, name, stunden, stundenlohn):
        super().__init__(name)
        self.__stunden = stunden
        self.__stundenlohn = stundenlohn

    def gehalt(self):
        return self.__stunden * self.__stundenlohn

team = [Festangestellter('Ali', 2400), Aushilfe('Bea', 40, 13.5), Festangestellter('Cem', 3100), Aushilfe('Dana', 12, 15)]
summe = 0
for m in team:
    print(m.abrechnung())
    summe += m.gehalt()
print(f'{summe:.2f}')""")
t('''Die Spielfiguren haben verschiedene Zugweiten. Ergänze die Unterklassen `Laeufer` (zieht immer 2 Felder) und `Springer` (zieht 3 Felder, aber nur bei geraden Würfelzahlen,
sonst 0), indem du `schritte(wurf)` überschreibst. `Figur.ziehen(wurf)` ist fertig. Lass jede Figur in `figuren` mit allen Würfen aus `wuerfe` ziehen und gib die Positionen aus.''',
  "class Figur:\n    def __init__(self, name):\n        self._name = name\n        self._pos = 0\n\n    def schritte(self, wurf):\n        return wurf\n\n"
  "    def ziehen(self, wurf):\n        self._pos += self.schritte(wurf)\n\n    def __str__(self):\n        return f'{self._name}: {self._pos}'",
  """
class Laeufer(Figur):
    def schritte(self, wurf):
        return 2

class Springer(Figur):
    def schritte(self, wurf):
        if wurf % 2 == 0:
            return 3
        return 0

figuren = [Figur('normal'), Laeufer('Läufer'), Springer('Springer')]
wuerfe = [3, 6, 1, 4, 2]
for f in figuren:
    for w in wuerfe:
        f.ziehen(w)
    print(f)""")
t('''Erzeuge ein Objekt der abstrakten Klasse `Form` und rufe `beschreibung()` auf. Fange den Fehler ab und gib `Form ist abstrakt` aus.''',
  FORM, """
try:
    print(Form().beschreibung())
except NotImplementedError:
    print('Form ist abstrakt')""")
predict("""class Tier:
    def laut(self):
        return '?'

    def zweimal(self):
        return self.laut() + self.laut()

class Hund(Tier):
    def laut(self):
        return 'Wau'

class Katze(Tier):
    pass

for t in [Hund(), Katze(), Tier()]:
    print(t.zweimal())""")
predict("""class A:
    def name(self):
        return 'A'

    def hallo(self):
        return 'Hallo ' + self.name()

class B(A):
    def name(self):
        return 'B'

    def hallo(self):
        return super().hallo() + '!'

print(A().hallo())
print(B().hallo())""")

# ---------------------------------------------------------------- 6
sec('Mehrstufige Vererbung')
ed('''#### Ketten von Klassen

Eine Unterklasse kann selbst wieder Oberklasse sein: `Dackel` erbt von `Hund`, `Hund` erbt von `Tier`. Ein Dackel hat dann alles von `Hund` **und** von `Tier`.
Sucht Python eine Methode, schaut es zuerst in der Klasse des Objekts, dann in ihrer Oberklasse, dann in deren Oberklasse usw.

`issubclass(Dackel, Tier)` prüft, ob eine Klasse (direkt oder weiter oben) von einer anderen erbt. Jede Klasse erbt am Ende von der eingebauten Klasse `object`.
Von dort stammen zum Beispiel das Standard-`__str__` und das Standard-`==`.

`type(x)` ist genau die Klasse des Objekts, `isinstance(x, K)` ist auch für alle Oberklassen `True`.''',
   """class Tier:
    def atmen(self):
        return 'atmet'

class Hund(Tier):
    def bellen(self):
        return 'bellt'

class Dackel(Hund):
    def buddeln(self):
        return 'buddelt'

d = Dackel()
print(d.atmen(), d.bellen(), d.buddeln())
print(issubclass(Dackel, Tier), issubclass(Tier, Dackel), issubclass(Tier, object))
print(type(d) == Hund, isinstance(d, Hund))""",
   'dackel.png',
   {'Tier': ([], ['+ atmen(): str']), 'Hund': ([], ['+ bellen(): str']), 'Dackel': ([], ['+ buddeln(): str'])},
   [('Hund', 'Tier', 'vererbung'), ('Dackel', 'Hund', 'vererbung')],
   {'Tier': (0, 0), 'Hund': (0, 1.6), 'Dackel': (0, 3.2)})

td('''Setze die Klassen aus dem Diagramm um. Ein E-Bike ist ein Fahrrad, ein Fahrrad ist ein Fahrzeug. `beschreibung()` wird in jeder Stufe mit `super()` erweitert:
`Fahrzeug` gibt `Fahrzeug mit 2 Rädern` zurück, `Fahrrad` hängt `, Pedale` an und `EBike` `, Motor 250 W`. Gib die Beschreibung aller drei Klassen aus.''',
   'ebike.png',
   {'Fahrzeug': (['# raeder: int'], ['+ Fahrzeug(raeder: int)', '+ beschreibung(): str']),
    'Fahrrad': ([], ['+ Fahrrad()', '+ beschreibung(): str']),
    'EBike': (['# watt: int'], ['+ EBike(watt: int)', '+ beschreibung(): str'])},
   [('Fahrrad', 'Fahrzeug', 'vererbung'), ('EBike', 'Fahrrad', 'vererbung')],
   {'Fahrzeug': (0, 0), 'Fahrrad': (0, 1.9), 'EBike': (0, 3.6)},
   body="""class Fahrzeug:
    def __init__(self, raeder):
        self._raeder = raeder

    def beschreibung(self):
        return f'Fahrzeug mit {self._raeder} Rädern'

class Fahrrad(Fahrzeug):
    def __init__(self):
        super().__init__(2)

    def beschreibung(self):
        return super().beschreibung() + ', Pedale'

class EBike(Fahrrad):
    def __init__(self, watt):
        super().__init__()
        self._watt = watt

    def beschreibung(self):
        return super().beschreibung() + f', Motor {self._watt} W'

print(Fahrzeug(2).beschreibung())
print(Fahrrad().beschreibung())
print(EBike(250).beschreibung())""")
t('''Gib für jede Klasse in `klassen` aus, ob sie eine Unterklasse von `Hund` ist, in der Form `Dackel True`. Verwende `issubclass()` und `K.__name__` für den Namen.''',
  "class Tier:\n    pass\n\nclass Hund(Tier):\n    pass\n\nclass Dackel(Hund):\n    pass\n\nclass Katze(Tier):\n    pass\n\nklassen = [Tier, Hund, Dackel, Katze]",
  """for k in klassen:
    print(k.__name__, issubclass(k, Hund))""")
t('''Zähle mit einem Dictionary, wie viele Objekte in `zoo` von jeder **genauen** Klasse sind (`type(x).__name__`), und gib es aus. Gib danach aus, wie viele Objekte
insgesamt Hunde sind (auch Dackel), mit `isinstance()`.''',
  "class Tier:\n    pass\n\nclass Hund(Tier):\n    pass\n\nclass Dackel(Hund):\n    pass\n\nclass Katze(Tier):\n    pass\n\nzoo = [Hund(), Dackel(), Katze(), Dackel(), Tier(), Hund()]",
  """anzahl = {}
for x in zoo:
    name = type(x).__name__
    anzahl[name] = anzahl.get(name, 0) + 1
print(anzahl)
hunde = 0
for x in zoo:
    if isinstance(x, Hund):
        hunde += 1
print(hunde)""")
predict("""class A:
    def f(self):
        return 'A'

    def g(self):
        return 'g von A'

class B(A):
    def f(self):
        return 'B'

class C(B):
    def g(self):
        return 'g von C'

c = C()
print(c.f(), c.g())
print(isinstance(c, A), type(c) == B)""")

# ---------------------------------------------------------------- 7
sec('Gemischte Übungen')
td('''Setze die Klassen um. `Medium` hat Titel und Ausleihdauer in Tagen (Klassenattribut `TAGE = 28`), `ausleihfrist(tag)` gibt den Rückgabetag (`tag + TAGE`) zurück.
`DVD` überschreibt nur `TAGE = 7`, `Zeitschrift` hat zusätzlich eine Heftnummer und erweitert `__str__` um ` Nr. 5`. Gib für jedes Medium in `medien` den Text und die Frist
für Ausleihtag 10 aus.''',
   'medium.png',
   {'Medium': (['# titel: str', 'static + TAGE: int'], ['+ Medium(titel: str)', '+ ausleihfrist(tag: int): int', '+ __str__(): str']),
    'DVD': ([], []),
    'Zeitschrift': (['# nummer: int'], ['+ Zeitschrift(titel: str, nummer: int)', '+ __str__(): str'])},
   [('DVD', 'Medium', 'vererbung'), ('Zeitschrift', 'Medium', 'vererbung')],
   {'Medium': (1.0, 0), 'DVD': (0, 2.3), 'Zeitschrift': (2.0, 2.3)},
   body="""class Medium:
    TAGE = 28

    def __init__(self, titel):
        self._titel = titel

    def ausleihfrist(self, tag):
        return tag + self.TAGE

    def __str__(self):
        return self._titel

class DVD(Medium):
    TAGE = 7

class Zeitschrift(Medium):
    def __init__(self, titel, nummer):
        super().__init__(titel)
        self._nummer = nummer

    def __str__(self):
        return super().__str__() + f' Nr. {self._nummer}'

medien = [Medium('Momo'), DVD('Shrek'), Zeitschrift('c\\'t', 5)]
for m in medien:
    print(m, m.ausleihfrist(10))""")
t('''Schreibe eine Klasse `Spielfigur` mit Name und Lebenspunkten (Start 100), `angreifen(gegner)` zieht dem Gegner `schaden()` Punkte ab, `schaden()` gibt 10 zurück,
`lebt()` gibt zurück, ob die Lebenspunkte über 0 sind. `Krieger` macht 15 Schaden, `Magier` 25 Schaden, verliert aber bei jedem Angriff selbst 5 Lebenspunkte
(erweitere `angreifen()`). Krieger und Magier greifen sich abwechselnd an (der Krieger beginnt), bis einer nicht mehr lebt. Gib nach jedem Angriff beide Lebenspunkte aus und am Ende den Sieger.''',
  body="""class Spielfigur:
    def __init__(self, name):
        self._name = name
        self._leben = 100

    def schaden(self):
        return 10

    def angreifen(self, gegner):
        gegner._leben -= self.schaden()

    def lebt(self):
        return self._leben > 0

class Krieger(Spielfigur):
    def schaden(self):
        return 15

class Magier(Spielfigur):
    def schaden(self):
        return 25

    def angreifen(self, gegner):
        super().angreifen(gegner)
        self._leben -= 5

k = Krieger('Konan')
m = Magier('Merlin')
angreifer, verteidiger = k, m
while k.lebt() and m.lebt():
    angreifer.angreifen(verteidiger)
    print(k._leben, m._leben)
    angreifer, verteidiger = verteidiger, angreifer
if k.lebt():
    print('Sieger:', k._name)
else:
    print('Sieger:', m._name)""")
td('''Setze die Klassen um und verbinde dabei Vererbung und Assoziation: Ein `Zoo` kennt beliebig viele Tiere. `Tier` ist abstrakt mit `futter_kg()`;
`Loewe` frisst 7 kg, `Elefant` 70 kg, `Pinguin` 0.5 kg. `Zoo.futterbedarf()` gibt die Summe zurück, `Zoo.anzahl(klasse)` die Zahl der Tiere einer Klasse (mit `isinstance`).
Lege die Tiere aus `bestand` an und gib den Futterbedarf und die Zahl der Pinguine aus.''',
   'zoo.png',
   {'Zoo': (['- tiere: list'], ['+ Zoo()', '+ aufnehmen(t: Tier): void', '+ futterbedarf(): float', '+ anzahl(klasse): int']),
    'Tier': (['# name: str'], ['+ Tier(name: str)', '+ futter_kg(): float']),
    'Loewe': ([], ['+ futter_kg(): float']), 'Elefant': ([], ['+ futter_kg(): float']), 'Pinguin': ([], ['+ futter_kg(): float'])},
   [('Zoo', 'Tier', 'assoziation', '0..*'), ('Loewe', 'Tier', 'vererbung'), ('Elefant', 'Tier', 'vererbung'), ('Pinguin', 'Tier', 'vererbung')],
   {'Zoo': (0, 0), 'Tier': (4.0, 0), 'Loewe': (2.4, 2.1), 'Elefant': (4.4, 2.1), 'Pinguin': (6.4, 2.1)},
   given="bestand = [('Loewe', 'Leo'), ('Pinguin', 'Pingu'), ('Elefant', 'Benjamin'), ('Pinguin', 'Pinga'), ('Loewe', 'Nala')]",
   body="""class Tier:
    def __init__(self, name):
        self._name = name

    def futter_kg(self):
        raise NotImplementedError

class Loewe(Tier):
    def futter_kg(self):
        return 7

class Elefant(Tier):
    def futter_kg(self):
        return 70

class Pinguin(Tier):
    def futter_kg(self):
        return 0.5

class Zoo:
    def __init__(self):
        self.__tiere = []

    def aufnehmen(self, t):
        self.__tiere.append(t)

    def futterbedarf(self):
        summe = 0
        for t in self.__tiere:
            summe += t.futter_kg()
        return summe

    def anzahl(self, klasse):
        n = 0
        for t in self.__tiere:
            if isinstance(t, klasse):
                n += 1
        return n

klassen = {'Loewe': Loewe, 'Elefant': Elefant, 'Pinguin': Pinguin}
zoo = Zoo()
for art, name in bestand:
    zoo.aufnehmen(klassen[art](name))
print(zoo.futterbedarf())
print(zoo.anzahl(Pinguin))""")
expl('''In der Aufgabe davor stehen **Klassen** als Werte in einem Dictionary: `klassen['Loewe']` ist die Klasse `Loewe`, und `klassen['Loewe']('Leo')` erzeugt einen Löwen.
Klassen sind in Python auch nur Werte, die man in Variablen speichern und an Funktionen übergeben kann (wie bei `anzahl(Pinguin)`).''',
     """class Hund:
    pass

k = Hund
h = k()
print(type(h).__name__, k.__name__)""")
t('''Schreibe die Klassen für ein Bestellsystem: `Produkt` mit Name und Nettopreis, `preis()` gibt den Preis mit 19 % zurück. `Rabattprodukt` hat zusätzlich einen Rabatt
in Prozent und erweitert `preis()` (Rabatt auf den Preis der Oberklasse). `Gutschein` ist ein Produkt mit negativem Preis ohne Mehrwertsteuer (überschreibt `preis()`).
Gib die Summe der Preise aller Posten in einer Liste mit Produkt('Buch', 10), Rabattprodukt('Spiel', 40, 25), Gutschein('Gutschein', -5) mit zwei Nachkommastellen aus.''',
  body="""class Produkt:
    def __init__(self, name, netto):
        self._name = name
        self._netto = netto

    def preis(self):
        return self._netto * 1.19

class Rabattprodukt(Produkt):
    def __init__(self, name, netto, rabatt):
        super().__init__(name, netto)
        self._rabatt = rabatt

    def preis(self):
        return super().preis() * (100 - self._rabatt) / 100

class Gutschein(Produkt):
    def preis(self):
        return self._netto

posten = [Produkt('Buch', 10), Rabattprodukt('Spiel', 40, 25), Gutschein('Gutschein', -5)]
summe = 0
for p in posten:
    summe += p.preis()
print(f'{summe:.2f}')""")
predict("""class Konto:
    def __init__(self, stand):
        self._stand = stand

    def gebuehr(self):
        return 5

    def monatsende(self):
        self._stand -= self.gebuehr()
        return self._stand

class Schuelerkonto(Konto):
    def gebuehr(self):
        return 0

class Premiumkonto(Konto):
    def gebuehr(self):
        return super().gebuehr() * 2

for k in [Konto(100), Schuelerkonto(100), Premiumkonto(100)]:
    k.monatsende()
    print(k.monatsende())""")

generate('oop_vererbung', 'OOP 4: Vererbung', INTRO)
