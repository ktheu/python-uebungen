# Erzeugt ../content/asyncio_anwendungen.ipynb (siehe nbgen.py). Viertes Notebook der asyncio-Reihe (asynchilfe.py, asyncnb.py).
# Regeln wie in den anderen asyncio-Notebooks: Zeiten nur ganzzahlig mit round(), Reihenfolgen nur bei Wartezeiten, die sich um
# mindestens 0.1 s unterscheiden (Drift beachten: Ketten von sleep(0.1) driften bis ca. 0.05 s), nie x,5 runden, nie asyncio.run() in Codezellen.
# Arbeiter mit `while True` werden immer mit cancel() beendet (nach queue.join()), Erzeuger/Verbraucher mit None als Ende-Signal.
# Nie Queue-/Task-/Future-Objekte ausgeben (Adressen).
from nbgen import sec, expl, task, predict, generate
from asynchilfe import t, reihe, AUSFUEHREN

INTRO = f'''In diesem Notebook geht es um Bausteine für größere asynchrone Programme: **Queues** (Warteschlangen), mit denen Coroutinen sich Arbeit zuschieben,
eigene **`async with`**-Objekte, **`async for`** mit asynchronen Generatoren und kleine Anwendungen, in denen alles zusammenkommt.

Die Reihe besteht aus vier Notebooks:

{reihe('asyncio_anwendungen')}

Du solltest die Notebooks **asyncio_grundlagen**, **asyncio_tasks** und **asyncio_steuerung** kennen (`create_task()`, `gather()`, `cancel()`, `Lock`, `Event`).
Klassen mit Methoden und Fehler abfangen brauchst du ebenfalls.

Die Abschnitte über `@asynccontextmanager` und über `Future` und `call_later` sind für das **Leistungsfach** gedacht.

Gemessene Zeiten sind nie ganz genau. Deshalb runden wir sie mit `round()` auf ganze Sekunden.

Jeder Abschnitt beginnt mit kurzen Erklärungen und Beispielen. Führe die Beispiele aus und probiere sie ruhig ein wenig aus.
Danach folgen viele kleine Übungen. Wenn etwas vorgegeben ist, steht es schon in der Codezelle.'''

# ---------------------------------------------------------------- 1
sec('Queue: Coroutinen schieben sich Arbeit zu')
expl('''#### Die Warteschlange `asyncio.Queue`

Eine `Queue` ist eine Warteschlange wie an der Kasse: Was **zuerst** hineinkommt, kommt **zuerst** wieder heraus (FIFO).
Die Besonderheit: Man kann **warten**, bis etwas in der Schlange ist.

- `await schlange.put(x)` legt `x` hinten an.
- `await schlange.get()` holt das vorderste Element. Ist die Schlange leer, wartet `get()`, bis jemand etwas hineinlegt.
- `schlange.qsize()` ist die Anzahl der Elemente, `schlange.empty()` fragt, ob sie leer ist.''',
     """import asyncio

schlange = asyncio.Queue()
await schlange.put('Ali')
await schlange.put('Bea')
await schlange.put('Cem')
print('Größe:', schlange.qsize())
print(await schlange.get())
print(await schlange.get())
print('Größe:', schlange.qsize())
print('leer?', schlange.empty())""")
expl('''#### Erzeuger und Verbraucher

Das wichtigste Muster mit einer Queue: Ein **Erzeuger** legt Arbeit in die Schlange, ein **Verbraucher** holt sie heraus und erledigt sie. Beide laufen gleichzeitig.
Der Verbraucher weiß nicht, wann der Erzeuger fertig ist. Deshalb legt der Erzeuger am Ende ein **Ende-Signal** in die Schlange, meist `None`.
Der Verbraucher hört auf, wenn er es holt.''',
     """import asyncio

schlange = asyncio.Queue()

async def erzeuger():
    for nr in [1, 2, 3]:
        await asyncio.sleep(0.2)
        print('Erzeuger legt ab:', nr)
        await schlange.put(nr)
    await schlange.put(None)

async def verbraucher():
    while True:
        wert = await schlange.get()
        if wert is None:
            break
        print('Verbraucher holt:', wert)
    print('Verbraucher fertig')

await asyncio.gather(erzeuger(), verbraucher())""")
expl('''#### Mehrere Verbraucher

Mehrere Verbraucher holen aus **derselben** Schlange. Jedes Element bekommt genau einer. Wer gerade frei ist, holt das nächste.
So kann man Arbeit auf mehrere „Kassen“ verteilen. Jeder Verbraucher braucht dann ein eigenes Ende-Signal.''',
     """import asyncio

kunden = [('Ali', 0.2), ('Bea', 0.5), ('Cem', 0.4), ('Dana', 0.2)]
schlange = asyncio.Queue()
for kunde in kunden:
    schlange.put_nowait(kunde)
schlange.put_nowait(None)
schlange.put_nowait(None)

async def kasse(nr):
    while True:
        kunde = await schlange.get()
        if kunde is None:
            break
        name, dauer = kunde
        print('Kasse', nr, 'bedient', name)
        await asyncio.sleep(dauer)
        print('Kasse', nr, 'fertig mit', name)

await asyncio.gather(kasse(1), kasse(2))""")
expl('''#### `put_nowait()` und `join()`

- `schlange.put_nowait(x)` legt etwas ab, **ohne** zu warten (eine normale Funktion, kein `await`).
- Ein Arbeiter ruft nach jedem erledigten Element `schlange.task_done()` auf.
- `await schlange.join()` wartet, bis **alle** Elemente erledigt sind (für jedes `put` ein `task_done`).

Typisches Muster: Arbeit in die Schlange legen, mehrere Arbeiter starten, mit `join()` auf das Ende warten, die Arbeiter (die in einer Endlosschleife warten) mit `cancel()` beenden.
Dann braucht man kein Ende-Signal.''',
     """import asyncio

schlange = asyncio.Queue()
for zahl in range(1, 7):
    schlange.put_nowait(zahl)
ergebnisse = []

async def arbeiter():
    while True:
        zahl = await schlange.get()
        await asyncio.sleep(0.1)
        ergebnisse.append(zahl * zahl)
        schlange.task_done()

arbeiterliste = []
for i in range(3):
    arbeiterliste.append(asyncio.create_task(arbeiter()))

await schlange.join()
for a in arbeiterliste:
    a.cancel()
await asyncio.gather(*arbeiterliste, return_exceptions=True)
print(sorted(ergebnisse))""")
expl('''#### Begrenzte Schlange: `maxsize`

Mit `asyncio.Queue(maxsize=n)` passen höchstens `n` Elemente hinein. Ist die Schlange **voll**, muss `put()` warten, bis jemand etwas herausgenommen hat.
So bremst ein langsamer Verbraucher einen schnellen Erzeuger aus.''',
     """import asyncio

schlange = asyncio.Queue(maxsize=2)

async def erzeuger():
    for nr in [1, 2, 3, 4]:
        await schlange.put(nr)
        print('abgelegt:', nr)
    await schlange.put(None)

async def verbraucher():
    while True:
        wert = await schlange.get()
        if wert is None:
            break
        print('geholt:', wert)
        await asyncio.sleep(0.3)

await asyncio.gather(erzeuger(), verbraucher())""")
expl('''#### Ohne Warten: `QueueFull` und `QueueEmpty`

`put_nowait()` bei einer vollen Schlange wirft `asyncio.QueueFull`, `get_nowait()` bei einer leeren Schlange wirft `asyncio.QueueEmpty`.
`schlange.full()` fragt, ob sie voll ist.''',
     """import asyncio

schlange = asyncio.Queue(maxsize=2)
schlange.put_nowait('a')
schlange.put_nowait('b')
print('voll?', schlange.full())
try:
    schlange.put_nowait('c')
except asyncio.QueueFull:
    print('Schlange ist voll')

print(schlange.get_nowait(), schlange.get_nowait())
try:
    schlange.get_nowait()
except asyncio.QueueEmpty:
    print('Schlange ist leer')""")
