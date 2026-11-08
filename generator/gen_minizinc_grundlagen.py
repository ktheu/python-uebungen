# Erzeugt ../content/minizinc_grundlagen.ipynb (siehe nbgen.py, mznnb.py). Erstes Notebook der MiniZinc-Reihe:
# minizinc_grundlagen, minizinc_daten, minizinc_zuordnung.
#
# Arbeitsblatt: Die Modelle stehen in Codezellen, die man nicht ausführt (nur kopiert); gerechnet wird in der MiniZinc IDE.
# Der Generator führt jedes Modell mit dem lokal installierten MiniZinc (Gecode) aus und prüft, ob die Lösung eindeutig ist
# (sonst Steuerzeile %! mehrdeutig, siehe mznnb.py). MiniZinc-Code immer als Raw-String (r"""..."""), wegen \( und \n.
#     python generator/gen_minizinc_grundlagen.py
import mznnb
from mznnb import t, vorhersage, reihe, ARBEITSBLATT
from nbgen import sec, expl, generate

INTRO = '''**MiniZinc** ist eine Sprache, in der man Probleme **beschreibt**, statt sie Schritt für Schritt zu lösen: Welche Größen sind gesucht,
welche Werte dürfen sie haben, welche Bedingungen müssen gelten, was soll möglichst groß oder klein werden? Ein Programm, der **Solver**,
sucht dann selbstständig eine Lösung. Das heißt **Constraint-Programmierung** (*constraint*: Bedingung). So lassen sich Rätsel,
Einkaufs-, Stunden- und Dienstpläne lösen, für die man sonst lange Schleifen und viel Ausprobieren bräuchte.

''' + reihe(1) + '''

''' + ARBEITSBLATT


# ---------------------------------------------------------------- 1
sec('Die MiniZinc IDE')
expl('''#### Ein Modell ausführen

1. Installiere die MiniZinc IDE von [minizinc.org](https://www.minizinc.org/) (*Download* → *MiniZinc IDE, bundled*: mit Solvern).
2. Öffne die IDE. Im großen Fenster schreibst du das **Modell** (Dateiendung `.mzn`).
3. Klicke auf **Run** (oder drücke Strg+R). Oben rechts steht der **Solver**; hier wird immer **Gecode** benutzt, der Standard.
4. Unten im Ausgabefenster erscheint die Lösung. Darunter stehen Markierungen:
   - `----------` beendet eine Lösung.
   - `==========` erscheint, wenn der Solver **fertig gesucht** hat: beim Optimieren, wenn bewiesen ist, dass es keine bessere Lösung gibt,
     und beim Ausgeben aller Lösungen, wenn es keine weitere gibt. Sucht er nur eine Lösung, fehlt diese Zeile.
   - `=====UNSATISFIABLE=====` bedeutet: Es gibt **keine** Lösung.

   Beim Optimieren zeigt die IDE oft auch die **Zwischenlösungen**, die der Solver unterwegs findet, jede besser als die vorige
   (Einstellung *Print intermediate solutions* im Konfigurationseditor). Die beste ist die letzte vor `==========`.
   Die erwarteten Ausgaben in diesem Notebook zeigen nur sie.

Kommentare beginnen in MiniZinc mit `%`. Jede Anweisung endet mit einem Semikolon `;`.

Im **Playground** im Browser ist es genauso: Modell links eintippen, auf *Run* klicken, die Ausgabe erscheint rechts.''', None)

