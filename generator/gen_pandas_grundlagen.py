# Erzeugt ../content/pandas_grundlagen.ipynb (siehe nbgen.py). Erstes Notebook der pandas-Reihe:
# pandas_grundlagen, pandas_auswaehlen, pandas_gruppieren, pandas_verbinden_zeit, pandas_diagramme_anwendungen.
#
# JupyterLite: pandas 3.0.2 (lokal pip install pandas==3.0.2, ohne pyarrow wie im Browser). Copy-on-Write: Werte nur mit loc ändern.
# Erwartete Ausgaben wie in JupyterLab (pandasnb.py): DataFrames als HTML-Tabelle (letzte Zeile oder display()), sonst Text.
# Keine Ausgaben von info() (Speicherangaben hängen von der Plattform ab).
import pandasnb
from nbgen import sec, expl, task, predict, generate, setup


def t(text, given='', body='', kind='normal'):
    """Aufgabe, deren Lösung aus dem vorgegebenen Code plus body besteht."""
    task(text, given=given, solution=(given + '\n' + body) if given else body, kind=kind)


DATEIEN = r"""dateien = {
    'schueler.csv': '''name;klasse;alter;wohnort;mathe;deutsch;englisch;fehltage
Ali;9a;15;Tübingen;2;3;2;4
Bea;9a;14;Rottenburg;1;2;1;0
Cem;9b;15;Tübingen;3;3;4;7
Dana;9b;16;Mössingen;2;1;2;2
Emil;9a;15;Tübingen;4;3;3;12
Fiona;9c;14;Rottenburg;1;1;2;1
Gus;9c;15;Mössingen;3;4;3;5
Hanna;9b;14;Tübingen;2;2;1;0
Ida;9c;15;Tübingen;2;3;3;3
Jan;9a;16;Rottenburg;5;4;4;15
Kim;9b;15;Mössingen;1;2;2;1
Lea;9c;14;Tübingen;3;2;2;6
''',
    'laender.csv': '''land,kuerzel,hauptstadt,einwohner,flaeche
Baden-Württemberg,BW,Stuttgart,11280,35748
Bayern,BY,München,13370,70542
Berlin,BE,Berlin,3760,891
Brandenburg,BB,Potsdam,2570,29654
Bremen,HB,Bremen,680,419
Hamburg,HH,Hamburg,1890,755
Hessen,HE,Wiesbaden,6390,21116
Mecklenburg-Vorpommern,MV,Schwerin,1630,23295
Niedersachsen,NI,Hannover,8140,47710
Nordrhein-Westfalen,NW,Düsseldorf,18140,34112
Rheinland-Pfalz,RP,Mainz,4160,19858
Saarland,SL,Saarbrücken,990,2571
Sachsen,SN,Dresden,4090,18450
Sachsen-Anhalt,ST,Magdeburg,2180,20459
Schleswig-Holstein,SH,Kiel,2950,15804
Thüringen,TH,Erfurt,2130,16202
''',
}
for name, inhalt in dateien.items():
    with open(name, 'w', encoding='utf-8') as f:
        f.write(inhalt)
print('Angelegt:', ', '.join(dateien))"""

INTRO = '''**pandas** ist das wichtigste Python-Paket für **Tabellen**. Mit pandas liest man Daten (z. B. aus CSV-Dateien) ein, wählt aus, rechnet, gruppiert und
erstellt Diagramme, ähnlich wie mit einer Tabellenkalkulation, aber mit Programmcode.

Die Reihe hat fünf Notebooks:

1. **Grundlagen**: Series und DataFrame, Spalten, Sortieren, CSV-Dateien (dieses Notebook)
2. Auswählen und aufräumen: Filtern, Text-Spalten, fehlende Werte
3. Gruppieren und auswerten: Aggregatfunktionen, groupby, Pivot-Tabellen, Vergleich mit SQL
4. Verbinden und Zeitreihen: merge, concat, Datum und Zeit
5. Diagramme und Anwendungen

**Tabellen anzeigen:** Steht ein DataFrame (eine Tabelle) in der **letzten Zeile** einer Zelle, zeigt JupyterLab ihn als Tabelle an. Mehrere Tabellen in einer Zelle zeigt man mit
`display(df)` an. Einzelne Werte gibt man wie gewohnt mit `print()` aus. Die erwarteten Ausgaben in den Aufgaben sehen genauso aus.

Du solltest Listen, Dictionaries, `lambda` und das Notebook zu Dateien schon kennen.

Jeder Abschnitt beginnt mit kurzen Erklärungen und Beispielen. Führe die Beispiele aus und probiere sie ruhig ein wenig aus.
Danach folgen viele kleine Übungen. Wenn etwas vorgegeben ist, steht es schon in der Codezelle.'''

