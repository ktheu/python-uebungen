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


ANZEIGEN = '''**Bilder anzeigen:** Steht ein Bild in der **letzten Zeile** einer Zelle, zeigt JupyterLab es an. Jede Zelle zeigt so ein Bild.
Mehrere Bilder setzt die Funktion `nebeneinander()` zu einem zusammen (erklärt in *Pillow: Grundlagen*; in den Aufgaben steht sie schon in der Zelle).
(`display(bild)` zeigt Pillow-Bilder im Browser-Python von JupyterLite leider nur leer an.)
Die erwarteten Ausgaben zeigen die Bilder höchstens 320 Pixel groß; große Bilder (Fotos) sind dort verkleinert.'''

SCHLUSS = '''Jeder Abschnitt beginnt mit kurzen Erklärungen und Beispielen. Führe die Beispiele aus und probiere sie ruhig ein wenig aus.
Danach folgen viele kleine Übungen. Wenn etwas vorgegeben ist, steht es schon in der Codezelle.'''

# display() zeigt Pillow-Bilder im Kernel von JupyterLite (pyodide_kernel 0.8.6) als leeres Bild (auch ein eigener image/png-Formatter
# hilft nicht). Deshalb zeigt jede Zelle nur ein Bild, das in der letzten Zeile; mehrere Bilder setzt nebeneinander() zu einem zusammen.
# Jede Zelle, die es benutzt, enthält die Definition (die Zellen werden beim Prüfen einzeln ausgeführt).
NEBEN = """def nebeneinander(bilder):
    \"\"\"Setzt mehrere Bilder mit 10 Pixeln Abstand nebeneinander zu einem Bild zusammen.\"\"\"
    gesamt = Image.new('RGB', (sum([b.width + 10 for b in bilder]) - 10, max([b.height for b in bilder])), 'lightgray')
    x = 0
    for b in bilder:
        gesamt.paste(b, (x, 0))
        x += b.width + 10
    return gesamt"""
N = '\n\n' + NEBEN  # an vorgegebenen Code anhängen

# Die beiden Fotos liegen als PNG in content/ (einmal lokal aus scikit-learn dekodiert, damit die Pixel überall gleich sind).
# Generatoren, die sie öffnen, übergeben generate(..., dateien=FOTOS).
FOTOS = ['pagode.png', 'bluete.png']

FOTOS_MD = '''**Fotos:** Neben den Notebooks liegen zwei Fotos mit je 640 × 427 Pixeln: `pagode.png` (ein chinesischer Tempel) und `bluete.png` (eine Blüte).
Fotos: Daniel Buechele, [CC BY 2.0](https://creativecommons.org/licenses/by/2.0/), aus dem Paket scikit-learn.
Eigene Fotos kannst du mit dem Pfeil-Symbol über der Dateiliste links hochladen und dann mit `Image.open('dateiname.jpg')` öffnen.'''
