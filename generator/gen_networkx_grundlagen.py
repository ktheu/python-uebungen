# Erzeugt ../content/networkx_grundlagen.ipynb (siehe nbgen.py). Erstes Notebook der networkx-Reihe:
# networkx_grundlagen, networkx_suchen, networkx_gewichtet, networkx_probleme.
#
# JupyterLite: networkx 3.6.1 (lokal pip install networkx==3.6.1); Ausgaben sind gleich, weil networkx die Einfügereihenfolge behält.
# Begriffe wie im Unterricht (InfoKursN/graphen/graphen.ipynb): Knoten, Kanten, adjazent, Nachbarn, Grad, Eingangs-/Ausgangsgrad,
# Vorgänger/Nachfolger, gewichtet, Adjazenzmatrix, Adjazenzliste (dict von sets bzw. dict von dicts).
# Nur Benutzung von networkx, keine eigenen Implementierungen der Algorithmen. Zeichnungen immer mit festen Koordinaten (pos).
from nbgen import sec, expl, task, predict, generate


def t(text, given='', body='', kind='normal'):
    """Aufgabe, deren Lösung aus dem vorgegebenen Code plus body besteht."""
    task(text, given=given, solution=(given + '\n' + body) if given else body, kind=kind)


INTRO = '''**networkx** ist ein Python-Paket für **Graphen**: Knoten, die durch Kanten verbunden sind. Damit kann man Straßennetze, Freundschaften,
Liniennetze oder Abhängigkeiten darstellen und viele bekannte Algorithmen (Breitensuche, Dijkstra, Spannbäume, …) mit einem einzigen Aufruf benutzen.

Die Reihe hat vier Notebooks:

1. **Grundlagen**: Graphen erstellen, untersuchen und zeichnen (dieses Notebook)
2. Suchen: Wege, Zusammenhang, Breiten- und Tiefensuche, Abhängigkeiten
3. Gewichtete Graphen: kürzeste Wege (Dijkstra, Bellman-Ford), minimale Spannbäume
4. Probleme: Euler-Wege, Färbungen, Dominating Sets, Rundreisen, soziale Netze

Du solltest Listen, Dictionaries, Sets und die matplotlib-Grundlagen schon kennen.

Jeder Abschnitt beginnt mit kurzen Erklärungen und Beispielen. Führe die Beispiele aus und probiere sie ruhig ein wenig aus.
Danach folgen viele kleine Übungen. Wenn etwas vorgegeben ist, steht es schon in der Codezelle.'''

# ---------------------------------------------------------------- 1
sec('Graphen erstellen')
expl('''#### Knoten und Kanten

Man importiert networkx üblicherweise als `nx`. `nx.Graph()` erzeugt einen leeren **ungerichteten** Graphen.

| Aufruf | bewirkt |
|---|---|
| `G.add_node('a')` | Knoten `a` hinzufügen |
| `G.add_nodes_from(['b', 'c'])` | mehrere Knoten hinzufügen |
| `G.add_edge('a', 'b')` | Kante zwischen `a` und `b` (fehlende Knoten werden mit angelegt) |
| `G.add_edges_from([('a', 'c'), ('b', 'c')])` | mehrere Kanten |
| `G.remove_edge('a', 'b')`, `G.remove_node('c')` | entfernen (mit einem Knoten verschwinden auch seine Kanten) |

`G.nodes` und `G.edges` enthalten die Knoten und Kanten; mit `list()` sieht man sie als Liste. `G.number_of_nodes()` und `G.number_of_edges()` zählen sie.
Knoten können Zeichenketten, Zahlen oder Tupel sein. networkx behält die Reihenfolge, in der sie hinzugefügt wurden.''',
     """import networkx as nx

G = nx.Graph()
G.add_node('a')
G.add_nodes_from(['b', 'c'])
G.add_edge('a', 'b')
G.add_edges_from([('a', 'c'), ('b', 'c'), ('c', 'd')])
print(list(G.nodes))
print(list(G.edges))
print(G.number_of_nodes(), G.number_of_edges())
G.remove_node('c')
print(list(G.edges))""")
expl('''#### Kurz: Graph aus einer Kantenliste

`nx.Graph(kantenliste)` erzeugt einen Graphen direkt aus einer Liste von Kanten.''',
     """import networkx as nx

G = nx.Graph([('Ulm', 'Stuttgart'), ('Stuttgart', 'Karlsruhe'), ('Ulm', 'München')])
print(list(G.nodes))""")

