# Erzeugt ../content/sql_abfragen.ipynb (siehe nbgen.py) für den SQLite-Kernel (xeus-sqlite) und die Datenbank kino.db.
#
#     py -3.13 -W error generator/gen_sql_abfragen.py
#
# Die Datenbank content/kino.db entsteht aus kino_db.py (nur neu geschrieben, wenn sich der Inhalt ändert).
# Geprüft wird mit Python-sqlite3 (sqlnb.sql_ausfuehrung): gleiche SQLite-Version (3.49.x) wie im Kernel.
# Erwartete Ausgaben sind HTML-Tabellen wie im Kernel (NULL = leere Zelle, Kommazahlen mit 15 Stellen).
# Jede Code-Zelle enthält genau EINE SQL-Anweisung (der Kernel führt nur die erste aus). Keine Zelle nur mit Kommentar.
# Ergebnisse ohne ORDER BY haben in SQLite eine feste Reihenfolge (gleiche Datei, gleiche Version), trotzdem meist sortieren.
import os
import sqlite3

from nbgen import sec, expl, task, predict, generate, setup
from sqlnb import sql_ausfuehrung, html_tabelle
from kino_db import erzeuge, er_bild

INHALT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'content')
erzeuge(os.path.join(INHALT, 'kino.db'))

_bilder = {}


def tabellen_bild(tabellen):
    schluessel = tuple(sorted(tabellen))
    if schluessel not in _bilder:
        _bilder[schluessel] = er_bild(list(schluessel))
    return {'tabellen.png': _bilder[schluessel]}


BILD = '\n\n![Tabellen](attachment:tabellen.png)'


def a(text, tabellen, loesung):
    """Aufgabe mit Diagramm der beteiligten Tabellen."""
    task(text + BILD, solution=loesung, anhaenge=tabellen_bild(tabellen))


def inhalt(tabelle):
    """Der vollständige Inhalt einer (kleinen) Tabelle als HTML, damit man ein Ergebnis wirklich vorhersagen kann."""
    con = sqlite3.connect(os.path.join(INHALT, 'kino.db'))
    try:
        return f'Inhalt der Tabelle `{tabelle}`:\n\n' + html_tabelle(con, con.execute(f'SELECT * FROM {tabelle}'))
    finally:
        con.close()


def v(code, tabellen, error=None, hinweis='', zeige=()):
    """Vorhersage-Aufgabe, mit Diagramm, wenn Tabellen beteiligt sind.
    hinweis: Text vor der Frage (z. B. Zeilenzahlen); zeige: Tabellen, deren Inhalt in der Aufgabe steht.
    Vorhersagen müssen ohne Ausführen lösbar sein: nur mit Angaben, die in der Aufgabe stehen."""
    text = ''.join(inhalt(t) + '\n' for t in zeige) + (hinweis + '\n\n' if hinweis else '')
    if tabellen:
        predict(code, error=error, anhaenge=tabellen_bild(tabellen), text='![Tabellen](attachment:tabellen.png)\n\n' + text)
    else:
        predict(code, error=error, text=text)


ALLE = ['film', 'saal', 'vorstellung', 'kunde', 'ticket']

INTRO = '''In diesem Notebook übst du **SQL-Abfragen** an der Datenbank eines Kinos: Filme, Säle, Vorstellungen, Kunden und Tickets.
Du schreibst in jede Code-Zelle **eine SQL-Anweisung**. Beim Ausführen erscheint das Ergebnis als Tabelle.
Das Notebook verwendet den Kernel **SQLite** (oben rechts steht „SQLite (xsqlite)“), nicht Python.

Jeder Abschnitt beginnt mit kurzen Erklärungen und Beispielen. Führe die Beispiele aus und probiere sie ruhig ein wenig aus.
Danach folgen viele kleine Übungen. Bei jeder Aufgabe siehst du die beteiligten Tabellen und darunter das **erwartete Ergebnis**.
Vergleiche dein Ergebnis damit, auch die Reihenfolge der Zeilen und die Spaltennamen.

**Wichtig:**
- Führe zuerst die Zelle mit `%LOAD kino.db r` aus. Sie öffnet die Datenbank (`r`: nur lesen, du kannst also nichts kaputt machen).
  Musst du das Notebook neu öffnen oder den Kernel neu starten, führe sie wieder aus.
- In jede Zelle gehört **genau eine** Anweisung. Stehen mehrere darin, wird nur die erste ausgeführt.
- Fehlende Werte (`NULL`) erscheinen in der Ergebnistabelle als **leeres Feld**.

**So liest du die Diagramme:** Jeder Kasten ist eine Tabelle mit ihren Spalten. **Unterstrichen** ist der Primärschlüssel,
**↑** markiert einen Fremdschlüssel. An den Verbindungslinien steht die Kardinalität: Eine Linie mit **1** und **n**
bedeutet zum Beispiel, dass zu einem Film (1) viele Vorstellungen (n) gehören.'''

setup('''#### Datenbank öffnen

**Führe diese Zelle zuerst aus.** Sie öffnet die Datenbank `kino.db`, die im selben Ordner wie dieses Notebook liegt.''',
      '%LOAD kino.db r')

# ---------------------------------------------------------------- 1
sec('Die Kino-Datenbank')
expl('''#### Die Tabellen

Die Datenbank `kino.db` gehört zu einem kleinen Kino mit vier Sälen. Sie enthält den Spielplan einer Woche (2. bis 8. November 2026).

![Datenbank kino.db](attachment:datenbank.png)

| Tabelle | Inhalt |
|---|---|
| `film` | alle Filme mit Genre, Erscheinungsjahr, Dauer in Minuten und Altersfreigabe (`fsk`) |
| `saal` | die Säle mit Anzahl der Plätze und Ausstattung |
| `vorstellung` | wann welcher Film in welchem Saal läuft, mit Eintrittspreis in Euro |
| `kunde` | die Kunden mit Geburtsjahr, Wohnort und E-Mail-Adresse (nicht alle haben eine) |
| `ticket` | die verkauften Tickets: wer welche Vorstellung besucht, mit Sitzplatz; `ermaessigt` ist 1 oder 0 |

Zwischen `kunde` und `vorstellung` besteht eine **n:m-Beziehung**: Ein Kunde besucht viele Vorstellungen, eine Vorstellung hat viele Besucher.
Sie wird durch die Tabelle `ticket` mit zwei Fremdschlüsseln aufgelöst.

`SELECT * FROM tabelle;` gibt eine ganze Tabelle aus. Der Stern `*` steht für „alle Spalten“.''',
     'SELECT * FROM saal;', anhaenge={'datenbank.png': er_bild(ALLE)})
expl('''#### Welche Tabellen und Spalten gibt es?

SQLite speichert die Beschreibung der Datenbank selbst in einer Tabelle: `sqlite_master` enthält alle Tabellen.
`PRAGMA table_info(film);` zeigt die Spalten einer Tabelle mit ihrem Datentyp; `pk` ist 1 beim Primärschlüssel.''',
     "SELECT name FROM sqlite_master WHERE type = 'table';")

a('Gib die ganze Tabelle `film` aus.', ['film'], 'SELECT * FROM film;')
a('Gib die ganze Tabelle `vorstellung` aus. (Sie ist lang. Schau dir an, wie Datum, Uhrzeit und Preis gespeichert sind.)', ['vorstellung'],
  'SELECT * FROM vorstellung;')
a('Gib mit `PRAGMA table_info(...)` die Spalten der Tabelle `ticket` aus.', ['ticket'], 'PRAGMA table_info(ticket);')
a('Gib die Namen aller Tabellen aus, die es in der Datenbank gibt.', ALLE, "SELECT name FROM sqlite_master WHERE type = 'table';")

