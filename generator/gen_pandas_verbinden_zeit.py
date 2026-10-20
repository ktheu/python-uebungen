# Erzeugt ../content/pandas_verbinden_zeit.ipynb (siehe nbgen.py). Viertes Notebook der pandas-Reihe.
# Wetterdaten: beim Generieren mit festem Seed erzeugt (ausgedacht, plausibler Jahresgang), als fester Text in der Setup-Zelle.
# pandas 3: resample mit 'ME' (Monatsende) und 'W' (Woche bis Sonntag); dt.day_name() ist englisch -> eigene deutsche Liste.

import pandasnb
from pandasdaten import wetter_csv
from nbgen import sec, expl, task, predict, generate, setup


def t(text, given='', body='', kind='normal'):
    """Aufgabe, deren Lösung aus dem vorgegebenen Code plus body besteht."""
    task(text, given=given, solution=(given + '\n' + body) if given else body, kind=kind)


DATEIEN = r"""dateien = {
    'wetter.csv': '''""" + wetter_csv() + r"""''',
    'kiosk_woche1.csv': '''datum;artikel;menge
2026-10-05;Brezel;31
2026-10-05;Apfel;12
2026-10-06;Brezel;28
2026-10-06;Apfel;15
2026-10-07;Brezel;35
2026-10-07;Apfel;9
''',
    'kiosk_woche2.csv': '''datum;artikel;menge
2026-10-12;Brezel;26
2026-10-12;Apfel;14
2026-10-13;Brezel;33
2026-10-13;Apfel;11
''',
}
for name, inhalt in dateien.items():
    with open(name, 'w', encoding='utf-8') as f:
        f.write(inhalt)
print('Angelegt:', ', '.join(dateien))"""

INTRO = '''In diesem Notebook verbindest du **mehrere Tabellen** miteinander (wie `JOIN` in SQL) und arbeitest mit **Datum und Zeit**: Tage, Wochen und Monate auswerten,
gleitende Durchschnitte und kumulierte Summen berechnen.

Die Reihe hat fünf Notebooks:

1. Grundlagen: Series und DataFrame, Spalten, Sortieren, CSV-Dateien
2. Auswählen und aufräumen: Filtern, Text-Spalten, fehlende Werte
3. Gruppieren und auswerten: Aggregatfunktionen, groupby, Pivot-Tabellen, Vergleich mit SQL
4. **Verbinden und Zeitreihen**: merge, concat, Datum und Zeit (dieses Notebook)
5. Diagramme und Anwendungen

Jeder Abschnitt beginnt mit kurzen Erklärungen und Beispielen. Führe die Beispiele aus und probiere sie ruhig ein wenig aus.
Danach folgen viele kleine Übungen. Wenn etwas vorgegeben ist, steht es schon in der Codezelle.'''

setup('''#### Beispieldateien anlegen

**Führe diese Zelle zuerst aus.** Sie legt `wetter.csv` (Temperatur in °C und Regen in mm für jeden Tag vom 1. Januar bis 30. Juni 2026; ausgedachte Werte) und zwei kleine
Kiosk-Dateien für zwei Wochen an.''', DATEIEN)

TABELLEN = ("import pandas as pd\n\nschueler = pd.DataFrame({'name': ['Ali', 'Bea', 'Cem', 'Dana', 'Emil'], 'klasse': ['9a', '9a', '9b', '9b', '9c']})\n"
            "klassen = pd.DataFrame({'klasse': ['9a', '9b', '9d'], 'lehrkraft': ['Frau Weber', 'Herr Kaya', 'Frau Graf'], 'raum': [101, 204, 112]})\n"
            "ags = pd.DataFrame({'name': ['Ali', 'Cem', 'Ali', 'Dana', 'Fiona'], 'ag': ['Chor', 'Robotik', 'Robotik', 'Theater', 'Chor']})")
W = "import pandas as pd\n\nw = pd.read_csv('wetter.csv', parse_dates=['datum'])"

