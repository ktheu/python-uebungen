# Erzeugt ../extern/pytorch_tensoren.ipynb (siehe nbgen.py). Erstes Notebook der PyTorch-Reihe:
# pytorch_tensoren, pytorch_lernen, pytorch_netze, pytorch_bilder.
#
# Läuft nicht in JupyterLite (kein PyTorch in Pyodide), sondern in Google Colab. Lokal in der py-3.13-venv p313torch
# (PyTorch für die CPU):
#     <venv>/python generator/gen_pytorch_tensoren.py
# Kein Pyodide-Check. Erwartete Ausgaben nur für Dinge, die überall gleich herauskommen (Formen, Datentypen, einfache Rechnungen);
# Zufallszahlen und Training nur in Beispielen oder bei kind='free'. Diagramme nur bei kind='free' (Colab zeigt Bild-Anhänge evtl. nicht an).
from nbgen import sec, generate
from torchhilfe import t, expl, predict, reihe, COLAB, SCHLUSS

INTRO = '''**PyTorch** ist eines der beiden großen Pakete für **Deep Learning**, also für große neuronale Netze, wie sie hinter Bilderkennung,
Übersetzungsprogrammen und Sprachmodellen stecken. In der scikit-learn-Reihe hast du neuronale Netze schon benutzt. Mit PyTorch baust und trainierst
du sie selbst und siehst, was dabei passiert.

Grundlage von allem sind **Tensoren**: Arrays wie in numpy, mit denen PyTorch rechnet, auch auf der Grafikkarte, und die sich merken können,
wie sie berechnet wurden (das braucht man für das Lernen, Notebook 2).

''' + reihe(1) + '''

Vorausgesetzt werden *numpy: Grundlagen* und *numpy: Zweidimensionale Arrays*.

''' + COLAB + '''

''' + SCHLUSS

T = 'import torch'

# ---------------------------------------------------------------- 1
sec('Tensoren erzeugen')
expl('''#### `torch.tensor()`

Ein **Tensor** ist ein Array mit Zahlen, genau wie ein numpy-Array: eine Zahl (0 Dimensionen), eine Liste (1 Dimension, ein **Vektor**),
eine Tabelle (2 Dimensionen, eine **Matrix**) oder mehr Dimensionen (z. B. ein Stapel von Bildern). `torch.tensor(liste)` erzeugt einen Tensor aus einer Liste.

- `t.shape` ist die **Form** (ein `torch.Size`, wie ein Tupel), `t.ndim` die Anzahl der Dimensionen, `t.numel()` die Anzahl der Zahlen.
- `t.dtype` ist der **Datentyp**: Ganze Zahlen werden `torch.int64`, Kommazahlen `torch.float32` (Kommazahlen mit 32 Bit, genug für neuronale Netze).''',
     """import torch

a = torch.tensor([1, 2, 3])
b = torch.tensor([[1.5, 2.0], [3.0, 4.0], [5.0, 6.0]])
print(a)
print(b)
print(a.shape, b.shape)
print(b.ndim, b.numel())
print(a.dtype, b.dtype)""")
expl('''#### Tensoren mit Mustern

Wie in numpy gibt es Funktionen, die Tensoren mit bestimmten Werten erzeugen. Die Form gibt man als einzelne Zahlen oder als Tupel an.

| Aufruf | Ergebnis |
|---|---|
| `torch.zeros(2, 3)`, `torch.ones(2, 3)` | lauter Nullen bzw. Einsen (Kommazahlen) |
| `torch.full((2, 3), 7.0)` | lauter 7.0 |
| `torch.arange(0, 10, 2)` | 0, 2, 4, 6, 8 (ohne die 10) |
| `torch.linspace(0, 1, 5)` | 5 gleichmäßig verteilte Werte von 0 bis 1 |
| `torch.eye(3)` | Einheitsmatrix (Einsen auf der Diagonalen) |

Mit `dtype=torch.float32` oder `t.float()` wird ein Tensor zu Kommazahlen, mit `t.long()` zu ganzen Zahlen (`int64`).''',
     """import torch

print(torch.zeros(2, 3))
print(torch.full((2, 2), 7.0))
print(torch.arange(0, 10, 2))
print(torch.linspace(0, 1, 5))
print(torch.eye(3))
print(torch.arange(3).float(), torch.tensor([1.7, 2.2]).long())""")

