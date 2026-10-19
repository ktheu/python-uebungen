# Erzeugt ../content/numpy_mathe.ipynb (siehe nbgen.py).
#
# Braucht numpy in derselben Version wie Pyodide in JupyterLite (zurzeit 2.4.6), siehe gen_numpy_grundlagen.py:
#     py -3.13 -W error generator/gen_numpy_mathe.py
#     py -3.13 generator/pyodide_check/pruefen.py generator/gen_numpy_mathe.py
#
# Fallstricke:
# - Ergebnisse von solve(), det(), inv(), roots(), polyfit() hängen in den letzten Stellen von der LAPACK-Bibliothek ab.
#   Deshalb immer runden. Beim Runden sehr kleiner negativer Zahlen entsteht -0. -> Daten so wählen, dass das nicht vorkommt.
# - np.roots(): Reihenfolge nicht festgelegt -> immer np.sort(). Keine doppelten Nullstellen (sonst komplexe Rundungsreste).
# - In Pyodide wirft np.linalg bei singulären Matrizen KEINEN LinAlgError (solve/inv liefern nan oder riesige Zahlen,
#   det() ist nur fast 0). Deshalb wird vorher die gerundete Determinante geprüft, kein try/except LinAlgError.
# - Die Beispieldateien legt die Setup-Zelle an (wie in gen_dateien.py).
from nbgen import sec, expl, task, predict, generate, setup


def t(text, given='', body='', kind='normal'):
    """Aufgabe, deren Lösung aus dem vorgegebenen Code plus body besteht."""
    task(text, given=given, solution=(given + '\n' + body) if given else body, kind=kind)


NP = 'import numpy as np'

INTRO = '''numpy ist auch ein Werkzeug für die **Mathematik**: Vektoren und Matrizen multiplizieren, lineare Gleichungssysteme lösen,
mit Polynomen rechnen (Nullstellen, Ableitungen, Extremstellen), Flächen berechnen und Regressionsgeraden durch Messwerte legen.
Vieles davon kennst du aus dem Mathematikunterricht. Hier lässt du den Computer rechnen.

Vorausgesetzt werden die Notebooks *numpy: Grundlagen*, *numpy: Filtern und Auswählen* und *numpy: Zweidimensionale Arrays*.
Für den letzten Abschnitt ist das Notebook *Dateien lesen* hilfreich.

Jeder Abschnitt beginnt mit kurzen Erklärungen und Beispielen. Führe die Beispiele aus und probiere sie ruhig ein wenig aus.
Danach folgen viele kleine Übungen. Wenn etwas vorgegeben ist, steht es schon in der Codezelle.

Der Computer rechnet mit Kommazahlen nicht ganz exakt: Statt `2` kommt manchmal `1.9999999999999998` heraus.
Deshalb wird in vielen Aufgaben mit `np.round()` gerundet.'''

setup('''#### Beispieldateien anlegen

**Führe diese Zelle zuerst aus.** Sie legt im aktuellen Ordner die Dateien an, die im Abschnitt *Daten aus Dateien* gebraucht werden.''',
      r"""dateien = {
    'abkuehlung.csv': 'minute,temperatur\n0,90.0\n1,82.1\n2,75.0\n3,68.6\n4,62.9\n5,57.7\n6,53.1\n7,48.9\n8,45.1\n9,41.7\n10,38.6\n',
    'lernzeit.csv': 'stunden;punkte\n1;35\n2;41\n2;46\n3;50\n4;58\n5;61\n5;67\n6;70\n7;76\n8;80\n',
    'wetter.csv': 'tag,tmin,tmax,regen\nMo,4.5,11.0,0.0\nDi,6.0,13.5,2.5\nMi,3.5,9.0,8.0\nDo,2.0,8.5,1.0\nFr,5.5,14.0,0.0\nSa,7.0,16.5,0.0\nSo,6.5,12.0,4.5\n',
    'gleichungen.txt': '2 1 -1 8\n-3 -1 2 -11\n-2 1 2 -3\n',
    'matrix.txt': '1 2 3\n0 1 4\n5 6 0\n',
}
for name, inhalt in dateien.items():
    with open(name, 'w', encoding='utf-8') as f:
        f.write(inhalt)
print('Angelegt:', ', '.join(dateien))""")

# ---------------------------------------------------------------- 1
sec('Vektoren')
expl('''#### Arrays als Vektoren

Ein eindimensionales Array kann man als **Vektor** auffassen. Addition, Subtraktion und Multiplikation mit einer Zahl
funktionieren elementweise, also genau wie in der Mathematik.

- Das **Skalarprodukt** `a · b = a₁b₁ + a₂b₂ + ...` berechnet man mit `a @ b` oder `np.dot(a, b)`.
- Die **Länge** (der Betrag) `|a|` ist `np.linalg.norm(a)`, also `√(a · a)`.
- Der **Abstand** zweier Punkte `p` und `q` ist die Länge von `q - p`.

Das Modul `np.linalg` (*lineare Algebra*) enthält die Funktionen für Vektoren und Matrizen.''',
     """import numpy as np

a = np.array([1, 2, 2])
b = np.array([3, 0, 4])
print(a + b)
print(2 * a - b)
print(a @ b)
print(np.dot(a, b))
print(np.linalg.norm(a))
print(np.linalg.norm(b - a))""")
expl('''#### Winkel und Kreuzprodukt

Für den Winkel `α` zwischen zwei Vektoren gilt `cos(α) = (a · b) / (|a| · |b|)`.

- `np.arccos(x)` berechnet den Winkel im Bogenmaß, `np.degrees()` rechnet ins Gradmaß um.
- Ist das Skalarprodukt 0, stehen die Vektoren **senkrecht** (orthogonal) aufeinander.
- `np.cross(a, b)` ist das **Kreuzprodukt** zweier Vektoren im Raum. Es steht senkrecht auf beiden.''',
     """import numpy as np

a = np.array([1, 0, 0])
b = np.array([1, 1, 0])
cos_alpha = a @ b / (np.linalg.norm(a) * np.linalg.norm(b))
print(np.round(np.degrees(np.arccos(cos_alpha)), 2))
n = np.cross(a, b)
print(n)
print(n @ a, n @ b)""")

V = NP + '\na = np.array([2, -1, 3])\nb = np.array([1, 4, 2])'
t('Gib `a + b`, `a - b` und `3 * a` aus.', V, """print(a + b)
print(a - b)
print(3 * a)""")
t('Gib das Skalarprodukt von `a` und `b` aus, einmal mit `@` und einmal mit `np.sum(a * b)`.', V,
  """print(a @ b)
print(np.sum(a * b))""")
t('Gib die Länge von `a` aus, einmal mit `np.linalg.norm()` und einmal mit `np.sqrt()` und dem Skalarprodukt. Runde auf drei Nachkommastellen.', V,
  """print(np.round(np.linalg.norm(a), 3))
print(np.round(np.sqrt(a @ a), 3))""")
t('Gib den Abstand der Punkte `P` und `Q` aus.',
  NP + '\nP = np.array([1, 2, 3])\nQ = np.array([4, 6, 3])',
  """print(np.linalg.norm(Q - P))""")
