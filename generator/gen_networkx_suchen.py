# Erzeugt ../content/networkx_suchen.ipynb (siehe nbgen.py). Zweites Notebook der networkx-Reihe.
# Reihenfolgen bei Breiten-/Tiefensuche hängen von der Reihenfolge der Kanten ab (networkx behält sie): gleich in JupyterLite.
# Mengen (connected_components, ancestors) immer sortiert ausgeben.
import networkx as nx

from nbgen import sec, expl, task, predict, generate


def t(text, given='', body='', kind='normal'):
    """Aufgabe, deren Lösung aus dem vorgegebenen Code plus body besteht."""
    task(text, given=given, solution=(given + '\n' + body) if given else body, kind=kind)


INTRO = '''In diesem Notebook geht es darum, in Graphen **Wege** zu finden: Ist ein Knoten von einem anderen aus erreichbar? Was ist der Weg mit den wenigsten Kanten?
In welcher Reihenfolge besuchen **Breitensuche** und **Tiefensuche** die Knoten? Und in welcher Reihenfolge erledigt man Aufgaben, die voneinander abhängen?

Die Reihe hat vier Notebooks:

1. Grundlagen: Graphen erstellen, untersuchen und zeichnen
2. **Suchen**: Wege, Zusammenhang, Breiten- und Tiefensuche, Abhängigkeiten (dieses Notebook)
3. Gewichtete Graphen: kürzeste Wege (Dijkstra, Bellman-Ford), minimale Spannbäume
4. Probleme: Euler-Wege, Färbungen, Dominating Sets, Rundreisen, soziale Netze

Jeder Abschnitt beginnt mit kurzen Erklärungen und Beispielen. Führe die Beispiele aus und probiere sie ruhig ein wenig aus.
Manche Beispiele enden absichtlich mit einer Fehlermeldung. Danach folgen viele kleine Übungen.
Wenn etwas vorgegeben ist, steht es schon in der Codezelle.'''

# ---------------------------------------------------------------- 1
sec('Wege und Zusammenhang')
expl('''#### Erreichbarkeit

Ein **Weg** ist eine Folge von Knoten, bei der aufeinanderfolgende Knoten durch Kanten verbunden sind.

| Aufruf | Ergebnis |
|---|---|
| `nx.has_path(G, u, v)` | gibt es einen Weg von u nach v? |
| `nx.is_connected(G)` | ist der (ungerichtete) Graph **zusammenhängend**, d. h. jeder Knoten von jedem erreichbar? |
| `nx.connected_components(G)` | die **Zusammenhangskomponenten**: Mengen von Knoten, die untereinander erreichbar sind |
| `nx.number_connected_components(G)` | ihre Anzahl |
| `nx.node_connected_component(G, v)` | die Komponente, in der v liegt |

Die Komponenten sind Mengen; zum Ausgeben sortiert man sie.''',
     """import networkx as nx

G = nx.Graph([(1, 2), (2, 3), (4, 5), (6, 6)])
print(nx.has_path(G, 1, 3), nx.has_path(G, 1, 5))
print(nx.is_connected(G), nx.number_connected_components(G))
for k in nx.connected_components(G):
    print(sorted(k))
print(sorted(nx.node_connected_component(G, 4)))""")
expl('''#### Gerichtete Graphen

In einem `DiGraph` beachtet `has_path` die Richtung. Ein gerichteter Graph ist **stark zusammenhängend** (`nx.is_strongly_connected`), wenn man von jedem Knoten zu jedem kommt.''',
     """import networkx as nx

D = nx.DiGraph([('a', 'b'), ('b', 'c'), ('c', 'a'), ('c', 'd')])
print(nx.has_path(D, 'a', 'd'), nx.has_path(D, 'd', 'a'))
print(nx.is_strongly_connected(D))""")

INSELN = "import networkx as nx\n\nB = nx.Graph([('A', 'B'), ('B', 'C'), ('D', 'E'), ('F', 'G'), ('G', 'H'), ('H', 'F'), ('C', 'A')])\nB.add_node('I')"
t('Auf einer Inselgruppe verbinden Brücken die Inseln (`B`). Gib aus, ob man von A nach C und von A nach F kommt, und ob das ganze Netz zusammenhängend ist.', INSELN,
  """print(nx.has_path(B, 'A', 'C'), nx.has_path(B, 'A', 'F'))
print(nx.is_connected(B))""")
t('Gib die Anzahl der Zusammenhangskomponenten aus und jede Komponente als sortierte Liste.', INSELN,
  """print(nx.number_connected_components(B))
for k in nx.connected_components(B):
    print(sorted(k))""")