t('Erzeuge einen Tensor mit den Zahlen 4, 8, 15, 16, 23, 42 und gib ihn, seine Form und seinen Datentyp aus.', T,
  """a = torch.tensor([4, 8, 15, 16, 23, 42])
print(a)
print(a.shape, a.dtype)""")
t('Erzeuge die Matrix mit den Zeilen 1, 2, 3 und 4, 5, 6 als Kommazahlen (`dtype=torch.float32`) und gib sie, ihre Form und die Anzahl der Zahlen aus.', T,
  """m = torch.tensor([[1, 2, 3], [4, 5, 6]], dtype=torch.float32)
print(m)
print(m.shape, m.numel())""")
t('Gib einen Tensor mit den ungeraden Zahlen von 1 bis 19 aus (`arange`) und einen mit 6 gleichmäßig verteilten Werten von −1 bis 1 (`linspace`).', T,
  """print(torch.arange(1, 20, 2))
print(torch.linspace(-1, 1, 6))""")
t('Erzeuge einen 3 × 4-Tensor aus lauter Einsen und einen 2 × 2 × 2-Tensor aus lauter Nullen. Gib beide Formen und die Anzahl der Dimensionen des zweiten aus.', T,
  """einsen = torch.ones(3, 4)
nullen = torch.zeros(2, 2, 2)
print(einsen.shape, nullen.shape)
print(nullen.ndim)""")
t('Wandle den Tensor `t` in Kommazahlen und wieder zurück in ganze Zahlen um und gib beide und ihre Datentypen aus. Was passiert mit 2.9 und −1.5?', T + '\n\nt = torch.tensor([2.9, -1.5, 3.0])',
  """ganz = t.long()
print(ganz, ganz.dtype)
print(ganz.float(), ganz.float().dtype)""")
t('Erzeuge eine 4 × 4-Einheitsmatrix und multipliziere sie mit 5.', T, "print(torch.eye(4) * 5)")
predict("""import torch

a = torch.tensor([[1, 2], [3, 4], [5, 6]])
print(a.shape)
print(a.ndim, a.numel())
print(a.dtype)""", erklaerung='''- 3 Zeilen mit je 2 Zahlen: `torch.Size([3, 2])`.
- 2 Dimensionen, `3 · 2 = 6` Zahlen.
- Nur ganze Zahlen in der Liste, deshalb `torch.int64`.''')
predict("""import torch

print(torch.arange(5))
print(torch.arange(2, 8, 3))
print(torch.zeros(3).dtype)""", erklaerung='''- `arange(5)` beginnt bei 0 und endet vor 5: `tensor([0, 1, 2, 3, 4])`.
- Von 2 in Schritten von 3, vor 8 aufhören: 2, 5: `tensor([2, 5])`.
- `zeros` erzeugt Kommazahlen: `torch.float32`.''')

# ---------------------------------------------------------------- 2
sec('Die Form verändern')
expl('''#### `reshape()`, `flatten()` und `.T`

- `t.reshape(2, 3)` ordnet dieselben Zahlen in einer neuen Form an (zeilenweise). Eine der Zahlen darf `-1` sein, dann wird sie passend ausgerechnet.
- `t.flatten()` macht aus jedem Tensor einen Vektor (z. B. ein Bild aus 28 × 28 Pixeln zu 784 Zahlen).
- `m.T` ist die **transponierte** Matrix (Zeilen und Spalten vertauscht).''',
     """import torch

t = torch.arange(6)
m = t.reshape(2, 3)
print(m)
print(t.reshape(3, -1))
print(m.T)
print(m.flatten())""")
expl('''#### Dimensionen hinzufügen und entfernen, Tensoren verbinden

Neuronale Netze verarbeiten immer einen **Stapel** (*batch*) von Beispielen auf einmal: Die erste Dimension ist die Nummer des Beispiels.
Ein einzelnes Beispiel muss deshalb oft eine zusätzliche Dimension bekommen.

- `t.unsqueeze(0)` fügt vorne eine Dimension der Größe 1 hinzu (Form `[3]` wird `[1, 3]`), `t.unsqueeze(1)` an Stelle 1 (`[3, 1]`).
- `t.squeeze()` entfernt alle Dimensionen der Größe 1.
- `torch.cat([a, b], dim=0)` hängt Tensoren entlang einer vorhandenen Dimension aneinander, `torch.stack([a, b])` legt sie entlang einer **neuen** Dimension übereinander.''',
     """import torch

a = torch.tensor([1, 2, 3])
b = torch.tensor([4, 5, 6])
print(a.unsqueeze(0).shape, a.unsqueeze(1).shape)
print(a.unsqueeze(0).squeeze().shape)
print(torch.cat([a, b], dim=0))
print(torch.stack([a, b]))""")

