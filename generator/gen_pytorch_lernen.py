# Erzeugt ../extern/pytorch_lernen.ipynb (siehe nbgen.py). Zweites Notebook der PyTorch-Reihe:
# pytorch_tensoren, pytorch_lernen, pytorch_netze, pytorch_bilder.
#
# Läuft nicht in JupyterLite, sondern in Google Colab. Lokal in der py-3.13-venv p313torch (PyTorch für die CPU).
# Kein Pyodide-Check. Erwartete Ausgaben nur für Gradienten und einzelne Rechenschritte; Trainingsschleifen sind kind='free'
# (der Aufgabentext sagt, welche Werte ungefähr herauskommen). Diagramme nur bei kind='free'.
from nbgen import sec, generate
from torchhilfe import t, expl, predict, reihe, COLAB, SCHLUSS

INTRO = '''Wie lernt ein neuronales Netz? Es verändert seine Gewichte in vielen kleinen Schritten so, dass sein Fehler kleiner wird. Dafür muss es wissen,
**in welche Richtung** es die Gewichte verändern soll: Das sagt ihm die **Ableitung** (der **Gradient**). PyTorch berechnet Ableitungen automatisch.
In diesem Notebook lernst du das Werkzeug dafür kennen, findest damit das Minimum einer Funktion und trainierst dein erstes Modell: eine Gerade,
erst ganz von Hand, dann mit den Bausteinen von PyTorch.

''' + reihe(2) + '''

Vorausgesetzt wird *PyTorch: Tensoren*. Aus dem Mathematikunterricht brauchst du nur: Die Ableitung ist die Steigung einer Funktion.

''' + COLAB + '''

''' + SCHLUSS

T = 'import torch'
GERADE = '''import torch

x = torch.tensor([0.0, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0])
y = torch.tensor([1.1, 2.9, 5.2, 6.8, 9.1, 11.0, 12.8, 15.2, 17.1, 18.9])'''
NN = '''import torch
from torch import nn

x = torch.tensor([0.0, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0]).unsqueeze(1)
y = torch.tensor([1.1, 2.9, 5.2, 6.8, 9.1, 11.0, 12.8, 15.2, 17.1, 18.9]).unsqueeze(1)'''

# ---------------------------------------------------------------- 1
sec('Ableitungen mit autograd')
expl('''#### `requires_grad` und `backward()`

Erzeugt man einen Tensor mit `requires_grad=True`, merkt sich PyTorch jede Rechnung, die mit ihm gemacht wird. Ruft man am Ende für ein Ergebnis `y`
die Methode `y.backward()` auf, berechnet PyTorch die Ableitung von `y` nach dem Tensor und speichert sie in `x.grad`. Das heißt **autograd**
(automatische Ableitung).

Beispiel: `y = x² + 2x` hat die Ableitung `y' = 2x + 2`, an der Stelle 3 also 8.''',
     """import torch

x = torch.tensor(3.0, requires_grad=True)
y = x ** 2 + 2 * x
print(y)
y.backward()
print(x.grad)""")
expl('''#### Mehrere Variablen

Hängt `y` von mehreren Tensoren ab, erhält jeder seinen eigenen Gradienten: die **partielle Ableitung**, also die Steigung, wenn man nur diese eine Variable verändert
und die anderen festhält. Für `y = w · x + b` ist die Ableitung nach `w` gleich `x` und die nach `b` gleich 1.

Achtung: Ruft man `backward()` mehrmals auf, werden die Gradienten **addiert**. Vor einer neuen Rechnung setzt man sie deshalb mit `w.grad = None` zurück.''',
     """import torch

w = torch.tensor(2.0, requires_grad=True)
b = torch.tensor(1.0, requires_grad=True)
x = torch.tensor(5.0)
y = w * x + b
y.backward()
print(w.grad, b.grad)
y = w * x + b
y.backward()
print(w.grad)
w.grad = None
print(w.grad)""")
expl('''#### Rechnen ohne Gedächtnis

Manchmal soll PyTorch eine Rechnung **nicht** verfolgen, z. B. wenn man die Gewichte selbst verändert oder nur eine Vorhersage braucht. Dafür gibt es
`with torch.no_grad():`. Einen Tensor mit Gedächtnis kann man mit `t.detach()` davon lösen (das braucht man z. B. vor `.numpy()`).''',
     """import torch

x = torch.tensor(2.0, requires_grad=True)
with torch.no_grad():
    z = x * 10
print(z.requires_grad)
y = x * 10
print(y.requires_grad, y.detach().requires_grad)""")