t('''Wie viele Brücken muss man **mindestens** bauen, damit alle Inseln verbunden sind? (Anzahl der Komponenten minus 1.) Verbinde dann den ersten Knoten jeder Komponente (`sorted(k)[0]`)
mit dem der nächsten Komponente und prüfe, ob das Netz jetzt zusammenhängt.''', INSELN,
  """komponenten = []
for k in nx.connected_components(B):
    komponenten.append(sorted(k)[0])
print(len(komponenten) - 1)
for i in range(len(komponenten) - 1):
    B.add_edge(komponenten[i], komponenten[i + 1])
print(nx.is_connected(B))""")
t('''Gib für jede Person in `kontakte` aus, wie viele Personen zu ihrer Komponente gehören (sie selbst eingeschlossen), in der Form `Ali 3`.''',
  "import networkx as nx\n\nkontakte = nx.Graph([('Ali', 'Bea'), ('Bea', 'Cem'), ('Dana', 'Emil'), ('Fiona', 'Gus'), ('Gus', 'Hanna'), ('Hanna', 'Ida')])",
  """for v in kontakte.nodes:
    print(v, len(nx.node_connected_component(kontakte, v)))""")
t('''Ein Einbahnstraßennetz (`E`): Prüfe, ob man von jedem Ort zu jedem kommt (stark zusammenhängend). Gib danach alle Paare (u, v) aus, bei denen man von u **nicht** nach v kommt.''',
  "import networkx as nx\n\nE = nx.DiGraph([('Markt', 'Kirche'), ('Kirche', 'Schule'), ('Schule', 'Markt'), ('Schule', 'Bad'), ('Bad', 'Park')])",
  """print(nx.is_strongly_connected(E))
for u in E.nodes:
    for v in E.nodes:
        if u != v and not nx.has_path(E, u, v):
            print(u, v)""")
predict("""import networkx as nx

G = nx.Graph([(1, 2), (3, 4), (4, 5)])
G.add_node(6)
print(nx.number_connected_components(G))
print(nx.has_path(G, 3, 5), nx.has_path(G, 2, 3))
print(sorted(nx.node_connected_component(G, 5)))""")

# ---------------------------------------------------------------- 2
sec('Breitensuche und kürzeste Wege')
expl('''#### Breitensuche

Die **Breitensuche** beginnt bei einem Startknoten, besucht dann alle seine Nachbarn, dann deren noch nicht besuchte Nachbarn usw. Sie arbeitet sich also
**Schicht für Schicht** nach außen vor.

| Aufruf | Ergebnis |
|---|---|
| `list(nx.bfs_layers(G, s))` | die Schichten: Liste von Listen (Abstand 0, 1, 2, …) |
| `list(nx.bfs_edges(G, s))` | die Kanten, über die die Knoten entdeckt werden |
| `nx.bfs_tree(G, s)` | der **Breitensuchbaum** (ein gerichteter Graph aus diesen Kanten) |

Welcher Nachbar zuerst besucht wird, hängt von der Reihenfolge ab, in der die Kanten eingefügt wurden.''',
     """import networkx as nx

G = nx.Graph([('a', 'b'), ('a', 'c'), ('b', 'd'), ('c', 'd'), ('c', 'e'), ('d', 'f'), ('e', 'f')])
print(list(nx.bfs_layers(G, 'a')))
print(list(nx.bfs_edges(G, 'a')))""")
expl('''#### Kürzeste Wege (nach Anzahl der Kanten)

Weil die Breitensuche Schicht für Schicht vorgeht, findet sie Wege mit **möglichst wenigen Kanten**:

- `nx.shortest_path(G, u, v)` gibt einen solchen Weg als Liste von Knoten zurück,
- `nx.shortest_path_length(G, u, v)` seine Länge (Anzahl der Kanten),
- `nx.single_source_shortest_path_length(G, u)` ein Dictionary mit den Abständen von u zu allen erreichbaren Knoten,
- `list(nx.all_shortest_paths(G, u, v))` alle kürzesten Wege.

Gibt es keinen Weg, entsteht ein Fehler (`NetworkXNoPath`).''',
     """import networkx as nx

G = nx.Graph([('a', 'b'), ('a', 'c'), ('b', 'd'), ('c', 'd'), ('c', 'e'), ('d', 'f'), ('e', 'f')])
print(nx.shortest_path(G, 'a', 'f'), nx.shortest_path_length(G, 'a', 'f'))
print(nx.single_source_shortest_path_length(G, 'a'))
print(list(nx.all_shortest_paths(G, 'a', 'f')))
G.add_node('z')
print(nx.shortest_path(G, 'a', 'z'))""", error=nx.NetworkXNoPath)

