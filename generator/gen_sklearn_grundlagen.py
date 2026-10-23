# Erzeugt ../content/sklearn_grundlagen.ipynb (siehe nbgen.py). Erstes Notebook der scikit-learn-Reihe:
# sklearn_grundlagen, sklearn_klassifikation, sklearn_regression, sklearn_unueberwacht.
#
# JupyterLite: scikit-learn 1.8.0 (mit scipy 1.18.0, numpy 2.4.6, pandas 3.0.2), lokal in der py-3.13-venv p313uebungen.
#     python generator/gen_sklearn_grundlagen.py
#     py -3.13 generator/pyodide_check/pruefen.py generator/gen_sklearn_grundlagen.py
#
# Fallstricke:
# - Erwartete Ausgaben wie in JupyterLab (pandasnb.py): DataFrames in der letzten Zeile als HTML-Tabelle.
#   Ein Modell darf NIE allein in der letzten Zeile stehen (auch nicht modell.fit(X, y)): JupyterLab zeigt es als Grafik, pandasnb als Text.
# - Neue Daten für predict() immer als DataFrame mit denselben Spaltennamen, sonst UserWarning "X does not have valid feature names".
# - Beim ersten fit() eines k-NN-Modells meldet Pyodide eine RuntimeWarning (JsProxy.as_object_map, aus threadpoolctl).
#   Die Setup-Zelle blendet sie aus.
# - Zahlen mit f-Strings ausgeben (f'{x:.3f}'), in Code-Zellen höchstens eine Leerzeile.
import pandasnb
from nbgen import sec, expl, predict, generate, setup
from sklearnhilfe import t, WARNUNG, WARNUNG_MD, IRIS_CSV, IRIS_MD, reihe, SCHLUSS

OBST_CSV = '''gewicht,verhaeltnis,sorte
230,1.2,Birne
165,0.96,Apfel
190,1.21,Birne
135,1.15,Birne
193,0.98,Apfel
198,0.97,Apfel
166,1.23,Birne
194,1.26,Birne
211,1.22,Birne
204,1.31,Birne
141,1.22,Birne
151,1.13,Birne
150,0.96,Apfel
159,1.22,Birne
169,0.96,Apfel
206,1.29,Birne
214,1.22,Birne
205,1.18,Birne
207,1.0,Apfel
204,0.9,Apfel
203,1.25,Birne
141,0.98,Apfel
147,1.12,Birne
111,0.97,Apfel
175,1.26,Birne
184,0.9,Apfel
196,0.99,Apfel
175,1.3,Birne
177,1.29,Birne
196,0.91,Apfel
209,1.29,Birne
171,1.3,Birne
164,0.96,Apfel
187,1.29,Birne
174,1.08,Apfel
161,0.93,Apfel
179,1.24,Birne
139,0.93,Apfel
181,0.99,Apfel
179,0.92,Apfel
144,0.99,Apfel
131,0.98,Apfel
193,1.02,Apfel
144,0.9,Apfel
169,0.92,Apfel
172,0.94,Apfel
171,1.24,Birne
175,1.29,Birne
'''

SETUP = WARNUNG + '\n\n' + IRIS_CSV + f"""

obst = '''{OBST_CSV}'''
with open('obst.csv', 'w', encoding='utf-8') as f:
    f.write(obst)
print('Angelegt: iris.csv, obst.csv')"""

INTRO = '''**scikit-learn** (kurz `sklearn`) ist das bekannteste Python-Paket für **maschinelles Lernen**: Der Computer lernt aus Beispielen,
z. B. aus vielen vermessenen Blüten, zu welcher Art eine neue Blüte gehört. Niemand schreibt dafür Regeln von Hand.
Dieses Notebook zeigt das Grundmuster, das bei allen Verfahren gleich ist, und wie man prüft, wie gut ein Modell ist.

''' + reihe(1) + '''

Vorausgesetzt werden *numpy: Grundlagen* und *matplotlib: Grundlagen*. Die Daten stehen in pandas-Tabellen; was du davon brauchst,
wiederholt der erste Abschnitt. Wer die pandas-Notebooks kennt, kann ihn überspringen.

''' + SCHLUSS

setup(f'''#### Beispieldaten anlegen

**Führe diese Zelle zuerst aus.** Sie legt zwei Dateien an:

- {IRIS_MD}
- `obst.csv`: ausgedachte Daten von 48 Äpfeln und Birnen mit dem Gewicht in g und dem Verhältnis von Höhe zu Breite.

{WARNUNG_MD}''', SETUP)

IRIS = "import pandas as pd\n\niris = pd.read_csv('iris.csv')"
OBST = "import pandas as pd\n\nobst = pd.read_csv('obst.csv')"
KNN_IRIS = '''import pandas as pd
from sklearn.neighbors import KNeighborsClassifier

iris = pd.read_csv('iris.csv')
X = iris[['bluete_laenge', 'bluete_breite']]
y = iris['art']'''
SPLIT_IRIS = '''import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

iris = pd.read_csv('iris.csv')
X = iris[['kelch_laenge', 'kelch_breite', 'bluete_laenge', 'bluete_breite']]
y = iris['art']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=0)'''
SPLIT_40 = '''import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

iris = pd.read_csv('iris.csv')
X = iris[['kelch_laenge', 'kelch_breite', 'bluete_laenge', 'bluete_breite']]
y = iris['art']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.4, random_state=0)'''
SPLIT_OBST = '''import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

obst = pd.read_csv('obst.csv')
X = obst[['gewicht', 'verhaeltnis']]
y = obst['sorte']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=0)'''