t('Ordne die Zahlen 1 bis 12 als 3 × 4-Matrix an, dann als 2 × 6-Matrix und dann als 4 Zeilen mit passender Spaltenzahl (`-1`).', T,
  """t = torch.arange(1, 13)
print(t.reshape(3, 4))
print(t.reshape(2, 6))
print(t.reshape(4, -1))""")
t('Erzeuge die Zahlen 0 bis 23 als Tensor der Form 2 × 3 × 4 und gib die Form aus. Mache daraus mit `flatten()` wieder einen Vektor und gib seine Form aus.', T,
  """t = torch.arange(24).reshape(2, 3, 4)
print(t.shape)
print(t.flatten().shape)""")
t('Gib die transponierte Matrix von `m` und ihre Form aus.', T + '\n\nm = torch.tensor([[1, 2, 3], [4, 5, 6]])',
  """print(m.T)
print(m.T.shape)""")
t('''Ein Netz erwartet die Eingabe als Stapel der Form `[Anzahl, 4]`. Mache aus dem einzelnen Beispiel `x` (Form `[4]`) einen Stapel mit einem Beispiel und gib die Form aus.
Mache ihn danach mit `squeeze()` wieder zu einem Vektor.''', T + '\n\nx = torch.tensor([5.1, 3.5, 1.4, 0.2])',
  """stapel = x.unsqueeze(0)
print(stapel.shape)
print(stapel.squeeze().shape)""")
t('Hänge die Tensoren `a` und `b` aneinander (`cat`) und lege sie übereinander (`stack`). Gib beide Ergebnisse und ihre Formen aus.', T + '\n\na = torch.tensor([1, 2])\nb = torch.tensor([3, 4])',
  """c = torch.cat([a, b])
s = torch.stack([a, b])
print(c, c.shape)
print(s, s.shape)""")
t('''Die beiden Matrizen `a` und `b` haben je 2 Zeilen. Hänge sie einmal untereinander (`dim=0`) und einmal nebeneinander (`dim=1`) an und gib die Ergebnisse aus.''',
  T + '\n\na = torch.tensor([[1, 2], [3, 4]])\nb = torch.tensor([[5, 6], [7, 8]])',
  """print(torch.cat([a, b], dim=0))
print(torch.cat([a, b], dim=1))""")
predict("""import torch

t = torch.arange(12).reshape(3, 4)
print(t.shape)
print(t.reshape(-1, 6).shape)
print(t.unsqueeze(0).shape)
print(torch.stack([t, t, t, t, t]).shape)""", erklaerung='''- 12 Zahlen in 3 Zeilen zu je 4: `torch.Size([3, 4])`.
- 6 Spalten, die Zeilenzahl wird ausgerechnet: `12 / 6 = 2`, also `torch.Size([2, 6])`.
- Vorne kommt eine Dimension der Größe 1 dazu: `torch.Size([1, 3, 4])`.
- 5 gleiche Matrizen übereinander gestapelt: `torch.Size([5, 3, 4])`.''')