# ---------------------------------------------------------------- 1
sec('Tabellen verbinden mit merge')
expl('''#### `pd.merge`

`pd.merge(links, rechts, on='spalte')` verbindet zwei Tabellen über eine gemeinsame Spalte, genau wie `JOIN` in SQL:

| Aufruf | SQL | Ergebnis |
|---|---|---|
| `pd.merge(a, b, on='k')` | `a JOIN b ON a.k = b.k` | nur Zeilen mit Partner in beiden Tabellen |
| `pd.merge(a, b, on='k', how='left')` | `a LEFT JOIN b ON ...` | alle Zeilen von a; ohne Partner steht `NaN` |
| `pd.merge(a, b, left_on='x', right_on='y')` | `ON a.x = b.y` | Spalten mit verschiedenen Namen |

Hat eine Zeile mehrere Partner, entsteht für jeden Partner eine Zeile.''',
     TABELLEN + """
display(pd.merge(schueler, klassen, on='klasse'))
pd.merge(schueler, klassen, on='klasse', how='left')""")

t('Verbinde `schueler` und `klassen` so, dass nur Schüler mit bekannter Klasse vorkommen, und lass Name, Lehrkraft und Raum anzeigen.', TABELLEN,
  "pd.merge(schueler, klassen, on='klasse')[['name', 'lehrkraft', 'raum']]")
t('''Lass alle Schüler mit ihrer Lehrkraft anzeigen, auch die ohne bekannte Klasse (`how='left'`).''', TABELLEN,
  "pd.merge(schueler, klassen, on='klasse', how='left')[['name', 'klasse', 'lehrkraft']]")
t('''Gib die Namen der Schüler aus, deren Klasse **nicht** in `klassen` steht (`how='left'`, dann die Zeilen mit fehlender Lehrkraft).''', TABELLEN,
  """m = pd.merge(schueler, klassen, on='klasse', how='left')
print(m.loc[m['lehrkraft'].isna(), 'name'].tolist())""")
t('Verbinde `schueler` mit `ags` (ein Schüler kann mehrere AGs haben) und lass Name, Klasse und AG anzeigen, sortiert nach Name und AG.', TABELLEN,
  "pd.merge(schueler, ags, on='name').sort_values(['name', 'ag'])")
t('''Lass für jede AG anzeigen, in welchen Klassen ihre Mitglieder sind: Verbinde `ags` mit `schueler` (`how='left'`, Fiona ist kein Schüler aus der Liste) und gruppiere nach AG
mit der Anzahl der Mitglieder (`anzahl`) und der Anzahl verschiedener Klassen (`klassen`, `nunique`).''', TABELLEN,
  """m = pd.merge(ags, schueler, on='name', how='left')
m.groupby('ag').agg(anzahl=('name', 'count'), klassen=('klasse', 'nunique'))""")
t('''Verbinde alle drei Tabellen: Schüler mit AGs und dann mit den Klassen. Lass Name, AG und Raum für alle Zeilen mit bekanntem Raum anzeigen, sortiert nach Raum und Name.''', TABELLEN,
  """m = pd.merge(pd.merge(schueler, ags, on='name'), klassen, on='klasse')
m[['name', 'ag', 'raum']].sort_values(['raum', 'name'])""")
t('''Die Spalten heißen verschieden: In `bestellungen` steht die Kundennummer in `kunde`, in `kunden` in `id`. Verbinde mit `left_on`/`right_on` und lass Name und Betrag anzeigen.''',
  "import pandas as pd\n\nkunden = pd.DataFrame({'id': [1, 2, 3], 'name': ['Mia', 'Tom', 'Ida']})\nbestellungen = pd.DataFrame({'kunde': [2, 1, 2, 3], 'betrag': [12.5, 8.0, 30.0, 4.5]})",
  "pd.merge(bestellungen, kunden, left_on='kunde', right_on='id')[['name', 'betrag']]")