setup('''#### Beispieldateien anlegen

**Führe diese Zelle zuerst aus.** Sie legt die Dateien `schueler.csv` (ausgedachte Daten) und `laender.csv` (Einwohner in Tausend und Fläche in km² der Bundesländer,
gerundet, Stand etwa 2023) an, mit denen im Abschnitt über CSV-Dateien gearbeitet wird.''', DATEIEN)

# ---------------------------------------------------------------- 1
sec('Series')
expl('''#### Eine Spalte: `Series`

Man importiert pandas üblicherweise als `pd`. Eine **Series** ist eine Spalte von Werten mit einem **Index** (den Zeilenbeschriftungen).

- `pd.Series([3, 5, 2])` hat den Index 0, 1, 2.
- `pd.Series([3, 5, 2], index=['Mo', 'Di', 'Mi'])` oder `pd.Series({'Mo': 3, 'Di': 5, 'Mi': 2})` hat eigene Beschriftungen.
- `s['Di']` gibt den Wert zur Beschriftung zurück, `s.iloc[0]` den Wert an Position 0.
- `s.values` sind die Werte (als numpy-Array), `s.index` die Beschriftungen.

Steht eine Series in der letzten Zeile, zeigt JupyterLab sie als Text an: links der Index, rechts die Werte, darunter der Datentyp.''',
     """import pandas as pd

regen = pd.Series({'Mo': 3, 'Di': 5, 'Mi': 0, 'Do': 2})
print(regen['Di'], regen.iloc[0])
print(list(regen.index))
regen""")
expl('''#### Rechnen mit Series

Rechnungen wirken auf **alle Werte auf einmal**: `s * 2`, `s + 1`, `s > 2`. Dazu gibt es viele Methoden:
`sum()`, `mean()`, `min()`, `max()`, `count()` (Anzahl), `idxmax()` (Index des größten Wertes), `sort_values()`.''',
     """import pandas as pd

regen = pd.Series({'Mo': 3, 'Di': 5, 'Mi': 0, 'Do': 2})
print(regen.sum(), regen.mean(), regen.max(), regen.idxmax())
regen * 10""")

t('''Erzeuge eine Series `punkte` mit den Punkten 12, 7, 15, 9 und den Namen Ali, Bea, Cem, Dana als Index. Lass sie anzeigen (letzte Zeile).''',
  "import pandas as pd",
  """punkte = pd.Series([12, 7, 15, 9], index=['Ali', 'Bea', 'Cem', 'Dana'])
punkte""")
t('Gib die Punkte von Cem, die Summe und den Durchschnitt aller Punkte aus.',
  "import pandas as pd\n\npunkte = pd.Series({'Ali': 12, 'Bea': 7, 'Cem': 15, 'Dana': 9})",
  """print(punkte['Cem'])
print(punkte.sum(), punkte.mean())""")
t('Gib den Namen mit den meisten und den mit den wenigsten Punkten aus (`idxmax`, `idxmin`).',
  "import pandas as pd\n\npunkte = pd.Series({'Ali': 12, 'Bea': 7, 'Cem': 15, 'Dana': 9})",
  "print(punkte.idxmax(), punkte.idxmin())")