# ---------------------------------------------------------------- 2
sec('Das erste Modell')
expl('''#### Parameter, Variablen, Bedingungen, Ziel

Für ein Klassenfest stehen 60 € zur Verfügung. Eine Pizza kostet 6 €, eine Brezel 1 €, ein Obstteller 4 €. Wie viele Punkte für die Zufriedenheit
jedes Teil bringt, steht im Ziel (Pizza 8, Brezel 1, Obstteller 5). Der Ofen schafft höchstens 6 Pizzen.

Ein MiniZinc-Modell hat diese Teile:

| Teil | Beispiel | Bedeutung |
|---|---|---|
| **Parameter** | `int: budget = 60;` | ein fester Wert (wie eine Konstante) |
| **Entscheidungsvariable** | `var 0..6: pizza;` | gesucht, mit dem erlaubten **Wertebereich** 0 bis 6 |
| **Bedingung** | `constraint ... <= budget;` | muss für jede Lösung gelten |
| **Ziel** | `solve maximize ...;` | was möglichst groß (`maximize`) oder klein (`minimize`) sein soll |
| **Ausgabe** | `output [...];` | was angezeigt wird; `\\(x)` setzt den Wert von `x` in den Text ein, `\\n` ist ein Zeilenumbruch |

Die Reihenfolge der Teile ist egal: MiniZinc ist eine **Beschreibung**, kein Ablauf.''',
     r"""int: budget = 60;

var 0..6: pizza;
var 0..30: brezeln;
var 0..10: obst;

constraint 6 * pizza + 1 * brezeln + 4 * obst <= budget;

solve maximize 8 * pizza + 1 * brezeln + 5 * obst;

output ["Pizzen: \(pizza), Brezeln: \(brezeln), Obstteller: \(obst)\n"];""")
expl('''#### Ohne `output`

Fehlt der `output`-Teil, gibt MiniZinc jede Variable in der Form `name = wert;` aus. Das ist zum Ausprobieren praktisch. Mit `var int: name = ...;`
kann man auch einen ausgerechneten Wert als eigene Variable anlegen, z. B. die Gesamtzufriedenheit, und sie als Ziel benutzen.''',
     r"""int: budget = 60;

var 0..6: pizza;
var 0..30: brezeln;
var 0..10: obst;
var int: punkte = 8 * pizza + 1 * brezeln + 5 * obst;

constraint 6 * pizza + 1 * brezeln + 4 * obst <= budget;

solve maximize punkte;""")

t('''Ändere das Budget im Beispiel auf 45 € und gib wieder aus, wie viele Pizzen, Brezeln und Obstteller gekauft werden (wie im ersten Beispiel).''',
  r"""int: budget = 45;

var 0..6: pizza;
var 0..30: brezeln;
var 0..10: obst;

constraint 6 * pizza + 1 * brezeln + 4 * obst <= budget;

solve maximize 8 * pizza + 1 * brezeln + 5 * obst;

output ["Pizzen: \(pizza), Brezeln: \(brezeln), Obstteller: \(obst)\n"];""")
t('''Für den Sporttag werden Getränke gekauft: Wasser (0,50 € pro Flasche, rechne in Cent) und Saft (1,20 €). Es müssen mindestens 60 Flaschen sein, davon mindestens 15 Saft.
Höchstens 40 Flaschen Wasser sind vorrätig. Was kostet der Einkauf mindestens? Gib die Anzahlen und die Kosten in Cent aus
(`Wasser: ..., Saft: ..., Kosten: ... Cent`).''',
  r"""var 0..40: wasser;
var 0..100: saft;
var int: kosten = 50 * wasser + 120 * saft;

constraint wasser + saft >= 60;
constraint saft >= 15;

solve minimize kosten;

output ["Wasser: \(wasser), Saft: \(saft), Kosten: \(kosten) Cent\n"];""")
t('''Ein Rechteck hat einen Umfang von höchstens 30 cm, beide Seiten sind ganze Zahlen von 1 bis 20 cm. Gesucht ist das Rechteck mit der größten Fläche,
bei dem die Seite `a` mindestens so lang ist wie `b`. Gib `a`, `b` und die Fläche ohne `output` aus (also in der Form `a = ...;`).''',
  r"""var 1..20: a;
var 1..20: b;
var int: flaeche = a * b;

constraint 2 * a + 2 * b <= 30;
constraint a >= b;

solve maximize flaeche;""")
t('''Ein Kiosk verkauft Lose zu 2 € und Glücksräder-Drehungen zu 3 €. Heute wurden insgesamt 40 Lose und Drehungen verkauft und 95 € eingenommen.
Wie viele Lose und wie viele Drehungen waren es? Benutze `solve satisfy;` (es gibt nichts zu optimieren, siehe Abschnitt 3) und gib `Lose: ..., Drehungen: ...` aus.''',
  r"""var 0..40: lose;
var 0..40: drehungen;

constraint lose + drehungen = 40;
constraint 2 * lose + 3 * drehungen = 95;

solve satisfy;

output ["Lose: \(lose), Drehungen: \(drehungen)\n"];""")
vorhersage(r"""var 0..10: x;
var 0..10: y;

constraint x + y = 10;
constraint x - y = 4;

solve satisfy;""", '''Die beiden Bedingungen sind ein lineares Gleichungssystem: Aus `x + y = 10` und `x - y = 4` folgt `x = 7` und `y = 3`.
Ohne `output` gibt MiniZinc `x = 7;` und `y = 3;` aus, danach `----------` (Ende der Lösung). Weil nur eine Lösung gesucht wurde, fehlt `==========`.''')

