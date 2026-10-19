# Erzeugt ../content/numpy_grundlagen.ipynb (siehe nbgen.py).
#
# Braucht numpy in derselben Version wie Pyodide in JupyterLite (zurzeit 2.4.6, Python 3.11 oder neuer):
#     py -3.13 -m pip install numpy==2.4.6
#     py -3.13 -W error generator/gen_numpy_grundlagen.py
#
# Fallstricke:
# - Ganze Zahlen sind lokal int64, in JupyterLite (wasm32) int32. Erwartete Ausgaben zeigen deshalb nie den dtype
#   von Ganzzahl-Arrays, und alle Zahlen bleiben weit unter 2**31.
# - Listen oder Tupel aus numpy-Zahlen werden als [np.int64(3), ...] ausgegeben. Deshalb immer einzelne Werte
#   oder .tolist() ausgeben.
# - Masken (a[a > 5]) kommen erst in numpy_filtern, 2D-Arrays erst in numpy_2d.
from nbgen import sec, expl, task, predict, generate


def t(text, given='', body='', kind='normal'):
    """Aufgabe, deren Lösung aus dem vorgegebenen Code plus body besteht."""
    task(text, given=given, solution=(given + '\n' + body) if given else body, kind=kind)


NP = 'import numpy as np'

INTRO = '''**numpy** ist das wichtigste Python-Paket zum Rechnen mit vielen Zahlen auf einmal. Statt Listen verwendet es **Arrays**:
Mit ihnen rechnet man ohne Schleife, zum Beispiel verdoppelt `a * 2` jede Zahl im Array. Das ist kürzer und viel schneller.
numpy ist die Grundlage für viele andere Pakete, etwa für Diagramme (matplotlib) und Datenanalyse (pandas).

Dieses Notebook behandelt eindimensionale Arrays, also Arrays, die wie eine Liste eine Reihe von Werten enthalten.
Weitere Notebooks behandeln das Filtern mit Bedingungen, zweidimensionale Arrays und Zufallszahlen mit numpy.

Jeder Abschnitt beginnt mit kurzen Erklärungen und Beispielen. Führe die Beispiele aus und probiere sie ruhig ein wenig aus.
Danach folgen viele kleine Übungen. Wenn etwas vorgegeben ist, steht es schon in der Codezelle.

Beim ersten `import numpy` wird numpy in den Browser geladen. Das dauert ein paar Sekunden.'''

# ---------------------------------------------------------------- 1
sec('Arrays erstellen')
expl('''#### numpy importieren und ein Array erstellen

numpy importiert man fast immer unter dem kurzen Namen `np`: `import numpy as np`.
Danach schreibt man `np.` vor jede numpy-Funktion.

`np.array(liste)` macht aus einer Liste ein **Array**.

- `print()` gibt ein Array in eckigen Klammern **ohne Kommas** aus.
- `len(a)` ist die Anzahl der Elemente, wie bei Listen.
- In einem Array haben alle Elemente **denselben Datentyp**. Mischt man ganze Zahlen und Kommazahlen,
  werden alle zu Kommazahlen. Ganze Kommazahlen wie `2.0` werden dabei kurz als `2.` angezeigt.''',
     """import numpy as np

a = np.array([3, 1, 4, 1, 5])
print(a)
print(len(a))
print(type(a))
print(np.array([1, 2.5, 3]))
print(np.array(['Anna', 'Ben']))""")
expl('''#### Arrays und Listen

Arrays sehen aus wie Listen, verhalten sich aber beim Rechnen anders:

| | Liste | Array |
|---|---|---|
| `* 2` | hängt die Liste zweimal hintereinander | verdoppelt jedes Element |
| `+` | hängt zwei Listen aneinander | addiert die Elemente paarweise |
| `+ 1` | Fehler | addiert 1 zu jedem Element |

Durch ein Array kann man wie durch eine Liste mit `for` laufen.
`a.tolist()` wandelt ein Array wieder in eine normale Python-Liste um.''',
     """import numpy as np

liste = [1, 2, 3]
a = np.array([1, 2, 3])
print(liste * 2)
print(a * 2)
print(liste + liste)
print(a + a)
print(a + 1)
for x in a:
    print(x)
print(a.tolist())""")

t('Erstelle aus der Liste `zahlen` ein Array `a` und gib es aus.',
  NP + '\nzahlen = [3, 1, 4, 1, 5, 9]',
  """a = np.array(zahlen)
print(a)""")
t('Erstelle ein Array mit den Zahlen 10, 20, 30 und 40 und gib es und darunter seine Länge aus.',
  NP,
  """a = np.array([10, 20, 30, 40])
print(a)
print(len(a))""")
t('Gib zuerst `liste * 3` und dann `a * 3` aus.',
  NP + '\nliste = [1, 2]\na = np.array([1, 2])',
  """print(liste * 3)
print(a * 3)""")
t('Gib zuerst `liste1 + liste2` und dann `a1 + a2` aus.',
  NP + '\nliste1 = [1, 2, 3]\nliste2 = [10, 20, 30]\na1 = np.array(liste1)\na2 = np.array(liste2)',
  """print(liste1 + liste2)
print(a1 + a2)""")
t('Erstelle ein Array mit den Kommazahlen 1.5, 2.0 und 3.25 und gib es aus.',
  NP,
  """print(np.array([1.5, 2.0, 3.25]))""")
t('Erstelle ein Array aus der Liste `namen` und gib es aus.',
  NP + "\nnamen = ['Anna', 'Ben', 'Cem']",
  """print(np.array(namen))""")
t('Gehe mit einer `for`-Schleife durch das Array und gib jedes Element mal 10 aus.',
  NP + '\na = np.array([2, 5, 7])',
  """for x in a:
    print(x * 10)""")
