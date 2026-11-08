# Erzeugt ../extern/minizinc_daten.ipynb (siehe nbgen.py, mznnb.py). Zweites Notebook der MiniZinc-Reihe:
# minizinc_grundlagen, minizinc_daten, minizinc_zuordnung.
#
# Arbeitsblatt: Die Modelle stehen in Codezellen, die man nicht ausführt (nur kopiert); gerechnet wird in der MiniZinc IDE.
# Der Generator führt jedes Modell mit dem lokal installierten MiniZinc (Gecode) aus und prüft, ob die Lösung eindeutig ist
# (sonst Steuerzeile %! mehrdeutig). Modell und Daten trennt die Zeile  % --- Daten (name.dzn) ---  (siehe mznnb.py).
#     python generator/gen_minizinc_daten.py
import mznnb
from mznnb import t, vorhersage, reihe, ARBEITSBLATT
from nbgen import sec, expl, generate

INTRO = '''Echte Probleme haben viele gleichartige Dinge: Produkte, Gegenstände, Kurse, Tage. Statt für jedes eine eigene Variable anzulegen, beschreibt man
sie mit **Aufzählungen** und **Arrays** und rechnet mit `sum` und `forall` über alle auf einmal. Die Daten (Preise, Mengen, Vorräte) trennt man vom Modell:
Dasselbe Modell löst dann viele Aufgaben. Zum Schluss geht es um **Mengen** als Variablen, wenn eine Auswahl gesucht ist.

''' + reihe(2) + '''

Vorausgesetzt wird *MiniZinc: Grundlagen*.

''' + ARBEITSBLATT

BAECKEREI = r"""enum PRODUKT = {BROETCHEN, BREZEL, MUFFIN};
enum ZUTAT = {MEHL, ZUCKER, OFEN};

array[PRODUKT] of int: gewinn = [20, 30, 50];                  % Cent pro Stück
array[ZUTAT] of int: vorrat = [6000, 1200, 480];               % Gramm, Gramm, Minuten
array[PRODUKT, ZUTAT] of int: verbrauch = [| 50,  0, 2
                                           | 80, 10, 3
                                           | 60, 30, 4 |];

array[PRODUKT] of var 0..200: menge;

constraint forall(z in ZUTAT)(
    sum(p in PRODUKT)(verbrauch[p, z] * menge[p]) <= vorrat[z]
);

solve maximize sum(p in PRODUKT)(gewinn[p] * menge[p]);

output ["\(p): \(menge[p])\n" | p in PRODUKT];"""

RUCKSACK = r"""enum DING;
int: kapazitaet;                     % Gramm
array[DING] of int: gewicht;
array[DING] of int: nutzen;

array[DING] of var 0..1: einpacken;  % 1: kommt mit, 0: bleibt zu Hause

constraint sum(d in DING)(gewicht[d] * einpacken[d]) <= kapazitaet;

solve maximize sum(d in DING)(nutzen[d] * einpacken[d]);

output ["\(d)\n" | d in DING where fix(einpacken[d]) = 1];"""

# ---------------------------------------------------------------- 1
sec('Aufzählungen und Arrays')
expl('''#### Arrays über Aufzählungen

Eine Schulbäckerei backt Brötchen, Brezeln und Muffins. Jedes Produkt bringt einen Gewinn und verbraucht Mehl, Zucker und Ofenzeit; von allem gibt es nur einen
begrenzten Vorrat. Wie viel soll sie von jedem Produkt backen?

- `enum PRODUKT = {BROETCHEN, BREZEL, MUFFIN};` legt die Namen fest.
- `array[PRODUKT] of int: gewinn = [20, 30, 50];` ist ein Array, dessen **Indizes die Produkte** sind: `gewinn[MUFFIN]` ist 50.
- `array[PRODUKT, ZUTAT] of int: verbrauch = [| ... | ... |];` ist ein **zweidimensionales** Array (eine Tabelle): Jede Zeile zwischen `|` gehört zu einem Produkt,
  jede Spalte zu einer Zutat. `verbrauch[BREZEL, MEHL]` ist 80.
- `array[PRODUKT] of var 0..200: menge;` ist ein Array von **Entscheidungsvariablen**, eine pro Produkt.
- `sum(p in PRODUKT)(...)` addiert über alle Produkte, `forall(z in ZUTAT)(...)` verlangt eine Bedingung für jede Zutat.
- `["\\(p): \\(menge[p])\\n" | p in PRODUKT]` erzeugt eine Liste von Texten, einen pro Produkt (eine **Array-Comprehension**, wie eine List Comprehension in Python).''',
     BAECKEREI)