t('Erzeuge einen leeren Graphen, füge die Kanten a–b, b–c, c–a und c–d einzeln mit `add_edge` hinzu und gib Knoten und Kanten als Listen aus.',
  body="""import networkx as nx

G = nx.Graph()
G.add_edge('a', 'b')
G.add_edge('b', 'c')
G.add_edge('c', 'a')
G.add_edge('c', 'd')
print(list(G.nodes))
print(list(G.edges))""")
t('Erzeuge den Graphen aus der Kantenliste `kanten` und gib die Anzahl der Knoten und Kanten aus.',
  "import networkx as nx\n\nkanten = [(1, 2), (1, 3), (2, 4), (3, 4), (4, 5), (5, 6), (4, 6)]",
  """G = nx.Graph(kanten)
print(G.number_of_nodes(), G.number_of_edges())""")
t('''Füge zum Graphen `G` den Knoten `e` ohne Kanten hinzu, entferne dann die Kante a–b und den Knoten `c`. Gib danach Knoten und Kanten aus.''',
  "import networkx as nx\n\nG = nx.Graph([('a', 'b'), ('b', 'c'), ('c', 'a'), ('c', 'd'), ('b', 'd')])",
  """G.add_node('e')
G.remove_edge('a', 'b')
G.remove_node('c')
print(list(G.nodes))
print(list(G.edges))""")
t('''Ein **vollständiger** Graph mit n Knoten hat zwischen je zwei Knoten eine Kante. Baue ihn für n = 5 mit zwei Schleifen (Knoten 1 bis 5, Kante von i nach j für i < j) und gib die
Anzahl der Kanten aus. Vergleiche mit der Formel n·(n−1)/2 und mit `nx.complete_graph(5)`.''',
  "import networkx as nx",
  """G = nx.Graph()
for i in range(1, 6):
    for j in range(i + 1, 6):
        G.add_edge(i, j)
print(G.number_of_edges())
print(5 * 4 // 2)
print(nx.complete_graph(5).number_of_edges())""")
expl('''#### Fertige Graphen

networkx kann viele bekannte Graphen erzeugen, z. B. `nx.complete_graph(n)` (vollständig, Knoten 0 bis n−1), `nx.path_graph(n)` (eine Kette), `nx.cycle_graph(n)` (ein Kreis)
und `nx.grid_2d_graph(m, n)` (ein Gitter, Knoten sind Tupel `(zeile, spalte)`).''',
     """import networkx as nx

print(list(nx.path_graph(4).edges))
print(list(nx.cycle_graph(4).edges))
print(nx.grid_2d_graph(2, 3).number_of_edges())""")
t('Gib die Anzahl der Knoten und Kanten von `nx.cycle_graph(6)`, `nx.path_graph(6)` und `nx.grid_2d_graph(3, 4)` aus, jeweils in einer Zeile.',
  "import networkx as nx",
  """for G in [nx.cycle_graph(6), nx.path_graph(6), nx.grid_2d_graph(3, 4)]:
    print(G.number_of_nodes(), G.number_of_edges())""")
predict("""import networkx as nx

G = nx.Graph()
G.add_edge(1, 2)
G.add_edge(2, 1)
G.add_edge(2, 3)
G.add_node(1)
print(G.number_of_nodes(), G.number_of_edges())""")

