# Erzeugt ../content/dateien.ipynb (siehe nbgen.py).
# Die Beispieldateien werden von der Setup-Zelle am Anfang des Notebooks angelegt.
from nbgen import sec, expl, task, predict, generate, setup

setup('''#### Beispieldateien anlegen

**Führe diese Zelle zuerst aus.** Sie legt im aktuellen Ordner die Dateien an, mit denen in diesem Notebook gearbeitet wird.
Wie man Dateien schreibt, musst du hier noch nicht verstehen.''',
      r"""dateien = {
    'gedicht.txt': '''Der Mond ist aufgegangen,
die goldnen Sternlein prangen
am Himmel hell und klar.
Der Wald steht schwarz und schweiget,
und aus den Wiesen steiget
der weiße Nebel wunderbar.
''',
    'zahlen.txt': '17\n4\n23\n8\n42\n15\n16\n9\n31\n12\n',
    'messwerte.txt': '12.5\n14.0\n13.5\n15.5\n11.0\n16.5\n14.5\n',
    'woerter.txt': 'Haus\nBaum\nElefant\nComputer\nEi\nSchmetterling\nAuto\nRegenbogen\n',
    'einkauf.txt': '  Milch\nBrot  \n\nEier\n   \nButter\nKäse\n',
    'schueler.csv': 'name;alter;ort\nAli;16;Berlin\nBea;17;Hamburg\nCem;15;Köln\nDana;16;Berlin\nEli;17;München\n',
    'noten.csv': 'name,mathe,deutsch,info\nAli,2,3,1\nBea,1,2,2\nCem,3,3,2\nDana,2,1,1\n',
    'preise.csv': 'produkt;preis\nMilch;1.20\nBrot;2.50\nKäse;4.99\nEier;3.10\n',
    'woerterbuch.txt': 'Hund=dog\nKatze=cat\nHaus=house\nBaum=tree\nMaus=mouse\n',
    'log.txt': '''2026-10-17 08:02 LOGIN ali
2026-10-17 08:15 LOGIN bea
2026-10-17 08:31 FEHLER drucker
2026-10-17 09:05 LOGOUT ali
2026-10-17 09:40 LOGIN cem
2026-10-17 10:12 FEHLER netzwerk
2026-10-17 10:30 LOGOUT bea
2026-10-17 11:00 LOGOUT cem
''',
    'karte.txt': '#######\n#S..#.#\n#.#...#\n#...#Z#\n#######\n',
    'matrix.txt': '1 2 3\n4 5 6\n7 8 9\n',
}
for name, inhalt in dateien.items():
    with open(name, 'w', encoding='utf-8') as f:
        f.write(inhalt)
print('Angelegt:', ', '.join(dateien))""")

# ---------------------------------------------------------------- 1
sec('Dateien öffnen und lesen')
expl('''#### `open()`, `read()` und `close()`

- `open(dateiname, encoding='utf-8')` öffnet eine Datei zum Lesen und gibt ein **Dateiobjekt** zurück.
  Die Angabe `encoding='utf-8'` sorgt dafür, dass Umlaute wie ä, ö, ü und ß richtig gelesen werden.
- `f.read()` liest den **ganzen Inhalt** als eine Zeichenkette. Zeilenumbrüche sind darin als `\\n` enthalten.
- `f.read(n)` liest nur die nächsten `n` Zeichen.
- `f.close()` schließt die Datei wieder.''',
     """f = open('gedicht.txt', encoding='utf-8')
inhalt = f.read()
f.close()
print(inhalt)""")
expl('''#### Die `with`-Anweisung

Mit `with open(...) as f:` wird die Datei **automatisch geschlossen**, sobald der eingerückte Block zu Ende ist,
auch wenn ein Fehler passiert. So sollte man Dateien immer öffnen.

Gibt es die Datei nicht, entsteht ein `FileNotFoundError`.''',
     """with open('gedicht.txt', encoding='utf-8') as f:
    anfang = f.read(8)
    rest = f.read()
print(anfang)
print(len(rest))""")

task('Lies die Datei `gedicht.txt` mit `with` und `read()` und gib ihren Inhalt aus.',
     solution="""with open('gedicht.txt', encoding='utf-8') as f:
    inhalt = f.read()
print(inhalt)""")
task('Gib aus, wie viele Zeichen die Datei `gedicht.txt` enthält.',
     solution="""with open('gedicht.txt', encoding='utf-8') as f:
    inhalt = f.read()
print(len(inhalt))""")
task('Lies mit `read(8)` nur die ersten 8 Zeichen von `gedicht.txt` und gib sie aus.',
     solution="""with open('gedicht.txt', encoding='utf-8') as f:
    print(f.read(8))""")