# ---------------------------------------------------------------- 1
sec('pandas zum Auffrischen')
expl('''#### Eine Tabelle einlesen

`pd.read_csv('datei.csv')` liest eine CSV-Datei in einen **DataFrame**, eine Tabelle mit benannten Spalten. Jede Zeile ist ein **Datensatz**
(hier: eine Blüte).

- `df.head(n)` zeigt die ersten `n` Zeilen (ohne Angabe 5).
- `df.shape` ist ein Tupel (Anzahl Zeilen, Anzahl Spalten), `len(df)` die Anzahl der Zeilen.
- `df.columns` sind die Spaltennamen, `list(df.columns)` macht daraus eine Liste.''',
     """import pandas as pd

iris = pd.read_csv('iris.csv')
print(iris.shape)
print(list(iris.columns))
iris.head()""")
expl('''#### Spalten und Kennzahlen

- `df['spalte']` ist **eine** Spalte (eine *Series*), `df[['a', 'b']]` mit **doppelten** Klammern ist eine Tabelle mit diesen Spalten.
- `df['spalte'].mean()`, `.min()`, `.max()` berechnen Kennzahlen einer Spalte.
- `df.describe()` zeigt die wichtigsten Kennzahlen aller Zahlenspalten.
- `df['spalte'].value_counts()` zählt, wie oft jeder Wert vorkommt. Bei gleichen Anzahlen ist die Reihenfolge nicht festgelegt;
  `.sort_index()` sortiert das Ergebnis nach den Werten (alphabetisch).''',
     """import pandas as pd

iris = pd.read_csv('iris.csv')
print(iris['bluete_laenge'].mean())
print(iris['art'].value_counts().sort_index())
iris[['bluete_laenge', 'bluete_breite']].describe()""")
expl('''#### Zeilen auswählen und Gruppen vergleichen

- `df[df['spalte'] > 5]` wählt die Zeilen aus, für die die Bedingung gilt. Mehrere Bedingungen verbindet man mit `&` (und) bzw. `|` (oder),
  jede in Klammern: `df[(df['a'] > 1) & (df['b'] == 'x')]`.
- `df.groupby('art').mean()` berechnet die Mittelwerte jeder Spalte getrennt für jede Art.''',
     """import pandas as pd

iris = pd.read_csv('iris.csv')
gross = iris[iris['bluete_laenge'] > 6.5]
print(len(gross))
display(gross)
iris.groupby('art').mean()""")

t('Lies `obst.csv` ein, gib die Form der Tabelle und die Spaltennamen als Liste aus und zeige die ersten 3 Zeilen an.', 'import pandas as pd',
  """obst = pd.read_csv('obst.csv')
print(obst.shape)
print(list(obst.columns))
obst.head(3)""")
t('Gib aus, wie viele Äpfel und wie viele Birnen in der Tabelle stehen (alphabetisch sortiert).', OBST, "print(obst['sorte'].value_counts().sort_index())")
t('Gib das kleinste, das größte und das mittlere Gewicht aus (das mittlere mit einer Nachkommastelle).', OBST,
  """print(obst['gewicht'].min())
print(obst['gewicht'].max())
print(f"{obst['gewicht'].mean():.1f}")""")
t('Zeige die Kennzahlen (`describe()`) der beiden Zahlenspalten an.', OBST, "obst[['gewicht', 'verhaeltnis']].describe()")
t('Zeige die Mittelwerte von Gewicht und Verhältnis für Äpfel und Birnen getrennt an.', OBST, "obst.groupby('sorte').mean()")
t('Zeige alle Früchte an, die schwerer als 205 g sind.', OBST, "obst[obst['gewicht'] > 205]")
t('Wie viele Äpfel haben ein Verhältnis von mindestens 1.0? Gib die Anzahl aus.', OBST,
  "print(len(obst[(obst['sorte'] == 'Apfel') & (obst['verhaeltnis'] >= 1.0)]))")
t('Zeige für die Iris-Daten die Mittelwerte aller vier Maße je Art an, gerundet auf eine Nachkommastelle (`.round(1)`).', IRIS,
  "iris.groupby('art').mean().round(1)")
t('''Zeichne ein Streudiagramm der Iris-Blüten mit der Blütenblattlänge auf der x-Achse und der Blütenblattbreite auf der y-Achse.
Zeichne jede Art in einer eigenen Farbe mit `label` (Schleife über die drei Arten, jeweils `plt.scatter()` mit den Zeilen dieser Art) und zeige die Legende an.''',
  IRIS + '\nimport matplotlib.pyplot as plt',
  """for art in ['setosa', 'versicolor', 'virginica']:
    teil = iris[iris['art'] == art]
    plt.scatter(teil['bluete_laenge'], teil['bluete_breite'], label=art)
plt.xlabel('bluete_laenge')
plt.ylabel('bluete_breite')
plt.legend()
plt.show()""")
predict("""import pandas as pd

df = pd.DataFrame({'a': [1, 2, 3, 4], 'b': ['x', 'y', 'x', 'x']})
print(df.shape)
print(len(df[df['a'] > 2]))
print(df['b'].value_counts()['x'])""", erklaerung='''- Die Tabelle hat 4 Zeilen und 2 Spalten: `(4, 2)`.
- Nur die Zeilen mit `a` gleich 3 und 4 erfüllen `a > 2`: `2`.
- Der Wert `'x'` kommt dreimal in Spalte `b` vor: `3`.''')

# ---------------------------------------------------------------- 2
sec('Merkmale und Zielwerte')
expl('''#### Lernen aus Beispielen

Beim **überwachten Lernen** gibt man dem Computer viele Beispiele, bei denen die richtige Antwort bekannt ist.

- Die **Merkmale** (*features*) sind die gemessenen Eigenschaften, hier z. B. die Maße einer Blüte. Man schreibt sie in eine Tabelle `X`
  (großes X, weil es mehrere Spalten sind).
- Der **Zielwert** (*target*, *label*) ist die gesuchte Antwort, hier die Art. Er steht in einer Spalte `y`.

Ist der Zielwert eine Kategorie (Art, Sorte, ja/nein), heißt die Aufgabe **Klassifikation**, die möglichen Werte heißen **Klassen**.
Ist er eine Zahl (Preis, Temperatur), heißt sie **Regression** (Notebook 3).

`y.unique()` sind die verschiedenen Werte von `y`, `sorted()` macht daraus eine sortierte Liste.''',
     """import pandas as pd

iris = pd.read_csv('iris.csv')
X = iris[['kelch_laenge', 'kelch_breite', 'bluete_laenge', 'bluete_breite']]
y = iris['art']
print(X.shape, y.shape)
print(sorted(y.unique()))
X.head(3)""")

