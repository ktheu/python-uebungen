# Erzeugt ../extern/pytorch_netze.ipynb (siehe nbgen.py). Drittes Notebook der PyTorch-Reihe:
# pytorch_tensoren, pytorch_lernen, pytorch_netze, pytorch_bilder.
#
# Läuft nicht in JupyterLite, sondern in Google Colab. Lokal in der py-3.13-venv p313torch (PyTorch für die CPU).
# Kein Pyodide-Check. Erwartete Ausgaben nur für Aufbau, Formen und Anzahl der Gewichte; Training ist kind='free'
# (der Aufgabentext sagt, welche Werte ungefähr herauskommen). Diagramme nur bei kind='free'.
from nbgen import sec, generate
from torchhilfe import t, expl, predict, reihe, COLAB, SCHLUSS

INTRO = '''In diesem Notebook baust du **neuronale Netze** aus Schichten zusammen und trainierst sie für die Klassifikation. Du lernst, wie man Netze als
eigene Klassen schreibt, wie man die Daten in kleinen Portionen (Mini-Batches) verarbeitet und wie man mit Testdaten Überanpassung erkennt.
Als Daten dienen wieder die Halbmonde aus der scikit-learn-Reihe, damit du die Ergebnisse vergleichen kannst.

''' + reihe(3) + '''

Vorausgesetzt werden *PyTorch: Lernen*, *scikit-learn: Klassifikation* (Halbmonde, Überanpassung) und das Notebook *OOP 1: Klassen und Objekte*.

''' + COLAB + '''

''' + SCHLUSS

NN = 'import torch\nfrom torch import nn'
MONDE = '''import torch
from torch import nn
from sklearn.datasets import make_moons
from sklearn.model_selection import train_test_split

X, y = make_moons(n_samples=500, noise=0.25, random_state=0)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=0)
X_train = torch.tensor(X_train, dtype=torch.float32)
X_test = torch.tensor(X_test, dtype=torch.float32)
y_train = torch.tensor(y_train)
y_test = torch.tensor(y_test)'''
TRAINING = '''

def trainiere(modell, X, y, epochen, lernrate=0.01):
    """Trainiert das Modell mit allen Daten auf einmal und gibt die Liste der Verluste zurück."""
    verlustfunktion = nn.CrossEntropyLoss()
    optimierer = torch.optim.Adam(modell.parameters(), lr=lernrate)
    verluste = []
    for epoche in range(epochen):
        verlust = verlustfunktion(modell(X), y)
        optimierer.zero_grad()
        verlust.backward()
        optimierer.step()
        verluste.append(verlust.item())
    return verluste


def genauigkeit(modell, X, y):
    with torch.no_grad():
        return (modell(X).argmax(dim=1) == y).float().mean().item()'''

# ---------------------------------------------------------------- 1
sec('Schichten stapeln: nn.Sequential')
expl('''#### Ein Netz aus Schichten

`nn.Sequential(...)` schaltet Schichten hintereinander: Die Ausgabe der einen ist die Eingabe der nächsten.

```
nn.Sequential(nn.Linear(2, 16), nn.ReLU(), nn.Linear(16, 2))
```

hat 2 Eingaben, eine **verborgene Schicht** mit 16 Neuronen und 2 Ausgaben. Zwischen den `Linear`-Schichten steht eine **Aktivierungsfunktion**:
`nn.ReLU()` setzt negative Werte auf 0 und lässt positive unverändert. Ohne sie wären zwei `Linear`-Schichten hintereinander nur eine einzige lineare
Rechnung, und das Netz könnte keine gekrümmten Grenzen lernen. `print(modell)` zeigt den Aufbau.''',
     NN + """

torch.manual_seed(0)
modell = nn.Sequential(nn.Linear(2, 16), nn.ReLU(), nn.Linear(16, 2))
print(modell)
x = torch.tensor([[0.5, -1.0], [2.0, 0.3], [0.0, 0.0]])
print(modell(x).shape)
print(sum([p.numel() for p in modell.parameters()]))""")
expl('''#### Aktivierungsfunktionen

| Funktion | Rechnung | Werte |
|---|---|---|
| `nn.ReLU()` | `max(0, x)` | 0 bis ∞, der Standard in verborgenen Schichten |
| `nn.Sigmoid()` | `1 / (1 + e^(-x))` | 0 bis 1 (die S-Kurve) |
| `nn.Tanh()` | Tangens hyperbolicus | −1 bis 1 |

Man kann sie auch direkt als Funktion aufrufen: `torch.relu(x)`, `torch.sigmoid(x)`, `torch.tanh(x)`.''',
     NN + """

x = torch.tensor([-2.0, -0.5, 0.0, 0.5, 2.0])
print(nn.ReLU()(x))
print(nn.Sigmoid()(x).round(decimals=3))
print(nn.Tanh()(x).round(decimals=3))""")