# ---------------------------------------------------------------- 2
sec('Nachbarn und Grad')
expl('''#### Nachbarn

Zwei Knoten sind **adjazent** (benachbart), wenn eine Kante sie verbindet.

| Aufruf | Ergebnis |
|---|---|
| `list(G.neighbors(v))` oder `list(G[v])` | die Nachbarn von v |
| `G.degree(v)` | der **Grad** von v: die Anzahl seiner Kanten |
| `dict(G.degree)` | Dictionary Knoten → Grad |
| `G.has_edge(u, v)` | gibt es eine Kante zwischen u und v? |
| `v in G` | gibt es den Knoten v? |''',
     """import networkx as nx

G = nx.Graph([('a', 'b'), ('a', 'c'), ('a', 'd'), ('b', 'c')])
print(list(G.neighbors('a')))
print(G.degree('a'), G.degree('d'))
print(dict(G.degree))
print(G.has_edge('b', 'c'), G.has_edge('b', 'd'), 'e' in G)""")
expl('''#### Der Handschlag-Satz

Jede Kante hat zwei Enden. Deshalb ist die **Summe aller Grade doppelt so groß wie die Anzahl der Kanten**, und die Anzahl der Knoten mit ungeradem Grad ist immer gerade.''',
     """import networkx as nx

G = nx.Graph([(1, 2), (1, 3), (2, 3), (3, 4), (4, 5)])
summe = 0
for v in G.nodes:
    summe += G.degree(v)
print(summe, 2 * G.number_of_edges())""")

FREUNDE = ("import networkx as nx\n\nG = nx.Graph([('Ali', 'Bea'), ('Ali', 'Cem'), ('Bea', 'Cem'), ('Bea', 'Dana'), ('Cem', 'Emil'), ('Dana', 'Emil'),\n"
           "              ('Emil', 'Fiona'), ('Bea', 'Emil')])")
t('Gib die Freunde (Nachbarn) von Bea und von Fiona als Listen aus.', FREUNDE,
  """print(list(G.neighbors('Bea')))
print(list(G.neighbors('Fiona')))""")
t('Gib für jede Person die Anzahl ihrer Freunde (den Grad) aus, in der Form `Ali 2`.', FREUNDE,
  """for v in G.nodes:
    print(v, G.degree(v))""")
t('Gib die Person mit den meisten Freunden aus (mit `max()` und `key=`).', FREUNDE,
  "print(max(G.nodes, key=lambda v: G.degree(v)))")
t('Prüfe, ob Ali und Dana befreundet sind und ob Bea und Emil befreundet sind. Gib außerdem aus, ob es die Person `Gus` gibt.', FREUNDE,
  """print(G.has_edge('Ali', 'Dana'), G.has_edge('Bea', 'Emil'))
print('Gus' in G)""")
t('''Gib die gemeinsamen Freunde von Ali und Dana als sortierte Liste aus (Schnittmenge der Nachbarn, mit `set()`).''', FREUNDE,
  "print(sorted(set(G.neighbors('Ali')) & set(G.neighbors('Dana'))))")
t('''Prüfe den Handschlag-Satz für den Freundesgraphen: Gib die Summe aller Grade und die doppelte Anzahl der Kanten aus, dann die Namen der Personen mit ungeradem Grad.''', FREUNDE,
  """summe = 0
ungerade = []
for v in G.nodes:
    summe += G.degree(v)
    if G.degree(v) % 2 == 1:
        ungerade.append(v)
print(summe, 2 * G.number_of_edges())
print(ungerade)""")
t('''Gib alle Personen aus, die mit **allen** Freunden von Ali befreundet sind (außer Ali selbst und außer den Freunden selbst).''', FREUNDE,
  """freunde = list(G.neighbors('Ali'))
for v in G.nodes:
    if v != 'Ali' and v not in freunde:
        alle = True
        for f in freunde:
            if not G.has_edge(v, f):
                alle = False
        if alle:
            print(v)""")
predict("""import networkx as nx

G = nx.Graph([(1, 2), (2, 3), (3, 1), (3, 4)])
print(list(G.neighbors(3)))
print(dict(G.degree))
print(G.has_edge(4, 3), G.has_edge(1, 4))""")