# ---------------------------------------------------------------- 3
sec('Erfüllbarkeit und alle Lösungen')
expl('''#### `solve satisfy`

Oft gibt es nichts zu optimieren: Gesucht ist nur **irgendeine** Lösung, die alle Bedingungen erfüllt (ein **Erfüllbarkeitsproblem**). Dann steht
`solve satisfy;` im Modell. Der Operator `mod` berechnet den Rest bei der Division (wie der Modulo-Operator `%` in Python), `div` die ganzzahlige Division.

Beispiel: Stellt sich ein Jahrgang in Reihen zu 4 auf, bleiben 3 übrig, in Reihen zu 5 bleiben 4 übrig, in Reihen zu 7 bleiben 6 übrig.
Der Jahrgang hat zwischen 100 und 200 Schülerinnen und Schüler.''',
     r"""var 100..200: jahrgang;

constraint jahrgang mod 4 = 3;
constraint jahrgang mod 5 = 4;
constraint jahrgang mod 7 = 6;

solve satisfy;""")
expl('''#### Alle Lösungen

Gibt es mehrere Lösungen, zeigt der Solver standardmäßig nur die erste. **Alle** Lösungen bekommt man in der IDE so: Klicke oben auf
*Show configuration editor* (das Zahnrad-Symbol) und setze unter *User-defined behavior* den Haken bei **Print all solutions**. Im Playground gibt es
dafür ebenfalls einen Schalter (*All solutions*).

Beispiel: Welche Rechtecke mit ganzzahligen Seiten `a <= b` haben die Fläche 36?''',
     r"""%! alle
var 1..36: a;
var 1..36: b;

constraint a * b = 36;
constraint a <= b;

solve satisfy;

output ["\(a) x \(b)\n"];""")

t('''Ein Zahlenrätsel: Gesucht ist eine Zahl zwischen 1 und 100, die bei der Division durch 3 den Rest 2, durch 5 den Rest 3 und durch 8 den Rest 1 lässt.
Gib sie aus (ohne `output`).''',
  r"""var 1..100: zahl;

constraint zahl mod 3 = 2;
constraint zahl mod 5 = 3;
constraint zahl mod 8 = 1;

solve satisfy;""")
t('''Ein Altersrätsel: Eine Mutter ist heute 4-mal so alt wie ihre Tochter. In 20 Jahren ist sie nur noch doppelt so alt. Gib beide Alter aus
(`Mutter: ..., Tochter: ...`).''',
  r"""var 0..120: mutter;
var 0..120: tochter;

constraint mutter = 4 * tochter;
constraint mutter + 20 = 2 * (tochter + 20);

solve satisfy;

output ["Mutter: \(mutter), Tochter: \(tochter)\n"];""")
t('''Gib **alle** Möglichkeiten aus, 1 € mit 10-, 20- und 50-Cent-Münzen zu bezahlen, in der Form `10er: ..., 20er: ..., 50er: ...` (jede Möglichkeit in einer Zeile).''',
  r"""%! alle
var 0..10: zehner;
var 0..5: zwanziger;
var 0..2: fuenfziger;

constraint 10 * zehner + 20 * zwanziger + 50 * fuenfziger = 100;

solve satisfy;

output ["10er: \(zehner), 20er: \(zwanziger), 50er: \(fuenfziger)\n"];""")
t('''Wie viele Möglichkeiten gibt es, 2 € mit 5-, 10-, 20- und 50-Cent-Münzen zu bezahlen? Schalte *Print all solutions* ein und zähle die Lösungen
(die IDE zeigt mit *Output solver statistics* im Konfigurationseditor am Ende `nSolutions` an).''',
  r"""%! anzahl
var 0..40: fuenfer;
var 0..20: zehner;
var 0..10: zwanziger;
var 0..4: fuenfziger;

constraint 5 * fuenfer + 10 * zehner + 20 * zwanziger + 50 * fuenfziger = 200;

solve satisfy;""")
t('''Gib alle Paare `x <= y` von ganzen Zahlen von 1 bis 50 aus, für die `x + y = 30` und `x * y` durch 7 teilbar ist (`x y` in einer Zeile).''',
  r"""%! alle
var 1..50: x;
var 1..50: y;

constraint x + y = 30;
constraint x <= y;
constraint (x * y) mod 7 = 0;

solve satisfy;

output ["\(x) \(y)\n"];""")
vorhersage(r"""var 1..9: n;

constraint n mod 2 = 0;
constraint n > 7;

solve satisfy;""", '''Gerade Zahlen von 1 bis 9, die größer als 7 sind, gibt es nur eine: `n = 8;`, danach `----------`.''')
vorhersage(r"""var 1..5: n;

constraint n * n = 10;

solve satisfy;""", '''Keine ganze Zahl von 1 bis 5 hat das Quadrat 10. Das Modell hat keine Lösung, MiniZinc meldet `=====UNSATISFIABLE=====` (*nicht erfüllbar*).''')