t('Berechne mit autograd die Ableitung von `f(x) = x³` an der Stelle 2 (von Hand: `3x² = 12`).', T,
  """x = torch.tensor(2.0, requires_grad=True)
f = x ** 3
f.backward()
print(x.grad)""")
t('Berechne die Ableitung von `f(x) = 4x² - 3x + 7` an den Stellen −1, 0 und 2.5 (für jede Stelle einen neuen Tensor).', T,
  """for stelle in [-1.0, 0.0, 2.5]:
    x = torch.tensor(stelle, requires_grad=True)
    f = 4 * x ** 2 - 3 * x + 7
    f.backward()
    print(stelle, x.grad.item())""")
t('Berechne die Ableitung von `f(x) = sin(x) · e^x` (`torch.sin`, `torch.exp`) an der Stelle 0 und an der Stelle 1 (4 Nachkommastellen).', T,
  """for stelle in [0.0, 1.0]:
    x = torch.tensor(stelle, requires_grad=True)
    f = torch.sin(x) * torch.exp(x)
    f.backward()
    print(f'{x.grad.item():.4f}')""")
t('''Für `f(a, b) = a² · b + b³` berechne die beiden partiellen Ableitungen an der Stelle `a = 2`, `b = 3` (von Hand: `2ab = 12` und `a² + 3b² = 31`).''', T,
  """a = torch.tensor(2.0, requires_grad=True)
b = torch.tensor(3.0, requires_grad=True)
f = a ** 2 * b + b ** 3
f.backward()
print(a.grad, b.grad)""")
t('''Der Gradient geht auch für Vektoren: Für `w = [1, 2, 3]` (mit `requires_grad=True`) und `f = (w ** 2).sum()` ist der Gradient `2w`. Gib ihn aus.''', T,
  """w = torch.tensor([1.0, 2.0, 3.0], requires_grad=True)
f = (w ** 2).sum()
f.backward()
print(w.grad)""")
t('''Zeige, dass sich Gradienten addieren: Berechne für `x = 1` (mit Gradient) dreimal hintereinander `y = 5 * x` und `y.backward()` und gib nach jedem Mal `x.grad` aus.
Setze danach `x.grad = None` und rechne noch einmal.''', T,
  """x = torch.tensor(1.0, requires_grad=True)
for i in range(3):
    y = 5 * x
    y.backward()
    print(x.grad)
x.grad = None
y = 5 * x
y.backward()
print(x.grad)""")
t('''Zeichne die Funktion `f(x) = x³ - 3x` und ihre Ableitung für x von −2.5 bis 2.5. Erzeuge dafür `x = torch.linspace(-2.5, 2.5, 100, requires_grad=True)`, berechne
`f`, rufe `f.sum().backward()` auf (dann enthält `x.grad` die Ableitung an jeder Stelle) und zeichne `f` und `x.grad` über `x` (vorher `.detach().numpy()`).''',
  T + '\nimport matplotlib.pyplot as plt',
  """x = torch.linspace(-2.5, 2.5, 100, requires_grad=True)
f = x ** 3 - 3 * x
f.sum().backward()
plt.plot(x.detach().numpy(), f.detach().numpy(), label='f')
plt.plot(x.detach().numpy(), x.grad.numpy(), label="f'")
plt.axhline(0, color='gray')
plt.legend()
plt.show()""", kind='free')
predict("""import torch

x = torch.tensor(4.0, requires_grad=True)
y = 3 * x + 2
y.backward()
print(y.item(), x.grad.item())""", erklaerung='''- `y = 3 · 4 + 2 = 14`, als Python-Zahl `14.0`.
- Die Ableitung einer Geraden ist ihre Steigung, also überall `3.0`.''')

