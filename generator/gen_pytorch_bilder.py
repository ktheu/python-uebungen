# Erzeugt ../extern/pytorch_bilder.ipynb (siehe nbgen.py). Viertes Notebook der PyTorch-Reihe:
# pytorch_tensoren, pytorch_lernen, pytorch_netze, pytorch_bilder.
#
# Läuft nicht in JupyterLite, sondern in Google Colab. Lokal in der py-3.13-venv p313torch (PyTorch für die CPU).
# Braucht beim Erzeugen Internet: Die Setup-Zelle lädt MNIST (ca. 12 MB, mit Fortschrittsanzeige) in den Ordner daten/,
# alle anderen Zellen finden die Dateien dort (keine Fortschrittsanzeige in erwarteten Ausgaben).
# Training nur mit 10 000 Trainingsbildern (Subset), damit der Generator auf der CPU schnell bleibt; Training ist kind='free'.
# Erwartete Ausgaben nur für Daten (Anzahlen, Formen, Ziffern) und Aufbau der Netze. Diagramme nur bei kind='free'.
from nbgen import sec, generate, setup
from torchhilfe import t, expl, predict, reihe, COLAB, SCHLUSS

INTRO = '''Im letzten Notebook der Reihe erkennt ein Netz **handgeschriebene Ziffern** aus dem berühmten Datensatz **MNIST**: 70 000 Bilder mit 28 × 28 Pixeln.
Zuerst mit einem Netz aus voll verbundenen Schichten wie in Notebook 3, dann mit einem **Faltungsnetz** (*convolutional neural network*, CNN),
der Art von Netz, mit der Bilderkennung in der Praxis arbeitet. Zum Schluss trainierst du auf der Grafikkarte und überträgst alles auf Bilder von Kleidungsstücken.

''' + reihe(4) + '''

Vorausgesetzt wird *PyTorch: Netze* (Trainingsschleife, `DataLoader`).

''' + COLAB + '''

''' + SCHLUSS

setup('''#### MNIST herunterladen

**Führe diese Zelle zuerst aus.** Sie lädt die MNIST-Daten (etwa 12 MB) in den Ordner `daten` herunter. In Colab bleiben sie dort, bis die Sitzung endet;
danach lädt die Zelle sie neu.''',
      """from torchvision import datasets

datasets.MNIST(root='daten', train=True, download=True)
datasets.MNIST(root='daten', train=False, download=True)
print('MNIST ist bereit.')""")

DATEN = '''import torch
from torch import nn
from torchvision import datasets, transforms

training = datasets.MNIST(root='daten', train=True, download=True, transform=transforms.ToTensor())
test = datasets.MNIST(root='daten', train=False, download=True, transform=transforms.ToTensor())'''
HILFE = '''
from torch.utils.data import DataLoader, Subset

device = 'cuda' if torch.cuda.is_available() else 'cpu'
torch.manual_seed(0)
lader = DataLoader(Subset(training, range(10000)), batch_size=64, shuffle=True)   # 10 000 Bilder, damit es schnell geht
testlader = DataLoader(test, batch_size=1000)


def trainiere(modell, lader, epochen):
    modell.to(device)
    verlustfunktion = nn.CrossEntropyLoss()
    optimierer = torch.optim.Adam(modell.parameters(), lr=0.001)
    for epoche in range(epochen):
        modell.train()
        for xb, yb in lader:
            xb, yb = xb.to(device), yb.to(device)
            verlust = verlustfunktion(modell(xb), yb)
            optimierer.zero_grad()
            verlust.backward()
            optimierer.step()


def genauigkeit(modell, lader):
    modell.eval()
    richtig = 0
    with torch.no_grad():
        for xb, yb in lader:
            xb, yb = xb.to(device), yb.to(device)
            richtig += (modell(xb).argmax(dim=1) == yb).sum().item()
    return richtig / len(lader.dataset)'''
CNN = '''nn.Sequential(nn.Conv2d(1, 16, 3, padding=1), nn.ReLU(), nn.MaxPool2d(2),
                       nn.Conv2d(16, 32, 3, padding=1), nn.ReLU(), nn.MaxPool2d(2),
                       nn.Flatten(), nn.Linear(32 * 7 * 7, 10))'''