# ---------------------------------------------------------------- 3
sec('Gerichtete Graphen')
expl('''#### `DiGraph`

In einem **gerichteten** Graphen (`nx.DiGraph()`) hat jede Kante eine Richtung: `add_edge('a', 'b')` ist eine Kante **von** a **nach** b.

| Aufruf | Ergebnis |
|---|---|
| `list(G.successors(v))` | **Nachfolger**: Knoten, zu denen eine Kante von v führt |
| `list(G.predecessors(v))` | **Vorgänger**: Knoten, von denen eine Kante zu v führt |
| `G.out_degree(v)` | **Ausgangsgrad** (Anzahl der ausgehenden Kanten) |
| `G.in_degree(v)` | **Eingangsgrad** (Anzahl der eingehenden Kanten) |

`G.has_edge('a', 'b')` und `G.has_edge('b', 'a')` sind hier verschieden.''',
     """import networkx as nx

G = nx.DiGraph([('a', 'b'), ('a', 'c'), ('a', 'd'), ('c', 'b'), ('d', 'a')])
print(list(G.successors('a')), list(G.predecessors('a')))
print(G.out_degree('a'), G.in_degree('a'))
print(G.has_edge('a', 'd'), G.has_edge('d', 'a'), G.has_edge('b', 'a'))""")

WEB = "import networkx as nx\n\nW = nx.DiGraph([('Start', 'News'), ('Start', 'Sport'), ('News', 'Sport'), ('Sport', 'Start'), ('News', 'Wetter'), ('Wetter', 'News'), ('Sport', 'Fußball')])"
t('Webseiten verlinken aufeinander (`W`). Gib die Seiten aus, auf die `News` verlinkt, und die Seiten, die auf `Sport` verlinken.', WEB,
  """print(list(W.successors('News')))
print(list(W.predecessors('Sport')))""")
t('Gib für jede Seite den Eingangsgrad (wie oft sie verlinkt wird) und den Ausgangsgrad aus, in der Form `Start 1 2`.', WEB,
  """for v in W.nodes:
    print(v, W.in_degree(v), W.out_degree(v))""")
t('Gib alle Seiten aus, die **keine** Links nach außen haben (Ausgangsgrad 0), und alle Paare von Seiten, die sich gegenseitig verlinken (jedes Paar nur einmal).', WEB,
  """for v in W.nodes:
    if W.out_degree(v) == 0:
        print(v)
for u, v in W.edges:
    if W.has_edge(v, u) and u < v:
        print(u, v)""")
t('''Auf Instagram folgt man Personen (gerichtet). Gib für jede Person in `F` aus, wie viele **Follower** sie hat, sortiert nach Followern (die meisten zuerst).''',
  "import networkx as nx\n\nF = nx.DiGraph([('Ali', 'Mia'), ('Bea', 'Mia'), ('Cem', 'Mia'), ('Mia', 'Ali'), ('Bea', 'Ali'), ('Dana', 'Cem'), ('Ali', 'Bea')])",
  """for v in sorted(F.nodes, key=lambda v: F.in_degree(v), reverse=True):
    print(v, F.in_degree(v))""")
t('''`G.to_undirected()` macht aus einem gerichteten Graphen einen ungerichteten (gegenseitige Kanten werden zu einer). Gib für `W` die Anzahl der Kanten vorher und nachher aus.''', WEB,
  """U = W.to_undirected()
print(W.number_of_edges(), U.number_of_edges())""")
predict("""import networkx as nx

G = nx.DiGraph([(1, 2), (2, 3), (3, 1), (1, 3)])
print(list(G.successors(1)), list(G.predecessors(1)))
print(G.in_degree(3), G.out_degree(3))
print(G.number_of_edges())""")

# ---------------------------------------------------------------- 4
sec('Gewichte und Attribute')
expl('''#### Gewichtete Kanten

Kanten können **Attribute** haben, meistens ein Gewicht (Entfernung, Kosten, Zeit): `G.add_edge('a', 'b', weight=8)`.

- `G['a']['b']['weight']` liest das Gewicht der Kante von a nach b.
- `G.edges(data='weight')` liefert die Kanten als Tripel `(u, v, gewicht)`.
- `G.size(weight='weight')` ist die Summe aller Gewichte.
- Auch Knoten können Attribute haben: `G.add_node('Ulm', einwohner=128928)`, gelesen mit `G.nodes['Ulm']['einwohner']`.''',
     """import networkx as nx

G = nx.Graph()
G.add_edge('a', 'b', weight=8)
G.add_edge('a', 'c', weight=2)
G.add_edge('c', 'b', weight=1)
print(G['a']['b']['weight'])
print(list(G.edges(data='weight')))
print(G.size(weight='weight'))
G.add_node('a', name='Start')
print(G.nodes['a']['name'])""")
expl('''`G.add_weighted_edges_from([(u, v, w), ...])` fügt viele gewichtete Kanten auf einmal hinzu.''',
     """import networkx as nx

G = nx.Graph()
G.add_weighted_edges_from([('a', 'b', 8), ('a', 'c', 2)])
print(list(G.edges(data='weight')))""")

