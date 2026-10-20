# Erzeugt ../content/pandas_auswaehlen.ipynb (siehe nbgen.py). Zweites Notebook der pandas-Reihe.
# Sortieren immer eindeutig (bei Gleichstand weitere Spalte), weil sort_values nicht stabil sortiert.
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
    'filme.csv': '''titel,jahr,genre,minuten,bewertung,fsk
Momo,1986,Fantasy,101,7.1,0
 Shrek ,2001,animation,90,7.9,0
Avatar,2009,Science-Fiction,162,7.9,12
Das Boot,1981,Drama,149,8.3,12
Toy Story,1995,Animation,81,8.3,0
Lola rennt,1998,Thriller,80,7.6,12
Shrek,2001,Animation,90,7.9,0
Good Bye Lenin!,2003,Drama,121,,6
Inception,2010,science-fiction,148,8.8,12
Der Schuh des Manitu,2001,Komödie,,6.2,6
Titanic,1997,Drama,194,7.9,12
Die Welle,2008,Drama,107,7.5,12
Fack ju Göhte,2013,Komödie,118,6.8,12
Coco,2017,Animation,105,8.4,0
''',
}
for name, inhalt in dateien.items():
    with open(name, 'w', encoding='utf-8') as f:
        f.write(inhalt)
print('Angelegt:', ', '.join(dateien))"""

INTRO = '''In diesem Notebook geht es darum, aus einer Tabelle die **Zeilen auszuwählen**, die man braucht, und Daten **aufzuräumen**:
Text vereinheitlichen, Werte ändern, fehlende Werte und doppelte Zeilen behandeln.

Die Reihe hat fünf Notebooks:

1. Grundlagen: Series und DataFrame, Spalten, Sortieren, CSV-Dateien
2. **Auswählen und aufräumen**: Filtern, Text-Spalten, fehlende Werte (dieses Notebook)
3. Gruppieren und auswerten: Aggregatfunktionen, groupby, Pivot-Tabellen, Vergleich mit SQL
4. Verbinden und Zeitreihen: merge, concat, Datum und Zeit
5. Diagramme und Anwendungen

Wie im ersten Notebook: Steht ein DataFrame in der letzten Zeile, wird er als Tabelle angezeigt; mehrere Tabellen mit `display()`.

Jeder Abschnitt beginnt mit kurzen Erklärungen und Beispielen. Führe die Beispiele aus und probiere sie ruhig ein wenig aus.
Danach folgen viele kleine Übungen. Wenn etwas vorgegeben ist, steht es schon in der Codezelle.'''

setup('''#### Beispieldateien anlegen

**Führe diese Zelle zuerst aus.** Sie legt `schueler.csv` (wie im ersten Notebook) und `filme.csv` an. Die Filmliste ist absichtlich etwas „unordentlich“:
Sie enthält fehlende Werte, eine doppelte Zeile und uneinheitliche Schreibweisen.''', DATEIEN)

S = "import pandas as pd\n\ns = pd.read_csv('schueler.csv', sep=';')"
F = "import pandas as pd\n\nf = pd.read_csv('filme.csv')"

# ---------------------------------------------------------------- 1
sec('Zeilen mit Bedingungen auswählen')
expl('''#### Boolesche Masken

`df['mathe'] < 3` ist eine Series aus `True`/`False`, eine **Maske**. `df[maske]` wählt die Zeilen aus, bei denen die Maske `True` ist.

Bedingungen verknüpft man mit `&` (und), `|` (oder) und `~` (nicht). Dabei muss **jede Bedingung in Klammern** stehen:
`df[(df['klasse'] == '9a') & (df['mathe'] <= 2)]`.

Wie viele Zeilen eine Bedingung erfüllen, ergibt `len(df[maske])` oder `maske.sum()`.''',
     S + """
gut = s[s['mathe'] <= 2]
print(len(gut), (s['mathe'] <= 2).sum())
s[(s['klasse'] == '9a') & (s['mathe'] <= 2)]""")
expl('''#### Zeilen und Spalten zugleich: `loc`

`df.loc[maske, ['spalte1', 'spalte2']]` wählt die passenden Zeilen und nur bestimmte Spalten aus.''',
     S + """
