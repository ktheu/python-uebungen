# Erzeugt ../content/matplotlib_diagrammtypen.ipynb (siehe nbgen.py).
#
# Braucht matplotlib 3.10.8 und numpy 2.4.6 (wie Pyodide in JupyterLite), siehe gen_matplotlib_grundlagen.py:
#     py -3.13 -W error generator/gen_matplotlib_diagrammtypen.py
#     py -3.13 generator/pyodide_check/pruefen.py generator/gen_matplotlib_diagrammtypen.py
#
# -W error macht auch veraltete matplotlib-Parameter zu Fehlern (z. B. boxplot(labels=...) -> tick_labels=...).
# Zufallsdaten immer mit festem Seed, damit die erwarteten Diagramme stimmen.
from nbgen import sec, expl, task, predict, generate, setup


def t(text, given='', body='', kind='normal'):
    """Aufgabe, deren Lösung aus dem vorgegebenen Code plus body besteht."""
    task(text, given=given, solution=(given + '\n' + body) if given else body, kind=kind)


PLT = 'import matplotlib.pyplot as plt'
NPP = 'import numpy as np\nimport matplotlib.pyplot as plt'

INTRO = '''Je nach Art der Daten passt ein anderes Diagramm: **Streudiagramme** für Zusammenhänge zwischen zwei Größen,
**Balkendiagramme** für Kategorien, **Histogramme** für Verteilungen, **Kreisdiagramme** für Anteile und **Boxplots** für den
Vergleich von Verteilungen. In diesem Notebook lernst du diese Diagrammtypen kennen.

Vorausgesetzt werden die Notebooks *matplotlib: Grundlagen* (Beschriften, Farben, Achsen) und *numpy: Grundlagen*.
Für einige Aufgaben ist *numpy: Zufall und Statistik* hilfreich.

Jeder Abschnitt beginnt mit kurzen Erklärungen und Beispielen. Führe die Beispiele aus und probiere sie ruhig ein wenig aus.
Danach folgen viele kleine Übungen. Unter den meisten Aufgaben siehst du das **erwartete Diagramm**. Zeichne es nach und vergleiche.'''

setup('''#### Beispieldateien anlegen

**Führe diese Zelle zuerst aus.** Sie legt im aktuellen Ordner die Dateien an, die im Abschnitt *Daten aus Dateien* gebraucht werden.''',
      r"""dateien = {
    'umfrage.csv': 'fach;stimmen\nMathe;14\nDeutsch;9\nEnglisch;11\nInformatik;18\nSport;23\nKunst;7\n',
    'sport.csv': 'name,groesse,weitsprung,klasse\nAli,168,4.10,9a\nBea,159,3.65,9a\nCem,175,4.55,9b\nDana,163,3.90,9b\nEli,181,4.80,9a\nFia,166,4.05,9b\nGus,172,4.30,9a\nHana,157,3.50,9b\nIda,170,4.20,9a\nJan,178,4.65,9b\n',
    'verkauf.csv': 'monat,eis,kakao\nJan,20,95\nFeb,25,90\nMär,40,70\nApr,65,50\nMai,90,30\nJun,120,20\nJul,140,15\nAug,135,15\nSep,95,30\nOkt,55,55\nNov,30,80\nDez,22,100\n',
}
for name, inhalt in dateien.items():
    with open(name, 'w', encoding='utf-8') as f:
        f.write(inhalt)
print('Angelegt:', ', '.join(dateien))""")

# ---------------------------------------------------------------- 1
sec('Streudiagramme')
expl('''#### `plt.scatter()`

`plt.scatter(x, y)` zeichnet für jedes Wertepaar einen **Punkt**, ohne die Punkte zu verbinden. So sieht man, ob zwei Größen
zusammenhängen (z. B. Körpergröße und Gewicht).

| Parameter | Bedeutung |
|---|---|
| `s` | Größe der Punkte (Fläche, z. B. `s=100`); auch ein Array: jeder Punkt eigene Größe |
| `color` | eine Farbe für alle Punkte |
| `marker` | Form wie bei `plot()`: `'o'`, `'s'`, `'^'`, ... |
| `alpha` | Deckkraft von 0 (unsichtbar) bis 1, hilfreich bei vielen überlappenden Punkten |
| `edgecolor` | Farbe des Randes |''',
     """import matplotlib.pyplot as plt

groesse = [158, 162, 165, 170, 172, 175, 180, 185]
gewicht = [52, 58, 57, 65, 68, 70, 77, 82]
plt.scatter(groesse, gewicht)
plt.xlabel('Größe (cm)')
plt.ylabel('Gewicht (kg)')
plt.show()

plt.scatter(groesse, gewicht, s=150, color='orange', marker='s', edgecolor='black', alpha=0.6)
plt.show()""")
expl('''#### Farben nach Werten

Mit `c=werte` bekommt jeder Punkt eine Farbe nach seinem Wert, mit `cmap='viridis'` (oder `'plasma'`, `'coolwarm'`, ...) wählt man die
**Farbskala**. `plt.colorbar()` zeigt daneben an, welche Farbe welchem Wert entspricht.''',
     """import numpy as np
import matplotlib.pyplot as plt

rng = np.random.default_rng(1)
x = rng.random(50)
y = rng.random(50)
plt.scatter(x, y, c=x + y, cmap='viridis', s=80)
plt.colorbar()
plt.show()""")