NETZ = ("import networkx as nx\n\nN = nx.Graph([('Ali', 'Bea'), ('Ali', 'Cem'), ('Bea', 'Dana'), ('Cem', 'Dana'), ('Cem', 'Emil'), ('Dana', 'Fiona'), ('Emil', 'Gus'),\n"
        "              ('Fiona', 'Gus'), ('Gus', 'Hanna'), ('Fiona', 'Ida')])")
t('''Ein Gerücht startet bei Ali und wird jede Stunde an alle Freunde weitererzählt. Gib mit `bfs_layers` aus, wer es nach 0, 1, 2, … Stunden neu erfährt, in der Form `Stunde 1: ['Bea', 'Cem']`.''', NETZ,
  """for stunde, schicht in enumerate(nx.bfs_layers(N, 'Ali')):
    print(f'Stunde {stunde}: {schicht}')""")
t('Gib die Kanten der Breitensuche ab Ali aus und die Anzahl der Kanten des Breitensuchbaums.', NETZ,
  """print(list(nx.bfs_edges(N, 'Ali')))
print(nx.bfs_tree(N, 'Ali').number_of_edges())""")
t('Gib einen kürzesten Weg von Ali zu Hanna und seine Länge aus, dann alle kürzesten Wege von Ali zu Gus.', NETZ,
  """print(nx.shortest_path(N, 'Ali', 'Hanna'))
print(nx.shortest_path_length(N, 'Ali', 'Hanna'))
print(list(nx.all_shortest_paths(N, 'Ali', 'Gus')))""")
t('''„Wie viele Ecken entfernt?“: Gib für jede Person den Abstand zu Ali aus und danach alle Personen mit dem größten Abstand (sortiert).''', NETZ,
  """abstand = nx.single_source_shortest_path_length(N, 'Ali')
for name, d in abstand.items():
    print(name, d)
weitester = max(abstand.values())
namen = []
for name, d in abstand.items():
    if d == weitester:
        namen.append(name)
print(sorted(namen))""")
t('''Der **Durchmesser** eines zusammenhängenden Graphen ist der größte Abstand zwischen zwei Knoten. Berechne ihn mit zwei Schleifen über alle Paare und `shortest_path_length`
und vergleiche mit `nx.diameter(N)`.''', NETZ,
  """groesster = 0
for u in N.nodes:
    for v in N.nodes:
        d = nx.shortest_path_length(N, u, v)
        if d > groesster:
            groesster = d
print(groesster, nx.diameter(N))""")
t('''Fange den Fehler ab, wenn es keinen Weg gibt: Füge den Knoten `Jan` ohne Kanten hinzu und gib für Hanna und Jan den Abstand zu Ali aus oder `kein Weg`.''', NETZ,
  """N.add_node('Jan')
for ziel in ['Hanna', 'Jan']:
    try:
        print(ziel, nx.shortest_path_length(N, 'Ali', ziel))
    except nx.NetworkXNoPath:
        print(ziel, 'kein Weg')""")
t('''In einem U-Bahn-Netz (Linien wie in `linien`) zählt jede Fahrt zwischen zwei Haltestellen als eine Station. Baue den Graphen und gib die Route mit den wenigsten Stationen von `Zoo` nach
`Hafen` und die Anzahl der Stationen aus.''',
  "import networkx as nx\n\nlinien = [['Zoo', 'Uni', 'Markt', 'Bahnhof', 'Hafen'], ['Zoo', 'Park', 'Rathaus', 'Hafen'], ['Uni', 'Park', 'Klinik']]",
  """U = nx.Graph()
for halte in linien:
    for i in range(len(halte) - 1):
        U.add_edge(halte[i], halte[i + 1])
weg = nx.shortest_path(U, 'Zoo', 'Hafen')
print(weg, len(weg) - 1)""")
predict("""import networkx as nx

G = nx.path_graph(5)
print(list(nx.bfs_layers(G, 2)))
print(nx.shortest_path(G, 0, 4))
print(nx.single_source_shortest_path_length(G, 4)[0])""")