STRASSEN = ("import networkx as nx\n\nS = nx.Graph()\nS.add_weighted_edges_from([('Stuttgart', 'Karlsruhe', 80), ('Stuttgart', 'Ulm', 95), ('Stuttgart', 'Heilbronn', 55),\n"
            "                          ('Karlsruhe', 'Heilbronn', 75), ('Karlsruhe', 'Freiburg', 135), ('Ulm', 'Konstanz', 150), ('Freiburg', 'Konstanz', 140)])")
t('Gib die Entfernung von Stuttgart nach Ulm und von Freiburg nach Karlsruhe aus (in km).', STRASSEN,
  """print(S['Stuttgart']['Ulm']['weight'])
print(S['Freiburg']['Karlsruhe']['weight'])""")
t('Gib alle Straßen mit ihrer Länge aus, in der Form `Stuttgart - Karlsruhe: 80 km`, und danach die Gesamtlänge aller Straßen.', STRASSEN,
  """for u, v, w in S.edges(data='weight'):
    print(f'{u} - {v}: {w} km')
print(S.size(weight='weight'))""")
t('Gib die längste Straße aus (mit `max()` über `S.edges(data=\'weight\')` und `key=`).', STRASSEN,
  "print(max(S.edges(data='weight'), key=lambda e: e[2]))")
t('''Berechne die Länge der Route Freiburg → Karlsruhe → Stuttgart → Ulm, indem du die Gewichte der Kanten zwischen aufeinanderfolgenden Städten addierst. Gib sie aus.''', STRASSEN,
  """route = ['Freiburg', 'Karlsruhe', 'Stuttgart', 'Ulm']
laenge = 0
for i in range(len(route) - 1):
    laenge += S[route[i]][route[i + 1]]['weight']
print(laenge)""")
t('''Gib die Städte aus, die von Stuttgart aus über eine direkte Straße von höchstens 90 km erreichbar sind.''', STRASSEN,
  """for nachbar in S.neighbors('Stuttgart'):
    if S['Stuttgart'][nachbar]['weight'] <= 90:
        print(nachbar)""")
t('''Speichere bei jeder Stadt die Einwohnerzahl aus `einwohner` als Knotenattribut `einwohner`. Gib dann die Stadt mit den meisten Einwohnern aus.''',
  STRASSEN + "\neinwohner = {'Stuttgart': 632865, 'Karlsruhe': 308707, 'Ulm': 128928, 'Heilbronn': 127658, 'Freiburg': 237244, 'Konstanz': 86495}",
  """for stadt, n in einwohner.items():
    S.add_node(stadt, einwohner=n)
print(max(S.nodes, key=lambda v: S.nodes[v]['einwohner']))""")
predict("""import networkx as nx

G = nx.Graph()
G.add_weighted_edges_from([(1, 2, 5), (2, 3, 2), (1, 3, 9)])
G[1][2]['weight'] = 4
print(G[2][1]['weight'], G.size(weight='weight'))""")