t('Wandle das Array mit `tolist()` in eine Liste um und gib die Liste aus.',
  NP + '\na = np.array([4, 8, 15, 16, 23, 42])',
  """print(a.tolist())""")
t('Erstelle ein Array aus der Liste `werte` und gib es aus. Achte darauf, wie die ganzen Zahlen jetzt aussehen.',
  NP + '\nwerte = [1, 2, 3.5, 4]',
  """print(np.array(werte))""")
t('''Verdopple jedes Element von `liste` einmal mit einer List Comprehension und einmal mit einem Array.
Gib beide Ergebnisse aus, das Array mit `tolist()`.''',
  NP + '\nliste = [3, 6, 9, 12]',
  """print([x * 2 for x in liste])
print((np.array(liste) * 2).tolist())""")
predict("""import numpy as np
print(np.array([1, 2, 3]) * 3)
print([1, 2, 3] * 3)
print(np.array([1, 2]) + np.array([10, 20]))
print(len(np.array([7, 8, 9])))
print(np.array([1, 2]).tolist() + [3])""")
predict("""import numpy as np
print([1, 2, 3] + 1)""", error=TypeError)

# ---------------------------------------------------------------- 2
sec('Arrays erzeugen mit arange(), linspace(), zeros(), ones() und full()')
expl('''#### `np.arange()`

`np.arange()` funktioniert wie `range()`, liefert aber gleich ein Array:

- `np.arange(stop)`: 0, 1, ..., stop - 1
- `np.arange(start, stop)` und `np.arange(start, stop, schritt)`: Der Stoppwert gehört **nicht** dazu.
- Anders als bei `range()` darf die Schrittweite auch eine Kommazahl sein.''',
     """import numpy as np

print(np.arange(5))
print(np.arange(2, 10))
print(np.arange(0, 20, 5))
print(np.arange(10, 0, -3))
print(np.arange(0, 2, 0.5))""")
expl('''#### `np.linspace()`

`np.linspace(start, stop, anzahl)` liefert `anzahl` Werte mit **gleichem Abstand** von `start` bis `stop`.
Hier gehört der Stoppwert **dazu**. Die Werte sind immer Kommazahlen.

Das ist praktisch für Wertetabellen: `np.linspace(0, 1, 5)` sind die Werte 0, 0.25, 0.5, 0.75 und 1.''',
     """import numpy as np

print(np.linspace(0, 1, 5))
print(np.linspace(0, 100, 3))
print(np.linspace(-1, 1, 9))""")
expl('''#### `np.zeros()`, `np.ones()` und `np.full()`

- `np.zeros(n)`: ein Array mit `n` Nullen
- `np.ones(n)`: ein Array mit `n` Einsen
- `np.full(n, wert)`: ein Array, in dem `n`-mal `wert` steht

`zeros()` und `ones()` liefern Kommazahlen. Mit `dtype=int` bekommt man ganze Zahlen.''',
     """import numpy as np

print(np.zeros(4))
print(np.ones(3))
print(np.ones(3, dtype=int))
print(np.full(5, 7))
print(np.full(3, 'x'))""")

t('Gib mit `np.arange()` ein Array mit den Zahlen 0 bis 9 aus.', NP, """print(np.arange(10))""")
t('Gib mit `np.arange()` ein Array mit den Zahlen 1 bis 10 aus.', NP, """print(np.arange(1, 11))""")
t('Gib mit `np.arange()` alle geraden Zahlen von 0 bis einschließlich 20 aus.', NP, """print(np.arange(0, 21, 2))""")
t('Gib mit `np.arange()` einen Countdown von 10 bis 1 aus.', NP, """print(np.arange(10, 0, -1))""")
t('Gib mit `np.arange()` alle Vielfachen von 7 aus, die kleiner als 100 sind (ohne die 0).', NP, """print(np.arange(7, 100, 7))""")
t('Gib mit `np.arange()` die Zahlen von 0 bis 1 (ohne 1) im Abstand 0.25 aus.', NP, """print(np.arange(0, 1, 0.25))""")
t('Gib mit `np.linspace()` fünf gleichmäßig verteilte Werte von 0 bis 1 aus.', NP, """print(np.linspace(0, 1, 5))""")
t('Gib mit `np.linspace()` die Werte 0, 10, 20, ..., 100 aus.', NP, """print(np.linspace(0, 100, 11))""")
t('Gib mit `np.linspace()` sieben Werte von -3 bis 3 aus.', NP, """print(np.linspace(-3, 3, 7))""")
t('Gib ein Array mit fünf Nullen aus.', NP, """print(np.zeros(5))""")
t('Gib ein Array mit vier Einsen als ganze Zahlen aus.', NP, """print(np.ones(4, dtype=int))""")
t('Gib ein Array aus, in dem sechsmal die Zahl 7 steht.', NP, """print(np.full(6, 7))""")
t('Gib ein Array aus, in dem fünfmal `?` steht.', NP, """print(np.full(5, '?'))""")
t('Gib mit `np.arange()` und `**` die Quadratzahlen von 1 bis 100 aus (also 1, 4, 9, ..., 100).', NP, """print(np.arange(1, 11) ** 2)""")
t('Gib mit `np.ones()` und `*` ein Array mit acht Einträgen aus, die alle 2.5 sind.', NP, """print(np.ones(8) * 2.5)""")
predict("""import numpy as np
print(np.arange(5))
print(np.arange(2, 10, 3))
print(np.linspace(1, 2, 3))
print(np.zeros(3))
print(np.arange(0, 1, 0.5))
print(len(np.linspace(0, 10, 4)))""")

