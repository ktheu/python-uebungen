# Erzeugt ../content/scipy_anwendungen.ipynb (siehe nbgen.py). Viertes Notebook der scipy-Reihe:
# scipy_analysis, scipy_daten, scipy_stochastik, scipy_anwendungen.
#
# JupyterLite: scipy 1.18.0 (mit numpy 2.4.6), lokal in einer py-3.13-venv: pip install scipy==1.18.0 numpy==2.4.6 matplotlib==3.10.8
#     python generator/gen_scipy_anwendungen.py
#     py -3.13 generator/pyodide_check/pruefen.py generator/gen_scipy_anwendungen.py
#
# Fallstricke:
# - solve_ivp() rechnet ohne Angabe nur auf etwa 3 Stellen genau -> immer rtol=1e-8, atol=1e-8 (im Notebook erklärt).
# - linprog(): Variablen mit dem Wert 0 erscheinen manchmal als -0. -> Aufgaben so wählen, dass alle Werte positiv sind.
# - KDTree.query() liefert numpy-Zahlen (Indizes int64 lokal, int32 in Pyodide) -> nie als Tupel ausgeben.
# - Konvexe Hüllen und Voronoi-Diagramme gibt es im shapely-Notebook (mengen_konstruktionen), hier nicht.
# - Zahlen werden mit f-Strings ausgegeben (f'{x:.4f}'), Arrays mit np.round().
import re

from nbgen import sec, expl, task, predict, generate


def t(text, given='', body='', kind='normal'):
    """Aufgabe, deren Lösung aus dem vorgegebenen Code plus body besteht."""
    loesung = (given + '\n' + body) if given else body
    task(text, given=given, solution=re.sub(r'\n{3,}', '\n\n', loesung), kind=kind)  # höchstens eine Leerzeile


NP_INT = 'import numpy as np\nfrom scipy import integrate'
NP_OPT = 'import numpy as np\nfrom scipy import optimize'
NP_SP = 'import numpy as np\nfrom scipy import spatial'

INTRO = '''Im letzten Notebook der Reihe setzt du **scipy** für Anwendungen ein: Vorgänge, bei denen man die **Änderungsrate** kennt
(Wachstum, Abkühlung, Räuber und Beute, Ausbreitung einer Krankheit), Planungsaufgaben mit **linearer Optimierung**,
**Abstände** und nächste Nachbarn zwischen vielen Punkten sowie Naturkonstanten und Einheiten.

Die Reihe hat vier Notebooks:

1. Analysis: Nullstellen, Gleichungen, Extremstellen, Integrale
2. Messdaten auswerten: Interpolation, Ausgleichskurven, Spitzen finden
3. Stochastik: Verteilungen und Hypothesentests
4. **Anwendungen**: Änderungsraten und Modelle, lineare Optimierung, Abstände (dieses Notebook)

Vorausgesetzt werden *scipy: Analysis*, *numpy: Zweidimensionale Arrays* und *matplotlib: Grundlagen*.

Jeder Abschnitt beginnt mit kurzen Erklärungen und Beispielen. Führe die Beispiele aus und probiere sie ruhig ein wenig aus.
Danach folgen viele kleine Übungen. Wenn etwas vorgegeben ist, steht es schon in der Codezelle.

Beim ersten `import scipy` lädt der Browser das Paket nach. Das dauert ein paar Sekunden.'''

GENAU = 'rtol=1e-8, atol=1e-8'

# ---------------------------------------------------------------- 1
sec('Änderungsraten: solve_ivp')
expl('''#### Von der Änderungsrate zum Verlauf

Oft weiß man nicht, wie sich eine Größe `y` im Lauf der Zeit verhält, sondern nur, **wie schnell sie sich ändert**. Bei einer Bakterienkultur
wächst die Anzahl pro Stunde um 30 % des aktuellen Bestands: Die Änderungsrate ist `y' = 0.3 · y`. Eine solche Gleichung,
in der die Ableitung vorkommt, heißt **Differentialgleichung**.

`integrate.solve_ivp(f, (t0, t1), [y0])` berechnet den Verlauf schrittweise (*solve initial value problem*, Anfangswertproblem):

- `f(t, y)` ist eine Funktion, die zu Zeit `t` und Bestand `y` die **Änderungsrate** zurückgibt. Sie muss `t` als ersten Parameter haben,
  auch wenn sie ihn nicht benutzt.
- `(t0, t1)` ist der Zeitraum, `[y0]` der **Anfangsbestand** (als Liste, weil es auch mehrere Größen sein können, siehe Abschnitt 3).
- `t_eval=[...]` gibt die Zeitpunkte an, für die man Werte haben will.

Das Ergebnis hat die Attribute `t` (die Zeitpunkte) und `y` (ein 2D-Array: Zeile 0 sind die Werte der ersten Größe).''',
     """import numpy as np
from scipy import integrate

def rate(t, y):
    return 0.3 * y

loesung = integrate.solve_ivp(rate, (0, 5), [100], t_eval=[0, 1, 2, 3, 4, 5], rtol=1e-8, atol=1e-8)
print(loesung.t)
print(np.round(loesung.y[0], 2))
print(np.round(100 * np.exp(0.3 * loesung.t), 2))""")
expl('''#### Genauigkeit: `rtol` und `atol`

`solve_ivp()` geht in kleinen Zeitschritten vor und schätzt dabei seinen Fehler. Ohne Angabe ist es nur auf etwa 3 Stellen genau
(das reicht für Diagramme). Mit `rtol=1e-8, atol=1e-8` (relativer und absoluter Fehler höchstens etwa 10⁻⁸) wird es sehr genau.
In diesem Notebook wird deshalb immer mit diesen Angaben gerechnet.''',
     """import numpy as np
from scipy import integrate

def rate(t, y):
    return 0.3 * y

grob = integrate.solve_ivp(rate, (0, 5), [100], t_eval=[5])
genau = integrate.solve_ivp(rate, (0, 5), [100], t_eval=[5], rtol=1e-8, atol=1e-8)
print(grob.y[0, 0])
print(genau.y[0, 0])
print(100 * np.exp(1.5))""")
expl('''#### Den Verlauf zeichnen

Für ein Diagramm gibt man mit `t_eval=np.linspace(t0, t1, 200)` viele Zeitpunkte an und zeichnet `loesung.y[0]` über `loesung.t`.''',
     """import numpy as np
from scipy import integrate
import matplotlib.pyplot as plt

def rate(t, y):
    return 0.3 * y

loesung = integrate.solve_ivp(rate, (0, 5), [100], t_eval=np.linspace(0, 5, 200), rtol=1e-8, atol=1e-8)
plt.plot(loesung.t, loesung.y[0])
plt.xlabel('Zeit in h')
plt.ylabel('Bakterien')
plt.show()""")

