# Erzeugt ../content/pillow_grundlagen.ipynb (siehe nbgen.py). Erstes Notebook der Pillow-Reihe:
# pillow_grundlagen, pillow_zeichnen, pillow_bearbeiten, pillow_pixel.
#
# JupyterLite: Pillow 12.2.0, lokal in der py-3.13-venv p313uebungen (pip install pillow==12.2.0).
#     python generator/gen_pillow_grundlagen.py
#     py -3.13 generator/pyodide_check/pruefen.py generator/gen_pillow_grundlagen.py
#
# Ausgaben wie in JupyterLab (pandasnb.py): Ein Bild in der letzten Zeile wird als erwartetes Bild angehängt
# (verkleinert auf höchstens 320 Pixel, Fotos als JPEG). Der Pyodide-Check vergleicht nur den Text, nicht die Bilder.
# Keine Dateigrößen ausgeben (hängen von zlib/libjpeg ab). Die Fotos liegen als PNG in content/ (dateien=FOTOS).
import pandasnb
from nbgen import sec, expl, predict, generate
from pillowhilfe import t, reihe, ANZEIGEN, SCHLUSS, FOTOS, FOTOS_MD, NEBEN, N

INTRO = '''Ein digitales Bild ist ein Raster aus **Pixeln** (Bildpunkten), jedes mit einer Farbe. Mit dem Paket **Pillow** (Modulname `PIL`) erzeugst, bearbeitest und
speicherst du Bilder in Python. In diesem Notebook lernst du, wie Pillow Bilder, Farben und Pixel darstellt, wie du einzelne Pixel liest und setzt,
mit Schleifen Muster erzeugst und Bilddateien speicherst und öffnest.

''' + reihe(1) + '''

Vorausgesetzt werden die Notebooks *Schleifen*, *Tupel* und *Funktionen*.

''' + ANZEIGEN + '''

''' + FOTOS_MD + '''

''' + SCHLUSS

P = 'from PIL import Image'

# ---------------------------------------------------------------- 1
sec('Ein Bild erzeugen')
expl('''#### `Image.new()`

`Image.new('RGB', (breite, hoehe), farbe)` erzeugt ein neues Bild, in dem jedes Pixel die angegebene Farbe hat. `'RGB'` ist der **Modus**: Jede Farbe besteht aus den
drei Anteilen **R**ot, **G**rün und **B**lau, jeder von 0 bis 255. Steht das Bild in der letzten Zeile der Zelle, wird es angezeigt.

- `bild.size` ist das Tupel `(breite, hoehe)`, `bild.width` und `bild.height` sind die einzelnen Werte.
- `bild.mode` ist der Modus.''',
     """from PIL import Image

bild = Image.new('RGB', (200, 100), (255, 128, 0))
print(bild.size, bild.width, bild.height, bild.mode)
bild""")
expl('''#### Farben angeben

Eine Farbe kann man auf drei Arten angeben:

| Schreibweise | Beispiel | Bedeutung |
|---|---|---|
| Tupel | `(255, 0, 0)` | Rot, Grün, Blau von 0 bis 255 |
| Name | `'red'`, `'gold'`, `'navy'` | englische Farbnamen (wie in HTML) |
| Hex-Code | `'#ff8800'` | je zwei Hexadezimalziffern für Rot, Grün, Blau |

`(0, 0, 0)` ist Schwarz, `(255, 255, 255)` Weiß, gleiche Anteile ergeben Grau. `ImageColor.getrgb(farbe)` rechnet Namen und Hex-Codes in ein Tupel um.''',
     """from PIL import Image, ImageColor

print(ImageColor.getrgb('gold'), ImageColor.getrgb('#ff8800'))
Image.new('RGB', (150, 40), '#ff8800')""")
expl('''#### Mehrere Bilder in einer Zelle: `nebeneinander()`

Eine Zelle zeigt nur das Bild in ihrer **letzten Zeile** an. (In JupyterLab gibt es dafür auch `display(bild)`, aber im Browser-Python von JupyterLite
bleiben Pillow-Bilder damit leer.) Will man mehrere Bilder vergleichen, setzt man sie zu **einem** Bild zusammen. Das macht die Funktion `nebeneinander(bilder)`:
Sie bekommt eine Liste von Bildern, erzeugt ein Bild, das breit genug für alle ist, und fügt die Bilder mit `paste()` nebeneinander ein (`paste()` lernst du in
*Pillow: Bearbeiten* genauer kennen). Du musst sie nicht selbst schreiben: In den Aufgaben, die sie brauchen, steht sie schon in der Zelle.''',
     """from PIL import Image

""" + NEBEN + """

nebeneinander([Image.new('RGB', (150, 40), 'navy'), Image.new('RGB', (150, 40), '#ff8800'), Image.new('RGB', (150, 40), (128, 128, 128))])""")