t('''Gib zusätzlich zu den Mengen den Gewinn in Cent und den Verbrauch jeder Zutat aus. Lege dafür `var int: gesamt = sum(...)` an und gib nach den Mengen
`Gewinn: ... Cent` und für jede Zutat eine Zeile `MEHL: ... von 6000` usw. aus. Zwei Listen verbindet man mit `++`.''',
  r"""enum PRODUKT = {BROETCHEN, BREZEL, MUFFIN};
enum ZUTAT = {MEHL, ZUCKER, OFEN};

array[PRODUKT] of int: gewinn = [20, 30, 50];
array[ZUTAT] of int: vorrat = [6000, 1200, 480];
array[PRODUKT, ZUTAT] of int: verbrauch = [| 50,  0, 2
                                           | 80, 10, 3
                                           | 60, 30, 4 |];

array[PRODUKT] of var 0..200: menge;
var int: gesamt = sum(p in PRODUKT)(gewinn[p] * menge[p]);

constraint forall(z in ZUTAT)(
    sum(p in PRODUKT)(verbrauch[p, z] * menge[p]) <= vorrat[z]
);

solve maximize gesamt;

output ["\(p): \(menge[p])\n" | p in PRODUKT] ++
       ["Gewinn: \(gesamt) Cent\n"] ++
       ["\(z): \(sum(p in PRODUKT)(verbrauch[p, z] * menge[p])) von \(vorrat[z])\n" | z in ZUTAT];""")
t('''Die Bäckerei will jeden Tag mindestens 20 Brezeln anbieten und höchstens 40 Muffins backen. Ergänze das Beispielmodell um diese beiden Bedingungen
und gib die Mengen aus.''',
  r"""enum PRODUKT = {BROETCHEN, BREZEL, MUFFIN};
enum ZUTAT = {MEHL, ZUCKER, OFEN};

array[PRODUKT] of int: gewinn = [20, 30, 50];
array[ZUTAT] of int: vorrat = [6000, 1200, 480];
array[PRODUKT, ZUTAT] of int: verbrauch = [| 50,  0, 2
                                           | 80, 10, 3
                                           | 60, 30, 4 |];

array[PRODUKT] of var 0..200: menge;

constraint forall(z in ZUTAT)(
    sum(p in PRODUKT)(verbrauch[p, z] * menge[p]) <= vorrat[z]
);
constraint menge[BREZEL] >= 20;
constraint menge[MUFFIN] <= 40;

solve maximize sum(p in PRODUKT)(gewinn[p] * menge[p]);

output ["\(p): \(menge[p])\n" | p in PRODUKT];""")
t('''Eine Klasse plant einen Ausflug. Es gibt drei Busunternehmen (`enum FIRMA = {A, B, C};`) mit Bussen für 20, 35 und 50 Personen zu 180 €, 260 € und 360 €.
Von jeder Firma sind höchstens 3 Busse frei. 140 Personen fahren mit. Wie viele Busse von jeder Firma sind am günstigsten? Gib die Anzahl je Firma und die
Kosten aus (`A: ...`, `B: ...`, `C: ...`, `Kosten: ... €`).''',
  r"""enum FIRMA = {A, B, C};
array[FIRMA] of int: plaetze = [20, 35, 50];
array[FIRMA] of int: preis = [180, 260, 360];
int: personen = 140;

array[FIRMA] of var 0..3: busse;
var int: kosten = sum(f in FIRMA)(preis[f] * busse[f]);

constraint sum(f in FIRMA)(plaetze[f] * busse[f]) >= personen;

solve minimize kosten;

output ["\(f): \(busse[f])\n" | f in FIRMA] ++ ["Kosten: \(kosten) €\n"];""")
t('''Für ein Müsli werden Haferflocken, Nüsse und Rosinen gemischt (Mengen in 10-g-Schritten, je höchstens 30 Schritte). Pro 10 g enthalten sie
Eiweiß `[1, 2, 0]` g, Zucker `[0, 1, 6]` g und kosten `[2, 9, 4]` Cent. Die Mischung braucht mindestens 40 g Eiweiß, höchstens 30 g Zucker und mindestens 450 g Gewicht.
Was kostet sie mindestens? Benutze ein 2D-Array für Eiweiß und Zucker und gib die Schritte je Zutat und die Kosten aus (`HAFER: ...` usw., `Kosten: ... Cent`).''',
  r"""enum ZUTAT = {HAFER, NUSS, ROSINE};
enum STOFF = {EIWEISS, ZUCKER};

array[ZUTAT, STOFF] of int: gehalt = [| 1, 0
                                      | 2, 1
                                      | 0, 6 |];
array[ZUTAT] of int: preis = [2, 9, 4];

array[ZUTAT] of var 0..30: menge;      % in 10-g-Schritten
var int: kosten = sum(z in ZUTAT)(preis[z] * menge[z]);

constraint sum(z in ZUTAT)(gehalt[z, EIWEISS] * menge[z]) >= 40;
constraint sum(z in ZUTAT)(gehalt[z, ZUCKER] * menge[z]) <= 30;
constraint sum(menge) >= 45;

solve minimize kosten;

output ["\(z): \(menge[z])\n" | z in ZUTAT] ++ ["Kosten: \(kosten) Cent\n"];""")
vorhersage(r"""enum TIER = {HUND, KATZE, MAUS};
array[TIER] of int: beine = [4, 4, 4];
array[TIER] of int: gewicht = [20, 4, 0];

output ["\(sum(beine))\n", "\(gewicht[KATZE])\n", "\(sum(t in TIER where gewicht[t] > 1)(1))\n"];""",
           '''Das Modell hat keine Variablen; es rechnet nur mit Parametern.
- `sum(beine)` addiert alle Einträge: `12`.
- `gewicht[KATZE]` ist `4`.
- Die letzte Summe zählt die Tiere mit mehr als 1 kg: Hund und Katze, also `2`.

Ohne `solve` ergänzt MiniZinc automatisch `solve satisfy`; danach steht `----------`.''')