# ---------------------------------------------------------------- 2
sec('Spalten auswählen')
expl('''#### `SELECT spalte1, spalte2 FROM tabelle`

Statt `*` gibt man die gewünschten Spalten mit Komma getrennt an. Sie erscheinen in dieser Reihenfolge.

- Mit `AS` gibt man einer Spalte im Ergebnis einen anderen Namen: `SELECT name AS saal FROM saal;`
- Man kann auch **rechnen**: `plaetze * 2`, `dauer / 60.0`. Achtung: Teilt man zwei ganze Zahlen, ist das Ergebnis ganzzahlig (`7 / 2` ist `3`).
  Mit `60.0` statt `60` wird mit Kommazahlen gerechnet. `ROUND(x, 2)` rundet auf zwei Nachkommastellen.
- `||` hängt Texte aneinander: `vorname || ' ' || nachname`. Texte stehen in **einfachen** Anführungszeichen.
- `LIMIT 5` am Ende gibt nur die ersten 5 Zeilen aus.''',
     '''SELECT titel, dauer, ROUND(dauer / 60.0, 2) AS stunden
FROM film
LIMIT 5;''')
expl('''#### `DISTINCT`

`SELECT DISTINCT spalte FROM tabelle;` gibt jeden Wert nur **einmal** aus, auch wenn er in mehreren Zeilen vorkommt.''',
     'SELECT DISTINCT wohnort FROM kunde;')

a('Gib Name und Anzahl der Plätze aller Säle aus.', ['saal'], 'SELECT name, plaetze FROM saal;')
a('Gib Vorname und Nachname der ersten 5 Kunden aus.', ['kunde'], 'SELECT vorname, nachname FROM kunde LIMIT 5;')
a('Gib Titel und Erscheinungsjahr der ersten 8 Filme aus. Die Spalten sollen im Ergebnis `Film` und `Jahr` heißen.', ['film'],
  'SELECT titel AS Film, jahr AS Jahr FROM film LIMIT 8;')
a('Gib für jeden Saal den Namen und die Anzahl der Plätze mit 10 zusätzlichen Notsitzen aus. Die zweite Spalte soll `mit_notsitzen` heißen.', ['saal'],
  'SELECT name, plaetze + 10 AS mit_notsitzen FROM saal;')
a('Gib für die ersten 5 Filme den Titel und die Dauer in Stunden aus, gerundet auf zwei Nachkommastellen (Spaltenname `stunden`).', ['film'],
  'SELECT titel, ROUND(dauer / 60.0, 2) AS stunden FROM film LIMIT 5;')
a("Gib für die ersten 6 Kunden den ganzen Namen in **einer** Spalte `name` aus, z. B. `Lena Hoffmann`.", ['kunde'],
  "SELECT vorname || ' ' || nachname AS name FROM kunde LIMIT 6;")
a('Gib alle Genres aus, jedes nur einmal.', ['film'], 'SELECT DISTINCT genre FROM film;')
a('Gib alle Tage aus, an denen Vorstellungen stattfinden, jeden nur einmal.', ['vorstellung'], 'SELECT DISTINCT datum FROM vorstellung;')
a('Gib alle Uhrzeiten aus, zu denen Vorstellungen beginnen, jede nur einmal.', ['vorstellung'], 'SELECT DISTINCT uhrzeit FROM vorstellung;')
a('''Gib für die ersten 5 Vorstellungen Datum, Uhrzeit, Preis und den Preis für eine Familie mit 4 Personen (Spalte `familie`) aus.''', ['vorstellung'],
  'SELECT datum, uhrzeit, preis, preis * 4 AS familie FROM vorstellung LIMIT 5;')
a('Gib für die ersten 5 Kunden Vorname, Nachname und das Alter im Jahr 2026 (Spalte `alter_2026`) aus.', ['kunde'],
  'SELECT vorname, nachname, 2026 - geburtsjahr AS alter_2026 FROM kunde LIMIT 5;')
v('SELECT 3 + 4 * 2 AS a, 7 / 2 AS b, 7 / 2.0 AS c, 7 % 2 AS d;', [])

# ---------------------------------------------------------------- 3
sec('Zeilen auswählen mit WHERE')
expl('''#### Bedingungen

Mit `WHERE` gibt man nur die Zeilen aus, die eine Bedingung erfüllen.

| Zeichen | Bedeutung |
|---|---|
| `=`, `<>` | gleich, ungleich (`!=` geht auch) |
| `<`, `>`, `<=`, `>=` | kleiner, größer, ... |
| `AND`, `OR`, `NOT` | und, oder, nicht |
| `BETWEEN a AND b` | zwischen a und b (beide einschließlich) |
| `IN ('a', 'b', 'c')` | einer der Werte in der Liste |

Texte und Datumsangaben stehen in einfachen Anführungszeichen: `WHERE genre = 'Krimi'`, `WHERE datum = '2026-11-03'`.
Weil Datum (`2026-11-03`) und Uhrzeit (`20:00`) so gespeichert sind, kann man sie auch mit `<` und `>` vergleichen.''',
     '''SELECT titel, jahr, fsk
FROM film
WHERE jahr = 2025 AND fsk <= 6;''')
expl('''#### `LIKE` und `NULL`

- `LIKE` vergleicht mit einem **Muster**: `%` steht für beliebig viele Zeichen, `_` für genau ein Zeichen.
  `titel LIKE 'Die %'` sind alle Titel, die mit „Die “ beginnen. Groß- und Kleinschreibung spielt bei `LIKE` keine Rolle (bei Umlauten schon).
- `NULL` bedeutet „kein Wert“. Ob ein Wert fehlt, prüft man mit `IS NULL` bzw. `IS NOT NULL`, **nicht** mit `= NULL`.''',
     '''SELECT vorname, nachname, email
FROM kunde
WHERE nachname LIKE 'S%';''')

F = ['film']
K = ['kunde']
a('Gib die Titel aller Komödien aus.', F, "SELECT titel FROM film WHERE genre = 'Komödie';")
a('Gib Titel und Dauer aller Filme aus, die länger als 120 Minuten sind.', F, 'SELECT titel, dauer FROM film WHERE dauer > 120;')
a('Gib die Titel aller Filme ohne Altersbeschränkung (FSK 0) aus.', F, 'SELECT titel FROM film WHERE fsk = 0;')
a('Gib Vorname und Nachname aller Kunden aus Greven aus.', K, "SELECT vorname, nachname FROM kunde WHERE wohnort = 'Greven';")
a('Gib für alle Vorstellungen am 4. November 2026 die Uhrzeit, die Film-Nummer und die Saal-Nummer aus.', ['vorstellung'],
  "SELECT uhrzeit, film_id, saal_id FROM vorstellung WHERE datum = '2026-11-04';")
a('Gib die Titel aller Filme aus dem Jahr 2025 mit FSK 12 aus.', F, 'SELECT titel FROM film WHERE jahr = 2025 AND fsk = 12;')
a('Gib Titel und Genre aller Horrorfilme und Krimis aus. Verwende `OR`.', F,
  "SELECT titel, genre FROM film WHERE genre = 'Horror' OR genre = 'Krimi';")
a('Gib Titel und Genre aller Horrorfilme und Krimis aus. Verwende diesmal `IN`.', F,
  "SELECT titel, genre FROM film WHERE genre IN ('Horror', 'Krimi');")
a('Gib Vorname, Nachname und Geburtsjahr aller Kunden aus, die von 2000 bis 2009 geboren sind. Verwende `BETWEEN`.', K,
  'SELECT vorname, nachname, geburtsjahr FROM kunde WHERE geburtsjahr BETWEEN 2000 AND 2009;')
a('Gib Vorname, Nachname und Wohnort aller Kunden aus Telgte, Senden oder Havixbeck aus.', K,
  "SELECT vorname, nachname, wohnort FROM kunde WHERE wohnort IN ('Telgte', 'Senden', 'Havixbeck');")