# ---------------------------------------------------------------- 3
sec('Tiefensuche')
expl('''#### Tiefensuche

Die **Tiefensuche** geht vom Startknoten aus immer **so tief wie möglich**: zum ersten noch nicht besuchten Nachbarn, von dort wieder zum ersten noch nicht besuchten Nachbarn usw.
Geht es nicht weiter, geht sie zurück (*Backtracking*) und probiert den nächsten Nachbarn.

| Aufruf | Ergebnis |
|---|---|
| `list(nx.dfs_preorder_nodes(G, s))` | die Knoten in der Reihenfolge, in der sie **zuerst besucht** werden |
| `list(nx.dfs_postorder_nodes(G, s))` | die Knoten in der Reihenfolge, in der sie **fertig** sind (alle Nachbarn erledigt) |
| `list(nx.dfs_edges(G, s))` | die Kanten, über die die Knoten entdeckt werden |
| `nx.dfs_tree(G, s)` | der **Tiefensuchbaum** |''',
     """import networkx as nx

G = nx.Graph([('a', 'b'), ('a', 'c'), ('b', 'd'), ('c', 'd'), ('c', 'e'), ('d', 'f'), ('e', 'f')])
print(list(nx.dfs_preorder_nodes(G, 'a')))
print(list(nx.dfs_postorder_nodes(G, 'a')))
print(list(nx.dfs_edges(G, 'a')))
print(list(nx.bfs_edges(G, 'a')))""")

BAUM = "import networkx as nx\n\nT = nx.Graph([('A', 'B'), ('A', 'C'), ('B', 'D'), ('B', 'E'), ('C', 'F'), ('C', 'G'), ('E', 'H')])"
t('Gib für den Baum `T` ab A die Reihenfolge der Breitensuche (Knoten der Schichten hintereinander) und die der Tiefensuche (preorder) aus.', BAUM,
  """bfs = []
for schicht in nx.bfs_layers(T, 'A'):
    bfs += schicht
print(bfs)
print(list(nx.dfs_preorder_nodes(T, 'A')))""")
t('Gib für den Baum `T` ab A die postorder-Reihenfolge der Tiefensuche aus.', BAUM,
  "print(list(nx.dfs_postorder_nodes(T, 'A')))")
t('''Die Reihenfolge der Tiefensuche hängt von der Reihenfolge der Nachbarn ab. Baue denselben Baum mit der umgekehrten Kantenliste (`kanten[::-1]`) und gib die preorder-Reihenfolge ab A aus.''',
  "import networkx as nx\n\nkanten = [('A', 'B'), ('A', 'C'), ('B', 'D'), ('B', 'E'), ('C', 'F'), ('C', 'G'), ('E', 'H')]",
  """print(list(nx.dfs_preorder_nodes(nx.Graph(kanten), 'A')))
print(list(nx.dfs_preorder_nodes(nx.Graph(kanten[::-1]), 'A')))""")
t('''Ein Ordnerbaum ist ein gerichteter Graph (Ordner → Unterordner/Datei). Gib mit `dfs_preorder_nodes` alle Einträge ab `/` aus, eingerückt nach ihrer Tiefe (2 Leerzeichen pro Ebene). Die Tiefe
liefert `nx.shortest_path_length(D, '/', eintrag)`.''',
  "import networkx as nx\n\nD = nx.DiGraph([('/', 'home'), ('/', 'etc'), ('home', 'ali'), ('home', 'bea'), ('ali', 'foto.jpg'), ('ali', 'brief.txt'), ('etc', 'config')])",
  """for eintrag in nx.dfs_preorder_nodes(D, '/'):
    print('  ' * nx.shortest_path_length(D, '/', eintrag) + eintrag)""")