t('Erzeuge ein grünes Bild (`(0, 200, 0)`) mit 300 × 150 Pixeln, gib seine Größe aus und zeige es an.', P,
  """bild = Image.new('RGB', (300, 150), (0, 200, 0))
print(bild.size)
bild""")
t('''Erzeuge ein quadratisches Bild mit 120 Pixeln Seitenlänge in der Farbe `'purple'` und zeige es an.''', P,
  "Image.new('RGB', (120, 120), 'purple')")
t('''Gib die Farbanteile von `'orange'`, `'skyblue'` und `'#336699'` als Tupel aus.''', 'from PIL import ImageColor',
  """for farbe in ['orange', 'skyblue', '#336699']:
    print(farbe, ImageColor.getrgb(farbe))""")
t('''Zeige fünf Quadrate mit 60 × 60 Pixeln nebeneinander an: Grau mit den Helligkeiten 0, 64, 128, 192 und 255 (alle drei Anteile gleich).
Sammle die Bilder in einer Liste und zeige `nebeneinander(bilder)` an.''', P + N,
  """bilder = []
for wert in [0, 64, 128, 192, 255]:
    bilder.append(Image.new('RGB', (60, 60), (wert, wert, wert)))
nebeneinander(bilder)""")
t('''Mische Farben: Zeige die Farben `(255, 255, 0)`, `(0, 255, 255)` und `(255, 0, 255)` als Bilder mit 100 × 50 Pixeln an. Rot und Grün ergeben Gelb,
Grün und Blau ergeben Türkis (Cyan), Rot und Blau ergeben Magenta.''', P + N,
  """bilder = []
for farbe in [(255, 255, 0), (0, 255, 255), (255, 0, 255)]:
    bilder.append(Image.new('RGB', (100, 50), farbe))
nebeneinander(bilder)""")
predict("""from PIL import Image

bild = Image.new('RGB', (640, 480), 'white')
print(bild.size)
print(bild.width * bild.height)
print(bild.mode)""", erklaerung='''- `size` ist `(breite, hoehe)`: `(640, 480)`.
- Das Bild hat `640 · 480 = 307200` Pixel.
- Der Modus ist `RGB`.''')

# ---------------------------------------------------------------- 2
sec('Pixel lesen und setzen')
expl('''#### `getpixel()` und `putpixel()`

Jedes Pixel hat eine Position `(x, y)`. Der **Ursprung** `(0, 0)` ist oben links, `x` wächst nach rechts, `y` wächst **nach unten** (anders als im Mathematikunterricht).
Das Pixel unten rechts hat die Position `(breite - 1, hoehe - 1)`.

- `bild.getpixel((x, y))` gibt die Farbe des Pixels als Tupel zurück.
- `bild.putpixel((x, y), farbe)` setzt die Farbe eines Pixels.

Die Position ist ein Tupel, deshalb die doppelten Klammern.''',
     """from PIL import Image

bild = Image.new('RGB', (20, 10), 'white')
bild.putpixel((0, 0), (255, 0, 0))
bild.putpixel((19, 9), (0, 0, 255))
print(bild.getpixel((0, 0)), bild.getpixel((19, 9)), bild.getpixel((5, 5)))
bild.resize((200, 100), Image.NEAREST)""")
expl('''#### Kleine Bilder vergrößert anzeigen

Ein Bild mit 20 × 10 Pixeln ist auf dem Bildschirm winzig. `bild.resize((200, 100), Image.NEAREST)` gibt eine vergrößerte Kopie zurück, in der jedes Pixel ein
10 × 10 großes Quadrat ist (`NEAREST`: jedes neue Pixel übernimmt die Farbe des nächsten alten, ohne zu glätten). Das Bild selbst bleibt unverändert.

Mit einer Schleife setzt man viele Pixel, z. B. eine waagerechte Linie in Zeile 4.''',
     """from PIL import Image

bild = Image.new('RGB', (20, 10), 'white')
for x in range(20):
    bild.putpixel((x, 4), (0, 0, 0))
bild.resize((200, 100), Image.NEAREST)""")

