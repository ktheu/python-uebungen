# Erzeugt ../content/pandas_gruppieren.ipynb (siehe nbgen.py). Drittes Notebook der pandas-Reihe.
# Kiosk-Daten: beim Generieren mit festem Seed erzeugt und als fester Text in die Setup-Zelle geschrieben.

import pandasnb
from pandasdaten import kiosk_csv
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
    'kiosk.csv': '''""" + kiosk_csv() + r"""''',
}
for name, inhalt in dateien.items():
    with open(name, 'w', encoding='utf-8') as f:
        f.write(inhalt)
print('Angelegt:', ', '.join(dateien))"""

INTRO = '''In diesem Notebook geht es darum, Daten **auszuwerten**: Summen und Durchschnitte bilden, nach Gruppen zusammenfassen (z. B. pro Klasse oder pro Tag),
Kreuztabellen erstellen und Werte in Klassen einteilen. Wer das Notebook zu SQL kennt, findet viele Bekannte wieder: `groupby` entspricht `GROUP BY`.

Die Reihe hat fünf Notebooks:

1. Grundlagen: Series und DataFrame, Spalten, Sortieren, CSV-Dateien
2. Auswählen und aufräumen: Filtern, Text-Spalten, fehlende Werte
3. **Gruppieren und auswerten**: Aggregatfunktionen, groupby, Pivot-Tabellen, Vergleich mit SQL (dieses Notebook)
4. Verbinden und Zeitreihen: merge, concat, Datum und Zeit
5. Diagramme und Anwendungen

Jeder Abschnitt beginnt mit kurzen Erklärungen und Beispielen. Führe die Beispiele aus und probiere sie ruhig ein wenig aus.
Danach folgen viele kleine Übungen. Wenn etwas vorgegeben ist, steht es schon in der Codezelle.'''

setup('''#### Beispieldateien anlegen

**Führe diese Zelle zuerst aus.** Sie legt `schueler.csv` (wie in den vorigen Notebooks) und `kiosk.csv` an: die Verkäufe eines Schulkiosks an 10 Schultagen
(Datum, Wochentag, Artikel, Kategorie, verkaufte Menge, Preis in Euro; ausgedachte Zahlen).''', DATEIEN)

S = "import pandas as pd\n\ns = pd.read_csv('schueler.csv', sep=';')"
K = "import pandas as pd\n\nk = pd.read_csv('kiosk.csv', sep=';')\nk['umsatz'] = k['menge'] * k['preis']"

# ---------------------------------------------------------------- 1
sec('Aggregatfunktionen')
expl('''#### Eine Zahl für eine Spalte

**Aggregatfunktionen** fassen viele Werte zu einem zusammen: `sum()`, `mean()`, `median()`, `min()`, `max()`, `count()` (Anzahl vorhandener Werte), `std()` (Standardabweichung).
Auf einen ganzen DataFrame angewendet, liefern sie eine Series mit einem Wert pro Spalte.

`df.agg(['sum', 'mean'])` berechnet mehrere auf einmal.

In SQL: `SELECT AVG(mathe), MAX(fehltage) FROM schueler;`''',
     S + """
print(s['mathe'].mean(), s['fehltage'].max(), s['fehltage'].median())
s[['mathe', 'deutsch', 'englisch']].agg(['mean', 'min', 'max'])""")

t('Gib die Summe aller Fehltage, den Median des Alters und die Anzahl der Schüler (`count()` der Spalte `name`) aus.', S,
  "print(s['fehltage'].sum(), s['alter'].median(), s['name'].count())")
t('Lass für die drei Notenspalten den Durchschnitt anzeigen (Series als letzte Zeile, auf 2 Stellen gerundet).', S,
  "s[['mathe', 'deutsch', 'englisch']].mean().round(2)")
t('Lass für die Spalten `menge` und `umsatz` des Kiosks Summe, Durchschnitt und Maximum anzeigen (`agg`, Ergebnis auf 2 Stellen gerundet).', K,
  "k[['menge', 'umsatz']].agg(['sum', 'mean', 'max']).round(2)")
t('Gib den Gesamtumsatz des Kiosks (2 Stellen) und die meistverkaufte Menge an einem Tag für einen Artikel mit Datum und Artikel aus (`idxmax` und `loc`).', K,
  """print(round(k['umsatz'].sum(), 2))
