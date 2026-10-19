# Erzeugt ../content/matplotlib_layout.ipynb (siehe nbgen.py).
#
# Braucht matplotlib 3.10.8 und numpy 2.4.6 (wie Pyodide in JupyterLite), siehe gen_matplotlib_grundlagen.py:
#     py -3.13 -W error generator/gen_matplotlib_layout.py
#     py -3.13 generator/pyodide_check/pruefen.py generator/gen_matplotlib_layout.py
#
# Stile nur mit plt.style.context() (wirkt nur im with-Block). plt.style.use() würde im Notebook in alle späteren
# Zellen durchschlagen (im Generator setzt run_mit_bildern() vor jeder Zelle rcdefaults(), im Browser nicht).
from nbgen import sec, expl, task, predict, generate


def t(text, given='', body='', kind='normal'):
    """Aufgabe, deren Lösung aus dem vorgegebenen Code plus body besteht."""
    task(text, given=given, solution=(given + '\n' + body) if given else body, kind=kind)


PLT = 'import matplotlib.pyplot as plt'
NPP = 'import numpy as np\nimport matplotlib.pyplot as plt'

INTRO = '''Bisher hat jede Zelle ein einzelnes Diagramm mit `plt.plot()`, `plt.title()` usw. gezeichnet. In diesem Notebook lernst du
die **objektorientierte Schreibweise** `fig, ax = plt.subplots()` kennen. Mit ihr zeichnet man **mehrere Diagramme** in ein Bild,
setzt zweite Achsen und logarithmische Skalen ein und stellt **2D-Arrays als Bilder** dar: Heatmaps, Spielfelder und Höhenlinien.

Vorausgesetzt werden die Notebooks *matplotlib: Grundlagen*, *matplotlib: Diagrammtypen* und *numpy: Zweidimensionale Arrays*.

Jeder Abschnitt beginnt mit kurzen Erklärungen und Beispielen. Führe die Beispiele aus und probiere sie ruhig ein wenig aus.
Danach folgen viele kleine Übungen. Unter den meisten Aufgaben siehst du das **erwartete Diagramm**. Zeichne es nach und vergleiche.'''

# ---------------------------------------------------------------- 1
sec('Figure und Axes')
expl('''#### `fig, ax = plt.subplots()`

Ein Bild in matplotlib besteht aus zwei Arten von Objekten:

- Die **Figure** (`fig`) ist das ganze Bild, sozusagen das Blatt Papier.
- Ein **Axes**-Objekt (`ax`) ist **ein Diagramm** darauf, mit Achsen, Linien und Beschriftungen. Eine Figure kann mehrere davon enthalten.

`fig, ax = plt.subplots()` erzeugt beides. Danach zeichnet man mit Methoden von `ax`. Die meisten heißen wie bei `plt`,
aber die Beschriftungen und Einstellungen bekommen ein `set_` davor:

| `plt`-Schreibweise | `ax`-Schreibweise |
|---|---|
| `plt.plot()`, `plt.scatter()`, `plt.bar()`, `plt.hist()` | `ax.plot()`, `ax.scatter()`, `ax.bar()`, `ax.hist()` |
| `plt.title('...')` | `ax.set_title('...')` |
| `plt.xlabel('...')`, `plt.ylabel('...')` | `ax.set_xlabel('...')`, `ax.set_ylabel('...')` |
| `plt.xlim(a, b)`, `plt.ylim(a, b)` | `ax.set_xlim(a, b)`, `ax.set_ylim(a, b)` |
| `plt.xticks(pos, namen)` | `ax.set_xticks(pos, namen)` |
| `plt.legend()`, `plt.grid(True)`, `plt.text()` | `ax.legend()`, `ax.grid(True)`, `ax.text()` |
| `plt.axis('equal')` | `ax.set_aspect('equal')` |

Die Größe gibt man gleich mit an: `plt.subplots(figsize=(8, 3))`. `plt.show()` zeigt das Bild wie bisher.''',
     """import numpy as np
import matplotlib.pyplot as plt

x = np.linspace(0, 2 * np.pi, 200)
fig, ax = plt.subplots(figsize=(7, 4))
ax.plot(x, np.sin(x), label='sin(x)')
ax.plot(x, np.cos(x), label='cos(x)')
ax.set_title('Sinus und Kosinus')
ax.set_xlabel('x')
ax.set_ylabel('y')
ax.legend()
ax.grid(True)
plt.show()""")

t('Zeichne mit `fig, ax = plt.subplots()` den Graphen von `x²` von -3 bis 3 (100 Punkte).', NPP,
  """x = np.linspace(-3, 3, 100)
fig, ax = plt.subplots()
ax.plot(x, x ** 2)
plt.show()""")
t('Zeichne die Temperaturen mit `ax` und Kreis-Markern, Titel `Woche`, Achsen `Tag` und `°C`.',
  PLT + '\ntemperaturen = [12, 15, 14, 18, 21, 19, 16]',
  """fig, ax = plt.subplots()
ax.plot(temperaturen, marker='o')
ax.set_title('Woche')
ax.set_xlabel('Tag')
ax.set_ylabel('°C')
plt.show()""")
t('Übersetze den Code in die `ax`-Schreibweise und führe ihn aus:\n```python\nplt.plot([1, 2, 3], [2, 4, 1], \'r--\')\nplt.xlim(0, 4)\nplt.ylim(0, 5)\nplt.title(\'Test\')\nplt.grid(True)\nplt.show()\n```',
  PLT, """fig, ax = plt.subplots()
ax.plot([1, 2, 3], [2, 4, 1], 'r--')
ax.set_xlim(0, 4)
ax.set_ylim(0, 5)
ax.set_title('Test')
ax.grid(True)
plt.show()""")
t('Zeichne ein Balkendiagramm der Haustiere mit `ax.bar()` in einer Figure der Größe 6 × 3.',
  PLT + "\ntiere = ['Hund', 'Katze', 'Fisch', 'Vogel']\nanzahl = [12, 9, 4, 3]",
  """fig, ax = plt.subplots(figsize=(6, 3))
ax.bar(tiere, anzahl)
plt.show()""")
t('Zeichne einen Kreis mit Radius 1 (200 Punkte) mit `ax` und sorge mit `ax.set_aspect(\'equal\')` dafür, dass er rund aussieht.', NPP,
  """w = np.linspace(0, 2 * np.pi, 200)
fig, ax = plt.subplots()
ax.plot(np.cos(w), np.sin(w))
ax.set_aspect('equal')
plt.show()""")
t('Zeichne `sin(x)` von 0 bis 2π (200 Punkte) mit `ax` und setze die x-Markierungen auf 0, π und 2π mit den Beschriftungen `0`, `π` und `2π`.', NPP,
  """x = np.linspace(0, 2 * np.pi, 200)
fig, ax = plt.subplots()
ax.plot(x, np.sin(x))
ax.set_xticks([0, np.pi, 2 * np.pi], ['0', 'π', '2π'])
plt.show()""")
t('''Zeichne die Messwerte mit `ax` und schreibe mit `ax.text()` an den höchsten Punkt `Max` (eine Einheit darüber, mittig). Setze die y-Achse von 0 bis 70.''',
  PLT + '\nwerte = [42, 47, 53, 49, 58, 44, 51]',
  """fig, ax = plt.subplots()
ax.plot(werte, marker='o')
i = werte.index(max(werte))
ax.text(i, max(werte) + 1, 'Max', ha='center')
ax.set_ylim(0, 70)
plt.show()""")
t('Zeichne die Geraden `y = x`, `y = 2x` und `y = 3x` von 0 bis 5 mit `ax`, Labels `m = 1`, `m = 2`, `m = 3` und Legende oben links. Gib dem ganzen Bild mit `fig.suptitle()` die Überschrift `Ursprungsgeraden`.', NPP,
  """x = np.array([0, 5])
fig, ax = plt.subplots()
for m in [1, 2, 3]:
    ax.plot(x, m * x, label=f'm = {m}')
ax.legend(loc='upper left')
fig.suptitle('Ursprungsgeraden')
plt.show()""")
predict("""import matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(3, 3))
ax.plot([0, 1, 1, 0, 0], [0, 0, 1, 1, 0])
ax.set_aspect('equal')
plt.show()
print(type(fig).__name__, type(ax).__name__)""")