t('Lege für die Obst-Daten `X` (die Spalten `gewicht` und `verhaeltnis`) und `y` (die Spalte `sorte`) an und gib ihre Formen aus.', OBST,
  """X = obst[['gewicht', 'verhaeltnis']]
y = obst['sorte']
print(X.shape, y.shape)""")
t('Gib die Klassen der Obst-Daten als sortierte Liste aus (`sorted(y.unique())`) und wie viele Klassen es sind.', OBST,
  """y = obst['sorte']
print(sorted(y.unique()))
print(len(y.unique()))""")
t('Lege für die Iris-Daten `X` nur mit den beiden Kelchblatt-Spalten an und zeige die letzten 3 Zeilen an (`tail(3)`).', IRIS,
  """X = iris[['kelch_laenge', 'kelch_breite']]
X.tail(3)""")
t('''Ist es eine Klassifikation oder eine Regression? Speichere für jede der vier Fragen den String `'Klassifikation'` oder `'Regression'` in der Liste `antworten`
und gib sie aus: (1) Ist eine E-Mail Spam? (2) Wie viel kostet eine Wohnung? (3) Welche Ziffer zeigt ein Bild? (4) Wie hoch wird morgen die Temperatur?''', '',
  """antworten = ['Klassifikation', 'Regression', 'Klassifikation', 'Regression']
print(antworten)""")
t('''Zeichne die Obst-Daten als Streudiagramm (Gewicht auf der x-Achse, Verhältnis auf der y-Achse), Äpfel rot und Birnen grün, mit Legende
und Achsenbeschriftungen `gewicht in g` und `verhaeltnis`.''', OBST + '\nimport matplotlib.pyplot as plt',
  """for sorte, farbe in [('Apfel', 'red'), ('Birne', 'green')]:
    teil = obst[obst['sorte'] == sorte]
    plt.scatter(teil['gewicht'], teil['verhaeltnis'], color=farbe, label=sorte)
plt.xlabel('gewicht in g')
plt.ylabel('verhaeltnis')
plt.legend()
plt.show()""")
predict("""import pandas as pd

df = pd.DataFrame({'groesse': [1.6, 1.8, 1.7], 'gewicht': [55, 80, 70], 'sport': ['ja', 'nein', 'ja']})
X = df[['groesse', 'gewicht']]
y = df['sport']
print(X.shape)
print(y.shape)
print(type(X).__name__, type(y).__name__)""", erklaerung='''- `X` hat 3 Zeilen und 2 Spalten: `(3, 2)`.
- `y` ist eine einzelne Spalte mit 3 Werten. Die Form einer Series hat nur eine Angabe: `(3,)`.
- Mit doppelten Klammern entsteht ein `DataFrame`, mit einfachen eine `Series`.''')

# ---------------------------------------------------------------- 3
sec('Das erste Modell: k-nächste Nachbarn')
expl('''#### Die Idee

Das Verfahren **k-nächste Nachbarn** (*k-nearest neighbors*, k-NN) ist besonders einfach: Um eine neue Blüte einzuordnen, sucht es unter allen bekannten
Blüten die `k` ähnlichsten, also die mit dem kleinsten Abstand der Merkmale. Die Art, die unter diesen `k` Nachbarn am häufigsten vorkommt, ist die Vorhersage.
Das „Lernen“ besteht hier nur darin, sich alle Beispiele zu merken.''', None)
expl('''#### Das Grundmuster: erzeugen, `fit`, `predict`

Alle Verfahren in scikit-learn werden gleich benutzt:

1. **Modell erzeugen**, mit Einstellungen in Klammern: `modell = KNeighborsClassifier(n_neighbors=3)`
2. **Trainieren** mit den Beispielen: `modell.fit(X, y)`
3. **Vorhersagen** für neue Daten: `modell.predict(X_neu)`. Das Ergebnis ist ein Array mit einer Vorhersage pro Zeile.

Die neuen Daten müssen eine Tabelle mit **denselben Spalten** wie `X` sein, auch wenn es nur eine Zeile ist.
`modell.classes_` enthält die Klassen, die das Modell kennt.''',
     KNN_IRIS + """

modell = KNeighborsClassifier(n_neighbors=3)
modell.fit(X, y)
neu = pd.DataFrame({'bluete_laenge': [1.5, 4.8, 6.0], 'bluete_breite': [0.3, 1.6, 2.2]})
print(modell.predict(neu))
print(modell.classes_)""")
expl('''#### Die Nachbarn ansehen und die Treffer zählen

- `modell.kneighbors(neu)` gibt zwei Arrays zurück: die Abstände zu den `k` nächsten Nachbarn und deren Zeilennummern in `X`.
- `modell.score(X, y)` sagt alle Zeilen von `X` vorher und gibt den Anteil der richtigen Vorhersagen zurück, die **Genauigkeit** (*accuracy*).''',
     KNN_IRIS + """

modell = KNeighborsClassifier(n_neighbors=3)
modell.fit(X, y)
neu = pd.DataFrame({'bluete_laenge': [4.87], 'bluete_breite': [1.58]})
abstaende, zeilen = modell.kneighbors(neu)
print(abstaende.round(3))
print(y.iloc[zeilen[0]].tolist())
print(f'{modell.score(X, y):.3f}')""")

t('''Trainiere ein k-NN-Modell mit `n_neighbors=3` auf den Obst-Daten (Merkmale `gewicht` und `verhaeltnis`) und sage die Sorte einer Frucht mit 180 g
und dem Verhältnis 1.2 voraus.''', OBST + '\nfrom sklearn.neighbors import KNeighborsClassifier',
  """X = obst[['gewicht', 'verhaeltnis']]
y = obst['sorte']
modell = KNeighborsClassifier(n_neighbors=3)
modell.fit(X, y)
neu = pd.DataFrame({'gewicht': [180], 'verhaeltnis': [1.2]})
print(modell.predict(neu))""")
t('''Sage mit dem Iris-Modell aus dem Beispiel (Blütenblattlänge und -breite, `k = 3`) die Arten von vier neuen Blüten auf einmal voraus:
(1.4 | 0.2), (4.0 | 1.2), (5.5 | 2.0) und (4.9 | 1.7).''', KNN_IRIS,
  """modell = KNeighborsClassifier(n_neighbors=3)
modell.fit(X, y)
neu = pd.DataFrame({'bluete_laenge': [1.4, 4.0, 5.5, 4.9], 'bluete_breite': [0.2, 1.2, 2.0, 1.7]})
print(modell.predict(neu))""")
t('''Trainiere das Iris-Modell mit `k = 1`, `k = 5` und `k = 15` und sage jeweils die Art der Blüte (4.87 | 1.58) voraus.
Gib `k` und die Vorhersage aus. (`modell.predict(neu)[0]` ist die erste und hier einzige Vorhersage.)''', KNN_IRIS,
  """neu = pd.DataFrame({'bluete_laenge': [4.87], 'bluete_breite': [1.58]})
for k in [1, 5, 15]:
    modell = KNeighborsClassifier(n_neighbors=k)
    modell.fit(X, y)
    print(k, modell.predict(neu)[0])""")