S = PLT + '\nlernzeit = [1, 2, 2, 3, 4, 5, 5, 6, 7, 8]\npunkte = [35, 41, 46, 50, 58, 61, 67, 70, 76, 80]'
t('Zeichne ein Streudiagramm von Lernzeit und Punkten.', S,
  """plt.scatter(lernzeit, punkte)
plt.show()""")
t('Zeichne das Streudiagramm mit roten Punkten der Größe 100 und beschrifte die Achsen mit `Lernzeit (h)` und `Punkte`.', S,
  """plt.scatter(lernzeit, punkte, s=100, color='red')
plt.xlabel('Lernzeit (h)')
plt.ylabel('Punkte')
plt.show()""")
t('Zeichne das Streudiagramm mit grünen Dreiecken der Größe 120 mit schwarzem Rand und Gitter.', S,
  """plt.scatter(lernzeit, punkte, s=120, color='green', marker='^', edgecolor='black')
plt.grid(True)
plt.show()""")
t('''Zeichne das Streudiagramm und zusätzlich die Regressionsgerade als rote Linie von 0 bis 9 (`np.polyfit(..., 1)`, siehe *numpy: Mathematik*).''',
  'import numpy as np\n' + S,
  """plt.scatter(lernzeit, punkte)
m, b = np.polyfit(lernzeit, punkte, 1)
x = np.array([0, 9])
plt.plot(x, m * x + b, color='red')
plt.show()""")
t('''Zeichne 300 zufällige Punkte (`rng.random(300)` für x, danach `rng.random(300)` für y) als kleine schwarze Punkte (`s=10`)
mit der Deckkraft 0.5. Sorge mit `plt.axis('equal')` für gleiche Einheiten.''',
  NPP + '\nrng = np.random.default_rng(3)',
  """x = rng.random(300)
y = rng.random(300)
plt.scatter(x, y, s=10, color='black', alpha=0.5)
plt.axis('equal')
plt.show()""")
t('''Zeichne die Städte als Punkte, deren Größe proportional zur Einwohnerzahl ist (`s = einwohner / 5000`). Schreibe die Namen mit `plt.text()` neben die Punkte (0.2 nach rechts).''',
  PLT + "\nnamen = ['Berlin', 'Hamburg', 'München', 'Köln']\nx = [13.4, 10.0, 11.6, 7.0]\ny = [52.5, 53.6, 48.1, 50.9]\neinwohner = [3700000, 1900000, 1500000, 1100000]",
  """plt.scatter(x, y, s=[e / 5000 for e in einwohner])
for i in range(len(namen)):
    plt.text(x[i] + 0.2, y[i], namen[i])
plt.show()""")
t('''Zeichne zwei Gruppen von Punkten in ein Diagramm: Klasse 9a in Blau, Klasse 9b in Orange, jeweils mit Label und einer Legende.''',
  PLT + '\ngroesse_a = [160, 165, 170, 172, 178]\nsprung_a = [3.6, 3.9, 4.1, 4.3, 4.6]\ngroesse_b = [158, 163, 168, 175, 180]\nsprung_b = [3.8, 4.0, 4.4, 4.5, 4.9]',
  """plt.scatter(groesse_a, sprung_a, color='blue', label='9a')
plt.scatter(groesse_b, sprung_b, color='orange', label='9b')
plt.legend()
plt.show()""")
t('''Zeichne 200 zufällige Punkte im Quadrat von -1 bis 1 (`rng.uniform(-1, 1, size=200)` für x, danach für y). Färbe sie nach ihrem Abstand
vom Ursprung (`c = np.sqrt(x**2 + y**2)`) mit der Farbskala `'plasma'` und zeige eine Farbleiste. Gleiche Einheiten.''',
  NPP + '\nrng = np.random.default_rng(4)',
  """x = rng.uniform(-1, 1, size=200)
y = rng.uniform(-1, 1, size=200)
plt.scatter(x, y, c=np.sqrt(x ** 2 + y ** 2), cmap='plasma')
plt.colorbar()
plt.axis('equal')
plt.show()""")
t('''**Monte-Carlo-π als Bild:** Zeichne 1000 zufällige Punkte im Einheitsquadrat (`rng.random(1000)` für x, danach für y).
Punkte im Viertelkreis (`x² + y² <= 1`) in Rot, die anderen in Grau, Größe 5. Gleiche Einheiten. Gib danach die Schätzung `4 * anteil` aus.''',
  NPP + '\nrng = np.random.default_rng(7)',
  """x = rng.random(1000)
y = rng.random(1000)
innen = x ** 2 + y ** 2 <= 1
plt.scatter(x[innen], y[innen], s=5, color='red')
plt.scatter(x[~innen], y[~innen], s=5, color='gray')
plt.axis('equal')
plt.show()
print(4 * innen.mean())""")
predict("""import matplotlib.pyplot as plt
plt.scatter([1, 2, 3], [3, 1, 2], s=[50, 200, 800])
plt.show()""")

# ---------------------------------------------------------------- 2
sec('Balkendiagramme')
expl('''#### `plt.bar()` und `plt.barh()`

`plt.bar(kategorien, werte)` zeichnet für jede Kategorie einen **senkrechten Balken**. Die Kategorien können Texte sein.
`plt.barh(kategorien, werte)` zeichnet **waagerechte** Balken, das ist bei langen Namen übersichtlicher.

- `color` kann eine Farbe oder eine Liste von Farben (eine pro Balken) sein.
- `width` ist die Breite der Balken (Standard 0.8), bei `barh` heißt es `height`.
- `edgecolor` gibt den Balken einen Rand.
- `plt.bar_label(balken)` schreibt die Werte an die Balken. Dazu speichert man das Ergebnis von `plt.bar()` in einer Variablen.''',
     """import matplotlib.pyplot as plt

faecher = ['Mathe', 'Deutsch', 'Englisch', 'Informatik']
stimmen = [14, 9, 11, 18]
balken = plt.bar(faecher, stimmen, color='skyblue', edgecolor='black')
plt.bar_label(balken)
plt.ylabel('Stimmen')
plt.show()

plt.barh(faecher, stimmen, color=['red', 'green', 'blue', 'orange'])
plt.show()""")