# ---------------------------------------------------------------- 4
sec('Verschiedene Werte: alldifferent und Kryptogramme')
expl('''#### `alldifferent`

Viele Rätsel verlangen, dass mehrere Variablen **verschiedene** Werte haben. Das könnte man mit vielen `!=`-Bedingungen schreiben. Kürzer ist der
**globale Constraint** `alldifferent([a, b, c, ...])`. Globale Constraints sind fertige Bausteine, die man mit `include "alldifferent.mzn";` einbindet
(oder alle auf einmal mit `include "globals.mzn";`). Die eckigen Klammern bilden eine Liste (ein Array) von Variablen.

Ein **Kryptogramm** ist eine Rechnung, in der jeder Buchstabe für eine Ziffer steht. Verschiedene Buchstaben sind verschiedene Ziffern, und eine Zahl
beginnt nicht mit 0. Das bekannteste ist SEND + MORE = MONEY.''',
     r"""include "alldifferent.mzn";

var 1..9: S;
var 0..9: E;
var 0..9: N;
var 0..9: D;
var 1..9: M;
var 0..9: O;
var 0..9: R;
var 0..9: Y;

constraint            1000 * S + 100 * E + 10 * N + D
                    + 1000 * M + 100 * O + 10 * R + E
         = 10000 * M + 1000 * O + 100 * N + 10 * E + Y;

constraint alldifferent([S, E, N, D, M, O, R, Y]);

solve satisfy;

output ["  \(S)\(E)\(N)\(D)\n",
        "+ \(M)\(O)\(R)\(E)\n",
        "= \(M)\(O)\(N)\(E)\(Y)\n"];""")

t('''Das Kryptogramm **ZWEI + ZWEI = VIER** hat mehrere Lösungen. Gib die Lösung aus, bei der VIER **am kleinsten** ist (lege dafür eine Variable `vier` an
und minimiere sie), wie im Beispiel untereinander.''',
  r"""include "alldifferent.mzn";

var 1..9: Z;
var 0..9: W;
var 0..9: E;
var 0..9: I;
var 1..9: V;
var 0..9: R;
var int: vier = 1000 * V + 100 * I + 10 * E + R;

constraint 2 * (1000 * Z + 100 * W + 10 * E + I) = vier;
constraint alldifferent([Z, W, E, I, V, R]);

solve minimize vier;

output ["  \(Z)\(W)\(E)\(I)\n",
        "+ \(Z)\(W)\(E)\(I)\n",
        "= \(V)\(I)\(E)\(R)\n"];""")
t('''Wie viele Lösungen hat das Kryptogramm **EINS + EINS = ZWEI**?''',
  r"""%! anzahl
include "alldifferent.mzn";

var 1..9: E;
var 0..9: I;
var 0..9: N;
var 0..9: S;
var 1..9: Z;
var 0..9: W;

constraint 2 * (1000 * E + 100 * I + 10 * N + S) = 1000 * Z + 100 * W + 10 * E + I;
constraint alldifferent([E, I, N, S, Z, W]);

solve satisfy;""")
t('''Bei **EINS + EINS = ZWEI** soll ZWEI möglichst groß sein. Lege dafür eine Variable `zwei` an und maximiere sie. Gib die Rechnung wie im Beispiel aus.''',
  r"""include "alldifferent.mzn";

var 1..9: E;
var 0..9: I;
var 0..9: N;
var 0..9: S;
var 1..9: Z;
var 0..9: W;
var int: zwei = 1000 * Z + 100 * W + 10 * E + I;

constraint 2 * (1000 * E + 100 * I + 10 * N + S) = zwei;
constraint alldifferent([E, I, N, S, Z, W]);

solve maximize zwei;

output ["  \(E)\(I)\(N)\(S)\n",
        "+ \(E)\(I)\(N)\(S)\n",
        "= \(Z)\(W)\(E)\(I)\n"];""")
