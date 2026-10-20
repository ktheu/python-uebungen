# Erzeugt ../content/pandas_diagramme_anwendungen.ipynb (siehe nbgen.py). Fünftes Notebook der pandas-Reihe.
# Diagramme mit df.plot (matplotlib); jede Diagramm-Zelle endet mit plt.show(), damit kein "<Axes: ...>" als Ausgabe erscheint.
# Aufgabentexte sagen genau, was gezeichnet wird (Art, Farben, Beschriftungen).
import pandasnb
from pandasdaten import SCHUELER, LAENDER, kiosk_csv, wetter_csv, setup_code
from nbgen import sec, expl, task, predict, generate, setup


def t(text, given='', body='', kind='normal'):
    """Aufgabe, deren Lösung aus dem vorgegebenen Code plus body besteht."""
    task(text, given=given, solution=(given + '\n' + body) if given else body, kind=kind)


INTRO = '''In diesem Notebook stellst du Daten mit **Diagrammen** dar, direkt aus pandas heraus (`df.plot`), und wertest in kleinen **Projekten** Datensätze von der Frage
bis zum Diagramm aus.

Die Reihe hat fünf Notebooks:

1. Grundlagen: Series und DataFrame, Spalten, Sortieren, CSV-Dateien
2. Auswählen und aufräumen: Filtern, Text-Spalten, fehlende Werte
3. Gruppieren und auswerten: Aggregatfunktionen, groupby, Pivot-Tabellen, Vergleich mit SQL
4. Verbinden und Zeitreihen: merge, concat, Datum und Zeit
5. **Diagramme und Anwendungen** (dieses Notebook)

Du solltest das Notebook zu den matplotlib-Grundlagen kennen. Die erwarteten Diagramme stehen als Bild unter den Aufgaben.

Jeder Abschnitt beginnt mit kurzen Erklärungen und Beispielen. Führe die Beispiele aus und probiere sie ruhig ein wenig aus.
Danach folgen viele kleine Übungen. Wenn etwas vorgegeben ist, steht es schon in der Codezelle.'''

setup('''#### Beispieldateien anlegen

**Führe diese Zelle zuerst aus.** Sie legt die Dateien aus den vorigen Notebooks an: `schueler.csv`, `laender.csv` (Einwohner in Tausend, Fläche in km², gerundet, Stand etwa 2023),
`kiosk.csv` (Verkäufe eines Schulkiosks) und `wetter.csv` (Temperatur und Regen von Januar bis Juni 2026, ausgedacht).''',
      setup_code({'schueler.csv': SCHUELER, 'laender.csv': LAENDER, 'kiosk.csv': kiosk_csv(), 'wetter.csv': wetter_csv()}))

PLT = "import matplotlib.pyplot as plt\nimport pandas as pd\n\n"
S = PLT + "s = pd.read_csv('schueler.csv', sep=';')"
L = PLT + "l = pd.read_csv('laender.csv')"
K = PLT + "k = pd.read_csv('kiosk.csv', sep=';', parse_dates=['datum'])\nk['umsatz'] = k['menge'] * k['preis']"
W = PLT + "w = pd.read_csv('wetter.csv', parse_dates=['datum']).set_index('datum')"

# ---------------------------------------------------------------- 1
sec('Liniendiagramme')
expl('''#### `plot()`

`df.plot()` bzw. `s.plot()` zeichnet ein **Liniendiagramm** mit matplotlib: auf der x-Achse der Index, für jede Spalte eine Linie. Mit `x='spalte'` und `y='spalte'` wählt man die Spalten selbst.

Wichtige Angaben: `title='...'`, `xlabel=`, `ylabel=`, `color=`, `figsize=(breite, hoehe)`, `legend=False`, `grid=True`, `marker='o'`.
`plot` gibt die matplotlib-Achse (`ax`) zurück; danach kann man wie gewohnt weiterarbeiten. Am Ende steht `plt.show()`.''',
     W + """
monat = w.resample('ME').mean()
monat['temperatur'].plot(title='Monatsmittel der Temperatur', ylabel='°C', marker='o', grid=True, figsize=(5, 3))
plt.show()""")