B = PLT + "\ntiere = ['Hund', 'Katze', 'Fisch', 'Vogel', 'Hamster']\nanzahl = [12, 9, 4, 3, 6]"
t('Zeichne ein Balkendiagramm, wie viele Schülerinnen und Schüler welches Haustier haben.', B,
  """plt.bar(tiere, anzahl)
plt.show()""")
t('Zeichne die Balken grün mit schwarzem Rand und dem Titel `Haustiere in der 9a`.', B,
  """plt.bar(tiere, anzahl, color='green', edgecolor='black')
plt.title('Haustiere in der 9a')
plt.show()""")
t('Zeichne die Balken waagerecht.', B,
  """plt.barh(tiere, anzahl)
plt.show()""")
t('Zeichne die Balken und schreibe die Werte mit `plt.bar_label()` an die Balken.', B,
  """balken = plt.bar(tiere, anzahl)
plt.bar_label(balken)
plt.show()""")
t('Zeichne schmale Balken (`width=0.4`) in der Farbe `#e76f51`.', B,
  """plt.bar(tiere, anzahl, width=0.4, color='#e76f51')
plt.show()""")
t('''Zeichne die Balken nach Anzahl sortiert, den größten zuerst. Sortiere dazu Paare aus Anzahl und Tier mit `sorted(..., reverse=True)` und zerlege sie wieder.''', B,
  """paare = sorted(zip(anzahl, tiere), reverse=True)
plt.bar([p[1] for p in paare], [p[0] for p in paare])
plt.show()""")
t('''Färbe den Balken mit dem größten Wert rot und alle anderen grau. Erstelle dazu eine Liste von Farben.''', B,
  """farben = ['red' if a == max(anzahl) else 'gray' for a in anzahl]
plt.bar(tiere, anzahl, color=farben)
plt.show()""")
t('''Zeichne die Temperaturabweichungen der Monate vom Mittelwert als Balken: positive Werte rot, negative blau.
Zeichne eine schwarze Linie bei 0.''',
  PLT + "\nmonate = ['Jan', 'Feb', 'Mär', 'Apr', 'Mai', 'Jun']\nabweichung = [-1.5, 0.8, 2.1, -0.4, 1.2, -2.0]",
  """farben = ['red' if a > 0 else 'blue' for a in abweichung]
plt.bar(monate, abweichung, color=farben)
plt.axhline(0, color='black')
plt.show()""")
t('''Zeichne die Würfelergebnisse als Balkendiagramm der Häufigkeiten: Würfle mit `rng.integers(1, 7, size=60)`, zähle mit `np.bincount(..., minlength=7)[1:]`
und zeichne die Balken über den Augenzahlen 1 bis 6. Zeichne eine rote gestrichelte Linie beim erwarteten Wert 10.''',
  NPP + '\nrng = np.random.default_rng(6)',
  """w = rng.integers(1, 7, size=60)
h = np.bincount(w, minlength=7)[1:]
plt.bar(range(1, 7), h)
plt.axhline(10, color='red', linestyle='--')
plt.show()""")
t('''Zeichne die Länder waagerecht mit ihren Einwohnerzahlen in Millionen, mit `bar_label()` und der x-Achse `Einwohner (Mio.)`.''',
  PLT + "\nlaender = ['Deutschland', 'Frankreich', 'Italien', 'Spanien', 'Polen']\neinwohner = [84.5, 68.4, 58.9, 48.6, 36.6]",
  """balken = plt.barh(laender, einwohner)
plt.bar_label(balken)
plt.xlabel('Einwohner (Mio.)')
plt.show()""")
predict("""import matplotlib.pyplot as plt
plt.bar([1, 2, 3], [3, -1, 2])
plt.bar([4], [5], color='red')
plt.show()""")

# ---------------------------------------------------------------- 3
sec('Gruppierte und gestapelte Balken')
expl('''#### Gruppierte Balken

Für mehrere Werte pro Kategorie stellt man die Balken nebeneinander. Dazu verwendet man Zahlen als x-Positionen (`np.arange()`)
und verschiebt jede Gruppe um eine halbe Balkenbreite. Mit `plt.xticks(positionen, namen)` stehen danach die Namen unter den Gruppen.''',
     """import numpy as np
import matplotlib.pyplot as plt

faecher = ['Mathe', 'Deutsch', 'Englisch']
klasse_a = [2.4, 2.9, 2.1]
klasse_b = [2.8, 2.5, 2.6]
x = np.arange(len(faecher))
b = 0.4
plt.bar(x - b / 2, klasse_a, width=b, label='9a')
plt.bar(x + b / 2, klasse_b, width=b, label='9b')
plt.xticks(x, faecher)
plt.legend()
plt.show()""")
expl('''#### Gestapelte Balken

Mit `bottom=werte` beginnt ein Balken nicht bei 0, sondern auf der Höhe `werte`. So stapelt man Balken übereinander:
Der zweite Balken bekommt als `bottom` die Werte des ersten, der dritte die Summe der ersten beiden.''',
     """import numpy as np
import matplotlib.pyplot as plt

tage = ['Mo', 'Di', 'Mi', 'Do', 'Fr']
bus = np.array([10, 12, 9, 11, 8])
rad = np.array([6, 5, 8, 7, 9])
fuss = np.array([4, 3, 3, 2, 3])
plt.bar(tage, bus, label='Bus')
plt.bar(tage, rad, bottom=bus, label='Rad')
plt.bar(tage, fuss, bottom=bus + rad, label='zu Fuß')
plt.legend()
plt.show()""")