t('''Erzeuge ein weißes Bild mit 10 × 10 Pixeln, setze die vier Eckpixel rot und gib ihre Farben zur Kontrolle aus. Zeige das Bild 20-fach vergrößert an (`NEAREST`).''', P,
  """bild = Image.new('RGB', (10, 10), 'white')
for ecke in [(0, 0), (9, 0), (0, 9), (9, 9)]:
    bild.putpixel(ecke, (255, 0, 0))
    print(bild.getpixel(ecke))
bild.resize((200, 200), Image.NEAREST)""")
t('''Zeichne in ein weißes 16 × 16-Bild eine senkrechte schwarze Linie in Spalte 5 und eine waagerechte blaue in Zeile 10. Zeige es 15-fach vergrößert an.''', P,
  """bild = Image.new('RGB', (16, 16), 'white')
for y in range(16):
    bild.putpixel((5, y), (0, 0, 0))
for x in range(16):
    bild.putpixel((x, 10), (0, 0, 255))
bild.resize((240, 240), Image.NEAREST)""")
t('''Zeichne in ein weißes 12 × 12-Bild die beiden Diagonalen in Rot (von oben links nach unten rechts: `(i, i)`, die andere: `(11 - i, i)`). Zeige es 20-fach vergrößert an.''', P,
  """bild = Image.new('RGB', (12, 12), 'white')
for i in range(12):
    bild.putpixel((i, i), (255, 0, 0))
    bild.putpixel((11 - i, i), (255, 0, 0))
bild.resize((240, 240), Image.NEAREST)""")
t('''Zeichne einen schwarzen Rahmen (1 Pixel breit) um ein gelbes Bild mit 30 × 20 Pixeln. Zähle dabei mit, wie viele Pixel du schwarz färbst (jedes nur einmal!),
und gib die Zahl aus. Zeige das Bild 8-fach vergrößert an.''', P,
  """bild = Image.new('RGB', (30, 20), 'yellow')
anzahl = 0
for x in range(30):
    for y in range(20):
        if x == 0 or x == 29 or y == 0 or y == 19:
            bild.putpixel((x, y), (0, 0, 0))
            anzahl += 1
print(anzahl)
bild.resize((240, 160), Image.NEAREST)""")
t('''Pixel-Kunst: Die Liste `muster` beschreibt ein Bild Zeile für Zeile, `#` ist schwarz, `.` ist weiß. Erzeuge daraus ein Bild (Breite = Länge einer Zeile, Höhe = Anzahl der Zeilen)
und zeige es 25-fach vergrößert an.''',
  P + "\n\nmuster = ['..##..##..',\n          '.####.###.',\n          '##########',\n          '##########',\n          '.########.',\n          '..######..',\n          '...####...',\n          '....##....']",
  """bild = Image.new('RGB', (len(muster[0]), len(muster)), 'white')
for y in range(len(muster)):
    for x in range(len(muster[y])):
        if muster[y][x] == '#':
            bild.putpixel((x, y), (200, 0, 0))
bild.resize((bild.width * 25, bild.height * 25), Image.NEAREST)""")
t('''Gib die Farben der Pixel `(0, 0)`, `(320, 200)` und `(639, 426)` des Fotos `pagode.png` aus (`Image.open('pagode.png')`).''', P,
  """foto = Image.open('pagode.png')
for position in [(0, 0), (320, 200), (639, 426)]:
    print(position, foto.getpixel(position))""")
predict("""from PIL import Image

bild = Image.new('RGB', (5, 3), 'black')
bild.putpixel((4, 2), (255, 255, 255))
print(bild.getpixel((4, 2)))
print(bild.getpixel((2, 1)))
bild.putpixel((5, 3), (255, 0, 0))""", error=IndexError, erklaerung='''- Das Pixel unten rechts `(4, 2)` wurde weiß gesetzt: `(255, 255, 255)`.
- Alle anderen sind schwarz: `(0, 0, 0)`.
- Bei 5 × 3 Pixeln gehen `x` von 0 bis 4 und `y` von 0 bis 2. `(5, 3)` liegt außerhalb: `IndexError`.''')