t('''Zeichne die Tagestemperaturen von Januar bis Juni als Linie (Farbe `'C3'`) mit dem Titel `Temperatur 2026`, der y-Beschriftung `°C`, ohne x-Beschriftung (`xlabel=''`), Gitter, Bildgröße 6 × 3.''', W,
  """w['temperatur'].plot(color='C3', title='Temperatur 2026', ylabel='°C', xlabel='', grid=True, figsize=(6, 3))
plt.show()""")
t('''Zeichne die Temperatur und ihren gleitenden 7-Tage-Durchschnitt in ein Diagramm: Lege die Spalte `mittel7` an und zeichne `w[['temperatur', 'mittel7']]` mit den Farben `['lightgray', 'C0']`
(`color=` mit einer Liste), Titel `Temperatur und 7-Tage-Mittel`, Bildgröße 6 × 3.''', W,
  """w['mittel7'] = w['temperatur'].rolling(7).mean()
w[['temperatur', 'mittel7']].plot(color=['lightgray', 'C0'], title='Temperatur und 7-Tage-Mittel', figsize=(6, 3))
plt.show()""")
t('''Zeichne die laufende Regensumme seit Jahresbeginn (`cumsum`) als Linie (Farbe `'C0'`), Titel `Regen seit 1. Januar`, y-Beschriftung `mm`, keine Legende, Bildgröße 5 × 3.''', W,
  """w['regen'].cumsum().plot(color='C0', title='Regen seit 1. Januar', ylabel='mm', legend=False, figsize=(5, 3))
plt.show()""")
t('''Zeichne für den Kiosk den Gesamtumsatz pro Tag (nach `datum` gruppieren) als Linie mit Punkten (`marker='o'`), Titel `Umsatz pro Tag`, y-Beschriftung `Euro`, Bildgröße 5 × 3.''', K,
  """k.groupby('datum')['umsatz'].sum().plot(marker='o', title='Umsatz pro Tag', ylabel='Euro', figsize=(5, 3))
plt.show()""")

# ---------------------------------------------------------------- 2
sec('Balkendiagramme')
expl('''#### `plot.bar` und `plot.barh`

`df.plot.bar()` zeichnet **senkrechte** Balken, `df.plot.barh()` **waagrechte**. Bei einem DataFrame mit mehreren Spalten stehen die Balken nebeneinander,
mit `stacked=True` übereinander. `rot=0` dreht die Beschriftungen der x-Achse waagrecht.

Meist zeichnet man das Ergebnis einer Gruppierung oder eine Pivot-Tabelle.''',
     K + """
k.groupby('kategorie')['umsatz'].sum().sort_values().plot.barh(color='C2', title='Umsatz pro Kategorie', xlabel='Euro', figsize=(5, 3))
plt.show()""")

t('''Zeichne die Einwohnerzahl (in Tausend) der Bundesländer als waagrechte Balken, sortiert nach Einwohnern (das größte oben: aufsteigend sortieren), mit dem Kürzel als Beschriftung
(`set_index('kuerzel')`), Farbe `'C0'`, Titel `Einwohner in Tausend`, ohne y-Beschriftung (`ylabel=''`), Bildgröße 5 × 5.''', L,
  """l.set_index('kuerzel')['einwohner'].sort_values().plot.barh(color='C0', title='Einwohner in Tausend', ylabel='', figsize=(5, 5))
plt.show()""")
t('''Zeichne den Mathe-, Deutsch- und Englisch-Durchschnitt pro Klasse als gruppierte senkrechte Balken (`groupby` und `mean`), Titel `Notendurchschnitt`, waagrechte Beschriftungen (`rot=0`),
Bildgröße 5 × 3.''', S,
  """s.groupby('klasse')[['mathe', 'deutsch', 'englisch']].mean().plot.bar(rot=0, title='Notendurchschnitt', figsize=(5, 3))
plt.show()""")
t('''Zeichne die verkaufte Menge pro Wochentag (Montag bis Freitag in dieser Reihenfolge) und Kategorie als **gestapelte** Balken: Pivot-Tabelle mit den Tagen als Zeilen und den Kategorien als
Spalten, Zeilen mit `.loc[[...]]` ordnen. Titel `Verkauf pro Wochentag`, `rot=0`, Bildgröße 6 × 3.''', K,
  """p = k.pivot_table(index='tag', columns='kategorie', values='menge', aggfunc='sum')
p = p.loc[['Montag', 'Dienstag', 'Mittwoch', 'Donnerstag', 'Freitag']]
p.plot.bar(stacked=True, rot=0, title='Verkauf pro Wochentag', figsize=(6, 3))
plt.show()""")
t('''Zeichne den Notenspiegel für Mathe (Anzahl der Schüler für die Noten 1 bis 6, auch 0 mit `reindex`) als senkrechte Balken in der Farbe `'C1'`, Titel `Mathe`, x-Beschriftung `Note`,
y-Beschriftung `Anzahl`, `rot=0`, Bildgröße 4 × 3.''', S,
  """s['mathe'].value_counts().reindex(range(1, 7), fill_value=0).plot.bar(color='C1', title='Mathe', xlabel='Note', ylabel='Anzahl', rot=0, figsize=(4, 3))
plt.show()""")