# ---------------------------------------------------------------- 2
sec('Mehrere Diagramme')
expl('''#### Ein Raster von Diagrammen

`fig, axs = plt.subplots(zeilen, spalten)` erzeugt ein Raster von Diagrammen. `axs` ist ein numpy-Array mit den Axes-Objekten:

- bei mehreren Zeilen und Spalten ein 2D-Array: `axs[0, 1]` ist oben, zweites von links,
- bei nur einer Zeile (oder Spalte) ein eindimensionales Array: `axs[0]`, `axs[1]`, ...

Mit `layout='constrained'` ordnet matplotlib die Diagramme so an, dass sich die Beschriftungen nicht überlappen.
`fig.suptitle('...')` setzt eine Überschrift über alle Diagramme.''',
     """import numpy as np
import matplotlib.pyplot as plt

x = np.linspace(-2, 2, 100)
fig, axs = plt.subplots(2, 2, figsize=(7, 5), layout='constrained')
axs[0, 0].plot(x, x)
axs[0, 0].set_title('x')
axs[0, 1].plot(x, x ** 2)
axs[0, 1].set_title('x²')
axs[1, 0].plot(x, x ** 3)
axs[1, 0].set_title('x³')
axs[1, 1].plot(x, np.abs(x))
axs[1, 1].set_title('|x|')
fig.suptitle('Vier Funktionen')
plt.show()""")
expl('''#### Schleifen und gemeinsame Achsen

- `axs.flat` durchläuft alle Diagramme der Reihe nach (zeilenweise). Zusammen mit `zip()` oder `enumerate()` füllt man sie in einer Schleife.
- Mit `sharex=True` bzw. `sharey=True` haben alle Diagramme dieselbe Einteilung der x- bzw. y-Achse. So kann man sie direkt vergleichen.
- Ein unbenutztes Diagramm blendet man mit `ax.axis('off')` aus.''',
     """import numpy as np
import matplotlib.pyplot as plt

x = np.linspace(0, 2 * np.pi, 200)
fig, axs = plt.subplots(1, 3, figsize=(9, 3), sharey=True, layout='constrained')
for k, ax in enumerate(axs.flat, 1):
    ax.plot(x, np.sin(k * x))
    ax.set_title(f'sin({k}x)')
plt.show()""")

t('Zeichne zwei Diagramme nebeneinander (Größe 8 × 3): links `x²`, rechts `x³`, jeweils von -2 bis 2 (100 Punkte) mit den Titeln `x²` und `x³`.', NPP,
  """x = np.linspace(-2, 2, 100)
fig, axs = plt.subplots(1, 2, figsize=(8, 3))
axs[0].plot(x, x ** 2)
axs[0].set_title('x²')
axs[1].plot(x, x ** 3)
axs[1].set_title('x³')
plt.show()""")
t('Zeichne zwei Diagramme untereinander (Größe 6 × 5, `layout=\'constrained\'`): oben die Temperaturen als Linie, unten den Regen als Balken.',
  PLT + "\ntage = ['Mo', 'Di', 'Mi', 'Do', 'Fr', 'Sa', 'So']\ntemperatur = [12, 15, 14, 18, 21, 19, 16]\nregen = [0, 2.5, 8, 1, 0, 0, 4.5]",
  """fig, axs = plt.subplots(2, 1, figsize=(6, 5), layout='constrained')
axs[0].plot(tage, temperatur, marker='o')
axs[1].bar(tage, regen)
plt.show()""")
t('Zeichne die beiden Diagramme aus der vorigen Aufgabe mit gemeinsamer x-Achse (`sharex=True`) und den y-Beschriftungen `°C` und `mm`.',
  PLT + "\ntage = ['Mo', 'Di', 'Mi', 'Do', 'Fr', 'Sa', 'So']\ntemperatur = [12, 15, 14, 18, 21, 19, 16]\nregen = [0, 2.5, 8, 1, 0, 0, 4.5]",
  """fig, axs = plt.subplots(2, 1, figsize=(6, 5), sharex=True, layout='constrained')
axs[0].plot(tage, temperatur, marker='o')
axs[0].set_ylabel('°C')
axs[1].bar(tage, regen)
axs[1].set_ylabel('mm')
plt.show()""")
t('''Zeichne ein 2 × 2-Raster (Größe 7 × 5, `layout='constrained'`) mit vier Diagrammtypen derselben Daten: Linie, Balken, Streudiagramm und waagerechte Balken.
Titel: `plot`, `bar`, `scatter`, `barh`.''',
  PLT + "\nx = ['A', 'B', 'C', 'D']\ny = [3, 7, 5, 2]",
  """fig, axs = plt.subplots(2, 2, figsize=(7, 5), layout='constrained')
axs[0, 0].plot(x, y)
axs[0, 0].set_title('plot')
axs[0, 1].bar(x, y)
axs[0, 1].set_title('bar')
axs[1, 0].scatter(x, y)
axs[1, 0].set_title('scatter')
axs[1, 1].barh(x, y)
axs[1, 1].set_title('barh')
plt.show()""")
t('''Zeichne mit einer Schleife über `axs.flat` die Parabeln `a · x²` für `a` = 1, 2, -1 und -2 in ein 2 × 2-Raster (x von -2 bis 2, 100 Punkte) mit
gemeinsamer y-Achse und den Titeln `a = 1` usw. Verwende `zip(axs.flat, [1, 2, -1, -2])`.''', NPP,
  """x = np.linspace(-2, 2, 100)
fig, axs = plt.subplots(2, 2, sharey=True, layout='constrained')
for ax, a in zip(axs.flat, [1, 2, -1, -2]):
    ax.plot(x, a * x ** 2)
    ax.set_title(f'a = {a}')
plt.show()""")
t('''Zeichne die Histogramme von drei Normalverteilungen nebeneinander mit gemeinsamen Achsen (Größe 9 × 3): `rng.normal(0, s, size=1000)` für `s` = 1, 2, 3 (in dieser Reihenfolge),
jeweils mit den Klassengrenzen `np.linspace(-10, 10, 41)` und den Titeln `σ = 1` usw.''',
  NPP + '\nrng = np.random.default_rng(2)',
  """fig, axs = plt.subplots(1, 3, figsize=(9, 3), sharex=True, sharey=True, layout='constrained')
for ax, s in zip(axs, [1, 2, 3]):
    ax.hist(rng.normal(0, s, size=1000), bins=np.linspace(-10, 10, 41))
    ax.set_title(f'σ = {s}')
plt.show()""")
t('''Zeichne ein 2 × 3-Raster (Größe 9 × 5) für fünf Funktionen `sin`, `cos`, `sqrt`, `exp` und `log` von 0.1 bis 3 (100 Punkte) mit dem Namen als Titel.
Blende das sechste Diagramm aus. Verwende eine Liste von Paaren `(name, funktion)`, z. B. `('sin', np.sin)`.''', NPP,
  """x = np.linspace(0.1, 3, 100)
funktionen = [('sin', np.sin), ('cos', np.cos), ('sqrt', np.sqrt), ('exp', np.exp), ('log', np.log)]
fig, axs = plt.subplots(2, 3, figsize=(9, 5), layout='constrained')
for ax, (name, f) in zip(axs.flat, funktionen):
    ax.plot(x, f(x))
    ax.set_title(name)
axs[1, 2].axis('off')
plt.show()""")
t('''Zeichne vier Würfelexperimente nebeneinander (Größe 10 × 2.5, gemeinsame y-Achse): Häufigkeiten der Augenzahlen bei 10, 100, 1000 und 10000 Würfen
(`rng.integers(1, 7, size=n)` in dieser Reihenfolge) als **relative** Häufigkeiten (Balken). Titel `n = 10` usw. und eine rote Linie bei 1/6.''',
  NPP + '\nrng = np.random.default_rng(3)',
  """fig, axs = plt.subplots(1, 4, figsize=(10, 2.5), sharey=True, layout='constrained')
for ax, n in zip(axs, [10, 100, 1000, 10000]):
    w = rng.integers(1, 7, size=n)
    ax.bar(range(1, 7), np.bincount(w, minlength=7)[1:] / n)
    ax.axhline(1 / 6, color='red')
    ax.set_title(f'n = {n}')
plt.show()""")
predict("""import matplotlib.pyplot as plt
fig, axs = plt.subplots(2, 3)
print(axs.shape)
print(len(axs.flat))
fig, axs = plt.subplots(1, 4)
print(axs.shape)
plt.close('all')""")