# ---------------------------------------------------------------- 3
sec('Auswählen')
expl('''#### Indizieren und Slicing

Wie bei numpy-Arrays: `t[0]` ist das erste Element (bei einer Matrix die erste Zeile), `m[1, 2]` das Element in Zeile 1, Spalte 2, `m[:, 0]` die erste Spalte,
`t[1:3]` die Elemente 1 und 2. Das Ergebnis ist wieder ein Tensor, auch bei einer einzelnen Zahl. `.item()` macht daraus eine gewöhnliche Python-Zahl,
`.tolist()` aus einem Tensor eine (verschachtelte) Liste.''',
     """import torch

m = torch.tensor([[10, 20, 30], [40, 50, 60]])
print(m[0])
print(m[1, 2], m[1, 2].item())
print(m[:, 0])
print(m[:, 1:])
print(m.tolist())""")
expl('''#### Auswählen mit Bedingungen

Ein Vergleich wie `t > 3` ergibt einen Tensor aus `True` und `False` (eine **Maske**). `t[t > 3]` wählt die passenden Elemente aus.
`torch.where(bedingung, a, b)` nimmt elementweise `a`, wo die Bedingung gilt, und sonst `b`.''',
     """import torch

t = torch.tensor([3, -1, 4, -1, 5, -9])
print(t > 0)
print(t[t > 0])
print((t < 0).sum())
print(torch.where(t > 0, t, torch.zeros_like(t)))""")

M = T + '\n\nm = torch.tensor([[2, 7, 1, 8], [2, 8, 1, 8], [4, 5, 9, 0]])'
t('Gib aus: die letzte Zeile von `m`, die Spalte mit Index 2, das Element in Zeile 1 und Spalte 3 als Python-Zahl.', M,
  """print(m[-1])
print(m[:, 2])
print(m[1, 3].item())""")
t('Gib die ersten beiden Zeilen und davon nur die Spalten 1 bis 3 (`1:4`) aus.', M, "print(m[:2, 1:4])")
t('Gib alle Zahlen von `m` aus, die größer als 4 sind, und wie viele es sind.', M,
  """print(m[m > 4])
print((m > 4).sum().item())""")
t('Ersetze in `m` alle Zahlen kleiner als 3 durch 0 (`torch.where`, `torch.zeros_like(m)`) und gib das Ergebnis aus.', M,
  "print(torch.where(m < 3, torch.zeros_like(m), m))")
t('Setze in `m` die ganze Spalte 0 auf −1 (`m[:, 0] = -1`) und gib `m` aus. Gib danach `m` als Liste aus.', M,
  """m[:, 0] = -1
print(m)
print(m.tolist())""")
predict("""import torch

t = torch.tensor([5, 2, 8, 1])
print(t[1:3])
print(t[t % 2 == 0])
print(t[-1].item() + t[0].item())""", erklaerung='''- Die Elemente mit Index 1 und 2: `tensor([2, 8])`.
- Die geraden Zahlen (Modulo-Operator `%`): `tensor([2, 8])`.
- `.item()` liefert Python-Zahlen: `1 + 5 = 6`.''')

# ---------------------------------------------------------------- 4
sec('Rechnen')
expl('''#### Elementweise und mit Matrizen

- `+`, `-`, `*`, `/`, `**` rechnen **elementweise**, wie in numpy. Mit einer einzelnen Zahl wird jedes Element verrechnet.
- Haben die Tensoren verschiedene Formen, wird der kleinere wenn möglich „gestreckt“ (**Broadcasting**): Eine Matrix plus ein Vektor addiert den Vektor zu jeder Zeile.
- `a @ b` ist die **Matrizenmultiplikation** (bei Vektoren das Skalarprodukt). Damit rechnet jede Schicht eines neuronalen Netzes.
- `torch.exp()`, `torch.sqrt()`, `torch.abs()` usw. wirken auf jedes Element. `t.round(decimals=2)` rundet.''',
     """import torch

a = torch.tensor([[1.0, 2.0], [3.0, 4.0]])
v = torch.tensor([10.0, 20.0])
print(a * 2)
print(a + v)
print(a @ v)
print(a @ a)
print(torch.sqrt(a).round(decimals=3))""")
expl('''#### Zusammenfassen mit `dim`

`t.sum()`, `t.mean()`, `t.max()`, `t.min()` fassen alle Zahlen zusammen. Mit `dim=0` wird **über die Zeilen** zusammengefasst (ein Ergebnis pro Spalte),
mit `dim=1` **über die Spalten** (ein Ergebnis pro Zeile). `t.argmax(dim=1)` gibt für jede Zeile die **Stelle** des größten Werts. So liest man später
ab, welche Klasse ein Netz vorhersagt. `mean()` geht nur mit Kommazahlen.''',
     """import torch

m = torch.tensor([[1.0, 5.0, 3.0], [8.0, 2.0, 6.0]])
print(m.sum(), m.mean())
print(m.sum(dim=0))
print(m.sum(dim=1))
print(m.max(dim=1).values)
print(m.argmax(dim=1))""")