t('Baue ein Netz mit 4 Eingaben, einer verborgenen Schicht mit 10 Neuronen (ReLU) und 3 Ausgaben. Gib den Aufbau und die Anzahl der Gewichte aus.', NN,
  """modell = nn.Sequential(nn.Linear(4, 10), nn.ReLU(), nn.Linear(10, 3))
print(modell)
print(sum([p.numel() for p in modell.parameters()]))""")
t('''Baue ein Netz mit 2 Eingaben, zwei verborgenen Schichten mit 32 und 16 Neuronen (je ReLU) und 2 Ausgaben. Gib die Form der Ausgabe für einen Stapel aus
100 zufälligen Eingaben (`torch.rand(100, 2)`) und die Anzahl der Gewichte aus.''', NN,
  """modell = nn.Sequential(nn.Linear(2, 32), nn.ReLU(), nn.Linear(32, 16), nn.ReLU(), nn.Linear(16, 2))
print(modell(torch.rand(100, 2)).shape)
print(sum([p.numel() for p in modell.parameters()]))""")
t('''Rechne die Anzahl der Gewichte des Netzes `Linear(2, 16)`, `ReLU`, `Linear(16, 2)` von Hand nach: Jede `Linear(a, b)`-Schicht hat `a · b` Gewichte und `b` bias-Werte.
Gib die Rechnung als Zahl aus und vergleiche mit PyTorch.''', NN,
  """print(2 * 16 + 16 + 16 * 2 + 2)
modell = nn.Sequential(nn.Linear(2, 16), nn.ReLU(), nn.Linear(16, 2))
print(sum([p.numel() for p in modell.parameters()]))""")
t('''Die einzelnen Schichten eines `Sequential` erreicht man wie bei einer Liste: `modell[0]` ist die erste. Gib für das Netz aus der vorigen Aufgabe die Form der
Gewichtsmatrix der ersten und der letzten Schicht und die Anzahl der Schichten (`len(modell)`) aus.''', NN,
  """modell = nn.Sequential(nn.Linear(2, 16), nn.ReLU(), nn.Linear(16, 2))
print(modell[0].weight.shape, modell[-1].weight.shape)
print(len(modell))""")
t('''Zeige, dass zwei `Linear`-Schichten **ohne** Aktivierung dasselbe sind wie eine: Setze bei `a = nn.Linear(1, 1)` und `b = nn.Linear(1, 1)` die Gewichte von Hand
(`a`: w = 2, b = 1; `b`: w = 3, b = −4) und berechne `b(a(x))` für `x = [[0], [1], [2]]`. Das Ergebnis liegt auf der Geraden `6x - 1`.''', NN,
  """a = nn.Linear(1, 1)
b = nn.Linear(1, 1)
with torch.no_grad():
    a.weight[:] = 2.0
    a.bias[:] = 1.0
    b.weight[:] = 3.0
    b.bias[:] = -4.0
    x = torch.tensor([[0.0], [1.0], [2.0]])
    print(b(a(x)))""")
t('''Zeichne die drei Aktivierungsfunktionen ReLU, Sigmoid und Tanh für x von −4 bis 4 (200 Punkte) in ein Diagramm mit Legende.''', NN + '\nimport matplotlib.pyplot as plt',
  """x = torch.linspace(-4, 4, 200)
plt.plot(x, torch.relu(x), label='ReLU')
plt.plot(x, torch.sigmoid(x), label='Sigmoid')
plt.plot(x, torch.tanh(x), label='Tanh')
plt.legend()
plt.grid()
plt.show()""", kind='free')
predict("""import torch
from torch import nn

relu = nn.ReLU()
print(relu(torch.tensor([-3.0, 0.0, 2.5])))
print(nn.Linear(10, 5).weight.shape)""", erklaerung='''- ReLU macht −3 zu 0 und lässt 0 und 2.5: `tensor([0.0000, 0.0000, 2.5000])`.
- Die Gewichtsmatrix hat eine Zeile pro Ausgabe und eine Spalte pro Eingabe: `torch.Size([5, 10])`.''')