# ---------------------------------------------------------------- 2
sec('Modell und Daten trennen')
expl('''#### `.dzn`-Dateien

Im Rucksack für den Wandertag ist nur Platz für 3 kg. Welche Gegenstände nimmt man mit, damit der Nutzen am größten ist? (Das ist das berühmte **Rucksackproblem**.)
Das Modell beschreibt das Problem **allgemein**: Die Gegenstände sind ein `enum DING;` **ohne** Werte, Gewichte und Nutzen sind Parameter ohne Wert.
Die Werte stehen in einer **Datendatei** mit der Endung `.dzn`. In der IDE öffnest du beide Dateien; beim Klick auf *Run* fragt die IDE, welche Datendatei
sie benutzen soll (im Playground legst du die Daten als zweite Datei an).

`einpacken[d]` ist 1, wenn der Gegenstand mitkommt. In `output` darf man nur fertige Werte abfragen: `fix(einpacken[d])` ist der Wert der Variablen in der Lösung.''',
     RUCKSACK + r"""
% --- Daten (wandertag.dzn) ---
DING = {WASSER, BROTE, JACKE, KAMERA, BUCH, SPIEL};
kapazitaet = 3000;
gewicht = [1000, 600, 900, 700, 500, 400];
nutzen = [10, 8, 6, 4, 2, 3];""")

t('''Benutze das Rucksack-Modell aus dem Beispiel unverändert mit einer neuen Datendatei `schwimmbad.dzn`: Gegenstände HANDTUCH, FLASCHE, SONNENCREME, BUCH, BALL, OBST
mit den Gewichten 800, 1000, 300, 500, 400, 600 g und dem Nutzen 9, 8, 7, 3, 4, 5; der Rucksack fasst 2500 g. Welche Gegenstände kommen mit?''',
  RUCKSACK + r"""
% --- Daten (schwimmbad.dzn) ---
DING = {HANDTUCH, FLASCHE, SONNENCREME, BUCH, BALL, OBST};
kapazitaet = 2500;
gewicht = [800, 1000, 300, 500, 400, 600];
nutzen = [9, 8, 7, 3, 4, 5];""")
t('''Erweitere das Rucksack-Modell um die Ausgabe des Gesamtgewichts und des Gesamtnutzens (`Gewicht: ... g, Nutzen: ...`) und löse es mit den Daten des Wandertags.''',
  r"""enum DING;
int: kapazitaet;
array[DING] of int: gewicht;
array[DING] of int: nutzen;

array[DING] of var 0..1: einpacken;
var int: summe_gewicht = sum(d in DING)(gewicht[d] * einpacken[d]);
var int: summe_nutzen = sum(d in DING)(nutzen[d] * einpacken[d]);

constraint summe_gewicht <= kapazitaet;

solve maximize summe_nutzen;

output ["\(d)\n" | d in DING where fix(einpacken[d]) = 1] ++
       ["Gewicht: \(summe_gewicht) g, Nutzen: \(summe_nutzen)\n"];
% --- Daten (wandertag.dzn) ---
DING = {WASSER, BROTE, JACKE, KAMERA, BUCH, SPIEL};
kapazitaet = 3000;
gewicht = [1000, 600, 900, 700, 500, 400];
nutzen = [10, 8, 6, 4, 2, 3];""")
t('''Beim Klassenfest gibt es Speisen, von denen man **mehrere** Portionen nehmen darf. Schreibe ein Modell mit `enum SPEISE;`, dem Platz auf dem Tisch (`int: platz;`),
dem Platzbedarf und der Beliebtheit je Portion und `array[SPEISE] of var 0..10: portionen;` und maximiere die Beliebtheit. Daten: Speisen NUDELSALAT, PIZZA, KUCHEN,
Platzbedarf 4, 7, 3, Beliebtheit 9, 17, 6, Platz 30. Gib die Portionen als Liste aus (`show(portionen)`).''',
  r"""enum SPEISE;
int: platz;
array[SPEISE] of int: bedarf;
array[SPEISE] of int: beliebtheit;

array[SPEISE] of var 0..10: portionen;

constraint sum(s in SPEISE)(bedarf[s] * portionen[s]) <= platz;

solve maximize sum(s in SPEISE)(beliebtheit[s] * portionen[s]);

output ["Portionen: ", show(portionen), "\n"];
% --- Daten (klassenfest.dzn) ---
SPEISE = {NUDELSALAT, PIZZA, KUCHEN};
platz = 30;
bedarf = [4, 7, 3];
beliebtheit = [9, 17, 6];""")
t('''Schreibe das Bäckerei-Modell aus Abschnitt 1 so um, dass alle Zahlen in einer Datendatei `montag.dzn` stehen (`enum PRODUKT;` und `enum ZUTAT;` ohne Werte,
die Arrays ohne Werte). Löse es mit diesen Daten: dieselben Produkte und Zutaten, Gewinn 20, 30, 50, aber nur 300 Minuten Ofenzeit (Mehl 6000, Zucker 1200).''',
  r"""enum PRODUKT;
enum ZUTAT;
array[PRODUKT] of int: gewinn;
array[ZUTAT] of int: vorrat;
array[PRODUKT, ZUTAT] of int: verbrauch;

array[PRODUKT] of var 0..200: menge;

constraint forall(z in ZUTAT)(
    sum(p in PRODUKT)(verbrauch[p, z] * menge[p]) <= vorrat[z]
);

solve maximize sum(p in PRODUKT)(gewinn[p] * menge[p]);

output ["\(p): \(menge[p])\n" | p in PRODUKT];
% --- Daten (montag.dzn) ---
PRODUKT = {BROETCHEN, BREZEL, MUFFIN};
ZUTAT = {MEHL, ZUCKER, OFEN};
gewinn = [20, 30, 50];
vorrat = [6000, 1200, 300];
verbrauch = [| 50,  0, 2
             | 80, 10, 3
             | 60, 30, 4 |];""")