# ---------------------------------------------------------------- 2
sec('Gradientenabstieg von Hand')
expl('''#### Bergab gehen

Wo hat `f(x) = (x - 3)² + 1` ihr Minimum? Statt die Ableitung gleich 0 zu setzen, kann man es **schrittweise** suchen:

1. Beginne irgendwo, z. B. bei `x = 0`.
2. Berechne die Ableitung an dieser Stelle. Ist sie negativ, fällt die Funktion nach rechts, also geht man nach rechts, und umgekehrt.
3. Gehe einen kleinen Schritt **gegen** die Steigung: `x = x - lernrate · f'(x)`.
4. Wiederhole das.

Das heißt **Gradientenabstieg**. Genau so lernen neuronale Netze, nur mit Millionen Variablen. Den Schritt macht man in `torch.no_grad()`, weil er nicht zur
Funktion gehört, und setzt danach den Gradienten zurück.''',
     """import torch

x = torch.tensor(0.0, requires_grad=True)
lernrate = 0.1
for schritt in range(1, 21):
    f = (x - 3) ** 2 + 1
    f.backward()
    with torch.no_grad():
        x -= lernrate * x.grad
    x.grad = None
    if schritt % 5 == 0:
        print(schritt, f'{x.item():.4f}')""")
expl('''#### Die Lernrate

Die **Lernrate** bestimmt die Größe der Schritte. Ist sie zu klein, kommt man nur sehr langsam voran. Ist sie zu groß, springt man über das Minimum hinweg,
im schlimmsten Fall immer weiter weg.''',
     """import torch

for lernrate in [0.01, 0.1, 0.9, 1.1]:
    x = torch.tensor(0.0, requires_grad=True)
    for schritt in range(20):
        f = (x - 3) ** 2 + 1
        f.backward()
        with torch.no_grad():
            x -= lernrate * x.grad
        x.grad = None
    print(lernrate, f'{x.item():.4f}')""")

t('''Führe für `f(x) = (x - 3)² + 1` mit Start 0 und Lernrate 0.1 die ersten 3 Schritte des Gradientenabstiegs aus. Gib nach jedem Schritt `x` aus (4 Nachkommastellen).
Von Hand: `f'(0) = -6`, also `x = 0 - 0.1 · (-6) = 0.6`.''', T,
  """x = torch.tensor(0.0, requires_grad=True)
for schritt in range(3):
    f = (x - 3) ** 2 + 1
    f.backward()
    with torch.no_grad():
        x -= 0.1 * x.grad
    x.grad = None
    print(f'{x.item():.4f}')""")
t('''Suche mit Gradientenabstieg das Minimum von `f(x) = x² - 4x + 7`: Start 5, Lernrate 0.1, 100 Schritte. Gib `x` und `f(x)` aus (4 Nachkommastellen).
Es sollte bei `x = 2`, `f = 3` liegen.''', T,
  """x = torch.tensor(5.0, requires_grad=True)
for schritt in range(100):
    f = x ** 2 - 4 * x + 7
    f.backward()
    with torch.no_grad():
        x -= 0.1 * x.grad
    x.grad = None
print(f'{x.item():.4f} {(x ** 2 - 4 * x + 7).item():.4f}')""")
t('''Wie viele Schritte braucht der Gradientenabstieg für `f(x) = (x - 3)² + 1` (Start 0) bis `|x - 3| < 0.001` bei den Lernraten 0.01, 0.1 und 0.5? Gib Lernrate und
Anzahl der Schritte aus.''', T,
  """for lernrate in [0.01, 0.1, 0.5]:
    x = torch.tensor(0.0, requires_grad=True)
    schritte = 0
    while abs(x.item() - 3) >= 0.001:
        f = (x - 3) ** 2 + 1
        f.backward()
        with torch.no_grad():
            x -= lernrate * x.grad
        x.grad = None
        schritte += 1
    print(lernrate, schritte)""")
t('''Gradientenabstieg mit zwei Variablen: Suche das Minimum von `f(a, b) = (a - 1)² + 2 · (b + 2)²` (Start `a = b = 0`, Lernrate 0.1, 100 Schritte). Ändere beide Variablen
in jedem Schritt. Gib `a` und `b` aus (3 Nachkommastellen); das Minimum liegt bei (1 | −2).''', T,
  """a = torch.tensor(0.0, requires_grad=True)
b = torch.tensor(0.0, requires_grad=True)
for schritt in range(100):
    f = (a - 1) ** 2 + 2 * (b + 2) ** 2
    f.backward()
    with torch.no_grad():
        a -= 0.1 * a.grad
        b -= 0.1 * b.grad
    a.grad = None
    b.grad = None
print(f'{a.item():.3f} {b.item():.3f}')""")
t('''Eine Funktion mit zwei Tälern: `f(x) = x⁴ - 4x² + x`. Starte den Gradientenabstieg (Lernrate 0.01, 500 Schritte) einmal bei −0.5 und einmal bei 0.5 und gib
jeweils das gefundene `x` aus (3 Nachkommastellen). Je nach Start landet man in einem anderen Tal, einem **lokalen Minimum**.''', T,
  """for start in [-0.5, 0.5]:
    x = torch.tensor(start, requires_grad=True)
    for schritt in range(500):
        f = x ** 4 - 4 * x ** 2 + x
        f.backward()
        with torch.no_grad():
            x -= 0.01 * x.grad
        x.grad = None
    print(start, f'{x.item():.3f}')""")