# ---------------------------------------------------------------- 5
sec('Adjazenzliste und Adjazenzmatrix')
expl('''#### Von der eigenen Darstellung zu networkx und zurück

Im Unterricht wird ein ungerichteter Graph als **Adjazenzliste** gespeichert: ein Dictionary, das jedem Knoten die Menge seiner Nachbarn zuordnet.
`nx.Graph(d)` bzw. `nx.DiGraph(d)` macht daraus einen networkx-Graphen. `nx.to_dict_of_lists(G)` ist der Rückweg (mit Listen statt Mengen).''',
     """import networkx as nx

d = {'a': {'b', 'c'}, 'b': {'d'}, 'c': {'b', 'd'}, 'd': {'b'}}
G = nx.DiGraph(d)
print(G.number_of_edges(), G.has_edge('c', 'd'))
print(sorted(G.successors('c')))
print(nx.to_dict_of_lists(nx.DiGraph([('a', 'b'), ('a', 'c'), ('b', 'c')])))""")
expl('''#### Gewichtete Adjazenzlisten

Ein gewichteter Graph ist im Unterricht ein Dictionary von Dictionaries: `{'a': {'b': 8, 'c': 2}, ...}`. Daraus baut man den networkx-Graphen mit einer Schleife über die Einträge.''',
     """import networkx as nx

d = {'a': {'b': 8, 'c': 2}, 'b': {'d': 4}, 'c': {'b': 1, 'd': 6}, 'd': {'b': 2}}
G = nx.DiGraph()
for u in d:
    for v, w in d[u].items():
        G.add_edge(u, v, weight=w)
print(list(G.edges(data='weight')))""")
expl('''#### Adjazenzmatrix

`nx.to_numpy_array(G, nodelist=[...], weight='weight', nonedge=...)` erzeugt die **Adjazenzmatrix** als numpy-Array. Die Zeilen und Spalten stehen in der Reihenfolge von `nodelist`.
Ohne Gewichte stehen 1 und 0 darin (`weight=None`). Bei gewichteten Graphen setzt man `nonedge=float('inf')` für fehlende Kanten, wie im Unterricht.
`.tolist()` macht daraus eine Liste von Listen.''',
     """import networkx as nx

G = nx.DiGraph([('a', 'b'), ('a', 'c'), ('b', 'd'), ('c', 'b'), ('c', 'd'), ('d', 'b')])
print(nx.to_numpy_array(G, nodelist=['a', 'b', 'c', 'd'], weight=None).tolist())
H = nx.DiGraph()
H.add_weighted_edges_from([('a', 'b', 8), ('a', 'c', 2), ('b', 'd', 4)])
print(nx.to_numpy_array(H, nodelist=['a', 'b', 'c', 'd'], nonedge=float('inf')).tolist())""")

t('''Erzeuge aus der ungerichteten Adjazenzliste `d` einen `nx.Graph` und gib die Anzahl der Kanten und die Nachbarn von `x` sortiert aus.''',
  "import networkx as nx\n\nd = {'x': {'y', 'z'}, 'y': {'x', 'w'}, 'z': {'x', 'w'}, 'w': {'y', 'z', 'v'}, 'v': {'w'}}",
  """G = nx.Graph(d)
print(G.number_of_edges())
print(sorted(G.neighbors('x')))""")
t('''Erzeuge aus der gewichteten Adjazenzliste `d` einen `nx.DiGraph` mit dem Attribut `weight` und gib das Gewicht der Kante von `c` nach `d` und die Summe aller Gewichte aus.''',
  "import networkx as nx\n\nd = {'a': {'b': 8, 'c': 2}, 'b': {'d': 4}, 'c': {'b': 1, 'd': 6}, 'd': {'b': 2}}",
  """G = nx.DiGraph()
for u in d:
    for v, w in d[u].items():
        G.add_edge(u, v, weight=w)
print(G['c']['d']['weight'])
print(G.size(weight='weight'))""")
t('Gib die Adjazenzmatrix (0/1) des ungerichteten Graphen `G` mit der Knotenreihenfolge 1, 2, 3, 4 als Liste von Listen aus.',
  "import networkx as nx\n\nG = nx.Graph([(1, 2), (1, 3), (2, 3), (3, 4)])",
  "print(nx.to_numpy_array(G, nodelist=[1, 2, 3, 4], weight=None).tolist())")
t('''Gib die Adjazenzmatrix des gewichteten gerichteten Graphen `G` (Reihenfolge a, b, c, d) mit `inf` für fehlende Kanten aus. Setze danach die Diagonale auf 0, wie im Unterricht
(Zeile i, Spalte i), und gib die Matrix Zeile für Zeile aus.''',
  "import networkx as nx\n\nG = nx.DiGraph()\nG.add_weighted_edges_from([('a', 'b', 8), ('a', 'c', 2), ('b', 'd', 4), ('c', 'b', 1), ('c', 'd', 6), ('d', 'b', 2)])",
  """M = nx.to_numpy_array(G, nodelist=['a', 'b', 'c', 'd'], nonedge=float('inf')).tolist()
for i in range(4):
    M[i][i] = 0
for zeile in M:
    print(zeile)""")
