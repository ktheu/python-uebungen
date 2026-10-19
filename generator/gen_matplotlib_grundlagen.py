# Erzeugt ../content/matplotlib_grundlagen.ipynb (siehe nbgen.py).
#
# Braucht matplotlib und numpy in denselben Versionen wie Pyodide in JupyterLite (zurzeit matplotlib 3.10.8, numpy 2.4.6):
#     py -3.13 -m pip install numpy==2.4.6 matplotlib==3.10.8
#     py -3.13 -W error generator/gen_matplotlib_grundlagen.py
#     py -3.13 generator/pyodide_check/pruefen.py generator/gen_matplotlib_grundlagen.py
#
# Die erwarteten Diagramme erzeugt nbgen.run_mit_bildern(): Jede Musterlösung wird ausgeführt, alle offenen Diagramme
# werden als PNG (72 dpi) an die Aufgabenzelle angehängt. Die Aufgabentexte müssen deshalb genau sagen, was gezeichnet wird.
# Nur pyplot-Schreibweise (plt.plot ...); fig, ax kommt erst in matplotlib_layout, scatter/bar/hist in matplotlib_diagrammtypen.
from nbgen import sec, expl, task, predict, generate


def t(text, given='', body='', kind='normal'):
    """Aufgabe, deren Lösung aus dem vorgegebenen Code plus body besteht."""
    task(text, given=given, solution=(given + '\n' + body) if given else body, kind=kind)


PLT = 'import matplotlib.pyplot as plt'
NPP = 'import numpy as np\nimport matplotlib.pyplot as plt'

INTRO = '''**matplotlib** ist das bekannteste Python-Paket zum Zeichnen von **Diagrammen**. In diesem Notebook geht es um
Liniendiagramme und Funktionsgraphen: Punkte verbinden, Funktionen zeichnen, Farben und Linien wählen, Diagramme beschriften
und Achsen einstellen.

Vorausgesetzt wird das Notebook *numpy: Grundlagen* (für `np.linspace()` und das Rechnen mit Arrays).
Weitere Notebooks behandeln andere Diagrammtypen (Balken, Histogramme, ...) und mehrere Diagramme nebeneinander.

Jeder Abschnitt beginnt mit kurzen Erklärungen und Beispielen. Führe die Beispiele aus und probiere sie ruhig ein wenig aus.
Danach folgen viele kleine Übungen. Unter den meisten Aufgaben siehst du das **erwartete Diagramm**. Zeichne es nach und vergleiche.
Dein Diagramm wird etwas größer angezeigt, sonst sollte es genauso aussehen.

Beim ersten `import matplotlib` wird matplotlib in den Browser geladen. Das dauert ein paar Sekunden.'''

# ---------------------------------------------------------------- 1
sec('Das erste Diagramm')
expl('''#### `plt.plot()` und `plt.show()`

matplotlib importiert man fast immer so: `import matplotlib.pyplot as plt`. Das Modul `pyplot` enthält die Zeichenbefehle.

- `plt.plot(x, y)` zeichnet die Punkte mit den x-Werten aus `x` und den y-Werten aus `y` und **verbindet** sie mit Linien.
  `x` und `y` können Listen oder numpy-Arrays sein und müssen gleich lang sein.
- `plt.show()` zeigt das Diagramm an. Schreibe es immer als letzte Zeile.

Jede Zelle zeichnet ein neues Diagramm. Die Achsen werden automatisch so eingeteilt, dass alle Punkte zu sehen sind.''',
     """import matplotlib.pyplot as plt

x = [1, 2, 3, 4, 5]
y = [2, 4, 3, 5, 1]
plt.plot(x, y)
plt.show()""")
expl('''#### Nur y-Werte

Gibt man nur **eine** Liste an, `plt.plot(y)`, verwendet matplotlib als x-Werte die Indizes 0, 1, 2, ...
Das ist praktisch für Messreihen, bei denen nur die Reihenfolge zählt.''',
     """import matplotlib.pyplot as plt

temperaturen = [12, 15, 14, 18, 21, 19, 16]
plt.plot(temperaturen)
plt.show()""")

t('Zeichne die Punkte (0, 0), (1, 1), (2, 4), (3, 9) und (4, 16) verbunden.',
  PLT, """x = [0, 1, 2, 3, 4]
y = [0, 1, 4, 9, 16]
plt.plot(x, y)
plt.show()""")
t('Zeichne den Kontostand. Gib nur die y-Werte an.',
  PLT + '\nkontostand = [100, 120, 90, 150, 170, 140, 200]',
  """plt.plot(kontostand)
plt.show()""")
t('Zeichne die Gerade `y = 2x + 1` für die ganzen Zahlen x von -3 bis 3. Erzeuge die Werte mit numpy.',
  NPP, """x = np.arange(-3, 4)
y = 2 * x + 1
plt.plot(x, y)
plt.show()""")
t('Zeichne eine Strecke vom Punkt (1, 1) zum Punkt (4, 3).',
  PLT, """plt.plot([1, 4], [1, 3])
plt.show()""")
t('Zeichne das Dreieck mit den Ecken A(0, 0), B(4, 0) und C(1, 3). Damit es geschlossen ist, muss der letzte Punkt wieder A sein.',
  PLT, """plt.plot([0, 4, 1, 0], [0, 0, 3, 0])
plt.show()""")
t('''Zeichne das **Haus vom Nikolaus** in einem Zug durch die Punkte (0, 0), (2, 0), (0, 2), (2, 2), (1, 3), (0, 2), (0, 0), (2, 2), (2, 0).''',
  PLT, """x = [0, 2, 0, 2, 1, 0, 0, 2, 2]
y = [0, 0, 2, 2, 3, 2, 0, 2, 0]
plt.plot(x, y)
plt.show()""")
t('Zeichne die Werte des Arrays `quadrate` (die Quadratzahlen von 1 bis 10) über den Zahlen 1 bis 10.',
  NPP + '\nn = np.arange(1, 11)\nquadrate = n ** 2',
  """plt.plot(n, quadrate)
plt.show()""")
t('Denke dir sieben Messwerte aus (z. B. deine Schlafdauer an den Tagen einer Woche) und zeichne sie.',
  PLT, """schlaf = [8, 7.5, 6, 7, 8.5, 9, 9.5]
plt.plot(schlaf)
plt.show()""", kind='free')
predict("""import matplotlib.pyplot as plt
plt.plot([3, 1, 2])
plt.show()""")