predict("""import pandas as pd

a = pd.DataFrame({'k': [1, 2, 3], 'x': ['a', 'b', 'c']})
b = pd.DataFrame({'k': [2, 3, 3, 4], 'y': [10, 20, 30, 40]})
print(len(pd.merge(a, b, on='k')), len(pd.merge(a, b, on='k', how='left')))
print(pd.merge(a, b, on='k')['y'].sum())""")

# ---------------------------------------------------------------- 2
sec('Tabellen aneinanderhängen mit concat')
expl('''#### `pd.concat`

`pd.concat([df1, df2])` hängt Tabellen mit denselben Spalten **untereinander**, z. B. die Daten mehrerer Wochen oder Dateien. Mit `ignore_index=True` wird der Index neu durchnummeriert.
Fehlt eine Spalte in einer Tabelle, steht dort `NaN`.''',
     """import pandas as pd

w1 = pd.read_csv('kiosk_woche1.csv', sep=';')
w2 = pd.read_csv('kiosk_woche2.csv', sep=';')
alle = pd.concat([w1, w2], ignore_index=True)
print(len(w1), len(w2), len(alle))
alle.tail(3)""")

t('Hänge die beiden Kiosk-Wochen aneinander und lass die Gesamtmenge pro Artikel anzeigen.', "import pandas as pd",
  """alle = pd.concat([pd.read_csv('kiosk_woche1.csv', sep=';'), pd.read_csv('kiosk_woche2.csv', sep=';')], ignore_index=True)
alle.groupby('artikel')['menge'].sum()""")
t('''Füge vor dem Aneinanderhängen jeder Woche eine Spalte `woche` mit 1 bzw. 2 hinzu. Lass dann eine Pivot-Tabelle mit den Artikeln als Zeilen, den Wochen als Spalten und dem Durchschnitt der
Tagesmenge (1 Stelle) anzeigen.''', "import pandas as pd",
  """w1 = pd.read_csv('kiosk_woche1.csv', sep=';')
w2 = pd.read_csv('kiosk_woche2.csv', sep=';')
w1['woche'] = 1
w2['woche'] = 2
alle = pd.concat([w1, w2], ignore_index=True)
alle.pivot_table(index='artikel', columns='woche', values='menge', aggfunc='mean').round(1)""")
t('''Erzeuge aus den Listen `jahre` eine Tabelle: Für jedes Jahr gibt es einen eigenen DataFrame mit den Spalten `jahr` und `schueler`. Hänge sie mit `concat` aneinander (`ignore_index=True`) und lass das Ergebnis anzeigen.''',
  "import pandas as pd\n\njahre = {2024: 812, 2025: 836, 2026: 851}",
  """teile = []
for jahr, anzahl in jahre.items():
    teile.append(pd.DataFrame({'jahr': [jahr], 'schueler': [anzahl]}))
pd.concat(teile, ignore_index=True)""")
predict("""import pandas as pd

a = pd.DataFrame({'x': [1, 2]})
b = pd.DataFrame({'x': [3], 'y': [9]})
c = pd.concat([a, b], ignore_index=True)
print(c.shape, c['x'].tolist(), c['y'].isna().sum())""")

# ---------------------------------------------------------------- 3
sec('Datum und Zeit')
expl('''#### Datumsspalten

Datumsangaben in einer CSV-Datei liest pandas als Text, außer man gibt `parse_dates=['datum']` an. Eine vorhandene Textspalte wandelt man mit `pd.to_datetime(df['datum'])` um.

Über `.dt` erhält man Teile des Datums: `dt.year`, `dt.month`, `dt.day`, `dt.dayofweek` (0 = Montag), `dt.strftime('%d.%m.%Y')`.
(`dt.day_name()` liefert englische Namen; deutsche Namen nimmt man aus einer eigenen Liste.)

Mit Daten kann man vergleichen (`df['datum'] >= '2026-03-01'`) und rechnen: Die Differenz zweier Daten ist eine Zeitspanne mit `.days`.''',
     W + """
print(w['datum'].dtype)
w['monat'] = w['datum'].dt.month
tage = ['Mo', 'Di', 'Mi', 'Do', 'Fr', 'Sa', 'So']
w['wochentag'] = w['datum'].dt.dayofweek.map(lambda i: tage[i])
print((w['datum'].max() - w['datum'].min()).days)
w.head(3)""")