a('Gib die Titel aller Filme aus, die mit „Die “ beginnen.', F, "SELECT titel FROM film WHERE titel LIKE 'Die %';")
a('Gib die Nachnamen aller Kunden aus, die auf „er“ enden.', K, "SELECT nachname FROM kunde WHERE nachname LIKE '%er';")
a('Gib die Titel aller Filme aus, in deren Titel das Wort „der“ vorkommt (auch „Der“ am Anfang).', F,
  "SELECT titel FROM film WHERE titel LIKE '%der %';")
a('Gib Vorname und Nachname aller Kunden aus, die **keine** E-Mail-Adresse haben.', K, 'SELECT vorname, nachname FROM kunde WHERE email IS NULL;')
a('Gib Vorname, Nachname und E-Mail aller Kunden aus Münster aus, die eine E-Mail-Adresse haben.', K,
  "SELECT vorname, nachname, email FROM kunde WHERE wohnort = 'Münster' AND email IS NOT NULL;")
a('Gib alle Vorstellungen (alle Spalten) am 6. November aus, die um 20:00 Uhr oder später beginnen.', ['vorstellung'],
  "SELECT * FROM vorstellung WHERE datum = '2026-11-06' AND uhrzeit >= '20:00';")
a('Gib Titel, Genre und FSK aller Filme aus, die **keine** Komödie sind und FSK unter 12 haben. Verwende `NOT`.', F,
  "SELECT titel, genre, fsk FROM film WHERE NOT genre = 'Komödie' AND fsk < 12;")
v("SELECT name FROM saal WHERE plaetze > 100 AND ausstattung = 'Standard';", ['saal'], zeige=['saal'])
v('SELECT vorname FROM kunde WHERE email = NULL;', K)

# ---------------------------------------------------------------- 4
sec('Sortieren und begrenzen')
expl('''#### `ORDER BY` und `LIMIT`

- `ORDER BY spalte` sortiert aufsteigend (`ASC`, das ist der Standard), `ORDER BY spalte DESC` absteigend.
- Mit mehreren Spalten wird zuerst nach der ersten sortiert, bei Gleichheit nach der zweiten: `ORDER BY nachname, vorname`.
- `LIMIT n` gibt nur die ersten `n` Zeilen aus, `LIMIT n OFFSET k` überspringt vorher `k` Zeilen.

Die Reihenfolge der Teile ist fest: `SELECT ... FROM ... WHERE ... ORDER BY ... LIMIT ...`''',
     '''SELECT titel, dauer
FROM film
ORDER BY dauer DESC
LIMIT 3;''')

a('Gib Name und Plätze aller Säle aus, den größten Saal zuerst.', ['saal'], 'SELECT name, plaetze FROM saal ORDER BY plaetze DESC;')
a('Gib Titel und Dauer der 5 kürzesten Filme aus, den kürzesten zuerst.', F, 'SELECT titel, dauer FROM film ORDER BY dauer LIMIT 5;')
a('Gib Vorname und Nachname aller Kunden aus Münster aus, sortiert nach Nachname.', K,
  "SELECT vorname, nachname FROM kunde WHERE wohnort = 'Münster' ORDER BY nachname;")
a('Gib Uhrzeit, Film-Nummer und Preis aller Vorstellungen am 7. November aus, nach Uhrzeit sortiert, bei gleicher Uhrzeit nach Preis.', ['vorstellung'],
  "SELECT uhrzeit, film_id, preis FROM vorstellung WHERE datum = '2026-11-07' ORDER BY uhrzeit, preis;")
a('Gib Vorname, Nachname und Geburtsjahr der 5 jüngsten Kunden aus. Bei gleichem Geburtsjahr soll nach Nachname sortiert werden.', K,
  'SELECT vorname, nachname, geburtsjahr FROM kunde ORDER BY geburtsjahr DESC, nachname LIMIT 5;')
a('Gib Titel, Genre und Jahr aller Filme aus 2025 aus, nach Genre sortiert und innerhalb eines Genres nach Titel.', F,
  'SELECT titel, genre, jahr FROM film WHERE jahr = 2025 ORDER BY genre, titel;')
a('Gib die Plätze 4 bis 6 der Rangliste der längsten Filme aus (Titel und Dauer). Verwende `OFFSET`.', F,
  'SELECT titel, dauer FROM film ORDER BY dauer DESC LIMIT 3 OFFSET 3;')
a('Gib Datum, Uhrzeit und Preis der 3 teuersten Vorstellungen aus. Bei gleichem Preis die frühere zuerst (nach Datum, dann Uhrzeit).', ['vorstellung'],
  'SELECT datum, uhrzeit, preis FROM vorstellung ORDER BY preis DESC, datum, uhrzeit LIMIT 3;')
a('Gib alle Wohnorte jeweils einmal in alphabetischer Reihenfolge aus.', K, 'SELECT DISTINCT wohnort FROM kunde ORDER BY wohnort;')
v('SELECT name, plaetze FROM saal ORDER BY ausstattung DESC LIMIT 2;', ['saal'], zeige=['saal'])

# ---------------------------------------------------------------- 5
sec('Aggregatfunktionen')
expl('''#### Zählen, Summe, Durchschnitt, Minimum und Maximum

**Aggregatfunktionen** fassen viele Zeilen zu **einem** Wert zusammen:

| Funktion | Ergebnis |
|---|---|
| `COUNT(*)` | Anzahl der Zeilen |
| `COUNT(spalte)` | Anzahl der Zeilen, in denen die Spalte **nicht** `NULL` ist |
| `COUNT(DISTINCT spalte)` | Anzahl der verschiedenen Werte |
| `SUM(spalte)`, `AVG(spalte)` | Summe, Durchschnitt |
| `MIN(spalte)`, `MAX(spalte)` | kleinster, größter Wert |

Mit `WHERE` werden vorher die Zeilen ausgewählt, die zusammengefasst werden. Den Ergebnisspalten gibt man am besten mit `AS` einen Namen.''',
     '''SELECT COUNT(*) AS anzahl, MIN(dauer) AS kuerzester, MAX(dauer) AS laengster, ROUND(AVG(dauer), 1) AS durchschnitt
FROM film;''')

a('Gib aus, wie viele Filme es gibt (Spaltenname `anzahl`).', F, 'SELECT COUNT(*) AS anzahl FROM film;')
a('Gib aus, wie viele Kunden eine E-Mail-Adresse haben. Verwende `COUNT(email)`.', K, 'SELECT COUNT(email) AS mit_email FROM kunde;')
a('Gib die durchschnittliche Dauer aller Filme aus, gerundet auf eine Nachkommastelle.', F, 'SELECT ROUND(AVG(dauer), 1) AS durchschnitt FROM film;')
a('Gib die Gesamtzahl der Plätze in allen Sälen aus.', ['saal'], 'SELECT SUM(plaetze) AS plaetze_gesamt FROM saal;')
a('Gib aus, wie viele Vorstellungen am Dienstag, dem 3. November, stattfinden.', ['vorstellung'],
  "SELECT COUNT(*) AS anzahl FROM vorstellung WHERE datum = '2026-11-03';")
a('Gib aus, aus wie vielen verschiedenen Orten die Kunden kommen.', K, 'SELECT COUNT(DISTINCT wohnort) AS orte FROM kunde;')
a('Gib den Durchschnittspreis der Vorstellungen in Saal 4 aus, gerundet auf zwei Nachkommastellen.', ['vorstellung'],
  'SELECT ROUND(AVG(preis), 2) AS durchschnittspreis FROM vorstellung WHERE saal_id = 4;')
a('Gib aus, wie viele ermäßigte Tickets verkauft wurden. Verwende `SUM()` (die Spalte enthält 1 oder 0).', ['ticket'],
  'SELECT SUM(ermaessigt) AS ermaessigt FROM ticket;')