t('Jeder bekommt 3 Bonuspunkte. Lass die neuen Punkte nach der Größe sortiert anzeigen, die meisten zuerst (`sort_values(ascending=False)`).',
  "import pandas as pd\n\npunkte = pd.Series({'Ali': 12, 'Bea': 7, 'Cem': 15, 'Dana': 9})",
  "(punkte + 3).sort_values(ascending=False)")
t('Rechne die Temperaturen von Celsius in Fahrenheit um (F = C · 9/5 + 32) und lass das Ergebnis anzeigen.',
  "import pandas as pd\n\ncelsius = pd.Series({'Mo': 12.5, 'Di': 15.0, 'Mi': 10.0, 'Do': 20.0})",
  "celsius * 9 / 5 + 32")
t('Lass für jeden Tag anzeigen, ob die Temperatur über 12 °C lag (eine Series mit `True`/`False`). Gib danach aus, an wie vielen Tagen das so war (`sum()` zählt die `True`).',
  "import pandas as pd\n\ncelsius = pd.Series({'Mo': 12.5, 'Di': 15.0, 'Mi': 10.0, 'Do': 20.0})",
  """warm = celsius > 12
print(warm.sum())
warm""")
predict("""import pandas as pd

s = pd.Series([4, 1, 7])
print(s.iloc[2], s.max(), s.count())
print(list(s * 2))""")

# ---------------------------------------------------------------- 2
sec('DataFrames erstellen')
expl('''#### Eine Tabelle: `DataFrame`

Ein **DataFrame** ist eine Tabelle: mehrere Spalten (jede eine Series) mit gemeinsamem Index. Man erzeugt ihn z. B. aus einem **Dictionary von Listen**
(Spaltenname → Werte) oder aus einer **Liste von Dictionaries** (eine Zeile pro Dictionary).

| Attribut | Ergebnis |
|---|---|
| `df.shape` | (Anzahl Zeilen, Anzahl Spalten) |
| `len(df)` | Anzahl Zeilen |
| `list(df.columns)` | Spaltennamen |
| `df.head(n)`, `df.tail(n)` | die ersten bzw. letzten n Zeilen (Standard 5) |''',
     """import pandas as pd

df = pd.DataFrame({'name': ['Ali', 'Bea', 'Cem'], 'alter': [15, 14, 15], 'note': [2.0, 1.3, 2.7]})
print(df.shape, len(df), list(df.columns))
df""")
expl('''#### Aus einer Liste von Dictionaries

Jedes Dictionary ist eine Zeile. Fehlt ein Wert, steht dort `NaN` (*not a number*, „fehlt“).''',
     """import pandas as pd

zeilen = [{'stadt': 'Ulm', 'einwohner': 128928}, {'stadt': 'Tübingen', 'einwohner': 91877, 'fluss': 'Neckar'}]
pd.DataFrame(zeilen)""")

t('Erzeuge einen DataFrame `filme` mit den Spalten `titel`, `jahr` und `minuten` für Momo (1986, 101), Shrek (2001, 90) und Avatar (2009, 162) und lass ihn anzeigen.',
  "import pandas as pd",
  """filme = pd.DataFrame({'titel': ['Momo', 'Shrek', 'Avatar'], 'jahr': [1986, 2001, 2009], 'minuten': [101, 90, 162]})
filme""")
t('Erzeuge den DataFrame aus der Liste `zeilen` und gib Anzahl der Zeilen und die Spaltennamen aus. Lass die Tabelle danach anzeigen.',
  "import pandas as pd\n\nzeilen = [{'tag': 'Mo', 'schritte': 8200}, {'tag': 'Di', 'schritte': 10400}, {'tag': 'Mi', 'schritte': 6100}, {'tag': 'Do', 'schritte': 12000}]",
  """df = pd.DataFrame(zeilen)
print(len(df), list(df.columns))
df""")
t('Lass die ersten 2 und die letzten 2 Zeilen von `df` anzeigen (zwei Tabellen, also mit `display()`).',
  "import pandas as pd\n\ndf = pd.DataFrame({'tag': ['Mo', 'Di', 'Mi', 'Do', 'Fr', 'Sa'], 'schritte': [8200, 10400, 6100, 12000, 9500, 15300]})",
  """display(df.head(2))
display(df.tail(2))""")
t('''Erzeuge aus zwei Listen `namen` und `punkte` einen DataFrame mit den Spalten `name` und `punkte` und gib `shape` aus.''',
  "import pandas as pd\n\nnamen = ['Ali', 'Bea', 'Cem', 'Dana', 'Emil']\npunkte = [17, 23, 12, 19, 21]",
  """df = pd.DataFrame({'name': namen, 'punkte': punkte})
print(df.shape)""")
predict("""import pandas as pd

df = pd.DataFrame({'a': [1, 2, 3, 4], 'b': [5, 6, 7, 8], 'c': [9, 10, 11, 12]})
print(df.shape)
print(list(df.columns), len(df))""")