t('''Gib für den Graphen `G` die Kanten des Tiefensuchbaums und die des Breitensuchbaums ab 1 aus. Gib außerdem für beide Bäume die Tiefe aus (größter Abstand vom Start im **Baum**,
`max(nx.single_source_shortest_path_length(baum, 1).values())`).''',
  "import networkx as nx\n\nG = nx.Graph([(1, 2), (1, 3), (1, 4), (2, 5), (3, 5), (4, 6), (5, 6), (5, 7)])",
  """d = nx.dfs_tree(G, 1)
b = nx.bfs_tree(G, 1)
print(list(d.edges))
print(list(b.edges))
print(max(nx.single_source_shortest_path_length(d, 1).values()), max(nx.single_source_shortest_path_length(b, 1).values()))""")
predict("""import networkx as nx

G = nx.Graph([(1, 2), (1, 3), (2, 4), (3, 4)])
print(list(nx.dfs_preorder_nodes(G, 1)))
print(list(nx.bfs_edges(G, 1)))""")

# ---------------------------------------------------------------- 4
sec('Labyrinthe als Gittergraph')
expl('''#### Ein Labyrinth als Graph

Ein Labyrinth aus Feldern ist ein **Gittergraph**: `nx.grid_2d_graph(zeilen, spalten)` hat die Knoten `(zeile, spalte)`, benachbarte Felder sind verbunden.
Mauern entfernt man mit `G.remove_nodes_from(liste)`. Danach findet `shortest_path` den kürzesten Weg durch das Labyrinth.''',
     """import networkx as nx

karte = ['S.#.',
         '.##.',
         '...Z']
G = nx.grid_2d_graph(len(karte), len(karte[0]))
mauern = []
for z in range(len(karte)):
    for s in range(len(karte[0])):
        if karte[z][s] == '#':
            mauern.append((z, s))
G.remove_nodes_from(mauern)
print(nx.shortest_path(G, (0, 0), (2, 3)))""")

KARTE = ("import networkx as nx\n\nkarte = ['S..#....',\n         '.#.#.##.',\n         '.#...#..',\n         '.####.#.',\n         '......#Z']\n\n"
         "def labyrinth(karte):\n    G = nx.grid_2d_graph(len(karte), len(karte[0]))\n    for z in range(len(karte)):\n        for s in range(len(karte[0])):\n"
         "            if karte[z][s] == '#':\n                G.remove_node((z, s))\n    return G\n")
t('Erzeuge mit `labyrinth()` den Graphen und gib die Länge des kürzesten Weges von S (0, 0) nach Z (4, 7) aus.', KARTE,
  """G = labyrinth(karte)
print(nx.shortest_path_length(G, (0, 0), (4, 7)))""")
t('''Zeichne den kürzesten Weg in die Karte ein: Ersetze jedes Feld des Weges (außer S und Z) durch `*` und gib die Karte Zeile für Zeile aus.''', KARTE,
  """G = labyrinth(karte)
weg = nx.shortest_path(G, (0, 0), (4, 7))
zeilen = []
for zeile in karte:
    zeilen.append(list(zeile))
for z, s in weg[1:-1]:
    zeilen[z][s] = '*'
for zeile in zeilen:
    print(''.join(zeile))""")
t('''Gib aus, wie viele freie Felder (Knoten) das Labyrinth hat und wie viele davon von S aus erreichbar sind (`node_connected_component`).''', KARTE,
  """G = labyrinth(karte)
print(G.number_of_nodes(), len(nx.node_connected_component(G, (0, 0))))""")
t('''Welche **eine** Mauer müsste man entfernen, damit der Weg von S nach Z am kürzesten wird? Probiere jede Mauer: Karte kopieren, Mauer durch `.` ersetzen, Weglänge berechnen.
Gib die Position der besten Mauer und die neue Weglänge aus (bei Gleichstand die erste).''', KARTE,
  """bestes = None
for z in range(len(karte)):
    for s in range(len(karte[0])):
        if karte[z][s] == '#':
            neu = list(karte)
            neu[z] = karte[z][:s] + '.' + karte[z][s + 1:]
            laenge = nx.shortest_path_length(labyrinth(neu), (0, 0), (4, 7))
            if bestes is None or laenge < bestes[1]:
                bestes = ((z, s), laenge)
print(bestes)""")