# ---------------------------------------------------------------- 3
sec('Eigenschaften und Datentypen')
expl('''#### `size`, `shape` und `ndim`

Ein Array hat einige Eigenschaften, die man ohne Klammern abfragt:

- `a.size`: die Anzahl aller Elemente
- `a.ndim`: die Anzahl der Dimensionen. Unsere Arrays sind eindimensional, also 1.
- `a.shape`: die Form als Tupel. Bei einem eindimensionalen Array mit 5 Elementen ist das `(5,)`.

Zweidimensionale Arrays (wie Tabellen oder Grids) kommen im Notebook *numpy_2d*. Dort sind `ndim` und `shape` wichtiger.''',
     """import numpy as np

a = np.array([3, 1, 4, 1, 5])
print(a.size)
print(a.ndim)
print(a.shape)""")
expl('''#### Datentypen: `dtype`

`a.dtype` gibt an, welchen Datentyp die Elemente haben:

| dtype | Bedeutung |
|---|---|
| `int64` oder `int32` | ganze Zahlen. Welcher Typ, hängt vom Rechner ab. Im Browser ist es meist `int32`. |
| `float64` | Kommazahlen |
| `bool` | `True` und `False` |
| `<U5` | Zeichenketten mit höchstens 5 Zeichen |

Mit `np.array(liste, dtype=float)` legt man den Typ beim Erstellen fest.''',
     """import numpy as np

print(np.array([1.5, 2.0]).dtype)
print(np.array([1, 2.5]).dtype)
print(np.array([True, False]).dtype)
print(np.array(['Anna', 'Ben']).dtype)
print(np.array([1, 2, 3], dtype=float))""")
expl('''#### Umwandeln mit `astype()`

`a.astype(typ)` gibt ein **neues** Array mit einem anderen Datentyp zurück:

- `a.astype(int)` macht aus Kommazahlen ganze Zahlen. Dabei werden die Nachkommastellen **abgeschnitten** (nicht gerundet).
- `a.astype(float)` macht aus ganzen Zahlen oder passenden Zeichenketten Kommazahlen.
- `a.astype(str)` macht aus Zahlen Zeichenketten.''',
     """import numpy as np

a = np.array([1.2, 2.7, -3.9])
print(a.astype(int))
b = np.array(['1.5', '2.25', '10'])
print(b.astype(float))
print(np.array([1, 2]).astype(float))
print(np.array([True, False, True]).astype(int))""")

t('Gib `size`, `ndim` und `shape` von `a` aus, jeweils in einer eigenen Zeile.',
  NP + '\na = np.array([5, 10, 15, 20, 25, 30, 35])',
  """print(a.size)
print(a.ndim)
print(a.shape)""")
t('Gib aus, wie viele Elemente `np.arange(3, 50, 4)` hat. Verwende `size`.',
  NP, """print(np.arange(3, 50, 4).size)""")
t('Gib den Datentyp von `a` aus.',
  NP + '\na = np.array([2.5, 3.0, 4.75])',
  """print(a.dtype)""")
t('Erstelle aus der Liste ein Array mit dem Datentyp `float` und gib es aus.',
  NP + '\nzahlen = [4, 8, 15]',
  """print(np.array(zahlen, dtype=float))""")
t('Wandle `a` mit `astype()` in ganze Zahlen um und gib das Ergebnis aus.',
  NP + '\na = np.array([3.14, 2.71, 9.99, -1.5])',
  """print(a.astype(int))""")
t('Die Preise stehen als Zeichenketten in einem Array. Wandle sie in Kommazahlen um und gib das Array und danach den doppelten Preis aus.',
  NP + "\npreise = np.array(['1.99', '0.5', '12.25'])",
  """p = preise.astype(float)
print(p)
print(p * 2)""")
t('Wandle das Array mit Wahrheitswerten in ganze Zahlen um und gib es aus.',
  NP + '\nantworten = np.array([True, True, False, True, False])',
  """print(antworten.astype(int))""")
t('Wandle die Zahlen in Zeichenketten um und gib das Ergebnis aus.',
  NP + '\na = np.array([7, 42, 100])',
  """print(a.astype(str))""")
t('Gib den Datentyp des Arrays mit den Namen aus.',
  NP + "\nnamen = np.array(['Ali', 'Bea', 'Charlotte'])",
  """print(namen.dtype)""")
predict("""import numpy as np
a = np.array([1.9, -1.9, 0.5])
print(a.astype(int))
print(a.shape)
print(np.array([1, 2]).astype(float))
print(np.array(['3', '4']).astype(int) + 1)""")

# ---------------------------------------------------------------- 4
sec('Elementweise rechnen')
expl('''#### Rechnen mit einer Zahl

Rechnet man ein Array mit einer Zahl, wird die Rechnung mit **jedem** Element ausgeführt.
Das geht mit allen Rechenzeichen: `+`, `-`, `*`, `/`, `//` (ganzzahlige Division), `%` (Modulo-Operator) und `**`.
Das Ergebnis ist ein neues Array. Bei `/` entstehen immer Kommazahlen.

Auch `+=`, `-=`, `*=` usw. funktionieren und ändern das Array selbst.''',
     """import numpy as np

a = np.array([1, 2, 3, 4])
print(a + 10)
print(a * 3)
print(a / 2)
print(a // 2)
print(a % 2)
print(a ** 2)
print(2 ** a)
print(10 - a)
a += 1
print(a)""")
expl('''#### Rechnen mit zwei Arrays

Rechnet man zwei Arrays **gleicher Länge** miteinander, wird elementweise gerechnet: das erste mit dem ersten, das zweite mit dem zweiten usw.
Haben die Arrays verschiedene Längen, gibt es einen `ValueError`.

Mit Listen bräuchte man dafür eine Schleife:''',
     """import numpy as np

preise = np.array([2.5, 1.0, 4.0])
mengen = np.array([2, 5, 3])
print(preise * mengen)

liste_p = [2.5, 1.0, 4.0]
liste_m = [2, 5, 3]
ergebnis = []
for i in range(len(liste_p)):
    ergebnis.append(liste_p[i] * liste_m[i])
print(ergebnis)""")