vorhersage(r"""enum DING;
array[DING] of int: gewicht;

output ["\(card(DING)) Dinge, zusammen \(sum(gewicht)) g\n"];
% --- Daten (test.dzn) ---
DING = {A, B, C, D};
gewicht = [100, 250, 50, 600];""", '''`card(DING)` ist die Anzahl der Werte der Aufzählung, hier 4. Die Summe der Gewichte ist `100 + 250 + 50 + 600 = 1000`.
Ausgabe: `4 Dinge, zusammen 1000 g`, danach `----------`.''')

# ---------------------------------------------------------------- 3
sec('Rechnen mit Arrays')
expl('''#### Bedingungen in Summen, Maximum und Minimum

- `sum(i in 1..5 where i mod 2 = 1)(a[i])` summiert nur über die `i`, für die die Bedingung hinter `where` gilt.
- `max(a)`, `min(a)` sind das größte und das kleinste Element, `length(a)` die Anzahl der Elemente.
- `forall(i in 1..4)(a[i] <= a[i + 1])` verlangt etwas für alle `i`; `exists(...)` verlangt es für mindestens eines.
- `[a[i] * 2 | i in 1..5]` erzeugt ein neues Array.

Beispiel: Fünf Zahlen von 1 bis 9, aufsteigend sortiert, verschieden, die Summe ist 25, das Maximum ist doppelt so groß wie das Minimum, und die Summe der
Zahlen an den ungeraden Stellen ist 15.''',
     r"""array[1..5] of var 1..9: a;

constraint forall(i in 1..4)(a[i] < a[i + 1]);
constraint sum(a) = 25;
constraint max(a) = 2 * min(a);
constraint sum(i in 1..5 where i mod 2 = 1)(a[i]) = 15;

solve satisfy;

output ["\(a)\n"];""")