t('''Gib für die Blüte (4.87 | 1.58) die Arten ihrer 5 nächsten Nachbarn und die Abstände (3 Nachkommastellen) aus.''', KNN_IRIS,
  """modell = KNeighborsClassifier(n_neighbors=5)
modell.fit(X, y)
neu = pd.DataFrame({'bluete_laenge': [4.87], 'bluete_breite': [1.58]})
abstaende, zeilen = modell.kneighbors(neu)
print(y.iloc[zeilen[0]].tolist())
print(abstaende.round(3))""")
t('Gib die Genauigkeit des Obst-Modells (`k = 3`) auf den eigenen Trainingsdaten aus (3 Nachkommastellen).', OBST + '\nfrom sklearn.neighbors import KNeighborsClassifier',
  """X = obst[['gewicht', 'verhaeltnis']]
y = obst['sorte']
modell = KNeighborsClassifier(n_neighbors=3)
modell.fit(X, y)
print(f'{modell.score(X, y):.3f}')""")
t('''Trainiere ein k-NN-Modell (`k = 5`) auf allen vier Iris-Maßen und sage die Art einer Blüte mit den Maßen 6.1, 2.8, 4.7, 1.2 voraus
(in der Reihenfolge der Spalten). Gib auch die Klassen des Modells aus.''', IRIS + '\nfrom sklearn.neighbors import KNeighborsClassifier',
  """spalten = ['kelch_laenge', 'kelch_breite', 'bluete_laenge', 'bluete_breite']
X = iris[spalten]
y = iris['art']
modell = KNeighborsClassifier(n_neighbors=5)
modell.fit(X, y)
neu = pd.DataFrame([[6.1, 2.8, 4.7, 1.2]], columns=spalten)
print(modell.predict(neu))
print(modell.classes_)""")
t('''Gib für die Iris-Daten (Blütenblattlänge und -breite) die Genauigkeit auf den Trainingsdaten für `k` = 1, 3, 5, 10, 25, 50 und 100 aus
(3 Nachkommastellen). Mit `k = 1` ist jede Blüte ihr eigener nächster Nachbar.''', KNN_IRIS,
  """for k in [1, 3, 5, 10, 25, 50, 100]:
    modell = KNeighborsClassifier(n_neighbors=k)
    modell.fit(X, y)
    print(f'{k} {modell.score(X, y):.3f}')""")
predict("""import pandas as pd
from sklearn.neighbors import KNeighborsClassifier

X = pd.DataFrame({'x': [1, 2, 3, 10, 11, 12]})
y = pd.Series(['A', 'A', 'A', 'B', 'B', 'B'])
modell = KNeighborsClassifier(n_neighbors=3)
modell.fit(X, y)
print(modell.predict(pd.DataFrame({'x': [0, 4, 9, 20]})))""", erklaerung='''Die nächsten 3 Nachbarn:
- von 0 und von 4 sind 1, 2, 3, alle `A`,
- von 9 sind 10, 11, 12, alle `B` (die 3 ist weiter weg als die 12),
- von 20 sind 10, 11, 12, alle `B`.

Ausgabe: `['A' 'A' 'B' 'B']`.''')
predict("""import pandas as pd
from sklearn.neighbors import KNeighborsClassifier

X = pd.DataFrame({'x': [1, 2, 3, 4, 5]})
y = pd.Series(['A', 'B', 'B', 'A', 'A'])
modell = KNeighborsClassifier(n_neighbors=5)
modell.fit(X, y)
print(modell.predict(pd.DataFrame({'x': [2]})))""", erklaerung='''Mit `k = 5` sind **alle** fünf Beispiele Nachbarn, egal wie weit weg. Dreimal `A` und zweimal `B`: Die Mehrheit ist `A`,
obwohl die beiden nächsten Nachbarn (bei 2 und 3) `B` sind. Ausgabe: `['A']`.''')

# ---------------------------------------------------------------- 4
sec('Trainings- und Testdaten')
expl('''#### Auf neuen Daten prüfen

Die Genauigkeit auf den Trainingsdaten sagt wenig: Mit `k = 1` ist sie immer 1, weil jede Blüte sich selbst als nächsten Nachbarn findet.
Ein Modell soll aber **neue** Daten richtig einordnen. Deshalb hält man einen Teil der Beispiele zurück:

`X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=0)`

- Mit `X_train`, `y_train` (**Trainingsdaten**, hier 75 %) wird trainiert.
- Mit `X_test`, `y_test` (**Testdaten**, hier 25 %) wird geprüft. Das Modell hat sie nie gesehen.
- Die Aufteilung ist zufällig. `random_state` legt den Zufall fest, sodass bei jedem Lauf dieselbe Aufteilung herauskommt.''',
     SPLIT_IRIS + """

print(X_train.shape, X_test.shape)
modell = KNeighborsClassifier(n_neighbors=1)
modell.fit(X_train, y_train)
print(f'Training: {modell.score(X_train, y_train):.3f}')
print(f'Test:     {modell.score(X_test, y_test):.3f}')""")
expl('''#### Gleich viele von jeder Klasse: `stratify`

Bei einer zufälligen Aufteilung kann eine Klasse in den Testdaten zu häufig oder zu selten vorkommen. Mit `stratify=y` wird so aufgeteilt,
dass die Anteile der Klassen in beiden Teilen gleich sind wie in `y`.''',
     """import pandas as pd
from sklearn.model_selection import train_test_split

iris = pd.read_csv('iris.csv')
X = iris[['bluete_laenge', 'bluete_breite']]
y = iris['art']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=1)
print(y_test.value_counts().sort_index())
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=1, stratify=y)
print(y_test.value_counts().sort_index())""")

t('Teile die Obst-Daten mit `test_size=0.25` und `random_state=0` auf und gib die Formen der vier Teile aus.', OBST + '\nfrom sklearn.model_selection import train_test_split',
  """X = obst[['gewicht', 'verhaeltnis']]
y = obst['sorte']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=0)
print(X_train.shape, X_test.shape, y_train.shape, y_test.shape)""")
t('Gib für die Iris-Aufteilung aus dem Beispiel die Genauigkeit auf Trainings- und Testdaten für `k = 5` aus (3 Nachkommastellen).', SPLIT_IRIS,
  """modell = KNeighborsClassifier(n_neighbors=5)
modell.fit(X_train, y_train)
print(f'{modell.score(X_train, y_train):.3f} {modell.score(X_test, y_test):.3f}')""")
t('''In der Zelle werden 40 % der Iris-Blüten als Testdaten zurückgehalten. Gib die Test-Genauigkeit für `k` von 1 bis 15 aus (3 Nachkommastellen).''', SPLIT_40,
  """for k in range(1, 16):
    modell = KNeighborsClassifier(n_neighbors=k)
    modell.fit(X_train, y_train)
    print(f'{k} {modell.score(X_test, y_test):.3f}')""")
t('''Die Genauigkeit hängt auch von der zufälligen Aufteilung ab. Teile die Iris-Daten mit `random_state` = 0 bis 4 auf (`test_size=0.25`)
und gib jeweils die Test-Genauigkeit für `k = 5` aus (3 Nachkommastellen).''',
  IRIS + '\nfrom sklearn.model_selection import train_test_split\nfrom sklearn.neighbors import KNeighborsClassifier',
  """X = iris[['kelch_laenge', 'kelch_breite', 'bluete_laenge', 'bluete_breite']]
y = iris['art']
for zufall in range(5):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=zufall)
    modell = KNeighborsClassifier(n_neighbors=5)
    modell.fit(X_train, y_train)
    print(f'{zufall} {modell.score(X_test, y_test):.3f}')""")