t('''Zeichne die Funktion `f(x) = (x - 3)² + 1` (x von −1 bis 7) und die ersten 10 Schritte des Gradientenabstiegs (Start 0, Lernrate 0.3) als rote Punkte auf dem Graphen.''',
  T + '\nimport matplotlib.pyplot as plt',
  """werte_x = torch.linspace(-1, 7, 100)
plt.plot(werte_x, (werte_x - 3) ** 2 + 1)
x = torch.tensor(0.0, requires_grad=True)
for schritt in range(10):
    f = (x - 3) ** 2 + 1
    plt.plot(x.item(), f.item(), 'ro')
    f.backward()
    with torch.no_grad():
        x -= 0.3 * x.grad
    x.grad = None
plt.show()""", kind='free')
predict("""import torch

x = torch.tensor(10.0, requires_grad=True)
f = x ** 2
f.backward()
with torch.no_grad():
    x -= 0.25 * x.grad
print(x.item())""", erklaerung='''Die Ableitung von `x²` ist `2x`, bei 10 also 20. Ein Schritt mit Lernrate 0.25: `10 - 0.25 · 20 = 5`. Ausgabe: `5.0`.''')

# ---------------------------------------------------------------- 3
sec('Eine Gerade lernen')
expl('''#### Fehler messen

Gegeben sind Messpunkte, die ungefähr auf einer Geraden liegen. Gesucht sind die **Gewichte** `w` (Steigung) und `b` (Achsenabschnitt) der Geraden `y = w · x + b`,
die am besten passt. Wie gut eine Gerade passt, misst der **Verlust** (*loss*): hier der **mittlere quadratische Fehler**
`mean((w · x + b - y)²)`. Ihn soll der Gradientenabstieg möglichst klein machen. Der Verlust hängt von `w` und `b` ab, also braucht man die Gradienten
nach `w` und `b`.''',
     GERADE + """

w = torch.tensor(0.0, requires_grad=True)
b = torch.tensor(0.0, requires_grad=True)
vorhersage = w * x + b
verlust = ((vorhersage - y) ** 2).mean()
print(f'{verlust.item():.4f}')
verlust.backward()
print(f'{w.grad.item():.4f} {b.grad.item():.4f}')""")
expl('''#### Die Trainingsschleife

Training heißt: Den Gradientenabstieg für den Verlust viele Male wiederholen. Jeder Durchlauf über alle Daten heißt **Epoche**.''',
     GERADE + """

w = torch.tensor(0.0, requires_grad=True)
b = torch.tensor(0.0, requires_grad=True)
lernrate = 0.01
for epoche in range(1, 2001):
    verlust = ((w * x + b - y) ** 2).mean()
    verlust.backward()
    with torch.no_grad():
        w -= lernrate * w.grad
        b -= lernrate * b.grad
    w.grad = None
    b.grad = None
    if epoche % 500 == 0:
        print(epoche, f'Verlust {verlust.item():.4f}, w = {w.item():.3f}, b = {b.item():.3f}')""")