t(f'''Ein Kapital von 2000 € wächst stetig mit 4 % pro Jahr: `y' = 0.04 · y`. Berechne mit `solve_ivp()` das Kapital nach 0, 5, 10, 15 und 20 Jahren
(`{GENAU}`) und gib die Werte auf zwei Nachkommastellen aus.''', NP_INT,
  f"""

def rate(t, y):
    return 0.04 * y

loesung = integrate.solve_ivp(rate, (0, 20), [2000], t_eval=[0, 5, 10, 15, 20], {GENAU})
print(np.round(loesung.y[0], 2))""")
t('''Vergleiche das Ergebnis der vorigen Aufgabe mit der Formel `2000 · e^(0.04 t)`: Gib für dieselben Zeitpunkte die größte Abweichung aus
(mit `:.1e`).''', NP_INT,
  f"""

def rate(t, y):
    return 0.04 * y

zeiten = np.array([0, 5, 10, 15, 20])
loesung = integrate.solve_ivp(rate, (0, 20), [2000], t_eval=zeiten, {GENAU})
print(f'{{np.abs(loesung.y[0] - 2000 * np.exp(0.04 * zeiten)).max():.1e}}')""", kind='free')
t(f'''Ein radioaktiver Stoff zerfällt: `y' = -0.0866 · y` (`t` in Tagen). Zu Beginn sind 80 g vorhanden. Gib die Masse nach 8, 16 und 24 Tagen aus
(zwei Nachkommastellen, `{GENAU}`). Die Halbwertszeit ist etwa 8 Tage.''', NP_INT,
  f"""

def rate(t, y):
    return -0.0866 * y

loesung = integrate.solve_ivp(rate, (0, 24), [80], t_eval=[8, 16, 24], {GENAU})
print(np.round(loesung.y[0], 2))""")
t(f'''In einen Teich fließt ein Schadstoff mit konstant 3 kg pro Tag, gleichzeitig wird jeden Tag 10 % des vorhandenen Schadstoffs abgebaut:
`y' = 3 - 0.1 · y`. Zu Beginn sind 0 kg im Teich. Gib die Menge nach 10, 20, 50 und 100 Tagen aus (zwei Nachkommastellen, `{GENAU}`).
Welchem Wert nähert sie sich?''', NP_INT,
  f"""

def rate(t, y):
    return 3 - 0.1 * y

loesung = integrate.solve_ivp(rate, (0, 100), [0], t_eval=[10, 20, 50, 100], {GENAU})
print(np.round(loesung.y[0], 2))""")
t(f'''Die Änderungsrate darf auch von der Zeit abhängen. Ein Speicher wird mit `y' = 5 + 2 · sin(t)` (Liter pro Minute) gefüllt und enthält zu Beginn 10 Liter.
Gib die Füllmenge nach 10 Minuten aus (zwei Nachkommastellen, `{GENAU}`) und vergleiche mit dem Integral `10 + ∫ (5 + 2 sin(t)) dt` von 0 bis 10 (`quad()`).''',
  NP_INT,
  f"""

def zufluss(t):
    return 5 + 2 * np.sin(t)

def rate(t, y):
    return zufluss(t)

loesung = integrate.solve_ivp(rate, (0, 10), [10], t_eval=[10], {GENAU})
print(f'{{loesung.y[0, 0]:.2f}}')
print(f'{{10 + integrate.quad(zufluss, 0, 10)[0]:.2f}}')""")
t(f'''Zeichne das Wachstum der Bakterien (`y' = 0.3 · y`, Start 100) mit `solve_ivp()` (200 Punkte von 0 bis 10, `{GENAU}`) als blaue Linie
und die Werte nach der Formel `100 · e^(0.3 t)` für die ganzen Stunden 0 bis 10 als rote Punkte. Die Punkte sollen genau auf der Linie liegen.''',
  NP_INT + '\nimport matplotlib.pyplot as plt',
  f"""

def rate(t, y):
    return 0.3 * y

loesung = integrate.solve_ivp(rate, (0, 10), [100], t_eval=np.linspace(0, 10, 200), {GENAU})
plt.plot(loesung.t, loesung.y[0], color='blue')
stunden = np.arange(11)
plt.plot(stunden, 100 * np.exp(0.3 * stunden), 'ro')
plt.show()""")
predict(f"""from scipy import integrate

def rate(t, y):
    return 2

loesung = integrate.solve_ivp(rate, (0, 3), [5], t_eval=[0, 1, 2, 3], {GENAU})
print(loesung.y.shape)
print(loesung.y[0].round(4))""", erklaerung='''- `y` hat eine Zeile (eine Größe) und eine Spalte pro Zeitpunkt in `t_eval`: `(1, 4)`.
- Die Änderungsrate ist immer 2, der Bestand steigt also pro Zeiteinheit um 2, ausgehend von 5: `[ 5.  7.  9. 11.]`.''')

# ---------------------------------------------------------------- 2
sec('Wachstumsmodelle mit Parametern')
expl('''#### Parameter mit `args=`

Viele Modelle haben **Parameter**, z. B. die Wachstumsrate `k` und die **Kapazitätsgrenze** `G` beim **logistischen Wachstum**:
`y' = k · y · (1 - y / G)`. Am Anfang wächst der Bestand fast exponentiell, in der Nähe von `G` wird das Wachstum immer langsamer.

Die Parameter schreibt man hinter `t` und `y` in die Funktion und gibt ihre Werte wie bei `quad()` mit `args=(...)` an.''',
     """import numpy as np
from scipy import integrate

def logistisch(t, y, k, g):
    return k * y * (1 - y / g)

loesung = integrate.solve_ivp(logistisch, (0, 30), [10], t_eval=[0, 5, 10, 15, 20, 30], args=(0.4, 1000), rtol=1e-8, atol=1e-8)
print(np.round(loesung.y[0], 1))""")
expl('''#### Wann wird ein Wert erreicht? `dense_output=True`

Mit `dense_output=True` kann man die Lösung danach an **jeder** Stelle auswerten: `loesung.sol(t)` gibt ein Array mit den Werten aller Größen
zur Zeit `t`. Damit findet man mit `brentq()` aus *scipy: Analysis*, wann ein bestimmter Wert erreicht wird.''',
     """from scipy import integrate, optimize

def logistisch(t, y, k, g):
    return k * y * (1 - y / g)

loesung = integrate.solve_ivp(logistisch, (0, 30), [10], args=(0.4, 1000), dense_output=True, rtol=1e-8, atol=1e-8)
print(f'{loesung.sol(12.5)[0]:.2f}')

def h(t):
    return loesung.sol(t)[0] - 500

print(f'{optimize.brentq(h, 0, 30):.2f}')""")

L = NP_INT + f'''

def logistisch(t, y, k, g):
    return k * y * (1 - y / g)'''
t(f'''Auf einer Insel werden 20 Kaninchen ausgesetzt. Die Insel bietet Platz für 2000 Kaninchen, die Wachstumsrate ist `k = 0.8` pro Jahr.
Gib den Bestand (ganze Tiere) nach 0, 2, 4, 6, 8 und 10 Jahren aus (`{GENAU}`).''', L,
  f"""
loesung = integrate.solve_ivp(logistisch, (0, 10), [20], t_eval=[0, 2, 4, 6, 8, 10], args=(0.8, 2000), {GENAU})
print(np.round(loesung.y[0]).astype(int))""")
t(f'''Wann sind es nach dem Modell der vorigen Aufgabe 1000 Kaninchen, wann 1900? Benutze `dense_output=True` und `brentq()` im Intervall von 0 bis 20
(zwei Nachkommastellen).''', L.replace('from scipy import integrate', 'from scipy import integrate, optimize'),
  f"""
loesung = integrate.solve_ivp(logistisch, (0, 20), [20], args=(0.8, 2000), dense_output=True, {GENAU})
for ziel in [1000, 1900]:
    def h(t):
        return loesung.sol(t)[0] - ziel
    print(f'{{ziel}} {{optimize.brentq(h, 0, 20):.2f}}')""")