s.loc[s['fehltage'] > 10, ['name', 'klasse', 'fehltage']]""")

t('Lass alle Schülerinnen und Schüler aus Tübingen anzeigen.', S, "s[s['wohnort'] == 'Tübingen']")
t('Lass Name und Englischnote aller Schüler mit einer Englischnote von 3 oder schlechter anzeigen.', S, "s.loc[s['englisch'] >= 3, ['name', 'englisch']]")
t('Gib aus, wie viele Schüler 15 Jahre alt sind und wie viele älter als 15 sind.', S,
  """print((s['alter'] == 15).sum())
print((s['alter'] > 15).sum())""")
t('Lass alle Schüler der 9b anzeigen, die in Deutsch eine 1 oder 2 haben.', S, "s[(s['klasse'] == '9b') & (s['deutsch'] <= 2)]")
t('Lass alle Schüler anzeigen, die in Mathe **oder** Englisch eine 4 oder schlechter haben (Name, Mathe, Englisch).', S,
  "s.loc[(s['mathe'] >= 4) | (s['englisch'] >= 4), ['name', 'mathe', 'englisch']]")
t('Lass alle Schüler anzeigen, die **nicht** in Tübingen wohnen, nur Name und Wohnort, sortiert nach Name.', S,
  "s.loc[~(s['wohnort'] == 'Tübingen'), ['name', 'wohnort']].sort_values('name')")
t('''Gib den Durchschnitt der Fehltage der Schüler mit einer Mathenote von 1 oder 2 und den der übrigen Schüler aus (2 Stellen).''', S,
  """gut = s['mathe'] <= 2
print(round(s.loc[gut, 'fehltage'].mean(), 2))
print(round(s.loc[~gut, 'fehltage'].mean(), 2))""")
t('Lass die Schüler der 9c mit den wenigsten Fehltagen zuerst anzeigen (nur Name und Fehltage, bei Gleichstand nach Name).', S,
  "s.loc[s['klasse'] == '9c', ['name', 'fehltage']].sort_values(['fehltage', 'name'])")
predict("""import pandas as pd

df = pd.DataFrame({'x': [1, 5, 3, 8], 'y': [2, 2, 9, 1]})
print(len(df[df['x'] > 2]))
print(len(df[(df['x'] > 2) & (df['y'] > 1)]))
print(df.loc[(df['x'] < 2) | (df['y'] < 2), 'x'].tolist())""")

# ---------------------------------------------------------------- 2
sec('isin, between und Ranglisten')
expl('''#### Mehrere Werte und Bereiche

- `df['spalte'].isin(['a', 'b'])`: ist der Wert einer aus der Liste?
- `df['spalte'].between(2, 4)`: liegt der Wert zwischen 2 und 4 (beide Grenzen eingeschlossen)?
- `df.nlargest(3, 'spalte')` und `df.nsmallest(3, 'spalte')`: die 3 Zeilen mit den größten bzw. kleinsten Werten.''',
     S + """
display(s[s['wohnort'].isin(['Rottenburg', 'Mössingen'])].head(3))
print(s['alter'].between(15, 16).sum())
s.nlargest(2, 'fehltage')""")

t('Lass alle Schüler der Klassen 9a und 9c anzeigen, die in Mathe eine 1 haben.', S, "s[s['klasse'].isin(['9a', '9c']) & (s['mathe'] == 1)]")
t('Gib aus, wie viele Schüler zwischen 2 und 6 Fehltage haben (einschließlich).', S, "print(s['fehltage'].between(2, 6).sum())")
t('Lass die drei Schüler mit den meisten Fehltagen anzeigen (Name und Fehltage).', S, "s.nlargest(3, 'fehltage')[['name', 'fehltage']]")
t('Lass alle Filme mit einer Laufzeit zwischen 90 und 120 Minuten anzeigen (Titel und Minuten, nach Minuten sortiert, bei Gleichstand nach Titel).', F,
  "f.loc[f['minuten'].between(90, 120), ['titel', 'minuten']].sort_values(['minuten', 'titel'])")
t('Lass die zwei am besten bewerteten Filme mit FSK 0 anzeigen (Titel und Bewertung).', F, "f[f['fsk'] == 0].nlargest(2, 'bewertung')[['titel', 'bewertung']]")
predict("""import pandas as pd