a('Gib das Geburtsjahr des ältesten und des jüngsten Kunden aus (Spalten `aeltester` und `juengster`).', K,
  'SELECT MIN(geburtsjahr) AS aeltester, MAX(geburtsjahr) AS juengster FROM kunde;')
a('Gib aus, wie viele Filme FSK 16 oder FSK 18 haben.', F, 'SELECT COUNT(*) AS anzahl FROM film WHERE fsk >= 16;')
a('Gib aus, wie viele Tickets für die Vorstellung mit der Nummer 18 verkauft wurden.', ['ticket'],
  'SELECT COUNT(*) AS tickets FROM ticket WHERE vorstellung_id = 18;')
a('Gib den niedrigsten, den höchsten und den durchschnittlichen Eintrittspreis aus (Durchschnitt auf zwei Stellen gerundet).', ['vorstellung'],
  'SELECT MIN(preis) AS min, MAX(preis) AS max, ROUND(AVG(preis), 2) AS schnitt FROM vorstellung;')
a('Gib in einer Zeile aus, wie viele Kunden es gibt (`kunden`), wie viele davon eine E-Mail-Adresse haben (`mit_email`) und aus wie vielen verschiedenen Orten sie kommen (`orte`).', K,
  'SELECT COUNT(*) AS kunden, COUNT(email) AS mit_email, COUNT(DISTINCT wohnort) AS orte FROM kunde;')

# ---------------------------------------------------------------- 6
sec('Gruppieren mit GROUP BY und HAVING')
expl('''#### `GROUP BY`

`GROUP BY spalte` bildet **Gruppen** aus allen Zeilen mit demselben Wert in dieser Spalte. Aggregatfunktionen werden dann **pro Gruppe** berechnet.
Im `SELECT` sollten nur die Gruppierungs-Spalte und Aggregatfunktionen stehen.''',
     '''SELECT genre, COUNT(*) AS anzahl
FROM film
GROUP BY genre
ORDER BY anzahl DESC;''')
expl('''#### `HAVING`

`WHERE` wählt **Zeilen** vor dem Gruppieren aus, `HAVING` wählt **Gruppen** nach dem Gruppieren aus.
In `HAVING` darf man deshalb Aggregatfunktionen verwenden, in `WHERE` nicht.

Reihenfolge: `SELECT ... FROM ... WHERE ... GROUP BY ... HAVING ... ORDER BY ... LIMIT ...`''',
     '''SELECT wohnort, COUNT(*) AS anzahl
FROM kunde
WHERE geburtsjahr < 2000
GROUP BY wohnort
HAVING COUNT(*) >= 2;''')

V = ['vorstellung']
a('Gib für jedes Genre die Anzahl der Filme aus.', F, 'SELECT genre, COUNT(*) AS anzahl FROM film GROUP BY genre;')
a('Gib für jeden Wohnort die Anzahl der Kunden aus, den Ort mit den meisten Kunden zuerst.', K,
  'SELECT wohnort, COUNT(*) AS anzahl FROM kunde GROUP BY wohnort ORDER BY anzahl DESC;')
a('Gib für jedes Genre die durchschnittliche Filmdauer aus, auf ganze Minuten gerundet (`ROUND(..., 0)`), nach Dauer absteigend sortiert.', F,
  'SELECT genre, ROUND(AVG(dauer), 0) AS dauer FROM film GROUP BY genre ORDER BY dauer DESC;')
a('Gib für jeden Tag die Anzahl der Vorstellungen aus.', V, 'SELECT datum, COUNT(*) AS anzahl FROM vorstellung GROUP BY datum;')
a('Gib für jeden Saal (Saal-Nummer) die Anzahl der Vorstellungen und den Durchschnittspreis (zwei Stellen) aus.', V,
  'SELECT saal_id, COUNT(*) AS anzahl, ROUND(AVG(preis), 2) AS preis FROM vorstellung GROUP BY saal_id;')
a('Gib die Genres aus, zu denen es mehr als 2 Filme gibt, mit der Anzahl.', F,
  'SELECT genre, COUNT(*) AS anzahl FROM film GROUP BY genre HAVING COUNT(*) > 2;')
a('Gib die Tage aus, an denen mindestens 7 Vorstellungen stattfinden.', V,
  'SELECT datum, COUNT(*) AS anzahl FROM vorstellung GROUP BY datum HAVING COUNT(*) >= 7;')
a('Gib die Nummern der Vorstellungen aus, für die genau 6 Tickets verkauft wurden.', ['ticket'],
  'SELECT vorstellung_id FROM ticket GROUP BY vorstellung_id HAVING COUNT(*) = 6;')
a('Gib für jede Altersfreigabe (FSK) die Anzahl der Filme aus, nach FSK sortiert.', F,
  'SELECT fsk, COUNT(*) AS anzahl FROM film GROUP BY fsk ORDER BY fsk;')
a('Gib für jede Anfangszeit den Durchschnittspreis aus (zwei Stellen).', V,
  'SELECT uhrzeit, ROUND(AVG(preis), 2) AS preis FROM vorstellung GROUP BY uhrzeit;')
a('Gib für jedes Genre die Anzahl der Filme aus, zähle aber nur Filme ab 2024. Nach Anzahl absteigend, bei Gleichheit nach Genre sortiert.', F,
  'SELECT genre, COUNT(*) AS anzahl FROM film WHERE jahr >= 2024 GROUP BY genre ORDER BY anzahl DESC, genre;')
a('Gib für jede Kunden-Nummer die Anzahl der gekauften Tickets aus, aber nur für Kunden mit mehr als 8 Tickets.', ['ticket'],
  'SELECT kunde_id, COUNT(*) AS tickets FROM ticket GROUP BY kunde_id HAVING COUNT(*) > 8;')
a('Gib die Genres aus, zu denen es mehr als einen Film mit FSK 12 oder höher gibt, mit der Anzahl dieser Filme (`anzahl`), nach Genre sortiert.', F,
  'SELECT genre, COUNT(*) AS anzahl FROM film WHERE fsk >= 12 GROUP BY genre HAVING COUNT(*) > 1 ORDER BY genre;')

# ---------------------------------------------------------------- 7
sec('Tabellen verbinden mit JOIN')
expl('''#### Warum verbinden?

In der Tabelle `vorstellung` steht nur die **Nummer** des Films (`film_id`), nicht sein Titel. Den Titel findet man in der Tabelle `film`
in der Zeile mit derselben `film_id`. Mit `JOIN` verbindet man die beiden Tabellen über diese Spalte:

```sql
SELECT ... FROM vorstellung JOIN film ON vorstellung.film_id = film.film_id
```

Hinter `ON` steht die **Verknüpfungsbedingung**: Fremdschlüssel = Primärschlüssel. Kommt ein Spaltenname in beiden Tabellen vor,
schreibt man den Tabellennamen davor: `film.film_id`. Mit **Abkürzungen** (Aliasen) wird es kürzer: `FROM vorstellung v JOIN film f ON v.film_id = f.film_id`.''' + BILD,
     '''SELECT v.datum, v.uhrzeit, f.titel
FROM vorstellung v JOIN film f ON v.film_id = f.film_id
WHERE v.datum = '2026-11-02';''', anhaenge={'tabellen.png': er_bild(['film', 'vorstellung'])})
expl('''#### Die andere Schreibweise

Man kann die Tabellen auch mit Komma aufzählen und die Verknüpfungsbedingung in `WHERE` schreiben. Das Ergebnis ist dasselbe.
**Ohne** Verknüpfungsbedingung wird jede Zeile der einen mit jeder Zeile der anderen Tabelle kombiniert (das **Kreuzprodukt**), das ist fast nie gewollt.''',
     '''SELECT v.datum, v.uhrzeit, f.titel
FROM vorstellung v, film f
WHERE v.film_id = f.film_id AND v.datum = '2026-11-02';''')