# ---------------------------------------------------------------- 3
sec('Muster mit Schleifen')
expl('''#### Für jedes Pixel eine Farbe berechnen

Mit zwei verschachtelten Schleifen über alle `x` und `y` kann man für jedes Pixel eine Farbe **ausrechnen**. Beim **Farbverlauf** hängt die Farbe von der Position ab:
Links (`x = 0`) ist der Rotanteil 0, rechts 255. Die Farbanteile müssen ganze Zahlen sein, deshalb `int()` bzw. `//`.

Bei großen Bildern ist `putpixel()` langsam. `pixel = bild.load()` liefert ein Objekt, mit dem `pixel[x, y] = farbe` schneller geht; hier reicht `putpixel()`.''',
     """from PIL import Image

bild = Image.new('RGB', (256, 100))
for x in range(256):
    for y in range(100):
        bild.putpixel((x, y), (x, 0, 255 - x))
bild""")

t('''Erzeuge einen waagerechten Verlauf von Schwarz nach Weiß (Grau mit dem Wert `x`) mit 256 × 50 Pixeln.''', P,
  """bild = Image.new('RGB', (256, 50))
for x in range(256):
    for y in range(50):
        bild.putpixel((x, y), (x, x, x))
bild""")
t('''Erzeuge einen **senkrechten** Verlauf mit 200 × 200 Pixeln: oben Blau `(0, 0, 255)`, unten Gelb `(255, 255, 0)`. Der Rot- und Grünanteil ist `y * 255 // 199`, der Blauanteil
`255` minus diesen Wert.''', P,
  """bild = Image.new('RGB', (200, 200))
for y in range(200):
    wert = y * 255 // 199
    for x in range(200):
        bild.putpixel((x, y), (wert, wert, 255 - wert))
bild""")
t('''Erzeuge ein Schachbrett mit 8 × 8 Feldern zu je 25 × 25 Pixeln (200 × 200 Pixel). Ein Feld ist schwarz, wenn `(x // 25 + y // 25) % 2 == 0`, sonst weiß.''', P,
  """bild = Image.new('RGB', (200, 200))
for x in range(200):
    for y in range(200):
        if (x // 25 + y // 25) % 2 == 0:
            bild.putpixel((x, y), (0, 0, 0))
        else:
            bild.putpixel((x, y), (255, 255, 255))
bild""")
t('''Erzeuge die Flagge von Deutschland mit 300 × 180 Pixeln: drei gleich hohe Streifen Schwarz, Rot `(221, 0, 0)` und Gold `(255, 206, 0)`.''', P,
  """bild = Image.new('RGB', (300, 180))
for y in range(180):
    if y < 60:
        farbe = (0, 0, 0)
    elif y < 120:
        farbe = (221, 0, 0)
    else:
        farbe = (255, 206, 0)
    for x in range(300):
        bild.putpixel((x, y), farbe)
bild""")
t('''Zeichne einen roten Kreis mit dem Radius 60 in die Mitte eines weißen 200 × 200-Bilds: Ein Pixel gehört zum Kreis, wenn `(x - 100)² + (y - 100)² <= 60²` ist.
Zähle die roten Pixel und vergleiche mit der Kreisfläche `π · 60²` (gerundet).''', P + '\nimport math',
  """bild = Image.new('RGB', (200, 200), 'white')
anzahl = 0
for x in range(200):
    for y in range(200):
        if (x - 100) ** 2 + (y - 100) ** 2 <= 60 ** 2:
            bild.putpixel((x, y), (255, 0, 0))
            anzahl += 1
print(anzahl, round(math.pi * 60 ** 2))
bild""")
t('''Erzeuge ein Bild mit 255 × 255 Pixeln, in dem der Rotanteil `x` und der Grünanteil `y` ist (Blau 0). Oben links ist es schwarz, unten rechts gelb.''', P,
  """bild = Image.new('RGB', (255, 255))
for x in range(255):
    for y in range(255):
        bild.putpixel((x, y), (x, y, 0))
bild""")
t('''Erzeuge ein Bild mit 200 × 200 Pixeln aus zufällig gefärbten Pixeln (`random.randint(0, 255)` für jeden Farbanteil, `random.seed(1)` vorher).
Es sieht aus wie das Rauschen eines alten Fernsehers.''', P + '\nimport random',
  """random.seed(1)
bild = Image.new('RGB', (200, 200))
for x in range(200):
    for y in range(200):
        bild.putpixel((x, y), (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))
bild""")
t('''Schreibe eine Funktion `streifen(breite, hoehe, farben)`, die ein Bild mit senkrechten, gleich breiten Streifen in den Farben der Liste `farben` zurückgibt.
Erzeuge damit die Flagge von Frankreich (`'#002395'`, `'white'`, `'#ed2939'`, 300 × 200) und die von Italien (`'#009246'`, `'white'`, `'#ce2b37'`).
`putpixel()` braucht ein Tupel, deshalb rechnest du die Farben mit `ImageColor.getrgb()` um.''', 'from PIL import Image, ImageColor' + N,
  """

def streifen(breite, hoehe, farben):
    bild = Image.new('RGB', (breite, hoehe))
    for x in range(breite):
        farbe = ImageColor.getrgb(farben[x * len(farben) // breite])
        for y in range(hoehe):
            bild.putpixel((x, y), farbe)
    return bild


nebeneinander([streifen(300, 200, ['#002395', 'white', '#ed2939']), streifen(300, 200, ['#009246', 'white', '#ce2b37'])])""")
predict("""from PIL import Image

bild = Image.new('RGB', (4, 1))
for x in range(4):
    bild.putpixel((x, 0), (x * 80, 0, 0))
print(bild.getpixel((3, 0)))
print(bild.getpixel((0, 0)))""", erklaerung='''Der Rotanteil ist `x · 80`: für `x = 3` also 240, für `x = 0` gleich 0. Ausgabe: `(240, 0, 0)` und `(0, 0, 0)`.''')