t(f'''Zeichne das logistische Wachstum der Kaninchen für die Wachstumsraten `k` = 0.4, 0.8 und 1.2 (jeweils 200 Punkte von 0 bis 20) in ein Diagramm
mit Legende (`k = 0.4` usw.) und der Kapazitätsgrenze als gestrichelter grauer Linie.''', L + '\nimport matplotlib.pyplot as plt',
  f"""
zeit = np.linspace(0, 20, 200)
for k in [0.4, 0.8, 1.2]:
    loesung = integrate.solve_ivp(logistisch, (0, 20), [20], t_eval=zeit, args=(k, 2000), {GENAU})
    plt.plot(loesung.t, loesung.y[0], label=f'k = {{k}}')
plt.axhline(2000, color='gray', linestyle='--')
plt.legend()
plt.show()""")
t(f'''**Abkühlung nach Newton:** Ein Kuchen kommt mit 180 °C aus dem Ofen in einen 20 °C warmen Raum. Seine Temperatur ändert sich mit
`T' = -k · (T - u)` (`u`: Raumtemperatur, `k = 0.07` pro Minute). Schreibe die Funktion mit den Parametern `k` und `u`, gib die Temperatur nach 10, 20 und 30 Minuten aus
(eine Nachkommastelle) und die Zeit, nach der der Kuchen nur noch 40 °C hat (zwei Nachkommastellen, `brentq()` zwischen 0 und 60).''',
  'import numpy as np\nfrom scipy import integrate, optimize',
  f"""

def abkuehlung(t, temp, k, u):
    return -k * (temp - u)

loesung = integrate.solve_ivp(abkuehlung, (0, 60), [180], args=(0.07, 20), dense_output=True, {GENAU})
for minute in [10, 20, 30]:
    print(f'{{minute}} {{loesung.sol(minute)[0]:.1f}}')

def h(t):
    return loesung.sol(t)[0] - 40

print(f'{{optimize.brentq(h, 0, 60):.2f}}')""")
t(f'''Ein Fischteich wird befischt: Pro Jahr werden `e` Tonnen Fisch entnommen. Das Modell ist `y' = 0.5 · y · (1 - y / 100) - e` (Start 60 Tonnen).
Gib für `e` = 5, 10 und 12 den Bestand nach 20 Jahren aus (eine Nachkommastelle, `{GENAU}`).
Je mehr entnommen wird, desto kleiner wird der Bestand, auf den sich der Teich einpendelt.''', NP_INT,
  f"""

def fischerei(t, y, e):
    return 0.5 * y * (1 - y / 100) - e

for e in [5, 10, 12]:
    loesung = integrate.solve_ivp(fischerei, (0, 20), [60], t_eval=[20], args=(e,), {GENAU})
    print(f'{{e}} {{loesung.y[0, 0]:.1f}}')""")
t(f'''Ein Medikament wird über eine Infusion mit 2 mg pro Stunde zugeführt und mit der Rate `k = 0.25` pro Stunde abgebaut: `y' = 2 - k · y` (Start 0 mg).
Gib die Menge nach 4, 8, 12 und 24 Stunden aus (zwei Nachkommastellen) und vergleiche den letzten Wert mit dem Grenzwert `2 / k`.''', NP_INT,
  f"""

def infusion(t, y, zufuhr, k):
    return zufuhr - k * y

loesung = integrate.solve_ivp(infusion, (0, 24), [0], t_eval=[4, 8, 12, 24], args=(2, 0.25), {GENAU})
print(np.round(loesung.y[0], 2))
print(2 / 0.25)""")
predict(f"""import numpy as np
from scipy import integrate

def logistisch(t, y, k, g):
    return k * y * (1 - y / g)

loesung = integrate.solve_ivp(logistisch, (0, 10), [500], t_eval=[0, 10], args=(0.5, 500), {GENAU})
print(np.round(loesung.y[0], 2))""", erklaerung='''Der Bestand startet genau an der Kapazitätsgrenze 500. Dort ist `1 - y / g = 0`, die Änderungsrate also 0.
Der Bestand bleibt die ganze Zeit 500: `[500. 500.]`.''')

# ---------------------------------------------------------------- 3
sec('Mehrere Größen: Räuber und Beute, Epidemien, Bewegungen')
expl('''#### Systeme von Änderungsraten

Hängen mehrere Größen voneinander ab, ist `y` eine Liste mit allen Größen, und die Funktion gibt eine Liste mit allen Änderungsraten zurück.

Beispiel **Räuber und Beute** (Modell von Lotka und Volterra): Hasen `h` vermehren sich und werden von Füchsen `f` gefressen,
Füchse vermehren sich, wenn es viele Hasen gibt, und sterben sonst:

- `h' = a · h - b · h · f`
- `f' = c · h · f - d · f`

`loesung.y[0]` sind dann die Hasen, `loesung.y[1]` die Füchse.''',
     """import numpy as np
from scipy import integrate
import matplotlib.pyplot as plt

def raeuber_beute(t, y, a, b, c, d):
    h, f = y
    return [a * h - b * h * f, c * h * f - d * f]

loesung = integrate.solve_ivp(raeuber_beute, (0, 40), [40, 9], t_eval=np.linspace(0, 40, 400),
                              args=(0.6, 0.03, 0.01, 0.5), rtol=1e-8, atol=1e-8)
plt.plot(loesung.t, loesung.y[0], label='Hasen')
plt.plot(loesung.t, loesung.y[1], label='Füchse')
plt.legend()
plt.show()""")
expl('''#### Bewegungen: Ort und Geschwindigkeit

Bei Bewegungen kennt man die **Beschleunigung** (die Änderungsrate der Geschwindigkeit `v`), und die Geschwindigkeit ist die Änderungsrate
des Orts `s`. Man rechnet also mit den beiden Größen `[s, v]`: `s' = v` und `v' = Beschleunigung`.

Beispiel freier Fall aus 100 m Höhe ohne Luftwiderstand: `v' = -9.81`. Die Höhe nach 2 Sekunden ist nach der Formel `100 - 9.81/2 · 2² = 80.38 m`.''',
     """from scipy import integrate

def fall(t, y):
    s, v = y
    return [v, -9.81]

loesung = integrate.solve_ivp(fall, (0, 4), [100, 0], t_eval=[0, 1, 2, 3, 4], rtol=1e-8, atol=1e-8)
print(loesung.y[0].round(3))
print(loesung.y[1].round(2))""")

RB = NP_INT + f'''

def raeuber_beute(t, y, a, b, c, d):
    h, f = y
    return [a * h - b * h * f, c * h * f - d * f]'''