s = pd.Series([3, 7, 5, 1, 9])
print(s.between(3, 7).sum(), s.isin([1, 2, 3]).sum())
print(s.nlargest(2).tolist())""")

# ---------------------------------------------------------------- 3
sec('Text-Spalten')
expl('''#### `.str`

Für Spalten mit Text gibt es über `.str` die bekannten String-Methoden, angewendet auf **jede** Zeile:

| Aufruf | Ergebnis |
|---|---|
| `df['t'].str.lower()`, `.str.upper()`, `.str.title()` | klein, groß, Wortanfänge groß |
| `df['t'].str.strip()` | Leerzeichen am Anfang und Ende entfernen |
| `df['t'].str.len()` | Länge |
| `df['t'].str.contains('ab')` | enthält den Text? (mit `case=False` ohne Groß-/Kleinschreibung) |
| `df['t'].str.startswith('A')`, `.str.endswith('!')` | beginnt/endet mit? |
| `df['t'].str.replace('alt', 'neu')` | ersetzen |
| `df['t'].str.split(' ').str[0]` | zerlegen und das erste Teil nehmen |''',
     F + """
print(f['titel'].str.len().max())
print(f['titel'].str.contains('der', case=False).sum())
f.loc[f['titel'].str.startswith('D'), ['titel', 'jahr']]""")

t('Lass Titel und Jahr aller Filme anzeigen, deren Titel das Wort `Die` oder `die` enthält (`contains` mit `case=False`).', F,
  "f.loc[f['titel'].str.contains('die', case=False), ['titel', 'jahr']]")
t('In der Spalte `genre` gibt es uneinheitliche Schreibweisen. Vereinheitliche sie mit `str.title()` (Wortanfänge groß) und gib die verschiedenen Genres sortiert aus (`sorted(... .unique())`).', F,
  """f['genre'] = f['genre'].str.title()
print(sorted(f['genre'].unique()))""")
expl('''`unique()` gibt die verschiedenen Werte einer Spalte zurück (in der Reihenfolge ihres ersten Auftretens), `nunique()` ihre Anzahl.''',
     """import pandas as pd

s = pd.Series(['b', 'a', 'b', 'c'])
print(s.unique().tolist(), s.nunique())""")
t('Ein Titel hat überflüssige Leerzeichen. Entferne sie in der ganzen Spalte mit `str.strip()` und gib aus, wie oft der Titel `Shrek` jetzt vorkommt.', F,
  """f['titel'] = f['titel'].str.strip()
print((f['titel'] == 'Shrek').sum())""")
t('Lass eine neue Spalte `kurz` mit den ersten 5 Buchstaben jedes Titels (`str[:5]`) zusammen mit dem Titel für die ersten 4 Filme anzeigen.', F,
  """f['kurz'] = f['titel'].str[:5]
f[['titel', 'kurz']].head(4)""")
t('Lass alle Filme anzeigen, deren Titel aus mehr als einem Wort besteht (Titel und Anzahl der Wörter, `str.split().str.len()`), nur die mit mindestens 3 Wörtern.', F,
  """f['woerter'] = f['titel'].str.split().str.len()
f.loc[f['woerter'] >= 3, ['titel', 'woerter']]""")
t('Lass in `schueler.csv` die Spalte `klasse` so umwandeln, dass `9a` zu `Klasse 9a` wird, und zeige die ersten 3 Zeilen von Name und Klasse.', S,
  """s['klasse'] = 'Klasse ' + s['klasse']
s[['name', 'klasse']].head(3)""")
predict("""import pandas as pd