FC = 'nn.Sequential(nn.Flatten(), nn.Linear(28 * 28, 128), nn.ReLU(), nn.Linear(128, 10))'

# ---------------------------------------------------------------- 1
sec('Die MNIST-Daten')
expl('''#### Bilder als Tensoren

`datasets.MNIST(root='daten', train=True, transform=transforms.ToTensor())` aus dem Paket `torchvision` sind die 60 000 **Trainingsbilder**, mit `train=False`
die 10 000 **Testbilder**. `transforms.ToTensor()` macht aus jedem Bild einen Tensor mit Helligkeiten von 0 (schwarz) bis 1 (weiß).

- `len(training)` ist die Anzahl der Bilder, `training[i]` das Paar `(bild, ziffer)`.
- Ein Bild hat die Form `[1, 28, 28]`: 1 **Kanal** (Graustufen; Farbbilder hätten 3 Kanäle für Rot, Grün, Blau) mit 28 × 28 Pixeln.
- `training.targets` enthält alle Ziffern als Tensor.''',
     DATEN + """

print(len(training), len(test))
bild, ziffer = training[0]
print(bild.shape, bild.dtype, ziffer)
print(f'{bild.min().item():.1f} {bild.max().item():.1f}')
print(training.targets[:10])""")
expl('''#### Bilder anzeigen

`plt.imshow(bild[0].numpy(), cmap='gray')` zeigt den einen Kanal eines Bilds an (`bild[0]` hat die Form `[28, 28]`). Wie in Notebook 1 wird der Tensor
für matplotlib vorher mit `.numpy()` in ein numpy-Array umgewandelt.''',
     DATEN + """
import matplotlib.pyplot as plt

plt.figure(figsize=(10, 2))
for i in range(10):
    bild, ziffer = training[i]
    plt.subplot(1, 10, i + 1)
    plt.imshow(bild[0].numpy(), cmap='gray')
    plt.title(ziffer)
    plt.axis('off')
plt.show()""")

t('Gib für das Testbild mit Index 0 die Ziffer, die Form des Bilds und die mittlere Helligkeit aus (4 Nachkommastellen).', DATEN,
  """bild, ziffer = test[0]
print(ziffer)
print(bild.shape)
print(f'{bild.mean().item():.4f}')""")
t('Wie oft kommt jede Ziffer in den Trainingsdaten vor? Gib `torch.bincount(training.targets)` aus.', DATEN, "print(torch.bincount(training.targets))")
t('Gib die Ziffern der Trainingsbilder 100 bis 119 aus und die Indizes der ersten fünf Trainingsbilder, die eine 7 zeigen (`torch.where(training.targets == 7)[0][:5]`).', DATEN,
  """print(training.targets[100:120])
print(torch.where(training.targets == 7)[0][:5])""")
t('''Wie viele Pixel des ersten Trainingsbilds sind „Tinte“ (Helligkeit größer als 0.5)? Und welcher Anteil der Fläche ist das (3 Nachkommastellen)?''', DATEN,
  """bild, ziffer = training[0]
tinte = (bild > 0.5).sum().item()
print(tinte)
print(f'{tinte / bild.numel():.3f}')""")
t('''Zeige die ersten 8 Testbilder, die eine 3 zeigen, nebeneinander an.''', DATEN + '\nimport matplotlib.pyplot as plt',
  """indizes = torch.where(test.targets == 3)[0][:8]
for nr, i in enumerate(indizes):
    plt.subplot(1, 8, nr + 1)
    plt.imshow(test[i.item()][0][0].numpy(), cmap='gray')
    plt.axis('off')
plt.show()""", kind='free')
t('''Berechne das „mittlere Bild“ jeder Ziffer aus den ersten 10 000 Trainingsbildern und zeige die zehn Bilder nebeneinander an. Die Bilder als Tensor `[60000, 28, 28]`
mit Werten von 0 bis 255 erhältst du mit `training.data`; teile durch 255.''', DATEN + '\nimport matplotlib.pyplot as plt',
  """bilder = training.data[:10000].float() / 255
ziffern = training.targets[:10000]
plt.figure(figsize=(10, 2))
for z in range(10):
    plt.subplot(1, 10, z + 1)
    plt.imshow(bilder[ziffern == z].mean(dim=0).numpy(), cmap='gray')
    plt.title(z)
    plt.axis('off')
plt.show()""", kind='free')
predict("""import torch

bilder = torch.zeros(64, 1, 28, 28)
print(bilder.shape[0])
print(bilder.flatten(start_dim=1).shape)
print(bilder[0][0].shape)""", erklaerung='''- Ein Stapel aus 64 Bildern: Die erste Dimension ist die Anzahl, `64`.
- `flatten(start_dim=1)` lässt die erste Dimension stehen und macht aus jedem Bild 784 Zahlen: `torch.Size([64, 784])`.
- `bilder[0]` ist ein Bild `[1, 28, 28]`, `bilder[0][0]` sein einziger Kanal: `torch.Size([28, 28])`.''')