# ---------------------------------------------------------------- 2
sec('Klassifizieren mit CrossEntropyLoss')
expl('''#### Eine Ausgabe pro Klasse

Für die Klassifikation hat das Netz **eine Ausgabe pro Klasse**. Die Ausgaben sind beliebige Zahlen (*logits*); `torch.softmax(..., dim=1)` würde daraus
Wahrscheinlichkeiten machen. Die vorhergesagte Klasse ist die mit der größten Ausgabe: `ausgabe.argmax(dim=1)`.

Die Verlustfunktion ist `nn.CrossEntropyLoss()`. Sie bekommt die rohen Ausgaben (Form `[Anzahl, Klassen]`) und die richtigen Klassen als ganze Zahlen
(Form `[Anzahl]`, Datentyp `int64`), wendet selbst Softmax an und bestraft kleine Wahrscheinlichkeiten für die richtige Klasse.''',
     NN + """

ausgabe = torch.tensor([[3.0, 0.5], [0.2, 1.8], [1.0, 1.1]])
richtig = torch.tensor([0, 1, 1])
print(torch.softmax(ausgabe, dim=1).round(decimals=3))
print(ausgabe.argmax(dim=1))
print(f'{nn.CrossEntropyLoss()(ausgabe, richtig).item():.4f}')""")
expl('''#### Das erste Netz trainieren

Die Halbmonde aus `make_moons` (500 Punkte) werden in Trainings- und Testdaten geteilt und in Tensoren umgewandelt. Die Funktionen `trainiere()` und `genauigkeit()`
fassen die Trainingsschleife aus Notebook 2 und das Auszählen der richtigen Vorhersagen zusammen; sie stehen in den Aufgaben schon in der Zelle.''',
     MONDE + TRAINING + """


torch.manual_seed(0)
modell = nn.Sequential(nn.Linear(2, 16), nn.ReLU(), nn.Linear(16, 2))
print(f'vorher: {genauigkeit(modell, X_test, y_test):.3f}')
verluste = trainiere(modell, X_train, y_train, 1000)
print(f'Verlust am Ende: {verluste[-1]:.4f}')
print(f'Training {genauigkeit(modell, X_train, y_train):.3f}, Test {genauigkeit(modell, X_test, y_test):.3f}')""")

t('''Berechne den Verlust `CrossEntropyLoss` für die Ausgaben in der Zelle einmal mit den richtigen Klassen `[0, 1]` und einmal mit den falschen `[1, 0]` (4 Nachkommastellen).
Je sicherer das Netz falsch liegt, desto größer der Verlust.''', NN + '\n\nausgabe = torch.tensor([[4.0, -1.0], [-2.0, 3.0]])',
  """verlustfunktion = nn.CrossEntropyLoss()
print(f'{verlustfunktion(ausgabe, torch.tensor([0, 1])).item():.4f}')
print(f'{verlustfunktion(ausgabe, torch.tensor([1, 0])).item():.4f}')""")
t('''Für ein Netz, das noch nichts weiß und für beide Klassen dieselbe Ausgabe liefert, ist der Verlust `ln(2)`. Prüfe das mit `ausgabe = torch.zeros(5, 2)`,
beliebigen Klassen und `torch.log(torch.tensor(2.0))` (4 Nachkommastellen).''', NN,
  """ausgabe = torch.zeros(5, 2)
richtig = torch.tensor([0, 1, 1, 0, 1])
print(f'{nn.CrossEntropyLoss()(ausgabe, richtig).item():.4f}')
print(f'{torch.log(torch.tensor(2.0)).item():.4f}')""")
t('''Trainiere das Netz aus dem Beispiel (Seed 0) nur 50, 200 und 1000 Epochen lang (jeweils neu) und gib Epochen und Test-Genauigkeit aus.
Die Genauigkeit sollte von etwa 0.84 auf etwa 0.93 steigen.''', MONDE + TRAINING,
  """

for epochen in [50, 200, 1000]:
    torch.manual_seed(0)
    modell = nn.Sequential(nn.Linear(2, 16), nn.ReLU(), nn.Linear(16, 2))
    trainiere(modell, X_train, y_train, epochen)
    print(epochen, f'{genauigkeit(modell, X_test, y_test):.3f}')""", kind='free')
t('''Vergleiche Netze mit 2, 8 und 64 Neuronen in der verborgenen Schicht (Seed 0, 1000 Epochen). Gib die Anzahl der Neuronen und die Genauigkeit auf Trainings- und Testdaten
aus. Die Test-Genauigkeit sollte von etwa 0.87 (2 Neuronen, fast gerade Grenze) auf etwa 0.91 (64 Neuronen) steigen.''', MONDE + TRAINING,
  """

for neuronen in [2, 8, 64]:
    torch.manual_seed(0)
    modell = nn.Sequential(nn.Linear(2, neuronen), nn.ReLU(), nn.Linear(neuronen, 2))
    trainiere(modell, X_train, y_train, 1000)
    print(neuronen, f'{genauigkeit(modell, X_train, y_train):.3f} {genauigkeit(modell, X_test, y_test):.3f}')""", kind='free')
t('''Ein Netz **ohne** Aktivierungsfunktion (`Linear(2, 16)`, `Linear(16, 2)`) ist nur eine lineare Grenze. Trainiere es (Seed 0, 1000 Epochen) und vergleiche die Test-Genauigkeit
mit dem Netz mit ReLU. Sie sollte deutlich kleiner sein (etwa 0.83 statt 0.93).''', MONDE + TRAINING,
  """

for name in ['ohne', 'mit ReLU']:
    torch.manual_seed(0)
    if name == 'ohne':
        modell = nn.Sequential(nn.Linear(2, 16), nn.Linear(16, 2))
    else:
        modell = nn.Sequential(nn.Linear(2, 16), nn.ReLU(), nn.Linear(16, 2))
    trainiere(modell, X_train, y_train, 1000)
    print(name, f'{genauigkeit(modell, X_test, y_test):.3f}')""", kind='free')