# ---------------------------------------------------------------- 4
sec('Modi: Graustufen und Transparenz')
expl('''#### `L`, `RGB` und `RGBA`

Der Modus bestimmt, was in einem Pixel steht:

| Modus | Pixel | Bedeutung |
|---|---|---|
| `'L'` | eine Zahl 0 bis 255 | Graustufen (*luminance*, Helligkeit) |
| `'RGB'` | Tupel mit 3 Zahlen | Farbe |
| `'RGBA'` | Tupel mit 4 Zahlen | Farbe und **Alpha** (Deckkraft: 0 durchsichtig, 255 deckend) |
| `'1'` | 0 oder 255 | nur Schwarz und Weiß |

`bild.convert('L')` wandelt in einen anderen Modus um, `bild.getbands()` gibt die Namen der **Kanäle** zurück. Graustufen berechnet Pillow mit
`L = 0.299·R + 0.587·G + 0.114·B`: Grün wirkt für das Auge heller als Rot und Blau.''',
     """from PIL import Image

farbig = Image.new('RGB', (100, 50), (255, 0, 0))
grau = farbig.convert('L')
print(farbig.getbands(), grau.getbands())
print(grau.getpixel((0, 0)))
print(Image.new('RGB', (1, 1), (0, 255, 0)).convert('L').getpixel((0, 0)))
grau""")

t('''Wandle die Farben Rot, Grün, Blau, Gelb und Weiß jeweils in Graustufen um (1 × 1-Bilder) und gib die Helligkeit aus.''', P,
  """for farbe in [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (255, 255, 255)]:
    print(farbe, Image.new('RGB', (1, 1), farbe).convert('L').getpixel((0, 0)))""")