FV = ['film', 'vorstellung']
SV = ['saal', 'vorstellung']
KT = ['kunde', 'ticket']
a('Gib für alle Vorstellungen am 3. November Uhrzeit und Filmtitel aus, nach Uhrzeit sortiert.', FV,
  '''SELECT v.uhrzeit, f.titel
FROM vorstellung v JOIN film f ON v.film_id = f.film_id
WHERE v.datum = '2026-11-03'
ORDER BY v.uhrzeit;''')
a('Gib für alle Vorstellungen am 3. November Uhrzeit und Saalname aus, nach Uhrzeit sortiert.', SV,
  '''SELECT v.uhrzeit, s.name
FROM vorstellung v JOIN saal s ON v.saal_id = s.saal_id
WHERE v.datum = '2026-11-03'
ORDER BY v.uhrzeit;''')
a('Gib Datum und Uhrzeit aller Vorstellungen des Films „Fußballfieber“ aus, nach Datum sortiert.', FV,
  '''SELECT v.datum, v.uhrzeit
FROM vorstellung v JOIN film f ON v.film_id = f.film_id
WHERE f.titel = 'Fußballfieber'
ORDER BY v.datum;''')
a('Gib Datum, Uhrzeit und Preis aller Vorstellungen in der „Lounge“ am 5. November aus. Verwende die Schreibweise mit Komma und `WHERE`.', SV,
  '''SELECT v.datum, v.uhrzeit, v.preis
FROM vorstellung v, saal s
WHERE v.saal_id = s.saal_id AND s.name = 'Lounge' AND v.datum = '2026-11-05';''')
a('Gib Titel, Datum und Uhrzeit aller Vorstellungen von Filmen mit FSK 0 aus, nach Datum und Uhrzeit sortiert.', FV,
  '''SELECT f.titel, v.datum, v.uhrzeit
FROM vorstellung v JOIN film f ON v.film_id = f.film_id
WHERE f.fsk = 0
ORDER BY v.datum, v.uhrzeit;''')
a('Gib Vorname, Nachname, Reihe und Platz aller Kunden mit einem Ticket für die Vorstellung 5 aus, nach Reihe und Platz sortiert.', KT,
  '''SELECT k.vorname, k.nachname, t.reihe, t.platz
FROM ticket t JOIN kunde k ON t.kunde_id = k.kunde_id
WHERE t.vorstellung_id = 5
ORDER BY t.reihe, t.platz;''')
a('Gib Vorstellungs-Nummer, Reihe und Platz aller Tickets von Lena Hoffmann aus.', KT,
  '''SELECT t.vorstellung_id, t.reihe, t.platz
FROM ticket t JOIN kunde k ON t.kunde_id = k.kunde_id
WHERE k.vorname = 'Lena' AND k.nachname = 'Hoffmann';''')
a('Gib für die Vorstellungen 1 bis 6 die Nummer, die Ausstattung des Saals und den Preis aus.', SV,
  '''SELECT v.vorstellung_id, s.ausstattung, v.preis
FROM vorstellung v JOIN saal s ON v.saal_id = s.saal_id
WHERE v.vorstellung_id <= 6;''')
v('SELECT COUNT(*) FROM film, saal;', ['film', 'saal'], hinweis='Die Tabelle `film` hat 21 Zeilen, die Tabelle `saal` hat 4 Zeilen.')
v('''SELECT COUNT(*)
FROM vorstellung v JOIN film f ON v.film_id = f.film_id;''', FV,
  hinweis='Die Tabelle `vorstellung` hat 46 Zeilen, die Tabelle `film` hat 21 Zeilen. Jede Vorstellung gehört zu genau einem Film.')

# ---------------------------------------------------------------- 8
sec('Mehrere Tabellen verbinden')
expl('''#### Ketten von JOINs

Man kann beliebig viele Tabellen verbinden, indem man mehrere `JOIN ... ON ...` hintereinander schreibt.
Für jede Verbindungslinie im Diagramm braucht man eine Verknüpfungsbedingung. Um von einem Kunden zum Filmtitel zu kommen, geht man
`kunde` → `ticket` → `vorstellung` → `film`.''' + BILD,
     '''SELECT k.vorname, k.nachname, f.titel, v.datum
FROM kunde k
JOIN ticket t ON t.kunde_id = k.kunde_id
JOIN vorstellung v ON t.vorstellung_id = v.vorstellung_id
JOIN film f ON v.film_id = f.film_id
WHERE k.nachname = 'Wagner';''', anhaenge={'tabellen.png': er_bild(['kunde', 'ticket', 'vorstellung', 'film'])})

KTVF = ['kunde', 'ticket', 'vorstellung', 'film']
a('Gib Titel, Datum und Uhrzeit aller Filme aus, die Jonas Becker gesehen hat, nach Datum sortiert.', KTVF,
  '''SELECT f.titel, v.datum, v.uhrzeit
FROM kunde k
JOIN ticket t ON t.kunde_id = k.kunde_id
JOIN vorstellung v ON t.vorstellung_id = v.vorstellung_id
JOIN film f ON v.film_id = f.film_id
WHERE k.vorname = 'Jonas' AND k.nachname = 'Becker'
ORDER BY v.datum;''')
a('Gib Vorname und Nachname aller Kunden aus, die den Film „Mission Mondbasis“ gesehen haben.', KTVF,
  '''SELECT k.vorname, k.nachname
FROM kunde k
JOIN ticket t ON t.kunde_id = k.kunde_id
JOIN vorstellung v ON t.vorstellung_id = v.vorstellung_id
JOIN film f ON v.film_id = f.film_id
WHERE f.titel = 'Mission Mondbasis';''')
a('Gib die Titel aller Filme aus, die im „Großen Saal“ laufen, jeden nur einmal und alphabetisch.', ['film', 'vorstellung', 'saal'],
  '''SELECT DISTINCT f.titel
FROM film f
JOIN vorstellung v ON v.film_id = f.film_id
JOIN saal s ON v.saal_id = s.saal_id
WHERE s.name = 'Großer Saal'
ORDER BY f.titel;''')
a('Gib Datum, Uhrzeit, Saalname und Filmtitel aller Vorstellungen am 6. November aus, nach Uhrzeit sortiert.', ['film', 'vorstellung', 'saal'],
  '''SELECT v.datum, v.uhrzeit, s.name, f.titel
FROM vorstellung v
JOIN saal s ON v.saal_id = s.saal_id
JOIN film f ON v.film_id = f.film_id
WHERE v.datum = '2026-11-06'
ORDER BY v.uhrzeit;''')
a('Gib Vorname, Nachname und Filmtitel aller Tickets von Kunden aus Havixbeck aus, nach Nachname sortiert.', KTVF,
  '''SELECT k.vorname, k.nachname, f.titel
FROM kunde k
JOIN ticket t ON t.kunde_id = k.kunde_id
JOIN vorstellung v ON t.vorstellung_id = v.vorstellung_id
JOIN film f ON v.film_id = f.film_id
WHERE k.wohnort = 'Havixbeck'
ORDER BY k.nachname;''')
a('Gib Vorname und Nachname aller Kunden aus, die einen Horrorfilm gesehen haben, jeden nur einmal und nach Nachname sortiert.', KTVF,
  '''SELECT DISTINCT k.vorname, k.nachname
FROM kunde k
JOIN ticket t ON t.kunde_id = k.kunde_id
JOIN vorstellung v ON t.vorstellung_id = v.vorstellung_id
JOIN film f ON v.film_id = f.film_id
WHERE f.genre = 'Horror'
ORDER BY k.nachname;''')
a('''Gib für alle Tickets der Vorstellungen am 8. November um 20:00 Uhr den Saalnamen, den Filmtitel, den Nachnamen des Kunden sowie Reihe und Platz aus,
nach Reihe und Platz sortiert.''', ['kunde', 'ticket', 'vorstellung', 'film', 'saal'],
  '''SELECT s.name, f.titel, k.nachname, t.reihe, t.platz
FROM ticket t
JOIN kunde k ON t.kunde_id = k.kunde_id
JOIN vorstellung v ON t.vorstellung_id = v.vorstellung_id
JOIN film f ON v.film_id = f.film_id
JOIN saal s ON v.saal_id = s.saal_id
WHERE v.datum = '2026-11-08' AND v.uhrzeit = '20:00'
ORDER BY t.reihe, t.platz;''')
a('Gib die Wohnorte aller Kunden aus, die im „Roten Saal“ waren, jeden nur einmal und alphabetisch.', ['kunde', 'ticket', 'vorstellung', 'saal'],
  '''SELECT DISTINCT k.wohnort
FROM kunde k
JOIN ticket t ON t.kunde_id = k.kunde_id
JOIN vorstellung v ON t.vorstellung_id = v.vorstellung_id
JOIN saal s ON v.saal_id = s.saal_id
WHERE s.name = 'Roter Saal'
ORDER BY k.wohnort;''')