t('''Zeichne die Verlustkurve des Trainings aus dem Beispiel (1000 Epochen).''', MONDE + TRAINING + '\nimport matplotlib.pyplot as plt',
  """

torch.manual_seed(0)
modell = nn.Sequential(nn.Linear(2, 16), nn.ReLU(), nn.Linear(16, 2))
verluste = trainiere(modell, X_train, y_train, 1000)
plt.plot(verluste)
plt.xlabel('Epoche')
plt.ylabel('Verlust')
plt.show()""", kind='free')
t('''Zeichne die Entscheidungsgrenze des trainierten Netzes (Seed 0, 1000 Epochen): Erzeuge mit `torch.meshgrid(torch.linspace(-2, 3, 200), torch.linspace(-1.5, 2, 200),
indexing='xy')` ein Gitter `gx, gy`, lege die Punkte mit `torch.stack([gx.flatten(), gy.flatten()], dim=1)` zu einem Stapel zusammen, sage für alle die Klasse vorher und
zeichne sie mit `plt.contourf(gx, gy, klassen.reshape(gx.shape), alpha=0.3, cmap='coolwarm')`. Zeichne die Testpunkte darüber.''',
  MONDE + TRAINING + '\nimport matplotlib.pyplot as plt',
  """

torch.manual_seed(0)
modell = nn.Sequential(nn.Linear(2, 16), nn.ReLU(), nn.Linear(16, 2))
trainiere(modell, X_train, y_train, 1000)
gx, gy = torch.meshgrid(torch.linspace(-2, 3, 200), torch.linspace(-1.5, 2, 200), indexing='xy')
gitter = torch.stack([gx.flatten(), gy.flatten()], dim=1)
with torch.no_grad():
    klassen = modell(gitter).argmax(dim=1)
plt.contourf(gx, gy, klassen.reshape(gx.shape), alpha=0.3, cmap='coolwarm')
plt.scatter(X_test[:, 0], X_test[:, 1], c=y_test, cmap='coolwarm', s=10)
plt.show()""", kind='free')
predict("""import torch

ausgabe = torch.tensor([[0.1, 2.0, -1.0], [3.0, 0.0, 2.9]])
print(ausgabe.argmax(dim=1))
print(torch.softmax(torch.tensor([1.0, 1.0]), dim=0))""", erklaerung='''- In der ersten Zeile ist die zweite Ausgabe am größten (Klasse 1), in der zweiten die erste (3.0 > 2.9, Klasse 0): `tensor([1, 0])`.
- Gleiche Ausgaben ergeben gleiche Wahrscheinlichkeiten: `tensor([0.5000, 0.5000])`.''')

# ---------------------------------------------------------------- 3
sec('Eigene Netze mit nn.Module')
expl('''#### Ein Netz als Klasse

Größere Netze schreibt man als eigene **Klasse**, die von `nn.Module` erbt:

- Im Konstruktor ruft man zuerst `super().__init__()` auf und legt die Schichten als Attribute an.
- Die Methode `forward(self, x)` beschreibt, wie die Eingabe durch die Schichten fließt. Hier kann man auch rechnen, verzweigen oder Schichten mehrfach benutzen.
- Aufgerufen wird das Netz wie eine Funktion: `modell(x)` ruft `forward()` auf.

PyTorch findet alle Gewichte der Schichten automatisch, `modell.parameters()` funktioniert also wie bei `Sequential`.''',
     NN + """

class Netz(nn.Module):
    def __init__(self, eingaben, neuronen, klassen):
        super().__init__()
        self.schicht1 = nn.Linear(eingaben, neuronen)
        self.schicht2 = nn.Linear(neuronen, klassen)

    def forward(self, x):
        x = torch.relu(self.schicht1(x))
        return self.schicht2(x)


modell = Netz(2, 16, 2)
print(modell)
print(modell(torch.zeros(5, 2)).shape)
print(sum([p.numel() for p in modell.parameters()]))""")