t('''Teile die Iris-Daten mit `test_size=0.3`, `random_state=2` und `stratify=y` auf und gib die Anzahl jeder Art in den Trainings- und in den Testdaten aus.''',
  IRIS + '\nfrom sklearn.model_selection import train_test_split',
  """X = iris[['bluete_laenge', 'bluete_breite']]
y = iris['art']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=2, stratify=y)
print(y_train.value_counts().sort_index())
print(y_test.value_counts().sort_index())""")
t('''Zeichne für die Aufteilung in der Zelle (40 % Testdaten) die Genauigkeit auf Trainings- und Testdaten für `k` von 1 bis 40 als zwei Linien mit Legende
(`Training`, `Test`) und der x-Achsen-Beschriftung `k`.''', SPLIT_40 + '\nimport matplotlib.pyplot as plt',
  """werte_k = range(1, 41)
training = []
test = []
for k in werte_k:
    modell = KNeighborsClassifier(n_neighbors=k)
    modell.fit(X_train, y_train)
    training.append(modell.score(X_train, y_train))
    test.append(modell.score(X_test, y_test))
plt.plot(werte_k, training, label='Training')
plt.plot(werte_k, test, label='Test')
plt.xlabel('k')
plt.legend()
plt.show()""")
predict("""import pandas as pd
from sklearn.model_selection import train_test_split

X = pd.DataFrame({'x': range(20)})
y = pd.Series(['A'] * 10 + ['B'] * 10)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0, stratify=y)
print(len(X_train), len(X_test))
print(y_test.value_counts()['A'])""", erklaerung='''- 20 % von 20 Zeilen sind 4 Testzeilen, 16 bleiben fürs Training: `16 4`.
- Mit `stratify=y` sind die Anteile in den Testdaten wie in `y`, also halb `A`, halb `B`: `2`.''')

# ---------------------------------------------------------------- 5
sec('Genauigkeit und Konfusionsmatrix')
expl('''#### Wo irrt sich das Modell?

Die Genauigkeit ist eine einzige Zahl. Genauer hinschauen kann man mit den Vorhersagen für die Testdaten:

- `accuracy_score(y_test, vorhersage)` aus `sklearn.metrics` berechnet die Genauigkeit wie `score()`.
- `confusion_matrix(y_test, vorhersage)` ist die **Konfusionsmatrix** (*Verwechslungsmatrix*): Zeile = richtige Klasse, Spalte = vorhergesagte Klasse.
  Auf der Diagonalen stehen die richtigen Vorhersagen, daneben die Verwechslungen. Die Klassen sind alphabetisch sortiert.

Mit einem DataFrame bekommt die Matrix lesbare Beschriftungen.''',
     SPLIT_IRIS + """
from sklearn.metrics import accuracy_score, confusion_matrix

modell = KNeighborsClassifier(n_neighbors=5)
modell.fit(X_train, y_train)
vorhersage = modell.predict(X_test)
print(f'{accuracy_score(y_test, vorhersage):.3f}')
matrix = confusion_matrix(y_test, vorhersage)
print(matrix)
pd.DataFrame(matrix, index=modell.classes_, columns=modell.classes_)""")
expl('''#### Die Fehler anzeigen und zeichnen

- `X_test[vorhersage != y_test]` wählt die Zeilen aus, die falsch eingeordnet wurden.
- `ConfusionMatrixDisplay.from_predictions(y_test, vorhersage)` zeichnet die Konfusionsmatrix als farbiges Diagramm.''',
     SPLIT_IRIS + """
from sklearn.metrics import ConfusionMatrixDisplay
import matplotlib.pyplot as plt

modell = KNeighborsClassifier(n_neighbors=5)
modell.fit(X_train, y_train)
vorhersage = modell.predict(X_test)
falsch = X_test[vorhersage != y_test]
print(len(falsch))
ConfusionMatrixDisplay.from_predictions(y_test, vorhersage)
plt.show()""")

t('''Trainiere ein k-NN-Modell (`k = 3`) auf den Obst-Trainingsdaten und gib die Vorhersagen für die Testdaten, die richtigen Sorten (`y_test.to_numpy()`)
und die Genauigkeit mit `accuracy_score()` aus (3 Nachkommastellen).''', SPLIT_OBST + '\nfrom sklearn.metrics import accuracy_score',
  """modell = KNeighborsClassifier(n_neighbors=3)
modell.fit(X_train, y_train)
vorhersage = modell.predict(X_test)
print(vorhersage)
print(y_test.to_numpy())
print(f'{accuracy_score(y_test, vorhersage):.3f}')""")
t('Gib für dasselbe Obst-Modell die Konfusionsmatrix als beschrifteten DataFrame aus.', SPLIT_OBST + '\nfrom sklearn.metrics import confusion_matrix',
  """modell = KNeighborsClassifier(n_neighbors=3)
modell.fit(X_train, y_train)
vorhersage = modell.predict(X_test)
pd.DataFrame(confusion_matrix(y_test, vorhersage), index=modell.classes_, columns=modell.classes_)""")
t('''Zeige für dasselbe Obst-Modell die falsch eingeordneten Früchte an, mit einer zusätzlichen Spalte `vorhersage`. Benutze dazu
`falsch = X_test[vorhersage != y_test].copy()` und `falsch['vorhersage'] = vorhersage[vorhersage != y_test]`.''', SPLIT_OBST,
  """modell = KNeighborsClassifier(n_neighbors=3)
modell.fit(X_train, y_train)
vorhersage = modell.predict(X_test)
falsch = X_test[vorhersage != y_test].copy()
falsch['vorhersage'] = vorhersage[vorhersage != y_test]
falsch""")
t('''Berechne die Genauigkeit des Iris-Modells (`k = 5`, alle vier Maße) ohne `score()` und ohne `accuracy_score()`: als Mittelwert von
`vorhersage == y_test` (`True` zählt als 1). Gib sie mit 3 Nachkommastellen aus.''', SPLIT_IRIS,
  """modell = KNeighborsClassifier(n_neighbors=5)
modell.fit(X_train, y_train)
vorhersage = modell.predict(X_test)
print(f'{(vorhersage == y_test).mean():.3f}')""")
t('''Zeichne die Konfusionsmatrix für das Iris-Modell mit `k = 1` (alle vier Maße) mit `ConfusionMatrixDisplay.from_predictions()`.''',
  SPLIT_IRIS + '\nfrom sklearn.metrics import ConfusionMatrixDisplay\nimport matplotlib.pyplot as plt',
  """modell = KNeighborsClassifier(n_neighbors=1)
modell.fit(X_train, y_train)
ConfusionMatrixDisplay.from_predictions(y_test, modell.predict(X_test))
plt.show()""")
t('''Eine Klasse für sich: Wie viele der Testblüten jeder Art wurden richtig erkannt? Gib für jede Art die Anzahl in den Testdaten und die Anzahl
der Treffer aus (Iris, `k = 5`, alle vier Maße). Die Treffer stehen auf der Diagonalen der Konfusionsmatrix (`matrix[i, i]`), die Anzahl ist die Zeilensumme.''',
  SPLIT_IRIS + '\nfrom sklearn.metrics import confusion_matrix',
  """modell = KNeighborsClassifier(n_neighbors=5)
modell.fit(X_train, y_train)
matrix = confusion_matrix(y_test, modell.predict(X_test))
for i, art in enumerate(modell.classes_):
    print(art, matrix[i].sum(), matrix[i, i])""")