t('Addiere zu jedem Element von `a` die Zahl 10 und gib das Ergebnis aus.',
  NP + '\na = np.array([5, 12, 7, 3])',
  """print(a + 10)""")
t('Gib alle Preise verdoppelt aus.',
  NP + '\npreise = np.array([1.5, 4.0, 2.25, 10.0])',
  """print(preise * 2)""")
t('Rechne die Temperaturen von Celsius in Fahrenheit um: `c * 9 / 5 + 32`.',
  NP + '\nc = np.array([0, 10, 25, 37, 100])',
  """print(c * 9 / 5 + 32)""")
t('Gib die Quadrate aller Zahlen in `a` aus.',
  NP + '\na = np.array([3, -2, 5, 10])',
  """print(a ** 2)""")
t('Gib mit `np.arange()` und `**` die Zweierpotenzen 2⁰ bis 2¹⁰ aus.',
  NP, """print(2 ** np.arange(11))""")
t('Gib für jede Zahl in `a` den Rest bei der Division durch 3 aus. Verwende den Modulo-Operator.',
  NP + '\na = np.array([10, 11, 12, 13, 14, 15])',
  """print(a % 3)""")
t('Die Werte sind Minuten. Gib aus, wie viele volle Stunden das jeweils sind, und darunter, wie viele Minuten übrig bleiben.',
  NP + '\nminuten = np.array([45, 60, 135, 200])',
  """print(minuten // 60)
print(minuten % 60)""")
t('Berechne für jede Position den Betrag `preis * menge` und gib das Array aus.',
  NP + '\npreise = np.array([0.99, 2.5, 1.2])\nmengen = np.array([3, 2, 5])',
  """print(preise * mengen)""")
t('Addiere die Punkte der beiden Runden elementweise und gib das Ergebnis aus.',
  NP + '\nrunde1 = np.array([12, 8, 15, 10])\nrunde2 = np.array([9, 14, 11, 10])',
  """print(runde1 + runde2)""")
t('Gib aus, um wie viel sich jeder Wert von `vorher` zu `nachher` verändert hat.',
  NP + '\nvorher = np.array([70, 82, 65, 90])\nnachher = np.array([68, 85, 65, 87])',
  """print(nachher - vorher)""")
t('Berechne den Durchschnitt aus den beiden Arbeiten für jede Person.',
  NP + '\narbeit1 = np.array([2, 3, 1, 4])\narbeit2 = np.array([3, 3, 2, 5])',
  """print((arbeit1 + arbeit2) / 2)""")
t('Rechne die Geschwindigkeiten von km/h in m/s um (teilen durch 3.6).',
  NP + '\nkmh = np.array([36, 72, 90, 108])',
  """print(kmh / 3.6)""")
t('Berechne die Flächen der Rechtecke.',
  NP + '\nlaengen = np.array([3, 5, 2, 10])\nbreiten = np.array([4, 5, 8, 1])',
  """print(laengen * breiten)""")
t('Berechne die Funktionswerte von `f(x) = x² - 3x + 2` für alle `x` und gib sie aus.',
  NP + '\nx = np.arange(-2, 6)',
  """print(x ** 2 - 3 * x + 2)""")
t('Ziehe mit `-=` von jedem Kontostand 5 Euro Gebühr ab und gib das Array aus.',
  NP + '\nkonten = np.array([100, 250, 30, 75])',
  """konten -= 5
print(konten)""")
predict("""import numpy as np
a = np.array([1, 2, 3])
print(a / 2)
print(a // 2)
print(a % 2)
print(a * a)
print(1 / a * 6)""")
predict("""import numpy as np
a = np.array([1, 2, 3])
b = np.array([10, 20])
print(a + b)""", error=ValueError)

# ---------------------------------------------------------------- 5
sec('Mathematische Funktionen')
expl('''#### Funktionen für jedes Element

numpy hat viele mathematische Funktionen, die auf **jedes** Element eines Arrays angewendet werden:

| Funktion | Ergebnis |
|---|---|
| `np.sqrt(a)` | Quadratwurzel |
| `np.abs(a)` | Betrag (ohne Vorzeichen) |
| `np.round(a, n)` | gerundet auf `n` Nachkommastellen (ohne `n`: auf ganze Zahlen) |
| `np.floor(a)` | abgerundet |
| `np.ceil(a)` | aufgerundet |

Außerdem gibt es die Kreiszahl `np.pi`.

Achtung: `np.round()` rundet genau in der Mitte (bei ...,5) zur **geraden** Zahl: `0.5` wird zu `0`, `1.5` und `2.5` werden zu `2`.''',
     """import numpy as np

a = np.array([1.25, -2.5, 3.75])
print(np.sqrt(np.array([4, 9, 16])))
print(np.abs(a))
print(np.round(a, 1))
print(np.floor(a))
print(np.ceil(a))
print(np.round(np.pi, 4))
print(np.round(np.array([0.5, 1.5, 2.5])))""")
expl('''#### `np.maximum()`, `np.minimum()` und `np.clip()`

- `np.maximum(a, b)` vergleicht zwei Arrays elementweise und nimmt jeweils den größeren Wert. `np.minimum(a, b)` den kleineren.
  Statt `b` kann man auch eine Zahl angeben.
- `np.clip(a, untere, obere)` begrenzt alle Werte: Was kleiner als `untere` ist, wird zu `untere`, was größer als `obere` ist, wird zu `obere`.''',
     """import numpy as np

a = np.array([3, 8, 1, 6])
b = np.array([5, 2, 4, 6])
print(np.maximum(a, b))
print(np.minimum(a, b))
print(np.maximum(a, 4))
print(np.clip(a, 2, 5))""")