t('Gib den Mittelpunkt der Strecke von `P` nach `Q` aus.',
  NP + '\nP = np.array([1, 2, 3])\nQ = np.array([4, 6, 3])',
  """print((P + Q) / 2)""")
t('Prüfe für jedes Paar, ob die Vektoren senkrecht aufeinander stehen (Skalarprodukt 0).',
  NP + '\npaare = [(np.array([1, 2]), np.array([-2, 1])), (np.array([3, 1, 2]), np.array([1, 1, -2])), (np.array([1, 1, 1]), np.array([1, 2, 3]))]',
  """for u, v in paare:
    print(u @ v == 0)""")
t('Gib den Winkel zwischen `u` und `v` in Grad aus, gerundet auf zwei Nachkommastellen.',
  NP + '\nu = np.array([3, 4])\nv = np.array([4, 3])',
  """cos_alpha = u @ v / (np.linalg.norm(u) * np.linalg.norm(v))
print(np.round(np.degrees(np.arccos(cos_alpha)), 2))""")
t('Bringe `v` auf die Länge 1 (Einheitsvektor), indem du durch die Länge teilst. Gib den Vektor und zur Kontrolle seine Länge aus.',
  NP + '\nv = np.array([2, 3, 6])',
  """e = v / np.linalg.norm(v)
print(np.round(e, 4))
print(np.round(np.linalg.norm(e), 4))""")
t('Gib das Kreuzprodukt von `a` und `b` aus und prüfe mit dem Skalarprodukt, dass es auf beiden senkrecht steht.', V,
  """n = np.cross(a, b)
print(n)
print(n @ a, n @ b)""")
t('Berechne den Flächeninhalt des Dreiecks `ABC` im Raum: die halbe Länge des Kreuzprodukts von `B - A` und `C - A`.',
  NP + '\nA = np.array([0, 0, 0])\nB = np.array([4, 0, 0])\nC = np.array([0, 3, 0])',
  """print(np.linalg.norm(np.cross(B - A, C - A)) / 2)""")
t('Ein Rundweg führt nacheinander durch die Punkte in `punkte` und zurück zum Start. Berechne seine Länge. Tipp: `np.vstack([punkte, punkte[:1]])` und `np.diff(..., axis=0)`.',
  NP + '\npunkte = np.array([[0, 0], [3, 0], [3, 4], [0, 4]])',
  """weg = np.vstack([punkte, punkte[:1]])
schritte = np.diff(weg, axis=0)
print(np.linalg.norm(schritte, axis=1).sum())""")
predict("""import numpy as np
a = np.array([1, 2])
b = np.array([3, 4])
print(a @ b)
print(a * b)
print(np.linalg.norm(np.array([3, 4])))
print(np.cross(np.array([1, 0, 0]), np.array([0, 1, 0])))""")

# ---------------------------------------------------------------- 2
sec('Matrizen multiplizieren')
expl('''#### `@` ist die Matrizenmultiplikation

Bei 2D-Arrays ist `A * B` die **elementweise** Multiplikation. Die **Matrizenmultiplikation** aus der Mathematik schreibt man `A @ B`:
Das Element in Zeile `i` und Spalte `j` von `A @ B` ist das Skalarprodukt von Zeile `i` von `A` und Spalte `j` von `B`.

- Die Spaltenzahl von `A` muss gleich der Zeilenzahl von `B` sein: `(m × n) @ (n × k)` ergibt `(m × k)`. Sonst gibt es einen `ValueError`.
- `A @ B` ist meist **nicht** gleich `B @ A`.
- `A @ v` mit einem Vektor `v` ergibt einen Vektor.
- `np.eye(n)` ist die Einheitsmatrix: `A @ np.eye(n)` ist wieder `A`.
- `np.linalg.matrix_power(A, k)` ist `A @ A @ ... @ A` (`k`-mal).''',
     """import numpy as np

A = np.array([[1, 2],
              [3, 4]])
B = np.array([[0, 1],
              [1, 0]])
print(A * B)
print(A @ B)
print(B @ A)
print(A @ np.array([1, 1]))
print(np.linalg.matrix_power(A, 3))""")
expl('''#### Anwendung: Bedarfsmatrizen

Eine Firma stellt aus **Rohstoffen** **Produkte** her. Die Bedarfsmatrix gibt an, wie viele Einheiten jedes Rohstoffs (Zeilen)
für ein Stück jedes Produkts (Spalten) gebraucht werden. Der Vektor `stueck` gibt an, wie viele Stück von jedem Produkt gefertigt werden.
Dann ist `bedarf @ stueck` der Gesamtbedarf an Rohstoffen.''',
     """import numpy as np

# Zeilen: Holz, Schrauben, Lack; Spalten: Stuhl, Tisch
bedarf = np.array([[ 4, 10],
                   [12, 20],
                   [ 1,  3]])
stueck = np.array([20, 5])
print(bedarf @ stueck)""")
expl('''#### Anwendung: Übergangsmatrizen

Eine Übergangsmatrix `M` beschreibt, wie sich eine Verteilung von einem Schritt zum nächsten ändert.
Das Element `M[i, j]` ist der Anteil, der von Zustand `j` nach Zustand `i` wechselt. Jede Spalte hat die Summe 1.
Mit der Verteilung `v` ist `M @ v` die Verteilung nach einem Schritt, `matrix_power(M, n) @ v` nach `n` Schritten.''',
     """import numpy as np

# Zwei Handy-Anbieter A und B: Jeden Monat bleiben 80 % bei A, 20 % wechseln zu B; von B wechseln 30 % zu A.
M = np.array([[0.8, 0.3],
              [0.2, 0.7]])
v = np.array([1000, 0])
print(M @ v)
print(M @ (M @ v))
print(np.round(np.linalg.matrix_power(M, 50) @ v, 1))""")