R = T + '\n\na = torch.tensor([1.0, 2.0, 3.0])\nb = torch.tensor([4.0, 5.0, 6.0])'
t('Gib `a + b`, `a * b`, `b / a` (3 Nachkommastellen) und `a ** 2` aus.', R,
  """print(a + b)
print(a * b)
print((b / a).round(decimals=3))
print(a ** 2)""")
t('Berechne das Skalarprodukt von `a` und `b` auf zwei Wegen: mit `@` und mit `(a * b).sum()`.', R,
  """print(a @ b)
print((a * b).sum())""")
t('Berechne die Länge (den Betrag) von `b`: die Wurzel aus der Summe der Quadrate. Gib sie mit 4 Nachkommastellen aus (`.item()` und f-String).', R,
  "print(f'{torch.sqrt((b ** 2).sum()).item():.4f}')")
t('''Multipliziere die Matrix `w` mit dem Vektor `x` (`w @ x`) und addiere den Vektor `bias`. So rechnet eine Schicht eines Netzes mit 2 Neuronen und 3 Eingaben.''',
  T + '\n\nw = torch.tensor([[0.5, -1.0, 2.0], [1.0, 0.0, -0.5]])\nx = torch.tensor([2.0, 1.0, 4.0])\nbias = torch.tensor([0.1, -0.2])',
  "print(w @ x + bias)")
NOTEN = T + '''

# Zeilen: Personen, Spalten: Noten in Mathe, Deutsch, Englisch, Physik
noten = torch.tensor([[2.0, 3.0, 1.0, 2.0],
                      [1.0, 2.0, 2.0, 1.0],
                      [4.0, 3.0, 3.0, 5.0]])'''
t('Gib für jede Person den Notendurchschnitt aus und für jedes Fach den Durchschnitt (`mean` mit `dim`, 2 Nachkommastellen).', NOTEN,
  """print(noten.mean(dim=1).round(decimals=2))
print(noten.mean(dim=0).round(decimals=2))""")
t('Gib für jede Person den Index des Fachs mit der schlechtesten (größten) Note aus und die schlechteste Note insgesamt.', NOTEN,
  """print(noten.argmax(dim=1))
print(noten.max())""")
t('''Ziehe von jeder Zeile den Mittelwert der Spalte ab (Broadcasting: `noten - noten.mean(dim=0)`) und gib das Ergebnis aus (2 Nachkommastellen). Danach ist jeder
Spaltenmittelwert 0.''', NOTEN,
  """zentriert = noten - noten.mean(dim=0)
print(zentriert.round(decimals=2))""")
t('''Die **Softmax**-Funktion macht aus beliebigen Zahlen Wahrscheinlichkeiten: `e^x / Summe aller e^x`. Netze für die Klassifikation benutzen sie in der letzten Schicht.
Berechne sie für `z` von Hand (`torch.exp`), dann mit `torch.softmax(z, dim=0)`, und gib die Summe aus (alles mit 4 Nachkommastellen).''',
  T + '\n\nz = torch.tensor([2.0, 1.0, 0.1])',
  """p = torch.exp(z) / torch.exp(z).sum()
print(p.round(decimals=4))
print(torch.softmax(z, dim=0).round(decimals=4))
print(f'{p.sum().item():.4f}')""")
predict("""import torch

m = torch.tensor([[1, 2], [3, 4]])
print(m * m)
print(m @ m)
print(m.sum(dim=0))
print(m.argmax(dim=0))""", erklaerung='''- `*` multipliziert elementweise: `[[1, 4], [9, 16]]`.
- `@` ist die Matrizenmultiplikation: Zeile mal Spalte, z. B. oben links `1·1 + 2·3 = 7`: `[[7, 10], [15, 22]]`.
- `dim=0` fasst über die Zeilen zusammen, ein Ergebnis pro Spalte: `[4, 6]`.
- In beiden Spalten steht der größte Wert in Zeile 1: `[1, 1]`.''')