t('Gib die Quadratwurzeln aller Zahlen aus.',
  NP + '\na = np.array([1, 4, 25, 49, 100])',
  """print(np.sqrt(a))""")
t('Gib die Abstände zwischen den Messwerten und dem Sollwert 20 aus, immer positiv.',
  NP + '\nmesswerte = np.array([18, 23, 20, 15, 26])',
  """print(np.abs(messwerte - 20))""")
t('Berechne die Bruttopreise (Nettopreis mal 1.19) und runde sie auf zwei Nachkommastellen.',
  NP + '\nnetto = np.array([10, 4.99, 19.9])',
  """print(np.round(netto * 1.19, 2))""")
t('Gib die Zahlen abgerundet und darunter aufgerundet aus.',
  NP + '\na = np.array([2.1, 2.9, -2.1, 5.0])',
  """print(np.floor(a))
print(np.ceil(a))""")
t('Berechne die Kreisflächen `π · r²` und runde sie auf zwei Nachkommastellen.',
  NP + '\nr = np.array([1, 2, 5, 10])',
  """print(np.round(np.pi * r ** 2, 2))""")
t('Ein Text hat 250 Wörter pro Seite. Gib für jeden Text aus, wie viele Seiten er braucht. Runde auf und wandle in ganze Zahlen um.',
  NP + '\nwoerter = np.array([100, 250, 251, 1000, 1210])',
  """print(np.ceil(woerter / 250).astype(int))""")
t('Jede Person hatte zwei Versuche. Gib für jede Person das bessere (größere) Ergebnis aus.',
  NP + '\nversuch1 = np.array([4.2, 5.1, 3.8, 4.9])\nversuch2 = np.array([4.5, 4.8, 4.1, 4.9])',
  """print(np.maximum(versuch1, versuch2))""")
t('Begrenze alle Punktzahlen auf den Bereich 0 bis 100.',
  NP + '\npunkte = np.array([-5, 40, 105, 99, 0, 130])',
  """print(np.clip(punkte, 0, 100))""")
t('Ersetze alle negativen Werte durch 0. Verwende `np.maximum()` mit einer Zahl.',
  NP + '\nwerte = np.array([3, -1, 4, -5, 9])',
  """print(np.maximum(werte, 0))""")
t('Berechne für jeden Punkt (x, y) den Abstand vom Ursprung `√(x² + y²)`.',
  NP + '\nx = np.array([3, 5, 8, 1])\ny = np.array([4, 12, 6, 0])',
  """print(np.sqrt(x ** 2 + y ** 2))""")
t('Runde die Zahlen auf ganze Zahlen und gib sie als ganze Zahlen aus.',
  NP + '\na = np.array([1.4, 1.6, 2.49, 7.51])',
  """print(np.round(a).astype(int))""")
predict("""import numpy as np
print(np.round(np.array([0.5, 1.5, 2.5, 3.5])))
print(np.floor(np.array([-0.5, 0.5])))
print(np.abs(np.array([-3, 0, 3])))
print(np.clip(np.array([1, 5, 9]), 3, 6))
print(np.sqrt(np.array([2, 8])) ** 2)""")

# ---------------------------------------------------------------- 6
sec('Auswerten: sum(), min(), max(), mean() und mehr')
expl('''#### Kennzahlen eines Arrays

| Methode | Ergebnis |
|---|---|
| `a.sum()` | Summe aller Elemente |
| `a.prod()` | Produkt aller Elemente |
| `a.min()`, `a.max()` | kleinstes und größtes Element |
| `a.mean()` | Mittelwert (Durchschnitt), immer eine Kommazahl |

Statt `a.sum()` kann man auch `np.sum(a)` schreiben, genauso bei den anderen.
Das Ergebnis ist eine einzelne numpy-Zahl. Mit `print()` sieht sie aus wie eine normale Zahl.''',
     """import numpy as np

a = np.array([4, 8, 15, 16, 23, 42])
print(a.sum())
print(a.min(), a.max())
print(a.mean())
print(np.sum(a))
print(np.array([1, 2, 3, 4]).prod())""")
expl('''#### Wo ist das Minimum? `argmin()` und `argmax()`

`a.argmin()` und `a.argmax()` geben den **Index** des kleinsten bzw. größten Elements zurück.
Kommt der Wert mehrfach vor, ist es der erste Index.

Mit dem Index kann man in einer anderen Liste nachsehen, zu wem der Wert gehört.''',
     """import numpy as np

tage = ['Mo', 'Di', 'Mi', 'Do', 'Fr']
temperaturen = np.array([12, 15, 11, 18, 18])
print(temperaturen.argmax())
print(tage[temperaturen.argmax()])
print(tage[temperaturen.argmin()])""")

t('Berechne mit `np.arange()` und `sum()` die Summe der Zahlen von 1 bis 100.',
  NP, """print(np.arange(1, 101).sum())""")
t('Berechne die Summe der Quadratzahlen von 1² bis 10².',
  NP, """print((np.arange(1, 11) ** 2).sum())""")
t('Berechne die Summe aller ungeraden Zahlen von 1 bis 99.',
  NP, """print(np.arange(1, 100, 2).sum())""")
t('Gib die niedrigste und die höchste Temperatur aus.',
  NP + '\ntemperaturen = np.array([12.5, 15.0, 9.5, 18.0, 14.5])',
  """print(temperaturen.min())
print(temperaturen.max())""")
t('Gib die Spannweite (größter minus kleinster Wert) der Messwerte aus.',
  NP + '\nmesswerte = np.array([23, 17, 31, 25, 19])',
  """print(messwerte.max() - messwerte.min())""")