# ---------------------------------------------------------------- 5
sec('Kreise, Bäume und Abhängigkeiten')
expl('''#### Kreise und Bäume

- Ein **Kreis** ist ein Weg, der zu seinem Anfang zurückführt. `nx.find_cycle(G)` gibt einen Kreis als Liste von Kanten zurück oder wirft `NetworkXNoCycle`.
- Ein **Baum** ist ein zusammenhängender Graph ohne Kreise (`nx.is_tree(G)`). Ein Baum mit n Knoten hat genau n − 1 Kanten.
- Ein **Wald** besteht aus mehreren Bäumen (`nx.is_forest(G)`).''',
     """import networkx as nx

G = nx.Graph([(1, 2), (2, 3), (3, 4), (4, 2)])
print(nx.find_cycle(G))
T = nx.Graph([(1, 2), (1, 3), (3, 4)])
print(nx.is_tree(T), T.number_of_nodes(), T.number_of_edges())
T.add_edge(5, 6)
print(nx.is_tree(T), nx.is_forest(T))""")
expl('''#### Abhängigkeiten: topologische Sortierung

Eine Kante a → b bedeutet: „a muss vor b erledigt werden“. Hat der gerichtete Graph **keinen Kreis** (`nx.is_directed_acyclic_graph(G)`), kann man alle Aufgaben in eine Reihenfolge
bringen, die alle Abhängigkeiten einhält: eine **topologische Sortierung**. `list(nx.lexicographical_topological_sort(G))` liefert eine, bei der von mehreren möglichen Aufgaben immer
die alphabetisch erste zuerst kommt.

`nx.ancestors(G, v)` sind alle Aufgaben, die vor v erledigt sein müssen (direkt oder indirekt), `nx.descendants(G, v)` alle, die von v abhängen. Beides sind Mengen.''',
     """import networkx as nx

A = nx.DiGraph([('Mehl kaufen', 'Teig machen'), ('Eier kaufen', 'Teig machen'), ('Teig machen', 'Backen'), ('Ofen an', 'Backen'), ('Backen', 'Essen')])
print(nx.is_directed_acyclic_graph(A))
print(list(nx.lexicographical_topological_sort(A)))
print(sorted(nx.ancestors(A, 'Backen')))""")

KURSE = "import networkx as nx\n\nK = nx.DiGraph([('Mathe 1', 'Mathe 2'), ('Mathe 2', 'Mathe 3'), ('Mathe 1', 'Physik 1'), ('Physik 1', 'Physik 2'), ('Mathe 2', 'Physik 2'),\n                ('Info 1', 'Info 2'), ('Mathe 2', 'Info 2'), ('Info 2', 'Projekt'), ('Physik 2', 'Projekt')])"
t('Ein Studienplan: Kante a → b heißt „a ist Voraussetzung für b“. Prüfe, ob es keine Kreise gibt, und gib eine Reihenfolge aller Kurse mit `lexicographical_topological_sort` aus.', KURSE,
  """print(nx.is_directed_acyclic_graph(K))
print(list(nx.lexicographical_topological_sort(K)))""")
t('Gib alle Kurse aus, die man vor dem `Projekt` belegen muss (sortiert), und alle Kurse, die auf `Mathe 2` aufbauen (sortiert).', KURSE,
  """print(sorted(nx.ancestors(K, 'Projekt')))
print(sorted(nx.descendants(K, 'Mathe 2')))""")
t('''Wie viele Semester braucht man mindestens, wenn man pro Semester beliebig viele Kurse belegen kann, deren Voraussetzungen erfüllt sind? Das ist die Anzahl der Knoten auf dem
**längsten** Weg: `len(nx.dag_longest_path(K))`. Gib den längsten Weg und die Zahl der Semester aus.''', KURSE,
  """weg = nx.dag_longest_path(K)
print(weg)
print(len(weg))""")
t('''Jemand trägt versehentlich die Voraussetzung `Projekt` → `Mathe 1` ein. Prüfe, ob der Plan dann noch erfüllbar ist, und gib den Kreis mit `find_cycle` aus.''', KURSE,
  """K.add_edge('Projekt', 'Mathe 1')
print(nx.is_directed_acyclic_graph(K))
print(nx.find_cycle(K))""")
t('''Gib für jeden der Graphen in `graphen` aus, ob er ein Baum ist, und wenn nicht, ob er einen Kreis hat (mit `try` und `nx.NetworkXNoCycle`) oder nicht zusammenhängend ist.''',
  "import networkx as nx\n\ngraphen = {'A': nx.Graph([(1, 2), (2, 3), (2, 4)]), 'B': nx.Graph([(1, 2), (2, 3), (3, 1)]), 'C': nx.Graph([(1, 2), (3, 4)])}",
  """for name, G in graphen.items():
    if nx.is_tree(G):
        print(name, 'Baum')
    else:
        try:
            nx.find_cycle(G)
            print(name, 'Kreis')
        except nx.NetworkXNoCycle:
            print(name, 'nicht zusammenhängend')""")