zeile = k.loc[k['menge'].idxmax()]
print(zeile['datum'], zeile['artikel'], zeile['menge'])""")
predict("""import pandas as pd

df = pd.DataFrame({'a': [1, 2, 3, 6], 'b': [4, 4, 4, 4]})
print(df['a'].mean(), df['a'].median(), df['b'].std())
print(df.sum().tolist())""")

# ---------------------------------------------------------------- 2
sec('Gruppieren mit groupby')
expl('''#### Pro Gruppe

`df.groupby('klasse')` teilt die Zeilen in **Gruppen** mit gleichem Wert in der Spalte `klasse`. Danach wählt man eine Spalte und eine Aggregatfunktion:
`df.groupby('klasse')['mathe'].mean()` ist der Mathe-Durchschnitt **pro Klasse** (eine Series mit der Klasse als Index).

- `df.groupby('klasse').size()` zählt die Zeilen pro Gruppe.
- `.reset_index()` macht aus dem Ergebnis wieder einen DataFrame mit der Gruppe als Spalte.
- Nach mehreren Spalten gruppiert man mit einer Liste: `df.groupby(['klasse', 'wohnort'])`.

In SQL: `SELECT klasse, AVG(mathe) FROM schueler GROUP BY klasse;`''',
     S + """
print(s.groupby('klasse').size().tolist())
display(s.groupby('klasse')['mathe'].mean().reset_index())
s.groupby(['klasse', 'wohnort'])['fehltage'].sum().reset_index()""")

t('Lass die Anzahl der Schüler pro Wohnort anzeigen (Series als letzte Zeile).', S, "s.groupby('wohnort').size()")
t('Lass den Durchschnitt der Englischnoten pro Klasse als DataFrame anzeigen (2 Stellen, `reset_index()`).', S,
  "s.groupby('klasse')['englisch'].mean().round(2).reset_index()")
t('Lass die verkaufte Menge pro Artikel anzeigen, die meistverkauften zuerst.', K,
  "k.groupby('artikel')['menge'].sum().sort_values(ascending=False)")
t('Lass den Umsatz pro Kategorie anzeigen (2 Stellen), als DataFrame mit den Spalten `kategorie` und `umsatz`, nach Umsatz absteigend sortiert.', K,
  "k.groupby('kategorie')['umsatz'].sum().round(2).reset_index().sort_values('umsatz', ascending=False)")
t('Gib aus, an welchem Wochentag (Spalte `tag`) insgesamt am meisten verkauft wurde (`idxmax` der Gruppensummen), und die Menge.', K,
  """pro_tag = k.groupby('tag')['menge'].sum()
print(pro_tag.idxmax(), pro_tag.max())""")
t('Lass die verkaufte Menge pro Kategorie und Wochentag als DataFrame anzeigen (`groupby` mit zwei Spalten, `reset_index()`), nur die Zeilen der Kategorie `Backwaren`.', K,
  """g = k.groupby(['kategorie', 'tag'])['menge'].sum().reset_index()
g[g['kategorie'] == 'Backwaren']""")
predict("""import pandas as pd

df = pd.DataFrame({'g': ['a', 'b', 'a', 'b', 'a'], 'x': [1, 2, 3, 4, 5]})
print(df.groupby('g')['x'].sum().tolist())
print(df.groupby('g').size().tolist(), df.groupby('g')['x'].max().tolist())""")

# ---------------------------------------------------------------- 3
sec('Mehrere Kennzahlen und Filtern nach dem Gruppieren')
expl('''#### Benannte Aggregation

Mit `agg` berechnet man mehrere Kennzahlen pro Gruppe und gibt ihnen Namen: `neuer_name=('spalte', 'funktion')`.

```python
df.groupby('klasse').agg(anzahl=('name', 'count'), mathe=('mathe', 'mean'), fehltage=('fehltage', 'sum'))
```

Das Ergebnis ist ein DataFrame mit einer Zeile pro Gruppe. Danach kann man ihn **filtern** wie jeden DataFrame; das entspricht `HAVING` in SQL:
`SELECT klasse, COUNT(*) AS anzahl FROM schueler GROUP BY klasse HAVING anzahl > 3;`''',
     S + """