t = pd.Series([' Ab', 'cd ', 'Ef'])
print(t.str.strip().str.lower().tolist())
print(t.str.len().tolist())
print(t.str.contains('b', case=False).sum())""")

# ---------------------------------------------------------------- 4
sec('Werte ändern: loc, map, apply, replace')
expl('''#### Mit Bedingung ändern

`df.loc[maske, 'spalte'] = wert` ändert die Werte in den ausgewählten Zeilen. (Schreibweisen wie `df[maske]['spalte'] = wert` funktionieren in pandas 3 **nicht**.)''',
     S + """
s.loc[s['fehltage'] > 10, 'fehltage'] = 10
s['fehltage'].tolist()""")
expl('''#### `map`, `apply` und `replace`

- `df['spalte'].map(dictionary)` ersetzt jeden Wert durch den Wert aus dem Dictionary.
- `df['spalte'].apply(funktion)` wendet eine Funktion (oft ein `lambda`) auf jeden Wert an.
- `df['spalte'].replace(alt, neu)` ersetzt bestimmte Werte, mit einem Dictionary auch mehrere.''',
     S + """
noten = {1: 'sehr gut', 2: 'gut', 3: 'befriedigend', 4: 'ausreichend', 5: 'mangelhaft', 6: 'ungenügend'}
s['mathe_text'] = s['mathe'].map(noten)
s['bestanden'] = s['mathe'].apply(lambda n: n <= 4)
s['ort'] = s['wohnort'].replace({'Tübingen': 'TÜ', 'Rottenburg': 'RO', 'Mössingen': 'MÖ'})
s[['name', 'mathe', 'mathe_text', 'bestanden', 'ort']].head(4)""")

t('Alle Schüler aus Mössingen bekommen in Englisch eine Note besser (minus 1). Ändere das mit `loc` und lass Name, Wohnort und Englisch dieser Schüler anzeigen.', S,
  """moe = s['wohnort'] == 'Mössingen'
s.loc[moe, 'englisch'] = s.loc[moe, 'englisch'] - 1
s.loc[moe, ['name', 'wohnort', 'englisch']]""")
t('Lege eine Spalte `stufe` an, die mit `map` aus der Klasse die Stufe macht: `9a` → `A`, `9b` → `B`, `9c` → `C`. Lass Name, Klasse und Stufe der ersten 4 Schüler anzeigen.', S,
  """s['stufe'] = s['klasse'].map({'9a': 'A', '9b': 'B', '9c': 'C'})
s[['name', 'klasse', 'stufe']].head(4)""")
expl('''`wert1 if bedingung else wert2` ist ein **bedingter Ausdruck**: Er ergibt `wert1`, wenn die Bedingung erfüllt ist, sonst `wert2`. In einem `lambda` ist das praktisch.''',
     """for n in [3, 8]:
    print('groß' if n > 5 else 'klein')""")
t('''Lege mit `apply` und einem `lambda` eine Spalte `warnung` an: `ja`, wenn ein Schüler mehr als 5 Fehltage hat, sonst `nein`. Gib aus, wie viele Warnungen es gibt.''', S,
  """s['warnung'] = s['fehltage'].apply(lambda x: 'ja' if x > 5 else 'nein')
print((s['warnung'] == 'ja').sum())""")
t('''Ersetze in der Filmliste die FSK-Zahlen mit `replace` durch Texte: 0 → `ohne`, 6 → `ab 6`, 12 → `ab 12`. Lass Titel und FSK der ersten 5 Filme anzeigen.''', F,
  """f['fsk'] = f['fsk'].replace({0: 'ohne', 6: 'ab 6', 12: 'ab 12'})
f[['titel', 'fsk']].head(5)""")
t('''Berechne die Laufzeit der Filme in Stunden und Minuten als Text, z. B. `2 h 42 min`, mit `apply` und einem `lambda`,
für die ersten 4 Filme (die alle eine Laufzeit haben). Lass Titel und die neue Spalte anzeigen.''', F,
  """kurz = f.head(4).copy()
kurz['dauer'] = kurz['minuten'].apply(lambda m: f'{int(m) // 60} h {int(m) % 60} min')
kurz[['titel', 'dauer']]""")
expl('''`df.copy()` macht eine eigene Kopie eines DataFrames. Ändert man die Kopie, bleibt das Original unverändert. Bei `head()` oder einer Auswahl ist das sinnvoll, wenn man danach neue Spalten anlegt.''',
     """import pandas as pd