t('''Berechne den Verlust (mittlerer quadratischer Fehler) der Geraden `y = 2x + 1` für die Messpunkte in der Zelle (4 Nachkommastellen).''', GERADE,
  """vorhersage = 2 * x + 1
print(f'{((vorhersage - y) ** 2).mean().item():.4f}')""")
t('''Berechne für `w = 1` und `b = 0` den Verlust und die Gradienten nach `w` und `b` (4 Nachkommastellen). Beide Gradienten sind negativ: `w` und `b` müssen größer werden.''',
  GERADE,
  """w = torch.tensor(1.0, requires_grad=True)
b = torch.tensor(0.0, requires_grad=True)
verlust = ((w * x + b - y) ** 2).mean()
verlust.backward()
print(f'{verlust.item():.4f}')
print(f'{w.grad.item():.4f} {b.grad.item():.4f}')""")
t('''Führe das Training aus dem Beispiel mit der Lernrate 0.02 für 3000 Epochen aus und gib am Ende den Verlust, `w` und `b` aus (4 Nachkommastellen).
`w` sollte etwa 2.0 und `b` etwa 1.0 sein. Vergleiche mit der exakten Lösung von `np.polyfit(x.numpy(), y.numpy(), 1)`.''',
  GERADE + '\nimport numpy as np',
  """w = torch.tensor(0.0, requires_grad=True)
b = torch.tensor(0.0, requires_grad=True)
for epoche in range(3000):
    verlust = ((w * x + b - y) ** 2).mean()
    verlust.backward()
    with torch.no_grad():
        w -= 0.02 * w.grad
        b -= 0.02 * b.grad
    w.grad = None
    b.grad = None
print(f'{verlust.item():.4f} {w.item():.4f} {b.item():.4f}')
print(np.polyfit(x.numpy(), y.numpy(), 1).round(4))""", kind='free')
t('''Was passiert bei zu großer Lernrate? Trainiere die Gerade mit den Lernraten 0.001, 0.01 und 0.05 für je 100 Epochen und gib am Ende den Verlust aus.
Bei 0.05 wird der Verlust riesig (die Schritte schießen immer weiter über das Ziel hinaus).''', GERADE,
  """for lernrate in [0.001, 0.01, 0.05]:
    w = torch.tensor(0.0, requires_grad=True)
    b = torch.tensor(0.0, requires_grad=True)
    for epoche in range(100):
        verlust = ((w * x + b - y) ** 2).mean()
        verlust.backward()
        with torch.no_grad():
            w -= lernrate * w.grad
            b -= lernrate * b.grad
        w.grad = None
        b.grad = None
    print(lernrate, f'{verlust.item():.4g}')""", kind='free')
t('''Speichere beim Training (Lernrate 0.01, 500 Epochen) den Verlust jeder Epoche in einer Liste und zeichne die **Verlustkurve** mit logarithmischer y-Achse
(`plt.yscale('log')`). Sie fällt erst schnell und dann immer langsamer.''', GERADE + '\nimport matplotlib.pyplot as plt',
  """w = torch.tensor(0.0, requires_grad=True)
b = torch.tensor(0.0, requires_grad=True)
verluste = []
for epoche in range(500):
    verlust = ((w * x + b - y) ** 2).mean()
    verluste.append(verlust.item())
    verlust.backward()
    with torch.no_grad():
        w -= 0.01 * w.grad
        b -= 0.01 * b.grad
    w.grad = None
    b.grad = None
plt.plot(verluste)
plt.yscale('log')
plt.xlabel('Epoche')
plt.ylabel('Verlust')
plt.show()""", kind='free')
predict("""import torch

x = torch.tensor([1.0, 2.0])
y = torch.tensor([3.0, 5.0])
w = torch.tensor(2.0)
b = torch.tensor(1.0)
print(((w * x + b - y) ** 2).mean().item())
print(((w * x - y) ** 2).mean().item())""", erklaerung='''- `2 · 1 + 1 = 3` und `2 · 2 + 1 = 5` treffen die Punkte genau: Verlust `0.0`.
- Ohne `b` sind beide Vorhersagen um 1 zu klein: `(1 + 1) / 2 = 1.0`.''')