# ---------------------------------------------------------------- 9
sec('JOIN und GROUP BY')
expl('''#### Verbinden und zusammenfassen

`JOIN` und `GROUP BY` lassen sich kombinieren: zuerst verbinden, dann gruppieren. So zählt man zum Beispiel die Tickets **pro Film**.
Gruppiert man nach dem Primärschlüssel (`f.film_id`), darf man auch die anderen Spalten dieser Tabelle (z. B. `f.titel`) ausgeben.''' + BILD,
     '''SELECT f.titel, COUNT(*) AS vorstellungen
FROM film f JOIN vorstellung v ON v.film_id = f.film_id
GROUP BY f.film_id
ORDER BY vorstellungen DESC
LIMIT 3;''', anhaenge={'tabellen.png': er_bild(['film', 'vorstellung'])})

TVF = ['ticket', 'vorstellung', 'film']
a('Gib für jeden Film die Anzahl der Vorstellungen aus, nach Anzahl absteigend und bei Gleichheit nach Titel sortiert. Nur die ersten 6.', FV,
  '''SELECT f.titel, COUNT(*) AS vorstellungen
FROM film f JOIN vorstellung v ON v.film_id = f.film_id
GROUP BY f.film_id
ORDER BY vorstellungen DESC, f.titel
LIMIT 6;''')
a('Gib die 5 Filme mit den meisten verkauften Tickets aus (Titel und Anzahl), bei Gleichheit nach Titel sortiert.', TVF,
  '''SELECT f.titel, COUNT(*) AS tickets
FROM ticket t
JOIN vorstellung v ON t.vorstellung_id = v.vorstellung_id
JOIN film f ON v.film_id = f.film_id
GROUP BY f.film_id
ORDER BY tickets DESC, f.titel
LIMIT 5;''')
a('''Gib die 5 Filme mit dem höchsten Umsatz aus: die Summe der Eintrittspreise aller verkauften Tickets (ohne Ermäßigung). Spalte `umsatz`.''', TVF,
  '''SELECT f.titel, SUM(v.preis) AS umsatz
FROM ticket t
JOIN vorstellung v ON t.vorstellung_id = v.vorstellung_id
JOIN film f ON v.film_id = f.film_id
GROUP BY f.film_id
ORDER BY umsatz DESC
LIMIT 5;''')
a('Gib für jeden Saal (Name) die Anzahl der verkauften Tickets aus, den Saal mit den meisten zuerst.', ['ticket', 'vorstellung', 'saal'],
  '''SELECT s.name, COUNT(*) AS tickets
FROM ticket t
JOIN vorstellung v ON t.vorstellung_id = v.vorstellung_id
JOIN saal s ON v.saal_id = s.saal_id
GROUP BY s.saal_id
ORDER BY tickets DESC;''')
a('Gib Vorname, Nachname und Anzahl der Tickets der 5 Kunden mit den meisten Tickets aus, bei Gleichheit nach Nachname sortiert.', KT,
  '''SELECT k.vorname, k.nachname, COUNT(*) AS tickets
FROM kunde k JOIN ticket t ON t.kunde_id = k.kunde_id
GROUP BY k.kunde_id
ORDER BY tickets DESC, k.nachname
LIMIT 5;''')
a('Gib für jeden Wohnort die Anzahl der verkauften Tickets aus, nach Anzahl absteigend sortiert.', KT,
  '''SELECT k.wohnort, COUNT(*) AS tickets
FROM kunde k JOIN ticket t ON t.kunde_id = k.kunde_id
GROUP BY k.wohnort
ORDER BY tickets DESC;''')
a('Gib für jedes Genre die Anzahl der verkauften Tickets aus, aber nur Genres mit mindestens 15 Tickets.', TVF,
  '''SELECT f.genre, COUNT(*) AS tickets
FROM ticket t
JOIN vorstellung v ON t.vorstellung_id = v.vorstellung_id
JOIN film f ON v.film_id = f.film_id
GROUP BY f.genre
HAVING COUNT(*) >= 15;''')
a('Gib für jeden Tag die Einnahmen aus allen verkauften Tickets aus (Summe der Preise, ohne Ermäßigung).', ['ticket', 'vorstellung'],
  '''SELECT v.datum, SUM(v.preis) AS einnahmen
FROM ticket t JOIN vorstellung v ON t.vorstellung_id = v.vorstellung_id
GROUP BY v.datum;''')
a('Betrachte nur ermäßigte Tickets (`ermaessigt = 1`). Gib Vorname, Nachname und die Summe der Preise dieser Tickets (Spalte `summe`) für alle Kunden aus, bei denen die Summe über 20 Euro liegt.',
  ['kunde', 'ticket', 'vorstellung'],
  '''SELECT k.vorname, k.nachname, SUM(v.preis) AS summe
FROM kunde k
JOIN ticket t ON t.kunde_id = k.kunde_id
JOIN vorstellung v ON t.vorstellung_id = v.vorstellung_id
WHERE t.ermaessigt = 1
GROUP BY k.kunde_id
HAVING SUM(v.preis) > 20;''')

# ---------------------------------------------------------------- 10
sec('LEFT JOIN')
expl('''#### Zeilen ohne Partner

`JOIN` (genauer `INNER JOIN`) gibt nur Zeilen aus, die in **beiden** Tabellen einen Partner haben. Ein Film ohne Vorstellung fehlt also im Ergebnis.

`LEFT JOIN` gibt **alle** Zeilen der linken Tabelle aus. Hat eine Zeile keinen Partner, stehen in den Spalten der rechten Tabelle `NULL`-Werte.
Damit findet man Zeilen **ohne** Partner (`WHERE rechts.spalte IS NULL`) oder zählt auch Nullen mit (`COUNT(rechts.spalte)`).''' + BILD,
     '''SELECT f.titel, COUNT(v.vorstellung_id) AS vorstellungen
FROM film f LEFT JOIN vorstellung v ON v.film_id = f.film_id
GROUP BY f.film_id
ORDER BY vorstellungen
LIMIT 6;''', anhaenge={'tabellen.png': er_bild(['film', 'vorstellung'])})