t('''Gesucht sind drei verschiedene Ziffern `a`, `b`, `c` von 1 bis 9 mit `a + b + c = 15` und `a * b * c = 48`, wobei `a < b < c`. Gib sie aus (ohne `output`).''',
  r"""include "alldifferent.mzn";

var 1..9: a;
var 1..9: b;
var 1..9: c;

constraint a + b + c = 15;
constraint a * b * c = 48;
constraint a < b /\ b < c;

solve satisfy;""")
vorhersage(r"""include "alldifferent.mzn";

var 1..3: a;
var 1..3: b;
var 1..3: c;

constraint alldifferent([a, b, c]);
constraint a > b;
constraint b > c;

solve satisfy;""", '''Drei verschiedene Werte von 1 bis 3, absteigend sortiert: Das geht nur mit `a = 3`, `b = 2`, `c = 1`.''')

# ---------------------------------------------------------------- 5
sec('Bedingungen verknüpfen')
expl('''#### Logische Operatoren

Bedingungen kann man verknüpfen:

| Operator | Bedeutung |
|---|---|
| `/\\` | und |
| `\\/` | oder |
| `->` | wenn ..., dann ... |
| `<->` | genau dann, wenn |
| `not` | nicht |

Ein Vergleich wie `(x = 3)` ist wahr oder falsch. In einer Summe zählt `true` als 1 und `false` als 0. So kann man zählen, wie viele Bedingungen
erfüllt sind. Beispiel: Ein Zahlenschloss hat drei Ziffern. Bei `abc` sind genau zwei Ziffern richtig und an der richtigen Stelle, die Summe der Ziffern ist 10,
und wenn die erste Ziffer gerade ist, ist die letzte ungerade.''',
     r"""var 0..9: a;
var 0..9: b;
var 0..9: c;

constraint (a = 4) + (b = 1) + (c = 5) = 2;
constraint a + b + c = 10;
constraint a mod 2 = 0 -> c mod 2 = 1;
constraint a > 0;

solve satisfy;

output ["Code: \(a)\(b)\(c)\n"];""")

t('''Ein Zahlenschloss mit drei Ziffern `a`, `b`, `c` (von 0 bis 9): Bei `2 8 6` ist genau eine Ziffer richtig und an der richtigen Stelle; bei `5 1 4` ist genau eine Ziffer
richtig und an der richtigen Stelle; keine der Ziffern ist 3, 7 oder 9; die Summe ist 13; `a` ist größer als `c`. Gib den Code aus (`Code: ...`).''',
  r"""var 0..9: a;
var 0..9: b;
var 0..9: c;

constraint (a = 2) + (b = 8) + (c = 6) = 1;
constraint (a = 5) + (b = 1) + (c = 4) = 1;
constraint not (a in {3, 7, 9}) /\ not (b in {3, 7, 9}) /\ not (c in {3, 7, 9});
constraint a + b + c = 13;
constraint a > c;

solve satisfy;

output ["Code: \(a)\(b)\(c)\n"];""")
t('''Vier Freunde (Anna, Ben, Cem, Dana) haben unterschiedlich viele Murmeln (1 bis 4). Es gilt: Anna hat mehr als Ben. Cem hat genau eine mehr als Dana.
Wenn Ben 1 Murmel hat, dann hat Dana 2. Ben hat nicht 3. Gib alle Anzahlen aus (ohne `output`).''',
  r"""include "alldifferent.mzn";

var 1..4: anna;
var 1..4: ben;
var 1..4: cem;
var 1..4: dana;

constraint alldifferent([anna, ben, cem, dana]);
constraint anna > ben;
constraint cem = dana + 1;
constraint ben = 1 -> dana = 2;
constraint ben != 3;

solve satisfy;""")
t('''Gib alle Zahlen von 1 bis 30 aus, die durch 3 **oder** durch 5 teilbar sind, aber **nicht** durch beide (eine Zahl pro Zeile).''',
  r"""%! alle
var 1..30: n;

constraint (n mod 3 = 0) \/ (n mod 5 = 0);
constraint not ((n mod 3 = 0) /\ (n mod 5 = 0));

solve satisfy;

output ["\(n)\n"];""")
vorhersage(r"""var 1..9: x;

constraint (x > 5) <-> (x mod 2 = 0);
constraint x > 6;

solve satisfy;""", '''Weil `x > 6` gilt, ist auch `x > 5` wahr. Wegen `<->` muss dann `x` gerade sein. Von 7, 8, 9 ist nur 8 gerade: `x = 8;`.''')