# ---------------------------------------------------------------- 4
sec('Mit den Bausteinen von PyTorch')
expl('''#### `nn.Linear`, `nn.MSELoss` und `torch.optim`

Die Teile der Trainingsschleife gibt es fertig:

- `nn.Linear(1, 1)` aus `torch.nn` ist eine **Schicht**, die `w · x + b` berechnet (1 Eingabe, 1 Ausgabe). Ihre Gewichte werden zufällig gewählt
  und stehen in `modell.weight` und `modell.bias`. Die Eingabe muss ein Stapel sein: Form `[Anzahl, 1]` (deshalb `unsqueeze(1)`).
- `nn.MSELoss()` berechnet den mittleren quadratischen Fehler.
- `torch.optim.SGD(modell.parameters(), lr=0.01)` ist der **Optimierer**: `optimierer.step()` macht den Schritt gegen die Gradienten aller Gewichte,
  `optimierer.zero_grad()` setzt die Gradienten zurück.

Die Trainingsschleife hat immer dieselben fünf Zeilen.''',
     NN + """

torch.manual_seed(0)
modell = nn.Linear(1, 1)
verlustfunktion = nn.MSELoss()
optimierer = torch.optim.SGD(modell.parameters(), lr=0.01)
for epoche in range(2000):
    vorhersage = modell(x)                       # 1. vorhersagen
    verlust = verlustfunktion(vorhersage, y)     # 2. Fehler messen
    optimierer.zero_grad()                       # 3. alte Gradienten löschen
    verlust.backward()                           # 4. Gradienten berechnen
    optimierer.step()                            # 5. Gewichte verbessern
print(f'{verlust.item():.4f}')
print(f'{modell.weight.item():.3f} {modell.bias.item():.3f}')""")
expl('''#### Vorhersagen und andere Optimierer

- Vorhersagen für neue Werte macht man mit `modell(x_neu)` innerhalb von `torch.no_grad()`.
- `torch.optim.Adam(modell.parameters(), lr=0.1)` ist ein Optimierer, der die Schrittweite für jedes Gewicht selbst anpasst. Er kommt oft schneller ans Ziel
  und ist der Standard für neuronale Netze.''',
     NN + """

torch.manual_seed(0)
modell = nn.Linear(1, 1)
verlustfunktion = nn.MSELoss()
optimierer = torch.optim.Adam(modell.parameters(), lr=0.1)
for epoche in range(500):
    verlust = verlustfunktion(modell(x), y)
    optimierer.zero_grad()
    verlust.backward()
    optimierer.step()
with torch.no_grad():
    print(modell(torch.tensor([[10.0], [20.0]])))""")

t('''Erzeuge eine Schicht `nn.Linear(3, 2)` (3 Eingaben, 2 Ausgaben) und gib die Formen von `weight` und `bias` und die Anzahl aller Gewichte aus
(`sum([p.numel() for p in schicht.parameters()])`).''', 'import torch\nfrom torch import nn',
  """schicht = nn.Linear(3, 2)
print(schicht.weight.shape, schicht.bias.shape)
print(sum([p.numel() for p in schicht.parameters()]))""")
t('''Setze die Gewichte einer Schicht `nn.Linear(2, 1)` von Hand auf `w = [[3, -1]]` und `b = [0.5]` (in `torch.no_grad()`: `schicht.weight[:] = torch.tensor([[3.0, -1.0]])`
und ebenso `bias`) und berechne die Ausgabe für den Stapel `[[1, 2], [0, 0], [2, 1]]`.''', 'import torch\nfrom torch import nn',
  """schicht = nn.Linear(2, 1)
with torch.no_grad():
    schicht.weight[:] = torch.tensor([[3.0, -1.0]])
    schicht.bias[:] = torch.tensor([0.5])
    print(schicht(torch.tensor([[1.0, 2.0], [0.0, 0.0], [2.0, 1.0]])))""")
t('''Prüfe, dass `nn.MSELoss()` dasselbe berechnet wie `((a - b) ** 2).mean()`, für die Tensoren in der Zelle.''',
  'import torch\nfrom torch import nn\n\na = torch.tensor([1.0, 2.0, 3.0])\nb = torch.tensor([1.5, 2.0, 5.0])',
  """print(nn.MSELoss()(a, b))
print(((a - b) ** 2).mean())""")
t('''Trainiere `nn.Linear(1, 1)` (Seed 0) mit `SGD` und Lernrate 0.02 für 3000 Epochen auf den Daten in der Zelle und sage die Werte für `x` = 10, 20 und 100 vorher
(eine Nachkommastelle). Sie sollten etwa 21, 41 und 201 sein.''', NN,
  """torch.manual_seed(0)
modell = nn.Linear(1, 1)
verlustfunktion = nn.MSELoss()
optimierer = torch.optim.SGD(modell.parameters(), lr=0.02)
for epoche in range(3000):
    verlust = verlustfunktion(modell(x), y)
    optimierer.zero_grad()
    verlust.backward()
    optimierer.step()
with torch.no_grad():
    print(modell(torch.tensor([[10.0], [20.0], [100.0]])).round(decimals=1))""", kind='free')