expl('''#### Andere Reihenfolgen: `LifoQueue` und `PriorityQueue`

- `asyncio.LifoQueue` ist ein **Stapel**: Das **zuletzt** abgelegte Element kommt zuerst heraus.
- `asyncio.PriorityQueue` gibt immer das **kleinste** Element zuerst heraus. Üblich sind Tupel `(priorität, text)`: Die kleinste Priorität kommt zuerst.''',
     """import asyncio

stapel = asyncio.LifoQueue()
for x in ['a', 'b', 'c']:
    stapel.put_nowait(x)
print(stapel.get_nowait(), stapel.get_nowait(), stapel.get_nowait())

wichtig = asyncio.PriorityQueue()
wichtig.put_nowait((3, 'Hausaufgaben'))
wichtig.put_nowait((1, 'Klausur lernen'))
wichtig.put_nowait((2, 'Referat'))
while not wichtig.empty():
    print(wichtig.get_nowait())""")

predict("""import asyncio

q = asyncio.Queue()
await q.put(1)
await q.put(2)
await q.put(3)
print(await q.get())
await q.put(4)
print(q.qsize())
print(await q.get())""", erklaerung='''Die Schlange arbeitet nach dem Prinzip „zuerst hinein, zuerst heraus“. Nach dem ersten `get()` (Ergebnis `1`) liegen `2` und `3` in der Schlange, dann kommt `4` dazu: drei Elemente. Das nächste `get()` liefert `2`.

```
1
3
2
```''')
predict("""import asyncio

q = asyncio.LifoQueue()
for x in [1, 2, 3]:
    q.put_nowait(x)
print(q.get_nowait())
print(q.get_nowait())""", erklaerung='''Eine `LifoQueue` ist ein Stapel: Das zuletzt abgelegte Element (`3`) kommt zuerst heraus, dann `2`.

```
3
2
```''')
predict("""import asyncio

q = asyncio.PriorityQueue()
q.put_nowait((2, 'b'))
q.put_nowait((3, 'c'))
q.put_nowait((1, 'a'))
print(q.get_nowait())
print(q.get_nowait()[1])""", erklaerung='''Eine `PriorityQueue` gibt immer das kleinste Element zuerst heraus. Die Tupel werden nach der ersten Zahl sortiert: zuerst `(1, 'a')`, dann `(2, 'b')`. Vom zweiten Tupel wird nur der Text (Index `1`) ausgegeben.

```
(1, 'a')
b
```''')
predict("""import asyncio

q = asyncio.Queue()

async def erzeuger():
    for x in ['a', 'b']:
        await asyncio.sleep(0.1)
        await q.put(x)
    await q.put(None)

async def verbraucher():
    while True:
        x = await q.get()
        if x is None:
            break
        print(x)
    print('Ende')

await asyncio.gather(verbraucher(), erzeuger())""", erklaerung='''Der Verbraucher beginnt zuerst, aber die Schlange ist leer: `get()` wartet. Der Erzeuger legt nach 0,1 Sekunden `a` ab, der Verbraucher gibt es aus.
Dasselbe passiert mit `b`. Dann legt der Erzeuger `None` ab, der Verbraucher beendet die Schleife und gibt `Ende` aus.

```
a
b
Ende
```''')
predict("""import asyncio

q = asyncio.Queue()
for x in range(3):
    q.put_nowait(x)

async def arbeiter():
    while True:
        x = await q.get()
        print('erledigt', x)
        q.task_done()

a = asyncio.create_task(arbeiter())
await q.join()
a.cancel()
print('fertig')""", erklaerung='''Der Arbeiter holt die Elemente nacheinander (`0`, `1`, `2`) und meldet jedes mit `task_done()`. Wenn alle erledigt sind, kehrt `join()` zurück. Dann wird der Arbeiter abgebrochen, und `fertig` wird ausgegeben.

```
erledigt 0
erledigt 1
erledigt 2
fertig
```''')
t('''Lege in einer Schlange nacheinander `'Mathe'`, `'Deutsch'` und `'Kunst'` ab (mit `await put`). Gib dann `qsize()` aus und danach alle Elemente in der Reihenfolge, in der sie herauskommen (mit `get()` in einer Schleife).''',
  given='import asyncio\n', body="""schlange = asyncio.Queue()
for fach in ['Mathe', 'Deutsch', 'Kunst']:
    await schlange.put(fach)
print(schlange.qsize())
while not schlange.empty():
    print(await schlange.get())""")
t('''Lege in eine `Queue(maxsize=2)` mit `put_nowait()` die Zahlen `1` und `2`. Gib `full()` aus. Versuche, `3` abzulegen, und gib `voll` aus, wenn `asyncio.QueueFull` entsteht.
Hole danach ein Element mit `get_nowait()` und gib es aus.''',
  given='import asyncio\n', body="""schlange = asyncio.Queue(maxsize=2)
schlange.put_nowait(1)
schlange.put_nowait(2)
print(schlange.full())
try:
    schlange.put_nowait(3)
except asyncio.QueueFull:
    print('voll')
print(schlange.get_nowait())""")
t('''Schreibe einen Erzeuger, der die Zahlen `1` bis `4` ablegt (nach jeder `0.1` Sekunden Pause) und am Ende `None`. Der Verbraucher gibt jedes **Quadrat** aus (`1`, `4`, `9`, `16`) und am Ende `Fertig`.
Die Schlange `schlange` ist vorgegeben.''',
  given='import asyncio\n\nschlange = asyncio.Queue()\n', body="""async def erzeuger():
    for zahl in [1, 2, 3, 4]:
        await asyncio.sleep(0.1)
        await schlange.put(zahl)
    await schlange.put(None)

async def verbraucher():
    while True:
        zahl = await schlange.get()
        if zahl is None:
            break
        print(zahl * zahl)
    print('Fertig')

await asyncio.gather(erzeuger(), verbraucher())""")
t('''Der Erzeuger `erzeuger()` ist vorgegeben und legt Preise ab (am Ende `None`). Schreibe den Verbraucher `kasse()`, der alle Preise addiert und am Ende `Summe: <betrag>` ausgibt.''',
  given="""import asyncio

schlange = asyncio.Queue()

async def erzeuger():
    for preis in [3, 5, 2, 10]:
        await asyncio.sleep(0.1)
        await schlange.put(preis)
    await schlange.put(None)
""", body="""async def kasse():
    summe = 0
    while True:
        preis = await schlange.get()
        if preis is None:
            break
        summe += preis
    print('Summe:', summe)

await asyncio.gather(erzeuger(), kasse())""")
t('''Zwei Kassen holen Kunden aus der Schlange. Die Kunden `kunden` und ihre Dauer sind vorgegeben, ebenso die beiden Ende-Signale. Schreibe `kasse(nr)`: Sie gibt `Kasse <nr> bedient <name>` aus, wartet die Dauer
und gibt dann `Kasse <nr> fertig mit <name>` aus. Starte beide Kassen gleichzeitig.''',
  given="""import asyncio

kunden = [('Ali', 0.2), ('Bea', 0.5), ('Cem', 0.4), ('Dana', 0.2)]
schlange = asyncio.Queue()
for kunde in kunden:
    schlange.put_nowait(kunde)
schlange.put_nowait(None)
schlange.put_nowait(None)
""", body="""async def kasse(nr):
    while True:
        kunde = await schlange.get()
        if kunde is None:
            break
        name, dauer = kunde
        print('Kasse', nr, 'bedient', name)
        await asyncio.sleep(dauer)
        print('Kasse', nr, 'fertig mit', name)

await asyncio.gather(kasse(1), kasse(2))""")
t('''Zehn Aufgaben `1` bis `10` liegen in der Schlange. Drei Arbeiter (Tasks) holen je eine Aufgabe, warten `0.1` Sekunden, hängen `aufgabe * 2` an die Liste `ergebnisse` an und rufen `task_done()` auf.
Warte mit `join()`, breche die Arbeiter ab und gib die **sortierte** Liste aus.''',
  given="""import asyncio

schlange = asyncio.Queue()
for nr in range(1, 11):
    schlange.put_nowait(nr)
ergebnisse = []
""", body="""async def arbeiter():
    while True:
        aufgabe = await schlange.get()
        await asyncio.sleep(0.1)
        ergebnisse.append(aufgabe * 2)
        schlange.task_done()

arbeiterliste = []
for i in range(3):
    arbeiterliste.append(asyncio.create_task(arbeiter()))

await schlange.join()
for a in arbeiterliste:
    a.cancel()
await asyncio.gather(*arbeiterliste, return_exceptions=True)
print(sorted(ergebnisse))""")
t('''Lege `(3, 'Hausaufgaben')`, `(1, 'Klausur lernen')`, `(4, 'Sport')` und `(2, 'Referat')` in eine `PriorityQueue`. Gib die Texte in der Reihenfolge aus, in der sie herauskommen (nach Priorität).''',
  given='import asyncio\n', body="""wichtig = asyncio.PriorityQueue()
for eintrag in [(3, 'Hausaufgaben'), (1, 'Klausur lernen'), (4, 'Sport'), (2, 'Referat')]:
    wichtig.put_nowait(eintrag)
while not wichtig.empty():
    prioritaet, text = wichtig.get_nowait()
    print(text)""")