t(f'''Gib für das Räuber-Beute-Modell aus dem Beispiel (Start 40 Hasen und 9 Füchse, Parameter `0.6, 0.03, 0.01, 0.5`) die Anzahl der Hasen und Füchse
nach 0, 5, 10, 15 und 20 Jahren aus (eine Nachkommastelle, `{GENAU}`).''', RB,
  f"""
loesung = integrate.solve_ivp(raeuber_beute, (0, 20), [40, 9], t_eval=[0, 5, 10, 15, 20], args=(0.6, 0.03, 0.01, 0.5), {GENAU})
print(np.round(loesung.y[0], 1))
print(np.round(loesung.y[1], 1))""")
t(f'''Bestimme im Räuber-Beute-Modell (Zeitraum 0 bis 40, 4001 Zeitpunkte) die größte Anzahl von Hasen und von Füchsen und wann sie zum ersten Mal erreicht wird
(Zeitpunkt mit einer Nachkommastelle, Anzahl mit einer Nachkommastelle).''', RB,
  f"""
loesung = integrate.solve_ivp(raeuber_beute, (0, 40), [40, 9], t_eval=np.linspace(0, 40, 4001), args=(0.6, 0.03, 0.01, 0.5), {GENAU})
for name, werte in [('Hasen', loesung.y[0]), ('Füchse', loesung.y[1])]:
    i = werte.argmax()
    print(f'{{name}} {{loesung.t[i]:.1f}} {{werte[i]:.1f}}')""")
t(f'''Zeichne für das Räuber-Beute-Modell (0 bis 40, 400 Punkte) die Füchse über den Hasen (x-Achse: Hasen, y-Achse: Füchse). Es entsteht eine geschlossene
Kurve, weil sich der Verlauf immer wiederholt. Beschrifte die Achsen und markiere den Startpunkt (40 | 9) als roten Punkt.''',
  RB + '\nimport matplotlib.pyplot as plt',
  f"""
loesung = integrate.solve_ivp(raeuber_beute, (0, 40), [40, 9], t_eval=np.linspace(0, 40, 400), args=(0.6, 0.03, 0.01, 0.5), {GENAU})
plt.plot(loesung.y[0], loesung.y[1])
plt.plot(40, 9, 'ro')
plt.xlabel('Hasen')
plt.ylabel('Füchse')
plt.show()""")
SIR = NP_INT + f'''

def sir(t, y, beta, gamma):
    s, i, r = y
    return [-beta * s * i, beta * s * i - gamma * i, gamma * i]'''
t(f'''**Ausbreitung einer Krankheit (SIR-Modell):** Die Anteile der Bevölkerung sind `s` (noch nicht erkrankt), `i` (gerade krank, ansteckend) und `r` (genesen).
Mit der Ansteckungsrate `β = 0.3` und der Genesungsrate `γ = 0.1` pro Tag gilt das Modell in der Zelle. Zu Beginn sind 1 % krank (`[0.99, 0.01, 0]`).
Gib die drei Anteile nach 0, 30, 60, 90 und 120 Tagen zeilenweise mit ihrem Namen aus (4 Nachkommastellen, `{GENAU}`).''', SIR,
  f"""
loesung = integrate.solve_ivp(sir, (0, 120), [0.99, 0.01, 0], t_eval=[0, 30, 60, 90, 120], args=(0.3, 0.1), {GENAU})
for name, werte in zip(['s', 'i', 'r'], loesung.y):
    print(name, np.round(werte, 4))""")
t(f'''Bestimme im SIR-Modell (0 bis 160 Tage, 1601 Zeitpunkte) den Tag mit den meisten Kranken und ihren Anteil (eine bzw. 4 Nachkommastellen) und den Anteil,
der am Ende nie krank war. Wiederhole das mit der halben Ansteckungsrate `β = 0.15` (z. B. durch Abstandsregeln).''', SIR,
  f"""
zeit = np.linspace(0, 160, 1601)
for beta in [0.3, 0.15]:
    loesung = integrate.solve_ivp(sir, (0, 160), [0.99, 0.01, 0], t_eval=zeit, args=(beta, 0.1), {GENAU})
    i = loesung.y[1].argmax()
    print(f'{{beta}} {{loesung.t[i]:.1f}} {{loesung.y[1, i]:.4f}} {{loesung.y[0, -1]:.4f}}')""")
t(f'''Zeichne die drei Anteile des SIR-Modells mit `β = 0.3` (0 bis 160 Tage, 400 Punkte) in ein Diagramm: `s` blau, `i` rot, `r` grün, mit Legende
(`nicht erkrankt`, `krank`, `genesen`) und der x-Achsen-Beschriftung `Tage`.''', SIR + '\nimport matplotlib.pyplot as plt',
  f"""
loesung = integrate.solve_ivp(sir, (0, 160), [0.99, 0.01, 0], t_eval=np.linspace(0, 160, 400), args=(0.3, 0.1), {GENAU})
plt.plot(loesung.t, loesung.y[0], color='blue', label='nicht erkrankt')
plt.plot(loesung.t, loesung.y[1], color='red', label='krank')
plt.plot(loesung.t, loesung.y[2], color='green', label='genesen')
plt.xlabel('Tage')
plt.legend()
plt.show()""")
t(f'''**Fall mit Luftwiderstand:** Ein Fallschirmspringer (80 kg) fällt aus dem Stand. Mit Luftwiderstand ist `v' = -9.81 + 0.25 / 80 · v²`
(`v` ist negativ, weil es nach unten geht). Gib die Geschwindigkeit in km/h nach 5, 10, 20 und 30 Sekunden aus (eine Nachkommastelle, `{GENAU}`)
und die Grenzgeschwindigkeit `√(9.81 · 80 / 0.25)` in km/h.''', NP_INT,
  f"""

def fall(t, y):
    s, v = y
    return [v, -9.81 + 0.25 / 80 * v ** 2]

loesung = integrate.solve_ivp(fall, (0, 30), [4000, 0], t_eval=[5, 10, 20, 30], {GENAU})
print(np.round(-loesung.y[1] * 3.6, 1))
print(f'{{np.sqrt(9.81 * 80 / 0.25) * 3.6:.1f}}')""")
t(f'''Ein Ball wird aus 2 m Höhe mit 15 m/s senkrecht nach oben geworfen (Höhe `s`, Geschwindigkeit `v`, `v' = -9.81`). Wann landet er auf dem Boden?
Benutze `dense_output=True` und `brentq()` für die Höhe 0 im Intervall von 1 bis 5 und gib auch die Aufprallgeschwindigkeit aus (zwei Nachkommastellen).''',
  'import numpy as np\nfrom scipy import integrate, optimize',
  f"""

def wurf(t, y):
    s, v = y
    return [v, -9.81]

loesung = integrate.solve_ivp(wurf, (0, 5), [2, 15], dense_output=True, {GENAU})

def hoehe(t):
    return loesung.sol(t)[0]

landung = optimize.brentq(hoehe, 1, 5)
print(f'{{landung:.2f}}')
print(f'{{loesung.sol(landung)[1]:.2f}}')""")
t(f'''**Federpendel:** Eine Masse an einer Feder schwingt. Für die Auslenkung `x` und die Geschwindigkeit `v` gilt `x' = v` und `v' = -4 · x - 0.2 · v`
(die Feder zieht zurück, die Reibung bremst). Start: `x = 1`, `v = 0`. Zeichne die Auslenkung für 0 bis 30 Sekunden (600 Punkte, `{GENAU}`) und
gib die Zeitpunkte der ersten drei Maxima nach dem Start aus (mit `signal.find_peaks()` aus *scipy: Messdaten*, zwei Nachkommastellen).''',
  NP_INT + '\nfrom scipy import signal\nimport matplotlib.pyplot as plt',
  f"""

def feder(t, y):
    x, v = y
    return [v, -4 * x - 0.2 * v]

loesung = integrate.solve_ivp(feder, (0, 30), [1, 0], t_eval=np.linspace(0, 30, 600), {GENAU})
spitzen = signal.find_peaks(loesung.y[0])[0]
print(np.round(loesung.t[spitzen[:3]], 2))
plt.plot(loesung.t, loesung.y[0])
plt.show()""")
predict(f"""from scipy import integrate

def bewegung(t, y):
    s, v = y
    return [v, 0]

loesung = integrate.solve_ivp(bewegung, (0, 4), [10, 3], t_eval=[0, 2, 4], {GENAU})
print(loesung.y.round(2))""", erklaerung='''Die Beschleunigung ist 0, die Geschwindigkeit bleibt also 3 (zweite Zeile). Der Ort startet bei 10 und nimmt pro Sekunde um 3 zu:
10, 16, 22 (erste Zeile). Ausgabe: `[[10. 16. 22.]` und `[ 3.  3.  3.]]`.''')