a = pd.DataFrame({'x': [1, 2]})
b = a.copy()
b['x'] = 0
print(a['x'].tolist(), b['x'].tolist())""")
predict("""import pandas as pd

s = pd.Series([1, 2, 3])
print(s.map({1: 'a', 2: 'b', 3: 'c'}).tolist())
print(s.apply(lambda x: x * x).tolist())
print(s.replace(2, 20).tolist())""")

# ---------------------------------------------------------------- 5
sec('Fehlende Werte')
expl('''#### `NaN`

Fehlende Werte zeigt pandas als `NaN` an. Aggregatfunktionen wie `mean()` oder `sum()` **überspringen** sie; `count()` zählt nur vorhandene Werte.

| Aufruf | Ergebnis |
|---|---|
| `df['spalte'].isna()` | Maske: wo fehlt der Wert? (`notna()` umgekehrt) |
| `df.isna().sum()` | Anzahl fehlender Werte pro Spalte |
| `df.dropna()` | Zeilen mit fehlenden Werten entfernen (`subset=['spalte']`: nur diese Spalte betrachten) |
| `df['spalte'].fillna(wert)` | fehlende Werte durch `wert` ersetzen |''',
     F + """
print(f.isna().sum().tolist())
print(f['bewertung'].count(), len(f))
f[f['bewertung'].isna()]""")

t('Gib für jede Spalte der Filmliste aus, wie viele Werte fehlen (Series als letzte Zeile).', F, "f.isna().sum()")
t('Lass alle Filme anzeigen, bei denen ein Wert fehlt (Bewertung oder Minuten). Benutze `isna()` für beide Spalten mit `|`.', F,
  "f[f['bewertung'].isna() | f['minuten'].isna()]")
t('Gib die durchschnittliche Bewertung (2 Stellen) aus und die Anzahl der Filme mit Bewertung. Entferne dann alle Zeilen mit fehlenden Werten und gib die Anzahl der übrigen Filme aus.', F,
  """print(round(f['bewertung'].mean(), 2), f['bewertung'].count())
print(len(f.dropna()))""")
t('''Ersetze fehlende Laufzeiten durch den Median der Laufzeiten (`median()`) und fehlende Bewertungen durch 0. Lass danach die beiden Filme anzeigen, bei denen etwas gefehlt hatte.''', F,
  """fehlte = f['bewertung'].isna() | f['minuten'].isna()
f['minuten'] = f['minuten'].fillna(f['minuten'].median())
f['bewertung'] = f['bewertung'].fillna(0)
f[fehlte]""")
t('''Nach dem Einlesen ist `minuten` eine Kommazahl-Spalte (wegen des fehlenden Wertes). Entferne die Zeile ohne Laufzeit (`dropna(subset=['minuten'])`), wandle die Spalte mit `astype(int)` in ganze
Zahlen um und gib die ersten 5 Laufzeiten als Liste aus.''', F,
  """g = f.dropna(subset=['minuten']).copy()
g['minuten'] = g['minuten'].astype(int)
print(g['minuten'].head(5).tolist())""")
predict("""import pandas as pd

s = pd.Series([2.0, None, 4.0, None])
print(s.count(), s.sum(), s.mean())
print(s.isna().sum(), s.fillna(1).tolist())""")

# ---------------------------------------------------------------- 6
sec('Doppelte Zeilen und Häufigkeiten')
expl('''#### Duplikate

- `df.duplicated()` ist `True` bei jeder Zeile, die genauso schon weiter oben steht.
- `df.drop_duplicates()` entfernt solche Zeilen; mit `subset=['spalte']` zählen nur diese Spalten.

#### `value_counts()`

`df['spalte'].value_counts()` zählt, wie oft jeder Wert vorkommt (die häufigsten zuerst). Mit `normalize=True` erhält man Anteile statt Anzahlen.''',
     F + """