t('Lass die Tage im März mit einer Temperatur über 10 °C anzeigen (Datum und Temperatur).', W,
  "w.loc[(w['datum'].dt.month == 3) & (w['temperatur'] > 10), ['datum', 'temperatur']]")
t('Lass für jeden Monat (Spalte `monat`) die Durchschnittstemperatur (1 Stelle) und die Regensumme (1 Stelle) anzeigen (Spalten `temperatur`, `regen`).', W,
  """w['monat'] = w['datum'].dt.month
w.groupby('monat').agg(temperatur=('temperatur', 'mean'), regen=('regen', 'sum')).round(1)""")
t('''Gib den wärmsten und den kältesten Tag mit Temperatur aus, das Datum im Format `TT.MM.JJJJ` (`strftime('%d.%m.%Y')` eines einzelnen Datums).''', W,
  """warm = w.loc[w['temperatur'].idxmax()]
kalt = w.loc[w['temperatur'].idxmin()]
print(warm['datum'].strftime('%d.%m.%Y'), warm['temperatur'])
print(kalt['datum'].strftime('%d.%m.%Y'), kalt['temperatur'])""")
t('''Lass für jeden Wochentag (Mo bis So, deutsche Abkürzungen aus der Liste `tage`) anzeigen, an wie vielen Tagen es geregnet hat (`regen > 0`) und wie viel Regen im Durchschnitt fiel (1 Stelle).
Die Reihenfolge soll Mo bis So sein: gruppiere nach `dt.dayofweek` und setze danach den Index auf `tage`.''', W + "\ntage = ['Mo', 'Di', 'Mi', 'Do', 'Fr', 'Sa', 'So']",
  """w['nass'] = w['regen'] > 0
g = w.groupby(w['datum'].dt.dayofweek).agg(regentage=('nass', 'sum'), regen=('regen', 'mean')).round(1)
g.index = tage
g""")
t('''Wie viele Tage liegen zwischen dem ersten Tag mit mindestens 20 °C und dem letzten Frosttag (Temperatur unter 0 °C) im Datensatz? Gib beide Daten (`strftime('%d.%m.')`) und die Anzahl der Tage aus.''', W,
  """erster_warm = w.loc[w['temperatur'] >= 20, 'datum'].min()
letzter_frost = w.loc[w['temperatur'] < 0, 'datum'].max()
print(letzter_frost.strftime('%d.%m.'), erster_warm.strftime('%d.%m.'))
print((erster_warm - letzter_frost).days)""")
expl('''`pd.Timestamp('2026-09-01')` ist ein einzelner Zeitpunkt. Zieht man ihn von einer Datumsspalte ab, erhält man eine Spalte mit Zeitspannen; `.dt.days` macht daraus ganze Tage.''',
     """import pandas as pd

s = pd.to_datetime(pd.Series(['2026-09-03', '2026-09-10']))
print((s - pd.Timestamp('2026-09-01')).dt.days.tolist())""")
t('''Wandle die Textspalte `datum` von `ereignisse` mit `pd.to_datetime` um (das Format ist `%d.%m.%Y`, also `format='%d.%m.%Y'`), sortiere nach Datum und lass die Tabelle mit einer Spalte `tage_bis`
anzeigen: Tage vom 1. September 2026 (`pd.Timestamp('2026-09-01')`) bis zum Ereignis.''',
  "import pandas as pd\n\nereignisse = pd.DataFrame({'was': ['Herbstferien', 'Schulfest', 'Abiball', 'Wandertag'], 'datum': ['26.10.2026', '18.07.2027', '02.07.2027', '23.09.2026']})",
  """ereignisse['datum'] = pd.to_datetime(ereignisse['datum'], format='%d.%m.%Y')
ereignisse = ereignisse.sort_values('datum')
ereignisse['tage_bis'] = (ereignisse['datum'] - pd.Timestamp('2026-09-01')).dt.days
ereignisse""")
predict("""import pandas as pd

d = pd.to_datetime(pd.Series(['2026-03-01', '2026-03-15', '2026-04-02']))
print(d.dt.month.tolist(), d.dt.day.tolist())
print((d.iloc[2] - d.iloc[0]).days)""")