t('Gib den Notendurchschnitt aus, gerundet auf zwei Nachkommastellen.',
  NP + '\nnoten = np.array([2, 3, 1, 2, 4, 2, 3])',
  """print(np.round(noten.mean(), 2))""")
t('Berechne mit `prod()` das Produkt der Zahlen von 1 bis 10 (also 10!).',
  NP, """print(np.arange(1, 11).prod())""")
t('Gib aus, an welchem Tag es am wärmsten und an welchem es am kältesten war.',
  NP + "\ntage = ['Mo', 'Di', 'Mi', 'Do', 'Fr', 'Sa', 'So']\ntemperaturen = np.array([14, 17, 12, 19, 21, 16, 11])",
  """print(tage[temperaturen.argmax()])
print(tage[temperaturen.argmin()])""")
t('Gib den Namen der Person mit den meisten Punkten und ihre Punktzahl aus.',
  NP + "\nnamen = ['Anna', 'Ben', 'Cem', 'Dana']\npunkte = np.array([78, 91, 85, 64])",
  """i = punkte.argmax()
print(namen[i], punkte[i])""")
t('Berechne den Gesamtbetrag des Einkaufs (Summe aus Preis mal Menge), gerundet auf zwei Nachkommastellen.',
  NP + '\npreise = np.array([0.99, 2.5, 1.2])\nmengen = np.array([3, 2, 5])',
  """print(np.round((preise * mengen).sum(), 2))""")
t('Berechne den Mittelwert der Werte von `np.linspace(0, 10, 21)`.',
  NP, """print(np.linspace(0, 10, 21).mean())""")
t('Gib aus, um wie viel jeder Wert vom Mittelwert abweicht.',
  NP + '\na = np.array([4, 7, 10, 3])',
  """print(a - a.mean())""")
t('Berechne die Summe `1/2 + 1/4 + 1/8 + ... + 1/1024`. Verwende `np.arange(1, 11)`.',
  NP, """print((1 / 2 ** np.arange(1, 11)).sum())""")
t('''Gib mit einem f-String den Mittelwert, das Minimum und das Maximum der Zeiten aus wie unten.
Der Mittelwert soll zwei Nachkommastellen haben (`:.2f`).''',
  NP + '\nzeiten = np.array([12.4, 11.9, 13.1, 12.0, 12.7])',
  """print(f'Mittelwert: {zeiten.mean():.2f}, Minimum: {zeiten.min()}, Maximum: {zeiten.max()}')""")
predict("""import numpy as np
a = np.array([5, 3, 9, 3, 9])
print(a.sum())
print(a.mean())
print(a.argmin())
print(a.argmax())
print(np.array([2, 2, 2]).prod())""")

# ---------------------------------------------------------------- 7
sec('Indizieren und Slicing')
expl('''#### Zugriff wie bei Listen

Auf einzelne Elemente und Teile eines Arrays greift man wie bei Listen zu:

- `a[0]` ist das erste, `a[-1]` das letzte Element.
- `a[2:5]` sind die Elemente mit Index 2, 3 und 4, `a[::2]` jedes zweite, `a[::-1]` alle rückwärts.
- Mit `a[i] = wert` ändert man ein Element.

Anders als bei Listen kann man einem ganzen Teil **eine Zahl** zuweisen: `a[1:4] = 0` setzt drei Elemente auf 0.
Auch `a[:3] *= 2` funktioniert.''',
     """import numpy as np

a = np.arange(10, 20)
print(a)
print(a[0], a[-1])
print(a[2:5])
print(a[::2])
print(a[::-1])
a[0] = 99
a[1:4] = 0
print(a)""")
expl('''#### Achtung: Datentyp beim Zuweisen

Ein Array behält seinen Datentyp. Weist man einem Array mit ganzen Zahlen eine Kommazahl zu,
werden die Nachkommastellen **abgeschnitten**.''',
     """import numpy as np

a = np.array([1, 2, 3])
a[0] = 7.9
print(a)
b = np.array([1.0, 2.0, 3.0])
b[0] = 7.9
print(b)""")
expl('''#### Achtung: Ein Slice ist keine Kopie

Bei Listen ist `liste[1:4]` eine neue Liste. Bei Arrays ist `a[1:4]` dagegen nur eine **Ansicht** (englisch *view*)
auf einen Teil von `a`. Ändert man die Ansicht, ändert sich auch `a`!

Will man eine unabhängige Kopie, schreibt man `a[1:4].copy()` oder `a.copy()`.''',
     """import numpy as np

a = np.array([1, 2, 3, 4, 5])
teil = a[1:4]
teil[0] = 99
print(a)

b = np.array([1, 2, 3, 4, 5])
kopie = b[1:4].copy()
kopie[0] = 99
print(b)
print(kopie)""")

A = NP + '\na = np.array([5, 10, 15, 20, 25, 30, 35, 40])'
t('Gib das erste und das letzte Element von `a` aus.', A, """print(a[0], a[-1])""")
t('Gib die ersten drei Elemente von `a` aus.', A, """print(a[:3])""")
t('Gib die letzten drei Elemente von `a` aus.', A, """print(a[-3:])""")
t('Gib die Elemente mit Index 2 bis 5 von `a` aus.', A, """print(a[2:6])""")
t('Gib jedes zweite Element von `a` aus, beginnend beim ersten.', A, """print(a[::2])""")
t('Gib jedes zweite Element von `a` aus, beginnend beim zweiten.', A, """print(a[1::2])""")
t('Gib `a` rückwärts aus.', A, """print(a[::-1])""")
t('Setze das erste Element von `a` auf 0 und das letzte auf 100. Gib `a` aus.', A,
  """a[0] = 0
a[-1] = 100
print(a)""")
t('Setze die Elemente mit Index 2 bis 4 von `a` auf -1. Gib `a` aus.', A,
  """a[2:5] = -1
print(a)""")
t('Setze jedes zweite Element von `a` auf 0, beginnend beim ersten. Gib `a` aus.', A,
  """a[::2] = 0
print(a)""")
t('Verdopple die erste Hälfte von `a` mit `*=`. Gib `a` aus.', A,
  """a[:4] *= 2
print(a)""")
t('Vertausche das erste und das letzte Element von `a`. Gib `a` aus.', A,
  """a[0], a[-1] = a[-1], a[0]
print(a)""")
t('Erstelle mit `copy()` eine Kopie von `a`. Setze in der Kopie alle Elemente auf 1. Gib danach `a` und die Kopie aus.', A,
  """kopie = a.copy()
kopie[:] = 1
print(a)
print(kopie)""")
t('''Berechne mit Slicing für jedes Element (außer dem ersten) die Differenz zum vorherigen Element: `a[1:] - a[:-1]`.''',
  NP + '\nwerte = np.array([3, 7, 8, 12, 20])',
  """print(werte[1:] - werte[:-1])""")