# ---------------------------------------------------------------- 3
sec('Achsen-Tricks')
expl('''#### Zweite y-Achse mit `twinx()`

Haben zwei Größen ganz verschiedene Einheiten oder Größenordnungen (z. B. Temperatur und Regenmenge), zeichnet man sie mit zwei y-Achsen:
`ax2 = ax.twinx()` erzeugt ein zweites Axes-Objekt mit derselben x-Achse und einer eigenen y-Achse rechts.
Damit man die Kurven zuordnen kann, färbt man die Achsenbeschriftung wie die Kurve.''',
     """import matplotlib.pyplot as plt

monate = ['Jan', 'Feb', 'Mär', 'Apr', 'Mai', 'Jun']
temperatur = [1, 2, 6, 10, 15, 18]
regen = [50, 40, 45, 40, 60, 70]
fig, ax = plt.subplots()
ax.bar(monate, regen, color='lightblue')
ax.set_ylabel('Regen (mm)', color='steelblue')
ax2 = ax.twinx()
ax2.plot(monate, temperatur, color='red', marker='o')
ax2.set_ylabel('Temperatur (°C)', color='red')
plt.show()""")
expl('''#### Logarithmische Achsen und weitere Einstellungen

- `ax.set_yscale('log')` teilt die y-Achse **logarithmisch** ein: Gleiche Abstände bedeuten gleiche **Faktoren** (1, 10, 100, 1000).
  Exponentielles Wachstum wird dann zu einer Geraden. Für die x-Achse gibt es `ax.set_xscale('log')`.
- `ax.invert_yaxis()` dreht die Richtung der y-Achse um (z. B. für Platzierungen: Platz 1 oben).
- `ax.spines['top'].set_visible(False)` blendet den oberen Rahmen aus, entsprechend `'right'`, `'left'`, `'bottom'`.''',
     """import numpy as np
import matplotlib.pyplot as plt

t = np.arange(0, 11)
fig, axs = plt.subplots(1, 2, figsize=(8, 3), layout='constrained')
axs[0].plot(t, 2 ** t, marker='o')
axs[0].set_title('normal')
axs[1].plot(t, 2 ** t, marker='o')
axs[1].set_yscale('log')
axs[1].set_title('logarithmisch')
plt.show()""")