# ---------------------------------------------------------------- 4
sec('Zeitreihen')
expl('''#### Datum als Index: `resample`

Macht man das Datum zum Index (`set_index('datum')`), kann man die Werte nach Zeitabschnitten zusammenfassen:
`df.resample('ME').mean()` bildet Monatsmittel (`'ME'` = Monatsende als Beschriftung), `'W'` Wochen (bis Sonntag), `'D'` Tage.

Ausschnitte wählt man mit `df.loc['2026-03']` (ganzer März) oder `df.loc['2026-03-10':'2026-03-20']` aus.''',
     W + """
w = w.set_index('datum')
display(w.loc['2026-03-10':'2026-03-13'])
w.resample('ME').mean().round(1)""")
expl('''#### Verlauf: `cumsum`, `diff`, `pct_change`, `rolling`, `shift`

| Aufruf | Ergebnis |
|---|---|
| `s.cumsum()` | kumulierte Summe (laufende Summe) |
| `s.diff()` | Änderung zum vorigen Wert |
| `s.pct_change()` | prozentuale Änderung zum vorigen Wert (als Anteil) |
| `s.rolling(7).mean()` | **gleitender Durchschnitt** über 7 Werte (die ersten 6 sind `NaN`) |
| `s.shift(1)` | Werte um eine Zeile nach unten verschoben (der Vortag) |''',
     """import pandas as pd

s = pd.Series([2, 4, 3, 7, 6])
print(s.cumsum().tolist(), s.diff().tolist())
print(s.rolling(3).mean().round(2).tolist())
print(s.shift(1).tolist())""")

WI = W + "\nw = w.set_index('datum')"
t('Lass die Monatsmittel der Temperatur und die Monatssummen des Regens (beides 1 Stelle) in einer Tabelle anzeigen (`resample(\'ME\').agg({...})`).', WI,
  "w.resample('ME').agg({'temperatur': 'mean', 'regen': 'sum'}).round(1)")
t('Lass die Tage vom 1. bis 7. Mai anzeigen und gib die Durchschnittstemperatur im ganzen Mai (1 Stelle) aus.', WI,
  """print(round(w.loc['2026-05', 'temperatur'].mean(), 1))
w.loc['2026-05-01':'2026-05-07']""")
t('''Berechne den gleitenden 7-Tage-Durchschnitt der Temperatur (`rolling(7).mean()`, 1 Stelle) als Spalte `mittel7` und lass die Tage 1. bis 10. Februar mit Temperatur und `mittel7` anzeigen.''', WI,
  """w['mittel7'] = w['temperatur'].rolling(7).mean().round(1)
w.loc['2026-02-01':'2026-02-10', ['temperatur', 'mittel7']]""")
t('''Berechne die laufende Regensumme seit dem 1. Januar (`cumsum`) und gib aus, an welchem Datum (`strftime('%d.%m.')`) die Summe zum ersten Mal 100 mm überschreitet.''', WI,
  """summe = w['regen'].cumsum()
print(summe[summe > 100].index[0].strftime('%d.%m.'))""")
t('''Finde den Tag mit dem größten Temperatursturz zum Vortag (`diff()`, kleinster Wert): Gib das Datum (`strftime('%d.%m.')`) und die Änderung (1 Stelle) aus.''', WI,
  """d = w['temperatur'].diff()
print(d.idxmin().strftime('%d.%m.'), round(d.min(), 1))""")
expl('''`series.to_frame()` macht aus einer Series einen DataFrame mit einer Spalte (die Spalte heißt wie die Series, mit `to_frame('name')` bekommt sie einen eigenen Namen). Dann kann man weitere Spalten hinzufügen.''',
     """import pandas as pd

pd.Series([1, 2], name='x').to_frame()""")
t('''Lass die Wochensummen des Regens (`resample('W')`, 1 Stelle) der Wochen im April anzeigen (die Wochen, deren Ende im April liegt: `.loc['2026-04']`) und die prozentuale Änderung zur Vorwoche
(`pct_change() * 100`, 1 Stelle) als zweite Spalte `aenderung`.''', WI,
  """woche = w['regen'].resample('W').sum().round(1).to_frame()
woche['aenderung'] = (woche['regen'].pct_change() * 100).round(1)
woche.loc['2026-04']""")
t('''Zähle die **längste Serie** aufeinanderfolgender Regentage (Regen > 0): Gehe die Werte mit einer Schleife durch, zähle die aktuelle Serie hoch oder setze sie auf 0 zurück und merke dir das Maximum.
Gib die Länge aus.''', WI,
  """laengste = 0
aktuell = 0
for r in w['regen']:
    if r > 0:
        aktuell += 1
        laengste = max(laengste, aktuell)
    else:
        aktuell = 0
print(laengste)""")
predict("""import pandas as pd

s = pd.Series([1, 3, 6, 10])
print(s.diff().tolist())
print(s.cumsum().tolist())
print(s.rolling(2).mean().tolist())""")