t('Gib die Summe der ersten vier und die Summe der letzten vier Elemente von `a` aus.', A,
  """print(a[:4].sum())
print(a[4:].sum())""")
predict("""import numpy as np
a = np.arange(6)
b = a[2:5]
b[:] = 0
print(a)
c = a.copy()
c[0] = 9
print(a[0], c[0])
a[1] = 2.99
print(a)""")

# ---------------------------------------------------------------- 8
sec('Kumulierte Summen, Differenzen und Verbinden')
expl('''#### `cumsum()`, `cumprod()` und `np.diff()`

- `a.cumsum()`: die **kumulierte Summe**. Jedes Element ist die Summe aller Elemente bis zu dieser Stelle (laufende Summe).
- `a.cumprod()`: entsprechend das laufende Produkt.
- `np.diff(a)`: die Differenzen benachbarter Elemente, also `a[1] - a[0]`, `a[2] - a[1]`, ... Das Ergebnis ist um 1 kürzer.

`np.diff()` ist das Gegenstück zu `cumsum()`.''',
     """import numpy as np

a = np.array([3, 1, 4, 1, 5])
print(a.cumsum())
print(a.cumprod())
print(np.diff(a))
print(np.diff(a.cumsum()))""")
expl('''#### Arrays verbinden und verlängern

Ein Array hat eine feste Länge. Es gibt kein `a.append()`. Stattdessen erzeugen diese Funktionen ein **neues** Array:

- `np.append(a, wert)` hängt einen Wert (oder mehrere Werte als Liste) hinten an.
- `np.concatenate([a, b])` hängt mehrere Arrays aneinander.

Will man in einer Schleife viele Werte sammeln, nimmt man besser eine Liste mit `append()`
und macht erst am Ende mit `np.array(liste)` ein Array daraus.''',
     """import numpy as np

a = np.array([1, 2, 3])
b = np.array([7, 8])
print(np.append(a, 4))
print(np.append(a, [4, 5]))
print(np.concatenate([a, b]))
print(np.concatenate([b, a, b]))
print(a)""")

t('Gib mit `cumsum()` die laufende Summe der Zahlen 1 bis 10 aus (das sind die Dreieckszahlen).',
  NP, """print(np.arange(1, 11).cumsum())""")
t('Gib mit `cumprod()` die Fakultäten 1!, 2!, ..., 10! aus.',
  NP, """print(np.arange(1, 11).cumprod())""")
t('Das Konto hat am Anfang 100 Euro. Gib mit `cumsum()` den Kontostand nach jeder Buchung aus.',
  NP + '\nbuchungen = np.array([50, -20, -45, 100, -30])',
  """print(100 + buchungen.cumsum())""")
t('Gib mit `np.diff()` aus, wie viele Kilometer an jedem Tag gefahren wurden.',
  NP + '\nkilometerstand = np.array([12500, 12580, 12580, 12710, 12755])',
  """print(np.diff(kilometerstand))""")
t('Gib die Gesamtstrecke aller Tage aus und den Durchschnitt pro Tag.',
  NP + '\nkilometerstand = np.array([12500, 12580, 12580, 12710, 12755])',
  """tage = np.diff(kilometerstand)
print(tage.sum())
print(tage.mean())""")
t('Ein Läufer hat nach jeder Runde die Gesamtzeit in Sekunden notiert. Gib die Zeiten der einzelnen Runden aus. Die erste Runde ist die erste Gesamtzeit.',
  NP + '\ngesamtzeit = np.array([62, 125, 190, 251])',
  """print(np.concatenate([gesamtzeit[:1], np.diff(gesamtzeit)]))""")
t('Gib aus, um wie viel Prozent die Werte von einem Jahr zum nächsten gewachsen sind, gerundet auf eine Nachkommastelle.',
  NP + '\neinwohner = np.array([2000, 2100, 2310, 2310, 2541])',
  """print(np.round(np.diff(einwohner) / einwohner[:-1] * 100, 1))""")
t('Hänge mit `np.append()` die Note 2 an `noten` an. Gib das neue Array aus.',
  NP + '\nnoten = np.array([3, 1, 2, 4])',
  """noten = np.append(noten, 2)
print(noten)""")
t('Verbinde die Noten beider Kurse zu einem Array und gib es und den Gesamtdurchschnitt aus (zwei Nachkommastellen).',
  NP + '\nkurs_a = np.array([2, 3, 1, 2])\nkurs_b = np.array([4, 2, 3])',
  """alle = np.concatenate([kurs_a, kurs_b])
print(alle)
print(np.round(alle.mean(), 2))""")
t('Sammle in einer Schleife alle Zahlen von 1 bis 50, die durch 7 teilbar sind, in einer Liste. Mache daraus ein Array und gib es aus.',
  NP,
  """liste = []
for i in range(1, 51):
    if i % 7 == 0:
        liste.append(i)
a = np.array(liste)
print(a)""")
predict("""import numpy as np
a = np.array([2, 2, 2, 2])
print(a.cumsum())
print(a.cumprod())
print(np.diff(np.array([1, 4, 9, 16])))
print(np.append(np.array([1]), [2, 3]))
print(len(np.concatenate([a, a])))""")