# ---------------------------------------------------------------- 2
sec('Ein voll verbundenes Netz')
expl('''#### 784 Eingaben

Ein Netz aus `Linear`-Schichten braucht Vektoren: `nn.Flatten()` macht aus jedem Bild `[1, 28, 28]` einen Vektor mit 784 Zahlen. Danach folgen eine verborgene Schicht
und 10 Ausgaben, eine pro Ziffer. Jedes Neuron der ersten Schicht ist mit **allen** 784 Pixeln verbunden (**voll verbunden**).

Die Daten kommen über einen `DataLoader` in Portionen von 64 Bildern. Damit es auch ohne Grafikkarte schnell geht, wird hier nur mit den ersten 10 000 Trainingsbildern
trainiert (`Subset(training, range(10000))`). Die Funktionen `trainiere()` und `genauigkeit()` stehen in den Aufgaben schon in der Zelle; sie schieben die Daten auch
auf die Grafikkarte, falls es eine gibt (Abschnitt 5).''',
     DATEN + HILFE + f"""


modell = {FC}
print(modell)
print(sum([p.numel() for p in modell.parameters()]))
xb, yb = next(iter(lader))
print(xb.shape, modell(xb).shape)
trainiere(modell, lader, 2)
print(f'Test-Genauigkeit: {{genauigkeit(modell, testlader):.3f}}')""")

t('''Rechne die Anzahl der Gewichte des Netzes `Flatten`, `Linear(784, 128)`, `ReLU`, `Linear(128, 10)` von Hand aus und vergleiche mit PyTorch.''', DATEN,
  f"""print(784 * 128 + 128 + 128 * 10 + 10)
modell = {FC}
print(sum([p.numel() for p in modell.parameters()]))""")
t('''Hole mit `next(iter(testlader))` die erste Portion aus den Testdaten (in der Zelle: Portionen zu 1000 Bildern) und gib die Formen der Bilder und der Ziffern
und die Form der Ausgabe eines (untrainierten) Netzes aus.''', DATEN + HILFE,
  f"""

xb, yb = next(iter(testlader))
print(xb.shape, yb.shape)
modell = {FC}
print(modell(xb).shape)""")
t('''Ein untrainiertes Netz rät. Gib seine Genauigkeit auf den Testdaten aus (Seed 1). Sie sollte etwa 0.1 sein (eine von zehn Ziffern).''', DATEN + HILFE,
  f"""

torch.manual_seed(1)
modell = {FC}
print(f'{{genauigkeit(modell, testlader):.3f}}')""", kind='free')
t('''Trainiere das Netz aus dem Beispiel 1, 3 und 5 Epochen lang (jeweils neu, Seed 0) und gib die Epochen und die Test-Genauigkeit aus. Sie sollte von etwa 0.90 auf etwa 0.93 steigen.''',
  DATEN + HILFE,
  f"""

for epochen in [1, 3, 5]:
    torch.manual_seed(0)
    modell = {FC}
    trainiere(modell, lader, epochen)
    print(epochen, f'{{genauigkeit(modell, testlader):.3f}}')""", kind='free')