G = NPP + "\nquartale = ['Q1', 'Q2', 'Q3', 'Q4']\nnord = np.array([120, 150, 170, 140])\nsued = np.array([100, 130, 160, 180])"
t('Zeichne die Umsätze von Nord und Süd als gruppierte Balken (Breite 0.4) mit Legende und den Quartalen unter den Gruppen.', G,
  """x = np.arange(len(quartale))
plt.bar(x - 0.2, nord, width=0.4, label='Nord')
plt.bar(x + 0.2, sued, width=0.4, label='Süd')
plt.xticks(x, quartale)
plt.legend()
plt.show()""")
t('Zeichne die Umsätze von Nord und Süd gestapelt mit Legende.', G,
  """plt.bar(quartale, nord, label='Nord')
plt.bar(quartale, sued, bottom=nord, label='Süd')
plt.legend()
plt.show()""")
t('''Zeichne die Umsätze gestapelt und schreibe die Gesamtsumme jedes Quartals über den Stapel (`plt.text()`, 5 über der Summe, mittig).
Setze `plt.ylim(0, 400)`.''', G,
  """plt.bar(quartale, nord, label='Nord')
plt.bar(quartale, sued, bottom=nord, label='Süd')
summe = nord + sued
for i in range(len(quartale)):
    plt.text(i, summe[i] + 5, str(summe[i]), ha='center')
plt.ylim(0, 400)
plt.legend()
plt.show()""")
t('''Zeichne drei Gruppen von Balken nebeneinander (Breite 0.25): die Noten der Klassen 9a, 9b und 9c in den drei Fächern. Mit Legende.''',
  NPP + "\nfaecher = ['Mathe', 'Deutsch', 'Englisch']\nnoten = {'9a': [2.4, 2.9, 2.1], '9b': [2.8, 2.5, 2.6], '9c': [2.2, 2.7, 3.0]}",
  """x = np.arange(len(faecher))
b = 0.25
for i, klasse in enumerate(noten):
    plt.bar(x + (i - 1) * b, noten[klasse], width=b, label=klasse)
plt.xticks(x, faecher)
plt.legend()
plt.show()""")
t('''Zeichne für jede Klasse waagerecht gestapelte Balken (`barh` mit `left=` statt `bottom=`) mit den Anteilen in Prozent für
`gut`, `mittel` und `schlecht`, mit Legende.''',
  NPP + "\nklassen = ['9a', '9b', '9c']\ngut = np.array([40, 55, 30])\nmittel = np.array([45, 30, 50])\nschlecht = np.array([15, 15, 20])",
  """plt.barh(klassen, gut, label='gut')
plt.barh(klassen, mittel, left=gut, label='mittel')
plt.barh(klassen, schlecht, left=gut + mittel, label='schlecht')
plt.legend()
plt.show()""")
t('''Zeichne die Einnahmen und Ausgaben je Monat als gruppierte Balken (Einnahmen grün, Ausgaben rot, Breite 0.4) und zusätzlich den Gewinn
(Einnahmen minus Ausgaben) als schwarze Linie mit Kreis-Markern über den Gruppen. Legende.''',
  NPP + "\nmonate = ['Jan', 'Feb', 'Mär', 'Apr']\neinnahmen = np.array([500, 620, 580, 700])\nausgaben = np.array([450, 480, 600, 520])",
  """x = np.arange(len(monate))
plt.bar(x - 0.2, einnahmen, width=0.4, color='green', label='Einnahmen')
plt.bar(x + 0.2, ausgaben, width=0.4, color='red', label='Ausgaben')
plt.plot(x, einnahmen - ausgaben, 'ko-', label='Gewinn')
plt.xticks(x, monate)
plt.legend()
plt.show()""")
predict("""import matplotlib.pyplot as plt
plt.bar(['A', 'B'], [1, 2])
plt.bar(['A', 'B'], [2, 1], bottom=[1, 2])
plt.show()""")

# ---------------------------------------------------------------- 4
sec('Histogramme')
expl('''#### `plt.hist()`

Ein **Histogramm** zeigt, wie sich viele Zahlenwerte verteilen: Der Wertebereich wird in Klassen (*bins*) eingeteilt,
und für jede Klasse zeigt ein Balken, wie viele Werte hineinfallen.

- `bins=10` teilt den Bereich in 10 gleich breite Klassen. Mit einer Liste wie `bins=[0, 10, 20, 30]` gibt man die Grenzen selbst vor.
- `edgecolor='black'` trennt die Balken sichtbar.
- `density=True` zeigt statt der Anzahlen relative Häufigkeiten (die Flächen ergeben zusammen 1).
- `plt.hist()` gibt die Anzahlen und die Grenzen zurück: `anzahl, grenzen, balken = plt.hist(...)`.''',
     """import numpy as np
import matplotlib.pyplot as plt

rng = np.random.default_rng(1)
groessen = rng.normal(170, 8, size=500)
plt.hist(groessen, bins=20, edgecolor='black')
plt.xlabel('Größe (cm)')
plt.ylabel('Anzahl')
plt.show()

anzahl, grenzen, balken = plt.hist([1, 2, 2, 3, 3, 3, 7], bins=[0, 2, 4, 6, 8], edgecolor='black')
plt.show()
print(anzahl)
print(grenzen)""")

H = NPP + '\nrng = np.random.default_rng(5)\nwerte = rng.normal(50, 10, size=1000)'
t('Zeichne ein Histogramm der 1000 Werte mit 30 Klassen.', H,
  """plt.hist(werte, bins=30)
plt.show()""")
t('Zeichne das Histogramm mit 15 Klassen in Orange mit schwarzem Rand.', H,
  """plt.hist(werte, bins=15, color='orange', edgecolor='black')
plt.show()""")
t('Zeichne das Histogramm mit den Klassengrenzen 0, 10, 20, ..., 100 (`range()`) und schwarzem Rand.', H,
  """plt.hist(werte, bins=range(0, 101, 10), edgecolor='black')
plt.show()""")
t('Zeichne das Histogramm mit den Klassengrenzen aus der vorigen Aufgabe und gib danach die Anzahlen als ganze Zahlen aus.', H,
  """anzahl, grenzen, balken = plt.hist(werte, bins=range(0, 101, 10), edgecolor='black')
plt.show()
print(anzahl.astype(int))""")
t('''Zeichne das Histogramm mit 30 Klassen und `density=True` und darüber die Glockenkurve der Normalverteilung als rote Linie:
`np.exp(-(x - 50)**2 / (2 * 10**2)) / (10 * np.sqrt(2 * np.pi))` für `x` von 10 bis 90 (200 Punkte).''', H,
  """plt.hist(werte, bins=30, density=True, edgecolor='black')
x = np.linspace(10, 90, 200)
plt.plot(x, np.exp(-(x - 50) ** 2 / (2 * 10 ** 2)) / (10 * np.sqrt(2 * np.pi)), color='red')
plt.show()""")
t('''Zeichne das Histogramm mit 30 Klassen und markiere den Mittelwert mit einer roten senkrechten Linie und die Werte Mittelwert ± Standardabweichung
mit grauen gestrichelten Linien.''', H,
  """plt.hist(werte, bins=30)
m = werte.mean()
s = werte.std()
plt.axvline(m, color='red')
plt.axvline(m - s, color='gray', linestyle='--')
plt.axvline(m + s, color='gray', linestyle='--')
plt.show()""")
t('''Vergleiche zwei Verteilungen in einem Diagramm: `a = rng.normal(165, 7, size=500)` (Label `Mädchen`), danach `b = rng.normal(178, 8, size=500)`
(Label `Jungen`). Zeichne beide Histogramme mit den Klassengrenzen 140, 142, ..., 210 (`range(140, 211, 2)`), Deckkraft 0.5 und Legende.''',
  NPP + '\nrng = np.random.default_rng(8)',
  """a = rng.normal(165, 7, size=500)
b = rng.normal(178, 8, size=500)
grenzen = range(140, 211, 2)
plt.hist(a, bins=grenzen, alpha=0.5, label='Mädchen')
plt.hist(b, bins=grenzen, alpha=0.5, label='Jungen')
plt.legend()
plt.show()""")
t('''Simuliere 10000 Würfe mit zwei Würfeln (`rng.integers(1, 7, size=(10000, 2))`) und zeichne ein Histogramm der Augensummen.
Damit jede Summe einen eigenen Balken bekommt, verwende die Grenzen 1.5, 2.5, ..., 12.5 (`np.arange(1.5, 13)`). Schwarzer Rand.''',
  NPP + '\nrng = np.random.default_rng(9)',
  """s = rng.integers(1, 7, size=(10000, 2)).sum(axis=1)
plt.hist(s, bins=np.arange(1.5, 13), edgecolor='black')
plt.show()""")
t('''Zeichne ein Histogramm der Noten mit einem Balken pro Note (Grenzen 0.5 bis 6.5), Breite 0.8 der Balken (`rwidth=0.8`) und den Noten 1 bis 6 als Beschriftung der x-Achse.''',
  PLT + '\nnoten = [2, 3, 1, 4, 2, 5, 3, 2, 2, 3, 1, 4, 3, 2, 6, 3, 2, 4, 3, 1]',
  """plt.hist(noten, bins=[0.5, 1.5, 2.5, 3.5, 4.5, 5.5, 6.5], rwidth=0.8)
plt.xticks(range(1, 7))
plt.show()""")
predict("""import matplotlib.pyplot as plt
anzahl, grenzen, balken = plt.hist([1, 1, 2, 5, 9], bins=[0, 5, 10])
plt.show()
print(anzahl)""")