predict("""from sklearn.metrics import accuracy_score, confusion_matrix

richtig = ['ja', 'ja', 'nein', 'nein', 'ja']
vorhersage = ['ja', 'nein', 'nein', 'ja', 'ja']
print(accuracy_score(richtig, vorhersage))
print(confusion_matrix(richtig, vorhersage))""", erklaerung='''- Richtig sind die Positionen 1, 3 und 5, also 3 von 5: `0.6`.
- Die Klassen sind alphabetisch sortiert: Zeile/Spalte 0 ist `ja`, 1 ist `nein`. Von den drei echten `ja` wurden 2 als `ja` und 1 als `nein` vorhergesagt,
  von den zwei echten `nein` 1 als `ja` und 1 als `nein`: `[[2 1]` und `[1 1]]`.''')

# ---------------------------------------------------------------- 6
sec('Skalieren und Pipelines')
expl('''#### Warum skalieren?

k-NN vergleicht Abstände. Beim Obst liegt das Gewicht zwischen etwa 110 und 230 g, das Verhältnis nur zwischen 0.9 und 1.3.
Ein Unterschied von 10 g zählt für den Abstand also viel mehr als der ganze Unterschied in der Form, obwohl gerade die Form Äpfel und Birnen trennt.

Der `StandardScaler` rechnet jedes Merkmal so um, dass es den Mittelwert 0 und die Standardabweichung 1 hat (`(x - Mittelwert) / Standardabweichung`).
Danach zählen alle Merkmale gleich viel.

- `scaler.fit(X_train)` merkt sich Mittelwerte und Standardabweichungen der **Trainingsdaten**,
- `scaler.transform(X)` rechnet damit um, `scaler.fit_transform(X_train)` macht beides auf einmal.

Wegen Rundungsfehlern kommt als Mittelwert nicht genau 0 heraus, sondern z. B. `1e-16`. Ob Zahlen fast gleich sind,
prüft `np.allclose(a, b)`.''',
     """import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler

obst = pd.read_csv('obst.csv')
X = obst[['gewicht', 'verhaeltnis']]
scaler = StandardScaler()
X_skaliert = scaler.fit_transform(X)
print(scaler.mean_.round(2))
print(X_skaliert[:3].round(2))
print(np.allclose(X_skaliert.mean(axis=0), 0), np.allclose(X_skaliert.std(axis=0), 1))""")
expl('''#### Pipelines

Skalieren und Modell gehören zusammen: Neue Daten müssen vor der Vorhersage genauso umgerechnet werden. Eine **Pipeline** verbindet beides zu einem Modell:
`make_pipeline(StandardScaler(), KNeighborsClassifier(n_neighbors=3))`. Bei `fit()` wird der Scaler mit den Trainingsdaten eingestellt,
bei `predict()` und `score()` werden die Daten automatisch umgerechnet.''',
     SPLIT_OBST + """
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

ohne = KNeighborsClassifier(n_neighbors=3)
ohne.fit(X_train, y_train)
mit = make_pipeline(StandardScaler(), KNeighborsClassifier(n_neighbors=3))
mit.fit(X_train, y_train)
print(f'ohne Skalieren: {ohne.score(X_test, y_test):.3f}')
print(f'mit Skalieren:  {mit.score(X_test, y_test):.3f}')""")

t('''Skaliere die vier Iris-Maße mit dem `StandardScaler`. Gib die Mittelwerte und Standardabweichungen vor dem Skalieren aus (2 Nachkommastellen)
und prüfe mit `np.allclose()`, dass sie danach 0 und 1 sind.''',
  IRIS + '\nimport numpy as np\nfrom sklearn.preprocessing import StandardScaler',
  """X = iris[['kelch_laenge', 'kelch_breite', 'bluete_laenge', 'bluete_breite']]
X_skaliert = StandardScaler().fit_transform(X)
print(X.mean().round(2).to_numpy(), X.std(ddof=0).round(2).to_numpy())
print(np.allclose(X_skaliert.mean(axis=0), 0), np.allclose(X_skaliert.std(axis=0), 1))""")
t('''Rechne das Gewicht 200 g mit den Werten des Scalers von Hand um: `(200 - mean_[0]) / scale_[0]` (`scale_` sind die Standardabweichungen).
Vergleiche mit `scaler.transform()` für die Frucht (200 | 1.0). Gib beides mit 3 Nachkommastellen aus.''', OBST + '\nfrom sklearn.preprocessing import StandardScaler',
  """X = obst[['gewicht', 'verhaeltnis']]
scaler = StandardScaler()
scaler.fit(X)
print(f'{(200 - scaler.mean_[0]) / scaler.scale_[0]:.3f}')
print(scaler.transform(pd.DataFrame({'gewicht': [200], 'verhaeltnis': [1.0]})).round(3))""")
t('''Vergleiche für die Obst-Daten die Test-Genauigkeit mit und ohne Skalieren für `k` = 1, 3, 5 und 7. Gib je Zeile `k` und beide Werte aus (3 Nachkommastellen).''',
  SPLIT_OBST + '\nfrom sklearn.pipeline import make_pipeline\nfrom sklearn.preprocessing import StandardScaler',
  """for k in [1, 3, 5, 7]:
    ohne = KNeighborsClassifier(n_neighbors=k)
    ohne.fit(X_train, y_train)
    mit = make_pipeline(StandardScaler(), KNeighborsClassifier(n_neighbors=k))
    mit.fit(X_train, y_train)
    print(f'{k} {ohne.score(X_test, y_test):.3f} {mit.score(X_test, y_test):.3f}')""")