t('''Vergleiche `SGD` (Lernrate 0.01) und `Adam` (Lernrate 0.1): Trainiere jeweils `nn.Linear(1, 1)` (Seed 0) für 200 Epochen und gib den Verlust am Ende aus (4 Nachkommastellen).
Bei dieser einfachen Aufgabe ist SGD sogar etwas besser (etwa 0.022 gegen 0.028). Adam spielt seine Stärke erst bei Netzen mit vielen Gewichten aus.''', NN,
  """for name in ['SGD', 'Adam']:
    torch.manual_seed(0)
    modell = nn.Linear(1, 1)
    if name == 'SGD':
        optimierer = torch.optim.SGD(modell.parameters(), lr=0.01)
    else:
        optimierer = torch.optim.Adam(modell.parameters(), lr=0.1)
    verlustfunktion = nn.MSELoss()
    for epoche in range(200):
        verlust = verlustfunktion(modell(x), y)
        optimierer.zero_grad()
        verlust.backward()
        optimierer.step()
    print(name, f'{verlust.item():.4f}')""", kind='free')
WOHN = '''import torch
from torch import nn

# Spalten: Fläche in 100 m², Zimmer / 10, Entfernung zur Innenstadt in 10 km (so sind alle Werte etwa gleich groß)
X = torch.tensor([[0.45, 0.2, 0.3], [0.80, 0.3, 0.5], [1.20, 0.4, 0.2], [0.60, 0.2, 1.0], [0.95, 0.3, 0.8],
                  [0.35, 0.1, 0.1], [1.40, 0.5, 1.2], [0.70, 0.3, 0.4], [1.05, 0.4, 0.6], [0.55, 0.2, 0.7]])
miete = torch.tensor([[600.0], [920.0], [1350.0], [610.0], [960.0], [520.0], [1380.0], [820.0], [1150.0], [610.0]])'''
t('''Mehrere Eingaben: Lerne die Miete aus drei Merkmalen mit `nn.Linear(3, 1)` (Seed 0, `Adam` mit Lernrate 0.5, 3000 Epochen). Teile die Mieten beim Training durch 1000
(dann sind auch die Zielwerte klein) und gib die gelernten Gewichte und die Vorhersage für eine Wohnung mit 75 m², 3 Zimmern und 4 km Entfernung in Euro aus
(ganze Euro). Die Gewichte sollten etwa 0.9, 0.4 und −0.2 sein (also etwa 900 € pro 100 m² und −200 € pro 10 km), die Vorhersage etwa 880 €.''', WOHN,
  """torch.manual_seed(0)
modell = nn.Linear(3, 1)
verlustfunktion = nn.MSELoss()
optimierer = torch.optim.Adam(modell.parameters(), lr=0.5)
for epoche in range(3000):
    verlust = verlustfunktion(modell(X), miete / 1000)
    optimierer.zero_grad()
    verlust.backward()
    optimierer.step()
print(modell.weight.detach().round(decimals=2), modell.bias.detach().round(decimals=2))
with torch.no_grad():
    print(f'{modell(torch.tensor([[0.75, 0.3, 0.4]])).item() * 1000:.0f}')""", kind='free')
t('''Zeichne die Messpunkte und die gelernte Gerade aus `nn.Linear(1, 1)` (Seed 0, Adam mit Lernrate 0.1, 500 Epochen) in ein Diagramm. Die Vorhersage für die Zeichnung
berechnest du in `torch.no_grad()` und wandelst sie mit `.numpy()` um.''', NN + '\nimport matplotlib.pyplot as plt',
  """torch.manual_seed(0)
modell = nn.Linear(1, 1)
verlustfunktion = nn.MSELoss()
optimierer = torch.optim.Adam(modell.parameters(), lr=0.1)
for epoche in range(500):
    verlust = verlustfunktion(modell(x), y)
    optimierer.zero_grad()
    verlust.backward()
    optimierer.step()
with torch.no_grad():
    linie = modell(x)
plt.scatter(x.numpy(), y.numpy())
plt.plot(x.numpy(), linie.numpy(), color='red')
plt.show()""", kind='free')
predict("""import torch
from torch import nn

schicht = nn.Linear(4, 3)
print(schicht.weight.shape)
print(schicht(torch.zeros(5, 4)).shape)""", erklaerung='''- Die Gewichtsmatrix hat eine Zeile pro Ausgabe und eine Spalte pro Eingabe: `torch.Size([3, 4])`.
- Ein Stapel aus 5 Beispielen mit je 4 Eingaben ergibt 5 Beispiele mit je 3 Ausgaben: `torch.Size([5, 3])`.''')