# ---------------------------------------------------------------- 5
sec('Kreisdiagramme')
expl('''#### `plt.pie()`

Ein **Kreisdiagramm** zeigt Anteile an einem Ganzen. `plt.pie(werte, labels=namen)` teilt den Kreis im Verhältnis der Werte auf.

| Parameter | Bedeutung |
|---|---|
| `labels` | Beschriftung der Stücke |
| `autopct='%1.0f%%'` | schreibt die Prozente in die Stücke (`%1.1f%%` mit einer Nachkommastelle) |
| `colors` | Liste von Farben |
| `explode` | Liste, wie weit jedes Stück herausgerückt wird (z. B. `[0, 0.1, 0]`) |
| `startangle` | Drehung in Grad, z. B. `90`: das erste Stück beginnt oben |
| `counterclock=False` | im Uhrzeigersinn statt gegen den Uhrzeigersinn |

Kreisdiagramme eignen sich nur für wenige Anteile. Bei vielen kleinen Stücken ist ein Balkendiagramm besser lesbar.''',
     """import matplotlib.pyplot as plt

verkehrsmittel = ['Bus', 'Fahrrad', 'zu Fuß', 'Auto']
anzahl = [12, 8, 6, 4]
plt.pie(anzahl, labels=verkehrsmittel, autopct='%1.0f%%')
plt.title('Schulweg')
plt.show()

plt.pie(anzahl, labels=verkehrsmittel, explode=[0.1, 0, 0, 0], startangle=90, counterclock=False,
        colors=['gold', 'yellowgreen', 'lightcoral', 'lightskyblue'])
plt.show()""")

P = PLT + "\nparteien = ['A', 'B', 'C', 'D', 'Sonstige']\nstimmen = [32, 27, 18, 13, 10]"
t('Zeichne ein Kreisdiagramm der Stimmen mit den Parteien als Beschriftung.', P,
  """plt.pie(stimmen, labels=parteien)
plt.show()""")
t('Zeichne das Kreisdiagramm mit Prozentangaben ohne Nachkommastellen und dem Titel `Wahlergebnis`.', P,
  """plt.pie(stimmen, labels=parteien, autopct='%1.0f%%')
plt.title('Wahlergebnis')
plt.show()""")
t('Zeichne das Kreisdiagramm mit Prozentangaben mit einer Nachkommastelle, beginnend oben (`startangle=90`) und im Uhrzeigersinn.', P,
  """plt.pie(stimmen, labels=parteien, autopct='%1.1f%%', startangle=90, counterclock=False)
plt.show()""")
t('Rücke das Stück von Partei A um 0.15 heraus.', P,
  """plt.pie(stimmen, labels=parteien, explode=[0.15, 0, 0, 0, 0])
plt.show()""")
t('''Zeichne das Kreisdiagramm mit den Farben `black`, `red`, `gold`, `green` und `lightgray`.''', P,
  """plt.pie(stimmen, labels=parteien, colors=['black', 'red', 'gold', 'green', 'lightgray'])
plt.show()""")
t('''Zeichne die Zeitverteilung eines Tages als Kreisdiagramm mit Prozenten. Prüfe vorher mit `print()`, ob die Stunden zusammen 24 ergeben.''',
  PLT + "\ntaetigkeiten = ['Schlafen', 'Schule', 'Hausaufgaben', 'Freizeit', 'Essen', 'Sonstiges']\nstunden = [9, 7, 1.5, 4, 1.5, 1]",
  """print(sum(stunden))
plt.pie(stunden, labels=taetigkeiten, autopct='%1.0f%%')
plt.show()""")
t('''Zeichne einen **Ring** statt eines Kreises: `wedgeprops=dict(width=0.4)` macht die Stücke nur 0.4 breit. Mit Prozenten (`pctdistance=0.8`).''', P,
  """plt.pie(stimmen, labels=parteien, autopct='%1.0f%%', pctdistance=0.8, wedgeprops=dict(width=0.4))
plt.show()""")
predict("""import matplotlib.pyplot as plt
plt.pie([1, 1, 2], labels=['a', 'b', 'c'], autopct='%1.0f%%')
plt.show()""")