t('''Gesucht sind sechs Ziffern von 0 bis 9 (`array[1..6] of var 0..9: z;`), absteigend sortiert (nicht unbedingt verschieden), mit der Summe 30, bei denen genau zwei
Ziffern 0 sind und mindestens einmal 7 vorkommt. Gib alle Lösungen aus (`show(z)`).''',
  r"""%! alle
array[1..6] of var 0..9: z;

constraint forall(i in 1..5)(z[i] >= z[i + 1]);
constraint sum(z) = 30;
constraint sum(i in 1..6)(z[i] = 0) = 2;
constraint exists(i in 1..6)(z[i] = 7);

solve satisfy;

output [show(z), "\n"];""")
t('''Eine Woche hat 5 Schultage. Die Hausaufgabenzeit (in Minuten, 0 bis 90) soll so verteilt werden, dass die Summe 240 ist, kein Tag mehr als 30 Minuten
mehr hat als der Vortag, der Freitag (Tag 5) höchstens 20 Minuten hat und der längste Tag möglichst kurz ist. Gib die Minuten als Liste und das Maximum aus
(`Minuten: ..., längster Tag: ...`). Weil es mehrere gleich gute Verteilungen gibt, kann deine Lösung anders aussehen.''',
  r"""%! mehrdeutig
array[1..5] of var 0..90: minuten;
var int: laengster = max(minuten);

constraint sum(minuten) = 240;
constraint forall(t in 2..5)(minuten[t] - minuten[t - 1] <= 30);
constraint minuten[5] <= 20;

solve minimize laengster;

output ["Minuten: \(minuten), längster Tag: \(laengster)\n"];""")
t('''Ein magisches Quadrat 3 × 3 enthält die Zahlen 1 bis 9, jede einmal; alle Zeilen, Spalten und die beiden Diagonalen haben die Summe 15.
Benutze `array[1..3, 1..3] of var 1..9: q;`, `alldifferent(q)` und `forall`. Damit Drehungen und Spiegelungen nicht mehrfach vorkommen, soll
`q[1, 1] < q[1, 3]`, `q[1, 1] < q[3, 1]` und `q[1, 3] < q[3, 1]` gelten. Gib das Quadrat zeilenweise aus.''',
  r"""include "alldifferent.mzn";

array[1..3, 1..3] of var 1..9: q;

constraint alldifferent(q);
constraint forall(i in 1..3)(sum(j in 1..3)(q[i, j]) = 15);
constraint forall(j in 1..3)(sum(i in 1..3)(q[i, j]) = 15);
constraint sum(i in 1..3)(q[i, i]) = 15;
constraint sum(i in 1..3)(q[i, 4 - i]) = 15;
constraint q[1, 1] < q[1, 3] /\ q[1, 1] < q[3, 1] /\ q[1, 3] < q[3, 1];

solve satisfy;

output [show(q[i, j]) ++ if j = 3 then "\n" else " " endif | i, j in 1..3];""")
t('''Wie viele magische Quadrate 3 × 3 gibt es **ohne** die Bedingungen gegen Drehungen und Spiegelungen?''',
  r"""%! anzahl
include "alldifferent.mzn";

array[1..3, 1..3] of var 1..9: q;

constraint alldifferent(q);
constraint forall(i in 1..3)(sum(j in 1..3)(q[i, j]) = 15);
constraint forall(j in 1..3)(sum(i in 1..3)(q[i, j]) = 15);
constraint sum(i in 1..3)(q[i, i]) = 15;
constraint sum(i in 1..3)(q[i, 4 - i]) = 15;

solve satisfy;""")
vorhersage(r"""array[1..6] of int: a = [3, 8, 1, 9, 4, 6];

output ["\(max(a)) \(min(a)) \(length(a))\n",
        "\(sum(i in 1..6 where a[i] > 4)(a[i]))\n",
        "\([a[i] + 1 | i in 1..3])\n"];""", '''- Größtes Element 9, kleinstes 1, sechs Elemente: `9 1 6`.
- Die Elemente größer als 4 sind 8, 9 und 6: `23`.
- Die ersten drei Elemente plus 1: `[4, 9, 2]`.''')

# ---------------------------------------------------------------- 4
sec('Mengen als Variablen')
expl('''#### `var set of`

Ist eine **Auswahl** gesucht, kann die Variable eine **Menge** sein: `var set of KURS: wahl;` ist irgendeine Teilmenge der Kurse. Mit Mengen kann man rechnen:

| Ausdruck | Bedeutung |
|---|---|
| `k in wahl` | `k` gehört zur Menge |
| `card(wahl)` | Anzahl der Elemente |
| `a union b`, `a intersect b`, `a diff b` | Vereinigung, Schnittmenge, Differenz |
| `a subset b` | `a` ist Teilmenge von `b` |
| `sum(k in wahl)(...)` | Summe über die Elemente der Menge |

Beispiel: In der Projektwoche hat man 12 Stunden Zeit. Jeder Kurs dauert eine bestimmte Zeit und macht unterschiedlich viel Spaß.''',
     r"""enum KURS = {TANZ, KOCHEN, ROBOTIK, THEATER, FOTO};
array[KURS] of int: dauer = [4, 5, 3, 2, 3];
array[KURS] of int: spass = [6, 8, 5, 3, 4];

var set of KURS: wahl;

constraint sum(k in wahl)(dauer[k]) <= 12;

solve maximize sum(k in wahl)(spass[k]);""")
expl('''#### Konflikte zwischen Auswahlen

Manche Kurse finden gleichzeitig statt. Jede **Konfliktgruppe** ist eine Menge von Kursen, aus der man höchstens einen wählen darf:
`card(wahl intersect gruppe) <= 1`. Ein Array von Mengen schreibt man `array[1..3] of set of KURS: gruppen = [{...}, {...}, {...}];`.''',
     r"""enum KURS = {TANZ, KOCHEN, ROBOTIK, THEATER, FOTO};
array[KURS] of int: dauer = [4, 5, 3, 2, 3];
array[KURS] of int: spass = [6, 8, 5, 3, 4];
array[1..2] of set of KURS: gruppen = [{TANZ, KOCHEN}, {KOCHEN, ROBOTIK, FOTO}];

var set of KURS: wahl;

constraint sum(k in wahl)(dauer[k]) <= 12;
constraint forall(g in 1..2)(card(wahl intersect gruppen[g]) <= 1);

solve maximize sum(k in wahl)(spass[k]);""")