# ---------------------------------------------------------------- 9
sec('Gemischte Übungen')
t('''Erstelle eine Wertetabelle für `f(x) = x² / 2` mit neun Werten von -2 bis 2 (`np.linspace()`).
Gib die Wertepaare mit `zip()` aus, beide mit zwei Nachkommastellen wie unten.''',
  NP,
  """x = np.linspace(-2, 2, 9)
y = x ** 2 / 2
for xi, yi in zip(x, y):
    print(f'{xi:.2f} {yi:.2f}')""")
t('Ein Kapital von 1000 Euro wird mit 3 % pro Jahr verzinst. Gib das Kapital nach 0 bis 5 Jahren aus, gerundet auf zwei Nachkommastellen.',
  NP,
  """jahre = np.arange(6)
print(np.round(1000 * 1.03 ** jahre, 2))""")
t('Gib für den Einkauf den Gesamtbetrag aus und den Artikel, für den am meisten bezahlt wurde.',
  NP + "\nartikel = ['Brot', 'Milch', 'Käse', 'Äpfel']\npreise = np.array([2.49, 1.19, 3.99, 0.6])\nmengen = np.array([1, 3, 2, 6])",
  """betraege = preise * mengen
print(np.round(betraege.sum(), 2))
print(artikel[betraege.argmax()])""")
t('''Gib für die Temperaturen der Woche den Mittelwert (eine Nachkommastelle) aus und darunter die größte Veränderung
von einem Tag zum nächsten (als Betrag).''',
  NP + '\ntemperaturen = np.array([14, 17, 12, 19, 21, 16, 11])',
  """print(np.round(temperaturen.mean(), 1))
print(np.abs(np.diff(temperaturen)).max())""")
t('Skaliere die Werte so, dass der kleinste 0 und der größte 1 wird: `(a - min) / (max - min)`.',
  NP + '\na = np.array([10, 15, 30, 20, 50])',
  """print((a - a.min()) / (a.max() - a.min()))""")
t('Berechne für jeden Lauf die Pace (Minuten pro Kilometer), gerundet auf eine Nachkommastelle.',
  NP + '\nstrecke_km = np.array([5, 10, 21.1, 3])\nzeit_min = np.array([27, 58, 130, 15])',
  """print(np.round(zeit_min / strecke_km, 1))""")
t('Berechne für jede Person den BMI `gewicht / groesse²`, gerundet auf eine Nachkommastelle.',
  NP + '\ngewicht = np.array([60, 72, 85, 55])\ngroesse = np.array([1.65, 1.80, 1.75, 1.60])',
  """print(np.round(gewicht / groesse ** 2, 1))""")
t('Berechne die Summe der Quadrate aller geraden Zahlen von 2 bis 20.',
  NP, """print((np.arange(2, 21, 2) ** 2).sum())""")
t('''Berechne den gleitenden Mittelwert über drei Werte: Für jede Stelle der Mittelwert aus dem Wert und seinen beiden Nachfolgern.
Verwende `(a[:-2] + a[1:-1] + a[2:]) / 3`.''',
  NP + '\na = np.array([3, 6, 9, 3, 6, 12, 0])',
  """print((a[:-2] + a[1:-1] + a[2:]) / 3)""")
t('''Berechne die Quadrate der Zahlen in `liste` einmal mit einer List Comprehension und einmal mit numpy.
Prüfe mit `==` und `tolist()`, ob beide Ergebnisse gleich sind, und gib `True` oder `False` aus.''',
  NP + '\nliste = [4, 7, 1, 9, 3]',
  """mit_liste = [x ** 2 for x in liste]
mit_numpy = (np.array(liste) ** 2).tolist()
print(mit_liste == mit_numpy)""")
t('''Ein Ball fällt aus 20 m Höhe. Nach jedem Aufprall erreicht er 60 % der vorherigen Höhe.
Gib die Höhen nach 0 bis 6 Aufprallen aus (gerundet auf zwei Nachkommastellen) und die Summe dieser Höhen.''',
  NP,
  """hoehen = 20 * 0.6 ** np.arange(7)
print(np.round(hoehen, 2))
print(np.round(hoehen.sum(), 2))""")
t('''Die Punkte einer Klassenarbeit sollen in Prozent umgerechnet werden (maximal 40 Punkte).
Gib die Prozente als ganze Zahlen (abgerundet) aus und darunter den Durchschnitt der Prozente, gerundet auf eine Nachkommastelle.''',
  NP + '\npunkte = np.array([32, 40, 18, 27, 35, 22])',
  """prozent = np.floor(punkte / 40 * 100).astype(int)
print(prozent)
print(np.round(prozent.mean(), 1))""")
t('''Erstelle mit `np.full()` ein Array mit 12 Monatsbeiträgen von 15 Euro. Im Dezember (letzter Monat) gibt es 50 % Rabatt.
Gib das Array und den Jahresbetrag aus.''',
  NP,
  """beitraege = np.full(12, 15.0)
beitraege[-1] *= 0.5
print(beitraege)
print(beitraege.sum())""")
predict("""import numpy as np
a = np.arange(1, 6)
print(a[::-1] * a)
print((a * a).sum())
print(np.diff(a ** 2))
print(a.cumsum()[-1] == a.sum())
print(np.round(a / 3, 2))""")

generate('numpy_grundlagen', 'numpy: Grundlagen', INTRO)