# ---------------------------------------------------------------- 6
sec('Boxplots')
expl('''#### `plt.boxplot()`

Ein **Boxplot** fasst eine Verteilung in fünf Werten zusammen:

- Die **Box** reicht vom unteren Quartil (25 %) bis zum oberen Quartil (75 %). Darin liegt die mittlere Hälfte der Werte.
- Die Linie in der Box ist der **Median**.
- Die **Antennen** (*whiskers*) reichen bis zum kleinsten und größten Wert, der nicht mehr als das 1,5-Fache der Boxlänge von der Box entfernt ist.
- Werte weiter draußen gelten als **Ausreißer** und werden als einzelne Kreise gezeichnet.

`plt.boxplot([daten1, daten2], tick_labels=['A', 'B'])` zeichnet mehrere Boxplots nebeneinander. So vergleicht man Verteilungen schnell.''',
     """import matplotlib.pyplot as plt

zeiten_a = [12.1, 12.5, 12.8, 13.0, 13.2, 13.5, 14.0, 16.5]
zeiten_b = [11.8, 12.0, 12.4, 12.6, 12.9, 13.1, 13.3, 13.6]
plt.boxplot([zeiten_a, zeiten_b], tick_labels=['Gruppe A', 'Gruppe B'])
plt.ylabel('Zeit (s)')
plt.show()""")

BX = NPP + '\nrng = np.random.default_rng(10)\nklasse_a = rng.normal(70, 10, size=30)\nklasse_b = rng.normal(65, 18, size=30)\nklasse_c = rng.normal(78, 6, size=30)'
t('Zeichne einen Boxplot der Punkte von Klasse A.', BX,
  """plt.boxplot(klasse_a)
plt.show()""")
t('Zeichne die Boxplots der drei Klassen nebeneinander mit den Beschriftungen `A`, `B` und `C`.', BX,
  """plt.boxplot([klasse_a, klasse_b, klasse_c], tick_labels=['A', 'B', 'C'])
plt.show()""")
t('Zeichne die drei Boxplots mit Beschriftungen, Titel `Punkte im Test`, y-Achse `Punkte` und einem waagerechten Gitter (`plt.grid(True, axis=\'y\')`).', BX,
  """plt.boxplot([klasse_a, klasse_b, klasse_c], tick_labels=['A', 'B', 'C'])
plt.title('Punkte im Test')
plt.ylabel('Punkte')
plt.grid(True, axis='y')
plt.show()""")
t('''Zeichne die drei Boxplots mit Beschriftungen und gefüllten Boxen (`patch_artist=True`). Gib danach für jede Klasse den Median mit einer Nachkommastelle aus.''', BX,
  """plt.boxplot([klasse_a, klasse_b, klasse_c], tick_labels=['A', 'B', 'C'], patch_artist=True)
plt.show()
for k in [klasse_a, klasse_b, klasse_c]:
    print(np.round(np.median(k), 1))""")
t('''Zeichne den Boxplot der Laufzeiten. Eine Zeit ist ein Ausreißer. Gib danach Median, unteres und oberes Quartil aus (`np.percentile()`).''',
  NPP + '\nzeiten = np.array([12.4, 11.9, 13.1, 12.0, 12.7, 17.8, 12.2, 11.6, 12.9, 12.5])',
  """plt.boxplot(zeiten)
plt.show()
print(np.percentile(zeiten, [25, 50, 75]))""")
t('''Zeichne die drei Boxplots waagerecht (`orientation='horizontal'`) mit Beschriftungen.''', BX,
  """plt.boxplot([klasse_a, klasse_b, klasse_c], tick_labels=['A', 'B', 'C'], orientation='horizontal')
plt.show()""")
predict("""import matplotlib.pyplot as plt
plt.boxplot([[1, 2, 3, 4, 5], [1, 2, 3, 4, 20]], tick_labels=['ohne', 'mit'])
plt.show()""")

# ---------------------------------------------------------------- 7
sec('Fehlerbalken, Flächen und Stufen')
expl('''#### Fehlerbalken und Flächen

- `plt.errorbar(x, y, yerr=fehler, capsize=4)` zeichnet Messwerte mit **Fehlerbalken**. `yerr` kann eine Zahl oder ein Array sein,
  `capsize` zeichnet kleine Querstriche an die Enden. Mit `fmt='o'` erscheinen nur Punkte ohne Verbindungslinie.
- `plt.fill_between(x, y1, y2)` färbt die Fläche zwischen zwei Kurven. Ohne `y2` wird bis zur x-Achse gefärbt.
  Mit `alpha` wird sie durchsichtig. Mit `where=bedingung` nur dort, wo die Bedingung gilt.''',
     """import numpy as np
import matplotlib.pyplot as plt

x = [1, 2, 3, 4, 5]
y = [2.1, 3.9, 6.2, 7.8, 10.1]
plt.errorbar(x, y, yerr=0.5, fmt='o', capsize=4)
plt.show()

x = np.linspace(0, 2, 100)
plt.plot(x, x ** 2)
plt.fill_between(x, x ** 2, alpha=0.3)
plt.show()""")
expl('''#### Stufendiagramme

`plt.step(x, y, where='post')` zeichnet eine **Treppe**: Der Wert bleibt gleich bis zum nächsten x-Wert und springt dann.
Das passt für Größen, die sich nur zu bestimmten Zeitpunkten ändern (Preise, Tarife, Kontostand).''',
     """import matplotlib.pyplot as plt

tage = [0, 3, 5, 9, 12]
kontostand = [100, 60, 150, 120, 120]
plt.step(tage, kontostand, where='post')
plt.show()""")