t('Gib für den gerichteten Graphen `G` die Adjazenzliste mit `nx.to_dict_of_lists()` aus.',
  "import networkx as nx\n\nG = nx.DiGraph([('a', 'b'), ('a', 'c'), ('b', 'd'), ('c', 'b'), ('c', 'd'), ('d', 'b')])",
  "print(nx.to_dict_of_lists(G))")
predict("""import networkx as nx

G = nx.Graph({1: [2, 3], 2: [3]})
print(G.number_of_edges())
print(nx.to_numpy_array(G, nodelist=[1, 2, 3], weight=None).tolist())""")

# ---------------------------------------------------------------- 6
sec('Graphen zeichnen')
expl('''#### `nx.draw`

`nx.draw(G, pos, ax=ax, with_labels=True)` zeichnet einen Graphen mit matplotlib. `pos` ist ein Dictionary, das jedem Knoten seine Koordinaten `(x, y)` zuordnet.
Ohne `pos` wählt networkx die Lage zufällig; mit festen Koordinaten sieht die Zeichnung immer gleich aus.

Weitere Angaben: `node_color='lightblue'`, `node_size=600`, `edge_color='gray'`, `width=2` (Linienstärke), `arrows=True` bei gerichteten Graphen.
Kantengewichte beschriftet man mit `nx.draw_networkx_edge_labels(G, pos, edge_labels=..., ax=ax)`. `nx.get_edge_attributes(G, 'weight')` liefert dafür das Dictionary
Kante → Gewicht.''',
     """import matplotlib.pyplot as plt
import networkx as nx

G = nx.Graph()
G.add_weighted_edges_from([('a', 'b', 8), ('a', 'c', 2), ('c', 'b', 1), ('b', 'd', 4), ('c', 'd', 6)])
pos = {'a': (0, 1), 'b': (2, 2), 'c': (2, 0), 'd': (4, 1)}
fig, ax = plt.subplots(figsize=(4, 2.5))
nx.draw(G, pos, ax=ax, with_labels=True, node_color='lightblue', node_size=600)
nx.draw_networkx_edge_labels(G, pos, edge_labels=nx.get_edge_attributes(G, 'weight'), ax=ax)
plt.show()""")

t('''Zeichne den Freundesgraphen mit den Koordinaten aus `pos`, Beschriftung, Knotenfarbe `'lightgreen'` und Knotengröße 1200. Bildgröße 4 × 3.''',
  "import matplotlib.pyplot as plt\n" + FREUNDE + "\npos = {'Ali': (0, 1), 'Bea': (1, 2), 'Cem': (1, 0), 'Dana': (2.5, 2), 'Emil': (2.5, 0), 'Fiona': (3.5, 1)}",
  """fig, ax = plt.subplots(figsize=(4, 3))
nx.draw(G, pos, ax=ax, with_labels=True, node_color='lightgreen', node_size=1200)
plt.show()""")
t('''Zeichne das Straßennetz mit den Koordinaten aus `pos`, Beschriftung (Schriftgröße 8: `font_size=8`), Knotenfarbe `'orange'`, Knotengröße 300 und die Entfernungen an den Kanten.
Bildgröße 5 × 4.''',
  "import matplotlib.pyplot as plt\n" + STRASSEN + "\npos = {'Stuttgart': (4, 4), 'Karlsruhe': (1.5, 5), 'Ulm': (6.5, 2.5), 'Heilbronn': (4, 6), 'Freiburg': (0.5, 1.5), 'Konstanz': (4.5, 0)}",
  """fig, ax = plt.subplots(figsize=(5, 4))
nx.draw(S, pos, ax=ax, with_labels=True, font_size=8, node_color='orange', node_size=300)
nx.draw_networkx_edge_labels(S, pos, edge_labels=nx.get_edge_attributes(S, 'weight'), ax=ax, font_size=8)
plt.show()""")
t('''Zeichne den Web-Graphen `W` als gerichteten Graphen mit Pfeilen, Beschriftung, Knotenfarbe `'lightblue'`, Knotengröße 1500, Schriftgröße 8 und den Koordinaten aus `pos`.
Färbe dabei die Knoten nach Eingangsgrad: `node_color` darf auch eine Liste von Farben in der Reihenfolge von `W.nodes` sein; Seiten mit Eingangsgrad 2 oder mehr `'salmon'`, die anderen `'lightblue'`.
Bildgröße 4 × 3.''',
  "import matplotlib.pyplot as plt\n" + WEB + "\npos = {'Start': (0, 1), 'News': (2, 2), 'Sport': (2, 0), 'Wetter': (4, 2), 'Fußball': (4, 0)}",
  """farben = []
for v in W.nodes:
    if W.in_degree(v) >= 2:
        farben.append('salmon')
    else:
        farben.append('lightblue')
fig, ax = plt.subplots(figsize=(4, 3))
nx.draw(W, pos, ax=ax, with_labels=True, node_color=farben, node_size=1500, font_size=8, arrows=True)
plt.show()""")