task('Gib den Inhalt von `gedicht.txt` in Großbuchstaben aus.',
     solution="""with open('gedicht.txt', encoding='utf-8') as f:
    inhalt = f.read()
print(inhalt.upper())""")
task("Gib aus, wie oft die Buchstabenfolge `'und'` in `gedicht.txt` vorkommt. Verwende `count()`.",
     solution="""with open('gedicht.txt', encoding='utf-8') as f:
    inhalt = f.read()
print(inhalt.count('und'))""")
task("Prüfe, ob das Wort `'Nebel'` in `gedicht.txt` vorkommt. Gib `True` oder `False` aus.",
     solution="""with open('gedicht.txt', encoding='utf-8') as f:
    inhalt = f.read()
print('Nebel' in inhalt)""")
task("Gib aus, wie viele Zeilen `gedicht.txt` hat. Zähle dazu die Zeilenumbrüche `'\\n'` mit `count()`.",
     solution="""with open('gedicht.txt', encoding='utf-8') as f:
    inhalt = f.read()
print(inhalt.count('\\n'))""")
task('Lies `woerter.txt` einmal **ohne** `with`: mit `open()`, `read()` und `close()`. Gib den Inhalt aus.',
     solution="""f = open('woerter.txt', encoding='utf-8')
inhalt = f.read()
f.close()
print(inhalt)""")
task("Ersetze beim Ausgeben von `gedicht.txt` das Wort `'Mond'` durch `'Sonne'`. Die Datei selbst bleibt unverändert.",
     solution="""with open('gedicht.txt', encoding='utf-8') as f:
    inhalt = f.read()
print(inhalt.replace('Mond', 'Sonne'))""")
predict("""with open('zahlen.txt', encoding='utf-8') as f:
    inhalt = f.read()
print(type(inhalt))
print(inhalt[:2])
print(inhalt[:2] * 2)""")
predict("""with open('gibtsnicht.txt', encoding='utf-8') as f:
    print(f.read())""", error=FileNotFoundError)

# ---------------------------------------------------------------- 2
sec('Zeilenweise lesen')
expl('''#### Zeile für Zeile mit `for`

Mit `for zeile in f:` liest man eine Datei **Zeile für Zeile**. Jede Zeile endet mit einem Zeilenumbruch `\\n`.
Gibt man sie mit `print()` aus, entsteht deshalb eine zusätzliche Leerzeile. Mit `zeile.strip()` entfernt man den
Zeilenumbruch (und Leerzeichen am Rand).''',
     """with open('woerter.txt', encoding='utf-8') as f:
    for zeile in f:
        print(zeile.strip())""")
expl('''#### `readline()`, `readlines()` und `splitlines()`

- `f.readline()` liest **eine** Zeile (mit `\\n` am Ende). Der nächste Aufruf liest die nächste Zeile.
- `f.readlines()` liest **alle** Zeilen und gibt sie als **Liste** zurück, jede mit `\\n`.
- `f.read().splitlines()` gibt ebenfalls eine Liste aller Zeilen zurück, aber **ohne** `\\n`.''',
     """with open('woerter.txt', encoding='utf-8') as f:
    erste = f.readline()
    zweite = f.readline()
print(erste.strip(), zweite.strip())
with open('woerter.txt', encoding='utf-8') as f:
    print(f.readlines()[:3])
with open('woerter.txt', encoding='utf-8') as f:
    print(f.read().splitlines()[:3])""")

task('Gib jede Zeile von `gedicht.txt` mit einer `for`-Schleife aus. Es sollen keine Leerzeilen dazwischen entstehen.',
     solution="""with open('gedicht.txt', encoding='utf-8') as f:
    for zeile in f:
        print(zeile.strip())""")
task('Gib die Zeilen von `gedicht.txt` nummeriert aus wie unten.',
     solution="""with open('gedicht.txt', encoding='utf-8') as f:
    nr = 1
    for zeile in f:
        print(f'{nr}: {zeile.strip()}')
        nr += 1""")
task('Zähle mit einer Schleife die Zeilen von `woerter.txt` und gib die Anzahl aus.',
     solution="""anzahl = 0
with open('woerter.txt', encoding='utf-8') as f:
    for zeile in f:
        anzahl += 1
print(anzahl)""")
task('Gib mit `readline()` nur die erste Zeile von `gedicht.txt` aus.',
     solution="""with open('gedicht.txt', encoding='utf-8') as f:
    print(f.readline().strip())""")
task('Gib mit `readline()` die ersten beiden Zeilen von `log.txt` aus.',
     solution="""with open('log.txt', encoding='utf-8') as f:
    print(f.readline().strip())
    print(f.readline().strip())""")