t('''Schreibe eine Klasse `ZweiSchichten(nn.Module)` mit zwei verborgenen Schichten (Anzahl der Neuronen `n1` und `n2` als Parameter des Konstruktors, ReLU nach beiden),
2 Eingaben und 2 Ausgaben. Erzeuge `ZweiSchichten(32, 16)` und gib die Form der Ausgabe für 10 Eingaben und die Anzahl der Gewichte aus.''', NN,
  """

class ZweiSchichten(nn.Module):
    def __init__(self, n1, n2):
        super().__init__()
        self.a = nn.Linear(2, n1)
        self.b = nn.Linear(n1, n2)
        self.c = nn.Linear(n2, 2)

    def forward(self, x):
        x = torch.relu(self.a(x))
        x = torch.relu(self.b(x))
        return self.c(x)


modell = ZweiSchichten(32, 16)
print(modell(torch.rand(10, 2)).shape)
print(sum([p.numel() for p in modell.parameters()]))""")
t('''Ergänze die Klasse `Netz` aus dem Beispiel um eine Methode `vorhersage(self, x)`, die in `torch.no_grad()` die Klassen (`argmax`) zurückgibt. Setze die Gewichte
von Hand: Alle Gewichte von `schicht1` auf 1, ihre bias-Werte auf 0, die Gewichte von `schicht2` auf `[[1, ...], [-1, ...]]` (Zeile 0 lauter 1, Zeile 1 lauter −1),
bias `[0, 0.5]`. Dann sagt das Netz für Punkte mit deutlich positiver Summe Klasse 0 vorher, sonst Klasse 1. Teste mit `[[1, 2], [-3, -1]]`.''', NN,
  """

class Netz(nn.Module):
    def __init__(self, eingaben, neuronen, klassen):
        super().__init__()
        self.schicht1 = nn.Linear(eingaben, neuronen)
        self.schicht2 = nn.Linear(neuronen, klassen)

    def forward(self, x):
        x = torch.relu(self.schicht1(x))
        return self.schicht2(x)

    def vorhersage(self, x):
        with torch.no_grad():
            return self(x).argmax(dim=1)


modell = Netz(2, 4, 2)
with torch.no_grad():
    modell.schicht1.weight[:] = 1.0
    modell.schicht1.bias[:] = 0.0
    modell.schicht2.weight[0] = 1.0
    modell.schicht2.weight[1] = -1.0
    modell.schicht2.bias[:] = torch.tensor([0.0, 0.5])
print(modell.vorhersage(torch.tensor([[1.0, 2.0], [-3.0, -1.0]])))""")
t('''Schreibe eine Klasse `TiefesNetz(nn.Module)`, deren Konstruktor eine Liste von Schichtgrößen bekommt, z. B. `[2, 32, 32, 2]`, und daraus die `Linear`-Schichten in einer
`nn.ModuleList` anlegt (eine Liste, deren Gewichte PyTorch findet). `forward` wendet nach jeder Schicht außer der letzten ReLU an. Gib für `[2, 32, 32, 2]` und
`[2, 8, 8, 8, 2]` die Anzahl der Gewichte aus.''', NN,
  """

class TiefesNetz(nn.Module):
    def __init__(self, groessen):
        super().__init__()
        self.schichten = nn.ModuleList()
        for i in range(len(groessen) - 1):
            self.schichten.append(nn.Linear(groessen[i], groessen[i + 1]))

    def forward(self, x):
        for schicht in self.schichten[:-1]:
            x = torch.relu(schicht(x))
        return self.schichten[-1](x)


for groessen in [[2, 32, 32, 2], [2, 8, 8, 8, 2]]:
    modell = TiefesNetz(groessen)
    print(groessen, sum([p.numel() for p in modell.parameters()]))""")
t('''Trainiere `TiefesNetz([2, 32, 32, 2])` aus der vorigen Aufgabe (Seed 0, 1000 Epochen) auf den Halbmonden und gib die Test-Genauigkeit aus (etwa 0.91).''',
  MONDE + TRAINING + '''


class TiefesNetz(nn.Module):
    def __init__(self, groessen):
        super().__init__()
        self.schichten = nn.ModuleList()
        for i in range(len(groessen) - 1):
            self.schichten.append(nn.Linear(groessen[i], groessen[i + 1]))

    def forward(self, x):
        for schicht in self.schichten[:-1]:
            x = torch.relu(schicht(x))
        return self.schichten[-1](x)''',
  """

torch.manual_seed(0)
modell = TiefesNetz([2, 32, 32, 2])
trainiere(modell, X_train, y_train, 1000)
print(f'{genauigkeit(modell, X_test, y_test):.3f}')""", kind='free')
predict("""import torch
from torch import nn

class Verdoppler(nn.Module):
    def forward(self, x):
        return 2 * x + 1


modell = Verdoppler()
print(modell(torch.tensor([1.0, 5.0])))
print(len(list(modell.parameters())))""", erklaerung='''- `forward` rechnet `2x + 1`: `tensor([ 3., 11.])`.
- Das Modul hat keine Schichten und damit keine Gewichte: `0`. (Ohne eigenen Konstruktor wird der von `nn.Module` benutzt.)''')

# ---------------------------------------------------------------- 4
sec('Daten in Portionen: DataLoader')
expl('''#### Mini-Batches

Bei großen Datenmengen (Notebook 4: 60 000 Bilder) rechnet man nicht mit allen Daten auf einmal, sondern mit kleinen Portionen (**Mini-Batches**), z. B. 32 Beispiele.
Nach jeder Portion werden die Gewichte verbessert, in einer Epoche also viele Male. Das spart Speicher und führt oft schneller zum Ziel.

- `TensorDataset(X, y)` aus `torch.utils.data` verbindet Merkmale und Klassen: `datensatz[i]` ist das Paar `(X[i], y[i])`.
- `DataLoader(datensatz, batch_size=32, shuffle=True)` liefert in einer `for`-Schleife die Portionen. `shuffle=True` mischt die Reihenfolge in jeder Epoche neu.''',
     MONDE + """
from torch.utils.data import TensorDataset, DataLoader

datensatz = TensorDataset(X_train, y_train)
print(len(datensatz))
print(datensatz[0])
lader = DataLoader(datensatz, batch_size=32, shuffle=False)
print(len(lader))
for xb, yb in lader:
    print(xb.shape, yb.shape)
    break""")