KLAUSUR = r"""enum AUFGABE = {A1, A2, A3, A4, A5, A6, A7, A8};
array[AUFGABE] of int: punkte = [10, 8, 6, 12, 5, 9, 7, 4];
array[AUFGABE] of int: minuten = [20, 15, 10, 25, 10, 20, 15, 5];
array[1..3] of set of AUFGABE: gleiches_thema = [{A1, A4, A6}, {A2, A3}, {A5, A7, A8}];"""
t(f'''Für eine Probeklausur wählt eine Lehrkraft Aufgaben aus. Gegeben sind:

```minizinc
{KLAUSUR}
```

Die Klausur darf höchstens 60 Minuten dauern, und aus jeder Gruppe mit gleichem Thema darf höchstens eine Aufgabe dran kommen. Welche Auswahl bringt die meisten Punkte?
Gib die Auswahl und die Punkte aus (`Aufgaben: ..., Punkte: ...`).''',
  KLAUSUR + r"""

var set of AUFGABE: wahl;
var int: summe = sum(a in wahl)(punkte[a]);

constraint sum(a in wahl)(minuten[a]) <= 60;
constraint forall(g in 1..3)(card(wahl intersect gleiches_thema[g]) <= 1);

solve maximize summe;

output ["Aufgaben: \(wahl), Punkte: \(summe)\n"];""")
t('''Ändere das Klausur-Modell so, dass **genau 3** Aufgaben gewählt werden (`card(wahl) = 3`), die Zeitgrenze aber 45 Minuten ist.''',
  KLAUSUR + r"""

var set of AUFGABE: wahl;
var int: summe = sum(a in wahl)(punkte[a]);

constraint sum(a in wahl)(minuten[a]) <= 45;
constraint forall(g in 1..3)(card(wahl intersect gleiches_thema[g]) <= 1);
constraint card(wahl) = 3;

solve maximize summe;

output ["Aufgaben: \(wahl), Punkte: \(summe)\n"];""")
t('''Die Aufgabe `A4` muss in jedem Fall drankommen, `A7` darf nicht drankommen, und die Klausur soll **möglichst kurz** sein, aber mindestens 25 Punkte bringen
(Themengruppen wie oben). Gib die Auswahl und die Minuten aus (`Aufgaben: ..., Minuten: ...`).''',
  KLAUSUR + r"""

var set of AUFGABE: wahl;
var int: dauer = sum(a in wahl)(minuten[a]);

constraint forall(g in 1..3)(card(wahl intersect gleiches_thema[g]) <= 1);
constraint A4 in wahl;
constraint not (A7 in wahl);
constraint sum(a in wahl)(punkte[a]) >= 25;

solve minimize dauer;

output ["Aufgaben: \(wahl), Minuten: \(dauer)\n"];""")
t('''Zwei Freundinnen wählen je eine Menge von Kursen aus der Projektwoche (`var set of KURS: anna;` und `var set of KURS: lea;`, Kurse und Dauer wie im Beispiel,
jede höchstens 12 Stunden). Sie wollen **mindestens zwei** Kurse gemeinsam besuchen, und zusammen sollen sie alle fünf Kurse abdecken (`anna union lea = KURS`).
Maximiere die Summe der Kurse beider. Weil es mehrere gleich gute Lösungen gibt, kann deine anders aussehen.''',
  r"""%! mehrdeutig
enum KURS = {TANZ, KOCHEN, ROBOTIK, THEATER, FOTO};
array[KURS] of int: dauer = [4, 5, 3, 2, 3];

var set of KURS: anna;
var set of KURS: lea;

constraint sum(k in anna)(dauer[k]) <= 12;
constraint sum(k in lea)(dauer[k]) <= 12;
constraint card(anna intersect lea) >= 2;
constraint anna union lea = KURS;

solve maximize card(anna) + card(lea);

output ["Anna: \(anna)\nLea: \(lea)\n"];""")
vorhersage(r"""set of int: a = {1, 2, 3, 4};
set of int: b = {3, 4, 5};

output ["\(a union b) \(a intersect b) \(a diff b) \(card(b))\n"];""", '''- Vereinigung: alle Elemente aus beiden Mengen, `1..5` (MiniZinc schreibt lückenlose Bereiche kurz als `von..bis`).
- Schnittmenge: `3..4`.
- Differenz `a diff b`: die Elemente von `a`, die nicht in `b` sind, `1..2`.
- `b` hat 3 Elemente.

Ausgabe: `1..5 3..4 1..2 3`.''')