t('''Trainiere das Netz aus dem Beispiel (Seed 0, 2 Epochen) und zeige die ersten 10 Testbilder mit der Vorhersage als Titel an. Die Vorhersage für ein einzelnes Bild bekommst du
mit `modell(bild.unsqueeze(0).to(device)).argmax().item()` (das Bild braucht eine Stapel-Dimension).''', DATEN + HILFE + '\nimport matplotlib.pyplot as plt',
  f"""

torch.manual_seed(0)
modell = {FC}
trainiere(modell, lader, 2)
modell.eval()
plt.figure(figsize=(10, 2))
for i in range(10):
    bild, ziffer = test[i]
    with torch.no_grad():
        vorhersage = modell(bild.unsqueeze(0).to(device)).argmax().item()
    plt.subplot(1, 10, i + 1)
    plt.imshow(bild[0].numpy(), cmap='gray')
    plt.title(vorhersage)
    plt.axis('off')
plt.show()""", kind='free')
predict(f"""import torch
from torch import nn

modell = {FC}
print(modell(torch.zeros(5, 1, 28, 28)).shape)
print(len(modell))""", erklaerung='''- 5 Bilder rein, für jedes 10 Ausgaben: `torch.Size([5, 10])`.
- Das Netz besteht aus 4 Schichten: `Flatten`, `Linear`, `ReLU`, `Linear`: `4`.''')

# ---------------------------------------------------------------- 3
sec('Faltungsnetze')
expl('''#### Filter, die über das Bild gleiten

Ein voll verbundenes Netz weiß nicht, welche Pixel nebeneinanderliegen. Ein **Faltungsnetz** nutzt das aus: Ein kleiner **Filter** (z. B. 3 × 3 Gewichte) gleitet über das Bild.
An jeder Stelle wird die gewichtete Summe der 3 × 3 Pixel darunter berechnet. So entsteht ein neues Bild (eine **Merkmalskarte**), das zeigt, wo das Muster des Filters
vorkommt, z. B. senkrechte Kanten. Die Gewichte der Filter lernt das Netz selbst.

Das Beispiel zeigt einen von Hand gewählten Filter für senkrechte Kanten: links negative, rechts positive Gewichte. `F.conv2d(bilder, filter, padding=1)` aus
`torch.nn.functional` wendet ihn an (`padding=1` ergänzt einen Rand aus Nullen, damit das Bild 28 × 28 bleibt).''',
     DATEN + """
import torch.nn.functional as F
import matplotlib.pyplot as plt

bild, ziffer = training[0]
filter = torch.tensor([[[[-1.0, 0.0, 1.0],
                         [-1.0, 0.0, 1.0],
                         [-1.0, 0.0, 1.0]]]])     # Form [1, 1, 3, 3]: 1 Filter, 1 Kanal
karte = F.conv2d(bild.unsqueeze(0), filter, padding=1)
print(karte.shape)
plt.subplot(1, 2, 1)
plt.imshow(bild[0].numpy(), cmap='gray')
plt.subplot(1, 2, 2)
plt.imshow(karte[0, 0].numpy(), cmap='bwr')
plt.show()""")
expl('''#### `Conv2d` und `MaxPool2d`

- `nn.Conv2d(1, 16, 3, padding=1)`: aus 1 Eingabekanal werden 16 Merkmalskarten, jede mit einem eigenen gelernten 3 × 3-Filter.
- `nn.MaxPool2d(2)` halbiert Breite und Höhe: Von je 2 × 2 Pixeln bleibt der größte Wert. Das macht das Netz unempfindlicher gegen kleine Verschiebungen.

Das Netz unten verkleinert das Bild so von 28 × 28 auf 14 × 14 und dann 7 × 7 mit 32 Merkmalskarten. Diese 32 · 7 · 7 = 1568 Zahlen gehen in eine `Linear`-Schicht mit
10 Ausgaben. Faltungsnetze brauchen viel weniger Gewichte als voll verbundene und sind trotzdem besser.''',
     DATEN + HILFE + f"""


modell = {CNN}
x = torch.zeros(1, 1, 28, 28)
for schicht in modell:
    x = schicht(x)
    print(type(schicht).__name__, list(x.shape))
print(sum([p.numel() for p in modell.parameters()]))
torch.manual_seed(0)
modell = {CNN}
trainiere(modell, lader, 2)
print(f'Test-Genauigkeit: {{genauigkeit(modell, testlader):.3f}}')""")