# ---------------------------------------------------------------- 2
sec('Funktionsgraphen')
expl('''#### Funktionen mit `np.linspace()` zeichnen

Für einen glatten Graphen braucht man **viele** x-Werte. `np.linspace(a, b, 100)` liefert 100 Werte von `a` bis `b`.
Mit numpy berechnet man dann alle y-Werte auf einmal, z. B. `y = x ** 2`.

Mit wenigen Punkten sieht der Graph eckig aus, weil matplotlib die Punkte nur mit geraden Linien verbindet.''',
     """import numpy as np
import matplotlib.pyplot as plt

x = np.linspace(-3, 3, 100)
plt.plot(x, x ** 2)
plt.show()

x = np.linspace(-3, 3, 5)
plt.plot(x, x ** 2)
plt.show()""")
expl('''#### Mehrere Graphen in einem Diagramm

Ruft man `plt.plot()` mehrmals vor `plt.show()` auf, landen alle Graphen im **selben** Diagramm.
matplotlib gibt ihnen automatisch verschiedene Farben: zuerst Blau, dann Orange, Grün, Rot, ...''',
     """import numpy as np
import matplotlib.pyplot as plt

x = np.linspace(0, 2 * np.pi, 200)
plt.plot(x, np.sin(x))
plt.plot(x, np.cos(x))
plt.show()""")

t('Zeichne den Graphen von `f(x) = x²` im Bereich von -3 bis 3 mit 100 Punkten.',
  NPP, """x = np.linspace(-3, 3, 100)
plt.plot(x, x ** 2)
plt.show()""")
t('Zeichne denselben Graphen mit nur 7 Punkten.',
  NPP, """x = np.linspace(-3, 3, 7)
plt.plot(x, x ** 2)
plt.show()""")
t('Zeichne `sin(x)` von 0 bis 2π (200 Punkte).',
  NPP, """x = np.linspace(0, 2 * np.pi, 200)
plt.plot(x, np.sin(x))
plt.show()""")
t('Zeichne `f(x) = x³ - 3x` von -2.5 bis 2.5 (200 Punkte).',
  NPP, """x = np.linspace(-2.5, 2.5, 200)
plt.plot(x, x ** 3 - 3 * x)
plt.show()""")
t('Zeichne die drei Parabeln `x²`, `2x²` und `0.5x²` von -2 bis 2 in ein Diagramm (in dieser Reihenfolge, 100 Punkte).',
  NPP, """x = np.linspace(-2, 2, 100)
plt.plot(x, x ** 2)
plt.plot(x, 2 * x ** 2)
plt.plot(x, 0.5 * x ** 2)
plt.show()""")
t('Zeichne die Exponentialfunktion `2^x` von -2 bis 4 (100 Punkte).',
  NPP, """x = np.linspace(-2, 4, 100)
plt.plot(x, 2 ** x)
plt.show()""")
t('Zeichne `f(x) = 1/x` von 0.1 bis 5 (200 Punkte).',
  NPP, """x = np.linspace(0.1, 5, 200)
plt.plot(x, 1 / x)
plt.show()""")
t('Zeichne die Betragsfunktion `|x|` von -4 bis 4 mit 9 Punkten. Dann ist 0 einer der Punkte und der Knick liegt genau bei 0.',
  NPP, """x = np.linspace(-4, 4, 9)
plt.plot(x, np.abs(x))
plt.show()""")
t('Zeichne mit einer Schleife die Geraden `y = a · x` für `a` = 1, 2, 3 und 4 von 0 bis 5 in ein Diagramm.',
  NPP, """x = np.linspace(0, 5, 2)
for a in range(1, 5):
    plt.plot(x, a * x)
plt.show()""")
t('Zeichne die Gerade `y = 0.5x - 1` und die Parabel `y = x² - 3` von -3 bis 3 in ein Diagramm (zuerst die Gerade, 100 Punkte).',
  NPP, """x = np.linspace(-3, 3, 100)
plt.plot(x, 0.5 * x - 1)
plt.plot(x, x ** 2 - 3)
plt.show()""")
t('Zeichne `sin(x)`, `sin(2x)` und `sin(3x)` von 0 bis 2π in ein Diagramm (300 Punkte).',
  NPP, """x = np.linspace(0, 2 * np.pi, 300)
for k in [1, 2, 3]:
    plt.plot(x, np.sin(k * x))
plt.show()""")
t('Zeichne den Graphen einer Funktion deiner Wahl.',
  NPP, """x = np.linspace(-5, 5, 200)
plt.plot(x, np.sin(x) * x)
plt.show()""", kind='free')
predict("""import numpy as np
import matplotlib.pyplot as plt
x = np.linspace(-1, 1, 3)
plt.plot(x, x ** 2)
plt.plot(x, -x)
plt.show()""")