t('''Erzeuge direkt ein Graustufenbild (`Image.new('L', (256, 50))`) mit einem Verlauf von Schwarz nach Weiß. Im Modus `L` ist jedes Pixel eine einzelne Zahl.''', P,
  """bild = Image.new('L', (256, 50))
for x in range(256):
    for y in range(50):
        bild.putpixel((x, y), x)
bild""")
t('''Öffne `bluete.png`, wandle es in Graustufen um und zeige beide Bilder (auf 320 × 213 verkleinert) nebeneinander an. Gib die Modi und die Farbe bzw. Helligkeit
des Pixels `(320, 213)` aus.''', P + N,
  """foto = Image.open('bluete.png')
grau = foto.convert('L')
print(foto.mode, grau.mode)
print(foto.getpixel((320, 213)), grau.getpixel((320, 213)))
nebeneinander([foto.resize((320, 213)), grau.resize((320, 213))])""")
t('''Wandle das Graustufen-Verlaufsbild in den Modus `'1'` (nur Schwarz und Weiß) um. Pillow verteilt dabei schwarze und weiße Punkte so, dass es von Weitem grau aussieht
(**Rastern**, *dithering*). Zeige das Ergebnis 2-fach vergrößert an.''', P,
  """bild = Image.new('L', (128, 40))
for x in range(128):
    for y in range(40):
        bild.putpixel((x, y), x * 2)
sw = bild.convert('1')
print(sw.mode, sw.getpixel((0, 0)), sw.getpixel((127, 0)))
sw.resize((256, 80), Image.NEAREST)""")
t('''Ein RGBA-Bild mit halbdurchsichtigem Rot: Erzeuge `Image.new('RGBA', (100, 100), (255, 0, 0, 128))`, gib seine Kanäle und ein Pixel aus und zeige es an. Vor dem Hintergrund
der Ausgabe wirkt es rosa, weil der Hintergrund durchscheint.''', P,
  """bild = Image.new('RGBA', (100, 100), (255, 0, 0, 128))
print(bild.getbands())
print(bild.getpixel((0, 0)))
bild""")
predict("""from PIL import Image

bild = Image.new('L', (3, 3), 100)
print(bild.getpixel((1, 1)))
print(bild.convert('RGB').getpixel((1, 1)))
print(len(bild.getbands()), len(bild.convert('RGBA').getbands()))""", erklaerung='''- Im Modus `L` ist ein Pixel eine Zahl: `100`.
- Beim Umwandeln nach RGB bekommen alle drei Anteile denselben Wert: `(100, 100, 100)`.
- `L` hat einen Kanal, `RGBA` vier: `1 4`.''')

# ---------------------------------------------------------------- 5
sec('Speichern und öffnen')
expl('''#### `save()` und `Image.open()`

- `bild.save('name.png')` speichert das Bild. Das Format ergibt sich aus der Dateiendung: `.png` (verlustfrei, gut für Grafiken), `.jpg` (verlustbehaftet, klein, gut für Fotos),
  `.gif`, `.bmp` u. a. Bei JPEG gibt `quality=...` (1 bis 95) die Qualität an.
- `Image.open('name.png')` öffnet eine Bilddatei. `bild.format` ist das Dateiformat.

In JupyterLite liegen die Dateien im Speicher des Browsers; in der Dateiliste links kannst du sie ansehen und herunterladen (Rechtsklick → *Download*).
JPEG kann keine Transparenz speichern; ein RGBA-Bild muss vorher mit `convert('RGB')` umgewandelt werden.''',
     """from PIL import Image

bild = Image.new('RGB', (100, 60), 'teal')
bild.save('tuerkis.png')
bild.save('tuerkis.jpg', quality=90)
for name in ['tuerkis.png', 'tuerkis.jpg']:
    geladen = Image.open(name)
    print(name, geladen.format, geladen.size, geladen.mode)""")

t('''Erzeuge ein rotes 50 × 50-Bild, speichere es als `rot.png` und als `rot.bmp`, öffne beide wieder und gib Format und Größe aus.''', P,
  """bild = Image.new('RGB', (50, 50), 'red')
bild.save('rot.png')
bild.save('rot.bmp')
for name in ['rot.png', 'rot.bmp']:
    geladen = Image.open(name)
    print(geladen.format, geladen.size)""")