t('''Zeichne die Messwerte mit Fehlerbalken: Punkte ohne Linie, Fehler aus dem Array `fehler`, Querstriche der Breite 5.''',
  PLT + '\nx = [10, 20, 30, 40, 50]\ny = [3.2, 5.1, 6.8, 9.2, 10.9]\nfehler = [0.3, 0.4, 0.3, 0.6, 0.5]',
  """plt.errorbar(x, y, yerr=fehler, fmt='o', capsize=5)
plt.show()""")
t('''Zeichne für jeden Monat den Mittelwert der Temperatur als Balken mit der Standardabweichung als Fehlerbalken (`plt.bar(..., yerr=..., capsize=4)`).''',
  PLT + "\nmonate = ['Jan', 'Apr', 'Jul', 'Okt']\nmittel = [1.5, 9.8, 19.2, 10.4]\nstreuung = [2.1, 2.8, 2.5, 2.3]",
  """plt.bar(monate, mittel, yerr=streuung, capsize=4)
plt.show()""")
t('Zeichne `sin(x)` von 0 bis π (100 Punkte) und färbe die Fläche darunter grün mit der Deckkraft 0.4.', NPP,
  """x = np.linspace(0, np.pi, 100)
plt.plot(x, np.sin(x), color='green')
plt.fill_between(x, np.sin(x), color='green', alpha=0.4)
plt.show()""")
t('''Zeichne `x` und `x²` von 0 bis 1 (100 Punkte) mit Legende und färbe die Fläche zwischen den Kurven orange (Deckkraft 0.3).''', NPP,
  """x = np.linspace(0, 1, 100)
plt.plot(x, x, label='x')
plt.plot(x, x ** 2, label='x²')
plt.fill_between(x, x, x ** 2, color='orange', alpha=0.3)
plt.legend()
plt.show()""")
t('''Zeichne `sin(x)` von 0 bis 2π (200 Punkte). Färbe die Flächen, wo `sin(x) > 0` ist, blau und wo `sin(x) < 0` ist, rot (Deckkraft 0.3, `where=`).''', NPP,
  """x = np.linspace(0, 2 * np.pi, 200)
y = np.sin(x)
plt.plot(x, y, color='black')
plt.fill_between(x, y, where=y > 0, color='blue', alpha=0.3)
plt.fill_between(x, y, where=y < 0, color='red', alpha=0.3)
plt.show()""")
t('''Zeichne die Temperaturen der Woche: das Tagesmittel als Linie und den Bereich zwischen Tiefst- und Höchstwert als hellblaue Fläche (Deckkraft 0.5).
Beschrifte die x-Achse mit den Tagen.''',
  NPP + "\ntage = ['Mo', 'Di', 'Mi', 'Do', 'Fr', 'Sa', 'So']\ntmin = np.array([4.5, 6.0, 3.5, 2.0, 5.5, 7.0, 6.5])\ntmax = np.array([11.0, 13.5, 9.0, 8.5, 14.0, 16.5, 12.0])",
  """x = np.arange(7)
plt.fill_between(x, tmin, tmax, color='lightblue', alpha=0.5)
plt.plot(x, (tmin + tmax) / 2)
plt.xticks(x, tage)
plt.show()""")
t('''Zeichne die Portokosten als Stufendiagramm (`where='post'`): bis 20 g 0.95 Euro, bis 50 g 1.10 Euro, bis 500 g 1.80 Euro, bis 1000 g 2.90 Euro.
Verwende die x-Werte `[0, 20, 50, 500, 1000]` und die y-Werte `[0.95, 1.10, 1.80, 2.90, 2.90]`. Achsen: `Gewicht (g)` und `Preis (Euro)`.''', PLT,
  """plt.step([0, 20, 50, 500, 1000], [0.95, 1.10, 1.80, 2.90, 2.90], where='post')
plt.xlabel('Gewicht (g)')
plt.ylabel('Preis (Euro)')
plt.show()""")
t('''Zeichne den Kontostand nach den Buchungen als Stufendiagramm mit Kreis-Markern: Start 100 Euro am Tag 0, die Buchungen an den Tagen in `tage`.
Berechne die Stände mit `np.cumsum()`.''',
  NPP + '\ntage = [0, 2, 5, 9, 14, 20]\nbuchungen = [100, -30, 80, -50, -20, 60]',
  """stand = np.cumsum(buchungen)
plt.step(tage, stand, where='post', marker='o')
plt.show()""")

# ---------------------------------------------------------------- 8
sec('Daten aus Dateien')
expl('''#### Daten einlesen und darstellen

Meist kommen die Daten aus Dateien. Die Setup-Zelle am Anfang hat drei Dateien angelegt.
Mit `np.loadtxt()` liest man sie ein (siehe *numpy: Mathematik*): Zahlenspalten normal, Textspalten mit `dtype=str`.''',
     """import numpy as np
import matplotlib.pyplot as plt

faecher = np.loadtxt('umfrage.csv', delimiter=';', skiprows=1, usecols=0, dtype=str, encoding='utf-8')
stimmen = np.loadtxt('umfrage.csv', delimiter=';', skiprows=1, usecols=1, encoding='utf-8')
print(faecher)
print(stimmen)
plt.bar(faecher, stimmen)
plt.show()""")

U = NPP + "\nfaecher = np.loadtxt('umfrage.csv', delimiter=';', skiprows=1, usecols=0, dtype=str, encoding='utf-8')\nstimmen = np.loadtxt('umfrage.csv', delimiter=';', skiprows=1, usecols=1, encoding='utf-8')"
t('Zeichne die Umfrage als waagerechte Balken, nach Stimmen sortiert (der größte Balken oben). Tipp: `argsort()`.', U,
  """r = stimmen.argsort()
plt.barh(faecher[r], stimmen[r])
plt.show()""")
t('Zeichne die Umfrage als Kreisdiagramm mit Prozenten.', U,
  """plt.pie(stimmen, labels=faecher, autopct='%1.0f%%')
plt.show()""")
SP = NPP + "\ngroesse, weite = np.loadtxt('sport.csv', delimiter=',', skiprows=1, usecols=(1, 2), unpack=True, encoding='utf-8')\nklasse = np.loadtxt('sport.csv', delimiter=',', skiprows=1, usecols=3, dtype=str, encoding='utf-8')"
t('Zeichne ein Streudiagramm von Größe und Weitsprungweite aus `sport.csv` mit Achsenbeschriftungen `Größe (cm)` und `Weite (m)`.', SP,
  """plt.scatter(groesse, weite)
plt.xlabel('Größe (cm)')
plt.ylabel('Weite (m)')
plt.show()""")
t('Zeichne das Streudiagramm mit den Klassen 9a und 9b in verschiedenen Farben (Masken) und einer Legende.', SP,
  """for k in ['9a', '9b']:
    plt.scatter(groesse[klasse == k], weite[klasse == k], label=k)
plt.legend()
plt.show()""")
t('Zeichne Boxplots der Weitsprungweiten beider Klassen nebeneinander.', SP,
  """plt.boxplot([weite[klasse == '9a'], weite[klasse == '9b']], tick_labels=['9a', '9b'])
plt.show()""")
VK = NPP + "\nmonate = np.loadtxt('verkauf.csv', delimiter=',', skiprows=1, usecols=0, dtype=str, encoding='utf-8')\neis, kakao = np.loadtxt('verkauf.csv', delimiter=',', skiprows=1, usecols=(1, 2), unpack=True, encoding='utf-8')"
t('Zeichne den Verkauf von Eis und Kakao über die Monate als Linien mit Kreis-Markern und Legende.', VK,
  """plt.plot(monate, eis, marker='o', label='Eis')
plt.plot(monate, kakao, marker='o', label='Kakao')
plt.legend()
plt.show()""")
t('Zeichne den Verkauf als gruppierte Balken (Breite 0.4) mit den Monaten unter den Gruppen und Legende.', VK,
  """x = np.arange(len(monate))
plt.bar(x - 0.2, eis, width=0.4, label='Eis')
plt.bar(x + 0.2, kakao, width=0.4, label='Kakao')
plt.xticks(x, monate)
plt.legend()
plt.show()""")
t('Zeichne ein Streudiagramm von Eis- und Kakaoverkäufen und gib den Korrelationskoeffizienten auf drei Nachkommastellen aus.', VK,
  """plt.scatter(eis, kakao)
plt.xlabel('Eis')
plt.ylabel('Kakao')
plt.show()
print(np.round(np.corrcoef(eis, kakao)[0, 1], 3))""")