task('Lies mit `readlines()` alle Zeilen von `gedicht.txt` in eine Liste. Gib die Anzahl der Zeilen und die letzte Zeile aus.',
     solution="""with open('gedicht.txt', encoding='utf-8') as f:
    zeilen = f.readlines()
print(len(zeilen))
print(zeilen[-1].strip())""")
task('Lies `woerter.txt` mit `read().splitlines()` in eine Liste und gib die Liste aus.',
     solution="""with open('woerter.txt', encoding='utf-8') as f:
    woerter = f.read().splitlines()
print(woerter)""")
task("Gib nur die Zeilen von `gedicht.txt` aus, die mit `'der'` beginnen, egal ob groß oder klein geschrieben.",
     solution="""with open('gedicht.txt', encoding='utf-8') as f:
    for zeile in f:
        if zeile.lower().startswith('der'):
            print(zeile.strip())""")
task('Gib für jede Zeile von `gedicht.txt` die Anzahl ihrer Zeichen aus (ohne den Zeilenumbruch).',
     solution="""with open('gedicht.txt', encoding='utf-8') as f:
    for zeile in f:
        print(len(zeile.strip()))""")
task('Gib die Zeilen von `gedicht.txt` in umgekehrter Reihenfolge aus.',
     solution="""with open('gedicht.txt', encoding='utf-8') as f:
    zeilen = f.read().splitlines()
zeilen.reverse()
for z in zeilen:
    print(z)""")
task('In `einkauf.txt` stehen manche Einträge mit Leerzeichen am Rand, und es gibt leere Zeilen. Gib alle Einträge ohne Leerzeichen aus. Leere Zeilen sollen übersprungen werden.',
     solution="""with open('einkauf.txt', encoding='utf-8') as f:
    for zeile in f:
        eintrag = zeile.strip()
        if eintrag != '':
            print(eintrag)""")
task('Lies die bereinigten Einträge aus `einkauf.txt` in eine Liste. Gib die Liste und ihre Länge aus.',
     solution="""einkauf = []
with open('einkauf.txt', encoding='utf-8') as f:
    for zeile in f:
        eintrag = zeile.strip()
        if eintrag != '':
            einkauf.append(eintrag)
print(einkauf)
print(len(einkauf))""")
predict("""with open('gedicht.txt', encoding='utf-8') as f:
    a = f.readline()
    b = f.readline()
print(len(a) - len(a.strip()))
print(b.split()[0])""")

# ---------------------------------------------------------------- 3
sec('Zahlen aus Dateien')
expl('''#### Zahlen umwandeln

Alles, was man aus einer Textdatei liest, sind **Zeichenketten**. Zum Rechnen wandelt man jede Zeile mit `int()`
oder `float()` in eine Zahl um. Am besten entfernt man vorher mit `strip()` den Zeilenumbruch.''',
     """summe = 0
with open('zahlen.txt', encoding='utf-8') as f:
    for zeile in f:
        summe += int(zeile.strip())
print(summe)""")

task('Berechne die Summe aller Zahlen in `zahlen.txt` und gib sie aus.',
     solution="""summe = 0
with open('zahlen.txt', encoding='utf-8') as f:
    for zeile in f:
        summe += int(zeile.strip())
print(summe)""")
task('Lies alle Zahlen aus `zahlen.txt` in eine Liste von ganzen Zahlen. Gib die Liste aus.',
     solution="""zahlen = []
with open('zahlen.txt', encoding='utf-8') as f:
    for zeile in f:
        zahlen.append(int(zeile.strip()))
print(zahlen)""")
task('Gib die größte und die kleinste Zahl aus `zahlen.txt` aus.',
     solution="""zahlen = []
with open('zahlen.txt', encoding='utf-8') as f:
    for zeile in f:
        zahlen.append(int(zeile.strip()))
print(max(zahlen))
print(min(zahlen))""")
task('Berechne den Durchschnitt der Zahlen in `zahlen.txt` und gib ihn aus.',
     solution="""zahlen = []
with open('zahlen.txt', encoding='utf-8') as f:
    for zeile in f:
        zahlen.append(int(zeile.strip()))
print(sum(zahlen) / len(zahlen))""")
task('Zähle, wie viele Zahlen in `zahlen.txt` größer als 15 sind. Gib die Anzahl aus.',
     solution="""anzahl = 0
with open('zahlen.txt', encoding='utf-8') as f:
    for zeile in f:
        if int(zeile.strip()) > 15:
            anzahl += 1
print(anzahl)""")
task('Gib nur die geraden Zahlen aus `zahlen.txt` aus, jede in einer eigenen Zeile.',
     solution="""with open('zahlen.txt', encoding='utf-8') as f:
    for zeile in f:
        z = int(zeile.strip())
        if z % 2 == 0:
            print(z)""")