# ---------------------------------------------------------------- 3
sec('Spalten auswählen und berechnen')
expl('''#### Spalten

- `df['spalte']` ist eine Spalte (eine Series), `df[['a', 'b']]` (mit **doppelten** Klammern) ein DataFrame mit diesen Spalten.
- `df['neu'] = ...` legt eine neue Spalte an, z. B. berechnet aus anderen: `df['summe'] = df['a'] + df['b']`.
- `df.rename(columns={'alt': 'neu'})` benennt um, `df.drop(columns=['a'])` entfernt Spalten. Beide geben einen **neuen** DataFrame zurück.
- Methoden wie `sum()`, `mean()`, `max()` gibt es auch für Spalten: `df['note'].mean()`.''',
     """import pandas as pd

df = pd.DataFrame({'name': ['Ali', 'Bea', 'Cem'], 'mathe': [2, 1, 3], 'deutsch': [3, 2, 3]})
df['schnitt'] = (df['mathe'] + df['deutsch']) / 2
print(df['mathe'].mean())
display(df[['name', 'schnitt']])
df.rename(columns={'name': 'vorname'}).drop(columns=['schnitt'])""")
expl('''#### `describe()`

`df.describe()` zeigt für jede Zahlenspalte die wichtigsten Kennzahlen: Anzahl (`count`), Mittelwert (`mean`), Standardabweichung (`std`), Minimum, Quartile (25 %, 50 % = Median, 75 %) und Maximum.''',
     """import pandas as pd

df = pd.DataFrame({'mathe': [2, 1, 3, 2], 'deutsch': [3, 2, 3, 1]})
df.describe()""")

NOTEN = ("import pandas as pd\n\ndf = pd.DataFrame({'name': ['Ali', 'Bea', 'Cem', 'Dana', 'Emil'], 'mathe': [2, 1, 3, 2, 4], 'deutsch': [3, 2, 3, 1, 3],\n"
         "                   'englisch': [2, 1, 4, 2, 3]})")
t('Lass nur die Spalten `name` und `englisch` anzeigen.', NOTEN, "df[['name', 'englisch']]")
t('Gib den Durchschnitt in Mathe, die beste (kleinste) Deutschnote und die Summe aller Englischnoten aus.', NOTEN,
  """print(df['mathe'].mean())
print(df['deutsch'].min())
print(df['englisch'].sum())""")
t('Berechne eine neue Spalte `schnitt` mit dem Durchschnitt der drei Fächer (auf 2 Stellen mit `.round(2)`) und lass die Tabelle anzeigen.', NOTEN,
  """df['schnitt'] = ((df['mathe'] + df['deutsch'] + df['englisch']) / 3).round(2)
df""")
t('Benenne die Spalte `mathe` in `Mathematik` um, entferne die Spalte `englisch` und lass das Ergebnis anzeigen.', NOTEN,
  "df.rename(columns={'mathe': 'Mathematik'}).drop(columns=['englisch'])")