expl('''#### Die Trainingsschleife mit Portionen

Die Schleife bekommt eine zweite Ebene: außen die Epochen, innen die Portionen.''',
     MONDE + """
from torch.utils.data import TensorDataset, DataLoader

torch.manual_seed(0)
lader = DataLoader(TensorDataset(X_train, y_train), batch_size=32, shuffle=True)
modell = nn.Sequential(nn.Linear(2, 16), nn.ReLU(), nn.Linear(16, 2))
verlustfunktion = nn.CrossEntropyLoss()
optimierer = torch.optim.Adam(modell.parameters(), lr=0.01)
for epoche in range(1, 101):
    for xb, yb in lader:
        verlust = verlustfunktion(modell(xb), yb)
        optimierer.zero_grad()
        verlust.backward()
        optimierer.step()
    if epoche % 25 == 0:
        with torch.no_grad():
            treffer = (modell(X_test).argmax(dim=1) == y_test).float().mean().item()
        print(epoche, f'{treffer:.3f}')""")

DL = MONDE + '\nfrom torch.utils.data import TensorDataset, DataLoader'
t('''Erzeuge einen `DataLoader` für die Trainingsdaten mit `batch_size=50` (ohne Mischen). Gib die Anzahl der Portionen und die Größe jeder Portion aus
(`len(yb)` in der Schleife). Die letzte ist kleiner.''', DL,
  """lader = DataLoader(TensorDataset(X_train, y_train), batch_size=50, shuffle=False)
print(len(lader))
for xb, yb in lader:
    print(len(yb), end=' ')
print()""")
t('''Wie oft werden die Gewichte in 20 Epochen verbessert, wenn die 350 Trainingsbeispiele in Portionen von 1, 32 und 350 verarbeitet werden? Gib die Portionsgröße und die
Anzahl der Schritte aus (`len(lader) * 20`).''', DL,
  """for groesse in [1, 32, 350]:
    lader = DataLoader(TensorDataset(X_train, y_train), batch_size=groesse)
    print(groesse, len(lader) * 20)""")
t('''Zeige, dass `shuffle=True` mischt: Gib mit Seed 1 die Klassen der ersten Portion (Größe 10) in zwei aufeinanderfolgenden Epochen aus. Ohne Mischen wären sie gleich.''', DL,
  """torch.manual_seed(1)
lader = DataLoader(TensorDataset(X_train, y_train), batch_size=10, shuffle=True)
for epoche in range(2):
    for xb, yb in lader:
        print(yb)
        break""", kind='free')
t('''Vergleiche Portionsgrößen: Trainiere das Netz aus dem Beispiel (Seed 0) mit `batch_size` 8, 32 und 350 jeweils 50 Epochen lang und gib Portionsgröße und Test-Genauigkeit aus.
Mit kleinen Portionen gibt es mehr Schritte pro Epoche, und das Netz ist nach 50 Epochen weiter (etwa 0.91 gegen etwa 0.84 bei 350).''', DL,
  """for groesse in [8, 32, 350]:
    torch.manual_seed(0)
    lader = DataLoader(TensorDataset(X_train, y_train), batch_size=groesse, shuffle=True)
    modell = nn.Sequential(nn.Linear(2, 16), nn.ReLU(), nn.Linear(16, 2))
    verlustfunktion = nn.CrossEntropyLoss()
    optimierer = torch.optim.Adam(modell.parameters(), lr=0.01)
    for epoche in range(50):
        for xb, yb in lader:
            verlust = verlustfunktion(modell(xb), yb)
            optimierer.zero_grad()
            verlust.backward()
            optimierer.step()
    with torch.no_grad():
        treffer = (modell(X_test).argmax(dim=1) == y_test).float().mean().item()
    print(groesse, f'{treffer:.3f}')""", kind='free')
predict("""import torch
from torch.utils.data import TensorDataset, DataLoader

X = torch.arange(10).float().unsqueeze(1)
y = torch.arange(10)
lader = DataLoader(TensorDataset(X, y), batch_size=4)
print(len(lader))
for xb, yb in lader:
    print(yb)""", erklaerung='''10 Beispiele in Portionen von 4 ergeben 3 Portionen (4, 4 und 2): `3`. Ohne `shuffle` bleibt die Reihenfolge:
`tensor([0, 1, 2, 3])`, `tensor([4, 5, 6, 7])`, `tensor([8, 9])`.''')