task('Gib die Zahlen aus `zahlen.txt` aufsteigend sortiert als Liste aus.',
     solution="""zahlen = []
with open('zahlen.txt', encoding='utf-8') as f:
    for zeile in f:
        zahlen.append(int(zeile.strip()))
zahlen.sort()
print(zahlen)""")
task('`messwerte.txt` enthält Temperaturen mit Nachkommastellen. Berechne den Durchschnitt und gib ihn mit zwei Nachkommastellen aus.',
     solution="""werte = []
with open('messwerte.txt', encoding='utf-8') as f:
    for zeile in f:
        werte.append(float(zeile.strip()))
print(f'{sum(werte) / len(werte):.2f}')""")
task('Gib den höchsten Messwert aus `messwerte.txt` aus und in welcher Zeile er steht. Die erste Zeile hat die Nummer 1.',
     solution="""with open('messwerte.txt', encoding='utf-8') as f:
    werte = f.read().splitlines()
hoechster = float(werte[0])
nr = 1
for i in range(len(werte)):
    w = float(werte[i])
    if w > hoechster:
        hoechster = w
        nr = i + 1
print(hoechster)
print(nr)""")
task('Zähle, wie viele Messwerte über dem Durchschnitt liegen. Gib die Anzahl aus.',
     solution="""werte = []
with open('messwerte.txt', encoding='utf-8') as f:
    for zeile in f:
        werte.append(float(zeile.strip()))
schnitt = sum(werte) / len(werte)
anzahl = 0
for w in werte:
    if w > schnitt:
        anzahl += 1
print(anzahl)""")
predict("""with open('zahlen.txt', encoding='utf-8') as f:
    zeilen = f.readlines()
print(int(zeilen[0]) + int(zeilen[1]))
print(zeilen[0].strip() + zeilen[1].strip())""")

# ---------------------------------------------------------------- 4
sec('CSV-Dateien: Zeilen zerlegen')
expl('''#### CSV-Dateien

In einer **CSV-Datei** stehen in jeder Zeile mehrere Werte, getrennt durch ein Trennzeichen, oft `;` oder `,`.
Die erste Zeile ist meist eine **Kopfzeile** mit den Spaltennamen.

- Mit `zeile.strip().split(';')` zerlegt man eine Zeile in eine Liste von Werten.
- Die Kopfzeile überspringt man z. B., indem man sie vor der Schleife mit `f.readline()` liest,
  oder indem man bei einer Liste von Zeilen mit `zeilen[1:]` arbeitet.''',
     """with open('schueler.csv', encoding='utf-8') as f:
    kopf = f.readline()
    for zeile in f:
        teile = zeile.strip().split(';')
        print(teile)""")

task('Gib jede Zeile von `schueler.csv` zerlegt als Liste aus, auch die Kopfzeile.',
     solution="""with open('schueler.csv', encoding='utf-8') as f:
    for zeile in f:
        print(zeile.strip().split(';'))""")
task('Gib die Spaltennamen aus der Kopfzeile von `schueler.csv` aus, jeden in einer eigenen Zeile.',
     solution="""with open('schueler.csv', encoding='utf-8') as f:
    kopf = f.readline().strip().split(';')
for name in kopf:
    print(name)""")
task('Gib nur die Namen aus `schueler.csv` aus, ohne die Kopfzeile.',
     solution="""with open('schueler.csv', encoding='utf-8') as f:
    f.readline()
    for zeile in f:
        teile = zeile.strip().split(';')
        print(teile[0])""")
task('Gib für jeden Schüler aus `schueler.csv` den Satz unten aus.',
     solution="""with open('schueler.csv', encoding='utf-8') as f:
    f.readline()
    for zeile in f:
        name, alter, ort = zeile.strip().split(';')
        print(f'{name} ist {alter} Jahre alt und wohnt in {ort}.')""")
task('Berechne das Durchschnittsalter der Schüler in `schueler.csv` und gib es aus.',
     solution="""summe = 0
anzahl = 0
with open('schueler.csv', encoding='utf-8') as f:
    f.readline()
    for zeile in f:
        teile = zeile.strip().split(';')
        summe += int(teile[1])
        anzahl += 1
print(summe / anzahl)""")
task('Gib die Namen aller Schüler aus `schueler.csv` aus, die in Berlin wohnen.',
     solution="""with open('schueler.csv', encoding='utf-8') as f:
    f.readline()
    for zeile in f:
        name, alter, ort = zeile.strip().split(';')
        if ort == 'Berlin':
            print(name)""")