# ---------------------------------------------------------------- 5
sec('Zufall und numpy')
expl('''#### Zufällige Tensoren

`torch.manual_seed(0)` legt den Zufallsgenerator fest, sodass bei jedem Lauf dieselben Zahlen kommen (auf derselben PyTorch-Version und demselben Rechner).

- `torch.rand(2, 3)`: gleichverteilt zwischen 0 und 1
- `torch.randn(2, 3)`: normalverteilt mit Mittelwert 0 und Standardabweichung 1 (so werden die Gewichte von Netzen am Anfang gewählt)
- `torch.randint(1, 7, (10,))`: ganze Zahlen von 1 bis 6 (Würfel)
- `torch.randperm(5)`: die Zahlen 0 bis 4 in zufälliger Reihenfolge (zum Mischen von Daten)''',
     """import torch

torch.manual_seed(0)
print(torch.rand(2, 3))
print(torch.randn(3))
print(torch.randint(1, 7, (10,)))
print(torch.randperm(5))""")
expl('''#### Zwischen numpy und PyTorch

- `torch.tensor(array)` macht aus einem numpy-Array einen Tensor (eine Kopie). numpy-Kommazahlen sind `float64`; mit `dtype=torch.float32` wird daraus der übliche Typ.
- `t.numpy()` macht aus einem Tensor ein numpy-Array, z. B. zum Zeichnen mit matplotlib.
- Daten aus einer pandas-Tabelle erhält man mit `torch.tensor(df[spalten].to_numpy(), dtype=torch.float32)`.''',
     """import numpy as np
import torch

a = np.array([[1.5, 2.5], [3.5, 4.5]])
t = torch.tensor(a)
print(t.dtype)
t = torch.tensor(a, dtype=torch.float32)
print(t.dtype)
print(type(t.numpy()), t.numpy())""")