# ---------------------------------------------------------------- 6
sec('Färben')
expl('''#### Aufzählungen und Färbungen

Mit `enum FARBE = {ROT, GRUEN, BLAU};` legt man eine **Aufzählung** an: einen eigenen Typ mit genau diesen Werten. `var FARBE: x;` ist dann eine Variable,
die eine dieser Farben annimmt.

Beim **Färben** sollen benachbarte Dinge verschiedene Farben bekommen. Das Beispiel teilt vier Klausuren auf drei Tage auf (die Tage sind die „Farben“):
Klausuren mit gemeinsamen Schülerinnen und Schülern dürfen nicht am selben Tag sein. Weil es mehrere passende Verteilungen gibt, kann deine Lösung
anders aussehen.''',
     r"""%! mehrdeutig
enum TAG = {MONTAG, DIENSTAG, MITTWOCH};

var TAG: mathe;
var TAG: deutsch;
var TAG: englisch;
var TAG: physik;

constraint mathe != deutsch;
constraint mathe != physik;
constraint deutsch != englisch;
constraint englisch != physik;
constraint mathe != englisch;

solve satisfy;""")

t('''Färbe die Karte der 16 Bundesländer mit vier Farben (`enum FARBE = {ROT, GRUEN, BLAU, GELB};`), sodass benachbarte Länder verschiedene Farben haben.
Benutze für die Länder die Kürzel als Variablennamen. Die Nachbarn sind:

| Land | Nachbarn |
|---|---|
| SH | HH, NI, MV |
| HH | NI |
| NI | HB, MV, BB, ST, TH, HE, NW |
| MV | BB |
| BB | BE, ST, SN |
| ST | SN, TH |
| SN | TH, BY |
| TH | HE, BY |
| HE | NW, RP, BW, BY |
| NW | RP |
| RP | SL, BW |
| BW | BY |

(Jedes Paar steht nur einmal in der Tabelle.) Gib die Farben ohne `output` aus. Weil es sehr viele Färbungen gibt, sieht deine Lösung vermutlich anders aus.''',
  r"""%! mehrdeutig
enum FARBE = {ROT, GRUEN, BLAU, GELB};

var FARBE: SH; var FARBE: HH; var FARBE: NI; var FARBE: HB;
var FARBE: MV; var FARBE: BB; var FARBE: BE; var FARBE: ST;
var FARBE: SN; var FARBE: TH; var FARBE: HE; var FARBE: NW;
var FARBE: RP; var FARBE: SL; var FARBE: BW; var FARBE: BY;

constraint SH != HH /\ SH != NI /\ SH != MV;
constraint HH != NI;
constraint NI != HB /\ NI != MV /\ NI != BB /\ NI != ST /\ NI != TH /\ NI != HE /\ NI != NW;
constraint MV != BB;
constraint BB != BE /\ BB != ST /\ BB != SN;
constraint ST != SN /\ ST != TH;
constraint SN != TH /\ SN != BY;
constraint TH != HE /\ TH != BY;
constraint HE != NW /\ HE != RP /\ HE != BW /\ HE != BY;
constraint NW != RP;
constraint RP != SL /\ RP != BW;
constraint BW != BY;

solve satisfy;""")
t('''Reichen für die Karte der Bundesländer aus der vorigen Aufgabe auch **drei** Farben? Ändere die Aufzählung auf drei Farben und führe das Modell aus.''',
  r"""enum FARBE = {ROT, GRUEN, BLAU};

var FARBE: SH; var FARBE: HH; var FARBE: NI; var FARBE: HB;
var FARBE: MV; var FARBE: BB; var FARBE: BE; var FARBE: ST;
var FARBE: SN; var FARBE: TH; var FARBE: HE; var FARBE: NW;
var FARBE: RP; var FARBE: SL; var FARBE: BW; var FARBE: BY;

constraint SH != HH /\ SH != NI /\ SH != MV;
constraint HH != NI;
constraint NI != HB /\ NI != MV /\ NI != BB /\ NI != ST /\ NI != TH /\ NI != HE /\ NI != NW;
constraint MV != BB;
constraint BB != BE /\ BB != ST /\ BB != SN;
constraint ST != SN /\ ST != TH;
constraint SN != TH /\ SN != BY;
constraint TH != HE /\ TH != BY;
constraint HE != NW /\ HE != RP /\ HE != BW /\ HE != BY;
constraint NW != RP;
constraint RP != SL /\ RP != BW;
constraint BW != BY;

solve satisfy;""")
t('''Fünf Arbeitsgemeinschaften sollen auf möglichst wenige Nachmittage verteilt werden. AGs mit gemeinsamen Mitgliedern dürfen nicht am selben Nachmittag sein:
Chor und Theater, Chor und Robotik, Theater und Schach, Robotik und Schach, Robotik und Garten, Schach und Garten. Nummeriere die Nachmittage mit 1 bis 5 und
minimiere die größte benutzte Nummer (`var int: tage = max([chor, theater, robotik, schach, garten]);`). Gib nur `tage` aus (`Nachmittage: ...`).''',
  r"""var 1..5: chor;
var 1..5: theater;
var 1..5: robotik;
var 1..5: schach;
var 1..5: garten;
var int: tage = max([chor, theater, robotik, schach, garten]);

constraint chor != theater /\ chor != robotik;
constraint theater != schach;
constraint robotik != schach /\ robotik != garten;
constraint schach != garten;

solve minimize tage;

output ["Nachmittage: \(tage)\n"];""")