a('Gib die Titel aller Filme aus, für die es **keine** Vorstellung gibt.', FV,
  '''SELECT f.titel
FROM film f LEFT JOIN vorstellung v ON v.film_id = f.film_id
WHERE v.vorstellung_id IS NULL;''')
a('Gib Vorname und Nachname aller Kunden aus, die **kein** Ticket gekauft haben.', KT,
  '''SELECT k.vorname, k.nachname
FROM kunde k LEFT JOIN ticket t ON t.kunde_id = k.kunde_id
WHERE t.ticket_id IS NULL;''')
a('Gib für die 5 Kunden mit den wenigsten Tickets Vorname, Nachname und Anzahl (auch 0) aus, bei Gleichheit nach Nachname sortiert.', KT,
  '''SELECT k.vorname, k.nachname, COUNT(t.ticket_id) AS tickets
FROM kunde k LEFT JOIN ticket t ON t.kunde_id = k.kunde_id
GROUP BY k.kunde_id
ORDER BY tickets, k.nachname
LIMIT 5;''')
a('Gib Nummer, Datum und Uhrzeit aller Vorstellungen aus, für die kein einziges Ticket verkauft wurde.', ['vorstellung', 'ticket'],
  '''SELECT v.vorstellung_id, v.datum, v.uhrzeit
FROM vorstellung v LEFT JOIN ticket t ON t.vorstellung_id = v.vorstellung_id
WHERE t.ticket_id IS NULL;''')
a('Gib für jedes Genre die Anzahl der Vorstellungen aus, auch wenn sie 0 ist, nach Genre sortiert.', FV,
  '''SELECT f.genre, COUNT(v.vorstellung_id) AS vorstellungen
FROM film f LEFT JOIN vorstellung v ON v.film_id = f.film_id
GROUP BY f.genre
ORDER BY f.genre;''')
v('''SELECT COUNT(*)
FROM film f LEFT JOIN vorstellung v ON v.film_id = f.film_id;''', FV,
  hinweis='Die Tabelle `vorstellung` hat 46 Zeilen, die Tabelle `film` hat 21 Zeilen. 4 der Filme haben keine Vorstellung.')

# ---------------------------------------------------------------- 11
sec('Unterabfragen')
expl('''#### Abfragen in Abfragen

Eine **Unterabfrage** ist eine `SELECT`-Anweisung in Klammern innerhalb einer anderen Anweisung.

- Liefert sie **einen** Wert, kann man damit vergleichen: `WHERE dauer > (SELECT AVG(dauer) FROM film)`.
- Liefert sie eine **Spalte** mit mehreren Werten, prüft man mit `IN` bzw. `NOT IN`, ob ein Wert darin vorkommt.

Erst wird die Unterabfrage ausgewertet, dann die äußere Abfrage.''',
     '''SELECT titel, dauer
FROM film
WHERE dauer > (SELECT AVG(dauer) FROM film)
ORDER BY dauer DESC;''')

a('Gib Titel und Dauer aller Filme aus, die kürzer als der Durchschnitt sind, nach Dauer sortiert.', F,
  '''SELECT titel, dauer
FROM film
WHERE dauer < (SELECT AVG(dauer) FROM film)
ORDER BY dauer;''')
a('Gib Titel und Dauer des längsten Films aus. Verwende eine Unterabfrage mit `MAX()`.', F,
  'SELECT titel, dauer FROM film WHERE dauer = (SELECT MAX(dauer) FROM film);')
a('Gib Vorname, Nachname und Geburtsjahr des ältesten Kunden aus.', K,
  'SELECT vorname, nachname, geburtsjahr FROM kunde WHERE geburtsjahr = (SELECT MIN(geburtsjahr) FROM kunde);')
a('Gib die Titel aller Filme aus, die in der „Lounge“ laufen. Verwende zwei verschachtelte Unterabfragen mit `IN` und `=` (ohne JOIN).', ['film', 'vorstellung', 'saal'],
  '''SELECT titel
FROM film
WHERE film_id IN (SELECT film_id FROM vorstellung
                  WHERE saal_id = (SELECT saal_id FROM saal WHERE name = 'Lounge'));''')
a('Gib Vorname und Nachname aller Kunden aus, die kein Ticket gekauft haben. Verwende diesmal `NOT IN`.', KT,
  'SELECT vorname, nachname FROM kunde WHERE kunde_id NOT IN (SELECT kunde_id FROM ticket);')
a('Gib Datum, Uhrzeit und Preis aller Vorstellungen am 6. November aus, deren Preis unter dem Durchschnittspreis aller Vorstellungen liegt.', V,
  '''SELECT datum, uhrzeit, preis
FROM vorstellung
WHERE datum = '2026-11-06' AND preis < (SELECT AVG(preis) FROM vorstellung);''')
a('Gib Vorname und Nachname aller Kunden aus, die älter sind als der Durchschnitt aller Kunden, nach Geburtsjahr sortiert.', K,
  '''SELECT vorname, nachname
FROM kunde
WHERE geburtsjahr < (SELECT AVG(geburtsjahr) FROM kunde)
ORDER BY geburtsjahr;''')
a('Gib die Titel aller Filme aus dem Genre des Films „Kettenreaktion“ aus (ohne „Kettenreaktion“ selbst).', F,
  '''SELECT titel
FROM film
WHERE genre = (SELECT genre FROM film WHERE titel = 'Kettenreaktion') AND titel <> 'Kettenreaktion';''')
a('Gib aus, wie viele Filme keine einzige Vorstellung haben (`ohne_vorstellung`). Verwende eine Unterabfrage mit `NOT IN`.', FV,
  'SELECT COUNT(*) AS ohne_vorstellung FROM film WHERE film_id NOT IN (SELECT film_id FROM vorstellung);')

# ---------------------------------------------------------------- 12
sec('Funktionen und CASE')
expl('''#### Text- und Datumsfunktionen

| Funktion | Ergebnis |
|---|---|
| `UPPER(t)`, `LOWER(t)` | Text in Groß- bzw. Kleinbuchstaben (nur ohne Umlaute zuverlässig) |
| `LENGTH(t)` | Anzahl der Zeichen |
| `SUBSTR(t, start, anzahl)` | Teil des Textes ab Position `start` (die erste Position ist 1) |
| `REPLACE(t, alt, neu)` | ersetzt Textstellen |
| `strftime('%d.%m.%Y', datum)` | Datum in einer anderen Form, hier `02.11.2026` |
| `strftime('%w', datum)` | Wochentag als Text: `'0'` Sonntag, `'1'` Montag, ..., `'6'` Samstag |''',
     '''SELECT titel, LENGTH(titel) AS laenge, SUBSTR(titel, 1, 5) AS anfang
FROM film
WHERE genre = 'Animation';''')
expl('''#### `CASE`

Mit `CASE` berechnet man je nach Bedingung einen anderen Wert, ähnlich wie `if` / `elif` / `else`:

```sql
CASE WHEN bedingung1 THEN wert1
     WHEN bedingung2 THEN wert2
     ELSE wert3 END
```

Die Bedingungen werden der Reihe nach geprüft, der erste passende Wert wird genommen.''',
     '''SELECT titel, fsk,
       CASE WHEN fsk = 0 THEN 'alle'
            WHEN fsk <= 12 THEN 'Kinder und Jugendliche'
            ELSE 'Erwachsene' END AS zielgruppe
FROM film
WHERE genre = 'Komödie';''')

a('Gib für alle Komödien den Titel in Großbuchstaben (Spalte `gross`) und die Anzahl der Zeichen des Titels (Spalte `zeichen`) aus.', F,
  "SELECT UPPER(titel) AS gross, LENGTH(titel) AS zeichen FROM film WHERE genre = 'Komödie';")
a('Gib für alle Kunden aus Telgte den abgekürzten Namen aus, z. B. `L. Klein` (Spalte `name`).', K,
  "SELECT SUBSTR(vorname, 1, 1) || '. ' || nachname AS name FROM kunde WHERE wohnort = 'Telgte';")
a('Gib alle Spieltage im deutschen Format (z. B. `02.11.2026`) aus, jeden nur einmal (Spalte `tag`).', V,
  "SELECT DISTINCT strftime('%d.%m.%Y', datum) AS tag FROM vorstellung;")