# ---------------------------------------------------------------- 3
sec('Farben, Linien und Marker')
expl('''#### Aussehen der Linie

`plt.plot()` hat viele Parameter für das Aussehen:

| Parameter | Bedeutung | Beispiele |
|---|---|---|
| `color` | Farbe | `'red'`, `'green'`, `'black'`, `'gray'`, `'orange'`, `'#ff8800'` |
| `linestyle` | Linienart | `'-'` durchgezogen, `'--'` gestrichelt, `':'` gepunktet, `'-.'` Strich-Punkt, `''` keine Linie |
| `linewidth` | Liniendicke | `1`, `3`, `0.5` |
| `marker` | Punkt-Symbol | `'o'` Kreis, `'s'` Quadrat, `'^'` Dreieck, `'x'` Kreuz, `'*'` Stern, `'.'` kleiner Punkt |
| `markersize` | Größe der Symbole | `5`, `10` |

Farben kann man mit englischen Namen oder als Hex-Code `'#rrggbb'` angeben.''',
     """import matplotlib.pyplot as plt

x = [1, 2, 3, 4, 5]
plt.plot(x, [1, 2, 3, 4, 5], color='red', linestyle='--')
plt.plot(x, [2, 3, 4, 5, 6], color='green', linewidth=4)
plt.plot(x, [3, 4, 5, 6, 7], color='#8800cc', marker='o', markersize=10)
plt.plot(x, [4, 5, 6, 7, 8], color='black', linestyle='', marker='s')
plt.show()""")
expl('''#### Kurzschreibweise

Farbe, Marker und Linienart kann man auch in **einer** Zeichenkette als drittes Argument angeben:
`'r--'` ist rot gestrichelt, `'go'` sind grüne Kreise ohne Linie, `'b^:'` sind blaue Dreiecke mit gepunkteter Linie.
Die Kurzzeichen für Farben sind `b` (blau), `g` (grün), `r` (rot), `c` (cyan), `m` (magenta), `y` (gelb), `k` (schwarz).''',
     """import matplotlib.pyplot as plt

x = [1, 2, 3, 4, 5]
plt.plot(x, [1, 2, 3, 4, 5], 'r--')
plt.plot(x, [2, 3, 4, 5, 6], 'go')
plt.plot(x, [3, 4, 5, 6, 7], 'b^:')
plt.plot(x, [4, 5, 6, 7, 8], 'ks-')
plt.show()""")

D = PLT + '\ntage = [1, 2, 3, 4, 5, 6, 7]\nwerte = [3, 5, 4, 7, 6, 8, 7]'
t('Zeichne die Werte als rote, gestrichelte Linie. Verwende `color` und `linestyle`.', D,
  """plt.plot(tage, werte, color='red', linestyle='--')
plt.show()""")
t('Zeichne die Werte als grüne Kreise **ohne** Linie. Verwende die Kurzschreibweise.', D,
  """plt.plot(tage, werte, 'go')
plt.show()""")
t('Zeichne die Werte als schwarze Linie mit quadratischen Markern.', D,
  """plt.plot(tage, werte, color='black', marker='s')
plt.show()""")
t('Zeichne die Werte als orange Linie mit der Dicke 5.', D,
  """plt.plot(tage, werte, color='orange', linewidth=5)
plt.show()""")
t('Zeichne die Werte als graue, gepunktete Linie mit großen Sternen (`marker=\'*\'`, `markersize=15`).', D,
  """plt.plot(tage, werte, color='gray', linestyle=':', marker='*', markersize=15)
plt.show()""")
t('Zeichne die Werte mit der Farbe `#2a9d8f` und Dreiecks-Markern.', D,
  """plt.plot(tage, werte, color='#2a9d8f', marker='^')
plt.show()""")
t('Zeichne `x²` von -2 bis 2 als blaue Linie (100 Punkte) und zusätzlich die ganzzahligen Punkte von -2 bis 2 als rote Kreise.', NPP,
  """x = np.linspace(-2, 2, 100)
plt.plot(x, x ** 2, 'b')
xp = np.arange(-2, 3)
plt.plot(xp, xp ** 2, 'ro')
plt.show()""")
t('Zeichne `sin(x)` von 0 bis 2π als durchgezogene schwarze Linie und `cos(x)` als rote Strich-Punkt-Linie (200 Punkte).', NPP,
  """x = np.linspace(0, 2 * np.pi, 200)
plt.plot(x, np.sin(x), 'k-')
plt.plot(x, np.cos(x), 'r-.')
plt.show()""")
t('Zeichne die Werte als dünne blaue Linie (Dicke 0.5) mit großen, magentafarbenen Kreisen. Für die Farbe der Marker gibt es `markerfacecolor`.', D,
  """plt.plot(tage, werte, color='blue', linewidth=0.5, marker='o', markersize=12, markerfacecolor='magenta')
plt.show()""")
t('Zeichne mit einer Schleife 5 waagerechte Linien `y = k` für `k` von 1 bis 5 von x = 0 bis x = 10, jede dicker als die vorige (`linewidth=k`), alle schwarz.', PLT,
  """for k in range(1, 6):
    plt.plot([0, 10], [k, k], color='black', linewidth=k)
plt.show()""")
predict("""import matplotlib.pyplot as plt
plt.plot([1, 2, 3], [1, 2, 1], 'rs')
plt.plot([1, 2, 3], [2, 1, 2], 'k:')
plt.show()""")