t('Lass `describe()` für die drei Notenspalten anzeigen.', NOTEN,
  "df[['mathe', 'deutsch', 'englisch']].describe()")
t('''Lege eine Spalte `bestanden` an, die `True` ist, wenn die Mathenote besser als 4 ist (`< 4`), und lass die Spalten `name`, `mathe`, `bestanden` anzeigen.''', NOTEN,
  """df['bestanden'] = df['mathe'] < 4
df[['name', 'mathe', 'bestanden']]""")
t('Gib die Spalte `name` als gewöhnliche Python-Liste aus (`list()` oder `.tolist()`).', NOTEN,
  "print(df['name'].tolist())")
predict("""import pandas as pd

df = pd.DataFrame({'x': [1, 2, 3], 'y': [10, 20, 30]})
df['z'] = df['x'] * df['y']
print(df['z'].sum(), list(df.columns))""")

# ---------------------------------------------------------------- 4
sec('Sortieren und Zeilen auswählen')
expl('''#### Sortieren

`df.sort_values('spalte')` sortiert nach einer Spalte, `ascending=False` absteigend. Nach mehreren Spalten: `df.sort_values(['klasse', 'name'])`
(mit `ascending=[True, False]` für jede Spalte einzeln). Der Index bleibt dabei an seiner Zeile.''',
     """import pandas as pd

df = pd.DataFrame({'name': ['Cem', 'Ali', 'Bea'], 'klasse': ['9b', '9a', '9a'], 'punkte': [12, 17, 23]})
display(df.sort_values('punkte', ascending=False))
df.sort_values(['klasse', 'name'])""")
expl('''#### Zeilen mit `loc` und `iloc`

- `df.iloc[0]` ist die Zeile an **Position** 0, `df.iloc[1:3]` die Zeilen an Position 1 und 2 (wie bei Listen).
- `df.loc[beschriftung]` ist die Zeile mit diesem **Index**, `df.loc[beschriftung, 'spalte']` ein einzelner Wert.
- `df.set_index('name')` macht eine Spalte zum Index; dann kann man mit `df.loc['Bea']` nach Namen suchen. `reset_index()` macht den Index wieder zur Spalte.

Ein einzelner Wert wird **geändert** mit `df.loc[zeile, 'spalte'] = wert`.''',
     """import pandas as pd

df = pd.DataFrame({'name': ['Ali', 'Bea', 'Cem'], 'punkte': [17, 23, 12]}).set_index('name')
print(df.loc['Bea', 'punkte'])
print(df.iloc[0]['punkte'])
df.loc['Cem', 'punkte'] = 14
df""")

SPIEL = ("import pandas as pd\n\ndf = pd.DataFrame({'name': ['Luna', 'Max', 'Ida', 'Tom', 'Mia', 'Ben'], 'level': [7, 9, 7, 3, 9, 5],\n"
         "                   'punkte': [4200, 5100, 3900, 1200, 4800, 2600]})")
t('Lass die Spieler nach Punkten absteigend sortiert anzeigen.', SPIEL, "df.sort_values('punkte', ascending=False)")
t('Lass die Spieler nach Level absteigend und bei gleichem Level nach Name aufsteigend sortiert anzeigen.', SPIEL,
  "df.sort_values(['level', 'name'], ascending=[False, True])")
t('Lass die drei Spieler mit den meisten Punkten anzeigen (sortieren und `head(3)`).', SPIEL,
  "df.sort_values('punkte', ascending=False).head(3)")