# ---------------------------------------------------------------- 4
sec('Lineare Optimierung')
expl('''#### `optimize.linprog()`

Eine Firma stellt zwei Produkte her und will den Gewinn maximieren. Die Produktion ist durch **Nebenbedingungen** begrenzt (Maschinenzeit, Material).
Sind Gewinn und Nebenbedingungen **linear** (keine Quadrate, keine Produkte der Variablen), heißt das **lineare Optimierung**.

`optimize.linprog(c, A_ub=A, b_ub=b, bounds=...)` sucht die Werte `x`, für die `c · x` (die Summe `c[0]·x[0] + c[1]·x[1] + ...`) **möglichst klein** ist,
unter den Bedingungen `A · x ≤ b` (jede Zeile von `A` mit `b` ist eine Ungleichung, *ub* heißt *upper bound*).
`bounds` gibt für jede Variable den Bereich als Tupel an, `(0, None)` heißt „mindestens 0, nach oben unbegrenzt“ (das ist auch der Standard).

Um zu **maximieren**, minimiert man `-c` und nimmt beim Ergebnis das Vorzeichen zurück. Das Ergebnis hat die Attribute `x` (die beste Lösung),
`fun` (der Wert von `c · x` dort) und `success` (ob eine Lösung gefunden wurde).

Beispiel: Tische bringen 30 € Gewinn, Stühle 40 €. Ein Tisch braucht 2 h Tischlerei und 4 h Lackiererei, ein Stuhl 3 h und 2 h.
Pro Woche hat die Tischlerei 120 h, die Lackiererei 160 h.''',
     """import numpy as np
from scipy import optimize

gewinn = np.array([30, 40])
A = np.array([[2, 3],      # Tischlerei
              [4, 2]])     # Lackiererei
b = np.array([120, 160])
ergebnis = optimize.linprog(-gewinn, A_ub=A, b_ub=b, bounds=[(0, None), (0, None)])
print(ergebnis.success)
print(ergebnis.x)
print(-ergebnis.fun)""")
expl('''#### Gleichungen, Mindestwerte und ganze Zahlen

- **Mindestwerte** („mindestens 20 Stück“) schreibt man als `≤`-Bedingung mit umgedrehtem Vorzeichen: `-x ≤ -20`, oder direkt in `bounds`: `(20, None)`.
- **Gleichungen** gibt man mit `A_eq=` und `b_eq=` an.
- Müssen die Lösungen **ganze Zahlen** sein (Stückzahlen), gibt man `integrality=[1, 1]` an (1 für jede ganzzahlige Variable).''',
     """from scipy import optimize

# Minimale Kosten: Futtermischung aus zwei Sorten (Preise 3 € und 2 € pro kg)
# mindestens 12 Einheiten Eiweiß (Sorte 1: 4, Sorte 2: 1 pro kg), mindestens 9 Einheiten Fett (1 und 3 pro kg)
ergebnis = optimize.linprog([3, 2], A_ub=[[-4, -1], [-1, -3]], b_ub=[-12, -9])
print(f'{ergebnis.x.round(4)} {ergebnis.fun:.4f}')
ganz = optimize.linprog([3, 2], A_ub=[[-4, -1], [-1, -3]], b_ub=[-12, -9], integrality=[1, 1])
print(ganz.x, ganz.fun)""")

t('''Eine Bäckerei backt Brote (Gewinn 1.50 €) und Kuchen (Gewinn 4 €). Ein Brot braucht 0.5 kg Mehl und 10 Minuten Ofenzeit, ein Kuchen 0.3 kg Mehl und 40 Minuten.
Pro Tag sind 60 kg Mehl und 3000 Minuten Ofenzeit verfügbar. Wie viele Brote und Kuchen bringen den größten Gewinn? Gib `x` und den Gewinn aus.''', NP_OPT,
  """gewinn = np.array([1.5, 4])
A = np.array([[0.5, 0.3], [10, 40]])
b = np.array([60, 3000])
e = optimize.linprog(-gewinn, A_ub=A, b_ub=b)
print(e.x.round(4))
print(f'{-e.fun:.2f}')""")
t('''Für das Tische-und-Stühle-Beispiel kommt eine dritte Bedingung hinzu: Es dürfen höchstens 30 Stühle hergestellt werden (`bounds`).
Gib die beste Lösung und den Gewinn aus.''', NP_OPT,
  """gewinn = np.array([30, 40])
A = np.array([[2, 3], [4, 2]])
b = np.array([120, 160])
e = optimize.linprog(-gewinn, A_ub=A, b_ub=b, bounds=[(0, None), (0, 30)])
print(e.x.round(4))
print(f'{-e.fun:.2f}')""")
t('''Ein Landwirt hat 100 ha Land für Weizen und Raps. Weizen bringt 600 €/ha Gewinn und braucht 4 Arbeitsstunden/ha, Raps 900 €/ha und 8 Stunden/ha.
Es stehen 560 Stunden zur Verfügung, und mindestens 30 ha sollen Weizen sein. Bestimme die Aufteilung und den Gewinn.''', NP_OPT,
  """gewinn = np.array([600, 900])
A = np.array([[1, 1], [4, 8]])
b = np.array([100, 560])
e = optimize.linprog(-gewinn, A_ub=A, b_ub=b, bounds=[(30, None), (0, None)])
print(e.x.round(4))
print(f'{-e.fun:.2f}')""")
t('''Ein Saft soll aus Apfelsaft (0.80 €/l, 10 g Zucker/l, 40 mg Vitamin C/l) und Orangensaft (1.20 €/l, 9 g Zucker/l, 500 mg Vitamin C/l) gemischt werden.
1000 Liter sollen entstehen (`A_eq`), mit mindestens 150 000 mg Vitamin C. Wie viele Liter von jeder Sorte sind am billigsten? Gib die Liter und die Kosten aus.''',
  NP_OPT,
  """kosten = np.array([0.8, 1.2])
e = optimize.linprog(kosten, A_ub=[[-40, -500]], b_ub=[-150000], A_eq=[[1, 1]], b_eq=[1000])
print(e.x.round(4))
print(f'{e.fun:.2f}')""")
t('''Ein Möbelhaus liefert aus zwei Lagern (Bestand 40 und 50 Sofas) an drei Filialen (Bedarf 30, 35 und 25). Die Transportkosten pro Sofa stehen in der Tabelle.
Die 6 Variablen sind die Mengen von Lager i nach Filiale j (zeilenweise). Bestimme die günstigste Verteilung als 2×3-Tabelle (`reshape(2, 3)`) und die Kosten.''',
  NP_OPT + '''

#                  Filiale 1  2   3
kosten = np.array([[8,        6,  10],     # Lager A
                   [9,       12,   7]])    # Lager B''',
  """A_ub = [[1, 1, 1, 0, 0, 0],      # Lager A gibt höchstens 40 ab
        [0, 0, 0, 1, 1, 1]]      # Lager B höchstens 50
b_ub = [40, 50]
A_eq = [[1, 0, 0, 1, 0, 0],      # Filiale 1 bekommt genau 30
        [0, 1, 0, 0, 1, 0],
        [0, 0, 1, 0, 0, 1]]
b_eq = [30, 35, 25]
e = optimize.linprog(kosten.flatten(), A_ub=A_ub, b_ub=b_ub, A_eq=A_eq, b_eq=b_eq)
print(e.x.reshape(2, 3).round(4))
print(f'{e.fun:.2f}')""")
t('''Für einen Ausflug mit 275 Personen stehen große Busse (50 Plätze, 400 €) und kleine Busse (30 Plätze, 270 €) zur Verfügung, aber nur 4 große.
Wie viele Busse jeder Sorte sind am günstigsten? Löse einmal ohne und einmal mit `integrality=[1, 1]` und gib jeweils `x` und die Kosten aus.''', NP_OPT,
  """kosten = [400, 270]
for ganz in [None, [1, 1]]:
    e = optimize.linprog(kosten, A_ub=[[-50, -30]], b_ub=[-275], bounds=[(0, 4), (0, None)], integrality=ganz)
    print(f'{e.x.round(4)} {e.fun:.2f}')""")