# ---------------------------------------------------------------- 4
sec('Beschriften')
expl('''#### Titel, Achsen und Gitter

- `plt.title('...')`: Überschrift
- `plt.xlabel('...')` und `plt.ylabel('...')`: Beschriftung der Achsen. Zu einer guten Beschriftung gehört die **Einheit**.
- `plt.grid(True)`: ein Gitter im Hintergrund, damit man Werte besser ablesen kann

Alle Befehle stehen zwischen `plt.plot()` und `plt.show()`.''',
     """import matplotlib.pyplot as plt

stunden = [8, 10, 12, 14, 16, 18]
temperatur = [12, 15, 19, 21, 20, 17]
plt.plot(stunden, temperatur, marker='o')
plt.title('Temperatur am 14. Mai')
plt.xlabel('Uhrzeit (h)')
plt.ylabel('Temperatur (°C)')
plt.grid(True)
plt.show()""")
expl('''#### Legende

Gibt man jedem Graphen mit `label='...'` einen Namen, zeigt `plt.legend()` eine **Legende** mit diesen Namen an.
Mit `plt.legend(loc='upper left')` legt man fest, wo sie steht (`'upper right'`, `'lower left'`, `'lower right'`, `'center'`, ...).
Ohne Angabe sucht matplotlib eine Stelle, an der sie nicht stört.''',
     """import numpy as np
import matplotlib.pyplot as plt

x = np.linspace(0, 2 * np.pi, 200)
plt.plot(x, np.sin(x), label='sin(x)')
plt.plot(x, np.cos(x), label='cos(x)')
plt.legend(loc='lower left')
plt.show()""")

W = PLT + "\njahre = [2019, 2020, 2021, 2022, 2023, 2024]\nschueler = [820, 845, 870, 860, 905, 930]"
t('Zeichne die Schülerzahlen mit Kreis-Markern und dem Titel `Schülerzahlen`.', W,
  """plt.plot(jahre, schueler, marker='o')
plt.title('Schülerzahlen')
plt.show()""")
t('Zeichne die Schülerzahlen und beschrifte die x-Achse mit `Jahr` und die y-Achse mit `Anzahl`.', W,
  """plt.plot(jahre, schueler)
plt.xlabel('Jahr')
plt.ylabel('Anzahl')
plt.show()""")
t('Zeichne die Schülerzahlen mit Titel, beiden Achsenbeschriftungen (wie in den vorigen Aufgaben) und einem Gitter.', W,
  """plt.plot(jahre, schueler, marker='o')
plt.title('Schülerzahlen')
plt.xlabel('Jahr')
plt.ylabel('Anzahl')
plt.grid(True)
plt.show()""")
t('Zeichne `x`, `x²` und `x³` von 0 bis 2 (100 Punkte) mit den Labels `x`, `x²` und `x³` und einer Legende.', NPP,
  """x = np.linspace(0, 2, 100)
plt.plot(x, x, label='x')
plt.plot(x, x ** 2, label='x²')
plt.plot(x, x ** 3, label='x³')
plt.legend()
plt.show()""")
t('''Zeichne die Temperaturen der beiden Städte mit Kreis-Markern und einer Legende oben rechts.
Titel: `Temperaturen im Juli`, x-Achse: `Tag`, y-Achse: `Temperatur (°C)`.''',
  PLT + '\ntag = [1, 2, 3, 4, 5, 6, 7]\nberlin = [24, 26, 29, 31, 27, 25, 23]\nhamburg = [21, 22, 25, 27, 24, 22, 20]',
  """plt.plot(tag, berlin, marker='o', label='Berlin')
plt.plot(tag, hamburg, marker='o', label='Hamburg')
plt.title('Temperaturen im Juli')
plt.xlabel('Tag')
plt.ylabel('Temperatur (°C)')
plt.legend(loc='upper right')
plt.show()""")
t('''Zeichne die Weg-Zeit-Diagramme der beiden Läufer (Strecke in m nach t Sekunden) mit Legende und Gitter.
Anna läuft 5 m pro Sekunde, Ben startet 20 m weiter vorne und läuft 4 m pro Sekunde. Zeichne von 0 bis 30 Sekunden.
Achsen: `Zeit (s)` und `Strecke (m)`.''', NPP,
  """t = np.linspace(0, 30, 2)
plt.plot(t, 5 * t, label='Anna')
plt.plot(t, 20 + 4 * t, label='Ben')
plt.xlabel('Zeit (s)')
plt.ylabel('Strecke (m)')
plt.legend()
plt.grid(True)
plt.show()""")
t('''Zeichne mit einer Schleife die Graphen von `x²`, `x² + 1`, `x² + 2` und `x² + 3` von -2 bis 2 (100 Punkte).
Die Labels sollen `c = 0`, `c = 1`, ... heißen (f-String). Füge eine Legende hinzu.''', NPP,
  """x = np.linspace(-2, 2, 100)
for c in range(4):
    plt.plot(x, x ** 2 + c, label=f'c = {c}')
plt.legend()
plt.show()""")
t('''Zeichne den Kontostand mit grünen Markern, Titel `Mein Konto`, Achsen `Monat` und `Euro` und Gitter.''',
  PLT + '\nmonat = [1, 2, 3, 4, 5, 6]\neuro = [50, 65, 40, 80, 95, 110]',
  """plt.plot(monat, euro, color='green', marker='o')
plt.title('Mein Konto')
plt.xlabel('Monat')
plt.ylabel('Euro')
plt.grid(True)
plt.show()""")
predict("""import matplotlib.pyplot as plt
plt.plot([1, 2], [1, 2], label='A')
plt.plot([1, 2], [2, 1])
plt.legend()
plt.title('Test')
plt.show()""")