task('Finde den ältesten Schüler in `schueler.csv`. Gibt es mehrere, nimm den ersten. Gib seinen Namen aus.',
     solution="""aeltester = ''
max_alter = 0
with open('schueler.csv', encoding='utf-8') as f:
    f.readline()
    for zeile in f:
        name, alter, ort = zeile.strip().split(';')
        if int(alter) > max_alter:
            max_alter = int(alter)
            aeltester = name
print(aeltester)""")
task('In `noten.csv` sind die Werte durch Kommas getrennt. Gib für jeden Schüler den Durchschnitt seiner drei Noten mit zwei Nachkommastellen aus wie unten.',
     solution="""with open('noten.csv', encoding='utf-8') as f:
    f.readline()
    for zeile in f:
        teile = zeile.strip().split(',')
        noten = [int(teile[1]), int(teile[2]), int(teile[3])]
        print(f'{teile[0]}: {sum(noten) / len(noten):.2f}')""")
task('Berechne für jedes Fach in `noten.csv` den Durchschnitt. Die Fachnamen stehen in der Kopfzeile. Gib das Ergebnis aus wie unten.',
     solution="""with open('noten.csv', encoding='utf-8') as f:
    zeilen = f.read().splitlines()
kopf = zeilen[0].split(',')
for spalte in range(1, len(kopf)):
    summe = 0
    for zeile in zeilen[1:]:
        summe += int(zeile.split(',')[spalte])
    print(f'{kopf[spalte]}: {summe / (len(zeilen) - 1)}')""")
task('Gib die Namen aller Schüler aus `noten.csv` aus, die in Info eine 1 haben.',
     solution="""with open('noten.csv', encoding='utf-8') as f:
    f.readline()
    for zeile in f:
        teile = zeile.strip().split(',')
        if teile[3] == '1':
            print(teile[0])""")
predict("""zeile = 'Ali;16;Berlin\\n'
teile = zeile.strip().split(';')
print(teile)
print(teile[1] + teile[1])
print(int(teile[1]) + 1)""")

# ---------------------------------------------------------------- 5
sec('Daten in Listen und Dictionaries sammeln')
expl('''#### Erst einlesen, dann auswerten

Oft liest man eine Datei zuerst vollständig in eine **Liste** oder ein **Dictionary** ein und wertet die Daten danach aus.
Dann muss man die Datei nur einmal lesen und kann die Daten mehrfach verwenden.''',
     """alter = {}
with open('schueler.csv', encoding='utf-8') as f:
    f.readline()
    for zeile in f:
        name, a, ort = zeile.strip().split(';')
        alter[name] = int(a)
print(alter)
print(alter['Cem'])""")

task('Lies `schueler.csv` in eine Liste von Tupeln `(name, alter, ort)` ein. Das Alter soll eine Zahl sein. Gib die Liste aus.',
     solution="""schueler = []
with open('schueler.csv', encoding='utf-8') as f:
    f.readline()
    for zeile in f:
        name, alter, ort = zeile.strip().split(';')
        schueler.append((name, int(alter), ort))
print(schueler)""")
task('Lies `schueler.csv` in ein Dictionary ein, das jedem Namen den Wohnort zuordnet. Gib das Dictionary und danach den Wohnort von Dana aus.',
     solution="""orte = {}
with open('schueler.csv', encoding='utf-8') as f:
    f.readline()
    for zeile in f:
        name, alter, ort = zeile.strip().split(';')
        orte[name] = ort
print(orte)
print(orte['Dana'])""")
task('Zähle mit einem Dictionary, wie viele Schüler aus `schueler.csv` in jedem Ort wohnen. Gib das Dictionary aus.',
     solution="""anzahl = {}
with open('schueler.csv', encoding='utf-8') as f:
    f.readline()
    for zeile in f:
        name, alter, ort = zeile.strip().split(';')
        anzahl[ort] = anzahl.get(ort, 0) + 1
print(anzahl)""")
task('Erstelle ein Dictionary, das jedem Alter die Liste der Schüler mit diesem Alter zuordnet. Gib es aus.',
     solution="""gruppen = {}
with open('schueler.csv', encoding='utf-8') as f:
    f.readline()
    for zeile in f:
        name, alter, ort = zeile.strip().split(';')
        gruppen.setdefault(int(alter), []).append(name)
print(gruppen)""")
task("In `woerterbuch.txt` steht in jeder Zeile ein deutsches und ein englisches Wort, getrennt durch `=`. Lies die Datei in ein Dictionary ein und gib die Übersetzung von `'Katze'` aus.",
     solution="""woerterbuch = {}
with open('woerterbuch.txt', encoding='utf-8') as f:
    for zeile in f:
        deutsch, englisch = zeile.strip().split('=')
        woerterbuch[deutsch] = englisch
print(woerterbuch['Katze'])""")
task("Übersetze mit dem Wörterbuch aus `woerterbuch.txt` jedes Wort aus `liste`. Gibt es keine Übersetzung, gib `???` aus.",
     given="liste = ['Haus', 'Hund', 'Fisch', 'Baum']",
     solution="""liste = ['Haus', 'Hund', 'Fisch', 'Baum']
woerterbuch = {}
with open('woerterbuch.txt', encoding='utf-8') as f:
    for zeile in f:
        deutsch, englisch = zeile.strip().split('=')
        woerterbuch[deutsch] = englisch
for w in liste:
    print(w, '->', woerterbuch.get(w, '???'))""")