t('''PNG ist verlustfrei, JPEG nicht: Speichere den Farbverlauf aus Abschnitt 3 (256 × 100, `(x, 0, 255 - x)`) als PNG und als JPEG mit `quality=10`, öffne beide und gib die
Farbe des Pixels `(100, 50)` aus. Beim PNG ist sie genau `(100, 0, 155)`.''', P,
  """bild = Image.new('RGB', (256, 100))
for x in range(256):
    for y in range(100):
        bild.putpixel((x, y), (x, 0, 255 - x))
bild.save('verlauf.png')
bild.save('verlauf.jpg', quality=10)
print(Image.open('verlauf.png').getpixel((100, 50)))
print(Image.open('verlauf.jpg').getpixel((100, 50)))""", kind='free')
t('''Öffne `pagode.png` und gib Format, Größe, Modus und die Anzahl der Pixel aus. Zeige das Foto an.''', P,
  """foto = Image.open('pagode.png')
print(foto.format, foto.size, foto.mode)
print(foto.width * foto.height)
foto""")
t('''Ein RGBA-Bild als JPEG speichern: Versuche es mit `Image.new('RGBA', (40, 40), (0, 0, 255, 100))` direkt (das gibt einen Fehler) und fange den Fehler mit `try`/`except OSError` ab.
Wandle das Bild danach in RGB um und speichere es als `blau.jpg`.''', P,
  """bild = Image.new('RGBA', (40, 40), (0, 0, 255, 100))
try:
    bild.save('blau.jpg')
except OSError:
    print('JPEG kann keine Transparenz speichern.')
bild.convert('RGB').save('blau.jpg')
print(Image.open('blau.jpg').mode)""")
predict("""from PIL import Image

Image.new('L', (30, 20), 0).save('schwarz.png')
bild = Image.open('schwarz.png')
print(bild.format, bild.mode, bild.size)""", erklaerung='''Das Bild wird als PNG gespeichert und wieder geöffnet. Format, Modus und Größe bleiben erhalten: `PNG L (30, 20)`.''')

# ---------------------------------------------------------------- 6
sec('Gemischte Übungen')
t('''Erzeuge die Flagge von Japan: weißes Bild 300 × 200 mit einem roten Kreis (`'#bc002d'`) in der Mitte, Radius 60.''', P,
  """bild = Image.new('RGB', (300, 200), 'white')
for x in range(300):
    for y in range(200):
        if (x - 150) ** 2 + (y - 100) ** 2 <= 60 ** 2:
            bild.putpixel((x, y), (188, 0, 45))
bild""")
t('''Erzeuge ein Bild mit 200 × 200 Pixeln mit **Ringen**: Die Farbe hängt vom Abstand `d` des Pixels zur Mitte ab; ist `int(d) // 10` gerade, ist das Pixel blau, sonst weiß.
Den Abstand berechnest du mit `math.sqrt()` oder `math.dist()`.''', P + '\nimport math',
  """bild = Image.new('RGB', (200, 200))
for x in range(200):
    for y in range(200):
        d = math.dist((x, y), (100, 100))
        if int(d) // 10 % 2 == 0:
            bild.putpixel((x, y), (0, 0, 200))
        else:
            bild.putpixel((x, y), (255, 255, 255))
bild""")
t('''Erzeuge ein Bild mit 256 × 256 Pixeln, in dem jedes Pixel die Farbe `(x * y % 256, x, 255 - y)` hat. Durch den Modulo-Operator entsteht ein
überraschendes Muster aus Bögen.''', P,
  """bild = Image.new('RGB', (256, 256))
for x in range(256):
    for y in range(256):
        bild.putpixel((x, y), (x * y % 256, x, 255 - y))
bild""")
t('''Zähle im Foto `bluete.png` die Pixel, deren Rotanteil größer ist als Grün- und Blauanteil zusammen („sehr rote“ Pixel), und gib die Anzahl und ihren Anteil an
allen Pixeln aus (3 Nachkommastellen). Das dauert ein paar Sekunden.''', P,
  """foto = Image.open('bluete.png')
anzahl = 0
for x in range(foto.width):
    for y in range(foto.height):
        r, g, b = foto.getpixel((x, y))
        if r > g + b:
            anzahl += 1
print(anzahl)
print(f'{anzahl / (foto.width * foto.height):.3f}')""")
t('''Gestalte ein eigenes Bild mit Schleifen und Bedingungen (z. B. eine andere Flagge, ein Muster, ein Pixel-Kunstwerk) und speichere es als PNG.''', '',
  """from PIL import Image

bild = Image.new('RGB', (300, 200), 'white')
for x in range(300):
    for y in range(200):
        if abs(x - 150) + abs(y - 100) < 80:
            bild.putpixel((x, y), (x % 256, y, 150))
bild.save('raute.png')
bild""", kind='free')

generate('pillow_grundlagen', 'Pillow 1: Grundlagen', INTRO, ausfuehren=pandasnb.ausfuehrung(), ausgabe_markdown=True, dateien=FOTOS)