t('''Zeichne den Eisverkauf (Balken, Farbe `orange`, y-Beschriftung `Eis`) und darüber mit einer zweiten y-Achse die Temperatur (rote Linie mit Kreisen, y-Beschriftung `°C`).''',
  PLT + "\nmonate = ['Apr', 'Mai', 'Jun', 'Jul', 'Aug', 'Sep']\neis = [65, 90, 120, 140, 135, 95]\ntemperatur = [10, 15, 18, 21, 20, 16]",
  """fig, ax = plt.subplots()
ax.bar(monate, eis, color='orange')
ax.set_ylabel('Eis')
ax2 = ax.twinx()
ax2.plot(monate, temperatur, color='red', marker='o')
ax2.set_ylabel('°C')
plt.show()""")
t('''Zeichne die Weltbevölkerung (in Milliarden) und den CO₂-Gehalt der Luft (in ppm) über den Jahren: Bevölkerung blau mit Achsenbeschriftung `Milliarden` in Blau,
CO₂ grün auf einer zweiten Achse mit `ppm` in Grün.''',
  PLT + '\njahre = [1960, 1970, 1980, 1990, 2000, 2010, 2020]\nbevoelkerung = [3.0, 3.7, 4.4, 5.3, 6.1, 6.9, 7.8]\nco2 = [317, 326, 339, 354, 369, 390, 414]',
  """fig, ax = plt.subplots()
ax.plot(jahre, bevoelkerung, color='blue')
ax.set_ylabel('Milliarden', color='blue')
ax2 = ax.twinx()
ax2.plot(jahre, co2, color='green')
ax2.set_ylabel('ppm', color='green')
plt.show()""")
t('Zeichne die Zweierpotenzen `2^n` für n von 0 bis 20 mit Kreis-Markern und logarithmischer y-Achse.', NPP,
  """n = np.arange(21)
fig, ax = plt.subplots()
ax.plot(n, 2 ** n, marker='o')
ax.set_yscale('log')
plt.show()""")
t('''Zeichne `x`, `x²`, `x³` und `2^x` von 1 bis 20 (100 Punkte) mit logarithmischer y-Achse, Legende und Gitter. Labels: `x`, `x²`, `x³`, `2^x`.''', NPP,
  """x = np.linspace(1, 20, 100)
fig, ax = plt.subplots()
ax.plot(x, x, label='x')
ax.plot(x, x ** 2, label='x²')
ax.plot(x, x ** 3, label='x³')
ax.plot(x, 2 ** x, label='2^x')
ax.set_yscale('log')
ax.legend()
ax.grid(True)
plt.show()""")
t('''Zeichne die Einwohnerzahlen der Orte als waagerechte Balken mit logarithmischer x-Achse. Ohne log-Achse sähe man das Dorf gar nicht.''',
  PLT + "\norte = ['Dorf', 'Kleinstadt', 'Stadt', 'Großstadt', 'Metropole']\neinwohner = [800, 12000, 95000, 650000, 3700000]",
  """fig, ax = plt.subplots()
ax.barh(orte, einwohner)
ax.set_xscale('log')
plt.show()""")
t('''Zeichne die Platzierungen eines Teams in der Tabelle über die Spieltage mit Kreis-Markern. Platz 1 soll oben stehen (`invert_yaxis()`), die y-Achse soll die Plätze 1 bis 18 zeigen
(`set_yticks(range(1, 19))`).''',
  PLT + '\nspieltag = [1, 2, 3, 4, 5, 6, 7, 8]\nplatz = [9, 6, 7, 4, 3, 5, 2, 1]',
  """fig, ax = plt.subplots()
ax.plot(spieltag, platz, marker='o')
ax.set_ylim(0.5, 18.5)
ax.set_yticks(range(1, 19))
ax.invert_yaxis()
plt.show()""")
t('Zeichne die Werte als Linie und blende den oberen und den rechten Rahmen aus.',
  PLT + '\nwerte = [3, 5, 4, 7, 6, 8, 7]',
  """fig, ax = plt.subplots()
ax.plot(werte)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
plt.show()""")
t('''Zeichne ein Koordinatensystem wie im Matheheft: `x³ - 3x` von -2.5 bis 2.5 (200 Punkte), die linke und untere Achse durch den Ursprung
(`ax.spines['left'].set_position('zero')`, ebenso `'bottom'`), oberer und rechter Rahmen ausgeblendet.''', NPP,
  """x = np.linspace(-2.5, 2.5, 200)
fig, ax = plt.subplots()
ax.plot(x, x ** 3 - 3 * x)
ax.spines['left'].set_position('zero')
ax.spines['bottom'].set_position('zero')
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
plt.show()""")

# ---------------------------------------------------------------- 4
sec('Stile und Farben')
expl('''#### Stile

matplotlib bringt fertige **Stile** mit, die Farben, Hintergrund, Gitter und Schrift auf einmal ändern.
`plt.style.available` ist die Liste aller Stile, z. B. `'ggplot'`, `'seaborn-v0_8'`, `'fivethirtyeight'`, `'dark_background'`, `'grayscale'`.

`with plt.style.context('ggplot'):` wendet einen Stil nur auf den eingerückten Code an.
(Es gibt auch `plt.style.use('ggplot')`, das gilt dann aber für **alle** folgenden Zellen.)''',
     """import numpy as np
import matplotlib.pyplot as plt

print(plt.style.available[:6])
x = np.linspace(0, 10, 100)
with plt.style.context('ggplot'):
    fig, ax = plt.subplots(figsize=(6, 3))
    for k in range(1, 4):
        ax.plot(x, np.sin(x + k), label=f'Welle {k}')
    ax.legend()
    plt.show()""")
expl('''#### Farben des Farbzyklus und Farbskalen

- Die automatischen Farben heißen `'C0'` (blau), `'C1'` (orange), `'C2'` (grün), `'C3'` (rot), ... bis `'C9'`. Man kann sie auch selbst angeben.
- Eine **Farbskala** (*colormap*) ordnet Zahlen von 0 bis 1 Farben zu: `plt.colormaps['viridis'](0.3)` ist die Farbe an der Stelle 0.3.
  So färbt man z. B. eine Kurvenschar von hell nach dunkel.''',
     """import numpy as np
import matplotlib.pyplot as plt

x = np.linspace(0, 2, 100)
skala = plt.colormaps['viridis']
fig, ax = plt.subplots()
for i in range(6):
    ax.plot(x, x ** (i + 1), color=skala(i / 5))
plt.show()""")

t('Zeichne `sin(x)` und `cos(x)` von 0 bis 2π (200 Punkte) mit Legende im Stil `ggplot`.', NPP,
  """x = np.linspace(0, 2 * np.pi, 200)
with plt.style.context('ggplot'):
    fig, ax = plt.subplots()
    ax.plot(x, np.sin(x), label='sin')
    ax.plot(x, np.cos(x), label='cos')
    ax.legend()
    plt.show()""")
t('Zeichne das Balkendiagramm der Haustiere im Stil `dark_background`.',
  PLT + "\ntiere = ['Hund', 'Katze', 'Fisch', 'Vogel']\nanzahl = [12, 9, 4, 3]",
  """with plt.style.context('dark_background'):
    fig, ax = plt.subplots()
    ax.bar(tiere, anzahl)
    plt.show()""")
t('Zeichne die drei Linien im Stil `fivethirtyeight` mit Legende.',
  NPP + '\nx = np.arange(10)\na = x\nb = 0.5 * x + 2\nc = 9 - x',
  """with plt.style.context('fivethirtyeight'):
    fig, ax = plt.subplots()
    ax.plot(x, a, label='a')
    ax.plot(x, b, label='b')
    ax.plot(x, c, label='c')
    ax.legend()
    plt.show()""")
t('Zeichne die vier Geraden `y = x + k` für k von 0 bis 3 (x von 0 bis 5) in den Farben `C3`, `C2`, `C1` und `C0` (in dieser Reihenfolge).', NPP,
  """x = np.array([0, 5])
fig, ax = plt.subplots()
for k, farbe in zip(range(4), ['C3', 'C2', 'C1', 'C0']):
    ax.plot(x, x + k, color=farbe)
plt.show()""")
t('''Zeichne die Kurvenschar `sin(x) · e^(-a·x)` für `a` = 0, 0.1, ..., 0.9 (10 Kurven, x von 0 bis 10, 300 Punkte) mit Farben aus der Skala `'plasma'`
(Kurve `i` bekommt `skala(i / 9)`).''', NPP,
  """x = np.linspace(0, 10, 300)
skala = plt.colormaps['plasma']
fig, ax = plt.subplots()
for i in range(10):
    a = i / 10
    ax.plot(x, np.sin(x) * np.exp(-a * x), color=skala(i / 9))
plt.show()""")
t('Gib aus, wie viele Stile es gibt und ob der Stil `ggplot` dabei ist.', PLT,
  """print(len(plt.style.available))
print('ggplot' in plt.style.available)""")