task('Lies `woerter.txt` in eine Liste ein und gib das längste Wort aus.',
     solution="""with open('woerter.txt', encoding='utf-8') as f:
    woerter = f.read().splitlines()
laengstes = woerter[0]
for w in woerter:
    if len(w) > len(laengstes):
        laengstes = w
print(laengstes)""")
task('Gib die Wörter aus `woerter.txt` nach ihrer Länge sortiert aus, das kürzeste zuerst. Verwende `sort(key=len)`.',
     solution="""with open('woerter.txt', encoding='utf-8') as f:
    woerter = f.read().splitlines()
woerter.sort(key=len)
print(woerter)""")
task('Lies `noten.csv` in ein Dictionary ein, das jedem Namen die Liste seiner Noten (als Zahlen) zuordnet. Gib das Dictionary aus.',
     solution="""noten = {}
with open('noten.csv', encoding='utf-8') as f:
    f.readline()
    for zeile in f:
        teile = zeile.strip().split(',')
        liste = []
        for n in teile[1:]:
            liste.append(int(n))
        noten[teile[0]] = liste
print(noten)""")
predict("""daten = {}
with open('woerterbuch.txt', encoding='utf-8') as f:
    for zeile in f:
        a, b = zeile.strip().split('=')
        daten[b] = a
print(len(daten))
print(daten['tree'])""")

# ---------------------------------------------------------------- 6
sec('Suchen und filtern')
expl('''#### Zeilen durchsuchen

Will man bestimmte Zeilen finden, liest man die Datei Zeile für Zeile und prüft jede Zeile, z. B. mit `in`,
`startswith()` oder nach dem Zerlegen mit `split()`.''',
     """with open('log.txt', encoding='utf-8') as f:
    for zeile in f:
        if 'LOGOUT' in zeile:
            print(zeile.strip())""")

task("Gib alle Zeilen aus `log.txt` aus, die `'FEHLER'` enthalten.",
     solution="""with open('log.txt', encoding='utf-8') as f:
    for zeile in f:
        if 'FEHLER' in zeile:
            print(zeile.strip())""")
task("Zähle, wie oft in `log.txt` ein `LOGIN` vorkommt. Gib die Anzahl aus.",
     solution="""anzahl = 0
with open('log.txt', encoding='utf-8') as f:
    for zeile in f:
        if 'LOGIN' in zeile:
            anzahl += 1
print(anzahl)""")
task('Gib die Namen aller Benutzer aus, die sich eingeloggt haben. Der Name ist das letzte Wort der Zeile.',
     solution="""with open('log.txt', encoding='utf-8') as f:
    for zeile in f:
        teile = zeile.split()
        if teile[2] == 'LOGIN':
            print(teile[-1])""")
task('Gib für jeden Fehler in `log.txt` die Uhrzeit und das betroffene Gerät aus wie unten.',
     solution="""with open('log.txt', encoding='utf-8') as f:
    for zeile in f:
        datum, zeit, art, wer = zeile.split()
        if art == 'FEHLER':
            print(f'{zeit} {wer}')""")
task('Zähle mit einem Dictionary, wie oft jede Art von Ereignis (`LOGIN`, `LOGOUT`, `FEHLER`) in `log.txt` vorkommt. Gib das Dictionary aus.',
     solution="""anzahl = {}
with open('log.txt', encoding='utf-8') as f:
    for zeile in f:
        art = zeile.split()[2]
        anzahl[art] = anzahl.get(art, 0) + 1
print(anzahl)""")
task('Gib für jeden Benutzer aus, wann er sich eingeloggt und wann ausgeloggt hat. Sammle die Zeiten dazu in zwei Dictionaries.',
     solution="""login = {}
logout = {}
with open('log.txt', encoding='utf-8') as f:
    for zeile in f:
        datum, zeit, art, wer = zeile.split()
        if art == 'LOGIN':
            login[wer] = zeit
        if art == 'LOGOUT':
            logout[wer] = zeit
for wer in login:
    print(f'{wer}: {login[wer]} bis {logout[wer]}')""")
task('Gib die erste und die letzte Zeile von `log.txt` aus.',
     solution="""with open('log.txt', encoding='utf-8') as f:
    zeilen = f.read().splitlines()
print(zeilen[0])
print(zeilen[-1])""")
task("Gib die Nummern aller Zeilen von `gedicht.txt` aus, in denen das Wort in `suchwort` vorkommt. Die erste Zeile hat die Nummer 1.",
     given="suchwort = 'und'",
     solution="""suchwort = 'und'
with open('gedicht.txt', encoding='utf-8') as f:
    zeilen = f.read().splitlines()
for i in range(len(zeilen)):
    if suchwort in zeilen[i]:
        print(i + 1)""")