# ---------------------------------------------------------------- 5
sec('Zeitreihen und Planung')
expl('''#### Ein Wert für jeden Zeitpunkt

Viele Planungsprobleme laufen über mehrere Zeitpunkte. Man legt dann für jeden Tag ein Array-Element an, oft mit einem **Startwert** an der Stelle 0, und beschreibt,
wie der Wert eines Tages aus dem des Vortags entsteht.

Beispiel: Der Schulgarten hat einen Regenwassertank mit 200 Litern. Jeden Tag kommt Regen hinzu (Liter), und zum Gießen wird Wasser entnommen. Der Tank darf nie leer
werden und nicht über 300 Liter steigen. Gesucht ist die Gießmenge (in Schritten von 10 Litern, höchstens 80 Liter), sodass möglichst viel gegossen wird.''',
     r"""%! mehrdeutig
int: tage = 5;
array[1..tage] of int: regen = [0, 40, 80, 0, 10];

array[0..tage] of var 0..300: tank;
array[1..tage] of var 0..8: giessen;     % in 10-Liter-Schritten

constraint tank[0] = 200;
constraint forall(t in 1..tage)(tank[t] = tank[t - 1] + regen[t] - 10 * giessen[t]);
constraint forall(t in 1..tage)(tank[t] >= 20);

solve maximize sum(giessen);

output ["Tank: \(tank)\nGießen: \(giessen)\n"];""")

t('''Ein Sparschwein: Zu Beginn sind 30 € darin. Jede Woche kommen 10 € Taschengeld dazu; in den Wochen 1 bis 6 werden `ausgaben = [5, 25, 0, 15, 30, 5]` Euro ausgegeben.
Berechne den Inhalt nach jeder Woche mit einem Array `array[0..6] of var int: inhalt;` (ohne `solve`-Ziel, also `solve satisfy`) und gib ihn aus (`Inhalt: ...`).''',
  r"""array[1..6] of int: ausgaben = [5, 25, 0, 15, 30, 5];

array[0..6] of var int: inhalt;

constraint inhalt[0] = 30;
constraint forall(w in 1..6)(inhalt[w] = inhalt[w - 1] + 10 - ausgaben[w]);

solve satisfy;

output ["Inhalt: \(inhalt)\n"];""")
t('''Ein Handy-Akku (Ladung 0 bis 100 %) startet morgens mit 80 %. In den 6 Stunden des Tages wird `verbrauch = [15, 20, 10, 25, 20, 15]` Prozent verbraucht. In jeder Stunde
kann man laden: `nichts` (+0), `kurz` (+10, Kosten 1) oder `lang` (+30, Kosten 2), mit `enum LADEN = {nichts, kurz, lang};` und zwei Arrays für Zuwachs und Kosten.
Die Ladung darf nie unter 20 % fallen und nie über 100 % steigen. Was kostet es mindestens? Gib die Ladungen, die Aktionen und die Kosten aus. Weil es mehrere gleich
günstige Pläne gibt, kann deiner anders aussehen.''',
  r"""%! mehrdeutig
enum LADEN = {nichts, kurz, lang};
array[LADEN] of int: zuwachs = [0, 10, 30];
array[LADEN] of int: kosten = [0, 1, 2];
array[1..6] of int: verbrauch = [15, 20, 10, 25, 20, 15];

array[0..6] of var 20..100: akku;
array[1..6] of var LADEN: aktion;
var int: summe = sum(s in 1..6)(kosten[aktion[s]]);

constraint akku[0] = 80;
constraint forall(s in 1..6)(akku[s] = akku[s - 1] - verbrauch[s] + zuwachs[aktion[s]]);

solve minimize summe;

output ["Akku: \(akku)\nAktionen: \(aktion)\nKosten: \(summe)\n"];""")
t('''Die Temperatur in einem Klassenraum (in °C) folgt der Regel `neu = (alt + außen) div 2 + wirkung`. Die Außentemperaturen der 5 Stunden sind `[10, 8, 6, 9, 12]`,
die Starttemperatur ist 20 °C. Die Heizung hat die Stufen `enum STUFE = {aus, mittel, hoch};` mit der Wirkung 0, 5 und 8 Grad und den Kosten 0, 2 und 4.
Die Temperatur soll in jeder Stunde zwischen 19 und 22 °C liegen. Was kosten die Stufen mindestens? Gib Temperaturen, Stufen und Kosten aus.
Es gibt mehrere gleich günstige Pläne; deiner kann anders aussehen.''',
  r"""%! mehrdeutig
enum STUFE = {aus, mittel, hoch};
array[STUFE] of int: wirkung = [0, 5, 8];
array[STUFE] of int: kosten = [0, 2, 4];
array[1..5] of int: aussen = [10, 8, 6, 9, 12];

array[0..5] of var 19..22: temp;
array[1..5] of var STUFE: stufe;
var int: summe = sum(s in 1..5)(kosten[stufe[s]]);

constraint temp[0] = 20;
constraint forall(s in 1..5)(temp[s] = (temp[s - 1] + aussen[s]) div 2 + wirkung[stufe[s]]);

solve minimize summe;

output ["Temperatur: \(temp)\nStufen: \(stufe)\nKosten: \(summe)\n"];""")
vorhersage(r"""array[0..3] of var int: x;

constraint x[0] = 1;
constraint forall(i in 1..3)(x[i] = 2 * x[i - 1] + 1);

solve satisfy;

output ["\(x)\n"];""", '''Jeder Wert ist das Doppelte des vorigen plus 1: 1, 3, 7, 15. Ausgabe: `[1, 3, 7, 15]`, danach `----------`.''')