# ---------------------------------------------------------------- 5
sec('Achsen einstellen')
expl('''#### Bereich und Einteilung

- `plt.xlim(a, b)` und `plt.ylim(a, b)` legen fest, welcher Bereich der Achsen zu sehen ist.
- `plt.xticks(positionen)` legt fest, an welchen Stellen Zahlen an der x-Achse stehen.
  Mit `plt.xticks(positionen, beschriftungen)` stehen dort stattdessen eigene Texte. Für die y-Achse gibt es `plt.yticks()`.
- `plt.axhline(y)` zeichnet eine waagerechte Linie über das ganze Diagramm, `plt.axvline(x)` eine senkrechte.
  Mit `plt.axhline(0, color='black')` und `plt.axvline(0, color='black')` bekommt man ein Koordinatenkreuz.''',
     """import numpy as np
import matplotlib.pyplot as plt

x = np.linspace(-3, 3, 100)
plt.plot(x, x ** 2 - 2)
plt.xlim(-4, 4)
plt.ylim(-3, 8)
plt.xticks([-4, -2, 0, 2, 4])
plt.axhline(0, color='black', linewidth=0.8)
plt.axvline(0, color='black', linewidth=0.8)
plt.show()""")
expl('''#### Gleiche Einheiten auf beiden Achsen

Normalerweise wählt matplotlib die Maßstäbe der beiden Achsen unabhängig voneinander. Ein Kreis sieht dann wie eine Ellipse aus.
Mit `plt.axis('equal')` ist eine Einheit auf beiden Achsen gleich lang.
`plt.axis('off')` blendet die Achsen ganz aus (z. B. für Zeichnungen).''',
     """import numpy as np
import matplotlib.pyplot as plt

w = np.linspace(0, 2 * np.pi, 200)
plt.plot(np.cos(w), np.sin(w))
plt.axis('equal')
plt.show()""")

t('Zeichne `x²` von -3 bis 3 (100 Punkte) und zeige nur den Bereich x von -1 bis 1 und y von 0 bis 1.', NPP,
  """x = np.linspace(-3, 3, 100)
plt.plot(x, x ** 2)
plt.xlim(-1, 1)
plt.ylim(0, 1)
plt.show()""")
t('Zeichne die Schülerzahlen so, dass die y-Achse bei 0 beginnt (`plt.ylim(0, 1000)`). So wirken die Unterschiede kleiner als ohne.',
  PLT + "\njahre = [2019, 2020, 2021, 2022, 2023, 2024]\nschueler = [820, 845, 870, 860, 905, 930]",
  """plt.plot(jahre, schueler, marker='o')
plt.ylim(0, 1000)
plt.show()""")
t('Zeichne `f(x) = x³ - 4x` von -3 bis 3 (200 Punkte) mit Koordinatenkreuz (schwarze Linien bei x = 0 und y = 0, Dicke 0.8).', NPP,
  """x = np.linspace(-3, 3, 200)
plt.plot(x, x ** 3 - 4 * x)
plt.axhline(0, color='black', linewidth=0.8)
plt.axvline(0, color='black', linewidth=0.8)
plt.show()""")
t('Zeichne die Temperaturen und beschrifte die x-Achse mit den Wochentagen statt mit Zahlen.',
  PLT + "\ntemperaturen = [12, 15, 14, 18, 21, 19, 16]\ntage = ['Mo', 'Di', 'Mi', 'Do', 'Fr', 'Sa', 'So']",
  """plt.plot(temperaturen, marker='o')
plt.xticks(range(7), tage)
plt.show()""")
t('''Zeichne `sin(x)` von 0 bis 2π (200 Punkte). Setze die Markierungen der x-Achse auf 0, π/2, π, 3π/2 und 2π und beschrifte sie mit
`0`, `π/2`, `π`, `3π/2` und `2π`.''', NPP,
  """x = np.linspace(0, 2 * np.pi, 200)
plt.plot(x, np.sin(x))
plt.xticks([0, np.pi / 2, np.pi, 3 * np.pi / 2, 2 * np.pi], ['0', 'π/2', 'π', '3π/2', '2π'])
plt.show()""")
t('Zeichne die Messwerte und eine rote, gestrichelte waagerechte Linie beim Grenzwert 50.',
  PLT + '\nmesswerte = [42, 47, 53, 49, 58, 44, 51]',
  """plt.plot(messwerte, marker='o')
plt.axhline(50, color='red', linestyle='--')
plt.show()""")
t('Zeichne einen Kreis mit Radius 2 um den Punkt (1, 1) (200 Punkte: `x = 1 + 2·cos(w)`, `y = 1 + 2·sin(w)`). Sorge dafür, dass er rund aussieht.', NPP,
  """w = np.linspace(0, 2 * np.pi, 200)
plt.plot(1 + 2 * np.cos(w), 1 + 2 * np.sin(w))
plt.axis('equal')
plt.show()""")
t('Zeichne ein Quadrat mit den Ecken (0, 0), (3, 0), (3, 3), (0, 3), sodass es wirklich quadratisch aussieht, und blende die Achsen aus.', PLT,
  """plt.plot([0, 3, 3, 0, 0], [0, 0, 3, 3, 0])
plt.axis('equal')
plt.axis('off')
plt.show()""")
t('Zeichne die Gerade `y = 2x - 1` von -2 bis 3 mit Gitter. Die x-Achse soll an jeder ganzen Zahl von -2 bis 3 eine Markierung haben (`range()`).', NPP,
  """x = np.linspace(-2, 3, 2)
plt.plot(x, 2 * x - 1)
plt.xticks(range(-2, 4))
plt.grid(True)
plt.show()""")
t('''Zeichne die Stundenwerte mit Kreis-Markern. Die x-Achse soll von 0 bis 24 gehen und alle 3 Stunden eine Markierung haben,
die y-Achse von 0 bis 30. Zeichne außerdem eine graue senkrechte Linie bei 12 Uhr.''',
  PLT + '\nstunde = [0, 3, 6, 9, 12, 15, 18, 21, 24]\ntemp = [8, 6, 7, 13, 19, 22, 18, 12, 9]',
  """plt.plot(stunde, temp, marker='o')
plt.xlim(0, 24)
plt.ylim(0, 30)
plt.xticks(range(0, 25, 3))
plt.axvline(12, color='gray')
plt.show()""")
predict("""import matplotlib.pyplot as plt
plt.plot([0, 1], [0, 1])
plt.xlim(0, 10)
plt.ylim(0, 10)
plt.show()""")