t('''Ein Browser merkt sich besuchte Seiten als **Stapel** (`LifoQueue`): Die zuletzt besuchte Seite kommt bei „Zurück“ zuerst. Lege `'Start'`, `'Plan'` und `'Mensa'` nacheinander ab
und gehe dann dreimal zurück (`get_nowait()`). Gib jedes Mal die Seite aus.''',
  given='import asyncio\n', body="""verlauf = asyncio.LifoQueue()
for seite in ['Start', 'Plan', 'Mensa']:
    verlauf.put_nowait(seite)
for i in range(3):
    print(verlauf.get_nowait())""")
t('''Die begrenzte Schlange `schlange` (`maxsize=1`) ist vorgegeben. Der Erzeuger legt `'a'`, `'b'`, `'c'` ab und gibt nach jedem `put` die Zeile `abgelegt: <x>` aus. Der Verbraucher holt alle drei, wartet dazwischen `0.3` Sekunden
und gibt `geholt: <x>` aus. Am Ende legt der Erzeuger `None` ab. Beobachte, wie der Erzeuger ausgebremst wird.''',
  given='import asyncio\n\nschlange = asyncio.Queue(maxsize=1)\n', body="""async def erzeuger():
    for x in ['a', 'b', 'c']:
        await schlange.put(x)
        print('abgelegt:', x)
    await schlange.put(None)

async def verbraucher():
    while True:
        x = await schlange.get()
        if x is None:
            break
        print('geholt:', x)
        await asyncio.sleep(0.3)

await asyncio.gather(erzeuger(), verbraucher())""")
task('''Der Verbraucher läuft ewig, weil kein Ende-Signal kommt. Die Zelle wird deshalb nach einem Zeitlimit abgebrochen und gibt `Zeit abgelaufen` aus. Verbessere den Erzeuger so, dass er am Ende `None` ablegt (und `Verbraucher fertig` ausgegeben wird).''',
     zelle="""import asyncio

schlange = asyncio.Queue()

async def erzeuger():
    for x in [1, 2]:
        await schlange.put(x)

async def verbraucher():
    while True:
        x = await schlange.get()
        if x is None:
            break
        print('geholt:', x)
    print('Verbraucher fertig')

try:
    await asyncio.wait_for(asyncio.gather(erzeuger(), verbraucher()), timeout=0.5)
except TimeoutError:
    print('Zeit abgelaufen')""",
     solution="""import asyncio

schlange = asyncio.Queue()

async def erzeuger():
    for x in [1, 2]:
        await schlange.put(x)
    await schlange.put(None)

async def verbraucher():
    while True:
        x = await schlange.get()
        if x is None:
            break
        print('geholt:', x)
    print('Verbraucher fertig')

try:
    await asyncio.wait_for(asyncio.gather(erzeuger(), verbraucher()), timeout=0.5)
except TimeoutError:
    print('Zeit abgelaufen')""")

# ---------------------------------------------------------------- 2
sec('async with: eigene Kontextmanager')
expl('''#### Wiederholung

`async with` hast du schon bei `Lock`, `Semaphore`, `TaskGroup` und `asyncio.timeout()` benutzt. Das sind **asynchrone Kontextmanager**: Beim Betreten des Blocks passiert etwas (zum Beispiel
die Sperre nehmen), beim Verlassen wieder etwas (die Sperre freigeben), und zwar **auch bei einem Fehler**. Dabei darf gewartet werden.

Man kann eigene Klassen dafür schreiben. Sie brauchen zwei Methoden:

- `async def __aenter__(self)` wird beim Betreten ausgeführt. Der Rückgabewert landet hinter `as`.
- `async def __aexit__(self, art, fehler, spur)` wird beim Verlassen ausgeführt. Die drei Parameter beschreiben einen Fehler im Block (sonst sind sie `None`). Du kannst sie meistens ignorieren.''',
     """import asyncio

class Verbindung:
    def __init__(self, name):
        self.name = name

    async def __aenter__(self):
        print('öffne', self.name)
        await asyncio.sleep(0.1)
        return self

    async def __aexit__(self, art, fehler, spur):
        await asyncio.sleep(0.1)
        print('schließe', self.name)

    async def sende(self, text):
        await asyncio.sleep(0.1)
        print(self.name, 'sendet', text)

async with Verbindung('Server') as v:
    await v.sende('Hallo')
    await v.sende('Tschüss')
print('draußen')""")
expl('''#### Aufräumen auch bei Fehlern

`__aexit__` läuft **immer**, auch wenn im Block ein Fehler auftritt. Danach geht der Fehler normal weiter und kann mit `try` und `except` abgefangen werden.
Das macht `async with` sicherer als „öffnen, arbeiten, schließen“ von Hand.''',
     """import asyncio

class Verbindung:
    def __init__(self, name):
        self.name = name

    async def __aenter__(self):
        print('öffne', self.name)
        return self

    async def __aexit__(self, art, fehler, spur):
        print('schließe', self.name)

try:
    async with Verbindung('Datenbank') as v:
        print('arbeite')
        raise ValueError('kaputt')
        print('wird nie erreicht')
except ValueError:
    print('Fehler gefangen')""")
expl('''#### Beispiel Stoppuhr

Ein Kontextmanager, der die Dauer des Blocks misst: `__aenter__` merkt sich die Startzeit, `__aexit__` gibt die Dauer aus.''',
     """import asyncio
import time

class Stoppuhr:
    async def __aenter__(self):
        self.start = time.perf_counter()
        return self

    async def __aexit__(self, art, fehler, spur):
        print('Dauer:', round(time.perf_counter() - self.start), 's')

async with Stoppuhr():
    await asyncio.sleep(1)
    await asyncio.sleep(1)""")

predict("""import asyncio

class Tuer:
    async def __aenter__(self):
        print('auf')

    async def __aexit__(self, art, fehler, spur):
        print('zu')

async with Tuer():
    print('drin')
print('draußen')""", erklaerung='''Beim Betreten läuft `__aenter__` (`auf`), dann der Block (`drin`), beim Verlassen `__aexit__` (`zu`). Erst danach folgt `draußen`.

```
auf
drin
zu
draußen
```''')
predict("""import asyncio

class Tuer:
    async def __aenter__(self):
        print('auf')

    async def __aexit__(self, art, fehler, spur):
        print('zu')

try:
    async with Tuer():
        print('drin')
        raise KeyError('x')
        print('nie')
except KeyError:
    print('Fehler')""", erklaerung='''`auf`, `drin`, dann tritt der Fehler auf. Der Block wird verlassen und `__aexit__` läuft trotzdem (`zu`). Danach fängt `except` den Fehler (`Fehler`). `nie` wird nicht ausgegeben.

```
auf
drin
zu
Fehler
```''')
predict("""import asyncio

class Raum:
    def __init__(self, name):
        self.name = name

    async def __aenter__(self):
        print('betrete', self.name)
        return self.name.upper()

    async def __aexit__(self, art, fehler, spur):
        print('verlasse', self.name)

async with Raum('Labor') as r:
    print(r)""", erklaerung='''Der Rückgabewert von `__aenter__` ist `'LABOR'` und landet in `r`. Er wird im Block ausgegeben.

```
betrete Labor
LABOR
verlasse Labor
```''')
t('''Schreibe eine Klasse `Labor` mit `__aenter__` (gibt `Labor offen` aus) und `__aexit__` (gibt `Labor geschlossen` aus). Benutze sie mit `async with` und gib im Block `Experiment läuft` aus.''',
  given='import asyncio\n', body="""class Labor:
    async def __aenter__(self):
        print('Labor offen')

    async def __aexit__(self, art, fehler, spur):
        print('Labor geschlossen')

async with Labor():
    print('Experiment läuft')""")