t('''Zeichne für das Tische-und-Stühle-Beispiel die Grenzgeraden der beiden Bedingungen (Tischlerei: `y = (120 - 2x) / 3`, Lackiererei: `y = (160 - 4x) / 2`)
für x von 0 bis 45 (die x-Achse sind Tische, die y-Achse Stühle) mit Legende, zeige y nur von 0 bis 50 (`plt.ylim(0, 50)`) und markiere die beste Lösung
als roten Punkt.''', NP_OPT + '\nimport matplotlib.pyplot as plt',
  """e = optimize.linprog([-30, -40], A_ub=[[2, 3], [4, 2]], b_ub=[120, 160])
x = np.linspace(0, 45, 100)
plt.plot(x, (120 - 2 * x) / 3, label='Tischlerei')
plt.plot(x, (160 - 4 * x) / 2, label='Lackiererei')
plt.plot(e.x[0], e.x[1], 'ro')
plt.ylim(0, 50)
plt.legend()
plt.show()""")
predict("""from scipy import optimize

e = optimize.linprog([-1, -1], A_ub=[[1, 1]], b_ub=[10], bounds=[(0, 4), (0, 4)])
print(f'{-e.fun:.4f}')
print(e.x.round(4))""", erklaerung='''Gesucht ist das größte `x + y` mit `x + y ≤ 10`, aber beide Variablen sind höchstens 4. Die Bedingung `x + y ≤ 10` spielt deshalb keine Rolle:
Das Beste ist `x = y = 4` mit `x + y = 8`. Ausgabe: `8.0000` und `[4. 4.]`.''')

# ---------------------------------------------------------------- 5
sec('Abstände und nächste Nachbarn')
expl('''#### `spatial.distance`

Das Modul `scipy.spatial` (*räumlich*) rechnet mit Punktmengen. In `spatial.distance` stehen verschiedene **Abstandsmaße**:

- `distance.euclidean(p, q)`: der gewöhnliche (euklidische) Abstand, Luftlinie nach Pythagoras
- `distance.cityblock(p, q)`: der **Manhattan-Abstand** `|x₁ - x₂| + |y₁ - y₂|`, wie in einer Stadt mit rechtwinkligen Straßen
- `distance.cdist(A, B)`: eine **Abstandsmatrix**. Zeile `i`, Spalte `j` enthält den Abstand von Punkt `A[i]` zu `B[j]`.
  Mit `metric='cityblock'` wird der Manhattan-Abstand verwendet.

Die Punkte stehen in 2D-Arrays: eine Zeile pro Punkt.''',
     """import numpy as np
from scipy.spatial import distance

print(distance.euclidean([0, 0], [3, 4]), distance.cityblock([0, 0], [3, 4]))
punkte = np.array([[0, 0], [3, 4], [6, 0]])
print(distance.cdist(punkte, punkte).round(2))
print(distance.cdist(punkte, punkte, metric='cityblock'))""")
expl('''#### Nächste Nachbarn: `spatial.KDTree`

Bei sehr vielen Punkten wäre es zu langsam, für jede Frage alle Abstände zu berechnen. Ein `KDTree` ordnet die Punkte so, dass man schnell suchen kann:

- `baum = spatial.KDTree(punkte)` baut den Suchbaum.
- `abstand, index = baum.query(p)` findet den **nächsten** Punkt zu `p` (seinen Index in `punkte` und den Abstand).
  Mit `k=3` erhält man die drei nächsten als Arrays.
- `baum.query_ball_point(p, r)` gibt eine Liste der Indizes aller Punkte im Abstand höchstens `r` zurück.''',
     """import numpy as np
from scipy import spatial

haltestellen = np.array([[1, 1], [4, 2], [2, 5], [6, 6]])
baum = spatial.KDTree(haltestellen)
abstand, index = baum.query([3, 3])
print(f'{index} {abstand:.4f}')
abstaende, indizes = baum.query([3, 3], k=2)
print(indizes, abstaende.round(4))
print(baum.query_ball_point([3, 3], 2.5))""")

ORTE = NP_SP + '''

orte = np.array([[0, 0], [4, 3], [1, 7], [8, 5], [5, 9]])   # in km
namen = ['A', 'B', 'C', 'D', 'E']'''
t('Gib die Abstandsmatrix der fünf Orte aus (Luftlinie, zwei Nachkommastellen).', ORTE,
  """print(spatial.distance.cdist(orte, orte).round(2))""")
t('''Welche beiden Orte liegen am weitesten auseinander? Gib ihre Namen und den Abstand (zwei Nachkommastellen) aus.
Benutze `argmax()` und `np.unravel_index(i, matrix.shape)`, das aus dem Index im flachen Array Zeile und Spalte macht.''', ORTE,
  """d = spatial.distance.cdist(orte, orte)
i, j = np.unravel_index(d.argmax(), d.shape)
print(f'{namen[i]} {namen[j]} {d[i, j]:.2f}')""")
t('''Ein Lager soll an einem der fünf Orte gebaut werden, sodass die **Summe** der Abstände zu allen Orten am kleinsten ist. Gib für jeden Ort die Summe
(zwei Nachkommastellen) und dann den besten Ort aus.''', ORTE,
  """summen = spatial.distance.cdist(orte, orte).sum(axis=1)
for name, s in zip(namen, summen):
    print(f'{name} {s:.2f}')
print(namen[summen.argmin()])""")
t('''In Manhattan fährt ein Taxi nur waagerecht und senkrecht. Gib die Abstandsmatrix der fünf Orte mit dem Manhattan-Abstand aus und das Paar von Orten,
bei dem der Unterschied zwischen Manhattan-Abstand und Luftlinie am größten ist (Namen und Unterschied, zwei Nachkommastellen).''', ORTE,
  """m = spatial.distance.cdist(orte, orte, metric='cityblock')
print(m)
u = m - spatial.distance.cdist(orte, orte)
i, j = np.unravel_index(u.argmax(), u.shape)
print(f'{namen[i]} {namen[j]} {u[i, j]:.2f}')""")
t('''Für jeden Ort ist der **nächste andere** Ort gesucht. Frage dafür mit `k=2` die zwei nächsten Punkte ab (der nächste ist der Ort selbst mit Abstand 0)
und gib für jeden Ort den Namen des Nachbarn und den Abstand (zwei Nachkommastellen) aus.''', ORTE,
  """baum = spatial.KDTree(orte)
for i in range(len(orte)):
    abstaende, indizes = baum.query(orte[i], k=2)
    print(f'{namen[i]} {namen[indizes[1]]} {abstaende[1]:.2f}')""")