AB = NP + '\nA = np.array([[2, 1],\n              [0, 3]])\nB = np.array([[1, 4],\n              [2, 1]])'
t('Gib `A @ B` und `B @ A` aus.', AB, """print(A @ B)
print(B @ A)""")
t('Gib `A * B` (elementweise) und `A @ B` aus.', AB, """print(A * B)
print(A @ B)""")
t('Gib `A @ v` aus.', AB + '\nv = np.array([3, -1])', """print(A @ v)""")
t('Prüfe mit `np.array_equal()`, ob `A @ np.eye(2)` gleich `A` ist.', AB, """print(np.array_equal(A @ np.eye(2), A))""")
t('Gib `A` hoch 4 aus, einmal mit `@` und einmal mit `np.linalg.matrix_power()`.', AB,
  """print(A @ A @ A @ A)
print(np.linalg.matrix_power(A, 4))""")
t('Multipliziere die 2 × 3-Matrix `C` mit der 3 × 2-Matrix `D`. Gib das Ergebnis und seine Form aus, danach die Form von `D @ C`.',
  NP + '\nC = np.array([[1, 0, 2],\n              [3, 1, 0]])\nD = np.array([[1, 2],\n              [0, 1],\n              [4, 0]])',
  """print(C @ D)
print((C @ D).shape)
print((D @ C).shape)""")
t('Berechne `C @ D` ohne `@`: Fülle eine 2 × 2-Matrix mit zwei Schleifen, das Element `[i, j]` ist das Skalarprodukt von Zeile `i` von `C` und Spalte `j` von `D`.',
  NP + '\nC = np.array([[1, 0, 2],\n              [3, 1, 0]])\nD = np.array([[1, 2],\n              [0, 1],\n              [4, 0]])',
  """E = np.zeros((2, 2), dtype=int)
for i in range(2):
    for j in range(2):
        E[i, j] = C[i] @ D[:, j]
print(E)""")
t('''Eine Bäckerei braucht für ein Brot 500 g Mehl, 10 g Hefe und 300 ml Wasser, für ein Brötchen 60 g Mehl, 2 g Hefe und 35 ml Wasser.
Stelle die Bedarfsmatrix auf (Zeilen: Mehl, Hefe, Wasser; Spalten: Brot, Brötchen) und berechne den Bedarf für 40 Brote und 300 Brötchen.''',
  NP, """bedarf = np.array([[500, 60],
                   [ 10,  2],
                   [300, 35]])
print(bedarf @ np.array([40, 300]))""")
t('''Zweistufige Produktion: `RZ` gibt an, wie viele Rohstoffe für ein Zwischenprodukt gebraucht werden, `ZE` wie viele Zwischenprodukte für ein Endprodukt.
Berechne die Matrix `RE = RZ @ ZE` (Rohstoffe pro Endprodukt) und den Rohstoffbedarf für 10 Stück von E1 und 20 Stück von E2.''',
  NP + '\nRZ = np.array([[2, 1],\n               [1, 3],\n               [0, 2]])\nZE = np.array([[1, 2],\n               [3, 1]])',
  """RE = RZ @ ZE
print(RE)
print(RE @ np.array([10, 20]))""")
t('''Ein Würfelkäfer durchläuft die Stadien Ei, Larve und Käfer. Die Übergangsmatrix beschreibt einen Monat: Aus jedem Käfer entstehen 6 Eier,
die Hälfte der Eier wird zur Larve, ein Drittel der Larven wird zum Käfer. Berechne die Population nach 1, 2 und 3 Monaten, Start mit `v`.''',
  NP + '\nM = np.array([[0,   0,   6],\n              [0.5, 0,   0],\n              [0,   1/3, 0]])\nv = np.array([120, 60, 30])',
  """for monat in range(1, 4):
    v = M @ v
    print(monat, np.round(v, 1))""")
t('''Verwende die Anbieter-Matrix aus dem Beispiel. Am Anfang haben A 300 und B 700 Kunden. Gib die Verteilung nach 1, 2, 5 und 20 Monaten aus (eine Nachkommastelle).''',
  NP + '\nM = np.array([[0.8, 0.3],\n              [0.2, 0.7]])\nv = np.array([300, 700])',
  """for n in [1, 2, 5, 20]:
    print(n, np.round(np.linalg.matrix_power(M, n) @ v, 1))""")
t('Prüfe, ob alle Spaltensummen der Übergangsmatrix 1 sind (runde vorher auf 10 Nachkommastellen).',
  NP + '\nM = np.array([[0.5, 0.2, 0.1],\n              [0.3, 0.7, 0.3],\n              [0.2, 0.1, 0.6]])',
  """print((np.round(M.sum(axis=0), 10) == 1).all())""")
predict("""import numpy as np
A = np.array([[1, 1], [0, 1]])
print(A @ A)
print(A * A)
print(np.linalg.matrix_power(A, 5))
print((A @ np.array([2, 3])).shape)""")
predict("""import numpy as np
A = np.ones((2, 3))
B = np.ones((2, 3))
print(A @ B)""", error=ValueError)

# ---------------------------------------------------------------- 3
sec('Lineare Gleichungssysteme')
expl('''#### `np.linalg.solve()`

Ein lineares Gleichungssystem wie

```
2x +  y = 5
 x - 3y = -1
```

schreibt man als `A · x = b` mit der Koeffizientenmatrix `A` und dem Vektor `b` der rechten Seiten.
`np.linalg.solve(A, b)` gibt die Lösung `x` zurück.

Zur Kontrolle setzt man ein: `A @ x` muss `b` ergeben. Wegen der Rundungsfehler vergleicht man mit `np.allclose(A @ x, b)`,
das kleine Abweichungen erlaubt. Für einzelne Zahlen gibt es `np.isclose(a, b)`.''',
     """import numpy as np

A = np.array([[2, 1],
              [1, -3]])
b = np.array([5, -1])
x = np.linalg.solve(A, b)
print(x)
print(A @ x)
print(np.allclose(A @ x, b))""")
expl('''#### Wenn es keine eindeutige Lösung gibt

Hat das Gleichungssystem keine oder unendlich viele Lösungen, ist die Matrix **singulär**. Man erkennt das an der
**Determinante** `np.linalg.det(A)`: Sie ist dann 0 (mehr zur Determinante im nächsten Abschnitt).
Wegen der Rundungsfehler kommt oft nur fast 0 heraus, deshalb rundet man vor dem Vergleich.

Prüfe das **vor** dem Lösen. Auf manchen Rechnern meldet `solve()` bei einer singulären Matrix einen Fehler (`LinAlgError`),
hier im Browser aber nicht: Dann kommen unsinnige Ergebnisse wie `nan` (*not a number*) oder riesige Zahlen heraus.''',
     """import numpy as np

A = np.array([[1, 2],
              [2, 4]])
b = np.array([3, 6])
print(np.round(np.linalg.det(A), 9))
if np.round(np.linalg.det(A), 9) == 0:
    print('keine eindeutige Lösung')
else:
    print(np.linalg.solve(A, b))""")