t('''Gib die Form der Ausgabe von `nn.Conv2d(1, 8, 3)` (ohne `padding`) und von `nn.Conv2d(1, 8, 3, padding=1)` für ein Bild `torch.zeros(1, 1, 28, 28)` aus. Ohne Rand
wird das Bild an jeder Seite um ein Pixel kleiner.''', 'import torch\nfrom torch import nn',
  """x = torch.zeros(1, 1, 28, 28)
print(nn.Conv2d(1, 8, 3)(x).shape)
print(nn.Conv2d(1, 8, 3, padding=1)(x).shape)""")
t('''Wie viele Gewichte hat `nn.Conv2d(1, 16, 3)`? Jeder der 16 Filter hat 3 · 3 Gewichte und einen bias-Wert. Rechne es aus und vergleiche mit PyTorch. Wie viele
hat `nn.Conv2d(16, 32, 3)` (jeder Filter hat jetzt 16 · 3 · 3 Gewichte)?''', 'import torch\nfrom torch import nn',
  """print(16 * 3 * 3 + 16, sum([p.numel() for p in nn.Conv2d(1, 16, 3).parameters()]))
print(32 * 16 * 3 * 3 + 32, sum([p.numel() for p in nn.Conv2d(16, 32, 3).parameters()]))""")
t('''Wende `nn.MaxPool2d(2)` auf die 4 × 4-Matrix `m` an (als Tensor der Form `[1, 1, 4, 4]`) und gib das Ergebnis aus. Von jedem 2 × 2-Block bleibt das Maximum.''',
  'import torch\nfrom torch import nn\n\nm = torch.tensor([[1.0, 3.0, 2.0, 0.0], [4.0, 2.0, 1.0, 1.0], [0.0, 1.0, 5.0, 6.0], [2.0, 2.0, 7.0, 3.0]])',
  "print(nn.MaxPool2d(2)(m.reshape(1, 1, 4, 4)))")
t('''Wende den Kantenfilter aus dem Beispiel von Hand auf das kleine Bild `b` an (`F.conv2d` ohne `padding`). Das Bild ist links dunkel und rechts hell; der Filter findet
die Kante in der Mitte.''',
  'import torch\nimport torch.nn.functional as F\n\nb = torch.tensor([[0.0, 0.0, 1.0, 1.0], [0.0, 0.0, 1.0, 1.0], [0.0, 0.0, 1.0, 1.0]]).reshape(1, 1, 3, 4)\nfilter = torch.tensor([[[[-1.0, 0.0, 1.0], [-1.0, 0.0, 1.0], [-1.0, 0.0, 1.0]]]])',
  "print(F.conv2d(b, filter))")
t('''Ändere den Filter aus dem Beispiel so, dass er **waagerechte** Kanten findet (oben −1, unten 1), und zeige das erste Trainingsbild und die Merkmalskarte nebeneinander.''',
  DATEN + '\nimport torch.nn.functional as F\nimport matplotlib.pyplot as plt',
  """bild, ziffer = training[0]
filter = torch.tensor([[[[-1.0, -1.0, -1.0],
                         [0.0, 0.0, 0.0],
                         [1.0, 1.0, 1.0]]]])
karte = F.conv2d(bild.unsqueeze(0), filter, padding=1)
plt.subplot(1, 2, 1)
plt.imshow(bild[0].numpy(), cmap='gray')
plt.subplot(1, 2, 2)
plt.imshow(karte[0, 0].numpy(), cmap='bwr')
plt.show()""", kind='free')
t('''Vergleiche die Anzahl der Gewichte des voll verbundenen Netzes und des Faltungsnetzes aus den Beispielen und trainiere beide (Seed 0, 2 Epochen). Gib für jedes den Namen,
die Anzahl der Gewichte und die Test-Genauigkeit aus. Das Faltungsnetz hat nur etwa ein Fünftel der Gewichte und ist besser (etwa 0.95 gegen 0.91).''', DATEN + HILFE,
  f"""

for name in ['voll verbunden', 'Faltung']:
    torch.manual_seed(0)
    if name == 'Faltung':
        modell = {CNN}
    else:
        modell = {FC}
    trainiere(modell, lader, 2)
    print(name, sum([p.numel() for p in modell.parameters()]), f'{{genauigkeit(modell, testlader):.3f}}')""", kind='free')