t('''In einem Park stehen Notrufsäulen. Gib für jeden Wanderer die Nummer (Index) der nächsten Säule und den Abstand in m aus (eine Nachkommastelle).''',
  NP_SP + '''

saeulen = np.array([[120, 80], [450, 300], [200, 520], [700, 150], [650, 600]])
wanderer = np.array([[300, 200], [600, 450], [100, 400], [690, 50]])''',
  """baum = spatial.KDTree(saeulen)
for w in wanderer:
    abstand, index = baum.query(w)
    print(f'{index} {abstand:.1f}')""")
t('''Erzeuge mit `rng = np.random.default_rng(12)` 500 zufällige Punkte im Quadrat von 0 bis 100 (`rng.uniform(0, 100, size=(500, 2))`). Wie viele davon liegen
höchstens 10 vom Mittelpunkt (50 | 50) entfernt? Zähle mit `query_ball_point()` und vergleiche mit dem erwarteten Wert `500 · π · 10² / 100²` (zwei Nachkommastellen).''',
  NP_SP,
  """rng = np.random.default_rng(12)
punkte = rng.uniform(0, 100, size=(500, 2))
baum = spatial.KDTree(punkte)
print(len(baum.query_ball_point([50, 50], 10)))
print(f'{500 * np.pi * 10 ** 2 / 100 ** 2:.2f}')""")
t('''Zeichne die Notrufsäulen als rote Quadrate (`'rs'`) und die Wanderer als blaue Punkte. Verbinde jeden Wanderer mit einer grauen Linie mit seiner nächsten Säule.
Sorge mit `plt.axis('equal')` für gleiche Einheiten auf beiden Achsen.''',
  NP_SP + '''
import matplotlib.pyplot as plt

saeulen = np.array([[120, 80], [450, 300], [200, 520], [700, 150], [650, 600]])
wanderer = np.array([[300, 200], [600, 450], [100, 400], [690, 50]])''',
  """baum = spatial.KDTree(saeulen)
for w in wanderer:
    abstand, index = baum.query(w)
    s = saeulen[index]
    plt.plot([w[0], s[0]], [w[1], s[1]], color='gray')
plt.plot(saeulen[:, 0], saeulen[:, 1], 'rs')
plt.plot(wanderer[:, 0], wanderer[:, 1], 'bo')
plt.axis('equal')
plt.show()""")
predict("""import numpy as np
from scipy import spatial

punkte = np.array([[0, 0], [10, 0], [0, 10]])
baum = spatial.KDTree(punkte)
abstand, index = baum.query([1, 8])
print(f'{index} {abstand:.4f}')
print(spatial.distance.cityblock([0, 0], [-2, 5]))""", erklaerung='''- Der Punkt (1 | 8) liegt am nächsten an (0 | 10), das ist Index `2`. Der Abstand ist `√(1² + 2²) = √5 ≈ 2.2361`.
- Der Manhattan-Abstand ist `|0 - (-2)| + |0 - 5| = 2 + 5 = 7`.''')

# ---------------------------------------------------------------- 6
sec('Konstanten und Einheiten')
expl('''#### `scipy.constants`

Das Modul `scipy.constants` enthält Naturkonstanten und Umrechnungsfaktoren in **SI-Einheiten** (Meter, Kilogramm, Sekunde, ...):

| Name | Bedeutung |
|---|---|
| `constants.g` | Fallbeschleunigung 9.80665 m/s² (Normwert) |
| `constants.c` | Lichtgeschwindigkeit in m/s |
| `constants.G` | Gravitationskonstante |
| `constants.h` | Plancksches Wirkungsquantum |
| `constants.minute`, `constants.hour`, `constants.day`, `constants.year` | Zeitspannen in Sekunden |
| `constants.kilo`, `constants.mega`, `constants.milli`, ... | Vorsilben als Faktor (1000, 10⁶, 0.001) |
| `constants.kmh`, `constants.mile`, `constants.inch` | 1 km/h in m/s, 1 Meile und 1 Zoll in Meter |

`constants.convert_temperature(wert, 'Celsius', 'Kelvin')` rechnet Temperaturen um (auch `'Fahrenheit'`).''',
     """from scipy import constants

print(constants.g, constants.c)
print(constants.hour, constants.day)
print(f'{constants.mile:.3f} {constants.inch}')
print(f'{100 * constants.kmh:.4f}')
print(constants.convert_temperature(100, 'Celsius', 'Fahrenheit'))
print(constants.convert_temperature(0, 'Celsius', 'Kelvin'))""")

t('''Wie lange braucht das Licht von der Sonne zur Erde (150 Millionen km)? Gib die Zeit in Sekunden und in Minuten aus (zwei Nachkommastellen) und benutze
`constants.c`, `constants.kilo`, `constants.mega` und `constants.minute`.''', 'from scipy import constants',
  """strecke = 150 * constants.mega * constants.kilo
zeit = strecke / constants.c
print(f'{zeit:.2f}')
print(f'{zeit / constants.minute:.2f}')""")
t('''Ein Lichtjahr ist die Strecke, die das Licht in einem Jahr zurücklegt. Gib sie in km aus (`:.4e`). Der nächste Stern ist 4.24 Lichtjahre entfernt.
Wie viele Jahre bräuchte eine Raumsonde mit 60 000 km/h (eine Nachkommastelle)?''', 'from scipy import constants',
  """lichtjahr = constants.c * constants.year
print(f'{lichtjahr / constants.kilo:.4e}')
geschwindigkeit = 60000 * constants.kmh
print(f'{4.24 * lichtjahr / geschwindigkeit / constants.year:.1f}')""")
t('''Rechne die Temperaturen -40, 0, 37 und 100 °C in Fahrenheit und Kelvin um (zwei Nachkommastellen). `convert_temperature()` nimmt auch ein Array.''',
  'import numpy as np\nfrom scipy import constants',
  """celsius = np.array([-40, 0, 37, 100])
print(constants.convert_temperature(celsius, 'Celsius', 'Fahrenheit').round(2))
print(constants.convert_temperature(celsius, 'Celsius', 'Kelvin').round(2))""")
t('''Ein Stein fällt ohne Luftwiderstand von einem 80 m hohen Turm. Berechne mit `constants.g` die Fallzeit `√(2h / g)` (zwei Nachkommastellen) und die
Aufprallgeschwindigkeit `g · t` in m/s und in km/h (eine Nachkommastelle).''', 'import numpy as np\nfrom scipy import constants',
  """zeit = np.sqrt(2 * 80 / constants.g)
v = constants.g * zeit
print(f'{zeit:.2f}')
print(f'{v:.1f} {v / constants.kmh:.1f}')""")
t('''Ein Fernseher hat eine Bildschirmdiagonale von 55 Zoll im Format 16 : 9. Gib die Diagonale, die Breite und die Höhe in cm aus (eine Nachkommastelle).
Die Breite ist `d · 16 / √(16² + 9²)`.''', 'import numpy as np\nfrom scipy import constants',
  """d = 55 * constants.inch * 100
print(f'{d:.1f}')
print(f'{d * 16 / np.sqrt(16 ** 2 + 9 ** 2):.1f} {d * 9 / np.sqrt(16 ** 2 + 9 ** 2):.1f}')""")
predict("""from scipy import constants

print(constants.kilo * constants.milli)
print(constants.hour / constants.minute)
print(constants.convert_temperature(273.15, 'Kelvin', 'Celsius'))""", erklaerung='''- `kilo` ist 1000, `milli` ist 0.001, das Produkt `1.0`.
- Eine Stunde hat 3600 Sekunden, eine Minute 60, also `60.0`.
- 273.15 K sind genau 0 °C: `0.0`.''')