# ---------------------------------------------------------------- 5
sec('2D-Arrays als Bilder: imshow()')
expl('''#### `ax.imshow()`

`ax.imshow(a)` zeigt ein 2D-Array als **Bild**: Jedes Element wird ein farbiges Kästchen, Zeile 0 oben.
Die Farbe ergibt sich aus dem Wert und der Farbskala `cmap`.

| Parameter | Bedeutung |
|---|---|
| `cmap` | Farbskala, z. B. `'viridis'`, `'gray'`, `'hot'`, `'coolwarm'`, `'Greens'`, `'binary'` |
| `vmin`, `vmax` | Werte für die Enden der Farbskala (sonst kleinster und größter Wert im Array) |

`fig.colorbar(bild, ax=ax)` zeigt die Farbskala daneben. Dazu speichert man das Ergebnis von `imshow()` in `bild`.
Bei Bildern stören die Achsen oft, dann hilft `ax.axis('off')`.''',
     """import numpy as np
import matplotlib.pyplot as plt

a = np.arange(12).reshape(3, 4)
fig, ax = plt.subplots()
bild = ax.imshow(a, cmap='viridis')
fig.colorbar(bild, ax=ax)
plt.show()

fig, ax = plt.subplots(figsize=(3, 3))
ax.imshow(np.eye(5), cmap='gray')
ax.axis('off')
plt.show()""")

t('Zeige das Array `np.arange(20).reshape(4, 5)` mit `imshow()` als Bild.', NPP,
  """fig, ax = plt.subplots()
ax.imshow(np.arange(20).reshape(4, 5))
plt.show()""")
t('Zeige ein 8 × 8-Schachbrett (`(zeile + spalte) % 2` mit Broadcasting) in Schwarz-Weiß (`cmap=\'gray\'`) ohne Achsen.', NPP,
  """i = np.arange(8)
brett = (i.reshape(-1, 1) + i) % 2
fig, ax = plt.subplots()
ax.imshow(brett, cmap='gray')
ax.axis('off')
plt.show()""")
t('Zeige ein zufälliges 10 × 10-Array (`rng.random((10, 10))`) mit der Farbskala `\'hot\'` und einer Farbleiste.',
  NPP + '\nrng = np.random.default_rng(1)',
  """a = rng.random((10, 10))
fig, ax = plt.subplots()
bild = ax.imshow(a, cmap='hot')
fig.colorbar(bild, ax=ax)
plt.show()""")
t('''Zeige ein Graustufen-Bild mit einem Farbverlauf: Ein 50 × 100-Array, in dem jede Zeile die Werte `np.linspace(0, 1, 100)` enthält
(`np.tile(np.linspace(0, 1, 100), (50, 1))` wiederholt die Zeile 50-mal). Farbskala `'gray'`, ohne Achsen.''', NPP,
  """a = np.tile(np.linspace(0, 1, 100), (50, 1))
fig, ax = plt.subplots()
ax.imshow(a, cmap='gray')
ax.axis('off')
plt.show()""")
t('''Zeichne das Einmaleins (10 × 10, mit Broadcasting) als Bild mit der Farbskala `'Blues'`. Beschrifte die Achsen mit den Zahlen 1 bis 10
(`ax.set_xticks(range(10), range(1, 11))` und entsprechend für y).''', NPP,
  """z = np.arange(1, 11)
tabelle = z.reshape(-1, 1) * z
fig, ax = plt.subplots()
ax.imshow(tabelle, cmap='Blues')
ax.set_xticks(range(10), range(1, 11))
ax.set_yticks(range(10), range(1, 11))
plt.show()""")
t('''Zeige das Einmaleins wie in der vorigen Aufgabe und schreibe zusätzlich in jedes Feld seinen Wert (`ax.text(s, z, wert, ha='center', va='center')`,
Schriftgröße 7). Ohne Achsenbeschriftung (`ax.axis('off')`).''', NPP,
  """z = np.arange(1, 11)
tabelle = z.reshape(-1, 1) * z
fig, ax = plt.subplots()
ax.imshow(tabelle, cmap='Blues')
for zeile in range(10):
    for spalte in range(10):
        ax.text(spalte, zeile, tabelle[zeile, spalte], ha='center', va='center', fontsize=7)
ax.axis('off')
plt.show()""")
t('''Ein „Bild“ aus Zahlen: Erstelle ein 7 × 7-Array aus Nullen und setze mit Slicing einen Rahmen (Rand) und ein Kreuz in der Mitte (Zeile 3 und Spalte 3) auf 1.
Zeige es mit `cmap='binary'` ohne Achsen.''', NPP,
  """a = np.zeros((7, 7))
a[0] = 1
a[-1] = 1
a[:, 0] = 1
a[:, -1] = 1
a[3] = 1
a[:, 3] = 1
fig, ax = plt.subplots()
ax.imshow(a, cmap='binary')
ax.axis('off')
plt.show()""")
t('''Zeige die drei Arrays nebeneinander (Größe 9 × 3) mit den Farbskalen `'viridis'`, `'gray'` und `'coolwarm'` und diesen Namen als Titel, alle ohne Achsen.''',
  NPP + '\na = np.arange(25).reshape(5, 5)',
  """fig, axs = plt.subplots(1, 3, figsize=(9, 3))
for ax, skala in zip(axs, ['viridis', 'gray', 'coolwarm']):
    ax.imshow(a, cmap=skala)
    ax.set_title(skala)
    ax.axis('off')
plt.show()""")
predict("""import numpy as np
import matplotlib.pyplot as plt
fig, ax = plt.subplots()
ax.imshow(np.array([[0, 1], [1, 0]]), cmap='gray')
plt.show()""")

# ---------------------------------------------------------------- 6
sec('Heatmaps')
expl('''#### Tabellen als Heatmap

Eine **Heatmap** stellt eine Tabelle als farbige Kästchen dar. Mit `set_xticks()` und `set_yticks()` beschriftet man Zeilen und Spalten,
mit `ax.text()` schreibt man die Werte hinein. Bei Temperaturen oder Abweichungen passt eine Farbskala von Blau nach Rot (`'coolwarm'`).''',
     """import numpy as np
import matplotlib.pyplot as plt

noten = np.array([[2, 3, 1, 1],
                  [4, 2, 3, 2],
                  [1, 2, 2, 1]])
namen = ['Anna', 'Ben', 'Cem']
faecher = ['Mathe', 'Deutsch', 'Englisch', 'Info']
fig, ax = plt.subplots()
bild = ax.imshow(noten, cmap='RdYlGn_r', vmin=1, vmax=6)
ax.set_xticks(range(4), faecher)
ax.set_yticks(range(3), namen)
for z in range(3):
    for s in range(4):
        ax.text(s, z, noten[z, s], ha='center', va='center')
fig.colorbar(bild, ax=ax)
plt.show()""")

TW = NPP + """
tage = ['Mo', 'Di', 'Mi', 'Do', 'Fr', 'Sa', 'So']
uhrzeiten = ['8 Uhr', '12 Uhr', '16 Uhr', '20 Uhr']
temp = np.array([[ 8, 14, 16, 11],
                 [ 7, 12, 15, 10],
                 [10, 17, 19, 13],
                 [ 9, 16, 18, 12],
                 [11, 18, 21, 15],
                 [12, 20, 22, 16],
                 [ 9, 13, 14, 10]])"""