# ---------------------------------------------------------------- 5
sec('Überanpassung erkennen')
expl('''#### Trainings- und Testverlust

Wie in der scikit-learn-Reihe kann ein großes Netz die Trainingsdaten auswendig lernen. Man erkennt das, wenn man **während** des Trainings auch den Verlust
auf den Testdaten misst: Der Trainingsverlust sinkt immer weiter, der Testverlust steigt ab einem Punkt wieder. Dort hätte man aufhören sollen
(**early stopping**). Besonders leicht passiert das bei wenigen Daten, hier 40 verrauschten Trainingspunkten.

`modell.train()` und `modell.eval()` schalten das Netz in den Trainings- bzw. Auswertungsmodus. Bei den Netzen hier ändert das nichts; manche Schichten
(z. B. `nn.Dropout`) verhalten sich aber verschieden, deshalb gewöhnt man es sich an.''',
     '''import torch
from torch import nn
from sklearn.datasets import make_moons
import matplotlib.pyplot as plt

X, y = make_moons(n_samples=440, noise=0.35, random_state=1)
X = torch.tensor(X, dtype=torch.float32)
y = torch.tensor(y)
X_train, y_train, X_test, y_test = X[:40], y[:40], X[40:], y[40:]

torch.manual_seed(0)
modell = nn.Sequential(nn.Linear(2, 128), nn.ReLU(), nn.Linear(128, 128), nn.ReLU(), nn.Linear(128, 2))
verlustfunktion = nn.CrossEntropyLoss()
optimierer = torch.optim.Adam(modell.parameters(), lr=0.01)
training, test = [], []
for epoche in range(1000):
    modell.train()
    verlust = verlustfunktion(modell(X_train), y_train)
    optimierer.zero_grad()
    verlust.backward()
    optimierer.step()
    modell.eval()
    with torch.no_grad():
        training.append(verlust.item())
        test.append(verlustfunktion(modell(X_test), y_test).item())
plt.plot(training, label='Training')
plt.plot(test, label='Test')
plt.ylim(0, 1.5)
plt.legend()
plt.show()''')

UEBER = '''import torch
from torch import nn
from sklearn.datasets import make_moons

X, y = make_moons(n_samples=440, noise=0.35, random_state=1)
X = torch.tensor(X, dtype=torch.float32)
y = torch.tensor(y)
X_train, y_train, X_test, y_test = X[:40], y[:40], X[40:], y[40:]'''
t('''Trainiere das große Netz aus dem Beispiel (Seed 0) und gib nach 50, 200 und 1000 Epochen die Genauigkeit auf Trainings- und Testdaten aus. Die Trainingsgenauigkeit
ist schon nach 50 Epochen 1.0, die Testgenauigkeit kommt nicht über etwa 0.84 hinaus: Das Netz hat die 40 Punkte auswendig gelernt.''', UEBER,
  """torch.manual_seed(0)
modell = nn.Sequential(nn.Linear(2, 128), nn.ReLU(), nn.Linear(128, 128), nn.ReLU(), nn.Linear(128, 2))
verlustfunktion = nn.CrossEntropyLoss()
optimierer = torch.optim.Adam(modell.parameters(), lr=0.01)
for epoche in range(1, 1001):
    verlust = verlustfunktion(modell(X_train), y_train)
    optimierer.zero_grad()
    verlust.backward()
    optimierer.step()
    if epoche in [50, 200, 1000]:
        with torch.no_grad():
            a = (modell(X_train).argmax(dim=1) == y_train).float().mean().item()
            b = (modell(X_test).argmax(dim=1) == y_test).float().mean().item()
        print(epoche, f'{a:.3f} {b:.3f}')""", kind='free')
t('''**Early stopping:** Trainiere das große Netz 1000 Epochen und merke dir die Epoche mit dem kleinsten Testverlust. Gib sie und den kleinsten Testverlust aus.
Das beste Ergebnis kommt schon nach wenigen Epochen (etwa Epoche 5, Testverlust etwa 0.37).''', UEBER,
  """torch.manual_seed(0)
modell = nn.Sequential(nn.Linear(2, 128), nn.ReLU(), nn.Linear(128, 128), nn.ReLU(), nn.Linear(128, 2))
verlustfunktion = nn.CrossEntropyLoss()
optimierer = torch.optim.Adam(modell.parameters(), lr=0.01)
beste_epoche, bester = 0, 100.0
for epoche in range(1, 1001):
    verlust = verlustfunktion(modell(X_train), y_train)
    optimierer.zero_grad()
    verlust.backward()
    optimierer.step()
    with torch.no_grad():
        testverlust = verlustfunktion(modell(X_test), y_test).item()
    if testverlust < bester:
        beste_epoche, bester = epoche, testverlust
print(beste_epoche, f'{bester:.4f}')""", kind='free')
t('''Gegen Überanpassung hilft **weight decay**: `torch.optim.Adam(..., weight_decay=0.01)` zieht die Gewichte bei jedem Schritt etwas zu 0, das Netz bleibt einfacher.
Vergleiche den Testverlust nach 1000 Epochen ohne und mit `weight_decay=0.01` (Seed 0). Er sollte mit weight decay deutlich kleiner sein (etwa 0.37 statt 3.4).''', UEBER,
  """for decay in [0.0, 0.01]:
    torch.manual_seed(0)
    modell = nn.Sequential(nn.Linear(2, 128), nn.ReLU(), nn.Linear(128, 128), nn.ReLU(), nn.Linear(128, 2))
    verlustfunktion = nn.CrossEntropyLoss()
    optimierer = torch.optim.Adam(modell.parameters(), lr=0.01, weight_decay=decay)
    for epoche in range(1000):
        verlust = verlustfunktion(modell(X_train), y_train)
        optimierer.zero_grad()
        verlust.backward()
        optimierer.step()
    with torch.no_grad():
        print(decay, f'{verlustfunktion(modell(X_test), y_test).item():.4f}')""", kind='free')