t('''Zeige die 16 gelernten Filter der ersten Schicht des trainierten Faltungsnetzes (Seed 0, 2 Epochen) als kleine Bilder an: `modell[0].weight` hat die Form `[16, 1, 3, 3]`,
`modell[0].weight[i, 0].detach().cpu()` ist der Filter `i`.''', DATEN + HILFE + '\nimport matplotlib.pyplot as plt',
  f"""

torch.manual_seed(0)
modell = {CNN}
trainiere(modell, lader, 2)
filter = modell[0].weight.detach().cpu()
plt.figure(figsize=(8, 2))
for i in range(16):
    plt.subplot(2, 8, i + 1)
    plt.imshow(filter[i, 0].numpy(), cmap='bwr')
    plt.axis('off')
plt.show()""", kind='free')
predict("""import torch
from torch import nn

x = torch.zeros(10, 3, 32, 32)
print(nn.Conv2d(3, 6, 5)(x).shape)
print(nn.MaxPool2d(2)(x).shape)""", erklaerung='''- 10 Farbbilder (3 Kanäle) mit 32 × 32 Pixeln. Ein 5 × 5-Filter ohne Rand macht das Bild an jeder Seite 2 Pixel kleiner: 32 − 4 = 28.
  Aus 3 Kanälen werden 6 Merkmalskarten: `torch.Size([10, 6, 28, 28])`.
- MaxPool halbiert Breite und Höhe, die Kanäle bleiben: `torch.Size([10, 3, 16, 16])`.''')

# ---------------------------------------------------------------- 4
sec('Fehler ansehen, speichern und laden')
expl('''#### Ein Modell speichern

Das Training dauert; danach will man das Netz behalten. `modell.state_dict()` enthält alle Gewichte, `torch.save(modell.state_dict(), 'ziffern.pt')` speichert sie in einer Datei.
Zum Laden erzeugt man ein Netz mit **demselben Aufbau** und lädt die Gewichte mit `modell.load_state_dict(torch.load('ziffern.pt'))`.

In Colab liegt die Datei im Ordner der Sitzung (links das Ordner-Symbol); dort kann man sie auch herunterladen.''',
     DATEN + HILFE + f"""


torch.manual_seed(0)
modell = {CNN}
trainiere(modell, lader, 1)
torch.save(modell.state_dict(), 'ziffern.pt')

neues_modell = {CNN}
neues_modell.load_state_dict(torch.load('ziffern.pt'))
print(f'{{genauigkeit(modell, testlader):.3f}} {{genauigkeit(neues_modell.to(device), testlader):.3f}}')""")

t('''Gib die Namen und Formen aller Einträge im `state_dict()` des Faltungsnetzes aus (`for name, w in modell.state_dict().items()`). Die Namen bestehen aus der Nummer der
Schicht und `weight` bzw. `bias`.''', 'import torch\nfrom torch import nn',
  f"""modell = {CNN}
for name, w in modell.state_dict().items():
    print(name, list(w.shape))""")
t('''Trainiere das Faltungsnetz (Seed 0, 2 Epochen) und zeige die ersten 10 Testbilder an, die es falsch erkennt, mit dem Titel `richtig→vorhergesagt`.''',
  DATEN + HILFE + '\nimport matplotlib.pyplot as plt',
  f"""

torch.manual_seed(0)
modell = {CNN}
trainiere(modell, lader, 2)
modell.eval()
xb, yb = next(iter(testlader))
with torch.no_grad():
    vorhersage = modell(xb.to(device)).argmax(dim=1).cpu()
falsch = torch.where(vorhersage != yb)[0][:10]
plt.figure(figsize=(10, 2))
for nr, i in enumerate(falsch):
    plt.subplot(1, 10, nr + 1)
    plt.imshow(xb[i, 0].numpy(), cmap='gray')
    plt.title(f'{{yb[i].item()}}→{{vorhersage[i].item()}}')
    plt.axis('off')
plt.show()""", kind='free')
t('''Welche Ziffern erkennt das Faltungsnetz (Seed 0, 2 Epochen) am schlechtesten? Berechne für jede Ziffer den Anteil der richtig erkannten Testbilder dieser Ziffer
(3 Nachkommastellen). Sammle dafür alle Vorhersagen der Testdaten mit `torch.cat()`.''', DATEN + HILFE,
  f"""

torch.manual_seed(0)
modell = {CNN}
trainiere(modell, lader, 2)
modell.eval()
vorhersagen = []
with torch.no_grad():
    for xb, yb in testlader:
        vorhersagen.append(modell(xb.to(device)).argmax(dim=1).cpu())
vorhersagen = torch.cat(vorhersagen)
for z in range(10):
    auswahl = test.targets == z
    print(z, f'{{(vorhersagen[auswahl] == z).float().mean().item():.3f}}')""", kind='free')