t('Zeige die Temperaturtabelle als Heatmap mit der Farbskala `\'coolwarm\'` und einer Farbleiste.', TW,
  """fig, ax = plt.subplots()
bild = ax.imshow(temp, cmap='coolwarm')
fig.colorbar(bild, ax=ax)
plt.show()""")
t('Zeige die Heatmap mit den Tagen als Zeilen- und den Uhrzeiten als Spaltenbeschriftung.', TW,
  """fig, ax = plt.subplots()
ax.imshow(temp, cmap='coolwarm')
ax.set_xticks(range(4), uhrzeiten)
ax.set_yticks(range(7), tage)
plt.show()""")
t('Zeige die beschriftete Heatmap und schreibe zusätzlich die Temperaturen in die Kästchen.', TW,
  """fig, ax = plt.subplots()
ax.imshow(temp, cmap='coolwarm')
ax.set_xticks(range(4), uhrzeiten)
ax.set_yticks(range(7), tage)
for z in range(7):
    for s in range(4):
        ax.text(s, z, temp[z, s], ha='center', va='center')
plt.show()""")
t('''Zeige die Heatmap der **Abweichungen** vom Mittelwert der ganzen Tabelle (`temp - temp.mean()`) mit `'coolwarm'`. Damit 0 genau in der Mitte der Skala liegt,
setze `vmin=-8` und `vmax=8`. Mit Farbleiste und den Beschriftungen wie oben.''', TW,
  """fig, ax = plt.subplots()
bild = ax.imshow(temp - temp.mean(), cmap='coolwarm', vmin=-8, vmax=8)
ax.set_xticks(range(4), uhrzeiten)
ax.set_yticks(range(7), tage)
fig.colorbar(bild, ax=ax)
plt.show()""")
t('''Zeige die Korrelationsmatrix der drei Größen (`np.corrcoef([groesse, gewicht, schuh])`) als Heatmap mit `'coolwarm'`, `vmin=-1`, `vmax=1`,
den Namen als Beschriftung und den Werten (zwei Nachkommastellen, f-String mit `:.2f`) in den Kästchen.''',
  NPP + "\ngroesse = [158, 162, 165, 170, 172, 175, 180, 185]\ngewicht = [52, 58, 57, 65, 68, 70, 77, 82]\nschuh = [37, 39, 38, 41, 42, 42, 44, 45]\nnamen = ['Größe', 'Gewicht', 'Schuh']",
  """k = np.corrcoef([groesse, gewicht, schuh])
fig, ax = plt.subplots()
ax.imshow(k, cmap='coolwarm', vmin=-1, vmax=1)
ax.set_xticks(range(3), namen)
ax.set_yticks(range(3), namen)
for z in range(3):
    for s in range(3):
        ax.text(s, z, f'{k[z, s]:.2f}', ha='center', va='center')
plt.show()""")
t('''Zeige als Heatmap, wie oft jede Kombination zweier Würfel vorkommt: Würfle `rng.integers(1, 7, size=(3600, 2))`, zähle in einem 6 × 6-Array mit einer Schleife
(`zaehler[a - 1, b - 1] += 1`) und zeige es mit `'Greens'`, Farbleiste und den Augenzahlen 1 bis 6 als Beschriftung.''',
  NPP + '\nrng = np.random.default_rng(4)',
  """w = rng.integers(1, 7, size=(3600, 2))
zaehler = np.zeros((6, 6), dtype=int)
for a, b in w:
    zaehler[a - 1, b - 1] += 1
fig, ax = plt.subplots()
bild = ax.imshow(zaehler, cmap='Greens')
ax.set_xticks(range(6), range(1, 7))
ax.set_yticks(range(6), range(1, 7))
fig.colorbar(bild, ax=ax)
plt.show()""")

# ---------------------------------------------------------------- 7
sec('Spielfelder')
expl('''#### Eigene Farben für Spielfelder

Für Spielfelder will man oft genau festgelegte Farben, z. B. 0 = Weg (weiß), 1 = Wand (schwarz), 2 = Ziel (grün).
`ListedColormap(['white', 'black', 'green'])` aus `matplotlib.colors` ist eine Farbskala mit genau diesen Farben.
Mit `vmin=0` und `vmax=2` gehört dann jede Zahl zu einer Farbe.

Ein Spielfeld aus Zeichenketten wandelt man vorher mit numpy in Zahlen um (z. B. mit Masken).''',
     """import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap

karte = np.array([list('#######'),
                  list('#S..#.#'),
                  list('#.#...#'),
                  list('#...#Z#'),
                  list('#######')])
feld = np.zeros(karte.shape)
feld[karte == '#'] = 1
feld[karte == 'S'] = 2
feld[karte == 'Z'] = 3
farben = ListedColormap(['white', 'black', 'blue', 'green'])
fig, ax = plt.subplots()
ax.imshow(feld, cmap=farben, vmin=0, vmax=3)
ax.axis('off')
plt.show()""")