# ---------------------------------------------------------------- 3
sec('Histogramme, Boxplots und Kreisdiagramme')
expl('''#### Verteilungen

- `s.plot.hist(bins=10)` zeichnet ein **Histogramm**: wie viele Werte in welchem Bereich liegen. `edgecolor='black'` umrandet die Balken.
- `df.plot.box()` zeichnet für jede Spalte einen **Boxplot** (Median, Quartile, Minimum/Maximum, Ausreißer als Punkte).
- `s.plot.pie(autopct='%1.0f%%')` zeichnet ein **Kreisdiagramm** mit Prozentangaben.''',
     W + """
fig, axs = plt.subplots(1, 2, figsize=(7, 3))
w['temperatur'].plot.hist(bins=15, edgecolor='black', ax=axs[0], title='Temperaturen')
w[['temperatur']].plot.box(ax=axs[1], title='Boxplot')
plt.show()""")
expl('''Mit `ax=` zeichnet `plot` in eine vorhandene Achse, z. B. in eines von mehreren Teildiagrammen aus `plt.subplots` (siehe Notebook matplotlib: Layout).''',
     PLT + """fig, axs = plt.subplots(1, 2, figsize=(4, 2))
pd.Series([1, 3, 2]).plot(ax=axs[0])
pd.Series([2, 1, 2]).plot.bar(ax=axs[1])
plt.show()""")

t('''Zeichne ein Histogramm der täglichen Regenmengen an Regentagen (`regen > 0`) mit 10 Klassen, schwarzen Rändern, Farbe `'C0'`, Titel `Regen an Regentagen`, x-Beschriftung `mm`, Bildgröße 4 × 3.''', W,
  """w.loc[w['regen'] > 0, 'regen'].plot.hist(bins=10, edgecolor='black', color='C0', title='Regen an Regentagen', figsize=(4, 3))
plt.xlabel('mm')
plt.show()""")
t('''Zeichne Boxplots der drei Notenspalten nebeneinander (`plot.box`), Titel `Noten`, Bildgröße 4 × 3.''', S,
  """s[['mathe', 'deutsch', 'englisch']].plot.box(title='Noten', figsize=(4, 3))
plt.show()""")
expl('''`df.boxplot(column='wert', by='gruppe')` zeichnet für jede Gruppe einen eigenen Boxplot nebeneinander. `w.index.month` sind die Monate eines Datums-Index.''',
     PLT + """df = pd.DataFrame({'g': ['a', 'a', 'b', 'b'], 'x': [1, 3, 2, 6]})
df.boxplot(column='x', by='g', figsize=(3, 2))
plt.suptitle('')
plt.show()""")
t('''Zeichne die Monatstemperaturen als Boxplots: eine Pivot-Tabelle ist hier unpraktisch. Lege eine Spalte `monat` an (`w.index.month`) und benutze `w.boxplot(column='temperatur', by='monat')` mit
`figsize=(6, 3)`. Setze danach den Titel `Temperatur pro Monat` mit `plt.title`, entferne den automatischen Obertitel mit `plt.suptitle('')`.''', W,
  """w['monat'] = w.index.month
w.boxplot(column='temperatur', by='monat', figsize=(6, 3))
plt.title('Temperatur pro Monat')
plt.suptitle('')
plt.show()""")
t('''Zeichne den Umsatzanteil der Kategorien des Kiosks als Kreisdiagramm mit Prozentangaben (`autopct='%1.0f%%'`), ohne y-Beschriftung (`ylabel=''`), Titel `Umsatzanteile`, Bildgröße 4 × 4.''', K,
  """k.groupby('kategorie')['umsatz'].sum().plot.pie(autopct='%1.0f%%', ylabel='', title='Umsatzanteile', figsize=(4, 4))
plt.show()""")