# ---------------------------------------------------------------- 6
sec('Text, Punkte und Pfeile')
expl('''#### Text und einzelne Punkte

- `plt.text(x, y, 'Text')` schreibt einen Text an die Stelle (x, y). Mit `fontsize=14` wird er größer, mit `color` farbig.
- Einen einzelnen Punkt zeichnet man mit `plt.plot([x], [y], 'ro')` oder einfach `plt.plot(x, y, 'ro')`.''',
     """import numpy as np
import matplotlib.pyplot as plt

x = np.linspace(-3, 3, 100)
plt.plot(x, x ** 2 - 4)
plt.plot([-2, 2], [0, 0], 'ro')
plt.text(-2, 0.5, 'Nullstelle')
plt.text(2, 0.5, 'Nullstelle')
plt.show()""")
expl('''#### Pfeile mit `plt.annotate()`

`plt.annotate('Text', xy=(x, y), xytext=(tx, ty), arrowprops=dict(arrowstyle='->'))` schreibt den Text an die Stelle `(tx, ty)`
und zeichnet einen Pfeil zum Punkt `(x, y)`. `dict(arrowstyle='->')` erzeugt ein Dictionary mit den Einstellungen des Pfeils.''',
     """import numpy as np
import matplotlib.pyplot as plt

x = np.linspace(0, 4, 100)
plt.plot(x, -(x - 2) ** 2 + 3)
plt.annotate('Hochpunkt (2|3)', xy=(2, 3), xytext=(2.5, 3.5), arrowprops=dict(arrowstyle='->'))
plt.ylim(-2, 4.5)
plt.show()""")

t('Zeichne `x² - 1` von -2 bis 2 (100 Punkte) und markiere die Nullstellen -1 und 1 mit roten Kreisen.', NPP,
  """x = np.linspace(-2, 2, 100)
plt.plot(x, x ** 2 - 1)
plt.plot([-1, 1], [0, 0], 'ro')
plt.show()""")
t('Zeichne die Messwerte und schreibe an den höchsten Wert den Text `Maximum`, eine Einheit über dem Punkt. Verwende `max()` und `index()`.',
  PLT + '\nmesswerte = [42, 47, 53, 49, 58, 44, 51]',
  """plt.plot(messwerte, marker='o')
i = messwerte.index(max(messwerte))
plt.text(i, max(messwerte) + 1, 'Maximum')
plt.show()""")
t('''Zeichne `f(x) = -(x - 1)² + 4` von -1 bis 3 (100 Punkte). Markiere den Scheitelpunkt (1|4) mit einem schwarzen Kreis
und zeige mit `plt.annotate()` und einem Pfeil vom Text `Scheitel` an der Stelle (2, 4.5) darauf. Setze `plt.ylim(0, 5)`.''', NPP,
  """x = np.linspace(-1, 3, 100)
plt.plot(x, -(x - 1) ** 2 + 4)
plt.plot(1, 4, 'ko')
plt.annotate('Scheitel', xy=(1, 4), xytext=(2, 4.5), arrowprops=dict(arrowstyle='->'))
plt.ylim(0, 5)
plt.show()""")
t('''Zwei Handytarife: Tarif A kostet 10 Euro plus 0.10 Euro pro Minute, Tarif B 20 Euro plus 0.05 Euro pro Minute.
Zeichne beide Kosten von 0 bis 400 Minuten mit Legende. Markiere den Schnittpunkt (200 Minuten, 30 Euro) mit einem roten Kreis
und schreibe `gleich teuer` an die Stelle (210, 27). Achsen: `Minuten` und `Kosten (Euro)`.''', NPP,
  """m = np.linspace(0, 400, 2)
plt.plot(m, 10 + 0.10 * m, label='Tarif A')
plt.plot(m, 20 + 0.05 * m, label='Tarif B')
plt.plot(200, 30, 'ro')
plt.text(210, 27, 'gleich teuer')
plt.xlabel('Minuten')
plt.ylabel('Kosten (Euro)')
plt.legend()
plt.show()""")
t('Schreibe an jeden Punkt der Messreihe seinen Wert (Text eine halbe Einheit über dem Punkt, mittig mit `ha=\'center\'`).',
  PLT + '\nwerte = [3, 5, 4, 7, 6]',
  """plt.plot(werte, marker='o')
for i in range(len(werte)):
    plt.text(i, werte[i] + 0.5, str(werte[i]), ha='center')
plt.ylim(0, 9)
plt.show()""")
t('''Zeichne `sin(x)` von 0 bis 2π (200 Punkte) und markiere Hochpunkt (π/2|1) und Tiefpunkt (3π/2|-1) mit roten Kreisen.
Schreibe `HP` und `TP` jeweils 0.1 rechts neben die Punkte. Setze `plt.ylim(-1.5, 1.5)`.''', NPP,
  """x = np.linspace(0, 2 * np.pi, 200)
plt.plot(x, np.sin(x))
plt.plot([np.pi / 2, 3 * np.pi / 2], [1, -1], 'ro')
plt.text(np.pi / 2 + 0.1, 1, 'HP')
plt.text(3 * np.pi / 2 + 0.1, -1, 'TP')
plt.ylim(-1.5, 1.5)
plt.show()""")
t('Schreibe in die Mitte eines leeren Diagramms mit Achsen von 0 bis 10 groß (Schriftgröße 30) und blau `Hallo!`. Tipp: `ha=\'center\'`.', PLT,
  """plt.xlim(0, 10)
plt.ylim(0, 10)
plt.text(5, 5, 'Hallo!', fontsize=30, color='blue', ha='center')
plt.show()""")