LAB = NPP + "\nfrom matplotlib.colors import ListedColormap\nkarte = np.array([list('##########'), list('#S.....#.#'), list('#.###.##.#'), list('#...#....#'), list('###.#.##.#'), list('#...#..#Z#'), list('##########')])"
t('Zeige das Labyrinth mit `imshow()`: Wände (`#`) schwarz, alles andere weiß (`cmap=\'binary\'` mit 1 für Wände). Ohne Achsen.', LAB,
  """feld = (karte == '#').astype(int)
fig, ax = plt.subplots()
ax.imshow(feld, cmap='binary')
ax.axis('off')
plt.show()""")
t('Zeige das Labyrinth mit eigenen Farben: Weg hellgrau, Wand dunkelblau, Start orange, Ziel grün (Zahlen 0 bis 3). Ohne Achsen.', LAB,
  """feld = np.zeros(karte.shape)
feld[karte == '#'] = 1
feld[karte == 'S'] = 2
feld[karte == 'Z'] = 3
fig, ax = plt.subplots()
ax.imshow(feld, cmap=ListedColormap(['lightgray', 'darkblue', 'orange', 'green']), vmin=0, vmax=3)
ax.axis('off')
plt.show()""")
t('''Zeichne ein Tic-Tac-Toe-Feld: Zeige ein 3 × 3-Array aus Einsen mit `cmap='Pastel1'` ohne Achsen und schreibe mit `ax.text()` die Zeichen aus `feld`
in die Kästchen (Schriftgröße 40, mittig).''',
  NPP + "\nfeld = np.array([list('XO.'), list('.XO'), list('O.X')])",
  """fig, ax = plt.subplots(figsize=(3, 3))
ax.imshow(np.ones((3, 3)), cmap='Pastel1')
for z in range(3):
    for s in range(3):
        if feld[z, s] != '.':
            ax.text(s, z, feld[z, s], ha='center', va='center', fontsize=40)
ax.axis('off')
plt.show()""")
t('''Zeige ein zufälliges 20 × 20-Feld aus „Bäumen“ (1) und „Wiese“ (0) mit `rng.random((20, 20)) < 0.4` in den Farben `'yellowgreen'` und `'darkgreen'`. Ohne Achsen.''',
  NPP + '\nfrom matplotlib.colors import ListedColormap\nrng = np.random.default_rng(5)',
  """wald = (rng.random((20, 20)) < 0.4).astype(int)
fig, ax = plt.subplots()
ax.imshow(wald, cmap=ListedColormap(['yellowgreen', 'darkgreen']))
ax.axis('off')
plt.show()""")
t('''**Game of Life:** Zeige den Gleiter in fünf Schritten nebeneinander (Größe 10 × 2, `cmap='binary'`, ohne Achsen, Titel `Schritt 0` bis `Schritt 4`).
Die Funktion `schritt()` ist vorgegeben (siehe *numpy: Zweidimensionale Arrays*).''',
  NPP + '''

def schritt(zellen):
    z, s = zellen.shape
    p = np.pad(zellen, 1)
    n = np.zeros((z, s), dtype=int)
    for dz in range(3):
        for ds in range(3):
            if dz != 1 or ds != 1:
                n += p[dz:dz + z, ds:ds + s]
    return (((zellen == 1) & ((n == 2) | (n == 3))) | ((zellen == 0) & (n == 3))).astype(int)

zellen = np.zeros((6, 6), dtype=int)
zellen[0, 1] = 1
zellen[1, 2] = 1
zellen[2, 0:3] = 1''',
  """fig, axs = plt.subplots(1, 5, figsize=(10, 2))
for i, ax in enumerate(axs):
    ax.imshow(zellen, cmap='binary')
    ax.set_title(f'Schritt {i}')
    ax.axis('off')
    zellen = schritt(zellen)
plt.show()""")
t('''**Minesweeper:** Zeige die Anzahl benachbarter Minen als Bild mit `'Oranges'` und schreibe die Zahlen hinein. Die Minen selbst sollen als `*` erscheinen.''',
  NPP + '\nminen = np.array([[0, 1, 0, 0, 0],\n                  [0, 0, 0, 1, 0],\n                  [1, 0, 0, 0, 0],\n                  [0, 0, 1, 0, 1]])',
  """z, s = minen.shape
p = np.pad(minen, 1)
anzahl = np.zeros((z, s), dtype=int)
for dz in range(3):
    for ds in range(3):
        if dz != 1 or ds != 1:
            anzahl += p[dz:dz + z, ds:ds + s]
fig, ax = plt.subplots()
ax.imshow(anzahl, cmap='Oranges')
for i in range(z):
    for j in range(s):
        ax.text(j, i, '*' if minen[i, j] else anzahl[i, j], ha='center', va='center', fontsize=16)
ax.axis('off')
plt.show()""")

# ---------------------------------------------------------------- 8
sec('Höhenlinien')
expl('''#### `np.meshgrid()`

Für eine Funktion mit **zwei** Variablen `f(x, y)` braucht man den Funktionswert an jedem Punkt eines Rasters.
`X, Y = np.meshgrid(x, y)` macht aus den Achsenwerten `x` und `y` zwei 2D-Arrays: `X` enthält in jeder Zeile die x-Werte, `Y` in jeder Spalte die y-Werte.
Dann berechnet man `Z = f(X, Y)` für alle Punkte auf einmal.''',
     """import numpy as np

x = np.array([0, 1, 2])
y = np.array([10, 20])
X, Y = np.meshgrid(x, y)
print(X)
print(Y)
print(X + Y)""")
expl('''#### `ax.contour()` und `ax.contourf()`

- `ax.contour(X, Y, Z)` zeichnet **Höhenlinien**: Linien, auf denen `Z` denselben Wert hat (wie auf einer Wanderkarte).
  `levels=10` legt die Anzahl fest, eine Liste die Werte selbst. `ax.clabel(linien)` schreibt die Werte an die Linien.
- `ax.contourf(X, Y, Z)` färbt die Flächen zwischen den Linien (*filled*). Mit `fig.colorbar()` bekommt man die Farbleiste.''',
     """import numpy as np
import matplotlib.pyplot as plt

x = np.linspace(-2, 2, 100)
X, Y = np.meshgrid(x, x)
Z = X ** 2 + Y ** 2
fig, axs = plt.subplots(1, 2, figsize=(9, 4), layout='constrained')
linien = axs[0].contour(X, Y, Z, levels=[0.5, 1, 2, 3, 4])
axs[0].clabel(linien)
axs[0].set_aspect('equal')
flaechen = axs[1].contourf(X, Y, Z, levels=10, cmap='viridis')
fig.colorbar(flaechen, ax=axs[1])
axs[1].set_aspect('equal')
plt.show()""")

GR = NPP + '\nx = np.linspace(-3, 3, 200)\nX, Y = np.meshgrid(x, x)'
t('Gib `X` und `Y` von `np.meshgrid(np.arange(3), np.arange(4))` aus und darunter ihre Form.', 'import numpy as np',
  """X, Y = np.meshgrid(np.arange(3), np.arange(4))
print(X)
print(Y)
print(X.shape)""")
t('Zeichne die Höhenlinien von `f(x, y) = x² + y²` mit 8 Höhenlinien und gleichen Einheiten.', GR,
  """Z = X ** 2 + Y ** 2
fig, ax = plt.subplots()
ax.contour(X, Y, Z, levels=8)
ax.set_aspect('equal')
plt.show()""")
t('Zeichne die gefärbten Höhenlinien von `f(x, y) = x² - y²` (Sattel) mit 15 Stufen, der Farbskala `\'coolwarm\'` und einer Farbleiste.', GR,
  """Z = X ** 2 - Y ** 2
fig, ax = plt.subplots()
flaechen = ax.contourf(X, Y, Z, levels=15, cmap='coolwarm')
fig.colorbar(flaechen, ax=ax)
ax.set_aspect('equal')
plt.show()""")
t('Zeichne die Höhenlinien von `f(x, y) = sin(x) · cos(y)` bei den Werten -0.5, 0, 0.5 und beschrifte sie mit `clabel()`.', GR,
  """Z = np.sin(X) * np.cos(Y)
fig, ax = plt.subplots()
linien = ax.contour(X, Y, Z, levels=[-0.5, 0, 0.5])
ax.clabel(linien)
ax.set_aspect('equal')
plt.show()""")
t('''Zeichne einen „Berg“ mit zwei Gipfeln: `Z = np.exp(-((X - 1)**2 + Y**2)) + 0.6 * np.exp(-((X + 1.2)**2 + (Y - 1)**2))`.
Gefärbte Flächen (`'terrain'`, 20 Stufen) und darüber schwarze Höhenlinien (10 Stufen, `colors='black'`, `linewidths=0.5`), gleiche Einheiten.''', GR,
  """Z = np.exp(-((X - 1) ** 2 + Y ** 2)) + 0.6 * np.exp(-((X + 1.2) ** 2 + (Y - 1) ** 2))
fig, ax = plt.subplots()
ax.contourf(X, Y, Z, levels=20, cmap='terrain')
ax.contour(X, Y, Z, levels=10, colors='black', linewidths=0.5)
ax.set_aspect('equal')
plt.show()""")
t('''Zeige dieselbe Funktion wie in der vorigen Aufgabe mit `imshow()` (`cmap='terrain'`, `origin='lower'`, `extent=(-3, 3, -3, 3)`, damit die Achsen stimmen).''', GR,
  """Z = np.exp(-((X - 1) ** 2 + Y ** 2)) + 0.6 * np.exp(-((X + 1.2) ** 2 + (Y - 1) ** 2))
fig, ax = plt.subplots()
ax.imshow(Z, cmap='terrain', origin='lower', extent=(-3, 3, -3, 3))
plt.show()""")
predict("""import numpy as np
X, Y = np.meshgrid(np.arange(2), np.arange(3))
print((X * 10 + Y).shape)
print(X * 10 + Y)""")