# ---------------------------------------------------------------- 7
sec('Variablen als Index')
expl('''#### Arrays mit festen Werten

`array[1..4] of int: preis = [5, 3, 8, 2];` ist ein **Array** (eine Liste) von Parametern mit den Indizes 1 bis 4; `preis[3]` ist 8.
Eine Liste in eckigen Klammern beginnt in MiniZinc **immer beim Index 1**. Soll das Array bei 0 beginnen, braucht man `array1d(0..9, [...])`.
Das Beispiel speichert, wie viele Leuchtbalken eine Siebensegmentanzeige für die Ziffern 0 bis 9 braucht (die 1 zwei, die 8 alle sieben): `segmente[8]` ist 7.

Das Besondere: Der Index darf eine **Entscheidungsvariable** sein. `segmente[z]` ist dann die Anzahl der Balken der gesuchten Ziffer `z`.
Beispiel: Welche zweistellige Zahl mit verschiedenen Ziffern braucht genau 5 Balken und ist durch 7 teilbar?''',
     r"""array[0..9] of int: segmente = array1d(0..9, [6, 2, 5, 5, 4, 5, 6, 3, 7, 6]);

var 1..9: zehner;
var 0..9: einer;

constraint segmente[zehner] + segmente[einer] = 5;
constraint (10 * zehner + einer) mod 7 = 0;
constraint zehner != einer;

solve satisfy;

output ["\(zehner)\(einer)\n"];""")

SEG = 'array[0..9] of int: segmente = array1d(0..9, [6, 2, 5, 5, 4, 5, 6, 3, 7, 6]);'
t(f'''Welche dreistellige Zahl mit drei verschiedenen Ziffern braucht auf der Siebensegmentanzeige (`{SEG}`) **möglichst viele** Balken und ist kleiner als 500?
Mehrere Zahlen erreichen die größte Anzahl; nimm von ihnen die **größte** Zahl. Das gelingt mit einem kombinierten Ziel: `solve maximize 1000 * balken + zahl;`
(1000 Balken-Punkte wiegen mehr als jede Zahl unter 1000, die Zahl entscheidet also nur bei gleich vielen Balken).
Gib die Zahl und die Anzahl der Balken aus (`Zahl: ..., Balken: ...`).''',
  r"""include "alldifferent.mzn";

array[0..9] of int: segmente = array1d(0..9, [6, 2, 5, 5, 4, 5, 6, 3, 7, 6]);

var 1..9: h;
var 0..9: z;
var 0..9: e;
var int: balken = segmente[h] + segmente[z] + segmente[e];
var int: zahl = 100 * h + 10 * z + e;

constraint alldifferent([h, z, e]);
constraint zahl < 500;

solve maximize 1000 * balken + zahl;

output ["Zahl: \(h)\(z)\(e), Balken: \(balken)\n"];""")
t(f'''Wie viele dreistellige Zahlen (Ziffern dürfen sich wiederholen) brauchen auf der Siebensegmentanzeige genau 10 Balken? (`{SEG}`)''',
  r"""%! anzahl
array[0..9] of int: segmente = array1d(0..9, [6, 2, 5, 5, 4, 5, 6, 3, 7, 6]);

var 1..9: h;
var 0..9: z;
var 0..9: e;

constraint segmente[h] + segmente[z] + segmente[e] = 10;

solve satisfy;""")
t('''Ein Würfel hat auf gegenüberliegenden Seiten die Augensummen 7. Die Augenzahlen stehen in einem Array `gegenueber = [6, 5, 4, 3, 2, 1]` (gegenüber von 1 liegt 6 usw.).
Zwei Würfel zeigen oben `x` und `y` mit `x < y`; die Summe der beiden **unten** liegenden Zahlen ist 9 und das Produkt der oben liegenden ist 6.
Gib `x` und `y` aus (ohne `output`).''',
  r"""array[1..6] of int: gegenueber = [6, 5, 4, 3, 2, 1];

var 1..6: x;
var 1..6: y;

constraint gegenueber[x] + gegenueber[y] = 9;
constraint x * y = 6;
constraint x < y;

solve satisfy;""")
vorhersage(r"""array[1..4] of int: preis = [5, 3, 8, 2];

var 1..4: i;

solve maximize preis[i];

output ["\(i): \(preis[i])\n"];""", '''Gesucht ist der Index mit dem größten Preis. Der größte Wert 8 steht an Stelle 3: Ausgabe `3: 8`, danach `----------` und `==========`
(beim Optimieren heißt die letzte Markierung: Es gibt keine bessere Lösung).''')