t('Mache `name` zum Index. Gib die Punkte von Ida aus und lass dann die Zeilen an den Positionen 1 bis 3 anzeigen (`iloc`).', SPIEL,
  """df = df.set_index('name')
print(df.loc['Ida', 'punkte'])
df.iloc[1:4]""")
t('''Tom steigt ein Level auf und bekommt 500 Punkte dazu. Ändere seine Werte mit `loc` (Index ist `name`) und lass seine Zeile als Tabelle anzeigen (`df.loc[['Tom']]`).''', SPIEL,
  """df = df.set_index('name')
df.loc['Tom', 'level'] = df.loc['Tom', 'level'] + 1
df.loc['Tom', 'punkte'] = df.loc['Tom', 'punkte'] + 500
df.loc[['Tom']]""")
t('''Sortiere nach Punkten absteigend und füge eine Spalte `platz` mit den Plätzen 1 bis 6 hinzu (`range(1, 7)`). Setze danach mit `reset_index(drop=True)` einen neuen Index 0 bis 5
und lass die Tabelle anzeigen.''', SPIEL,
  """df = df.sort_values('punkte', ascending=False).reset_index(drop=True)
df['platz'] = range(1, 7)
df""")
predict("""import pandas as pd

df = pd.DataFrame({'n': [5, 3, 8]}, index=['a', 'b', 'c'])
print(df.loc['b', 'n'], df.iloc[2]['n'])
print(list(df.sort_values('n').index))""")

# ---------------------------------------------------------------- 5
sec('CSV-Dateien')
expl('''#### Einlesen mit `read_csv`

`pd.read_csv('datei.csv')` liest eine CSV-Datei als DataFrame ein. Die erste Zeile wird zu den Spaltennamen, die Datentypen erkennt pandas selbst.
Ist das Trennzeichen kein Komma, gibt man es an: `sep=';'`. Die Setup-Zelle ganz oben hat die Dateien `schueler.csv` (mit `;`) und `laender.csv` (mit `,`) angelegt.''',
     """import pandas as pd

schueler = pd.read_csv('schueler.csv', sep=';')
print(schueler.shape)
schueler.head(3)""")
expl('''#### Speichern mit `to_csv`

`df.to_csv('datei.csv', index=False)` speichert einen DataFrame als CSV-Datei. Mit `index=False` wird der Index nicht mitgespeichert.''',
     """import pandas as pd

df = pd.DataFrame({'a': [1, 2], 'b': [3, 4]})
df.to_csv('test.csv', index=False)
with open('test.csv', encoding='utf-8') as f:
    print(f.read())""")

t('Lies `laender.csv` ein, gib die Anzahl der Zeilen und Spalten aus und lass die ersten 4 Zeilen anzeigen.',
  "import pandas as pd",
  """laender = pd.read_csv('laender.csv')
print(laender.shape)
laender.head(4)""")
expl('''`astype(int)` wandelt die Werte einer Spalte in ganze Zahlen um (z. B. nach dem Runden). Ebenso gibt es `astype(float)` und `astype(str)`.''',
     """import pandas as pd

s = pd.Series([2.0, 3.0])
print(s.astype(int).tolist())""")
t('''Berechne für die Bundesländer die **Bevölkerungsdichte** (Einwohner pro km²; die Einwohner stehen in Tausend, also `einwohner * 1000 / flaeche`) als ganze Zahl
(`.round(0).astype(int)`) in einer neuen Spalte `dichte`. Lass Land und Dichte der 5 am dichtesten besiedelten Länder anzeigen.''',
  "import pandas as pd\n\nlaender = pd.read_csv('laender.csv')",
  """laender['dichte'] = (laender['einwohner'] * 1000 / laender['flaeche']).round(0).astype(int)
laender.sort_values('dichte', ascending=False)[['land', 'dichte']].head(5)""")
t('Gib die Gesamtzahl der Einwohner Deutschlands (in Tausend) und die Gesamtfläche aus. Gib außerdem das flächengrößte und das flächenkleinste Land aus.',
  "import pandas as pd\n\nlaender = pd.read_csv('laender.csv')",
  """print(laender['einwohner'].sum(), laender['flaeche'].sum())
print(laender.loc[laender['flaeche'].idxmax(), 'land'], laender.loc[laender['flaeche'].idxmin(), 'land'])""")
t('''Lies `schueler.csv` ein (Trennzeichen `;`), berechne den Durchschnitt der drei Noten als Spalte `schnitt` (2 Stellen) und lass `name`, `klasse` und `schnitt` sortiert nach `schnitt` (bei Gleichstand nach Name) anzeigen.''',
  "import pandas as pd",
  """s = pd.read_csv('schueler.csv', sep=';')
s['schnitt'] = ((s['mathe'] + s['deutsch'] + s['englisch']) / 3).round(2)
s.sort_values(['schnitt', 'name'])[['name', 'klasse', 'schnitt']]""")
t('''Speichere aus `schueler.csv` nur die Spalten `name` und `fehltage`, sortiert nach Fehltagen absteigend (bei Gleichstand nach Name aufsteigend), in der Datei `fehltage.csv` (ohne Index). Gib den Inhalt der neuen Datei aus.''',
  "import pandas as pd\n\ns = pd.read_csv('schueler.csv', sep=';')",
  """s[['name', 'fehltage']].sort_values(['fehltage', 'name'], ascending=[False, True]).to_csv('fehltage.csv', index=False)
with open('fehltage.csv', encoding='utf-8') as f:
    print(f.read())""")