# ---------------------------------------------------------------- 9
sec('Gemischte Übungen')
t('''Erstelle ein **Wetter-Dashboard** (2 × 2, Größe 9 × 6, `layout='constrained'`, Überschrift `Wetter der Woche`):
oben links die Temperaturen als Linie mit Kreisen, oben rechts der Regen als Balken, unten links ein Kreisdiagramm der Wetterarten,
unten rechts die Temperaturen der Tage nach Uhrzeit als Heatmap (`'coolwarm'`). Titel: `Temperatur`, `Regen`, `Wetter`, `Tagesverlauf`.''',
  NPP + """
tage = ['Mo', 'Di', 'Mi', 'Do', 'Fr', 'Sa', 'So']
temperatur = [12, 15, 14, 18, 21, 19, 16]
regen = [0, 2.5, 8, 1, 0, 0, 4.5]
wetter = ['sonnig', 'bewölkt', 'Regen']
anzahl = [3, 2, 2]
verlauf = np.array([[8, 14, 11], [7, 12, 10], [10, 17, 13], [9, 16, 12], [11, 18, 15], [12, 20, 16], [9, 13, 10]])""",
  """fig, axs = plt.subplots(2, 2, figsize=(9, 6), layout='constrained')
axs[0, 0].plot(tage, temperatur, marker='o')
axs[0, 0].set_title('Temperatur')
axs[0, 1].bar(tage, regen)
axs[0, 1].set_title('Regen')
axs[1, 0].pie(anzahl, labels=wetter, autopct='%1.0f%%')
axs[1, 0].set_title('Wetter')
axs[1, 1].imshow(verlauf, cmap='coolwarm')
axs[1, 1].set_yticks(range(7), tage)
axs[1, 1].set_title('Tagesverlauf')
fig.suptitle('Wetter der Woche')
plt.show()""")
t('''Zeichne eine **Funktionsuntersuchung** in drei Diagrammen untereinander mit gemeinsamer x-Achse (Größe 6 × 7): `f(x) = x³ - 3x`, `f'(x) = 3x² - 3` und
`f''(x) = 6x` von -2.5 bis 2.5 (200 Punkte), Titel `f`, `f'`, `f''`, in jedem Diagramm eine schwarze Linie bei y = 0 und graue gestrichelte Linien bei x = -1 und x = 1.''', NPP,
  """x = np.linspace(-2.5, 2.5, 200)
fig, axs = plt.subplots(3, 1, figsize=(6, 7), sharex=True, layout='constrained')
for ax, y, name in zip(axs, [x ** 3 - 3 * x, 3 * x ** 2 - 3, 6 * x], ['f', "f'", "f''"]):
    ax.plot(x, y)
    ax.axhline(0, color='black')
    ax.axvline(-1, color='gray', linestyle='--')
    ax.axvline(1, color='gray', linestyle='--')
    ax.set_title(name)
plt.show()""")
t('''Zeige ein „Pixelbild“: Das Array `smiley` (8 × 8) enthält 0 für Hintergrund, 1 für Gesicht und 2 für Augen und Mund.
Zeige es mit den Farben `'white'`, `'gold'` und `'black'` ohne Achsen.''',
  NPP + '\nfrom matplotlib.colors import ListedColormap\nsmiley = np.array([[0, 0, 1, 1, 1, 1, 0, 0],\n                   [0, 1, 1, 1, 1, 1, 1, 0],\n                   [1, 1, 2, 1, 1, 2, 1, 1],\n                   [1, 1, 1, 1, 1, 1, 1, 1],\n                   [1, 2, 1, 1, 1, 1, 2, 1],\n                   [1, 1, 2, 2, 2, 2, 1, 1],\n                   [0, 1, 1, 1, 1, 1, 1, 0],\n                   [0, 0, 1, 1, 1, 1, 0, 0]])',
  """fig, ax = plt.subplots(figsize=(3, 3))
ax.imshow(smiley, cmap=ListedColormap(['white', 'gold', 'black']))
ax.axis('off')
plt.show()""")
t('''Zeichne die **Ausbreitung einer Welle**: vier Diagramme im 2 × 2-Raster mit gemeinsamen Achsen. Diagramm `k` (k = 0 bis 3) zeigt die gefärbten Höhenlinien von
`np.sin(np.sqrt(X**2 + Y**2) - k)` für x und y von -6 bis 6 (200 Punkte), `cmap='Blues'`, Titel `t = 0` bis `t = 3`, gleiche Einheiten.''', NPP,
  """x = np.linspace(-6, 6, 200)
X, Y = np.meshgrid(x, x)
r = np.sqrt(X ** 2 + Y ** 2)
fig, axs = plt.subplots(2, 2, sharex=True, sharey=True, layout='constrained')
for k, ax in enumerate(axs.flat):
    ax.contourf(X, Y, np.sin(r - k), cmap='Blues')
    ax.set_title(f't = {k}')
    ax.set_aspect('equal')
plt.show()""")
t('''Vergleiche Verteilungen in einem 1 × 3-Raster (Größe 10 × 3): Histogramm, Boxplot und sortierte Werte (`np.sort()` als Linie) derselben Daten
`rng.normal(50, 10, size=200)`. Titel: `Histogramm`, `Boxplot`, `sortiert`.''',
  NPP + '\nrng = np.random.default_rng(6)',
  """daten = rng.normal(50, 10, size=200)
fig, axs = plt.subplots(1, 3, figsize=(10, 3), layout='constrained')
axs[0].hist(daten, bins=20)
axs[0].set_title('Histogramm')
axs[1].boxplot(daten)
axs[1].set_title('Boxplot')
axs[2].plot(np.sort(daten))
axs[2].set_title('sortiert')
plt.show()""")
t('Gestalte ein eigenes Diagramm-Raster mit mindestens drei verschiedenen Diagrammtypen zu einem Thema deiner Wahl.', NPP,
  """x = np.linspace(0, 10, 100)
fig, axs = plt.subplots(1, 3, figsize=(10, 3), layout='constrained')
axs[0].plot(x, np.sqrt(x))
axs[1].bar(['A', 'B', 'C'], [3, 5, 2])
axs[2].imshow(np.arange(16).reshape(4, 4))
plt.show()""", kind='free')

generate('matplotlib_layout', 'matplotlib: Layout, Bilder und Heatmaps', INTRO)