g = s.groupby('klasse').agg(anzahl=('name', 'count'), mathe=('mathe', 'mean'), fehltage=('fehltage', 'sum'))
display(g)
g[g['fehltage'] > 15]""")

t('''Lass pro Klasse die Anzahl der Schüler, das jüngste und das höchste Alter und den Durchschnitt der Fehltage (2 Stellen) anzeigen (Spalten `anzahl`, `juengste`, `aelteste`, `fehltage`).''', S,
  """s.groupby('klasse').agg(anzahl=('name', 'count'), juengste=('alter', 'min'), aelteste=('alter', 'max'),
                        fehltage=('fehltage', 'mean')).round(2)""")
t('''Lass pro Artikel die Gesamtmenge (`menge`), den Gesamtumsatz (`umsatz`, 2 Stellen) und die größte Tagesmenge (`rekord`) anzeigen, nach Umsatz absteigend.''', K,
  """k.groupby('artikel').agg(menge=('menge', 'sum'), umsatz=('umsatz', 'sum'), rekord=('menge', 'max')).round(2).sort_values('umsatz', ascending=False)""")
t('Lass nur die Artikel anzeigen, von denen insgesamt mehr als 250 Stück verkauft wurden (Artikel und Menge, nach Menge absteigend).', K,
  """g = k.groupby('artikel')['menge'].sum().reset_index()
g[g['menge'] > 250].sort_values('menge', ascending=False)""")
t('Lass die Wohnorte anzeigen, deren Schüler im Durchschnitt mehr als 4 Fehltage haben, mit Anzahl (`anzahl`) und Durchschnitt (`fehltage`, 2 Stellen).', S,
  """g = s.groupby('wohnort').agg(anzahl=('name', 'count'), fehltage=('fehltage', 'mean')).round(2)
g[g['fehltage'] > 4]""")
t('''Gruppiere nach Klasse und Wohnort und lass für jede Kombination die Anzahl und den Mathe-Durchschnitt anzeigen; nur Kombinationen mit mindestens 2 Schülern (als DataFrame mit `reset_index()`).''', S,
  """g = s.groupby(['klasse', 'wohnort']).agg(anzahl=('name', 'count'), mathe=('mathe', 'mean')).reset_index()
g[g['anzahl'] >= 2]""")
predict("""import pandas as pd

df = pd.DataFrame({'g': ['x', 'y', 'x', 'y', 'z'], 'w': [2, 3, 4, 5, 6]})
r = df.groupby('g').agg(n=('w', 'count'), s=('w', 'sum'))
print(r['n'].tolist(), r['s'].tolist())
print(r[r['s'] > 6].index.tolist())""")

# ---------------------------------------------------------------- 4
sec('Pivot-Tabellen und Kreuztabellen')
expl('''#### `pivot_table`

Eine **Pivot-Tabelle** ordnet die Gruppen in Zeilen **und** Spalten an:

```python
df.pivot_table(index='kategorie', columns='tag', values='menge', aggfunc='sum')
```

Zeilen sind die Kategorien, Spalten die Tage, in den Zellen steht die Summe der Mengen. `fill_value=0` füllt leere Zellen, `margins=True` ergänzt Summen (`All`).

#### `pd.crosstab`

`pd.crosstab(df['a'], df['b'])` zählt, wie oft jede Kombination von Werten vorkommt (eine **Kreuztabelle**, Häufigkeitstabelle).''',
     K + """
display(k.pivot_table(index='kategorie', columns='tag', values='menge', aggfunc='sum'))
s = pd.read_csv('schueler.csv', sep=';')
pd.crosstab(s['klasse'], s['wohnort'])""")

t('Lass eine Pivot-Tabelle mit den Artikeln als Zeilen, den Wochentagen als Spalten und der Summe der Mengen anzeigen. Die Wochentage sollen in der Reihenfolge Montag bis Freitag stehen: wähle die Spalten danach mit einer Liste aus.', K,
  """p = k.pivot_table(index='artikel', columns='tag', values='menge', aggfunc='sum')