t('''Zeichne selbst eine Ziffer: Erzeuge ein Bild `torch.zeros(28, 28)` und setze Bereiche mit Slicing auf 1, z. B. für eine 1 die Spalten 13 bis 15 in den Zeilen 5 bis 23.
Lass das gespeicherte Netz aus dem Beispiel (`ziffern.pt`, vorher das Beispiel ausführen) die Ziffer erkennen und gib die drei wahrscheinlichsten Ziffern mit
`torch.softmax` und `topk(3)` aus.''', 'import torch\nfrom torch import nn\nimport matplotlib.pyplot as plt',
  f"""modell = {CNN}
modell.load_state_dict(torch.load('ziffern.pt'))
modell.eval()
bild = torch.zeros(28, 28)
bild[5:23, 13:16] = 1.0
with torch.no_grad():
    p = torch.softmax(modell(bild.reshape(1, 1, 28, 28)), dim=1)[0]
werte, ziffern = p.topk(3)
for w, z in zip(werte, ziffern):
    print(z.item(), f'{{w.item():.3f}}')
plt.imshow(bild.numpy(), cmap='gray')
plt.show()""", kind='free')

# ---------------------------------------------------------------- 5
sec('Mehr Rechenleistung: die Grafikkarte')
expl('''#### Alle 60 000 Bilder

Mit der Grafikkarte lohnt es sich, mit **allen** Trainingsbildern und mehr Epochen zu trainieren. Stelle in Colab den Laufzeittyp auf *T4 GPU* um
(*Laufzeit → Laufzeittyp ändern*) und führe danach die Setup-Zelle noch einmal aus. Die Funktionen `trainiere()` und `genauigkeit()` schieben Netz und Daten mit
`.to(device)` auf die Grafikkarte. Ohne Grafikkarte läuft der Code auch, dauert aber deutlich länger.''',
     DATEN + HILFE + f"""
import time

print(device)
alle = DataLoader(training, batch_size=128, shuffle=True)
torch.manual_seed(0)
modell = {CNN}
start = time.perf_counter()
trainiere(modell, alle, 1)
print(f'{{time.perf_counter() - start:.1f}} s')
print(f'Test-Genauigkeit: {{genauigkeit(modell, testlader):.3f}}')""")
t('''Trainiere das Faltungsnetz mit allen Trainingsbildern 5 Epochen lang auf der Grafikkarte und gib nach jeder Epoche die Test-Genauigkeit aus. Sie sollte auf etwa 0.99 steigen.
(Ohne Grafikkarte dauert das einige Minuten.)''', DATEN + HILFE,
  f"""

alle = DataLoader(training, batch_size=128, shuffle=True)
torch.manual_seed(0)
modell = {CNN}
for epoche in range(1, 6):
    trainiere(modell, alle, 1)
    print(epoche, f'{{genauigkeit(modell, testlader):.3f}}')""", kind='free')
t('''Miss, wie lange eine Epoche mit allen Trainingsbildern auf der CPU und auf der Grafikkarte dauert. Setze dazu `device` einmal auf `'cpu'` und einmal auf `'cuda'`
(die Funktionen benutzen die Variable `device`).''', DATEN + HILFE + '\nimport time',
  f"""

alle = DataLoader(training, batch_size=128, shuffle=True)
geraete = ['cpu', 'cuda'] if torch.cuda.is_available() else ['cpu']
for geraet in geraete:
    device = geraet
    torch.manual_seed(0)
    modell = {CNN}
    start = time.perf_counter()
    trainiere(modell, alle, 1)
    print(geraet, f'{{time.perf_counter() - start:.1f}} s')""", kind='free')