t('''Löse das Gleichungssystem und gib die Lösung aus (gerundet auf zwei Nachkommastellen).
```
3x + 2y = 12
 x -  y = -1
```''', NP, """A = np.array([[3, 2],
              [1, -1]])
b = np.array([12, -1])
print(np.round(np.linalg.solve(A, b), 2))""")
t('''Löse das Gleichungssystem, gib die Lösung aus und prüfe sie mit `np.allclose()`.
```
 x + y + z = 6
2x - y + z = 3
 x + 2y - z = 2
```''', NP, """A = np.array([[1, 1, 1],
              [2, -1, 1],
              [1, 2, -1]])
b = np.array([6, 3, 2])
x = np.linalg.solve(A, b)
print(np.round(x, 2))
print(np.allclose(A @ x, b))""")
t('''Für ein Konzert wurden 400 Karten verkauft, Erwachsene zahlen 25 Euro, Schüler 15 Euro. Die Einnahmen waren 8200 Euro.
Wie viele Karten jeder Sorte wurden verkauft? Stelle das Gleichungssystem auf und löse es.''', NP,
  """A = np.array([[1, 1],
              [25, 15]])
b = np.array([400, 8200])
print(np.round(np.linalg.solve(A, b)))""")
t('''Ein Vater ist heute dreimal so alt wie sein Sohn. In 12 Jahren ist er nur noch doppelt so alt.
Löse das Gleichungssystem `v = 3s` und `v + 12 = 2(s + 12)` (umgestellt: `v - 3s = 0` und `v - 2s = 12`).''', NP,
  """A = np.array([[1, -3],
              [1, -2]])
b = np.array([0, 12])
print(np.round(np.linalg.solve(A, b)))""")
t('''Bestimme die Parabel `f(x) = ax² + bx + c` durch die Punkte (1, 2), (2, 3) und (3, 6).
Jeder Punkt liefert eine Gleichung `a·x² + b·x + c = y`. Gib `a`, `b` und `c` aus.''', NP,
  """x = np.array([1, 2, 3])
y = np.array([2, 3, 6])
A = np.vstack([x ** 2, x, np.ones(3)]).T
print(np.round(np.linalg.solve(A, y), 2))""")
t('''Ein Händler mischt zwei Teesorten zu 10 kg einer Mischung für 18 Euro pro kg. Sorte A kostet 15 Euro pro kg, Sorte B 22.50 Euro pro kg.
Wie viele kg jeder Sorte braucht er?''', NP,
  """A = np.array([[1, 1],
              [15, 22.5]])
b = np.array([10, 180])
print(np.round(np.linalg.solve(A, b), 2))""")
t('Prüfe für jedes Gleichungssystem `A · x = b` mit der gerundeten Determinante, ob es eine eindeutige Lösung hat. Gib die Lösung aus (zwei Nachkommastellen) oder `keine eindeutige Lösung`.',
  NP + '\nsysteme = [(np.array([[1, 2], [3, 4]]), np.array([5, 6])),\n           (np.array([[2, 4], [1, 2]]), np.array([6, 3])),\n           (np.array([[1, 1], [1, -1]]), np.array([10, 2]))]',
  """for A, b in systeme:
    if np.round(np.linalg.det(A), 9) == 0:
        print('keine eindeutige Lösung')
    else:
        print(np.round(np.linalg.solve(A, b), 2))""")
t('''Bestimme die **stationäre Verteilung** der Anbieter-Matrix: die Verteilung `x`, die sich nicht mehr ändert (`M @ x = x`), mit 1000 Kunden insgesamt.
Das Gleichungssystem ist `(M - I) x = 0`. Ersetze die letzte Gleichung durch `x₁ + x₂ = 1000`.''',
  NP + '\nM = np.array([[0.8, 0.3],\n              [0.2, 0.7]])',
  """A = M - np.eye(2)
A[-1] = [1, 1]
b = np.array([0, 1000])
print(np.round(np.linalg.solve(A, b), 1))""")
t('Löse das Gleichungssystem, das in der Datei `gleichungen.txt` steht (die letzte Spalte ist die rechte Seite). Lies die Datei mit `np.loadtxt()` (mehr dazu in Abschnitt 8).',
  NP, """daten = np.loadtxt('gleichungen.txt', encoding='utf-8')
A = daten[:, :-1]
b = daten[:, -1]
print(np.round(np.linalg.solve(A, b), 2))""")
predict("""import numpy as np
A = np.array([[1, 0], [0, 2]])
print(np.linalg.solve(A, np.array([3, 4])))
print(np.allclose(0.1 + 0.2, 0.3))
print(0.1 + 0.2 == 0.3)""")

# ---------------------------------------------------------------- 4
sec('Determinante und Inverse')
expl('''#### `np.linalg.det()` und `np.linalg.inv()`

- `np.linalg.det(A)` ist die **Determinante** einer quadratischen Matrix. Für eine 2 × 2-Matrix ist sie `a·d - b·c`.
  Ist die Determinante 0, ist die Matrix singulär (nicht invertierbar).
- `np.linalg.inv(A)` ist die **inverse Matrix** `A⁻¹`. Es gilt `A @ inv(A) = I` (Einheitsmatrix).
  Damit ist die Lösung von `A · x = b` auch `inv(A) @ b`. `solve()` ist aber genauer und schneller.

Beide rechnen mit Kommazahlen. Deshalb sollte man das Ergebnis runden.

`np.column_stack([u, v])` setzt Vektoren als **Spalten** zu einer Matrix zusammen (wie `np.vstack([u, v]).T`).''',
     """import numpy as np

A = np.array([[4, 7],
              [2, 6]])
print(np.linalg.det(A))
print(np.round(np.linalg.det(A), 6))
A_inv = np.linalg.inv(A)
print(A_inv)
print(np.round(A @ A_inv, 6))""")

t('Gib die Determinante von `A` aus, einmal mit `np.linalg.det()` (gerundet auf 6 Stellen) und einmal mit der Formel `a·d - b·c`.',
  NP + '\nA = np.array([[3, 8],\n              [4, 6]])',
  """print(np.round(np.linalg.det(A), 6))
print(A[0, 0] * A[1, 1] - A[0, 1] * A[1, 0])""")
t('Gib die Determinante der 3 × 3-Matrix aus der Datei `matrix.txt` aus, gerundet auf 6 Stellen.',
  NP, """M = np.loadtxt('matrix.txt', encoding='utf-8')
print(np.round(np.linalg.det(M), 6))""")
t('Gib die Inverse von `A` aus (gerundet auf 4 Stellen) und prüfe mit `np.allclose()`, dass `A @ inv(A)` die Einheitsmatrix ist.',
  NP + '\nA = np.array([[2, 1],\n              [5, 3]])',
  """A_inv = np.linalg.inv(A)
print(np.round(A_inv, 4))
print(np.allclose(A @ A_inv, np.eye(2)))""")
t('Gib die Inverse der Matrix aus `matrix.txt` aus, gerundet auf zwei Nachkommastellen.',
  NP, """M = np.loadtxt('matrix.txt', encoding='utf-8')
print(np.round(np.linalg.inv(M), 2))""")
t('Löse `A · x = b` mit der Inversen und vergleiche mit `solve()`. Gib beide Lösungen gerundet auf zwei Nachkommastellen aus.',
  NP + '\nA = np.array([[2, 1],\n              [5, 3]])\nb = np.array([4, 11])',
  """print(np.round(np.linalg.inv(A) @ b, 2))
print(np.round(np.linalg.solve(A, b), 2))""")
t('Gib für jede Matrix `invertierbar` oder `singulär` aus. Verwende die gerundete Determinante.',
  NP + '\nmatrizen = [np.array([[1, 2], [3, 4]]), np.array([[2, 6], [1, 3]]),\n            np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]]), np.eye(3)]',
  """for M in matrizen:
    if np.round(np.linalg.det(M), 9) == 0:
        print('singulär')
    else:
        print('invertierbar')""")