t('''Schreibe eine Klasse `Datei` mit einem Namen (`__init__(self, name)`). `__aenter__` wartet `0.1` Sekunden, gibt `öffne <name>` aus und gibt das **Objekt selbst** zurück (`return self`).
`__aexit__` gibt `schließe <name>` aus. Benutze `async with Datei('noten.txt') as d:` und gib im Block `d.name` aus.''',
  given='import asyncio\n', body="""class Datei:
    def __init__(self, name):
        self.name = name

    async def __aenter__(self):
        await asyncio.sleep(0.1)
        print('öffne', self.name)
        return self

    async def __aexit__(self, art, fehler, spur):
        print('schließe', self.name)

async with Datei('noten.txt') as d:
    print(d.name)""")
t('''Die Klasse `Stoppuhr` ist vorgegeben. Benutze sie, um zwei Coroutinen `a()` (1 Sekunde) und `b()` (1 Sekunde) **gleichzeitig** mit `gather` zu messen (`Dauer: 1 s`).''',
  given="""import asyncio
import time

class Stoppuhr:
    async def __aenter__(self):
        self.start = time.perf_counter()
        return self

    async def __aexit__(self, art, fehler, spur):
        print('Dauer:', round(time.perf_counter() - self.start), 's')

async def a():
    await asyncio.sleep(1)

async def b():
    await asyncio.sleep(1)
""", body="""async with Stoppuhr():
    await asyncio.gather(a(), b())""")
t('''Die Klasse `Tuer` ist vorgegeben. Wirf im Block einen `ValueError` und fange ihn **außerhalb** des Blocks ab. Die Ausgabe ist `Tuer auf`, `Tuer zu` und `Fehler gefangen`.''',
  given="""import asyncio

class Tuer:
    async def __aenter__(self):
        print('Tuer auf')

    async def __aexit__(self, art, fehler, spur):
        print('Tuer zu')
""", body="""try:
    async with Tuer():
        raise ValueError('x')
except ValueError:
    print('Fehler gefangen')""")
t('''Schreibe eine Klasse `Zaehler`, die mit `__aenter__` das Dictionary `daten['offen']` um `1` erhöht und mit `__aexit__` wieder um `1` senkt (`daten` ist vorgegeben).
Gib im Block `daten['offen']` aus, außerhalb des Blocks auch.''',
  given="""import asyncio

daten = {'offen': 0}
""", body="""class Zaehler:
    async def __aenter__(self):
        daten['offen'] += 1

    async def __aexit__(self, art, fehler, spur):
        daten['offen'] -= 1

async with Zaehler():
    print(daten['offen'])
print(daten['offen'])""")
t('''Schreibe eine Klasse `Sitzung(name)`. `__aenter__` gibt `<name> meldet sich an` aus und `__aexit__` gibt `<name> meldet sich ab` aus. Verschachtele zwei `async with`: erst `Sitzung('Ali')`, darin `Sitzung('Bea')`.
Gib im innersten Block `arbeiten` aus.''',
  given='import asyncio\n', body="""class Sitzung:
    def __init__(self, name):
        self.name = name

    async def __aenter__(self):
        print(self.name, 'meldet sich an')

    async def __aexit__(self, art, fehler, spur):
        print(self.name, 'meldet sich ab')

async with Sitzung('Ali'):
    async with Sitzung('Bea'):
        print('arbeiten')""")
task('''Die Verbindung wird von Hand geöffnet und geschlossen. Tritt ein Fehler auf, wird sie **nicht** geschlossen (`schließe` fehlt in der Ausgabe). Schreibe den Code mit `async with` und der Klasse `Verbindung`, sodass sie immer geschlossen wird.''',
     zelle="""import asyncio

class Verbindung:
    async def oeffne(self):
        print('öffne')

    async def schliesse(self):
        print('schließe')

v = Verbindung()
await v.oeffne()
try:
    print('arbeite')
    raise ValueError('kaputt')
    await v.schliesse()
except ValueError:
    print('Fehler gefangen')""",
     solution="""import asyncio

class Verbindung:
    async def __aenter__(self):
        print('öffne')

    async def __aexit__(self, art, fehler, spur):
        print('schließe')

try:
    async with Verbindung():
        print('arbeite')
        raise ValueError('kaputt')
except ValueError:
    print('Fehler gefangen')""")

# ---------------------------------------------------------------- 3
sec('async for und asynchrone Generatoren')
expl('''#### Asynchrone Generatoren

Eine Funktion mit `async def`, in der `yield` steht, ist ein **asynchroner Generator**. `yield wert` liefert einen Wert nach außen und **pausiert** die Funktion an dieser Stelle.
Beim nächsten Wert läuft sie dort weiter. Dazwischen darf gewartet werden (`await`).

Einen solchen Generator liest man mit **`async for`**. Die Schleife wartet jedes Mal auf den nächsten Wert, und währenddessen können andere Coroutinen arbeiten.''',
     """import asyncio

async def messwerte(n):
    for i in range(1, n + 1):
        await asyncio.sleep(0.1)
        yield i * 10

async for wert in messwerte(3):
    print('Messwert:', wert)
print('Fertig')""")
expl('''#### Abbrechen und Listen sammeln

- Mit `break` kann man `async for` vorzeitig verlassen.
- Eine **Listen-Schreibweise** mit `async for` sammelt alle Werte: `[w async for w in generator()]`. Eine Bedingung ist wie gewohnt möglich.
- `await anext(generator)` holt genau **einen** Wert.''',
     """import asyncio

async def messwerte(n):
    for i in range(1, n + 1):
        await asyncio.sleep(0.1)
        yield i * 10

async for wert in messwerte(10):
    if wert > 30:
        break
    print('kleiner als 40:', wert)

alle = [w async for w in messwerte(5)]
print(alle)

grosse = [w async for w in messwerte(5) if w >= 30]
print(grosse)

gen = messwerte(5)
print(await anext(gen))
print(await anext(gen))""")
expl('''#### Zwei `async for` gleichzeitig

Jede Schleife wartet für sich. Läuft jede in einer eigenen Coroutine (oder einem Task), arbeiten sie gleichzeitig. Im Beispiel liefert `A` alle 0,1 Sekunden einen Wert und `B` alle 0,25 Sekunden.''',
     """import asyncio

async def takt(name, pause, n):
    for i in range(1, n + 1):
        await asyncio.sleep(pause)
        yield name + str(i)

async def lies(name, pause, n):
    async for wert in takt(name, pause, n):
        print(wert)

await asyncio.gather(lies('A', 0.1, 3), lies('B', 0.25, 2))""")
expl('''#### Generator mit Queue

Ein asynchroner Generator kann Werte aus einer Queue holen und weitergeben. So wird aus einer Schlange ein bequem lesbarer Datenstrom.
Das Ende-Signal `None` beendet den Generator mit `return`.''',
     """import asyncio

schlange = asyncio.Queue()

async def aus_schlange():
    while True:
        wert = await schlange.get()
        if wert is None:
            return
        yield wert

async def erzeuger():
    for x in ['a', 'b', 'c']:
        await asyncio.sleep(0.1)
        await schlange.put(x)
    await schlange.put(None)

async def verbraucher():
    async for x in aus_schlange():
        print('bekommen:', x)
    print('Ende')

await asyncio.gather(erzeuger(), verbraucher())""")
expl('''#### `@asynccontextmanager` (Leistungsfach)

Statt einer Klasse mit `__aenter__` und `__aexit__` kann man einen Kontextmanager auch mit einem asynchronen Generator schreiben. Der Dekorator `@asynccontextmanager` (aus `contextlib`)
macht daraus einen: Alles **vor** dem `yield` ist das Betreten, alles **danach** das Verlassen. Der Wert hinter `yield` landet hinter `as`.
Ein `try ... finally` um das `yield` sorgt dafür, dass das Aufräumen auch bei Fehlern läuft.

Ein Dekorator ist eine Zeile mit `@` über einer Funktion. Sie verändert, was die Funktion tut.''',
     """import asyncio
from contextlib import asynccontextmanager

@asynccontextmanager
async def labor(name):
    print('öffne', name)
    await asyncio.sleep(0.1)
    try:
        yield name.upper()
    finally:
        print('schließe', name)

async with labor('Chemie') as raum:
    print('arbeite in', raum)""")