f['titel'] = f['titel'].str.strip()
f['genre'] = f['genre'].str.title()
print(f.duplicated().sum())
f = f.drop_duplicates()
print(len(f))
f['genre'].value_counts()""")

FS = F + "\nf['titel'] = f['titel'].str.strip()\nf['genre'] = f['genre'].str.title()"
t('Gib aus, wie viele doppelte Zeilen es (nach dem Aufräumen der Titel und Genres) gibt, und lass die doppelte Zeile anzeigen.', FS,
  """print(f.duplicated().sum())
f[f.duplicated()]""")
t('Entferne doppelte Filme und lass die Anzahl der Filme pro Genre anzeigen (Series als letzte Zeile).', FS,
  "f.drop_duplicates()['genre'].value_counts()")
t('Lass für die Schüler anzeigen, wie viel Prozent aus jedem Wohnort kommen (`normalize=True`, mal 100, auf 1 Stelle gerundet).', S,
  "(s['wohnort'].value_counts(normalize=True) * 100).round(1)")
t('Gib aus, aus wie vielen verschiedenen Wohnorten und Klassen die Schüler kommen (`nunique()`).', S,
  "print(s['wohnort'].nunique(), s['klasse'].nunique())")
t('''Behalte von jedem Erscheinungsjahr nur den **ersten** Film (`drop_duplicates(subset=['jahr'])`) und lass Titel und Jahr nach Jahr sortiert anzeigen.''', FS,
  "f.drop_duplicates(subset=['jahr'])[['titel', 'jahr']].sort_values('jahr')")
predict("""import pandas as pd

df = pd.DataFrame({'a': [1, 1, 2, 1], 'b': ['x', 'x', 'y', 'z']})
print(df.duplicated().sum(), len(df.drop_duplicates(subset=['a'])))
print(df['a'].value_counts().tolist())""")

# ---------------------------------------------------------------- 7
sec('Gemischte Übungen')
t('''Räume die Filmliste vollständig auf: Titel ohne Leerzeichen, Genres einheitlich (`title()`), Duplikate entfernen, Zeilen mit fehlenden Werten entfernen. Lass dann alle Dramen
mit einer Bewertung von mindestens 7.5 anzeigen (Titel, Jahr, Bewertung), nach Bewertung absteigend sortiert (bei Gleichstand nach Titel).''', F,
  """f['titel'] = f['titel'].str.strip()
f['genre'] = f['genre'].str.title()
f = f.drop_duplicates().dropna()
gut = f[(f['genre'] == 'Drama') & (f['bewertung'] >= 7.5)]
gut[['titel', 'jahr', 'bewertung']].sort_values(['bewertung', 'titel'], ascending=[False, True])""")
t('''Ein Zeugnis-Check: Lass alle Schüler anzeigen, die in mindestens einem Fach eine 4 oder schlechter haben, mit einer Spalte `faecher`, die angibt, in wie vielen Fächern
(Summe der drei Masken, als Zahl). Nur Name und `faecher`.''', S,
  """schlecht = (s['mathe'] >= 4).astype(int) + (s['deutsch'] >= 4).astype(int) + (s['englisch'] >= 4).astype(int)
s['faecher'] = schlecht
s.loc[s['faecher'] > 0, ['name', 'faecher']]""")
expl('''`maske.mean()` ist der **Anteil** der `True`-Werte, weil `True` als 1 und `False` als 0 zählt.''',
     """import pandas as pd

print(pd.Series([True, False, True, True]).mean())""")

t('''Gib für die Filme (aufgeräumt wie oben) aus, welcher Anteil der Filme ab 2000 erschienen ist (Prozent, 1 Stelle) und welches Jahrzehnt am häufigsten vorkommt
(`(jahr // 10 * 10).value_counts().idxmax()`).''', F,
  """f['titel'] = f['titel'].str.strip()
f = f.drop_duplicates(subset=['titel'])
print(round((f['jahr'] >= 2000).mean() * 100, 1))
print((f['jahr'] // 10 * 10).value_counts().idxmax())""")
generate('pandas_auswaehlen', 'pandas 2: Auswählen und aufräumen', INTRO, ausfuehren=pandasnb.ausfuehrung(), ausgabe_markdown=True)