# ---------------------------------------------------------------- 6
sec('Gemischte Übungen')
t('''Ein Händler auf dem Wochenmarkt hat einen Stand mit 6 Metern Länge. Er kann Kisten mit Äpfeln (Breite 1 m, Gewinn 30 €), Erdbeeren (Breite 2 m, Gewinn 70 €) und
Kürbissen (Breite 3 m, Gewinn 95 €) aufstellen, von jeder Sorte höchstens 2 Kisten. Modelliere es mit `enum` und Arrays und gib die Kisten je Sorte und den Gewinn aus.''',
  r"""enum SORTE = {APFEL, ERDBEERE, KUERBIS};
array[SORTE] of int: breite = [1, 2, 3];
array[SORTE] of int: gewinn = [30, 70, 95];

array[SORTE] of var 0..2: kisten;
var int: summe = sum(s in SORTE)(gewinn[s] * kisten[s]);

constraint sum(s in SORTE)(breite[s] * kisten[s]) <= 6;

solve maximize summe;

output ["\(s): \(kisten[s])\n" | s in SORTE] ++ ["Gewinn: \(summe) €\n"];""")
t('''Ein Stundenplan-Puzzle mit Mengen: Fünf Fächer (`enum FACH = {DE, MA, EN, SP, KU};`) sollen auf den Vormittag (`var set of FACH: vormittag;`) und den Nachmittag
(`nachmittag`) verteilt werden, jedes Fach genau einmal (die beiden Mengen haben keine gemeinsamen Elemente und ergeben zusammen alle Fächer). Mathe und Deutsch
müssen vormittags sein, Sport nachmittags; vormittags dürfen höchstens 3 Fächer sein und die Fächerstunden `stunden = [2, 2, 1, 2, 1]` sollen auf beiden Hälften
möglichst gleich verteilt sein (minimiere den Betrag der Differenz mit `abs`).''',
  r"""enum FACH = {DE, MA, EN, SP, KU};
array[FACH] of int: stunden = [2, 2, 1, 2, 1];

var set of FACH: vormittag;
var set of FACH: nachmittag;
var int: differenz = abs(sum(f in vormittag)(stunden[f]) - sum(f in nachmittag)(stunden[f]));

constraint vormittag intersect nachmittag = {};
constraint vormittag union nachmittag = FACH;
constraint MA in vormittag /\ DE in vormittag /\ SP in nachmittag;
constraint card(vormittag) <= 3;

solve minimize differenz;

output ["Vormittag: \(vormittag)\nNachmittag: \(nachmittag)\nDifferenz: \(differenz)\n"];""")
t('''Schreibe ein eigenes Planungsmodell mit `enum`, Arrays und einer Datendatei, z. B. für den Einkauf zu einer Geburtstagsfeier, und löse es mit zwei verschiedenen
Datendateien.''',
  r"""%! mehrdeutig
enum ARTIKEL;
int: budget;
array[ARTIKEL] of int: preis;
array[ARTIKEL] of int: freude;

array[ARTIKEL] of var 0..5: anzahl;

constraint sum(a in ARTIKEL)(preis[a] * anzahl[a]) <= budget;

solve maximize sum(a in ARTIKEL)(freude[a] * anzahl[a]);

output ["\(a): \(anzahl[a])\n" | a in ARTIKEL];
% --- Daten (feier.dzn) ---
ARTIKEL = {LUFTBALLONS, CHIPS, LIMO, KUCHEN};
budget = 40;
preis = [3, 2, 4, 12];
freude = [4, 3, 5, 15];""", kind='free')

generate('minizinc_daten', 'MiniZinc 2: Daten', INTRO, sprache='minizinc', ausfuehren=mznnb.ausfuehrung(),
         darstellung=mznnb.darstellung, zellen=mznnb.zellen, ordner='extern')