# ---------------------------------------------------------------- 7
sec('Gemischte Übungen')
t(f'''**Wurf mit Luftwiderstand:** Ein Ball wird unter 45° mit 20 m/s geworfen. Für die Größen `[x, y, vx, vy]` gilt `x' = vx`, `y' = vy`,
`vx' = -0.02 · v · vx`, `vy' = -9.81 - 0.02 · v · vy` mit `v = √(vx² + vy²)`. Bestimme mit `dense_output=True` und `brentq()` (Höhe 0 zwischen 1 und 5),
wann und wie weit vom Abwurf der Ball landet (zwei Nachkommastellen, `{GENAU}`). Ohne Luftwiderstand wären es `20² / 9.81` Meter.''',
  'import numpy as np\nfrom scipy import integrate, optimize',
  f"""

def wurf(t, z):
    x, y, vx, vy = z
    v = np.sqrt(vx ** 2 + vy ** 2)
    return [vx, vy, -0.02 * v * vx, -9.81 - 0.02 * v * vy]

v0 = 20 / np.sqrt(2)
loesung = integrate.solve_ivp(wurf, (0, 5), [0, 0, v0, v0], dense_output=True, {GENAU})

def hoehe(t):
    return loesung.sol(t)[1]

landung = optimize.brentq(hoehe, 1, 5)
print(f'{{landung:.2f}} {{loesung.sol(landung)[0]:.2f}}')
print(f'{{20 ** 2 / 9.81:.2f}}')""")
t(f'''Zeichne die Flugbahn des Balls aus der vorigen Aufgabe (`y` über `x`, 200 Punkte von 0 bis zur Landezeit) und zum Vergleich die Bahn ohne Luftwiderstand
(`vx' = 0`, `vy' = -9.81`, gestrichelt). Zeige nur Höhen ab 0 (`plt.ylim(bottom=0)`) und benutze `plt.axis('equal')` nicht.''',
  'import numpy as np\nfrom scipy import integrate, optimize\nimport matplotlib.pyplot as plt',
  f"""

def wurf(t, z, k):
    x, y, vx, vy = z
    v = np.sqrt(vx ** 2 + vy ** 2)
    return [vx, vy, -k * v * vx, -9.81 - k * v * vy]

v0 = 20 / np.sqrt(2)
for k, stil in [(0.02, '-'), (0, '--')]:
    loesung = integrate.solve_ivp(wurf, (0, 5), [0, 0, v0, v0], args=(k,), dense_output=True, {GENAU})

    def hoehe(t):
        return loesung.sol(t)[1]

    landung = optimize.brentq(hoehe, 1, 5)
    werte = loesung.sol(np.linspace(0, landung, 200))
    plt.plot(werte[0], werte[1], stil)
plt.ylim(bottom=0)
plt.show()""")
t('''Ein Paketdienst hat drei Depots und sechs Kunden. Ordne jeden Kunden dem nächsten Depot zu (`KDTree`) und gib für jedes Depot die Indizes seiner Kunden
und die Summe der Abstände (eine Nachkommastelle) aus.''',
  NP_SP + '''

depots = np.array([[2, 2], [8, 3], [5, 8]])
kunden = np.array([[1, 4], [3, 1], [7, 1], [9, 5], [4, 7], [6, 9]])''',
  """baum = spatial.KDTree(depots)
abstaende, zuordnung = baum.query(kunden)
for d in range(len(depots)):
    print(f'{d} {np.where(zuordnung == d)[0]} {abstaende[zuordnung == d].sum():.1f}')""")
t(f'''**Wie lange reicht ein Vorrat?** Ein Wasserspeicher enthält 5000 Liter. Pro Stunde werden `400 + 150 · sin(π t / 12)` Liter entnommen, und es fließen
konstant 300 Liter zu. Bestimme mit `solve_ivp()`, `dense_output=True` und `brentq()` (zwischen 1 und 100), wann der Speicher leer ist (zwei Nachkommastellen).''',
  'import numpy as np\nfrom scipy import integrate, optimize',
  f"""

def rate(t, y):
    return 300 - (400 + 150 * np.sin(np.pi * t / 12))

loesung = integrate.solve_ivp(rate, (0, 100), [5000], dense_output=True, {GENAU})

def menge(t):
    return loesung.sol(t)[0]

print(f'{{optimize.brentq(menge, 1, 100):.2f}}')""")
t('''Eine Schule plant ein Sommerfest und verkauft Waffeln (Gewinn 0.80 €) und Crêpes (Gewinn 1.20 €). Teig: 0.1 kg pro Waffel und 0.08 kg pro Crêpe,
40 kg sind da. Zeit: 2 Minuten pro Waffel, 4 Minuten pro Crêpe, 1200 Minuten stehen zur Verfügung. Es sollen mindestens 100 Waffeln sein.
Bestimme die beste Aufteilung (ganzzahlig) und den Gewinn.''', NP_OPT,
  """e = optimize.linprog([-0.8, -1.2], A_ub=[[0.1, 0.08], [2, 4]], b_ub=[40, 1200], bounds=[(100, None), (0, None)], integrality=[1, 1])
print(e.x)
print(f'{-e.fun:.2f}')""")
t('''Denk dir selbst ein Modell mit einer Änderungsrate aus (z. B. das Abkühlen deines Tees, das Füllen einer Badewanne mit offenem Abfluss, die Ausbreitung
eines Gerüchts) und berechne und zeichne den Verlauf mit `solve_ivp()`.''', '',
  f"""import numpy as np
from scipy import integrate
import matplotlib.pyplot as plt

def geruecht(t, y, k, n):
    return k * y * (n - y) / n

loesung = integrate.solve_ivp(geruecht, (0, 14), [2], t_eval=np.linspace(0, 14, 200), args=(0.9, 1200), {GENAU})
plt.plot(loesung.t, loesung.y[0])
plt.xlabel('Tage')
plt.ylabel('Personen, die es wissen')
plt.show()""", kind='free')

generate('scipy_anwendungen', 'scipy: Anwendungen', intro=INTRO)