# ---------------------------------------------------------------- 9
sec('Gemischte Übungen')
t('''Simuliere 1000 Münzwürfe (`rng.integers(0, 2, size=1000)`) und zeichne den Anteil der Köpfe nach jedem Wurf (`cumsum()` durch `np.arange(1, 1001)`)
als Linie. Zeichne eine rote gestrichelte Linie bei 0.5 und setze `plt.ylim(0, 1)`. Achsen: `Anzahl Würfe` und `Anteil Kopf`.''',
  NPP + '\nrng = np.random.default_rng(12)',
  """m = rng.integers(0, 2, size=1000)
anteil = m.cumsum() / np.arange(1, 1001)
plt.plot(np.arange(1, 1001), anteil)
plt.axhline(0.5, color='red', linestyle='--')
plt.ylim(0, 1)
plt.xlabel('Anzahl Würfe')
plt.ylabel('Anteil Kopf')
plt.show()""")
t('''Zeichne fünf Irrfahrten mit je 200 Schritten (`rng.choice([-1, 1], size=(5, 200))`, `cumsum(axis=1)`) als Linien in ein Diagramm
und eine schwarze Linie bei 0.''',
  NPP + '\nrng = np.random.default_rng(13)',
  """wege = rng.choice([-1, 1], size=(5, 200)).cumsum(axis=1)
for weg in wege:
    plt.plot(weg)
plt.axhline(0, color='black')
plt.show()""")
t('''Zeichne die Notenverteilung einer Klassenarbeit als Balkendiagramm mit den Noten 1 bis 6 als Beschriftung und den Anzahlen über den Balken (`bar_label`).
Färbe die Balken der Noten 5 und 6 rot, die anderen grün. Gib danach den Durchschnitt mit zwei Nachkommastellen aus.''',
  NPP + '\nnoten = np.array([2, 3, 1, 4, 2, 5, 3, 2, 2, 3, 1, 4, 3, 2, 6, 3, 2, 4, 3, 1, 5, 3])',
  """h = np.bincount(noten, minlength=7)[1:]
farben = ['green', 'green', 'green', 'green', 'red', 'red']
balken = plt.bar(range(1, 7), h, color=farben)
plt.bar_label(balken)
plt.xticks(range(1, 7))
plt.show()
print(np.round(noten.mean(), 2))""")
t('''Stelle dieselben Daten auf drei Arten dar, jeweils in einem eigenen Diagramm der Größe 4 × 3: als Balken, als Kreis (mit Prozenten) und als waagerechte Balken.''',
  PLT + "\nsprachen = ['Python', 'Java', 'C++', 'JavaScript']\nanteil = [45, 25, 10, 20]",
  """plt.figure(figsize=(4, 3))
plt.bar(sprachen, anteil)
plt.show()
plt.figure(figsize=(4, 3))
plt.pie(anteil, labels=sprachen, autopct='%1.0f%%')
plt.show()
plt.figure(figsize=(4, 3))
plt.barh(sprachen, anteil)
plt.show()""")
t('''Zeichne die Bevölkerungspyramide: Männer als Balken nach links (negative Werte, `barh`), Frauen nach rechts, mit Legende und einer schwarzen Linie bei 0.''',
  NPP + "\nalter = ['0-19', '20-39', '40-59', '60-79', '80+']\nmaenner = np.array([7.6, 9.8, 11.5, 8.4, 2.3])\nfrauen = np.array([7.2, 9.4, 11.3, 9.3, 3.8])",
  """plt.barh(alter, -maenner, label='Männer')
plt.barh(alter, frauen, label='Frauen')
plt.axvline(0, color='black')
plt.legend()
plt.show()""")
t('''Zeichne zufällig verteilte Punkte mit einem Zusammenhang: `x = rng.uniform(0, 10, size=60)`, danach `y = 2 * x + rng.normal(0, 3, size=60)`.
Zeichne die Punkte, die Regressionsgerade in Rot und färbe den Bereich ± 3 um die Gerade grau (Deckkraft 0.2) für x von 0 bis 10.''',
  NPP + '\nrng = np.random.default_rng(14)',
  """x = rng.uniform(0, 10, size=60)
y = 2 * x + rng.normal(0, 3, size=60)
plt.scatter(x, y)
m, b = np.polyfit(x, y, 1)
xg = np.array([0, 10])
plt.plot(xg, m * xg + b, color='red')
plt.fill_between(xg, m * xg + b - 3, m * xg + b + 3, color='gray', alpha=0.2)
plt.show()""")
t('Stelle selbst gewählte Daten (z. B. eine Umfrage in deiner Klasse) mit einem passenden Diagrammtyp dar.', NPP,
  """lieblingsessen = ['Pizza', 'Nudeln', 'Döner', 'Salat']
stimmen = [10, 7, 6, 3]
plt.bar(lieblingsessen, stimmen)
plt.show()""", kind='free')

generate('matplotlib_diagrammtypen', 'matplotlib: Diagrammtypen', INTRO)