# ---------------------------------------------------------------- 6
sec('Gemischte Übungen')
t('''Klassifiziere die Iris-Daten (`load_iris()` aus scikit-learn, 4 Merkmale, 3 Arten) mit einem Netz `Linear(4, 16)`, ReLU, `Linear(16, 3)`. Skaliere die Merkmale vorher
mit `StandardScaler` (an den Trainingsdaten eingestellt), teile mit `train_test_split(..., test_size=0.3, random_state=0, stratify=daten.target)` auf und trainiere 300 Epochen
(Seed 0, Adam, Lernrate 0.01). Die Test-Genauigkeit sollte nahe bei 1 liegen.''',
  '''import torch
from torch import nn
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

daten = load_iris()''',
  """X_train, X_test, y_train, y_test = train_test_split(daten.data, daten.target, test_size=0.3, random_state=0, stratify=daten.target)
scaler = StandardScaler()
X_train = torch.tensor(scaler.fit_transform(X_train), dtype=torch.float32)
X_test = torch.tensor(scaler.transform(X_test), dtype=torch.float32)
y_train = torch.tensor(y_train)
y_test = torch.tensor(y_test)
torch.manual_seed(0)
modell = nn.Sequential(nn.Linear(4, 16), nn.ReLU(), nn.Linear(16, 3))
verlustfunktion = nn.CrossEntropyLoss()
optimierer = torch.optim.Adam(modell.parameters(), lr=0.01)
for epoche in range(300):
    verlust = verlustfunktion(modell(X_train), y_train)
    optimierer.zero_grad()
    verlust.backward()
    optimierer.step()
with torch.no_grad():
    print(f'{(modell(X_test).argmax(dim=1) == y_test).float().mean().item():.3f}')""", kind='free')
t('''Ein Netz für Zahlen (Regression): Lerne die Funktion `y = sin(x)` für x von −3 bis 3 aus 200 Punkten mit etwas Rauschen (Seed 0, `torch.randn(200, 1) * 0.1`). Das Netz hat
1 Eingabe, zwei verborgene Schichten mit 32 Neuronen (Tanh) und 1 Ausgabe, die Verlustfunktion ist `nn.MSELoss()` (Adam, Lernrate 0.01, 1000 Epochen). Zeichne die Punkte
und die gelernte Kurve.''', NN + '\nimport matplotlib.pyplot as plt',
  """torch.manual_seed(0)
x = torch.linspace(-3, 3, 200).unsqueeze(1)
y = torch.sin(x) + torch.randn(200, 1) * 0.1
modell = nn.Sequential(nn.Linear(1, 32), nn.Tanh(), nn.Linear(32, 32), nn.Tanh(), nn.Linear(32, 1))
verlustfunktion = nn.MSELoss()
optimierer = torch.optim.Adam(modell.parameters(), lr=0.01)
for epoche in range(1000):
    verlust = verlustfunktion(modell(x), y)
    optimierer.zero_grad()
    verlust.backward()
    optimierer.step()
with torch.no_grad():
    kurve = modell(x)
plt.scatter(x, y, s=5, color='gray')
plt.plot(x, kurve, color='red')
plt.show()""", kind='free')
t('''Vergleiche mit scikit-learn: Trainiere auf den Halbmond-Daten (aus der Zelle) `MLPClassifier(hidden_layer_sizes=(16,), max_iter=2000, learning_rate_init=0.01,
random_state=0)` und gib seine Test-Genauigkeit aus. Sie sollte ähnlich sein wie die deines PyTorch-Netzes (etwa 0.92).''',
  '''from sklearn.datasets import make_moons
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier

X, y = make_moons(n_samples=500, noise=0.25, random_state=0)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=0)''',
  """modell = MLPClassifier(hidden_layer_sizes=(16,), max_iter=2000, learning_rate_init=0.01, random_state=0)
modell.fit(X_train, y_train)
print(f'{modell.score(X_test, y_test):.3f}')""", kind='free')

generate('pytorch_netze', 'PyTorch 3: Netze', INTRO, ordner='extern')