# ---------------------------------------------------------------- 7
sec('Größe und Speichern')
expl('''#### `plt.figure()` und `plt.savefig()`

- `plt.figure(figsize=(breite, hoehe))` beginnt ein neues Diagramm mit der angegebenen Größe (in Zoll, 1 Zoll = 2.54 cm).
  Es muss **vor** `plt.plot()` stehen. Ohne Angabe ist die Größe `(6.4, 4.8)`.
- `plt.savefig('name.png')` speichert das Diagramm als Bilddatei, **vor** `plt.show()`.
  Mit `dpi=150` wird es feiner, mit der Endung `.pdf` oder `.svg` entsteht eine Vektorgrafik.

In JupyterLite landet die Datei im Datei-Browser links. Von dort kann man sie herunterladen.''',
     """import os
import numpy as np
import matplotlib.pyplot as plt

x = np.linspace(0, 10, 200)
plt.figure(figsize=(8, 2))
plt.plot(x, np.sin(x))
plt.savefig('welle.png', dpi=100)
plt.show()
print(os.path.exists('welle.png'))""")

t('Zeichne `sin(x)` von 0 bis 4π (300 Punkte) in einem breiten, flachen Diagramm der Größe 10 × 2.', NPP,
  """x = np.linspace(0, 4 * np.pi, 300)
plt.figure(figsize=(10, 2))
plt.plot(x, np.sin(x))
plt.show()""")
t('Zeichne den Kreis mit Radius 1 (200 Punkte) in einem quadratischen Diagramm der Größe 4 × 4 mit `plt.axis(\'equal\')`.', NPP,
  """w = np.linspace(0, 2 * np.pi, 200)
plt.figure(figsize=(4, 4))
plt.plot(np.cos(w), np.sin(w))
plt.axis('equal')
plt.show()""")
t('''Zeichne die Temperaturen mit Titel `Wochentemperaturen` und speichere das Diagramm als `temperaturen.png`.
Gib danach mit `os.path.exists()` aus, ob die Datei existiert.''',
  'import os\n' + PLT + '\ntemperaturen = [12, 15, 14, 18, 21, 19, 16]',
  """plt.plot(temperaturen)
plt.title('Wochentemperaturen')
plt.savefig('temperaturen.png')
plt.show()
print(os.path.exists('temperaturen.png'))""")
t('''Zeichne zwei getrennte Diagramme nacheinander in derselben Zelle: zuerst `x²`, dann `x³`, beide von -2 bis 2 (100 Punkte).
Beginne jedes mit `plt.figure(figsize=(4, 3))` und beende jedes mit `plt.show()`.''', NPP,
  """x = np.linspace(-2, 2, 100)
plt.figure(figsize=(4, 3))
plt.plot(x, x ** 2)
plt.show()
plt.figure(figsize=(4, 3))
plt.plot(x, x ** 3)
plt.show()""")
t('Speichere den Graphen von `x²` von -2 bis 2 als PDF-Datei `parabel.pdf` und als PNG-Datei `parabel.png` mit 200 dpi. Gib danach aus, welche der beiden Dateien größer ist.',
  'import os\n' + NPP,
  """x = np.linspace(-2, 2, 100)
plt.plot(x, x ** 2)
plt.savefig('parabel.pdf')
plt.savefig('parabel.png', dpi=200)
plt.show()
if os.path.getsize('parabel.pdf') > os.path.getsize('parabel.png'):
    print('PDF')
else:
    print('PNG')""", kind='free')