t('''Würfle 1000-mal mit `torch.randint` (Seed 1) und gib den Mittelwert der Augenzahlen aus (mit `.float()`, 2 Nachkommastellen). Er sollte nahe bei 3.5 liegen.''', T,
  """torch.manual_seed(1)
wuerfe = torch.randint(1, 7, (1000,))
print(f'{wuerfe.float().mean().item():.2f}')""", kind='free')
t('''Erzeuge 10000 normalverteilte Zahlen (Seed 2) und gib Mittelwert und Standardabweichung (`std()`) aus (2 Nachkommastellen). Sie sollten nahe bei 0 und 1 liegen.''', T,
  """torch.manual_seed(2)
z = torch.randn(10000)
print(f'{z.mean().item():.2f} {z.std().item():.2f}')""", kind='free')
t('''Prüfe, dass `manual_seed` den Zufall festlegt: Setze zweimal den Seed 5, erzeuge jedes Mal `torch.rand(3)` und vergleiche die beiden Tensoren mit `torch.equal()`.''', T,
  """torch.manual_seed(5)
a = torch.rand(3)
torch.manual_seed(5)
b = torch.rand(3)
print(torch.equal(a, b))""")
t('''Mische die Zeilen der Matrix `daten` zufällig (Seed 3): `daten[torch.randperm(4)]`. Gib das Ergebnis aus und prüfe, dass die Summe aller Zahlen gleich bleibt.''',
  T + '\n\ndaten = torch.tensor([[1, 10], [2, 20], [3, 30], [4, 40]])',
  """torch.manual_seed(3)
gemischt = daten[torch.randperm(4)]
print(gemischt)
print(gemischt.sum() == daten.sum())""", kind='free')
t('''Wandle das numpy-Array `werte` in einen `float32`-Tensor um, verdopple ihn und wandle das Ergebnis zurück in ein numpy-Array. Gib die Datentypen und das Ergebnis aus.''',
  'import numpy as np\nimport torch\n\nwerte = np.array([0.5, 1.5, 2.5])',
  """t = torch.tensor(werte, dtype=torch.float32)
ergebnis = (t * 2).numpy()
print(t.dtype, ergebnis.dtype)
print(ergebnis)""")
t('''Lade die Iris-Daten mit `load_iris()` aus scikit-learn (`daten.data` ist ein numpy-Array, `daten.target` die Arten 0, 1, 2) und mache daraus einen `float32`-Tensor `X`
und einen `int64`-Tensor `y`. Gib die Formen, die Datentypen und die Mittelwerte der vier Maße aus (2 Nachkommastellen).''',
  'import torch\nfrom sklearn.datasets import load_iris\n\ndaten = load_iris()',
  """X = torch.tensor(daten.data, dtype=torch.float32)
y = torch.tensor(daten.target)
print(X.shape, y.shape)
print(X.dtype, y.dtype)
print(X.mean(dim=0).round(decimals=2))""")
t('''Zeichne ein Histogramm (`plt.hist(t.numpy(), bins=30)`) von 5000 normalverteilten Zahlen aus `torch.randn` (Seed 0).''', T + '\nimport matplotlib.pyplot as plt',
  """torch.manual_seed(0)
t = torch.randn(5000)
plt.hist(t.numpy(), bins=30)
plt.show()""", kind='free')

# ---------------------------------------------------------------- 6
sec('Die Grafikkarte')
expl('''#### `device`

Neuronale Netze rechnen vor allem Matrizenmultiplikationen. Eine **Grafikkarte** (GPU) kann Tausende davon gleichzeitig ausführen und ist dafür viel schneller als
der Prozessor (CPU). In PyTorch liegt jeder Tensor auf einem **Gerät** (*device*): `t.device` zeigt es an, `t.to('cuda')` kopiert ihn auf die Grafikkarte
(`cuda` ist der Name der Schnittstelle von NVIDIA). Rechnen kann man nur mit Tensoren, die auf demselben Gerät liegen.

Üblich ist diese Zeile, die die Grafikkarte nimmt, wenn es eine gibt: `device = 'cuda' if torch.cuda.is_available() else 'cpu'`.

**In Colab** bekommst du eine Grafikkarte über *Laufzeit → Laufzeittyp ändern → T4 GPU*. Danach startet das Notebook neu. Für die kleinen Beispiele dieser Reihe
reicht die CPU; erst in Notebook 4 lohnt sich die Grafikkarte.''',
     """import torch

device = 'cuda' if torch.cuda.is_available() else 'cpu'
print(device)
t = torch.ones(3)
print(t.device)
t = t.to(device)
print(t.device)""")
t('''Erzeuge zwei zufällige 1000 × 1000-Matrizen (Seed 0) auf dem Gerät `device` (`torch.rand(1000, 1000, device=device)`), multipliziere sie und gib das Gerät
und die Form des Ergebnisses aus. Miss die Zeit mit `time.perf_counter()` vor und nach der Multiplikation. Probiere es mit und ohne Grafikkarte.''',
  'import time\nimport torch\n\ndevice = \'cuda\' if torch.cuda.is_available() else \'cpu\'',
  """torch.manual_seed(0)
a = torch.rand(1000, 1000, device=device)
b = torch.rand(1000, 1000, device=device)
start = time.perf_counter()
c = a @ b
ende = time.perf_counter()
print(c.device, c.shape)
print(f'{ende - start:.4f} s')""", kind='free')