t('''Berechne den Flächeninhalt des Dreiecks mit den Ecken `A`, `B` und `C` in der Ebene: der Betrag der Determinante der Matrix aus den Spalten
`B - A` und `C - A`, geteilt durch 2.''',
  NP + '\nA = np.array([1, 1])\nB = np.array([5, 2])\nC = np.array([2, 4])',
  """M = np.column_stack([B - A, C - A])
print(np.round(abs(np.linalg.det(M)) / 2, 2))""")
t('Prüfe für jedes Punkte-Tripel, ob die drei Punkte auf einer Geraden liegen (Determinante wie in der vorigen Aufgabe gleich 0).',
  NP + '\ntripel = [(np.array([0, 0]), np.array([1, 2]), np.array([2, 4])),\n          (np.array([1, 1]), np.array([2, 3]), np.array([4, 6])),\n          (np.array([-1, 3]), np.array([1, 1]), np.array([3, -1]))]',
  """for A, B, C in tripel:
    M = np.column_stack([B - A, C - A])
    print(np.round(np.linalg.det(M), 9) == 0)""")
predict("""import numpy as np
print(np.round(np.linalg.det(np.eye(3)), 6))
print(np.round(np.linalg.det(np.array([[2, 0], [0, 5]])), 6))
print(np.linalg.inv(np.array([[2.0, 0.0], [0.0, 4.0]])))""")

# ---------------------------------------------------------------- 5
sec('Polynome')
expl('''#### Polynome als Koeffizienten-Arrays

numpy speichert ein Polynom als Array seiner **Koeffizienten**, beginnend mit der **höchsten** Potenz:
`f(x) = 2x³ - 3x + 1` ist `[2, 0, -3, 1]` (der Koeffizient von `x²` ist 0).

- `np.polyval(f, x)` berechnet `f(x)`. Für `x` darf man auch ein Array angeben.
- `np.roots(f)` gibt die **Nullstellen** zurück. Ihre Reihenfolge ist nicht festgelegt, deshalb sortiert man mit `np.sort()`.
  Gibt es keine reellen Nullstellen, erhält man komplexe Zahlen (mit `j` geschrieben).
- `np.polyder(f)` ist die **Ableitung**, `np.polyder(f, 2)` die zweite Ableitung.''',
     """import numpy as np

f = np.array([1, -6, 11, -6])     # x³ - 6x² + 11x - 6
print(np.polyval(f, 0))
print(np.polyval(f, np.array([0, 1, 2, 3, 4])))
print(np.sort(np.round(np.roots(f), 6)))
print(np.polyder(f))
print(np.polyder(f, 2))
print(np.roots([1, 0, 1]))""")
expl('''#### Extremstellen

An einer Extremstelle ist die erste Ableitung 0. Die Nullstellen von `np.polyder(f)` sind also die Kandidaten.
Mit der zweiten Ableitung entscheidet man: `f''(x) > 0` ist ein Tiefpunkt, `f''(x) < 0` ein Hochpunkt.''',
     """import numpy as np

f = np.array([1, -6, 9, 1])     # x³ - 6x² + 9x + 1
f1 = np.polyder(f)
f2 = np.polyder(f, 2)
for x in np.sort(np.roots(f1)):
    art = 'Tiefpunkt' if np.polyval(f2, x) > 0 else 'Hochpunkt'
    print(np.round(x, 4), np.round(np.polyval(f, x), 4), art)""")

F = NP + '\nf = np.array([1, -2, -5, 6])     # x³ - 2x² - 5x + 6'
t('Gib `f(2)` und `f(-1)` aus.', F, """print(np.polyval(f, 2))
print(np.polyval(f, -1))""")
t('Gib eine Wertetabelle von `f` für die ganzen Zahlen von -3 bis 4 aus: zuerst das Array der x-Werte, darunter das der y-Werte.', F,
  """x = np.arange(-3, 5)
print(x)
print(np.polyval(f, x))""")
t('Gib die Nullstellen von `f` sortiert und gerundet auf 4 Stellen aus.', F, """print(np.sort(np.round(np.roots(f), 4)))""")
t('Gib die Nullstellen von `g(x) = x² - 5x + 6` aus und vergleiche mit der p-q-Formel: `x = 2.5 ± √(2.5² - 6)`.',
  NP, """print(np.sort(np.round(np.roots([1, -5, 6]), 4)))
print(2.5 - np.sqrt(2.5 ** 2 - 6), 2.5 + np.sqrt(2.5 ** 2 - 6))""")
t('Gib die Ableitung und die zweite Ableitung von `f` aus.', F, """print(np.polyder(f))
print(np.polyder(f, 2))""")
t('Gib die Steigung von `f` an den Stellen 0, 1 und 2 aus (Werte der Ableitung).', F, """print(np.polyval(np.polyder(f), np.array([0, 1, 2])))""")
t('''Bestimme die Extremstellen von `f`. Gib für jede die Stelle, den Funktionswert (beide auf 3 Stellen gerundet) und `Hochpunkt` oder `Tiefpunkt` aus.''', F,
  """f1 = np.polyder(f)
f2 = np.polyder(f, 2)
for x in np.sort(np.roots(f1)):
    art = 'Tiefpunkt' if np.polyval(f2, x) > 0 else 'Hochpunkt'
    print(np.round(x, 3), np.round(np.polyval(f, x), 3), art)""")
t('Bestimme die Wendestelle von `f` (Nullstelle der zweiten Ableitung), gerundet auf 4 Stellen.', F,
  """print(np.round(np.roots(np.polyder(f, 2)), 4))""")
t('''Bestimme die Gleichung der **Tangente** an `f` an der Stelle `x0 = 3`: Die Steigung ist `m = f'(x0)`, der Achsenabschnitt `b = f(x0) - m·x0`.
Gib `m` und `b` aus.''', F,
  """x0 = 3
m = np.polyval(np.polyder(f), x0)
b = np.polyval(f, x0) - m * x0
print(m, b)""")
t('Prüfe für jedes Polynom, ob es reelle Nullstellen hat. Verwende `np.iscomplexobj(np.roots(p))`: Es ist `True`, wenn komplexe Nullstellen herauskommen.',
  NP + '\npolynome = [[1, 0, -4], [1, 0, 4], [1, 2, 5], [2, -3, 1]]',
  """for p in polynome:
    if np.iscomplexobj(np.roots(p)):
        print(p, 'keine reellen Nullstellen')
    else:
        print(p, np.sort(np.round(np.roots(p), 4)))""")
t('''Ein Ball wird senkrecht nach oben geworfen. Seine Höhe in Metern nach `t` Sekunden ist `h(t) = -4.9t² + 15t + 1.5`.
Gib die maximale Höhe und den Zeitpunkt aus, zu dem der Ball auf dem Boden aufkommt (die positive Nullstelle). Runde auf zwei Nachkommastellen.''',
  NP + '\nh = np.array([-4.9, 15, 1.5])',
  """t_max = np.roots(np.polyder(h))[0]
print(np.round(np.polyval(h, t_max), 2))
print(np.round(np.roots(h).max(), 2))""")
predict("""import numpy as np
p = np.array([1, 0, -1])
print(np.polyval(p, 3))
print(np.polyder(p))
print(np.sort(np.roots(p)))
print(np.polyval([5], 100))""")