# ---------------------------------------------------------------- 4
sec('Streudiagramme und Korrelation')
expl('''#### `plot.scatter` und `corr`

`df.plot.scatter(x='a', y='b')` zeichnet ein **Streudiagramm**: einen Punkt pro Zeile. So sieht man, ob zwei Größen zusammenhängen.

`df['a'].corr(df['b'])` ist der **Korrelationskoeffizient** r zwischen −1 und 1: Nahe 1 heißt „je größer a, desto größer b“, nahe −1 „je größer a, desto kleiner b“, nahe 0 „kein linearer Zusammenhang“.
`df[['a', 'b', 'c']].corr()` zeigt alle Paare als Tabelle.''',
     S + """
print(round(s['mathe'].corr(s['englisch']), 2))
s.plot.scatter(x='fehltage', y='mathe', title='Fehltage und Mathenote', figsize=(4, 3))
plt.show()""")

t('''Zeichne für die Bundesländer ein Streudiagramm mit der Fläche auf der x-Achse und den Einwohnern auf der y-Achse (Farbe `'C2'`, Titel `Fläche und Einwohner`, Bildgröße 4 × 3) und gib den
Korrelationskoeffizienten (2 Stellen) aus.''', L,
  """print(round(l['flaeche'].corr(l['einwohner']), 2))
l.plot.scatter(x='flaeche', y='einwohner', color='C2', title='Fläche und Einwohner', figsize=(4, 3))
plt.show()""")
t('''Lass die Korrelationstabelle der Spalten `mathe`, `deutsch`, `englisch` und `fehltage` (2 Stellen) anzeigen.''', S,
  "s[['mathe', 'deutsch', 'englisch', 'fehltage']].corr().round(2)")
t('''Zeichne das Streudiagramm Temperatur (x) gegen Regen (y) für alle Tage mit kleinen Punkten (`s=10`), Titel `Temperatur und Regen`, Bildgröße 4 × 3, und gib den Korrelationskoeffizienten (2 Stellen) aus.''', W,
  """print(round(w['temperatur'].corr(w['regen']), 2))
w.plot.scatter(x='temperatur', y='regen', s=10, title='Temperatur und Regen', figsize=(4, 3))
plt.show()""")
t('''Beschrifte im Streudiagramm Fläche/Einwohner die Punkte der Stadtstaaten (Berlin, Hamburg, Bremen) mit ihrem Kürzel (`ax.annotate(text, (x, y))` in einer Schleife über die drei Zeilen,
`itertuples()`). Titel `Stadtstaaten`, Bildgröße 4 × 3.''', L,
  """ax = l.plot.scatter(x='flaeche', y='einwohner', title='Stadtstaaten', figsize=(4, 3))
for z in l[l['kuerzel'].isin(['BE', 'HH', 'HB'])].itertuples():
    ax.annotate(z.kuerzel, (z.flaeche, z.einwohner))
plt.show()""")