# ---------------------------------------------------------------- 5
sec('Gemischte Übungen')
t('''Eine Parabel lernen: Die Punkte in der Zelle liegen ungefähr auf `y = 0.5x² - 2x + 3`. Gib dem Modell `nn.Linear(2, 1)` als Eingaben `x` und `x²`
(`torch.cat([x, x ** 2], dim=1)`) und trainiere es (Seed 0, Adam mit Lernrate 0.05, 3000 Epochen). Die Gewichte sollten etwa −2 und 0.5 sein, der bias etwa 3.''',
  '''import torch
from torch import nn

x = torch.tensor([-2.0, -1.0, 0.0, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0]).unsqueeze(1)
y = torch.tensor([9.1, 5.4, 3.1, 1.4, 1.1, 1.6, 2.9, 5.6, 9.0]).unsqueeze(1)''',
  """eingabe = torch.cat([x, x ** 2], dim=1)
torch.manual_seed(0)
modell = nn.Linear(2, 1)
optimierer = torch.optim.Adam(modell.parameters(), lr=0.05)
verlustfunktion = nn.MSELoss()
for epoche in range(3000):
    verlust = verlustfunktion(modell(eingabe), y)
    optimierer.zero_grad()
    verlust.backward()
    optimierer.step()
print(modell.weight.detach().round(decimals=2), modell.bias.detach().round(decimals=2))""", kind='free')
t('''**Logistische Regression** mit PyTorch: Für die Lernzeiten in der Zelle ist bekannt, ob die Prüfung bestanden wurde (1) oder nicht (0). Das Modell ist `nn.Linear(1, 1)`,
dessen Ausgabe mit `torch.sigmoid()` zu einer Wahrscheinlichkeit wird (die S-Kurve aus *scikit-learn: Klassifikation*). Die Verlustfunktion für Wahrscheinlichkeiten ist
`nn.BCELoss()` (*binary cross entropy*). Trainiere (Seed 0, Adam mit Lernrate 0.1, 2000 Epochen) und gib die Wahrscheinlichkeiten für 2, 4 und 6 Stunden aus
(3 Nachkommastellen). Sie sollten etwa 0.10, 0.58 und 0.94 sein.''',
  '''import torch
from torch import nn

stunden = torch.tensor([0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5, 5.5, 6, 6.5, 7]).unsqueeze(1)
bestanden = torch.tensor([0.0, 0, 0, 0, 1, 0, 0, 1, 0, 1, 1, 1, 1, 1]).unsqueeze(1)''',
  """torch.manual_seed(0)
modell = nn.Linear(1, 1)
optimierer = torch.optim.Adam(modell.parameters(), lr=0.1)
verlustfunktion = nn.BCELoss()
for epoche in range(2000):
    verlust = verlustfunktion(torch.sigmoid(modell(stunden)), bestanden)
    optimierer.zero_grad()
    verlust.backward()
    optimierer.step()
with torch.no_grad():
    print(torch.sigmoid(modell(torch.tensor([[2.0], [4.0], [6.0]]))).round(decimals=3))""", kind='free')
t('''Schreibe eine Funktion `minimum(f, start, lernrate, schritte)`, die mit Gradientenabstieg ein Minimum der Python-Funktion `f` sucht und das gefundene `x` als Python-Zahl
zurückgibt. Teste sie mit `f(x) = (x - 1)² · (x + 2)² + x` (Start 2, Lernrate 0.01, 1000 Schritte, 3 Nachkommastellen).''', T,
  """

def minimum(f, start, lernrate, schritte):
    x = torch.tensor(start, requires_grad=True)
    for schritt in range(schritte):
        wert = f(x)
        wert.backward()
        with torch.no_grad():
            x -= lernrate * x.grad
        x.grad = None
    return x.item()


def f(x):
    return (x - 1) ** 2 * (x + 2) ** 2 + x


print(f'{minimum(f, 2.0, 0.01, 1000):.3f}')""")

generate('pytorch_lernen', 'PyTorch 2: Lernen', INTRO, ordner='extern')