p[['Montag', 'Dienstag', 'Mittwoch', 'Donnerstag', 'Freitag']]""")
t('Lass eine Pivot-Tabelle mit den Kategorien als Zeilen und den beiden Daten des Montags (`2026-10-05` und `2026-10-12`) als Spalten anzeigen: Umsatz (2 Stellen). Filtere vorher auf die Montage.', K,
  """mo = k[k['tag'] == 'Montag']
mo.pivot_table(index='kategorie', columns='datum', values='umsatz', aggfunc='sum').round(2)""")
t('Lass eine Kreuztabelle der Klassen und der Mathenoten anzeigen (wie viele Schüler jeder Klasse haben welche Note) mit Summen (`margins=True`).', S,
  "pd.crosstab(s['klasse'], s['mathe'], margins=True)")
t('Lass eine Pivot-Tabelle mit den Wohnorten als Zeilen und den Klassen als Spalten anzeigen, in den Zellen der Durchschnitt der Deutschnoten (2 Stellen), leere Zellen mit 0 gefüllt.', S,
  "s.pivot_table(index='wohnort', columns='klasse', values='deutsch', aggfunc='mean', fill_value=0).round(2)")
predict("""import pandas as pd

df = pd.DataFrame({'a': ['x', 'x', 'y', 'y'], 'b': ['p', 'q', 'p', 'p'], 'v': [1, 2, 3, 4]})
p = df.pivot_table(index='a', columns='b', values='v', aggfunc='sum', fill_value=0)
print(p.loc['y', 'p'], p.loc['y', 'q'], p.loc['x', 'q'])
print(pd.crosstab(df['a'], df['b']).loc['y', 'p'])""")

# ---------------------------------------------------------------- 5
sec('Klassen bilden, Ränge und Anteile')
expl('''#### `pd.cut`: Werte in Klassen einteilen

`pd.cut(spalte, bins=[0, 3, 6, 10], labels=['wenig', 'mittel', 'viel'])` teilt Zahlen in Bereiche ein: (0, 3], (3, 6], (6, 10]. Die rechte Grenze gehört jeweils dazu.
Mit `right=False` gehört die linke Grenze dazu.

#### `rank`

`df['spalte'].rank(ascending=False, method='min')` vergibt Rangplätze (1 = größter Wert); bei Gleichstand bekommen alle den kleinsten Platz.

#### Anteile in der Gruppe: `transform`

`df.groupby('klasse')['fehltage'].transform('sum')` berechnet die Gruppensumme und schreibt sie in **jede** Zeile der Gruppe. So rechnet man Anteile an der Gruppe aus.''',
     S + """
s['fehlen'] = pd.cut(s['fehltage'], bins=[-1, 2, 6, 100], labels=['kaum', 'manchmal', 'oft'])
s['rang'] = s['fehltage'].rank(ascending=False, method='min').astype(int)
s['anteil'] = (s['fehltage'] / s.groupby('klasse')['fehltage'].transform('sum') * 100).round(1)
s[['name', 'klasse', 'fehltage', 'fehlen', 'rang', 'anteil']].head(6)""")

t('''Teile die Schüler mit `pd.cut` nach ihrer Mathenote in die Gruppen `gut` (1–2), `mittel` (3) und `schwach` (4–6) ein (Grenzen `[0, 2, 3, 6]`) und lass anzeigen, wie viele Schüler in jeder Gruppe sind
(`value_counts(sort=False)`).''', S,
  """s['gruppe'] = pd.cut(s['mathe'], bins=[0, 2, 3, 6], labels=['gut', 'mittel', 'schwach'])
s['gruppe'].value_counts(sort=False)""")
t('''Teile die Tagesmengen des Kiosks in die Klassen `0-14`, `15-29`, `30-44`, `45-59` ein (`bins=[0, 15, 30, 45, 60]`, `right=False`) und lass anzeigen, wie oft jede Klasse vorkommt (`sort=False`).''', K,
  """k['klasse'] = pd.cut(k['menge'], bins=[0, 15, 30, 45, 60], right=False, labels=['0-14', '15-29', '30-44', '45-59'])