# ---------------------------------------------------------------- 7
sec('Gemischte Übungen')
t('''Ein Graustufenbild besteht aus Helligkeiten von 0 (schwarz) bis 255 (weiß). Das Bild `bild` in der Zelle hat 4 × 4 Pixel. Gib die Form, die mittlere Helligkeit
(2 Nachkommastellen) und das hellste Pixel (Zeile und Spalte, mit `argmax()` und `divmod(index, 4)`) aus. Teile danach alle Werte durch 255 (dann liegen sie zwischen 0 und 1,
wie Netze es mögen) und gib das Ergebnis mit 2 Nachkommastellen aus.''',
  T + '\n\nbild = torch.tensor([[0, 50, 50, 0], [50, 200, 255, 50], [50, 210, 230, 50], [0, 50, 50, 0]], dtype=torch.float32)',
  """print(bild.shape)
print(f'{bild.mean().item():.2f}')
print(divmod(bild.argmax().item(), 4))
print((bild / 255).round(decimals=2))""")
t('''Abstände zwischen Punkten mit Broadcasting: `punkte` hat die Form `[4, 2]`. `punkte.unsqueeze(1) - punkte.unsqueeze(0)` hat die Form `[4, 4, 2]` und enthält alle
Differenzen. Berechne daraus die 4 × 4-Matrix aller Abstände (Wurzel der Summe der Quadrate über `dim=2`, 2 Nachkommastellen).''',
  T + '\n\npunkte = torch.tensor([[0.0, 0.0], [3.0, 4.0], [6.0, 0.0], [0.0, 8.0]])',
  """differenzen = punkte.unsqueeze(1) - punkte.unsqueeze(0)
print(differenzen.shape)
abstaende = torch.sqrt((differenzen ** 2).sum(dim=2))
print(abstaende.round(decimals=2))""")
t('''Ein Netz hat für 4 Bilder je 3 Werte ausgegeben (Zeilen von `ausgabe`, eine Spalte pro Klasse 0, 1, 2). Berechne mit `softmax` (`dim=1`) die Wahrscheinlichkeiten
(3 Nachkommastellen), die vorhergesagten Klassen (`argmax`) und den Anteil richtiger Vorhersagen im Vergleich mit `richtig`.''',
  T + '\n\nausgabe = torch.tensor([[2.0, 0.5, -1.0], [0.1, 0.2, 3.0], [1.0, 1.5, 0.5], [-0.5, 2.5, 0.0]])\nrichtig = torch.tensor([0, 2, 0, 1])',
  """p = torch.softmax(ausgabe, dim=1)
print(p.round(decimals=3))
vorhersage = p.argmax(dim=1)
print(vorhersage)
print((vorhersage == richtig).float().mean().item())""")
t('''Normiere die Spalten der Matrix `daten`: Ziehe von jeder Spalte ihren Mittelwert ab und teile durch ihre Standardabweichung (`std(dim=0)`). Gib das Ergebnis und
die Mittelwerte und Standardabweichungen danach aus (alles 2 Nachkommastellen). Das macht `StandardScaler` aus scikit-learn (der allerdings mit einer etwas anderen
Standardabweichung rechnet).''',
  T + '\n\ndaten = torch.tensor([[170.0, 60.0], [180.0, 80.0], [160.0, 55.0], [175.0, 75.0]])',
  """normiert = (daten - daten.mean(dim=0)) / daten.std(dim=0)
print(normiert.round(decimals=2))
print(normiert.mean(dim=0).abs().round(decimals=2), normiert.std(dim=0).round(decimals=2))""")
t('''Simuliere mit Tensoren 10000-mal das Werfen von zwei Würfeln (Seed 4, `torch.randint(1, 7, (10000, 2))`), addiere die Augenzahlen je Wurf und gib die relativen
Häufigkeiten der Summen 2 bis 12 aus (`torch.bincount()`, 3 Nachkommastellen). Die 7 sollte am häufigsten sein (etwa 0.167).''', T,
  """torch.manual_seed(4)
wuerfe = torch.randint(1, 7, (10000, 2))
summen = wuerfe.sum(dim=1)
haeufigkeit = torch.bincount(summen, minlength=13)[2:] / 10000
print(haeufigkeit.round(decimals=3))""", kind='free')

generate('pytorch_tensoren', 'PyTorch 1: Tensoren', INTRO, ordner='extern')