task('Finde das häufigste Wort in `gedicht.txt`. Wandle dazu alles in Kleinbuchstaben um und entferne Kommas und Punkte am Rand jedes Wortes mit `strip(\',.\')`. Gib das Wort und seine Anzahl aus. Kommen mehrere Wörter gleich oft vor, nimm das Wort, das zuerst im Gedicht steht.',
     solution="""anzahl = {}
with open('gedicht.txt', encoding='utf-8') as f:
    for w in f.read().lower().split():
        w = w.strip(',.')
        anzahl[w] = anzahl.get(w, 0) + 1
bestes = ''
meiste = 0
for w, n in anzahl.items():
    if n > meiste:
        bestes = w
        meiste = n
print(bestes, meiste)""")
predict("""with open('log.txt', encoding='utf-8') as f:
    zeilen = f.readlines()
print(len(zeilen))
print(zeilen[2].split()[3])
print(zeilen[-1].split()[1][:2])""")

# ---------------------------------------------------------------- 7
sec('Grids aus Dateien')
expl('''#### Eine Karte oder Tabelle einlesen

Eine Textdatei mit mehreren gleich langen Zeilen kann man als **Grid** lesen:
`read().splitlines()` liefert eine Liste von Zeichenketten. Mit `list(zeile)` macht man daraus eine veränderbare Liste von Listen.
Stehen Zahlen in der Datei, zerlegt man jede Zeile mit `split()` und wandelt die Teile mit `int()` um.''',
     """with open('karte.txt', encoding='utf-8') as f:
    karte = f.read().splitlines()
print(karte[1][1])
with open('matrix.txt', encoding='utf-8') as f:
    for zeile in f:
        print([int(x) for x in zeile.split()])""")

task('Lies `karte.txt` in eine Liste von Zeichenketten ein. Gib die Anzahl der Zeilen und der Spalten aus.',
     solution="""with open('karte.txt', encoding='utf-8') as f:
    karte = f.read().splitlines()
print(len(karte))
print(len(karte[0]))""")
task("Finde in `karte.txt` die Position von `'S'` und von `'Z'`. Gib beide aus wie unten.",
     solution="""with open('karte.txt', encoding='utf-8') as f:
    karte = f.read().splitlines()
for z in range(len(karte)):
    for s in range(len(karte[z])):
        if karte[z][s] == 'S':
            print('Start:', z, s)
        if karte[z][s] == 'Z':
            print('Ziel:', z, s)""")
task("Zähle die Wände `'#'` in `karte.txt` und gib die Anzahl aus.",
     solution="""with open('karte.txt', encoding='utf-8') as f:
    inhalt = f.read()
print(inhalt.count('#'))""")
task("Lies `karte.txt` in eine Liste von Listen ein, setze ein `'X'` in Zeile 2 und Spalte 3 und gib die Karte mit `join()` aus.",
     solution="""with open('karte.txt', encoding='utf-8') as f:
    feld = [list(zeile) for zeile in f.read().splitlines()]
feld[2][3] = 'X'
for zeile in feld:
    print(''.join(zeile))""")
task('Lies `matrix.txt` in ein Grid aus ganzen Zahlen ein. Gib es zeilenweise aus.',
     solution="""grid = []
with open('matrix.txt', encoding='utf-8') as f:
    for zeile in f:
        werte = []
        for x in zeile.split():
            werte.append(int(x))
        grid.append(werte)
for zeile in grid:
    print(zeile)""")
task('Gib für jede Zeile von `matrix.txt` die Summe aus und danach die Summe der Hauptdiagonale.',
     solution="""grid = []
with open('matrix.txt', encoding='utf-8') as f:
    for zeile in f:
        grid.append([int(x) for x in zeile.split()])
for zeile in grid:
    print(sum(zeile))
diagonale = 0
for i in range(len(grid)):
    diagonale += grid[i][i]
print(diagonale)""")
predict("""with open('matrix.txt', encoding='utf-8') as f:
    zeilen = f.read().splitlines()
print(zeilen[1])
print(zeilen[1].split())
print(zeilen[2][0] + zeilen[0][-1])""")