k['klasse'].value_counts(sort=False)""")
t('''Vergib den Schülern Rangplätze nach der Summe der drei Noten (`summe`; kleinste Summe = Platz 1, `method='min'`) und lass Name, Summe und Platz sortiert nach Platz und Name anzeigen.''', S,
  """s['summe'] = s['mathe'] + s['deutsch'] + s['englisch']
s['platz'] = s['summe'].rank(method='min').astype(int)
s[['name', 'summe', 'platz']].sort_values(['platz', 'name'])""")
t('''Berechne für jeden Artikel, welchen Anteil (in Prozent, 1 Stelle) er am Umsatz **seiner Kategorie** hat. Lass Kategorie, Artikel und Anteil der Gesamtumsätze anzeigen (erst nach Artikel gruppieren,
dann `transform('sum')` über die Kategorie).''', K,
  """g = k.groupby(['kategorie', 'artikel'])['umsatz'].sum().reset_index()
g['anteil'] = (g['umsatz'] / g.groupby('kategorie')['umsatz'].transform('sum') * 100).round(1)
g[['kategorie', 'artikel', 'anteil']]""")
predict("""import pandas as pd

s = pd.Series([10, 30, 20, 30])
print(s.rank(ascending=False, method='min').tolist())
print(pd.cut(s, bins=[0, 15, 25, 40], labels=['a', 'b', 'c']).tolist())""")

# ---------------------------------------------------------------- 6
sec('Gemischte Übungen')
expl('''`reindex(liste, fill_value=0)` bringt eine Series in die Reihenfolge der Liste; Einträge, die es nicht gab, bekommen den Wert `fill_value`.''',
     """import pandas as pd

s = pd.Series({'b': 2, 'a': 1})
s.reindex(['a', 'b', 'c'], fill_value=0)""")
t('''Erstelle einen Notenspiegel für Mathe: Lass für jede Note 1 bis 6 die Anzahl anzeigen, auch für Noten, die niemand hat (`value_counts().reindex(range(1, 7), fill_value=0)`).
Gib danach den Durchschnitt (2 Stellen) aus.''', S,
  """spiegel = s['mathe'].value_counts().reindex(range(1, 7), fill_value=0)
print(round(s['mathe'].mean(), 2))
spiegel""")
t('''Vergleiche die beiden Wochen des Kiosks: Bestimme die Woche aus dem Datum (`datum < '2026-10-12'` → Woche 1, sonst 2) und lass eine Pivot-Tabelle mit den Kategorien als Zeilen, den Wochen als Spalten
und dem Umsatz (2 Stellen) anzeigen. Füge eine Spalte `veraenderung` (Woche 2 minus Woche 1, 2 Stellen) hinzu.''', K,
  """k['woche'] = k['datum'].apply(lambda d: 1 if d < '2026-10-12' else 2)
p = k.pivot_table(index='kategorie', columns='woche', values='umsatz', aggfunc='sum').round(2)
p['veraenderung'] = (p[2] - p[1]).round(2)
p""")
expl('''`df.groupby('tag')['menge'].idxmax()` gibt für jede Gruppe den **Index** der Zeile mit dem größten Wert zurück. Mit `df.loc[...]` wählt man diese Zeilen dann aus.''',
     """import pandas as pd

df = pd.DataFrame({'g': ['a', 'a', 'b'], 'x': [5, 9, 2]})
print(df.groupby('g')['x'].idxmax().tolist())""")

t('''Welcher Artikel ist an welchem Wochentag am beliebtesten? Lass für jeden Wochentag (Montag bis Freitag) den Artikel mit der größten Gesamtmenge und die Menge anzeigen
(nach `tag` und `artikel` gruppieren, dann pro Tag `idxmax`).''', K,
  """g = k.groupby(['tag', 'artikel'])['menge'].sum().reset_index()
beste = g.loc[g.groupby('tag')['menge'].idxmax()].set_index('tag')
beste.loc[['Montag', 'Dienstag', 'Mittwoch', 'Donnerstag', 'Freitag']]""")
generate('pandas_gruppieren', 'pandas 3: Gruppieren und auswerten', INTRO, ausfuehren=pandasnb.ausfuehrung(), ausgabe_markdown=True)