# ---------------------------------------------------------------- 8
sec('Gemischte Übungen')
t('''Der Hausmeister kauft Glühbirnen: kleine Packungen mit 3 Birnen für 4 €, große mit 8 Birnen für 9 €. Er braucht mindestens 50 Birnen und will möglichst wenig bezahlen.
Gib die Packungen und den Preis aus
(`klein: ..., groß: ..., Preis: ... €`).''',
  r"""var 0..20: klein;
var 0..10: gross;
var int: preis = 4 * klein + 9 * gross;

constraint 3 * klein + 8 * gross >= 50;

solve minimize preis;

output ["klein: \(klein), groß: \(gross), Preis: \(preis) €\n"];""")
t('''Ein magisches Dreieck: Die Zahlen 1 bis 6 werden auf die drei Ecken (`a`, `b`, `c`) und die drei Seitenmitten (`x` zwischen a und b, `y` zwischen b und c,
`z` zwischen c und a) verteilt, jede Zahl genau einmal. Die Summe jeder Seite (Ecke + Mitte + Ecke) soll 9 sein. Damit nicht gedrehte und gespiegelte Lösungen
mehrfach erscheinen, soll `a < b < c` gelten. Gib alle Lösungen aus (`a b c / x y z`).''',
  r"""%! alle
include "alldifferent.mzn";

var 1..6: a; var 1..6: b; var 1..6: c;
var 1..6: x; var 1..6: y; var 1..6: z;

constraint alldifferent([a, b, c, x, y, z]);
constraint a + x + b = 9;
constraint b + y + c = 9;
constraint c + z + a = 9;
constraint a < b /\ b < c;

solve satisfy;

output ["\(a) \(b) \(c) / \(x) \(y) \(z)\n"];""")
t('''Welche größte Summe kann ein magisches Dreieck aus der vorigen Aufgabe haben? Mache die Seitensumme zu einer Variablen `s` (alle drei Seiten gleich `s`) und maximiere sie.
Gib die Summe und die Verteilung aus (`Summe ...: a b c / x y z`).''',
  r"""include "alldifferent.mzn";

var 1..6: a; var 1..6: b; var 1..6: c;
var 1..6: x; var 1..6: y; var 1..6: z;
var 6..15: s;

constraint alldifferent([a, b, c, x, y, z]);
constraint a + x + b = s;
constraint b + y + c = s;
constraint c + z + a = s;
constraint a < b /\ b < c;

solve maximize s;

output ["Summe \(s): \(a) \(b) \(c) / \(x) \(y) \(z)\n"];""")
t('''Erfinde ein eigenes Kryptogramm (z. B. mit deinem Namen) oder ein Zahlenrätsel und löse es mit MiniZinc. Prüfe mit *Print all solutions*, ob die Lösung eindeutig ist.''',
  r"""%! mehrdeutig
include "alldifferent.mzn";

var 1..9: M; var 0..9: I; var 0..9: A;
var 1..9: P; var 0..9: Z;

constraint (100 * M + 10 * I + A) + (100 * M + 10 * I + A) = 1000 * P + 100 * I + 10 * Z + A;
constraint alldifferent([M, I, A, P, Z]);

solve satisfy;""", kind='free')

generate('minizinc_grundlagen', 'MiniZinc 1: Grundlagen', INTRO, sprache='minizinc', ausfuehren=mznnb.ausfuehrung(),
         darstellung=mznnb.darstellung, zellen=mznnb.zellen)