# ---------------------------------------------------------------- 5
sec('Gemischte Übungen')
expl('''`df.itertuples()` durchläuft die Zeilen eines DataFrames; jede Zeile ist ein namedtuple, die Spalten erreicht man mit `zeile.spalte` (siehe Notebook zu `collections`).''',
     """import pandas as pd

df = pd.DataFrame({'a': [1, 2], 'b': ['x', 'y']})
for zeile in df.itertuples():
    print(zeile.a, zeile.b)""")
t('''Verbinde die Temperaturen mit einer Tabelle der Ferien (`ferien`, mit `start` und `ende`): Lege eine Spalte `ferien` an, die `True` ist, wenn das Datum in einem der Zeiträume liegt
(Schleife über die Zeilen von `ferien` mit `itertuples()`, für jede `between(start, ende)` mit `|` verknüpfen). Gib die Durchschnittstemperatur in den Ferien und außerhalb (1 Stelle) aus.''',
  W + "\nferien = pd.DataFrame({'name': ['Winter', 'Ostern', 'Pfingsten'], 'start': pd.to_datetime(['2026-01-01', '2026-03-30', '2026-05-26']),\n"
  "                       'ende': pd.to_datetime(['2026-01-05', '2026-04-11', '2026-06-05'])})",
  """w['ferien'] = False
for f in ferien.itertuples():
    w['ferien'] = w['ferien'] | w['datum'].between(f.start, f.ende)
print(round(w.loc[w['ferien'], 'temperatur'].mean(), 1))
print(round(w.loc[~w['ferien'], 'temperatur'].mean(), 1))""")
t('''Ein Schwimmbad öffnet an Tagen mit mindestens 20 °C. Lass pro Monat anzeigen, an wie vielen Tagen es geöffnet hat (nur Monate mit mindestens einem Tag, Spalte `tage`).''', W,
  """offen = w[w['temperatur'] >= 20]
g = offen.groupby(offen['datum'].dt.month).size().to_frame('tage')
g""")
t('''Vergleiche die erste und zweite Hälfte jedes Monats: Lege eine Spalte `haelfte` an (1 für Tag 1–15, 2 sonst) und lass eine Pivot-Tabelle (Monate als Zeilen, Hälften als Spalten,
mittlere Temperatur auf 1 Stelle) anzeigen.''', W,
  """w['monat'] = w['datum'].dt.month
w['haelfte'] = w['datum'].dt.day.apply(lambda d: 1 if d <= 15 else 2)
w.pivot_table(index='monat', columns='haelfte', values='temperatur', aggfunc='mean').round(1)""")

generate('pandas_verbinden_zeit', 'pandas 4: Tabellen verbinden und Zeitreihen', INTRO, ausfuehren=pandasnb.ausfuehrung(), ausgabe_markdown=True)