t('''Sage mit dem Obst-Modell mit und ohne Skalieren (`k = 3`, trainiert auf allen Obst-Daten) die Sorte einer Frucht mit 165 g und dem Verhältnis 1.25 voraus.
Die Form spricht klar für eine Birne.''', OBST + '\nfrom sklearn.neighbors import KNeighborsClassifier\nfrom sklearn.pipeline import make_pipeline\nfrom sklearn.preprocessing import StandardScaler',
  """X = obst[['gewicht', 'verhaeltnis']]
y = obst['sorte']
neu = pd.DataFrame({'gewicht': [165], 'verhaeltnis': [1.25]})
ohne = KNeighborsClassifier(n_neighbors=3)
ohne.fit(X, y)
mit = make_pipeline(StandardScaler(), KNeighborsClassifier(n_neighbors=3))
mit.fit(X, y)
print(ohne.predict(neu), mit.predict(neu))""")
t('''Ein Fehler, der oft passiert: Der Scaler wird mit **allen** Daten eingestellt, bevor aufgeteilt wird. Dann „kennt“ das Modell schon etwas von den Testdaten.
Baue für die Iris-Daten (alle vier Maße) eine Pipeline aus `StandardScaler` und k-NN (`k = 5`), trainiere sie korrekt nur mit den Trainingsdaten
und gib die Test-Genauigkeit aus (3 Nachkommastellen).''', SPLIT_IRIS + '\nfrom sklearn.pipeline import make_pipeline\nfrom sklearn.preprocessing import StandardScaler',
  """modell = make_pipeline(StandardScaler(), KNeighborsClassifier(n_neighbors=5))
modell.fit(X_train, y_train)
print(f'{modell.score(X_test, y_test):.3f}')""")
t('''Zeichne die skalierten Obst-Daten als Streudiagramm (Äpfel rot, Birnen grün) mit gleichen Einheiten auf beiden Achsen (`plt.axis('equal')`).
Die skalierten Werte sind ein Array: Spalte 0 ist das Gewicht, Spalte 1 das Verhältnis.''',
  OBST + '\nfrom sklearn.preprocessing import StandardScaler\nimport matplotlib.pyplot as plt',
  """X_skaliert = StandardScaler().fit_transform(obst[['gewicht', 'verhaeltnis']])
for sorte, farbe in [('Apfel', 'red'), ('Birne', 'green')]:
    auswahl = (obst['sorte'] == sorte).to_numpy()
    plt.scatter(X_skaliert[auswahl, 0], X_skaliert[auswahl, 1], color=farbe, label=sorte)
plt.axis('equal')
plt.legend()
plt.show()""")
predict("""import numpy as np
from sklearn.preprocessing import StandardScaler

X = np.array([[1.0], [2.0], [3.0]])
print(StandardScaler().fit_transform(X).round(3).tolist())""", erklaerung='''Mittelwert 2, Standardabweichung `√((1 + 0 + 1) / 3) = √(2/3) ≈ 0.816`.
`(1 - 2) / 0.816 ≈ -1.225`, `(2 - 2) / 0.816 = 0`, `(3 - 2) / 0.816 ≈ 1.225`.
Ausgabe: `[[-1.225], [0.0], [1.225]]`.''')

# ---------------------------------------------------------------- 7
sec('Entscheidungsgrenzen zeichnen')
expl('''#### `DecisionBoundaryDisplay`

Bei zwei Merkmalen kann man zeichnen, welche Klasse das Modell an **jeder** Stelle der Ebene vorhersagen würde. Die Grenzen zwischen den Farbflächen heißen
**Entscheidungsgrenzen**. `DecisionBoundaryDisplay.from_estimator(modell, X, response_method='predict', alpha=0.3)` aus `sklearn.inspection` zeichnet die Flächen
(`alpha` macht sie durchscheinend). Die Punkte zeichnet man danach mit `plt.scatter()` darüber.''',
     KNN_IRIS + """
from sklearn.inspection import DecisionBoundaryDisplay
import matplotlib.pyplot as plt

modell = KNeighborsClassifier(n_neighbors=5)
modell.fit(X, y)
DecisionBoundaryDisplay.from_estimator(modell, X, response_method='predict', alpha=0.3)
for art in modell.classes_:
    teil = X[y == art]
    plt.scatter(teil['bluete_laenge'], teil['bluete_breite'], label=art, s=15)
plt.legend()
plt.show()""")

t('''Zeichne die Entscheidungsgrenzen des Iris-Modells (Blütenblattlänge und -breite) für `k = 1` mit den Punkten darüber wie im Beispiel.
Die Grenzen sind zackig, weil jeder einzelne Punkt zählt.''', KNN_IRIS + '\nfrom sklearn.inspection import DecisionBoundaryDisplay\nimport matplotlib.pyplot as plt',
  """modell = KNeighborsClassifier(n_neighbors=1)
modell.fit(X, y)
DecisionBoundaryDisplay.from_estimator(modell, X, response_method='predict', alpha=0.3)
for art in modell.classes_:
    teil = X[y == art]
    plt.scatter(teil['bluete_laenge'], teil['bluete_breite'], label=art, s=15)
plt.legend()
plt.show()""")
t('''Zeichne die Entscheidungsgrenzen des Obst-Modells (`k = 3`) **ohne** Skalieren mit den Früchten darüber (Äpfel rot, Birnen grün).
Die Grenzen verlaufen fast senkrecht: Das Modell entscheidet fast nur nach dem Gewicht.''',
  OBST + '\nfrom sklearn.neighbors import KNeighborsClassifier\nfrom sklearn.inspection import DecisionBoundaryDisplay\nimport matplotlib.pyplot as plt',
  """X = obst[['gewicht', 'verhaeltnis']]
y = obst['sorte']
modell = KNeighborsClassifier(n_neighbors=3)
modell.fit(X, y)
DecisionBoundaryDisplay.from_estimator(modell, X, response_method='predict', alpha=0.3)
for sorte, farbe in [('Apfel', 'red'), ('Birne', 'green')]:
    teil = X[y == sorte]
    plt.scatter(teil['gewicht'], teil['verhaeltnis'], color=farbe, label=sorte)
plt.legend()
plt.show()""")
t('''Zeichne dasselbe für die Pipeline **mit** `StandardScaler`. Jetzt verläuft die Grenze waagerecht zwischen den Formen.''',
  OBST + '''
from sklearn.neighbors import KNeighborsClassifier
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.inspection import DecisionBoundaryDisplay
import matplotlib.pyplot as plt''',
  """X = obst[['gewicht', 'verhaeltnis']]
y = obst['sorte']
modell = make_pipeline(StandardScaler(), KNeighborsClassifier(n_neighbors=3))
modell.fit(X, y)
DecisionBoundaryDisplay.from_estimator(modell, X, response_method='predict', alpha=0.3)
for sorte, farbe in [('Apfel', 'red'), ('Birne', 'green')]:
    teil = X[y == sorte]
    plt.scatter(teil['gewicht'], teil['verhaeltnis'], color=farbe, label=sorte)
plt.legend()
plt.show()""")
t('''Zeichne die Entscheidungsgrenzen für die Iris-Kelchblätter (`kelch_laenge` und `kelch_breite`) mit `k = 15` und die Blüten darüber.
Mit den Kelchblättern lassen sich *versicolor* und *virginica* schlecht trennen.''',
  IRIS + '\nfrom sklearn.neighbors import KNeighborsClassifier\nfrom sklearn.inspection import DecisionBoundaryDisplay\nimport matplotlib.pyplot as plt',
  """X = iris[['kelch_laenge', 'kelch_breite']]
y = iris['art']
modell = KNeighborsClassifier(n_neighbors=15)
modell.fit(X, y)
DecisionBoundaryDisplay.from_estimator(modell, X, response_method='predict', alpha=0.3)
for art in modell.classes_:
    teil = X[y == art]
    plt.scatter(teil['kelch_laenge'], teil['kelch_breite'], label=art, s=15)
plt.legend()
plt.show()""")