predict("""import asyncio

async def gen():
    for i in range(3):
        await asyncio.sleep(0.1)
        yield i

async for x in gen():
    print(x)
print('Ende')""", erklaerung='''`async for` holt die Werte `0`, `1`, `2` nacheinander aus dem Generator. Wenn er fertig ist, endet die Schleife, und `Ende` wird ausgegeben.

```
0
1
2
Ende
```''')
predict("""import asyncio

async def gen():
    for i in range(5):
        await asyncio.sleep(0.1)
        yield i * i

async for x in gen():
    if x > 5:
        break
    print(x)""", erklaerung='''Der Generator liefert `0`, `1`, `4`, `9`, ... Bei `9` ist `x > 5` wahr, und `break` beendet die Schleife. `9` wird nicht ausgegeben.

```
0
1
4
```''')
predict("""import asyncio

async def gen():
    for i in range(4):
        await asyncio.sleep(0.1)
        yield i

print([x async for x in gen() if x % 2 == 0])""", erklaerung='''Der Generator liefert `0`, `1`, `2`, `3`. Die Bedingung `x % 2 == 0` behält nur die geraden Werte.

```
[0, 2]
```''')
predict("""import asyncio

async def gen():
    yield 'a'
    yield 'b'
    yield 'c'

g = gen()
print(await anext(g))
print(await anext(g))
async for x in g:
    print(x)""", erklaerung='''`anext` holt die ersten beiden Werte (`a`, `b`) einzeln. Die Schleife macht beim Rest weiter und gibt nur noch `c` aus.

```
a
b
c
```''')
t('''Schreibe einen asynchronen Generator `zaehle(n)`, der die Zahlen von `1` bis `n` liefert (mit `await asyncio.sleep(0.1)` vor jedem Wert). Gib die Werte für `n = 4` mit `async for` aus.''',
  given='import asyncio\n', body="""async def zaehle(n):
    for i in range(1, n + 1):
        await asyncio.sleep(0.1)
        yield i

async for zahl in zaehle(4):
    print(zahl)""")
t('''Schreibe einen asynchronen Generator `quadrate(zahlen)`, der für jede Zahl der Liste nach `0.1` Sekunden das Quadrat liefert. Gib die Summe der gelieferten Werte aus (mit einer Variablen, die in `async for` erhöht wird).''',
  given='import asyncio\n\nzahlen = [2, 3, 4]\n', body="""async def quadrate(zahlen):
    for z in zahlen:
        await asyncio.sleep(0.1)
        yield z * z

summe = 0
async for q in quadrate(zahlen):
    summe += q
print(summe)""")
t('''Der asynchrone Generator `wetter()` ist vorgegeben. Sammle alle Temperaturen mit der Listen-Schreibweise `[... async for ...]` in `werte` und gib die Liste aus, dann den **Höchstwert** (`max`).''',
  given="""import asyncio

async def wetter():
    for temperatur in [14, 18, 21, 19]:
        await asyncio.sleep(0.1)
        yield temperatur
""", body="""werte = [t async for t in wetter()]
print(werte)
print(max(werte))""")
t('''Der Generator `wetter()` ist vorgegeben. Sammle mit einer Listen-Schreibweise nur die Temperaturen, die **mindestens 20** sind, und gib die Liste aus.''',
  given="""import asyncio

async def wetter():
    for temperatur in [14, 18, 21, 19, 25]:
        await asyncio.sleep(0.1)
        yield temperatur
""", body="""warm = [t async for t in wetter() if t >= 20]
print(warm)""")
t('''Der Generator `sensor()` liefert die Werte `3, 8, 1, 9, 4`. Lies ihn mit `async for` und beende die Schleife mit `break`, sobald ein Wert **größer als 8** kommt. Gib alle Werte vorher aus.''',
  given="""import asyncio

async def sensor():
    for wert in [3, 8, 1, 9, 4]:
        await asyncio.sleep(0.1)
        yield wert
""", body="""async for wert in sensor():
    if wert > 8:
        print('Alarm')
        break
    print(wert)""")
t('''Schreibe einen asynchronen Generator `gerade(n)`, der aus den Zahlen `1` bis `n` nur die **geraden** liefert (mit `await asyncio.sleep(0.1)` vor jeder Zahl). Gib die Werte für `n = 7` aus.''',
  given='import asyncio\n', body="""async def gerade(n):
    for i in range(1, n + 1):
        await asyncio.sleep(0.1)
        if i % 2 == 0:
            yield i

async for zahl in gerade(7):
    print(zahl)""")
t('''Der Generator `buchstaben()` ist vorgegeben (liefert `'x'`, `'y'`, `'z'`). Hole mit `anext()` zwei Werte einzeln und gib sie aus. Gib danach den Rest mit `async for` aus.''',
  given="""import asyncio

async def buchstaben():
    for b in ['x', 'y', 'z']:
        await asyncio.sleep(0.1)
        yield b

g = buchstaben()
""", body="""print(await anext(g))
print(await anext(g))
async for b in g:
    print(b)""")
t('''Der Generator `takt(name, pause, n)` ist vorgegeben. Lies mit zwei Coroutinen (`async for`) gleichzeitig `takt('A', 0.1, 3)` und `takt('B', 0.25, 2)` und gib alle Werte aus. Die Ausgabe zeigt, wie die Werte sich mischen.''',
  given="""import asyncio

async def takt(name, pause, n):
    for i in range(1, n + 1):
        await asyncio.sleep(pause)
        yield name + str(i)
""", body="""async def lies(name, pause, n):
    async for wert in takt(name, pause, n):
        print(wert)

await asyncio.gather(lies('A', 0.1, 3), lies('B', 0.25, 2))""")
t('''Die Schlange `schlange` und der Erzeuger sind vorgegeben. Schreibe einen asynchronen Generator `aus_schlange()`, der Werte aus der Schlange liefert und bei `None` mit `return` endet.
Lies ihn in `verbraucher()` mit `async for` und gib jeden Wert als `bekommen: <wert>` aus.''',
  given="""import asyncio

schlange = asyncio.Queue()

async def erzeuger():
    for x in [10, 20, 30]:
        await asyncio.sleep(0.1)
        await schlange.put(x)
    await schlange.put(None)
""", body="""async def aus_schlange():
    while True:
        wert = await schlange.get()
        if wert is None:
            return
        yield wert

async def verbraucher():
    async for wert in aus_schlange():
        print('bekommen:', wert)

await asyncio.gather(erzeuger(), verbraucher())""")
t('''(Leistungsfach) Schreibe mit `@asynccontextmanager` einen Kontextmanager `sitzung(name)`: Vor dem `yield` wird `<name> beginnt` ausgegeben, nach dem `yield` (in einem `finally`) `<name> endet`.
Benutze ihn mit `async with sitzung('Probe'):` und gib im Block `drin` aus.''',
  given='import asyncio\nfrom contextlib import asynccontextmanager\n', body="""@asynccontextmanager
async def sitzung(name):
    print(name, 'beginnt')
    try:
        yield
    finally:
        print(name, 'endet')

async with sitzung('Probe'):
    print('drin')""")