# ---------------------------------------------------------------- 6
sec('Flächen und Integrale')
expl('''#### Exakt mit `np.polyint()`

`np.polyint(f)` ist eine **Stammfunktion** des Polynoms `f` (mit der Konstanten 0).
Das Integral von `a` bis `b` ist dann `F(b) - F(a)`.''',
     """import numpy as np

f = np.array([3, 0, 0])    # 3x²
F = np.polyint(f)
print(F)
print(np.polyval(F, 2) - np.polyval(F, 0))""")
expl('''#### Näherungsweise mit `np.trapezoid()`

Hat man nur Messwerte oder eine Funktion, die kein Polynom ist, berechnet man die Fläche **näherungsweise**:
`np.trapezoid(y, x)` zerlegt die Fläche unter den Punkten in Trapeze und addiert sie.
Je mehr Punkte, desto genauer.

Dafür braucht man oft weitere mathematische Funktionen, die wie `np.sqrt()` auf jedes Element wirken:
`np.sin()`, `np.cos()` (im Bogenmaß; `np.radians(grad)` rechnet Grad in Bogenmaß um), `np.exp()` (e-Funktion) und `np.log()` (natürlicher Logarithmus).''',
     """import numpy as np

x = np.linspace(0, 2, 5)
print(np.trapezoid(x ** 2, x))
x = np.linspace(0, 2, 1001)
print(np.round(np.trapezoid(x ** 2, x), 6))
print(np.round(8 / 3, 6))""")

t('Gib eine Stammfunktion von `f(x) = 4x³ - 6x + 2` aus.', NP, """print(np.polyint(np.array([4, 0, -6, 2])))""")
t('Berechne das Integral von `f(x) = x² + 1` von 0 bis 3 exakt mit `np.polyint()`.', NP,
  """F = np.polyint(np.array([1, 0, 1]))
print(np.polyval(F, 3) - np.polyval(F, 0))""")
t('Berechne dasselbe Integral näherungsweise mit `np.trapezoid()` und 7 sowie 301 gleichmäßig verteilten Punkten (`np.linspace()`). Runde auf 4 Stellen.', NP,
  """for n in [7, 301]:
    x = np.linspace(0, 3, n)
    print(n, np.round(np.trapezoid(x ** 2 + 1, x), 4))""")
t('''Berechne die Fläche, die der Graph von `f(x) = -x² + 4` mit der x-Achse einschließt. Bestimme dazu zuerst die Nullstellen als Grenzen.
Gib die Fläche auf 4 Stellen gerundet aus.''', NP,
  """f = np.array([-1, 0, 4])
a, b = np.sort(np.roots(f))
F = np.polyint(f)
print(np.round(np.polyval(F, b) - np.polyval(F, a), 4))""")
t('Berechne mit `np.trapezoid()` und 1001 Punkten die Fläche unter `sin(x)` von 0 bis π (exakt: 2). Runde auf 5 Stellen.', NP,
  """x = np.linspace(0, np.pi, 1001)
print(np.round(np.trapezoid(np.sin(x), x), 5))""")
t('''Ein Auto fährt mit den gemessenen Geschwindigkeiten (in m/s) zu den Zeitpunkten (in s). Der zurückgelegte Weg ist die Fläche unter
der Geschwindigkeitskurve. Berechne ihn mit `np.trapezoid()`.''',
  NP + '\nzeit = np.array([0, 2, 4, 6, 8, 10])\ngeschwindigkeit = np.array([0, 5, 9, 12, 13, 13])',
  """print(np.trapezoid(geschwindigkeit, zeit))""")
t('Berechne die Fläche zwischen den Graphen von `f(x) = x` und `g(x) = x²` zwischen ihren Schnittstellen 0 und 1, exakt mit `np.polyint()` von `f - g`.', NP,
  """d = np.array([-1, 1, 0])     # f(x) - g(x) = -x² + x
D = np.polyint(d)
print(np.round(np.polyval(D, 1) - np.polyval(D, 0), 6))""")
predict("""import numpy as np
print(np.polyint(np.array([2, 0])))
print(np.trapezoid(np.array([1, 1, 1]), np.array([0, 1, 2])))
print(np.trapezoid(np.array([0, 2]), np.array([0, 2])))""")

# ---------------------------------------------------------------- 7
sec('Regression')
expl('''#### Regressionsgerade mit `np.polyfit()`

Messwerte liegen selten genau auf einer Geraden. Die **Regressionsgerade** ist die Gerade, die am besten zu den Punkten passt
(die Summe der quadrierten senkrechten Abstände ist am kleinsten).

`np.polyfit(x, y, 1)` gibt die Koeffizienten `[m, b]` der Geraden `y = m·x + b` zurück.
Mit einem höheren Grad, z. B. `np.polyfit(x, y, 2)`, bekommt man eine Regressions-**Parabel**.
Das Ergebnis ist ein Koeffizienten-Array wie in Abschnitt 5, man kann es also mit `np.polyval()` auswerten.

Wie gut die Gerade passt, misst das **Bestimmtheitsmaß** `R²`: das Quadrat des Korrelationskoeffizienten `np.corrcoef(x, y)[0, 1]`.
Es liegt zwischen 0 (passt gar nicht) und 1 (alle Punkte auf der Geraden).''',
     """import numpy as np

x = np.array([1, 2, 3, 4, 5])
y = np.array([2.1, 3.9, 6.2, 7.8, 10.1])
m, b = np.polyfit(x, y, 1)
print(np.round(m, 3), np.round(b, 3))
print(np.round(np.polyval([m, b], 6), 2))
print(np.round(np.corrcoef(x, y)[0, 1] ** 2, 4))""")

L = NP + '\nstunden = np.array([1, 2, 2, 3, 4, 5, 5, 6, 7, 8])\npunkte = np.array([35, 41, 46, 50, 58, 61, 67, 70, 76, 80])'
t('Bestimme die Regressionsgerade für Lernzeit und Punkte. Gib Steigung und Achsenabschnitt auf zwei Nachkommastellen aus.', L,
  """m, b = np.polyfit(stunden, punkte, 1)
print(np.round(m, 2), np.round(b, 2))""")
t('Wie viele Punkte sagt die Regressionsgerade für 10 Stunden Lernzeit voraus? Runde auf eine Nachkommastelle.', L,
  """gerade = np.polyfit(stunden, punkte, 1)
print(np.round(np.polyval(gerade, 10), 1))""")
t('Gib das Bestimmtheitsmaß `R²` aus, gerundet auf 4 Stellen.', L,
  """print(np.round(np.corrcoef(stunden, punkte)[0, 1] ** 2, 4))""")