# ---------------------------------------------------------------- 5
sec('Projekt: Bundesländer')
expl('''#### Von der Frage zum Diagramm

Eine kleine Datenanalyse hat meist diese Schritte: **Frage** stellen, Daten **einlesen**, **aufbereiten** (neue Spalten, filtern), **auswerten** (sortieren, gruppieren) und das Ergebnis als
**Tabelle oder Diagramm** darstellen. Die folgenden Aufgaben bauen aufeinander auf; die Zwischenschritte stehen jeweils schon in der Codezelle.''',
     L + """
l['dichte'] = (l['einwohner'] * 1000 / l['flaeche']).round(0)
l.sort_values('dichte', ascending=False).head(3)""")

L2 = L + "\nl['dichte'] = (l['einwohner'] * 1000 / l['flaeche']).round(0)"
t('''Welche Bundesländer sind dichter besiedelt als Deutschland insgesamt? Berechne die Dichte für Deutschland (Summe der Einwohner · 1000 / Summe der Flächen, ganze Zahl) und gib sie aus.
Lass dann Land und Dichte der dichter besiedelten Länder sortiert anzeigen.''', L2,
  """d = round(l['einwohner'].sum() * 1000 / l['flaeche'].sum())
print(d)
l.loc[l['dichte'] > d, ['land', 'dichte']].sort_values('dichte', ascending=False)""")
t('''Teile die Länder in **Stadtstaaten** (BE, HH, HB) und **Flächenländer** ein (Spalte `art`) und lass pro Art die Summe von Einwohnern und Fläche und die Dichte (ganze Zahl) anzeigen.''', L2,
  """l['art'] = l['kuerzel'].apply(lambda x: 'Stadtstaat' if x in ['BE', 'HH', 'HB'] else 'Flächenland')
g = l.groupby('art')[['einwohner', 'flaeche']].sum()
g['dichte'] = (g['einwohner'] * 1000 / g['flaeche']).round(0).astype(int)
g""")
t('''Zeichne die Dichte der **Flächenländer** als senkrechte Balken (Kürzel als Beschriftung, nach Dichte absteigend), Farbe `'C4'`, mit einer waagrechten gestrichelten Linie für die Dichte
Deutschlands (`plt.axhline(d, color='black', linestyle='--')`), Titel `Einwohner pro km²`, `rot=0`, ohne x-Beschriftung, Bildgröße 6 × 3.''', L2,
  """d = round(l['einwohner'].sum() * 1000 / l['flaeche'].sum())
fl = l[~l['kuerzel'].isin(['BE', 'HH', 'HB'])].set_index('kuerzel')['dichte'].sort_values(ascending=False)
fl.plot.bar(color='C4', title='Einwohner pro km²', rot=0, xlabel='', figsize=(6, 3))
plt.axhline(d, color='black', linestyle='--')
plt.show()""")

# ---------------------------------------------------------------- 6
sec('Projekt: Schulkiosk')
K2 = K + "\nk['woche'] = k['datum'].apply(lambda d: 1 if d < pd.Timestamp('2026-10-12') else 2)"
t('''Der Kiosk will wissen, welche Artikel sich lohnen. Lass pro Artikel Menge und Umsatz (2 Stellen) und den Anteil am Gesamtumsatz in Prozent (1 Stelle, Spalte `anteil`) anzeigen,
nach Umsatz absteigend.''', K2,
  """g = k.groupby('artikel')[['menge', 'umsatz']].sum().round(2)
g['anteil'] = (g['umsatz'] / g['umsatz'].sum() * 100).round(1)
g.sort_values('umsatz', ascending=False)""")
t('''Vergleiche die beiden Wochen: Lass eine Pivot-Tabelle mit den Artikeln als Zeilen, den Wochen als Spalten und der Menge anzeigen, mit einer Spalte `plus` (Woche 2 minus Woche 1),
nach `plus` absteigend sortiert (bei Gleichstand nach Artikel: erst `reset_index()`, dann nach `['plus', 'artikel']` sortieren und `artikel` wieder zum Index machen).''', K2,
  """p = k.pivot_table(index='artikel', columns='woche', values='menge', aggfunc='sum')
p['plus'] = p[2] - p[1]
p.reset_index().sort_values(['plus', 'artikel'], ascending=[False, True]).set_index('artikel')""")
t('''Zeichne die Menge pro Artikel für beide Wochen als gruppierte waagrechte Balken (Pivot-Tabelle mit den Wochen als Spalten), Titel `Woche 1 und 2`, Bildgröße 5 × 4.''', K2,
  """p = k.pivot_table(index='artikel', columns='woche', values='menge', aggfunc='sum')
p.plot.barh(title='Woche 1 und 2', figsize=(5, 4))
plt.show()""")
t('''Freitags gibt es mehr Backwaren. Zeichne für die Kategorie `Backwaren` die Menge pro Datum als Linie mit Punkten, Titel `Backwaren`, y-Beschriftung `Stück`, Bildgröße 5 × 3,
und gib die durchschnittliche Menge an Freitagen und an den anderen Tagen (1 Stelle) aus.''', K2,
  """b = k[k['kategorie'] == 'Backwaren']
pro_tag = b.groupby('datum')['menge'].sum()
fr = b.groupby(['datum', 'tag'])['menge'].sum().reset_index()
print(round(fr.loc[fr['tag'] == 'Freitag', 'menge'].mean(), 1), round(fr.loc[fr['tag'] != 'Freitag', 'menge'].mean(), 1))
pro_tag.plot(marker='o', title='Backwaren', ylabel='Stück', figsize=(5, 3))
plt.show()""")