predict("""import networkx as nx

G = nx.DiGraph([('c', 'b'), ('b', 'a'), ('d', 'a')])
print(list(nx.lexicographical_topological_sort(G)))
print(sorted(nx.ancestors(G, 'a')), sorted(nx.descendants(G, 'c')))""")
predict("""import networkx as nx

T = nx.Graph([(1, 2), (2, 3)])
print(nx.is_tree(T))
nx.find_cycle(T)""", error=nx.NetworkXNoCycle)

# ---------------------------------------------------------------- 6
sec('Gemischte Übungen')
t('''Ein **Wortleiter**-Rätsel: Von `HAND` nach `WILD`, indem man in jedem Schritt genau einen Buchstaben ändert und nur Wörter aus `woerter` benutzt. Baue den Graphen (Kante bei genau einem
Unterschied an derselben Stelle) und gib die kürzeste Leiter aus.''',
  "import networkx as nx\n\nwoerter = ['HAND', 'HUND', 'WAND', 'RAND', 'RIND', 'WIND', 'BUND', 'BAND', 'WILD', 'MILD', 'MIND']",
  """def nachbarn(a, b):
    n = 0
    for x, y in zip(a, b):
        if x != y:
            n += 1
    return n == 1

G = nx.Graph()
for i in range(len(woerter)):
    for j in range(i + 1, len(woerter)):
        if nachbarn(woerter[i], woerter[j]):
            G.add_edge(woerter[i], woerter[j])
print(nx.shortest_path(G, 'HAND', 'WILD'))""")
t('''Ein Springer auf dem Schachbrett: Felder (z, s) mit 0 ≤ z, s ≤ 7 sind verbunden, wenn ein Springerzug dazwischen liegt (z ± 1, s ± 2 oder z ± 2, s ± 1). Baue den Graphen und gib aus, wie viele
Züge der Springer mindestens von (0, 0) nach (7, 7) braucht, und einen solchen Weg.''',
  "import networkx as nx",
  """G = nx.Graph()
for z in range(8):
    for s in range(8):
        for dz, ds in [(1, 2), (2, 1), (-1, 2), (-2, 1)]:
            if 0 <= z + dz < 8 and 0 <= s + ds < 8:
                G.add_edge((z, s), (z + dz, s + ds))
print(nx.shortest_path_length(G, (0, 0), (7, 7)))
print(nx.shortest_path(G, (0, 0), (7, 7)))""")
t('''Ein Computervirus breitet sich im Netzwerk `V` aus: Jeden Tag befällt es alle Nachbarn befallener Rechner. Am Tag 0 ist `PC1` befallen. Gib aus, an welchem Tag jeder Rechner befallen ist,
und welcher Rechner zuletzt befallen wird. Welche Rechner bleiben verschont, wenn man vorher die Verbindung `Router`–`Server` trennt? Gib sie sortiert aus.''',
  "import networkx as nx\n\nV = nx.Graph([('PC1', 'PC2'), ('PC1', 'Router'), ('PC2', 'Router'), ('Router', 'Server'), ('Server', 'PC3'), ('Server', 'PC4'), ('PC4', 'Drucker')])",
  """tage = nx.single_source_shortest_path_length(V, 'PC1')
print(tage)
print(max(tage, key=lambda r: tage[r]))
V.remove_edge('Router', 'Server')
verschont = []
for r in V.nodes:
    if not nx.has_path(V, 'PC1', r):
        verschont.append(r)
print(sorted(verschont))""")
predict("""import networkx as nx

G = nx.cycle_graph(6)
print(nx.shortest_path_length(G, 0, 3), nx.shortest_path_length(G, 0, 5))
print(list(nx.bfs_layers(G, 0))[-1])
print(nx.is_tree(G))""")

generate('networkx_suchen', 'networkx 2: Wege, Breiten- und Tiefensuche, Abhängigkeiten', INTRO)