t('''Gib die **Residuen** aus: für jeden Punkt die Differenz zwischen gemessenem Wert und dem Wert auf der Geraden (zwei Nachkommastellen).
Gib danach den Punkt (Stunden und Punkte) mit dem größten Betrag des Residuums aus.''', L,
  """gerade = np.polyfit(stunden, punkte, 1)
residuen = punkte - np.polyval(gerade, stunden)
print(np.round(residuen, 2))
i = np.abs(residuen).argmax()
print(stunden[i], punkte[i])""")
t('''Ab wie vielen Stunden Lernzeit sagt die Gerade mindestens 90 Punkte voraus? Löse `m·x + b = 90` nach `x` auf und runde auf eine Nachkommastelle.''', L,
  """m, b = np.polyfit(stunden, punkte, 1)
print(np.round((90 - b) / m, 1))""")
t('''Die Bremswege eines Autos (in m) wachsen ungefähr quadratisch mit der Geschwindigkeit (in km/h). Bestimme mit `np.polyfit(..., 2)` eine
Regressionsparabel (Koeffizienten auf 4 Stellen gerundet) und sage den Bremsweg bei 130 km/h voraus (eine Nachkommastelle).''',
  NP + '\nv = np.array([30, 50, 70, 90, 110])\nweg = np.array([9.5, 23.0, 42.0, 66.5, 96.0])',
  """parabel = np.polyfit(v, weg, 2)
print(np.round(parabel, 4))
print(np.round(np.polyval(parabel, 130), 1))""")
t('''Vergleiche eine Gerade und eine Parabel für die Bremswege: Gib für beide die Summe der quadrierten Residuen aus (zwei Nachkommastellen).''',
  NP + '\nv = np.array([30, 50, 70, 90, 110])\nweg = np.array([9.5, 23.0, 42.0, 66.5, 96.0])',
  """for grad in [1, 2]:
    k = np.polyfit(v, weg, grad)
    print(grad, np.round(((weg - np.polyval(k, v)) ** 2).sum(), 2))""")
t('''Exponentielles Wachstum: Die Anzahl der Bakterien verdoppelt sich ungefähr regelmäßig. Lege eine Gerade durch die Punkte `(t, ln(anzahl))`
(`np.log()` ist der natürliche Logarithmus). Gib die Steigung `k` (4 Stellen) und die Verdopplungszeit `ln(2) / k` (zwei Nachkommastellen) aus.''',
  NP + '\nt = np.array([0, 1, 2, 3, 4, 5])\nanzahl = np.array([100, 162, 270, 440, 715, 1180])',
  """k, c = np.polyfit(t, np.log(anzahl), 1)
print(np.round(k, 4))
print(np.round(np.log(2) / k, 2))""")
predict("""import numpy as np
x = np.array([0, 1, 2, 3])
y = 2 * x + 1
print(np.round(np.polyfit(x, y, 1), 6))
print(np.round(np.corrcoef(x, y)[0, 1] ** 2, 6))
print(len(np.polyfit(x, y, 2)))""")

# ---------------------------------------------------------------- 8
sec('Daten aus Dateien')
expl('''#### `np.loadtxt()`

`np.loadtxt(dateiname)` liest eine Textdatei mit Zahlen in ein Array. Jede Zeile wird eine Zeile des Arrays.

| Parameter | Bedeutung |
|---|---|
| `delimiter=','` | Trennzeichen zwischen den Werten (ohne Angabe: Leerzeichen) |
| `skiprows=1` | die erste Zeile (die Überschriften) überspringen |
| `usecols=(1, 2)` | nur diese Spalten lesen |
| `unpack=True` | die Spalten einzeln zurückgeben, z. B. `x, y = np.loadtxt(...)` |
| `dtype=str` | die Werte als Zeichenketten lesen (für Spalten mit Text) |
| `encoding='utf-8'` | wie bei `open()`: immer angeben |

Die Setup-Zelle am Anfang des Notebooks hat die Dateien angelegt.''',
     """import numpy as np

with open('abkuehlung.csv', encoding='utf-8') as f:
    print(f.read()[:40])
daten = np.loadtxt('abkuehlung.csv', delimiter=',', skiprows=1, encoding='utf-8')
print(daten.shape)
print(daten[:3])
minute, temperatur = np.loadtxt('abkuehlung.csv', delimiter=',', skiprows=1, unpack=True, encoding='utf-8')
print(temperatur[:3])""")
expl('''#### `np.savetxt()`

`np.savetxt(dateiname, array, fmt='%.2f', delimiter=',')` schreibt ein Array in eine Textdatei.
`fmt` legt das Format jeder Zahl fest: `'%d'` für ganze Zahlen, `'%.2f'` für zwei Nachkommastellen.
Mit `header='a,b'` und `comments=''` schreibt man eine Überschriftenzeile.''',
     """import numpy as np

a = np.array([[1, 2.5], [3, 4.25]])
np.savetxt('test.csv', a, fmt='%.2f', delimiter=',', header='x,y', comments='')
with open('test.csv', encoding='utf-8') as f:
    print(f.read())""")

AK = NP + "\nminute, temperatur = np.loadtxt('abkuehlung.csv', delimiter=',', skiprows=1, unpack=True, encoding='utf-8')"
t('Lies `abkuehlung.csv` mit `np.loadtxt()` (Überschrift überspringen) in ein Array und gib seine Form und die letzte Zeile aus.', NP,
  """daten = np.loadtxt('abkuehlung.csv', delimiter=',', skiprows=1, encoding='utf-8')
print(daten.shape)
print(daten[-1])""")
t('Gib aus, um wie viel Grad die Temperatur in jeder Minute gesunken ist (eine Nachkommastelle).', AK,
  """print(np.round(-np.diff(temperatur), 1))""")
t('Gib aus, nach wie vielen Minuten die Temperatur zum ersten Mal unter 50 Grad lag.', AK,
  """print(minute[temperatur < 50][0])""")