a('Gib für alle Kunden aus Greven Vorname und Alter im Jahr 2026 aus, die jüngsten zuerst.', K,
  "SELECT vorname, 2026 - geburtsjahr AS alter_2026 FROM kunde WHERE wohnort = 'Greven' ORDER BY alter_2026;")
a('''Gib für alle Filme aus 2025 den Titel, die Dauer und eine Spalte `laenge` aus: `kurz` unter 100 Minuten, `mittel` bis 120 Minuten, sonst `lang`.
Nach Dauer sortiert.''', F,
  '''SELECT titel, dauer,
       CASE WHEN dauer < 100 THEN 'kurz'
            WHEN dauer <= 120 THEN 'mittel'
            ELSE 'lang' END AS laenge
FROM film
WHERE jahr = 2025
ORDER BY dauer;''')
a('Gib aus, wie viele Filme kurz, mittel und lang sind (Einteilung wie in der vorigen Aufgabe). Gruppiere nach dem `CASE`-Ausdruck.', F,
  '''SELECT CASE WHEN dauer < 100 THEN 'kurz'
            WHEN dauer <= 120 THEN 'mittel'
            ELSE 'lang' END AS laenge,
       COUNT(*) AS anzahl
FROM film
GROUP BY laenge;''')
a('''Berechne die tatsächlichen Gesamteinnahmen: Ermäßigte Tickets kosten 80 % des Preises. Verwende `CASE` in `SUM()` und runde auf zwei Nachkommastellen.''',
  ['ticket', 'vorstellung'],
  '''SELECT ROUND(SUM(CASE WHEN t.ermaessigt = 1 THEN v.preis * 0.8 ELSE v.preis END), 2) AS einnahmen
FROM ticket t JOIN vorstellung v ON t.vorstellung_id = v.vorstellung_id;''')
a("Gib aus, wie viele Vorstellungen am Wochenende (Samstag und Sonntag) stattfinden. Verwende `strftime('%w', datum)`.", V,
  "SELECT COUNT(*) AS wochenende FROM vorstellung WHERE strftime('%w', datum) IN ('0', '6');")
a('Gib die E-Mail-Adressen aller Kunden aus Senden aus. Fehlt sie, soll `keine` dastehen. Tipp: `CASE WHEN email IS NULL THEN ...`.', K,
  "SELECT vorname, CASE WHEN email IS NULL THEN 'keine' ELSE email END AS email FROM kunde WHERE wohnort = 'Senden';")
v("SELECT LENGTH('Kino'), SUBSTR('Kinosaal', 5, 4), REPLACE('2026-11-02', '-', '.');", [])

# ---------------------------------------------------------------- 13
sec('Gemischte Übungen')
a('Welcher Film hat die meisten Zuschauer? Gib Titel und Anzahl der Tickets aus (nur die erste Zeile).', TVF,
  '''SELECT f.titel, COUNT(*) AS zuschauer
FROM ticket t
JOIN vorstellung v ON t.vorstellung_id = v.vorstellung_id
JOIN film f ON v.film_id = f.film_id
GROUP BY f.film_id
ORDER BY zuschauer DESC
LIMIT 1;''')
a('''Gib für jede Vorstellung am Samstag, dem 7. November, Uhrzeit, Saalname, verkaufte Tickets und die Auslastung in Prozent (eine Nachkommastelle) aus.
Auch Vorstellungen ohne Tickets sollen erscheinen. Nach Uhrzeit sortiert.''', ['ticket', 'vorstellung', 'saal'],
  '''SELECT v.uhrzeit, s.name, COUNT(t.ticket_id) AS tickets, ROUND(COUNT(t.ticket_id) * 100.0 / s.plaetze, 1) AS prozent
FROM vorstellung v
JOIN saal s ON v.saal_id = s.saal_id
LEFT JOIN ticket t ON t.vorstellung_id = v.vorstellung_id
WHERE v.datum = '2026-11-07'
GROUP BY v.vorstellung_id
ORDER BY v.uhrzeit;''')
a('Gib Vorname und Nachname der Kunden aus, die Filme aus mindestens 5 verschiedenen Genres gesehen haben, mit der Anzahl der Genres.', KTVF,
  '''SELECT k.vorname, k.nachname, COUNT(DISTINCT f.genre) AS genres
FROM kunde k
JOIN ticket t ON t.kunde_id = k.kunde_id
JOIN vorstellung v ON t.vorstellung_id = v.vorstellung_id
JOIN film f ON v.film_id = f.film_id
GROUP BY k.kunde_id
HAVING COUNT(DISTINCT f.genre) >= 5;''')
a('Gib für jedes Genre das Durchschnittsalter der Zuschauer im Jahr 2026 aus (eine Nachkommastelle), das jüngste Publikum zuerst.', KTVF,
  '''SELECT f.genre, ROUND(AVG(2026 - k.geburtsjahr), 1) AS alter_schnitt
FROM kunde k
JOIN ticket t ON t.kunde_id = k.kunde_id
JOIN vorstellung v ON t.vorstellung_id = v.vorstellung_id
JOIN film f ON v.film_id = f.film_id
GROUP BY f.genre
ORDER BY alter_schnitt;''')
a('Gib Vorname und Nachname aller Kunden aus, die zusammen mit Lena Hoffmann in einer Vorstellung waren (ohne Lena selbst), jeden nur einmal.', KT,
  '''SELECT DISTINCT k.vorname, k.nachname
FROM kunde k JOIN ticket t ON t.kunde_id = k.kunde_id
WHERE t.vorstellung_id IN (SELECT t2.vorstellung_id
                           FROM ticket t2 JOIN kunde k2 ON t2.kunde_id = k2.kunde_id
                           WHERE k2.vorname = 'Lena' AND k2.nachname = 'Hoffmann')
  AND NOT (k.vorname = 'Lena' AND k.nachname = 'Hoffmann');''')
a('Gib den Saal mit den höchsten Einnahmen (Summe der Preise aller Tickets, ohne Ermäßigung) mit den Einnahmen aus.', ['ticket', 'vorstellung', 'saal'],
  '''SELECT s.name, SUM(v.preis) AS einnahmen
FROM ticket t
JOIN vorstellung v ON t.vorstellung_id = v.vorstellung_id
JOIN saal s ON v.saal_id = s.saal_id
GROUP BY s.saal_id
ORDER BY einnahmen DESC
LIMIT 1;''')
a('Gib Titel und Anzahl der Tickets aller Filme mit FSK 16 oder 18 aus, die von Kunden unter 25 Jahren (im Jahr 2026) gesehen wurden, nach Anzahl absteigend.', KTVF,
  '''SELECT f.titel, COUNT(*) AS tickets
FROM kunde k
JOIN ticket t ON t.kunde_id = k.kunde_id
JOIN vorstellung v ON t.vorstellung_id = v.vorstellung_id
JOIN film f ON v.film_id = f.film_id
WHERE f.fsk >= 16 AND 2026 - k.geburtsjahr < 25
GROUP BY f.film_id
ORDER BY tickets DESC;''')
a('''Gib für jeden Wochentag (Spalte `wochentag` mit `strftime('%w', datum)`) die Zahl der verkauften Tickets aus, nach Wochentag sortiert.''', ['ticket', 'vorstellung'],
  '''SELECT strftime('%w', v.datum) AS wochentag, COUNT(*) AS tickets
FROM ticket t JOIN vorstellung v ON t.vorstellung_id = v.vorstellung_id
GROUP BY wochentag
ORDER BY wochentag;''')

generate('sql_abfragen', 'SQL-Abfragen mit SQLite', INTRO, sprache='sqlite', ausfuehren=sql_ausfuehrung(INHALT))