# ---------------------------------------------------------------- 8
sec('Gemischte Übungen')
t('''Zeichne die Fieberkurve: Temperaturen mit roten Kreisen und roter Linie, eine graue gestrichelte Linie bei 37 °C,
Titel `Fieberkurve`, Achsen `Tag` und `Temperatur (°C)`, die Tage als Beschriftung der x-Achse.''',
  PLT + "\ntage = ['Mo', 'Di', 'Mi', 'Do', 'Fr']\ntemperatur = [38.9, 39.4, 38.2, 37.5, 36.8]",
  """plt.plot(temperatur, 'ro-')
plt.axhline(37, color='gray', linestyle='--')
plt.xticks(range(5), tage)
plt.title('Fieberkurve')
plt.xlabel('Tag')
plt.ylabel('Temperatur (°C)')
plt.show()""")
t('''Vergleiche lineares und exponentielles Wachstum von 0 bis 10 Jahren (100 Punkte): Konto A bekommt jedes Jahr 100 Euro dazu (Start 1000),
Konto B 8 % Zinsen (Start 1000). Zeichne beide mit Legende (`linear`, `exponentiell`), Gitter und den Achsen `Jahre` und `Euro`.''', NPP,
  """t = np.linspace(0, 10, 100)
plt.plot(t, 1000 + 100 * t, label='linear')
plt.plot(t, 1000 * 1.08 ** t, label='exponentiell')
plt.xlabel('Jahre')
plt.ylabel('Euro')
plt.legend()
plt.grid(True)
plt.show()""")
t('''Zeichne die Funktion `f(x) = x³ - 3x² + 2` von -1.5 bis 3.5 (200 Punkte) mit Koordinatenkreuz (schwarz, Dicke 0.8).
Markiere die Extrempunkte (0|2) und (2|-2) mit grünen Kreisen und den Wendepunkt (1|0) mit einem roten Quadrat.''', NPP,
  """x = np.linspace(-1.5, 3.5, 200)
plt.plot(x, x ** 3 - 3 * x ** 2 + 2)
plt.axhline(0, color='black', linewidth=0.8)
plt.axvline(0, color='black', linewidth=0.8)
plt.plot([0, 2], [2, -2], 'go')
plt.plot(1, 0, 'rs')
plt.show()""")
t('''Zeichne eine **Spirale**: `w` von 0 bis 6π (500 Punkte), `r = w`, `x = r·cos(w)`, `y = r·sin(w)`. Gleiche Einheiten, ohne Achsen.''', NPP,
  """w = np.linspace(0, 6 * np.pi, 500)
plt.plot(w * np.cos(w), w * np.sin(w))
plt.axis('equal')
plt.axis('off')
plt.show()""")
t('''Zeichne ein **Herz** in Rot mit Linienstärke 3: `t` von 0 bis 2π (300 Punkte), `x = 16·sin(t)³`,
`y = 13·cos(t) - 5·cos(2t) - 2·cos(3t) - cos(4t)`. Gleiche Einheiten, ohne Achsen.''', NPP,
  """t = np.linspace(0, 2 * np.pi, 300)
x = 16 * np.sin(t) ** 3
y = 13 * np.cos(t) - 5 * np.cos(2 * t) - 2 * np.cos(3 * t) - np.cos(4 * t)
plt.plot(x, y, color='red', linewidth=3)
plt.axis('equal')
plt.axis('off')
plt.show()""")
t('''Zeichne einen **Stern** mit 5 Zacken: Die Punkte liegen auf einem Kreis mit Radius 1 bei den Winkeln 90°, 90° + 144°, 90° + 2·144°, ...
(6 Punkte, damit er geschlossen ist). Rechne die Winkel mit `np.radians()` um. Gleiche Einheiten, ohne Achsen, gelbe Linie der Dicke 3.''', NPP,
  """w = np.radians(90 + 144 * np.arange(6))
plt.plot(np.cos(w), np.sin(w), color='gold', linewidth=3)
plt.axis('equal')
plt.axis('off')
plt.show()""")
t('''Zeichne ein **Schachbrett-Muster aus Linien**: 9 waagerechte und 9 senkrechte schwarze Linien bei 0, 1, ..., 8 (jeweils von 0 bis 8).
Gleiche Einheiten, ohne Achsen.''', PLT,
  """for i in range(9):
    plt.plot([0, 8], [i, i], color='black')
    plt.plot([i, i], [0, 8], color='black')
plt.axis('equal')
plt.axis('off')
plt.show()""")
t('''Zeichne die **Sinus-Annäherung durch Polynome**: `sin(x)` (schwarz, Dicke 3) und die Näherungen `x`, `x - x³/6` und `x - x³/6 + x⁵/120`
von -4 bis 4 (200 Punkte) mit den Labels `sin(x)`, `Grad 1`, `Grad 3`, `Grad 5`, Legende und `plt.ylim(-2, 2)`.''', NPP,
  """x = np.linspace(-4, 4, 200)
plt.plot(x, np.sin(x), color='black', linewidth=3, label='sin(x)')
plt.plot(x, x, label='Grad 1')
plt.plot(x, x - x ** 3 / 6, label='Grad 3')
plt.plot(x, x - x ** 3 / 6 + x ** 5 / 120, label='Grad 5')
plt.ylim(-2, 2)
plt.legend()
plt.show()""")
t('''Zeichne die Graphen von `f(x) = x²` und ihrer Ableitung `f'(x) = 2x` von -2 bis 2 (100 Punkte). Zeichne außerdem die Tangente an `f`
bei `x = 1` (`y = 2x - 1`) als graue gestrichelte Linie und den Berührpunkt (1|1) als schwarzen Kreis. Legende mit `f`, `f'` und `Tangente`.''', NPP,
  """x = np.linspace(-2, 2, 100)
plt.plot(x, x ** 2, label='f')
plt.plot(x, 2 * x, label="f'")
plt.plot(x, 2 * x - 1, color='gray', linestyle='--', label='Tangente')
plt.plot(1, 1, 'ko')
plt.legend()
plt.show()""")
t('''Zeichne die **Zinseszins-Entwicklung** von 1000 Euro für die Zinssätze 1 %, 3 % und 5 % über 30 Jahre (ganze Jahre, mit Markern `'.'`).
Labels `1 %`, `3 %`, `5 %`, Legende oben links, Titel `Zinseszins`.''', NPP,
  """jahre = np.arange(31)
for p in [1, 3, 5]:
    plt.plot(jahre, 1000 * (1 + p / 100) ** jahre, marker='.', label=f'{p} %')
plt.legend(loc='upper left')
plt.title('Zinseszins')
plt.show()""")
predict("""import numpy as np
import matplotlib.pyplot as plt
w = np.linspace(0, 2 * np.pi, 7)
plt.plot(np.cos(w), np.sin(w), 'o-')
plt.axis('equal')
plt.show()""")

generate('matplotlib_grundlagen', 'matplotlib: Grundlagen', INTRO)