# ---------------------------------------------------------------- 8
sec('Gemischte Übungen')
task('Gib für `gedicht.txt` die Anzahl der Zeilen, der Wörter und der Zeichen aus wie unten.',
     solution="""with open('gedicht.txt', encoding='utf-8') as f:
    inhalt = f.read()
print('Zeilen:', len(inhalt.splitlines()))
print('Wörter:', len(inhalt.split()))
print('Zeichen:', len(inhalt))""")
task('Gib die längste Zeile von `gedicht.txt` aus.',
     solution="""with open('gedicht.txt', encoding='utf-8') as f:
    zeilen = f.read().splitlines()
laengste = zeilen[0]
for z in zeilen:
    if len(z) > len(laengste):
        laengste = z
print(laengste)""")
task("Gib das letzte Wort jeder Zeile von `gedicht.txt` aus, ohne Komma oder Punkt. So sieht man, welche Wörter sich reimen.",
     solution="""with open('gedicht.txt', encoding='utf-8') as f:
    for zeile in f:
        print(zeile.split()[-1].strip(',.'))""")
task('Zähle, wie oft jeder Vokal (a, e, i, o, u) in `gedicht.txt` vorkommt. Groß- und Kleinschreibung sollen keine Rolle spielen. Gib das Ergebnis aus wie unten.',
     solution="""with open('gedicht.txt', encoding='utf-8') as f:
    inhalt = f.read().lower()
for v in 'aeiou':
    print(v, inhalt.count(v))""")
task('''Lies die Preise aus `preise.csv` in ein Dictionary ein. Berechne dann den Preis für alle Einträge aus `einkauf.txt`.
Gibt es für einen Eintrag keinen Preis, gib `kein Preis für ...` aus. Gib am Ende die Summe mit zwei Nachkommastellen aus.''',
     solution="""preise = {}
with open('preise.csv', encoding='utf-8') as f:
    f.readline()
    for zeile in f:
        produkt, preis = zeile.strip().split(';')
        preise[produkt] = float(preis)
summe = 0
with open('einkauf.txt', encoding='utf-8') as f:
    for zeile in f:
        eintrag = zeile.strip()
        if eintrag == '':
            continue
        if eintrag in preise:
            summe += preise[eintrag]
        else:
            print(f'kein Preis für {eintrag}')
print(f'Summe: {summe:.2f} Euro')""")
task('Finde in `noten.csv` den Schüler mit dem besten (kleinsten) Notendurchschnitt. Gib seinen Namen aus.',
     solution="""bester = ''
bester_schnitt = 7
with open('noten.csv', encoding='utf-8') as f:
    f.readline()
    for zeile in f:
        teile = zeile.strip().split(',')
        noten = [int(n) for n in teile[1:]]
        schnitt = sum(noten) / len(noten)
        if schnitt < bester_schnitt:
            bester = teile[0]
            bester_schnitt = schnitt
print(bester)""")
task('Gib alle Wörter aus `woerter.txt`, die mehr als 5 Buchstaben haben, in Großbuchstaben aus.',
     solution="""with open('woerter.txt', encoding='utf-8') as f:
    for zeile in f:
        w = zeile.strip()
        if len(w) > 5:
            print(w.upper())""")
task('Schreibe eine Funktion `lies_zahlen(dateiname)`, die alle Zahlen aus einer Datei mit einer Zahl pro Zeile als Liste von ganzen Zahlen zurückgibt. Gib damit die Summe der Zahlen aus `zahlen.txt` aus.',
     solution="""def lies_zahlen(dateiname):
    zahlen = []
    with open(dateiname, encoding='utf-8') as f:
        for zeile in f:
            zahlen.append(int(zeile.strip()))
    return zahlen

print(sum(lies_zahlen('zahlen.txt')))""")
task("Schreibe eine Funktion `zeilen_mit(dateiname, wort)`, die eine Liste aller Zeilen (ohne Zeilenumbruch) zurückgibt, in denen `wort` vorkommt. Gib damit alle Zeilen aus `log.txt` aus, die `'bea'` enthalten.",
     solution="""def zeilen_mit(dateiname, wort):
    ergebnis = []
    with open(dateiname, encoding='utf-8') as f:
        for zeile in f:
            if wort in zeile:
                ergebnis.append(zeile.strip())
    return ergebnis

for z in zeilen_mit('log.txt', 'bea'):
    print(z)""")
task('Gib die Zahlen aus `zahlen.txt` als einfaches Balkendiagramm aus: Für je 5 angefangene Einheiten ein `#`. Die Zahl steht rechtsbündig in 3 Zeichen Breite davor wie unten. Tipp: `(z + 4) // 5`.',
     solution="""with open('zahlen.txt', encoding='utf-8') as f:
    for zeile in f:
        z = int(zeile.strip())
        print(f'{z:3} ' + '#' * ((z + 4) // 5))""")
predict("""with open('woerter.txt', encoding='utf-8') as f:
    w = f.read().splitlines()
print(len(w))
print(w[0][0] + w[-1][0])
print(sorted(w)[0])""")

generate('dateien', 'Dateien lesen')