# ---------------------------------------------------------------- 4
sec('Anwendungen')
expl('''#### Pipeline mit mehreren Stufen

Man kann Queues hintereinander schalten: Eine Stufe holt aus einer Schlange und legt ihr Ergebnis in die nächste. Jede Stufe ist eine eigene Coroutine, alle laufen gleichzeitig.
Das **Ende-Signal** `None` wird von Stufe zu Stufe weitergereicht.

Im Beispiel: Ein Lader liefert Seitennamen, eine Stufe schreibt sie groß, eine dritte gibt sie aus.''',
     """import asyncio

geladen = asyncio.Queue()
bearbeitet = asyncio.Queue()

async def lader():
    for seite in ['start', 'plan', 'mensa']:
        await asyncio.sleep(0.3)
        await geladen.put(seite)
    await geladen.put(None)

async def bearbeiter():
    while True:
        seite = await geladen.get()
        if seite is None:
            await bearbeitet.put(None)
            break
        await asyncio.sleep(0.1)
        await bearbeitet.put(seite.upper())

async def ausgeber():
    while True:
        seite = await bearbeitet.get()
        if seite is None:
            break
        print('Ausgabe:', seite)

await asyncio.gather(lader(), bearbeiter(), ausgeber())""")
expl('''#### Wiederholen mit Pause

Netzwerkaufrufe schlagen manchmal fehl. Dann versucht man es ein paarmal erneut. Die Funktion `unsicher()` scheitert zweimal und klappt beim dritten Versuch.''',
     """import asyncio

zaehler = {'versuche': 0}

async def unsicher():
    zaehler['versuche'] += 1
    await asyncio.sleep(0.1)
    if zaehler['versuche'] < 3:
        raise ConnectionError('keine Verbindung')
    return 'Daten'

async def mit_wiederholung(max_versuche):
    for versuch in range(1, max_versuche + 1):
        try:
            ergebnis = await unsicher()
            print('Versuch', versuch, 'hat geklappt')
            return ergebnis
        except ConnectionError:
            print('Versuch', versuch, 'ist fehlgeschlagen')
            await asyncio.sleep(0.1)
    return None

print(await mit_wiederholung(5))""")
expl('''#### Einfacher Crawler

Ein **Crawler** besucht Seiten und folgt ihren Links. Die zu besuchenden Seiten stehen in einer Queue, mehrere Arbeiter holen sie. Ein Set `besucht` verhindert, dass eine Seite doppelt besucht wird.
Mit `join()` wartet man, bis nichts mehr zu tun ist.''',
     """import asyncio

links = {'start': ['plan', 'mensa'], 'plan': ['start', 'hilfe'], 'mensa': ['hilfe'], 'hilfe': []}
besucht = set()
schlange = asyncio.Queue()

async def arbeiter():
    while True:
        seite = await schlange.get()
        if seite not in besucht:
            besucht.add(seite)
            await asyncio.sleep(0.1)
            for ziel in links[seite]:
                if ziel not in besucht:
                    schlange.put_nowait(ziel)
        schlange.task_done()

schlange.put_nowait('start')
arbeiterliste = []
for i in range(2):
    arbeiterliste.append(asyncio.create_task(arbeiter()))

await schlange.join()
for a in arbeiterliste:
    a.cancel()
await asyncio.gather(*arbeiterliste, return_exceptions=True)
print(sorted(besucht))""")
expl('''#### Hintergrund-Task mit Stopp-Signal

Ein Task kann im Hintergrund etwas Regelmäßiges tun (zum Beispiel einen „Herzschlag“ ausgeben), bis ein `Event` ihn beendet.''',
     """import asyncio

stopp = asyncio.Event()

async def herzschlag():
    while not stopp.is_set():
        print('piep')
        await asyncio.sleep(0.2)
    print('Herzschlag beendet')

hintergrund = asyncio.create_task(herzschlag())
await asyncio.sleep(0.5)
stopp.set()
await hintergrund
print('Hauptprogramm fertig')""")

predict("""import asyncio

a = asyncio.Queue()
b = asyncio.Queue()

async def stufe1():
    for x in [1, 2]:
        await a.put(x)
    await a.put(None)

async def stufe2():
    while True:
        x = await a.get()
        if x is None:
            await b.put(None)
            return
        await b.put(x * 10)

async def stufe3():
    while True:
        x = await b.get()
        if x is None:
            return
        print(x)

await asyncio.gather(stufe1(), stufe2(), stufe3())""", erklaerung='''Stufe 1 legt `1` und `2` ab, Stufe 2 multipliziert mit 10 und reicht weiter, Stufe 3 gibt aus. Das Ende-Signal `None` wandert durch alle Stufen und beendet sie nacheinander.

```
10
20
```''')
predict("""import asyncio

stopp = asyncio.Event()

async def tick():
    n = 0
    while not stopp.is_set():
        n += 1
        await asyncio.sleep(0.1)
    return n

task = asyncio.create_task(tick())
await asyncio.sleep(0.25)
stopp.set()
print(await task)""", erklaerung='''Der Task zählt bei `0` Sekunden (`n = 1`), bei 0,1 (`n = 2`) und bei 0,2 (`n = 3`). Nach 0,25 Sekunden wird das Signal gesetzt, bei der nächsten Prüfung endet die Schleife. `n` ist `3`.

```
3
```''')
t('''Schreibe eine Pipeline mit zwei Stufen: `erzeuger()` legt `1`, `2`, `3` in die Schlange `roh` (am Ende `None`). `verdoppler()` holt aus `roh`, legt das Doppelte in `fertig` und reicht das `None` weiter.
`ausgeber()` gibt die Werte aus `fertig` aus. Starte alle drei gleichzeitig.''',
  given='import asyncio\n\nroh = asyncio.Queue()\nfertig = asyncio.Queue()\n', body="""async def erzeuger():
    for x in [1, 2, 3]:
        await roh.put(x)
    await roh.put(None)

async def verdoppler():
    while True:
        x = await roh.get()
        if x is None:
            await fertig.put(None)
            return
        await fertig.put(x * 2)

async def ausgeber():
    while True:
        x = await fertig.get()
        if x is None:
            return
        print(x)

await asyncio.gather(erzeuger(), verdoppler(), ausgeber())""")
t('''Die Coroutine `unsicher()` ist vorgegeben: Sie scheitert zweimal mit `ConnectionError` und klappt beim dritten Mal. Schreibe `mit_wiederholung(max_versuche)`: Sie versucht es bis zu `max_versuche` Mal
und gibt bei Erfolg `Versuch <nr> hat geklappt` aus und `'Daten'` zurück. Bei einem Fehler gibt sie `Versuch <nr> ist fehlgeschlagen` aus und wartet `0.1` Sekunden. Rufe sie mit `5` auf und gib das Ergebnis aus.''',
  given="""import asyncio

zaehler = {'versuche': 0}

async def unsicher():
    zaehler['versuche'] += 1
    await asyncio.sleep(0.1)
    if zaehler['versuche'] < 3:
        raise ConnectionError('keine Verbindung')
    return 'Daten'
""", body="""async def mit_wiederholung(max_versuche):
    for versuch in range(1, max_versuche + 1):
        try:
            ergebnis = await unsicher()
            print('Versuch', versuch, 'hat geklappt')
            return ergebnis
        except ConnectionError:
            print('Versuch', versuch, 'ist fehlgeschlagen')
            await asyncio.sleep(0.1)
    return None

print(await mit_wiederholung(5))""")
t('''Rufe dieselbe Funktion `unsicher()` mit `mit_wiederholung(2)` auf (nur zwei Versuche). Es klappt nicht. Gib in diesem Fall `Aufgegeben` aus (die Funktion gibt dann `None` zurück). Alles andere ist vorgegeben.''',
  given="""import asyncio

zaehler = {'versuche': 0}

async def unsicher():
    zaehler['versuche'] += 1
    await asyncio.sleep(0.1)
    if zaehler['versuche'] < 3:
        raise ConnectionError('keine Verbindung')
    return 'Daten'

async def mit_wiederholung(max_versuche):
    for versuch in range(1, max_versuche + 1):
        try:
            return await unsicher()
        except ConnectionError:
            await asyncio.sleep(0.1)
    return None
""", body="""ergebnis = await mit_wiederholung(2)
if ergebnis is None:
    print('Aufgegeben')
else:
    print(ergebnis)""")