# ---------------------------------------------------------------- 7
sec('Projekt: Wetter')
t('''Erstelle eine Monatsübersicht: pro Monat die mittlere, die höchste und die tiefste Temperatur (1 Stelle), die Regensumme (1 Stelle) und die Zahl der Regentage (Spalten `mittel`, `max`, `min`,
`regen`, `regentage`). Benutze `resample('ME').agg(...)` mit benannten Kennzahlen und setze danach den Index auf die Monatsnamen in `monate`.''',
  W + "\nmonate = ['Jan', 'Feb', 'Mär', 'Apr', 'Mai', 'Jun']",
  """w['regentag'] = w['regen'] > 0
m = w.resample('ME').agg(mittel=('temperatur', 'mean'), max=('temperatur', 'max'), min=('temperatur', 'min'),
                         regen=('regen', 'sum'), regentage=('regentag', 'sum')).round(1)
m.index = monate
m""")
t('''Zeichne ein **Klimadiagramm**: Regensumme pro Monat als blaue Balken (`'C0'`) und das Monatsmittel der Temperatur als rote Linie mit Punkten (`'C3'`, `marker='o'`) auf einer
zweiten y-Achse (`ax2 = ax.twinx()`). Beschrifte die Achsen mit `mm` und `°C`, setze die Monatsnamen als x-Beschriftungen (`ax.set_xticks(range(6))`, `ax.set_xticklabels(monate)`),
Titel `Klimadiagramm Januar bis Juni`, Bildgröße 5 × 3.''',
  W + "\nmonate = ['Jan', 'Feb', 'Mär', 'Apr', 'Mai', 'Jun']",
  """m = w.resample('ME').agg({'temperatur': 'mean', 'regen': 'sum'})
fig, ax = plt.subplots(figsize=(5, 3))
ax.bar(range(6), m['regen'], color='C0')
ax.set_ylabel('mm')
ax2 = ax.twinx()
ax2.plot(range(6), m['temperatur'], color='C3', marker='o')
ax2.set_ylabel('°C')
ax.set_xticks(range(6))
ax.set_xticklabels(monate)
ax.set_title('Klimadiagramm Januar bis Juni')
plt.show()""")
t('''Wie oft folgt auf einen Regentag wieder ein Regentag? Berechne mit `shift(1)` für jeden Tag, ob der Vortag ein Regentag war, und gib den Anteil der Regentage nach einem Regentag und nach einem
trockenen Tag (jeweils Prozent, 1 Stelle) aus.''', W,
  """nass = w['regen'] > 0
vortag = nass.shift(1, fill_value=False)
print(round(nass[vortag].mean() * 100, 1))
print(round(nass[~vortag].mean() * 100, 1))""")

generate('pandas_diagramme_anwendungen', 'pandas 5: Diagramme und Anwendungen', INTRO, ausfuehren=pandasnb.ausfuehrung(), ausgabe_markdown=True)