# ---------------------------------------------------------------- 7
sec('Gemischte Übungen')
t('''Das Liniennetz einer kleinen Stadt: Jede Linie ist eine Liste von Haltestellen; aufeinanderfolgende Haltestellen sind verbunden. Baue den Graphen und gib die Anzahl der Haltestellen,
die Anzahl der Verbindungen und die **Umsteigehaltestellen** aus (Grad mindestens 3), sortiert.''',
  "import networkx as nx\n\nlinien = {'1': ['Bahnhof', 'Markt', 'Rathaus', 'Uni'], '2': ['Klinik', 'Markt', 'Schule', 'Stadion'], '3': ['Bahnhof', 'Schule', 'See']}",
  """G = nx.Graph()
for halte in linien.values():
    for i in range(len(halte) - 1):
        G.add_edge(halte[i], halte[i + 1])
print(G.number_of_nodes(), G.number_of_edges())
umsteigen = []
for v in G.nodes:
    if G.degree(v) >= 3:
        umsteigen.append(v)
print(sorted(umsteigen))""")
t('''Ein Wörter-Graph: Zwei Wörter aus `woerter` sind verbunden, wenn sie sich in **genau einem** Buchstaben an derselben Stelle unterscheiden (z. B. `Hand` und `Hund`). Baue den Graphen
mit zwei Schleifen über alle Paare und gib die Nachbarn von `Hand` und den Grad von `Wand` aus.''',
  "import networkx as nx\n\nwoerter = ['Hand', 'Hund', 'Wand', 'Rand', 'Rind', 'Wind', 'Bund', 'Band', 'Wild']",
  """def unterschiede(a, b):
    n = 0
    for x, y in zip(a, b):
        if x != y:
            n += 1
    return n

G = nx.Graph()
G.add_nodes_from(woerter)
for i in range(len(woerter)):
    for j in range(i + 1, len(woerter)):
        if unterschiede(woerter[i], woerter[j]) == 1:
            G.add_edge(woerter[i], woerter[j])
print(list(G.neighbors('Hand')))
print(G.degree('Wand'))""")
t('''Ein Turnier „jeder gegen jeden“: Die Ergebnisse stehen in `spiele` als (Sieger, Verlierer). Speichere sie als gerichteten Graphen (Kante vom Sieger zum Verlierer). Gib die Tabelle aus:
für jedes Team die Siege (Ausgangsgrad) und Niederlagen (Eingangsgrad), sortiert nach Siegen.''',
  "import networkx as nx\n\nspiele = [('Rot', 'Blau'), ('Grün', 'Rot'), ('Rot', 'Gelb'), ('Blau', 'Grün'), ('Gelb', 'Blau'), ('Grün', 'Gelb')]",
  """T = nx.DiGraph(spiele)
for team in sorted(T.nodes, key=lambda v: T.out_degree(v), reverse=True):
    print(team, T.out_degree(team), T.in_degree(team))""")
predict("""import networkx as nx

G = nx.Graph([('a', 'b'), ('b', 'c')])
G.add_edge('c', 'd', weight=5)
G.remove_node('b')
print(list(G.nodes), list(G.edges))
print(G.number_of_edges(), G.size(weight='weight'))""")

generate('networkx_grundlagen', 'networkx 1: Graphen erstellen, untersuchen und zeichnen', INTRO)