t('''Die Abkühlung folgt ungefähr `T(t) = 20 + 70 · e^(-k·t)`. Lege dazu eine Gerade durch `(minute, ln(temperatur - 20))` und gib `-k` als Steigung (4 Stellen) aus.
Sage damit die Temperatur nach 20 Minuten voraus: `20 + e^(b + m·20)` (eine Nachkommastelle, `np.exp()` ist die e-Funktion).''', AK,
  """m, b = np.polyfit(minute, np.log(temperatur - 20), 1)
print(np.round(m, 4))
print(np.round(20 + np.exp(b + m * 20), 1))""")
t('Lies `lernzeit.csv` (Trennzeichen `;`) mit `unpack=True` ein und gib die Regressionsgerade (zwei Nachkommastellen) aus.', NP,
  """stunden, punkte = np.loadtxt('lernzeit.csv', delimiter=';', skiprows=1, unpack=True, encoding='utf-8')
print(np.round(np.polyfit(stunden, punkte, 1), 2))""")
t('Lies aus `wetter.csv` nur die Zahlenspalten 1 bis 3 (`usecols=(1, 2, 3)`) und gib die Mittelwerte jeder Spalte aus (zwei Nachkommastellen).', NP,
  """w = np.loadtxt('wetter.csv', delimiter=',', skiprows=1, usecols=(1, 2, 3), encoding='utf-8')
print(np.round(w.mean(axis=0), 2))""")
t('Lies die Tage aus `wetter.csv` mit `dtype=str` und `usecols=0` und die Regenmengen mit `usecols=3`. Gib die Tage aus, an denen es geregnet hat.', NP,
  """tage = np.loadtxt('wetter.csv', delimiter=',', skiprows=1, usecols=0, dtype=str, encoding='utf-8')
regen = np.loadtxt('wetter.csv', delimiter=',', skiprows=1, usecols=3, encoding='utf-8')
print(tage[regen > 0])""")
t('Gib den Tag mit dem größten Unterschied zwischen Tiefst- und Höchsttemperatur aus und den Unterschied.', NP,
  """tage = np.loadtxt('wetter.csv', delimiter=',', skiprows=1, usecols=0, dtype=str, encoding='utf-8')
tmin, tmax = np.loadtxt('wetter.csv', delimiter=',', skiprows=1, usecols=(1, 2), unpack=True, encoding='utf-8')
d = tmax - tmin
print(tage[d.argmax()], d.max())""")
t('''Berechne für jeden Tag aus `wetter.csv` die Durchschnittstemperatur `(tmin + tmax) / 2`. Speichere Tiefst-, Höchst- und Durchschnittstemperatur mit
`np.savetxt()` in `temperaturen.csv` (zwei Nachkommastellen, Überschrift `tmin,tmax,mittel`). Gib danach den Inhalt der Datei aus.''', NP,
  """tmin, tmax = np.loadtxt('wetter.csv', delimiter=',', skiprows=1, usecols=(1, 2), unpack=True, encoding='utf-8')
tabelle = np.column_stack([tmin, tmax, (tmin + tmax) / 2])
np.savetxt('temperaturen.csv', tabelle, fmt='%.2f', delimiter=',', header='tmin,tmax,mittel', comments='')
with open('temperaturen.csv', encoding='utf-8') as f:
    print(f.read())""")
predict("""import numpy as np
a = np.loadtxt('matrix.txt', encoding='utf-8')
print(a.shape)
print(a[0])
print(a.dtype)""")

# ---------------------------------------------------------------- 9
sec('Gemischte Übungen')
t('''Bestimme die Gerade durch die Punkte `P` und `Q`: Löse das Gleichungssystem `m·x + b = y` für beide Punkte. Gib `m` und `b` aus.
Prüfe danach, ob der Punkt `R` auf der Geraden liegt.''',
  NP + '\nP = np.array([1, 3])\nQ = np.array([4, 9])\nR = np.array([6, 13])',
  """A = np.array([[P[0], 1],
              [Q[0], 1]])
m, b = np.linalg.solve(A, np.array([P[1], Q[1]]))
print(np.round(m, 4), np.round(b, 4))
print(np.isclose(m * R[0] + b, R[1]))""")
t('''Bestimme das Polynom 3. Grades durch die vier Punkte mit `np.polyfit(x, y, 3)` (vier Punkte, Grad 3: Das Polynom geht genau durch alle Punkte).
Gib die Koeffizienten (4 Stellen) und den Funktionswert an der Stelle 5 (zwei Nachkommastellen) aus.''',
  NP + '\nx = np.array([0, 1, 2, 4])\ny = np.array([1, 3, 7, 45])',
  """p = np.polyfit(x, y, 3)
print(np.round(p, 4))
print(np.round(np.polyval(p, 5), 2))""")
t('''**Newton-Verfahren:** Bestimme die Nullstelle von `f(x) = x³ - 2x - 5` in der Nähe von 2. Wiederhole sechsmal `x = x - f(x) / f'(x)` und gib `x` nach jedem Schritt aus (8 Stellen).
Prüfe am Ende mit `np.isclose()`, ob `f(x)` ungefähr 0 ist.''',
  NP + '\nf = np.array([1, 0, -2, -5])',
  """f1 = np.polyder(f)
x = 2.0
for i in range(6):
    x = x - np.polyval(f, x) / np.polyval(f1, x)
    print(np.round(x, 8))
print(np.isclose(np.polyval(f, x), 0))""")
t('''**Drehung:** Die Matrix `D = [[cos α, -sin α], [sin α, cos α]]` dreht Punkte um den Ursprung. Drehe die Ecken des Quadrats um 90 Grad
(`np.radians(90)` rechnet in Bogenmaß um). Die Ecken stehen als Spalten in `ecken`. Gib das Ergebnis gerundet auf 6 Stellen und plus `0.0` aus
(damit aus `-0.` eine `0.` wird).''',
  NP + '\necken = np.array([[1, 2, 2, 1],\n                  [1, 1, 2, 2]])',
  """a = np.radians(90)
D = np.array([[np.cos(a), -np.sin(a)],
              [np.sin(a),  np.cos(a)]])
print(np.round(D @ ecken, 6) + 0.0)""")
t('''Prüfe, dass zwei Drehungen um 30 Grad dasselbe ergeben wie eine Drehung um 60 Grad. Schreibe eine Funktion `drehung(grad)`, die die Drehmatrix zurückgibt,
und vergleiche mit `np.allclose()`.''', NP,
  """def drehung(grad):
    a = np.radians(grad)
    return np.array([[np.cos(a), -np.sin(a)],
                     [np.sin(a),  np.cos(a)]])

print(np.allclose(drehung(30) @ drehung(30), drehung(60)))""")
t('''**Langzeitverhalten:** In einer Stadt nutzen die Menschen Auto (A), Bus (B) oder Fahrrad (F). Die Übergangsmatrix beschreibt ein Jahr.
Am Anfang sind es 5000, 3000 und 2000 Personen. Gib die Verteilung nach 1, 5 und 50 Jahren aus (ganze Zahlen gerundet).''',
  NP + '\n# Spalten: von A, B, F; Zeilen: nach A, B, F\nM = np.array([[0.7, 0.2, 0.1],\n              [0.2, 0.7, 0.2],\n              [0.1, 0.1, 0.7]])\nv = np.array([5000, 3000, 2000])',
  """for n in [1, 5, 50]:
    print(n, np.round(np.linalg.matrix_power(M, n) @ v))""")
t('''Berechne für die Abkühlungsdaten aus `abkuehlung.csv` die mittlere Abkühlungsgeschwindigkeit (Grad pro Minute) mit einer Regressionsgeraden
für die ersten 5 Minuten und für die Minuten 6 bis 10. Gib beide Steigungen auf zwei Nachkommastellen aus.''',
  NP + "\nminute, temperatur = np.loadtxt('abkuehlung.csv', delimiter=',', skiprows=1, unpack=True, encoding='utf-8')",
  """m1 = np.polyfit(minute[:6], temperatur[:6], 1)[0]
m2 = np.polyfit(minute[6:], temperatur[6:], 1)[0]
print(np.round(m1, 2), np.round(m2, 2))""")
predict("""import numpy as np
A = np.array([[2, 0], [0, 3]])
print(A @ A)
print(np.round(np.linalg.det(A), 6))
print(np.linalg.solve(A, np.array([4, 9])))
print(np.polyval(np.polyder([1, 0, 0]), 5))""")

generate('numpy_mathe', 'numpy: Mathematik', INTRO)