t('''Ein Crawler besucht Seiten. `links`, `besucht` und die Schlange sind vorgegeben. Schreibe `arbeiter()` (holt eine Seite, besucht sie, falls noch nicht besucht, legt ihre Links ab, ruft `task_done()` auf).
Starte `'start'` mit zwei Arbeitern, warte mit `join()`, brich die Arbeiter ab und gib die **sortierte** Liste der besuchten Seiten aus.''',
  given="""import asyncio

links = {'start': ['a', 'b'], 'a': ['c'], 'b': ['c', 'd'], 'c': [], 'd': ['start']}
besucht = set()
schlange = asyncio.Queue()
""", body="""async def arbeiter():
    while True:
        seite = await schlange.get()
        if seite not in besucht:
            besucht.add(seite)
            await asyncio.sleep(0.1)
            for ziel in links[seite]:
                if ziel not in besucht:
                    schlange.put_nowait(ziel)
        schlange.task_done()

schlange.put_nowait('start')
arbeiterliste = []
for i in range(2):
    arbeiterliste.append(asyncio.create_task(arbeiter()))

await schlange.join()
for a in arbeiterliste:
    a.cancel()
await asyncio.gather(*arbeiterliste, return_exceptions=True)
print(sorted(besucht))""")
t('''Starte als Hintergrund-Task eine Coroutine `herzschlag()`, die in einer Schleife `while not stopp.is_set():` alle `0.2` Sekunden `piep` ausgibt. Das Hauptprogramm wartet `0.5` Sekunden, setzt das `Event` `stopp`,
wartet auf den Task und gibt `Hauptprogramm fertig` aus (dreimal `piep`).''',
  given='import asyncio\n\nstopp = asyncio.Event()\n', body="""async def herzschlag():
    while not stopp.is_set():
        print('piep')
        await asyncio.sleep(0.2)

hintergrund = asyncio.create_task(herzschlag())
await asyncio.sleep(0.5)
stopp.set()
await hintergrund
print('Hauptprogramm fertig')""")
t('''Eine Kasse bedient die Kunden aus der Schlange nacheinander (jeder braucht `0.4` Sekunden). Die Kunden kommen alle `0.15` Sekunden an: `ankunft()` legt `'Ali'`, `'Bea'`, `'Cem'` mit einer Pause von `0.15` Sekunden vor jedem ab
und gibt `<name> kommt` aus (Ende-Signal `None`). `kasse()` gibt `<name> bedient` und nach `0.4` Sekunden `<name> fertig` aus.''',
  given='import asyncio\n\nschlange = asyncio.Queue()\n', body="""async def ankunft():
    for name in ['Ali', 'Bea', 'Cem']:
        await asyncio.sleep(0.15)
        print(name, 'kommt')
        await schlange.put(name)
    await schlange.put(None)

async def kasse():
    while True:
        name = await schlange.get()
        if name is None:
            break
        print(name, 'bedient')
        await asyncio.sleep(0.4)
        print(name, 'fertig')

await asyncio.gather(ankunft(), kasse())""")
t('''Drei Schüler geben Hausaufgaben ab. Jeder Schüler (`abgeben(name)`) braucht eine Sekunde und trägt sich danach in die Liste `abgegeben` ein. Mit einem `Lock` darf immer nur einer am Lehrerpult stehen.
Starte alle drei gleichzeitig und gib die Liste in der Reihenfolge `['Ali', 'Bea', 'Cem']` aus, außerdem die Gesamtdauer (`Dauer: 3 s`).''',
  given='import asyncio\nimport time\n\nabgegeben = []\npult = asyncio.Lock()\n', body="""async def abgeben(name):
    async with pult:
        await asyncio.sleep(1)
        abgegeben.append(name)

start = time.perf_counter()
await asyncio.gather(abgeben('Ali'), abgeben('Bea'), abgeben('Cem'))
print(abgegeben)
print('Dauer:', round(time.perf_counter() - start), 's')""")
t('''Schreibe `hole_mit_zeitlimit(name, dauer)`: Sie wartet `dauer` Sekunden (`asyncio.sleep`) und gibt `<name> ok` zurück, aber höchstens `0.3` Sekunden lang (`wait_for`). Bei Zeitüberschreitung gibt sie `<name> zu langsam` zurück.
Frage `('A', 0.1)`, `('B', 0.6)`, `('C', 0.2)` gleichzeitig ab und gib die Ergebnisse als Liste aus.''',
  given='import asyncio\n', body="""async def hole_mit_zeitlimit(name, dauer):
    try:
        await asyncio.wait_for(asyncio.sleep(dauer), timeout=0.3)
        return name + ' ok'
    except TimeoutError:
        return name + ' zu langsam'

ergebnisse = await asyncio.gather(hole_mit_zeitlimit('A', 0.1), hole_mit_zeitlimit('B', 0.6), hole_mit_zeitlimit('C', 0.2))
print(ergebnisse)""")

# ---------------------------------------------------------------- 5
sec('Future und call_later (Ausblick, Leistungsfach)')
expl('''#### Was ist ein `Future`?

Ein **Future** ist ein Platzhalter für ein Ergebnis, das erst später da ist. Du kennst ihn schon: Ein Task **ist** ein Future (mit einer Coroutine dahinter).
Man kann aber auch einen „leeren“ Future selbst erzeugen und später das Ergebnis eintragen:

- `loop = asyncio.get_running_loop()` holt die laufende Event-Loop.
- `f = loop.create_future()` erzeugt einen leeren Future.
- `f.set_result(wert)` trägt das Ergebnis ein. `f.done()` ist dann `True`.
- `await f` wartet, bis das Ergebnis eingetragen ist, und liefert es.''',
     """import asyncio

loop = asyncio.get_running_loop()
f = loop.create_future()
print(f.done())
f.set_result(42)
print(f.done())
print(await f)""")
expl('''#### Wer trägt das Ergebnis ein?

Meist trägt jemand anderes das Ergebnis ein, als der, der wartet. Hier wartet das Hauptprogramm, während eine andere Coroutine nach 0,2 Sekunden die Antwort einträgt.

Auch einen Fehler kann man eintragen: `f.set_exception(fehler)`. Dann wirft `await f` diesen Fehler.''',
     """import asyncio

loop = asyncio.get_running_loop()
antwort = loop.create_future()

async def server():
    await asyncio.sleep(0.2)
    antwort.set_result('Hallo Client')

asyncio.create_task(server())
print('Client wartet')
print(await antwort)""")
expl('''#### `call_later()`

`loop.call_later(sekunden, funktion, argumente...)` ruft eine **normale** Funktion (keine Coroutine) nach der angegebenen Zeit auf. Man kann damit zum Beispiel einen Future später fertig machen.''',
     """import asyncio

loop = asyncio.get_running_loop()
f = loop.create_future()
loop.call_later(0.2, f.set_result, 'Zeit ist um')
print('Warte ...')
print(await f)

loop.call_later(0.1, print, 'Piep!')
await asyncio.sleep(0.3)
aufgabe = asyncio.create_task(asyncio.sleep(0))
print(isinstance(aufgabe, asyncio.Future))
await aufgabe""")