# ---------------------------------------------------------------- 8
sec('Gemischte Übungen')
WEIN = '''import pandas as pd
from sklearn.datasets import load_wine

wein = load_wine(as_frame=True).frame'''
t('''scikit-learn bringt weitere Datensätze mit, z. B. `load_wine`: 178 Weine aus drei Anbaugebieten (`target` 0, 1, 2) mit 13 chemischen Messwerten.
Gib die Form der Tabelle und die Anzahl der Weine je Gebiet aus und zeige die Spalten `alcohol`, `color_intensity` und `target` der ersten 3 Zeilen an.''', WEIN,
  """print(wein.shape)
print(wein['target'].value_counts().sort_index())
wein[['alcohol', 'color_intensity', 'target']].head(3)""")
t('''Teile die Wein-Daten (alle 13 Messwerte als `X`, `target` als `y`) mit `test_size=0.25`, `random_state=0` und `stratify=y` auf. Vergleiche die
Test-Genauigkeit von k-NN (`k = 5`) ohne und mit `StandardScaler` (3 Nachkommastellen). `wein.drop(columns='target')` sind alle Spalten außer `target`.''',
  WEIN + '''
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler''',
  """X = wein.drop(columns='target')
y = wein['target']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=0, stratify=y)
ohne = KNeighborsClassifier(n_neighbors=5)
ohne.fit(X_train, y_train)
mit = make_pipeline(StandardScaler(), KNeighborsClassifier(n_neighbors=5))
mit.fit(X_train, y_train)
print(f'{ohne.score(X_test, y_test):.3f} {mit.score(X_test, y_test):.3f}')""")
t('''Warum hilft das Skalieren beim Wein so viel? Zeige die Kennzahlen `mean`, `min` und `max` der Spalten `proline`, `magnesium` und `hue` an
(`describe().loc[['mean', 'min', 'max']]`, auf 2 Nachkommastellen gerundet).''', WEIN,
  """wein[['proline', 'magnesium', 'hue']].describe().loc[['mean', 'min', 'max']].round(2)""")
t('''Gib für die skalierte Wein-Pipeline die Konfusionsmatrix der Testdaten aus (Aufteilung wie oben).''',
  WEIN + '''
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import confusion_matrix''',
  """X = wein.drop(columns='target')
y = wein['target']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=0, stratify=y)
modell = make_pipeline(StandardScaler(), KNeighborsClassifier(n_neighbors=5))
modell.fit(X_train, y_train)
print(confusion_matrix(y_test, modell.predict(X_test)))""")
t('''Welche zwei Merkmale trennen die Weine gut? Trainiere für die Paare (`alcohol`, `proline`), (`flavanoids`, `color_intensity`) und (`ash`, `magnesium`)
jeweils eine skalierte k-NN-Pipeline (`k = 5`) auf den Trainingsdaten und gib das Paar und die Test-Genauigkeit aus (3 Nachkommastellen).''',
  WEIN + '''
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler''',
  """y = wein['target']
for paar in [['alcohol', 'proline'], ['flavanoids', 'color_intensity'], ['ash', 'magnesium']]:
    X = wein[paar]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=0, stratify=y)
    modell = make_pipeline(StandardScaler(), KNeighborsClassifier(n_neighbors=5))
    modell.fit(X_train, y_train)
    print(paar, f'{modell.score(X_test, y_test):.3f}')""")
t('''Zeichne die Entscheidungsgrenzen der skalierten Pipeline (`k = 5`) für die Wein-Merkmale `flavanoids` und `color_intensity`
(trainiert auf allen Weinen) mit den Weinen darüber, gefärbt nach `target` (`plt.scatter(..., c=y)`).''',
  WEIN + '''
from sklearn.neighbors import KNeighborsClassifier
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.inspection import DecisionBoundaryDisplay
import matplotlib.pyplot as plt''',
  """X = wein[['flavanoids', 'color_intensity']]
y = wein['target']
modell = make_pipeline(StandardScaler(), KNeighborsClassifier(n_neighbors=5))
modell.fit(X, y)
DecisionBoundaryDisplay.from_estimator(modell, X, response_method='predict', alpha=0.3)
plt.scatter(X['flavanoids'], X['color_intensity'], c=y, s=15)
plt.show()""")
t('''Erstelle selbst eine kleine Tabelle mit mindestens 12 Beispielen und zwei Merkmalen (z. B. Größe und Gewicht von Hunden und Katzen) und
trainiere ein k-NN-Modell. Sage einige neue Beispiele voraus und zeichne die Entscheidungsgrenzen.''', '',
  """import pandas as pd
from sklearn.neighbors import KNeighborsClassifier
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.inspection import DecisionBoundaryDisplay
import matplotlib.pyplot as plt

tiere = pd.DataFrame({
    'groesse': [25, 23, 30, 28, 24, 26, 45, 60, 50, 55, 40, 65],
    'gewicht': [4.0, 3.5, 5.0, 4.5, 3.8, 4.2, 12.0, 30.0, 20.0, 25.0, 10.0, 35.0],
    'tier': ['Katze'] * 6 + ['Hund'] * 6})
X = tiere[['groesse', 'gewicht']]
y = tiere['tier']
modell = make_pipeline(StandardScaler(), KNeighborsClassifier(n_neighbors=3))
modell.fit(X, y)
print(modell.predict(pd.DataFrame({'groesse': [27, 42], 'gewicht': [5.5, 9.0]})))
DecisionBoundaryDisplay.from_estimator(modell, X, response_method='predict', alpha=0.3)
plt.scatter(X['groesse'], X['gewicht'])
plt.show()""", kind='free')

generate('sklearn_grundlagen', 'scikit-learn 1: Grundlagen', INTRO, ausfuehren=pandasnb.ausfuehrung(), ausgabe_markdown=True)