# ---------------------------------------------------------------- 6
sec('Gemischte Übungen')
t('''**Fashion-MNIST** hat dieselbe Form wie MNIST, zeigt aber Kleidungsstücke (0 T-Shirt, 1 Hose, 2 Pullover, 3 Kleid, 4 Mantel, 5 Sandale, 6 Hemd, 7 Sneaker,
8 Tasche, 9 Stiefel). Lade es mit `datasets.FashionMNIST(...)` (gleiche Parameter wie MNIST), zeige die ersten 10 Bilder mit ihrer Klasse an und trainiere das
Faltungsnetz darauf (10 000 Bilder, Seed 0, 3 Epochen). Die Test-Genauigkeit sollte bei etwa 0.84 liegen: Kleidung ist schwerer als Ziffern.''',
  'import torch\nfrom torch import nn\nfrom torch.utils.data import DataLoader, Subset\nfrom torchvision import datasets, transforms\nimport matplotlib.pyplot as plt',
  f"""namen = ['T-Shirt', 'Hose', 'Pullover', 'Kleid', 'Mantel', 'Sandale', 'Hemd', 'Sneaker', 'Tasche', 'Stiefel']
training = datasets.FashionMNIST(root='daten', train=True, download=True, transform=transforms.ToTensor())
test = datasets.FashionMNIST(root='daten', train=False, download=True, transform=transforms.ToTensor())
plt.figure(figsize=(12, 2))
for i in range(10):
    bild, klasse = training[i]
    plt.subplot(1, 10, i + 1)
    plt.imshow(bild[0].numpy(), cmap='gray')
    plt.title(namen[klasse], fontsize=8)
    plt.axis('off')
plt.show()
torch.manual_seed(0)
lader = DataLoader(Subset(training, range(10000)), batch_size=64, shuffle=True)
modell = {CNN}
verlustfunktion = nn.CrossEntropyLoss()
optimierer = torch.optim.Adam(modell.parameters(), lr=0.001)
for epoche in range(3):
    for xb, yb in lader:
        verlust = verlustfunktion(modell(xb), yb)
        optimierer.zero_grad()
        verlust.backward()
        optimierer.step()
richtig = 0
with torch.no_grad():
    for xb, yb in DataLoader(test, batch_size=1000):
        richtig += (modell(xb).argmax(dim=1) == yb).sum().item()
print(f'{{richtig / len(test):.3f}}')""", kind='free')
t('''Gegen Überanpassung bei Bildern hilft **Dropout**: `nn.Dropout(0.25)` setzt beim Training zufällig ein Viertel der Werte auf 0 (bei `modell.eval()` nicht).
Baue ein Faltungsnetz mit `nn.Dropout(0.25)` vor der letzten `Linear`-Schicht, trainiere es wie im Beispiel (Seed 0, 2 Epochen) und vergleiche die Test-Genauigkeit mit dem
Netz ohne Dropout. Bei so kurzem Training macht Dropout noch kaum einen Unterschied (etwa 0.95 in beiden Fällen); es hilft vor allem bei langem Training
und großen Netzen.''', DATEN + HILFE,
  """

for name in ['ohne', 'mit Dropout']:
    torch.manual_seed(0)
    schichten = [nn.Conv2d(1, 16, 3, padding=1), nn.ReLU(), nn.MaxPool2d(2),
                 nn.Conv2d(16, 32, 3, padding=1), nn.ReLU(), nn.MaxPool2d(2), nn.Flatten()]
    if name == 'mit Dropout':
        schichten.append(nn.Dropout(0.25))
    schichten.append(nn.Linear(32 * 7 * 7, 10))
    modell = nn.Sequential(*schichten)
    trainiere(modell, lader, 2)
    print(name, f'{genauigkeit(modell, testlader):.3f}')""", kind='free')
t('''Baue ein eigenes, größeres Faltungsnetz (z. B. drei `Conv2d`-Schichten oder mehr Filter) und versuche, mit den 10 000 Trainingsbildern in 3 Epochen eine möglichst hohe
Test-Genauigkeit zu erreichen. Mehr als 0.97 ist gut.''', DATEN + HILFE,
  """

torch.manual_seed(0)
modell = nn.Sequential(nn.Conv2d(1, 32, 3, padding=1), nn.ReLU(), nn.Conv2d(32, 32, 3, padding=1), nn.ReLU(), nn.MaxPool2d(2),
                       nn.Conv2d(32, 64, 3, padding=1), nn.ReLU(), nn.MaxPool2d(2),
                       nn.Flatten(), nn.Dropout(0.25), nn.Linear(64 * 7 * 7, 10))
trainiere(modell, lader, 3)
print(f'{genauigkeit(modell, testlader):.3f}')""", kind='free')

generate('pytorch_bilder', 'PyTorch 4: Bilder', INTRO, ordner='extern')