# ---------------------------------------------------------------- 6
sec('Gemischte Übungen')
t('''Ein Einkaufszettel: Erzeuge einen DataFrame aus `posten` mit den Spalten `artikel`, `preis`, `menge`, berechne `summe = preis * menge` (2 Stellen) und lass die Tabelle anzeigen.
Gib danach den Gesamtbetrag mit 2 Nachkommastellen aus.''',
  "import pandas as pd\n\nposten = [('Milch', 1.19, 2), ('Brot', 2.49, 1), ('Äpfel', 0.45, 6), ('Käse', 3.99, 1)]",
  """df = pd.DataFrame(posten, columns=['artikel', 'preis', 'menge'])
df['summe'] = (df['preis'] * df['menge']).round(2)
display(df)
print(f"{df['summe'].sum():.2f}")""")
expl('''`pd.DataFrame(liste_von_tupeln, columns=[...])` erzeugt einen DataFrame aus einer Liste von Tupeln (eine Zeile pro Tupel) mit den angegebenen Spaltennamen.''',
     """import pandas as pd

pd.DataFrame([(1, 'a'), (2, 'b')], columns=['zahl', 'buchstabe'])""")
t('''Die Bundesliga-Tabelle: Berechne aus `siege`, `unentschieden`, `niederlagen` die Spalten `spiele` und `punkte` (3 pro Sieg, 1 pro Unentschieden). Sortiere nach Punkten absteigend und
lass die Tabelle mit allen Spalten anzeigen.''',
  "import pandas as pd\n\nt = pd.DataFrame({'verein': ['Stuttgart', 'Freiburg', 'Heidenheim', 'Hoffenheim'], 'siege': [6, 5, 4, 3], 'unentschieden': [2, 4, 3, 5],\n"
  "                  'niederlagen': [2, 1, 3, 2]})",
  """t['spiele'] = t['siege'] + t['unentschieden'] + t['niederlagen']
t['punkte'] = 3 * t['siege'] + t['unentschieden']
t.sort_values('punkte', ascending=False)""")
t('''Gib für `laender.csv` aus, wie viel Prozent der Einwohner Deutschlands in Baden-Württemberg leben (1 Stelle). Mache dazu `kuerzel` zum Index.''',
  "import pandas as pd\n\nlaender = pd.read_csv('laender.csv').set_index('kuerzel')",
  "print(round(laender.loc['BW', 'einwohner'] / laender['einwohner'].sum() * 100, 1))")
predict("""import pandas as pd

df = pd.DataFrame({'name': ['a', 'b', 'c'], 'wert': [3, 1, 2]})
df = df.sort_values('wert')
print(df['name'].tolist(), df.index.tolist())
print(df.iloc[0]['name'], df.loc[0, 'name'])""")

generate('pandas_grundlagen', 'pandas 1: Series und DataFrame', INTRO, ausfuehren=pandasnb.ausfuehrung(), ausgabe_markdown=True)
