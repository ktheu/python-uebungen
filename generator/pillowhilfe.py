"""Gemeinsames für die Pillow-Notebooks (gen_pillow_*.py)."""
import re

from nbgen import task


def t(text, given='', body='', kind='normal'):
    """Aufgabe, deren Lösung aus dem vorgegebenen Code plus body besteht."""
    given = re.sub(r'\n{3,}', '\n\n', given)  # höchstens eine Leerzeile
    loesung = (given + '\n' + body) if given else body
    task(text, given=given, solution=re.sub(r'\n{3,}', '\n\n', loesung), kind=kind)


REIHE = '''Die Reihe hat vier Notebooks:

1. Grundlagen: Bilder erzeugen, Pixel, Farben, Speichern und Öffnen
2. Zeichnen: Formen, Text, Grafiken mit Schleifen und Funktionen
3. Bearbeiten: Ausschneiden, Drehen, Filter, Helligkeit, Collagen, animierte GIFs
4. Pixel: Bildverarbeitung selbst programmieren, mit Schleifen und mit numpy'''


def reihe(nr):
    """Liste der Notebooks, das aktuelle fett und mit dem Zusatz (dieses Notebook)."""
    zeilen = REIHE.split('\n')
    i = 1 + nr
    name, rest = zeilen[i][3:].split(':', 1)
    zeilen[i] = f'{nr}. **{name}**:{rest} (dieses Notebook)'
    return '\n'.join(zeilen)


ANZEIGEN = '''**Bilder anzeigen:** Steht ein Bild in der **letzten Zeile** einer Zelle, zeigt JupyterLab es an. Mehrere Bilder in einer Zelle zeigt man mit `display(bild)` an.
Die erwarteten Ausgaben zeigen die Bilder höchstens 320 Pixel groß; große Bilder (Fotos) sind dort verkleinert.'''

SCHLUSS = '''Jeder Abschnitt beginnt mit kurzen Erklärungen und Beispielen. Führe die Beispiele aus und probiere sie ruhig ein wenig aus.
Danach folgen viele kleine Übungen. Wenn etwas vorgegeben ist, steht es schon in der Codezelle.'''

# Setup-Zelle für alle Pillow-Notebooks: Im Kernel von JupyterLite (pyodide_kernel 0.8.6) zeigt display(bild) ein leeres Bild,
# weil display() die PNG-Bytes von Pillow nicht in Base64 umwandelt (nur die letzte Zeile tut das). Liefert der Formatter selbst
# Base64-Text, funktioniert beides. Außerhalb von Jupyter (Generator, Pyodide-Check) ist get_ipython() None, dann passiert nichts.
ANZEIGE = """import base64
import io
from IPython import get_ipython
from PIL import Image

def als_png(bild):
    puffer = io.BytesIO()
    bild.save(puffer, 'PNG')
    return base64.b64encode(puffer.getvalue()).decode('ascii')

def kein_jpeg(bild):
    return None

ipython = get_ipython()
if ipython is not None:
    ipython.display_formatter.formatters['image/png'].for_type(Image.Image, als_png)
    ipython.display_formatter.formatters['image/jpeg'].for_type(Image.Image, kein_jpeg)
print('Bereit: Bilder werden auch mit display() angezeigt.')"""

ANZEIGE_MD = '''#### Bildanzeige einrichten

**Führe diese Zelle zuerst aus** (nach jedem Neustart des Kernels wieder). Im Browser-Python von JupyterLite zeigt `display(bild)` sonst nur ein leeres Bild an;
die Zelle sorgt dafür, dass Pillow-Bilder dort richtig übertragen werden. Wie sie funktioniert, musst du nicht verstehen.'''

# Die beiden Fotos liegen als PNG in content/ (einmal lokal aus scikit-learn dekodiert, damit die Pixel überall gleich sind).
# Generatoren, die sie öffnen, übergeben generate(..., dateien=FOTOS).
FOTOS = ['pagode.png', 'bluete.png']

FOTOS_MD = '''**Fotos:** Neben den Notebooks liegen zwei Fotos mit je 640 × 427 Pixeln: `pagode.png` (ein chinesischer Tempel) und `bluete.png` (eine Blüte).
Fotos: Daniel Buechele, [CC BY 2.0](https://creativecommons.org/licenses/by/2.0/), aus dem Paket scikit-learn.
Eigene Fotos kannst du mit dem Pfeil-Symbol über der Dateiliste links hochladen und dann mit `Image.open('dateiname.jpg')` öffnen.'''