predict("""import asyncio

loop = asyncio.get_running_loop()
f = loop.create_future()

async def sag():
    await asyncio.sleep(0.1)
    f.set_result('x')

asyncio.create_task(sag())
print(f.done())
print(await f)
print(f.done())""", erklaerung='''Am Anfang ist der Future leer (`False`). `await f` wartet, bis `sag()` das Ergebnis `x` einträgt. Danach ist er fertig (`True`).

```
False
x
True
```''')
predict("""import asyncio

loop = asyncio.get_running_loop()
f = loop.create_future()
f.set_exception(ValueError('kaputt'))
try:
    await f
except ValueError as e:
    print('Fehler:', e)""", erklaerung='''Ein Future kann auch mit einem Fehler fertig werden. `await f` wirft dann diesen Fehler, hier den `ValueError` mit dem Text `kaputt`.

```
Fehler: kaputt
```''')
t('''Erzeuge mit `loop.create_future()` einen Future `f`. Gib `f.done()` aus (`False`), trage mit `set_result` den Wert `'fertig'` ein, gib `f.done()` noch einmal aus (`True`) und gib `await f` aus.''',
  given='import asyncio\n\nloop = asyncio.get_running_loop()\n', body="""f = loop.create_future()
print(f.done())
f.set_result('fertig')
print(f.done())
print(await f)""")
t('''Die Coroutine `lade()` ist vorgegeben und trägt nach `0.2` Sekunden das Ergebnis `'Stundenplan'` in den Future `ergebnis` ein. Starte sie als Task, gib `Warte auf Ergebnis` aus
und danach das Ergebnis (`await ergebnis`).''',
  given="""import asyncio

loop = asyncio.get_running_loop()
ergebnis = loop.create_future()

async def lade():
    await asyncio.sleep(0.2)
    ergebnis.set_result('Stundenplan')
""", body="""asyncio.create_task(lade())
print('Warte auf Ergebnis')
print(await ergebnis)""")
t('''Benutze `loop.call_later(0.2, f.set_result, 'Gong')`, um den Future `f` nach `0.2` Sekunden fertig zu machen. Gib `Warte auf den Gong` aus und danach den Wert von `await f`.''',
  given='import asyncio\n\nloop = asyncio.get_running_loop()\nf = loop.create_future()\n', body="""loop.call_later(0.2, f.set_result, 'Gong')
print('Warte auf den Gong')
print(await f)""")
t('''Trage mit `set_exception` den Fehler `KeyError('fehlt')` in den Future `f` ein. Fange den Fehler beim `await f` ab und gib `Fehler: KeyError` aus (mit `type(e).__name__`).''',
  given='import asyncio\n\nloop = asyncio.get_running_loop()\nf = loop.create_future()\n', body="""f.set_exception(KeyError('fehlt'))
try:
    await f
except KeyError as e:
    print('Fehler:', type(e).__name__)""")
t('''Zwei Futures `a` und `b` werden nach `0.3` und `0.1` Sekunden mit `call_later` gefüllt (`'A'` und `'B'`). Warte mit `gather` auf beide und gib die Ergebnisliste aus (`['A', 'B']`).''',
  given='import asyncio\n\nloop = asyncio.get_running_loop()\na = loop.create_future()\nb = loop.create_future()\n', body="""loop.call_later(0.3, a.set_result, 'A')
loop.call_later(0.1, b.set_result, 'B')
print(await asyncio.gather(a, b))""")

# ---------------------------------------------------------------- 6
sec('Gemischte Übungen')
t('''Ein Erzeuger legt die Wörter `['Schule', 'Pause', 'Mathe']` ab (am Ende `None`). Zwei Verbraucher (`leser(nr)`) holen Wörter, warten `0.2` Sekunden und sammeln die Länge in `laengen`.
Jeder Verbraucher braucht sein eigenes Ende-Signal. Gib am Ende `sorted(laengen)` aus.''',
  given='import asyncio\n\nschlange = asyncio.Queue()\nlaengen = []\n', body="""async def erzeuger():
    for wort in ['Schule', 'Pause', 'Mathe']:
        await schlange.put(wort)
    await schlange.put(None)
    await schlange.put(None)

async def leser(nr):
    while True:
        wort = await schlange.get()
        if wort is None:
            break
        await asyncio.sleep(0.2)
        laengen.append(len(wort))

await asyncio.gather(erzeuger(), leser(1), leser(2))
print(sorted(laengen))""")
t('''Der asynchrone Generator `ticker(n)` liefert nach je `0.1` Sekunden die Zahlen `1` bis `n`. Schreibe eine Coroutine `summe(n)`, die alle gelieferten Zahlen mit `async for` addiert und die Summe **zurückgibt**.
Gib `await summe(5)` aus.''',
  given="""import asyncio

async def ticker(n):
    for i in range(1, n + 1):
        await asyncio.sleep(0.1)
        yield i
""", body="""async def summe(n):
    ergebnis = 0
    async for zahl in ticker(n):
        ergebnis += zahl
    return ergebnis

print(await summe(5))""")
t('''Schreibe eine Klasse `Messung` als `async with`-Objekt, die beim Betreten `Messung startet` ausgibt und beim Verlassen `Messung beendet`.
Führe darin zwei `gather`-Aufgaben `messe(1)` und `messe(2)` aus (jede wartet `0.2` Sekunden und gibt `Sensor <nr> fertig` aus).''',
  given='import asyncio\n\nasync def messe(nr):\n    await asyncio.sleep(0.2)\n    print(\'Sensor\', nr, \'fertig\')\n', body="""class Messung:
    async def __aenter__(self):
        print('Messung startet')

    async def __aexit__(self, art, fehler, spur):
        print('Messung beendet')

async with Messung():
    await asyncio.gather(messe(1), messe(2))""")
t('''Vier Arbeiter-Tasks holen aus einer Schlange mit den Zahlen `1` bis `8` und tragen `zahl + 100` in die Liste `ergebnisse` ein (nach `0.1` Sekunden, mit `task_done()`).
Nach `join()` brichst du die Arbeiter ab und gibst die sortierte Liste und die Dauer aus (`Dauer: 0 s`, weil acht Aufgaben auf vier Arbeiter nur etwa `0.2` Sekunden dauern).''',
  given="""import asyncio
import time

schlange = asyncio.Queue()
for zahl in range(1, 9):
    schlange.put_nowait(zahl)
ergebnisse = []
""", body="""async def arbeiter():
    while True:
        zahl = await schlange.get()
        await asyncio.sleep(0.1)
        ergebnisse.append(zahl + 100)
        schlange.task_done()

start = time.perf_counter()
arbeiterliste = []
for i in range(4):
    arbeiterliste.append(asyncio.create_task(arbeiter()))
await schlange.join()
for a in arbeiterliste:
    a.cancel()
await asyncio.gather(*arbeiterliste, return_exceptions=True)
print(sorted(ergebnisse))
print('Dauer:', round(time.perf_counter() - start), 's')""")
t('''Die Kantine hat zwei Kassen (`Semaphore(2)`) und fünf Schüler, die unterschiedlich lange zum Bezahlen brauchen (`bezahle(name, dauer)`). Starte alle fünf gleichzeitig und gib nach jedem Bezahlen `<name> hat bezahlt` aus.
Die Dauer steht in der Liste `schueler` (in Sekunden). Gib am Ende die gerundete Gesamtdauer aus (`Dauer: 1 s`).''',
  given="""import asyncio
import time

kassen = asyncio.Semaphore(2)
schueler = [('Ali', 0.2), ('Bea', 0.5), ('Cem', 0.4), ('Dana', 0.2), ('Emil', 0.3)]
""", body="""async def bezahle(name, dauer):
    async with kassen:
        await asyncio.sleep(dauer)
        print(name, 'hat bezahlt')

start = time.perf_counter()
aufgaben = []
for name, dauer in schueler:
    aufgaben.append(bezahle(name, dauer))
await asyncio.gather(*aufgaben)
print('Dauer:', round(time.perf_counter() - start), 's')""")
predict("""import asyncio

q = asyncio.Queue()

async def a():
    for x in [1, 2, 3]:
        await q.put(x)
    await q.put(None)

async def b():
    async def quelle():
        while True:
            x = await q.get()
            if x is None:
                return
            yield x * x
    async for y in quelle():
        print(y)

await asyncio.gather(a(), b())""", erklaerung='''`quelle` ist ein asynchroner Generator innerhalb von `b`, der Werte aus der Schlange liefert und quadriert. `async for` gibt die Quadrate der Reihe nach aus. Bei `None` endet der Generator mit `return`.

```
1
4
9
```''')
predict("""import asyncio

class K:
    def __init__(self, n):
        self.n = n

    async def __aenter__(self):
        print('+', self.n)
        return self

    async def __aexit__(self, art, fehler, spur):
        print('-', self.n)

async with K(1) as a:
    async with K(2) as b:
        print(a.n + b.n)""", erklaerung='''Beim Betreten läuft `__aenter__` von außen nach innen (`+ 1`, `+ 2`). Im Block steht die Summe `3`. Beim Verlassen läuft `__aexit__` von innen nach außen (`- 2`, `- 1`).

```
+ 1
+ 2
3
- 2
- 1
```''')

generate('asyncio_anwendungen', 'asyncio 4: Anwendungen', intro=INTRO, ausfuehren=AUSFUEHREN)
