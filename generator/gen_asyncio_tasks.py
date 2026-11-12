# Erzeugt ../content/asyncio_tasks.ipynb (siehe nbgen.py). Zweites Notebook der asyncio-Reihe (asynchilfe.py, asyncnb.py).
# Regeln wie in gen_asyncio_grundlagen.py: Zeiten nur ganzzahlig mit round(), Reihenfolgen nur bei Wartezeiten, die sich um mindestens
# 0.1 s unterscheiden (oder mit asyncio.sleep(0)). Nie ein Task-Objekt ausgeben (repr enthält Adressen), nie Fehlertexte von ZeroDivisionError.
# Tasks, die am Ende einer Zelle noch laufen, bricht der Generator ab (im Notebook liefen sie weiter): nicht darauf bauen.
from nbgen import sec, expl, task, predict, generate
from asynchilfe import t, reihe, AUSFUEHREN
import asyncio

INTRO = f'''In diesem Notebook lernst du, wie man mehrere Aufgaben **gleichzeitig** laufen lässt und ihre Ergebnisse einsammelt:
mit **Tasks** (`create_task()`), genauer mit `gather()`, mit `as_completed()` und `wait()` und mit der `TaskGroup`.

Die Reihe besteht aus vier Notebooks:

{reihe('asyncio_tasks')}

Du solltest das Notebook **asyncio_grundlagen** kennen: `async def`, `await`, `asyncio.sleep()`, `gather()` und `await` direkt in einer Notebook-Zelle.
Fehler abfangen mit `try` und `except` brauchst du ebenfalls.

Gemessene Zeiten sind nie ganz genau. Deshalb runden wir sie mit `round()` auf ganze Sekunden.

Jeder Abschnitt beginnt mit kurzen Erklärungen und Beispielen. Führe die Beispiele aus und probiere sie ruhig ein wenig aus.
Danach folgen viele kleine Übungen. Wenn etwas vorgegeben ist, steht es schon in der Codezelle.'''

# ---------------------------------------------------------------- 1
sec('Tasks mit create_task()')
expl('''#### Coroutine und Task

Eine Coroutine läuft erst, wenn man sie mit `await` aufruft, und der Aufrufer wartet dabei, bis sie fertig ist.

Ein **Task** ist eine Coroutine, die schon bei der Event-Loop **angemeldet** ist und „im Hintergrund“ läuft. Man erzeugt ihn mit `asyncio.create_task(coroutine)`.
Der Aufruf kehrt sofort zurück. Der Task beginnt, sobald die Loop wieder dran ist, also bei dem nächsten `await` im Code, der ihn gestartet hat.

Mit `await task` wartet man später darauf, dass er fertig ist, und erhält seinen Rückgabewert.''',
     """import asyncio

async def sag(text):
    print(text)

t1 = asyncio.create_task(sag('Hallo aus dem Task'))
print('Task wurde erzeugt')
await t1
print('Task ist fertig')""")
expl('''#### Inzwischen etwas anderes tun

Der Vorteil: Während der Task wartet, kann der Code, der ihn gestartet hat, etwas anderes tun.
Hier lädt der Task die Startseite (2 Sekunden), und das Hauptprogramm arbeitet währenddessen weiter.''',
     """import asyncio

async def lade(seite, dauer):
    print('Lade', seite)
    await asyncio.sleep(dauer)
    print('Fertig:', seite)
    return len(seite)

aufgabe = asyncio.create_task(lade('Startseite', 1))
print('Ich mache inzwischen etwas anderes')
await asyncio.sleep(0.5)
print('Ich bin mit dem anderen fertig')
laenge = await aufgabe
print('Ergebnis:', laenge)""")
expl('''#### Zwei Tasks gleichzeitig

Erzeugt man **beide** Tasks, bevor man auf einen wartet, laufen sie gleichzeitig. Die Gesamtdauer ist die längere der beiden Zeiten.
Wichtig ist die Reihenfolge: **erst alle Tasks erzeugen, dann warten.**''',
     """import asyncio
import time

async def lade(seite):
    await asyncio.sleep(1)
    return len(seite)

start = time.perf_counter()
t1 = asyncio.create_task(lade('Start'))
t2 = asyncio.create_task(lade('Stundenplan'))
a = await t1
b = await t2
print('Längen:', a, b)
print('Dauer:', round(time.perf_counter() - start), 's')""")
expl('''#### Viele Tasks in einer Liste

Mit einer Schleife erzeugt man beliebig viele Tasks und merkt sie sich in einer Liste. In einer zweiten Schleife wartet man auf alle.

Es ist wichtig, den Task in einer **Variablen** zu behalten. Sonst kann Python ihn aufräumen, bevor er fertig ist.''',
     """import asyncio

async def verdopple(x):
    await asyncio.sleep(0.2)
    return x * 2

tasks = []
for zahl in [1, 2, 3, 4]:
    tasks.append(asyncio.create_task(verdopple(zahl)))

for aufgabe in tasks:
    print(await aufgabe)""")
expl('''#### Überblick

| Schreibweise | Was passiert |
|---|---|
| `await coroutine()` | startet sie und wartet sofort bis zum Ende (nacheinander) |
| `task = create_task(coroutine())` | meldet sie an und macht sofort weiter; `await task` wartet später |
| `await gather(c1, c2, c3)` | meldet alle an und wartet, bis alle fertig sind |

`gather()` macht aus den Coroutinen intern selbst Tasks.''', None)

predict("""import asyncio

async def sag(text):
    print(text)

task = asyncio.create_task(sag('Task'))
print('A')
await task
print('B')""", erklaerung='''`create_task` startet den Task noch nicht sofort. Der Code läuft weiter und gibt `A` aus. Erst bei `await task` kommt die Loop zum Task, er gibt `Task` aus.
Danach folgt `B`.

```
A
Task
B
```''')
predict("""import asyncio

async def sag(text):
    print(text)

task = asyncio.create_task(sag('Task'))
print('A')
await asyncio.sleep(0)
print('B')""", erklaerung='''`await asyncio.sleep(0)` gibt die Kontrolle ab. Die Loop lässt den Task laufen, der `Task` ausgibt. Erst dann geht es mit `B` weiter.
Der Task ist ohne `await task` trotzdem fertig geworden.

```
A
Task
B
```''')
predict("""import asyncio
import time

async def warte(text):
    await asyncio.sleep(1)
    print(text)

start = time.perf_counter()
t1 = asyncio.create_task(warte('x'))
t2 = asyncio.create_task(warte('y'))
await t1
await t2
print(round(time.perf_counter() - start))""", erklaerung='''Beide Tasks sind schon angemeldet, bevor das erste `await` kommt. Sie warten deshalb gleichzeitig, zusammen nur 1 Sekunde.
`x` wurde zuerst gestartet und ist zuerst fertig.

```
x
y
1
```''')
predict("""import asyncio

async def f(x):
    await asyncio.sleep(0.1)
    return x + 1

t1 = asyncio.create_task(f(1))
t2 = asyncio.create_task(f(10))
print(await t2)
print(await t1)""", erklaerung='''Man darf die Tasks in beliebiger Reihenfolge abholen. `await t2` liefert `11`. `t1` ist inzwischen auch fertig, `await t1` liefert sofort `2`.

```
11
2
```''')
t('''Schreibe eine Coroutine `hallo()`, die `Hallo aus dem Task` ausgibt. Erzeuge daraus mit `create_task` einen Task, gib `Task erzeugt` aus und warte dann mit `await` auf den Task.''',
  given='import asyncio\n', body="""async def hallo():
    print('Hallo aus dem Task')

aufgabe = asyncio.create_task(hallo())
print('Task erzeugt')
await aufgabe""")
t('''Die Coroutine `kaffee()` ist vorgegeben. Starte sie als Task, gib danach `Tisch wird gedeckt` aus und warte dann auf den Task.
So deckt man den Tisch, während der Kaffee kocht.''',
  given="""import asyncio

async def kaffee():
    print('Kaffee wird gekocht')
    await asyncio.sleep(0.2)
    print('Kaffee ist fertig')
""", body="""aufgabe = asyncio.create_task(kaffee())
print('Tisch wird gedeckt')
await aufgabe""")
t('''Die Coroutine `lade(seite)` ist vorgegeben (eine Sekunde). Starte `'Start'` und `'Mensa'` als zwei Tasks, warte danach auf beide und gib die Summe ihrer Rückgabewerte aus
sowie die Dauer.''',
  given="""import asyncio
import time

async def lade(seite):
    await asyncio.sleep(1)
    return len(seite)
""", body="""start = time.perf_counter()
t1 = asyncio.create_task(lade('Start'))
t2 = asyncio.create_task(lade('Mensa'))
a = await t1
b = await t2
print('Summe:', a + b)
print('Dauer:', round(time.perf_counter() - start), 's')""")
t('''Die Coroutine `quadrat(z)` ist vorgegeben. Erzeuge in einer Schleife für alle Zahlen der Liste einen Task und merke sie dir in der Liste `tasks`.
Gib danach in einer zweiten Schleife die Ergebnisse aus (ein Ergebnis pro Zeile).''',
  given="""import asyncio

async def quadrat(z):
    await asyncio.sleep(0.1)
    return z * z

zahlen = [2, 3, 4, 5]
""", body="""tasks = []
for z in zahlen:
    tasks.append(asyncio.create_task(quadrat(z)))

for aufgabe in tasks:
    print(await aufgabe)""")
t('''Die Coroutine `warte_und_sag(text, dauer)` ist vorgegeben. Starte `('lang', 0.3)` und `('kurz', 0.1)` als Tasks und gib mit `print('Beide laufen')` dazwischen
Bescheid. Warte danach auf beide Tasks.''',
  given="""import asyncio

async def warte_und_sag(text, dauer):
    await asyncio.sleep(dauer)
    print(text)
""", body="""t1 = asyncio.create_task(warte_und_sag('lang', 0.3))
t2 = asyncio.create_task(warte_und_sag('kurz', 0.1))
print('Beide laufen')
await t1
await t2""")
t('''Schreibe eine Coroutine `zaehle(name)`, die `<name> 1`, `<name> 2` und `<name> 3` ausgibt (mit `await asyncio.sleep(0)` nach jeder Ausgabe).
Starte `'A'` und `'B'` als Tasks und warte auf beide.''',
  given='import asyncio\n', body="""async def zaehle(name):
    for i in range(1, 4):
        print(name, i)
        await asyncio.sleep(0)

t1 = asyncio.create_task(zaehle('A'))
t2 = asyncio.create_task(zaehle('B'))
await t1
await t2""")
task('''Die drei Seiten werden nacheinander geladen (drei Sekunden). Verbessere den Code mit `create_task`, sodass sie gleichzeitig laden (Dauer: `1`).''',
     zelle="""import asyncio
import time

async def lade(seite):
    await asyncio.sleep(1)
    print('Geladen:', seite)

start = time.perf_counter()
await lade('A')
await lade('B')
await lade('C')
print('Dauer:', round(time.perf_counter() - start), 's')""",
     solution="""import asyncio
import time

async def lade(seite):
    await asyncio.sleep(1)
    print('Geladen:', seite)

start = time.perf_counter()
t1 = asyncio.create_task(lade('A'))
t2 = asyncio.create_task(lade('B'))
t3 = asyncio.create_task(lade('C'))
await t1
await t2
await t3
print('Dauer:', round(time.perf_counter() - start), 's')""")
task('''Die Tasks werden hier erst erzeugt und gleich abgewartet, deshalb laufen sie nacheinander (Dauer: `2`). Verbessere den Code so, dass beide Tasks gleichzeitig laufen (Dauer: `1`).''',
     zelle="""import asyncio
import time

async def arbeite(name):
    await asyncio.sleep(1)
    return name

start = time.perf_counter()
a = await asyncio.create_task(arbeite('x'))
b = await asyncio.create_task(arbeite('y'))
print(a, b)
print('Dauer:', round(time.perf_counter() - start), 's')""",
     solution="""import asyncio
import time

async def arbeite(name):
    await asyncio.sleep(1)
    return name

start = time.perf_counter()
t1 = asyncio.create_task(arbeite('x'))
t2 = asyncio.create_task(arbeite('y'))
a = await t1
b = await t2
print(a, b)
print('Dauer:', round(time.perf_counter() - start), 's')""")

# ---------------------------------------------------------------- 2
sec('Zustand und Ergebnis eines Tasks')
expl('''#### `done()` und `result()`

Ein Task hat Methoden, die seinen Zustand verraten:

- `task.done()` ist `True`, wenn der Task fertig ist (erfolgreich oder mit Fehler), sonst `False`.
- `task.result()` gibt den Rückgabewert zurück. Das geht erst, wenn der Task fertig ist.''',
     """import asyncio

async def quadrat(zahl):
    await asyncio.sleep(0.2)
    return zahl * zahl

aufgabe = asyncio.create_task(quadrat(6))
print('fertig?', aufgabe.done())
await aufgabe
print('fertig?', aufgabe.done())
print('Ergebnis:', aufgabe.result())""")
expl('''#### Fehler: `result()` zu früh

Ruft man `result()` auf, bevor der Task fertig ist, gibt es einen `asyncio.InvalidStateError`.''',
     """import asyncio

async def quadrat(zahl):
    await asyncio.sleep(0.2)
    return zahl * zahl

aufgabe = asyncio.create_task(quadrat(6))
print(aufgabe.result())""", error=asyncio.InvalidStateError)
expl('''#### Namen für Tasks

Jeder Task kann einen Namen haben: `asyncio.create_task(coroutine, name='lader')`. Mit `task.get_name()` liest man ihn wieder aus.
Das ist praktisch, wenn man viele Tasks verwaltet.''',
     """import asyncio

async def lade(seite):
    await asyncio.sleep(0.1)
    return len(seite)

tasks = []
for seite in ['Start', 'Plan']:
    tasks.append(asyncio.create_task(lade(seite), name='lade-' + seite))

for aufgabe in tasks:
    ergebnis = await aufgabe
    print(aufgabe.get_name(), ergebnis)""")
expl('''#### Fehler in einem Task

Wirft die Coroutine eines Tasks einen Fehler, dann steckt dieser im Task. Man bekommt ihn, wenn man auf den Task wartet (`await task`).
Dort kann man ihn wie gewohnt mit `try` und `except` abfangen.''',
     """import asyncio

async def teile(a, b):
    await asyncio.sleep(0.1)
    return a / b

aufgabe = asyncio.create_task(teile(1, 0))
try:
    await aufgabe
except ZeroDivisionError:
    print('Durch null geteilt')
print('fertig?', aufgabe.done())""")
expl('''#### Warten, bis ein Task fertig ist

Mit einer Schleife kann man `done()` immer wieder prüfen und dazwischen mit `await asyncio.sleep()` anderen Tasks Zeit lassen.
Im Beispiel braucht der Task 0,25 Sekunden. Die Schleife prüft alle 0,1 Sekunden.''',
     """import asyncio

async def arbeit():
    await asyncio.sleep(0.25)
    return 'ok'

aufgabe = asyncio.create_task(arbeit())
while not aufgabe.done():
    print('noch nicht fertig')
    await asyncio.sleep(0.1)
print('Ergebnis:', aufgabe.result())""")

predict("""import asyncio

async def f():
    return 5

aufgabe = asyncio.create_task(f())
print(aufgabe.done())
await asyncio.sleep(0)
print(aufgabe.done())
print(aufgabe.result())""", erklaerung='''Direkt nach `create_task` ist der Task noch nicht gelaufen: `False`. Nach `await asyncio.sleep(0)` hat die Loop ihn ausgeführt: `True`. Dann liefert `result()` den Wert `5`.

```
False
True
5
```''')
predict("""import asyncio

async def f(x):
    await asyncio.sleep(0.1)
    return x

t1 = asyncio.create_task(f('a'))
t2 = asyncio.create_task(f('b'))
await t1
print(t1.done(), t2.done())
await t2
print(t2.result())""", erklaerung='''Beide Tasks warten gleichzeitig 0,1 Sekunden. Wenn `await t1` zurückkehrt, ist `t2` auch schon fertig (es war direkt nach `t1` dran).

```
True True
b
```''')
t('''Die Coroutine `quadrat(z)` ist vorgegeben. Starte einen Task für `9` und gib `fertig? False` aus, solange er noch nicht gelaufen ist.
Warte dann auf den Task und gib `fertig? True` und `Ergebnis: 81` aus (mit `done()` und `result()`).''',
  given="""import asyncio

async def quadrat(z):
    await asyncio.sleep(0.1)
    return z * z
""", body="""aufgabe = asyncio.create_task(quadrat(9))
print('fertig?', aufgabe.done())
await aufgabe
print('fertig?', aufgabe.done())
print('Ergebnis:', aufgabe.result())""")
t('''Die Coroutine `lade(seite)` ist vorgegeben. Starte Tasks für `'Start'`, `'Plan'` und `'Mensa'` mit den Namen `'t-Start'`, `'t-Plan'` und `'t-Mensa'`
(Name = `'t-' + seite`). Gib für jeden Task `<Name>: <Ergebnis>` aus.''',
  given="""import asyncio

async def lade(seite):
    await asyncio.sleep(0.1)
    return len(seite)
""", body="""tasks = []
for seite in ['Start', 'Plan', 'Mensa']:
    tasks.append(asyncio.create_task(lade(seite), name='t-' + seite))

for aufgabe in tasks:
    ergebnis = await aufgabe
    print(f'{aufgabe.get_name()}: {ergebnis}')""")
t('''Die Coroutine `teile(a, b)` ist vorgegeben. Starte einen Task für `teile(10, 0)`. Fange den Fehler beim Warten ab und gib in diesem Fall `Geht nicht` aus.''',
  given="""import asyncio

async def teile(a, b):
    await asyncio.sleep(0.1)
    return a / b
""", body="""aufgabe = asyncio.create_task(teile(10, 0))
try:
    print(await aufgabe)
except ZeroDivisionError:
    print('Geht nicht')""")
t('''Die Coroutine `hole(name)` ist vorgegeben und wirft einen `KeyError`, wenn der Name fehlt. Starte Tasks für `'Ali'`, `'Zoe'` und `'Bea'`.
Warte in einer Schleife auf jeden Task. Gib den Wert aus oder, falls es einen `KeyError` gab, `<name>: unbekannt`.''',
  given="""import asyncio

punkte = {'Ali': 12, 'Bea': 17}

async def hole(name):
    await asyncio.sleep(0.1)
    return punkte[name]

namen = ['Ali', 'Zoe', 'Bea']
""", body="""tasks = []
for name in namen:
    tasks.append(asyncio.create_task(hole(name)))

for i in range(len(namen)):
    try:
        print(namen[i], await tasks[i])
    except KeyError:
        print(namen[i], 'unbekannt')""")
t('''Die Coroutine `arbeit()` ist vorgegeben. Starte sie als Task und gib in einer Schleife `Warte ...` aus, solange der Task nicht fertig ist (`done()`), mit `await asyncio.sleep(0.1)` dazwischen.
Gib danach das Ergebnis aus. Die Schleife läuft dreimal.''',
  given="""import asyncio

async def arbeit():
    await asyncio.sleep(0.25)
    return 'Fertig!'
""", body="""aufgabe = asyncio.create_task(arbeit())
while not aufgabe.done():
    print('Warte ...')
    await asyncio.sleep(0.1)
print(aufgabe.result())""")
t('''Die Coroutine `lade(seite, dauer)` ist vorgegeben. Starte `('A', 0.3)` und `('B', 0.1)` als Tasks. Warte erst `0.2` Sekunden mit `asyncio.sleep(0.2)`
und gib dann für jeden Task `<Name> fertig: <True/False>` aus (mit `done()`).''',
  given="""import asyncio

async def lade(seite, dauer):
    await asyncio.sleep(dauer)
    return seite
""", body="""t1 = asyncio.create_task(lade('A', 0.3))
t2 = asyncio.create_task(lade('B', 0.1))
await asyncio.sleep(0.2)
print('A fertig:', t1.done())
print('B fertig:', t2.done())
await t1""")

# ---------------------------------------------------------------- 3
sec('gather() genauer')
expl('''#### Wiederholung: `gather()`

`await asyncio.gather(c1, c2, ...)` führt Coroutinen (oder Tasks) gleichzeitig aus und gibt die Ergebnisse als **Liste in der Reihenfolge der Argumente** zurück.
Mit `gather(*liste)` übergibt man eine ganze Liste.''',
     """import asyncio

async def lade(seite, dauer):
    await asyncio.sleep(dauer)
    return seite.upper()

aufgaben = []
for seite, dauer in [('start', 0.3), ('plan', 0.1), ('mensa', 0.2)]:
    aufgaben.append(lade(seite, dauer))

ergebnisse = await asyncio.gather(*aufgaben)
print(ergebnisse)""")
expl('''#### Wenn eine Aufgabe einen Fehler hat

Wirft eine der Aufgaben einen Fehler, wirft `await asyncio.gather(...)` diesen Fehler an die Stelle des `await`. Man fängt ihn mit `try` und `except` ab.
Die Ergebnisse der anderen Aufgaben bekommt man dann nicht.''',
     """import asyncio

async def teile(a, b):
    await asyncio.sleep(0.1)
    return a / b

try:
    ergebnisse = await asyncio.gather(teile(10, 2), teile(1, 0), teile(9, 3))
    print(ergebnisse)
except ZeroDivisionError:
    print('Eine Division ging schief')""")
expl('''#### `return_exceptions=True`

Mit `gather(..., return_exceptions=True)` bricht `gather` bei einem Fehler **nicht** ab. Stattdessen steht in der Ergebnisliste an der Stelle der fehlerhaften Aufgabe das **Fehlerobjekt**.
Mit `isinstance(wert, Exception)` erkennt man, ob ein Eintrag ein Fehler ist. Den Namen des Fehlertyps liefert `type(wert).__name__`.''',
     """import asyncio

async def teile(a, b):
    await asyncio.sleep(0.1)
    return a / b

ergebnisse = await asyncio.gather(teile(10, 2), teile(1, 0), teile(9, 3), return_exceptions=True)
for ergebnis in ergebnisse:
    if isinstance(ergebnis, Exception):
        print('Fehler:', type(ergebnis).__name__)
    else:
        print('Ergebnis:', ergebnis)""")
expl('''#### Tasks an `gather()` übergeben

`gather` akzeptiert auch fertige Tasks. Das ist nützlich, wenn man die Tasks zwischendurch noch für etwas anderes braucht (zum Beispiel `done()`).''',
     """import asyncio

async def lade(seite):
    await asyncio.sleep(0.1)
    return seite

t1 = asyncio.create_task(lade('A'))
t2 = asyncio.create_task(lade('B'))
ergebnisse = await asyncio.gather(t1, t2)
print(ergebnisse)
print(t1.done(), t2.done())""")

predict("""import asyncio

async def f(x):
    await asyncio.sleep(0.1)
    if x == 2:
        raise ValueError('zwei')
    return x

ergebnisse = await asyncio.gather(f(1), f(2), f(3), return_exceptions=True)
print(len(ergebnisse))
print(ergebnisse[0], ergebnisse[2])
print(type(ergebnisse[1]).__name__)""", erklaerung='''Mit `return_exceptions=True` wirft `gather` keinen Fehler. Die Liste hat drei Einträge: `1`, den `ValueError` (statt eines Ergebnisses) und `3`.

```
3
1 3
ValueError
```''')
predict("""import asyncio

async def f(x):
    await asyncio.sleep(0.1)
    if x == 2:
        raise ValueError('zwei')
    return x

try:
    ergebnisse = await asyncio.gather(f(1), f(2), f(3))
    print('Ergebnisse:', ergebnisse)
except ValueError as e:
    print('Fehler:', e)""", erklaerung='''Ohne `return_exceptions` wirft `gather` den Fehler der zweiten Aufgabe. Die `print`-Zeile im `try`-Block wird nie erreicht. Der Text des Fehlers ist `zwei`.

```
Fehler: zwei
```''')
t('''Die Coroutine `laenge(wort)` ist vorgegeben. Hole mit `gather(*aufgaben)` die Längen aller Wörter der Liste `woerter` (die Coroutinen erzeugst du in einer Schleife) und gib die **größte** Länge aus (`max()`).''',
  given="""import asyncio

async def laenge(wort):
    await asyncio.sleep(0.1)
    return len(wort)

woerter = ['Schule', 'Pause', 'Informatik', 'Kunst']
""", body="""aufgaben = []
for wort in woerter:
    aufgaben.append(laenge(wort))
ergebnisse = await asyncio.gather(*aufgaben)
print(max(ergebnisse))""")
t('''Die Coroutine `teile(a, b)` ist vorgegeben. Berechne mit `gather` die Aufgaben `teile(8, 2)`, `teile(5, 0)` und `teile(9, 3)`. Fange die Fehler mit `try` ab und gib `Fehler` aus.''',
  given="""import asyncio

async def teile(a, b):
    await asyncio.sleep(0.1)
    return a / b
""", body="""try:
    ergebnisse = await asyncio.gather(teile(8, 2), teile(5, 0), teile(9, 3))
    print(ergebnisse)
except ZeroDivisionError:
    print('Fehler')""")
t('''Berechne dieselben drei Aufgaben mit `gather(..., return_exceptions=True)`. Gib für jedes Ergebnis eine Zeile aus: bei einem Fehler `Fehler: <Typname>`, sonst `Ergebnis: <wert>`.''',
  given="""import asyncio

async def teile(a, b):
    await asyncio.sleep(0.1)
    return a / b
""", body="""ergebnisse = await asyncio.gather(teile(8, 2), teile(5, 0), teile(9, 3), return_exceptions=True)
for ergebnis in ergebnisse:
    if isinstance(ergebnis, Exception):
        print('Fehler:', type(ergebnis).__name__)
    else:
        print('Ergebnis:', ergebnis)""")
t('''Die Coroutine `hole_alter(name)` ist vorgegeben und wirft bei einem unbekannten Namen einen `KeyError`. Hole die Alter von `['Ali', 'Zoe', 'Bea']` mit `gather(..., return_exceptions=True)`.
Gib die Summe der Alter aus, die es gibt (`Summe: 29`). Nimm dazu nur Einträge, die keine Fehler sind.''',
  given="""import asyncio

alter = {'Ali': 15, 'Bea': 14}

async def hole_alter(name):
    await asyncio.sleep(0.1)
    return alter[name]

namen = ['Ali', 'Zoe', 'Bea']
""", body="""aufgaben = []
for name in namen:
    aufgaben.append(hole_alter(name))
ergebnisse = await asyncio.gather(*aufgaben, return_exceptions=True)

summe = 0
for ergebnis in ergebnisse:
    if not isinstance(ergebnis, Exception):
        summe += ergebnis
print('Summe:', summe)""")
t('''Die Coroutine `lade(seite)` ist vorgegeben. Erzeuge Tasks für `'A'`, `'B'` und `'C'` in einer Schleife. Übergib sie mit `gather(*tasks)` und gib danach die Ergebnisliste
und danach `True`, wenn alle Tasks `done()` sind (prüfe das mit einer Schleife: `fertig = True`, bei einem nicht fertigen Task `False`).''',
  given="""import asyncio

async def lade(seite):
    await asyncio.sleep(0.1)
    return seite * 2
""", body="""tasks = []
for seite in ['A', 'B', 'C']:
    tasks.append(asyncio.create_task(lade(seite)))

ergebnisse = await asyncio.gather(*tasks)
print(ergebnisse)

fertig = True
for aufgabe in tasks:
    if not aufgabe.done():
        fertig = False
print(fertig)""")
task('''Die Zelle bricht mit einem `ZeroDivisionError` ab, weil eine Aufgabe fehlschlägt. Verbessere sie mit `return_exceptions=True`, sodass die Liste `['Fehler', 5.0]` ausgegeben wird.
Ersetze dazu jedes Fehlerobjekt in der Liste durch den Text `'Fehler'`.''',
     zelle="""import asyncio

async def teile(a, b):
    await asyncio.sleep(0.1)
    return a / b

try:
    ergebnisse = await asyncio.gather(teile(1, 0), teile(10, 2))
except ZeroDivisionError:
    ergebnisse = ['Abbruch']
print(ergebnisse)""",
     solution="""import asyncio

async def teile(a, b):
    await asyncio.sleep(0.1)
    return a / b

ergebnisse = await asyncio.gather(teile(1, 0), teile(10, 2), return_exceptions=True)
for i in range(len(ergebnisse)):
    if isinstance(ergebnisse[i], Exception):
        ergebnisse[i] = 'Fehler'
print(ergebnisse)""")

# ---------------------------------------------------------------- 4
sec('as_completed(): in der Reihenfolge der Fertigstellung')
expl('''#### Ergebnisse, sobald sie fertig sind

`gather` liefert alle Ergebnisse erst, wenn **alle** Aufgaben fertig sind. Oft möchte man aber ein Ergebnis **sofort** verarbeiten, sobald es da ist.

`asyncio.as_completed(aufgaben)` gibt die Aufgaben in der Reihenfolge zurück, in der sie **fertig werden**. Man schreibt:

```python
for f in asyncio.as_completed(aufgaben):
    ergebnis = await f
```

Die Aufgabe, die zuerst fertig ist, kommt zuerst dran.''',
     """import asyncio

async def lade(seite, dauer):
    await asyncio.sleep(dauer)
    return seite

aufgaben = [lade('A', 0.3), lade('B', 0.1), lade('C', 0.2)]
for f in asyncio.as_completed(aufgaben):
    ergebnis = await f
    print('Fertig:', ergebnis)""")
expl('''#### Welches Ergebnis gehört wozu?

Weil die Reihenfolge nicht die der Liste ist, muss die Coroutine selbst mitliefern, **wozu** das Ergebnis gehört. Zum Beispiel gibt sie ein Paar `(name, wert)` zurück.''',
     """import asyncio

async def lade(seite, dauer):
    await asyncio.sleep(dauer)
    return (seite, len(seite))

aufgaben = []
for seite, dauer in [('Stundenplan', 0.3), ('Mensa', 0.1), ('Start', 0.2)]:
    aufgaben.append(lade(seite, dauer))

for f in asyncio.as_completed(aufgaben):
    name, laenge = await f
    print(name, 'hat', laenge, 'Zeichen')""")
expl('''#### Vergleich: gather und as_completed

| | `gather` | `as_completed` |
|---|---|---|
| Ergebnisse kommen | alle auf einmal, am Ende | nacheinander, sobald fertig |
| Reihenfolge | die der Argumente | die der Fertigstellung |
| gut für | alles zusammen weiterverarbeiten | sofort anzeigen oder verarbeiten |''', None)

predict("""import asyncio

async def f(name, dauer):
    await asyncio.sleep(dauer)
    return name

aufgaben = [f('x', 0.2), f('y', 0.1)]
for aufgabe in asyncio.as_completed(aufgaben):
    print(await aufgabe)""", erklaerung='''`y` wartet nur 0,1 Sekunden und ist zuerst fertig. Deshalb liefert `as_completed` diese Aufgabe als erste.

```
y
x
```''')
predict("""import asyncio

async def f(name, dauer):
    await asyncio.sleep(dauer)
    return name

aufgaben = [f('x', 0.2), f('y', 0.1)]
ergebnisse = await asyncio.gather(*aufgaben)
print(ergebnisse)""", erklaerung='''`gather` liefert die Ergebnisse in der Reihenfolge der Argumente, nicht in der Reihenfolge der Fertigstellung.

```
['x', 'y']
```''')
t('''Die Coroutine `lade(seite, dauer)` ist vorgegeben und gibt den Namen der Seite zurück. Erzeuge die Coroutinen für `('Start', 0.3)`, `('Plan', 0.1)` und `('Mensa', 0.2)` in einer Liste
und gib die Namen mit `as_completed` in der Reihenfolge der Fertigstellung aus.''',
  given="""import asyncio

async def lade(seite, dauer):
    await asyncio.sleep(dauer)
    return seite
""", body="""aufgaben = [lade('Start', 0.3), lade('Plan', 0.1), lade('Mensa', 0.2)]
for f in asyncio.as_completed(aufgaben):
    print(await f)""")
t('''Die Coroutine `lauf(name, zeit)` ist vorgegeben (sie wartet `zeit` Sekunden). Drei Läufer starten gleichzeitig. Gib die Platzierung aus:
`1. Platz: <name>`, `2. Platz: ...`, `3. Platz: ...`. Zähle dazu die Plätze mit einer Variablen hoch.''',
  given="""import asyncio

async def lauf(name, zeit):
    await asyncio.sleep(zeit)
    return name

laeufer = [('Ali', 0.3), ('Bea', 0.1), ('Cem', 0.2)]
""", body="""aufgaben = []
for name, zeit in laeufer:
    aufgaben.append(lauf(name, zeit))

platz = 0
for f in asyncio.as_completed(aufgaben):
    name = await f
    platz += 1
    print(f'{platz}. Platz: {name}')""")
t('''Die Coroutine `lade(seite, dauer)` ist vorgegeben und gibt das Paar `(seite, dauer)` zurück. Gib mit `as_completed` für jede Seite `<seite> nach <dauer> Sekunden` aus.
Die Seiten sind `('A', 0.2)`, `('B', 0.3)` und `('C', 0.1)`.''',
  given="""import asyncio

async def lade(seite, dauer):
    await asyncio.sleep(dauer)
    return (seite, dauer)
""", body="""aufgaben = [lade('A', 0.2), lade('B', 0.3), lade('C', 0.1)]
for f in asyncio.as_completed(aufgaben):
    seite, dauer = await f
    print(seite, 'nach', dauer, 'Sekunden')""")
t('''Die Coroutine `lade(seite, dauer)` ist vorgegeben. Sammle mit `as_completed` alle Namen **in der Reihenfolge der Fertigstellung** in der Liste `fertig`
und gib die Liste aus. Gib danach auch das Ergebnis von `gather` aus (Reihenfolge der Argumente).
Aufgaben: `('x', 0.3)`, `('y', 0.1)`, `('z', 0.2)`.''',
  given="""import asyncio

async def lade(seite, dauer):
    await asyncio.sleep(dauer)
    return seite
""", body="""fertig = []
aufgaben = [lade('x', 0.3), lade('y', 0.1), lade('z', 0.2)]
for f in asyncio.as_completed(aufgaben):
    fertig.append(await f)
print(fertig)

aufgaben = [lade('x', 0.3), lade('y', 0.1), lade('z', 0.2)]
print(await asyncio.gather(*aufgaben))""")
t('''Die Coroutine `pruefe(zahl)` ist vorgegeben: Sie wartet je nach Zahl unterschiedlich lange und gibt `(zahl, True)` zurück, wenn die Zahl gerade ist, sonst `(zahl, False)`.
Prüfe die Zahlen `[3, 1, 2]` mit `as_completed` und gib für jede eine Zeile `<zahl>: gerade` oder `<zahl>: ungerade` aus.''',
  given="""import asyncio

async def pruefe(zahl):
    await asyncio.sleep(zahl * 0.1)
    return (zahl, zahl % 2 == 0)

zahlen = [3, 1, 2]
""", body="""aufgaben = []
for zahl in zahlen:
    aufgaben.append(pruefe(zahl))

for f in asyncio.as_completed(aufgaben):
    zahl, gerade = await f
    if gerade:
        print(f'{zahl}: gerade')
    else:
        print(f'{zahl}: ungerade')""")

# ---------------------------------------------------------------- 5
sec('wait(): auf Tasks warten')
expl('''#### `asyncio.wait()`

`asyncio.wait(tasks)` wartet auf eine Menge von **Tasks** (Coroutinen müssen vorher mit `create_task` zu Tasks gemacht werden). Es gibt zwei Mengen zurück:
`fertig` (Tasks, die fertig sind) und `offen` (Tasks, die noch laufen).

Standardmäßig wartet `wait`, bis **alle** fertig sind. Dann ist `offen` leer. Das Ergebnis eines Tasks holt man mit `task.result()`.
Mengen haben **keine feste Reihenfolge**. Wenn man die Ergebnisse ausgeben will, sortiert man sie vorher.''',
     """import asyncio

async def verdopple(x):
    await asyncio.sleep(0.1)
    return x * 2

tasks = []
for zahl in [3, 1, 2]:
    tasks.append(asyncio.create_task(verdopple(zahl)))

fertig, offen = await asyncio.wait(tasks)
print('fertig:', len(fertig), 'offen:', len(offen))

ergebnisse = []
for aufgabe in fertig:
    ergebnisse.append(aufgabe.result())
print(sorted(ergebnisse))""")
expl('''#### `return_when=asyncio.FIRST_COMPLETED`

Mit `return_when=asyncio.FIRST_COMPLETED` kehrt `wait` schon zurück, sobald der **erste** Task fertig ist. Die anderen laufen weiter und stehen in `offen`.
Das ist ein „Wer ist zuerst?“-Rennen.

Auf die übrigen kann man danach mit einem weiteren `await asyncio.wait(offen)` warten.''',
     """import asyncio

async def lauf(name, zeit):
    await asyncio.sleep(zeit)
    return name

tasks = []
for name, zeit in [('Ali', 0.3), ('Bea', 0.1), ('Cem', 0.2)]:
    tasks.append(asyncio.create_task(lauf(name, zeit)))

fertig, offen = await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)
for aufgabe in fertig:
    print('Zuerst im Ziel:', aufgabe.result())
print('Noch unterwegs:', len(offen))

fertig2, offen2 = await asyncio.wait(offen)
print('Danach fertig:', len(fertig2), 'offen:', len(offen2))""")
expl('''#### Vergleich der Werkzeuge

| Werkzeug | gibt zurück | wann |
|---|---|---|
| `gather` | Liste der Ergebnisse | wenn alle fertig sind |
| `as_completed` | ein Ergebnis nach dem anderen | sobald jeweils eine Aufgabe fertig ist |
| `wait` | Mengen `fertig` und `offen` von Tasks | wenn alle, die erste oder die erste mit Fehler fertig ist |''', None)

predict("""import asyncio

async def f(x):
    await asyncio.sleep(0.1)
    return x

tasks = []
for x in [1, 2, 3]:
    tasks.append(asyncio.create_task(f(x)))

fertig, offen = await asyncio.wait(tasks)
print(len(fertig), len(offen))""", erklaerung='''Ohne `return_when` wartet `wait`, bis alle Tasks fertig sind. Es gibt also drei fertige und keine offenen Tasks.

```
3 0
```''')
predict("""import asyncio

async def f(name, zeit):
    await asyncio.sleep(zeit)
    return name

t1 = asyncio.create_task(f('a', 0.3))
t2 = asyncio.create_task(f('b', 0.1))
fertig, offen = await asyncio.wait([t1, t2], return_when=asyncio.FIRST_COMPLETED)
print(len(fertig), len(offen))
for aufgabe in fertig:
    print(aufgabe.result())
await t1""", erklaerung='''`b` ist nach 0,1 Sekunden fertig, und `wait` kehrt dann sofort zurück. In `fertig` steht ein Task, in `offen` einer (`a` läuft noch). `result()` liefert `b`.
Am Ende wartet `await t1` noch auf den anderen Task.

```
1 1
b
```''')
t('''Die Coroutine `verdopple(x)` ist vorgegeben. Erzeuge Tasks für alle Zahlen der Liste, warte mit `asyncio.wait` auf alle und gib die **sortierte** Liste der Ergebnisse aus.''',
  given="""import asyncio

async def verdopple(x):
    await asyncio.sleep(0.1)
    return x * 2

zahlen = [5, 2, 8, 1]
""", body="""tasks = []
for zahl in zahlen:
    tasks.append(asyncio.create_task(verdopple(zahl)))

fertig, offen = await asyncio.wait(tasks)
ergebnisse = []
for aufgabe in fertig:
    ergebnisse.append(aufgabe.result())
print(sorted(ergebnisse))""")
t('''Die Coroutine `lauf(name, zeit)` ist vorgegeben. Starte Tasks für `('Ali', 0.3)`, `('Bea', 0.1)`, `('Cem', 0.2)`. Warte mit `FIRST_COMPLETED`, bis der erste im Ziel ist,
und gib `Sieger: <Name>` aus.''',
  given="""import asyncio

async def lauf(name, zeit):
    await asyncio.sleep(zeit)
    return name
""", body="""tasks = []
for name, zeit in [('Ali', 0.3), ('Bea', 0.1), ('Cem', 0.2)]:
    tasks.append(asyncio.create_task(lauf(name, zeit)))

fertig, offen = await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)
for aufgabe in fertig:
    print('Sieger:', aufgabe.result())
await asyncio.wait(offen)""")
t('''Starte mit der vorgegebenen Coroutine `lauf` wie in der Aufgabe davor drei Tasks. Gib nach `FIRST_COMPLETED` mit `print(len(fertig), len(offen))` die Anzahlen aus.
Warte dann mit `await asyncio.wait(offen)` auf den Rest und gib die Anzahlen noch einmal aus.''',
  given="""import asyncio

async def lauf(name, zeit):
    await asyncio.sleep(zeit)
    return name

tasks = []
for name, zeit in [('Ali', 0.3), ('Bea', 0.1), ('Cem', 0.2)]:
    tasks.append(asyncio.create_task(lauf(name, zeit)))
""", body="""fertig, offen = await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)
print(len(fertig), len(offen))
fertig, offen = await asyncio.wait(offen)
print(len(fertig), len(offen))""")
t('''Starte drei Tasks mit Namen (`name='t1'`, `'t2'`, `'t3'`) für `schlafe(0.2)`, `schlafe(0.1)` und `schlafe(0.3)`. Warte mit `FIRST_COMPLETED` und gib den **Namen** des ersten fertigen Tasks aus
(`get_name()`). Warte danach auf die restlichen.''',
  given="""import asyncio

async def schlafe(zeit):
    await asyncio.sleep(zeit)
""", body="""tasks = []
for nr, zeit in [(1, 0.2), (2, 0.1), (3, 0.3)]:
    tasks.append(asyncio.create_task(schlafe(zeit), name='t' + str(nr)))

fertig, offen = await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)
for aufgabe in fertig:
    print(aufgabe.get_name())
await asyncio.wait(offen)""")

# ---------------------------------------------------------------- 6
sec('TaskGroup')
expl('''#### Tasks in einer Gruppe

Seit Python 3.11 gibt es `asyncio.TaskGroup`. Sie fasst Tasks zu einer **Gruppe** zusammen und wartet am Ende automatisch auf alle:

```python
async with asyncio.TaskGroup() as gruppe:
    t1 = gruppe.create_task(coroutine1())
    t2 = gruppe.create_task(coroutine2())
# hier sind alle Tasks fertig
```

`async with` funktioniert wie `with`, nur darf beim Betreten und Verlassen gewartet werden. Wichtig für dich: Beim **Verlassen** des Blocks (also nach dem Einrücken)
wartet die Gruppe, bis alle ihre Tasks fertig sind. Die Ergebnisse holt man danach mit `task.result()`.''',
     """import asyncio

async def lade(seite):
    print('Lade', seite)
    await asyncio.sleep(1)
    return len(seite)

async with asyncio.TaskGroup() as gruppe:
    t1 = gruppe.create_task(lade('Start'))
    t2 = gruppe.create_task(lade('Mensa'))
    print('Beide Tasks sind angemeldet')

print('Alle fertig:', t1.result(), t2.result())""")
expl('''#### Dauer und viele Tasks

Auch in einer Schleife kann man Tasks in der Gruppe erzeugen. Die Gesamtdauer ist wieder die längste Wartezeit.''',
     """import asyncio
import time

async def arbeite(nr):
    await asyncio.sleep(1)
    return nr * nr

start = time.perf_counter()
tasks = []
async with asyncio.TaskGroup() as gruppe:
    for nr in [1, 2, 3, 4]:
        tasks.append(gruppe.create_task(arbeite(nr)))

ergebnisse = []
for aufgabe in tasks:
    ergebnisse.append(aufgabe.result())
print(ergebnisse)
print('Dauer:', round(time.perf_counter() - start), 's')""")
expl('''#### Warum TaskGroup?

Die Gruppe räumt auf: Verlässt man den Block, sind **alle** Tasks fertig, nichts läuft heimlich weiter. Das ist sicherer als einzelne `create_task`-Aufrufe,
bei denen man leicht vergisst, auf einen Task zu warten.

Geht in der Gruppe ein Task schief, werden die anderen abgebrochen. Wie man solche Fehler behandelt, lernst du im nächsten Notebook (`asyncio_steuerung`).''', None)

predict("""import asyncio

async def sag(text):
    print(text)

async with asyncio.TaskGroup() as gruppe:
    gruppe.create_task(sag('Task 1'))
    gruppe.create_task(sag('Task 2'))
    print('im Block')
print('nach dem Block')""", erklaerung='''Im Block werden die Tasks nur angemeldet. Erst wenn der Block verlassen wird (oder der Code wartet), kommen sie dran. Deshalb steht `im Block` zuerst.
Nach dem Block sind beide Tasks fertig.

```
im Block
Task 1
Task 2
nach dem Block
```''')
predict("""import asyncio
import time

async def warte():
    await asyncio.sleep(1)

start = time.perf_counter()
async with asyncio.TaskGroup() as gruppe:
    gruppe.create_task(warte())
    gruppe.create_task(warte())
    gruppe.create_task(warte())
print(round(time.perf_counter() - start))""", erklaerung='''Die drei Tasks warten gleichzeitig. Die Gruppe ist fertig, wenn der längste fertig ist: nach 1 Sekunde.

```
1
```''')
t('''Die Coroutine `quadrat(z)` ist vorgegeben. Erzeuge in einer `TaskGroup` Tasks für `2`, `3` und `4` (merke sie dir in `tasks`). Gib nach dem Block die Ergebnisse aus.''',
  given="""import asyncio

async def quadrat(z):
    await asyncio.sleep(0.1)
    return z * z
""", body="""tasks = []
async with asyncio.TaskGroup() as gruppe:
    for z in [2, 3, 4]:
        tasks.append(gruppe.create_task(quadrat(z)))

for aufgabe in tasks:
    print(aufgabe.result())""")
t('''Die Coroutine `lade(seite)` ist vorgegeben (eine Sekunde). Lade alle Seiten der Liste in einer `TaskGroup`. Gib danach `Alle geladen` und die Dauer aus.''',
  given="""import asyncio
import time

async def lade(seite):
    await asyncio.sleep(1)
    print('Geladen:', seite)

seiten = ['Start', 'Plan', 'Mensa', 'Hilfe']
""", body="""start = time.perf_counter()
async with asyncio.TaskGroup() as gruppe:
    for seite in seiten:
        gruppe.create_task(lade(seite))
print('Alle geladen')
print('Dauer:', round(time.perf_counter() - start), 's')""")
t('''Die Coroutine `hole_note(fach)` ist vorgegeben. Hole in einer `TaskGroup` die Noten aller Fächer der Liste. Gib danach den **Durchschnitt** der Noten aus (Summe geteilt durch Anzahl).''',
  given="""import asyncio

noten = {'Mathe': 2, 'Deutsch': 3, 'Physik': 1, 'Kunst': 2}

async def hole_note(fach):
    await asyncio.sleep(0.1)
    return noten[fach]

faecher = ['Mathe', 'Deutsch', 'Physik', 'Kunst']
""", body="""tasks = []
async with asyncio.TaskGroup() as gruppe:
    for fach in faecher:
        tasks.append(gruppe.create_task(hole_note(fach)))

summe = 0
for aufgabe in tasks:
    summe += aufgabe.result()
print(summe / len(tasks))""")
t('''Schreibe `zaehle(name)` (gibt `<name> 1`, `<name> 2` aus, nach jeder Ausgabe `await asyncio.sleep(0)`). Starte `'A'`, `'B'` und `'C'` in einer `TaskGroup`.
Gib nach dem Block `Fertig` aus.''',
  given='import asyncio\n', body="""async def zaehle(name):
    for i in range(1, 3):
        print(name, i)
        await asyncio.sleep(0)

async with asyncio.TaskGroup() as gruppe:
    for name in ['A', 'B', 'C']:
        gruppe.create_task(zaehle(name))
print('Fertig')""")
task('''Der Code startet die Tasks mit `create_task`, wartet aber nicht auf sie. Die Zelle gibt deshalb `Ergebnis: 0` aus (die Tasks sind noch nicht gelaufen). Verbessere den Code mit einer `TaskGroup` und `result()`, sodass `Ergebnis: 14` ausgegeben wird.''',
     zelle="""import asyncio

async def zahl(x):
    await asyncio.sleep(0.1)
    return x

t1 = asyncio.create_task(zahl(6))
t2 = asyncio.create_task(zahl(8))
print('Ergebnis:', t1.done() + t2.done())""",
     solution="""import asyncio

async def zahl(x):
    await asyncio.sleep(0.1)
    return x

async with asyncio.TaskGroup() as gruppe:
    t1 = gruppe.create_task(zahl(6))
    t2 = gruppe.create_task(zahl(8))
print('Ergebnis:', t1.result() + t2.result())""")

# ---------------------------------------------------------------- 7
sec('Gemischte Übungen')
t('''Die Coroutine `bestelle(gericht)` ist vorgegeben und gibt den Preis zurück. Bestelle `'Pizza'`, `'Salat'` und `'Suppe'` als drei Tasks gleichzeitig. Gib die Gesamtsumme und die Dauer aus.''',
  given="""import asyncio
import time

preise = {'Pizza': 5, 'Salat': 3, 'Suppe': 2}

async def bestelle(gericht):
    await asyncio.sleep(1)
    return preise[gericht]
""", body="""start = time.perf_counter()
tasks = []
for gericht in ['Pizza', 'Salat', 'Suppe']:
    tasks.append(asyncio.create_task(bestelle(gericht)))

summe = 0
for aufgabe in tasks:
    summe += await aufgabe
print('Summe:', summe)
print('Dauer:', round(time.perf_counter() - start), 's')""")
t('''Die Coroutine `lade(seite, dauer)` ist vorgegeben. Zeige jede Seite **sofort**, wenn sie fertig ist (`as_completed`), und gib am Ende mit `gather` (eine zweite, gleiche Runde) die Namen in der Reihenfolge der Argumente aus.
Seiten: `('Start', 0.2)`, `('Plan', 0.1)`, `('Mensa', 0.3)`.''',
  given="""import asyncio

async def lade(seite, dauer):
    await asyncio.sleep(dauer)
    return seite

daten = [('Start', 0.2), ('Plan', 0.1), ('Mensa', 0.3)]
""", body="""aufgaben = []
for seite, dauer in daten:
    aufgaben.append(lade(seite, dauer))
for f in asyncio.as_completed(aufgaben):
    print('Gerade fertig:', await f)

aufgaben = []
for seite, dauer in daten:
    aufgaben.append(lade(seite, dauer))
print(await asyncio.gather(*aufgaben))""")
t('''Die Coroutine `hole_punkte(name)` ist vorgegeben und wirft einen `KeyError` für unbekannte Namen. Hole die Punkte für `['Ali', 'Zoe', 'Bea']` mit `gather(..., return_exceptions=True)`.
Gib für jeden Namen `<name>: <punkte>` oder `<name>: nicht gefunden` aus.''',
  given="""import asyncio

punkte = {'Ali': 12, 'Bea': 17}

async def hole_punkte(name):
    await asyncio.sleep(0.1)
    return punkte[name]

namen = ['Ali', 'Zoe', 'Bea']
""", body="""aufgaben = []
for name in namen:
    aufgaben.append(hole_punkte(name))
ergebnisse = await asyncio.gather(*aufgaben, return_exceptions=True)

for i in range(len(namen)):
    if isinstance(ergebnisse[i], Exception):
        print(f'{namen[i]}: nicht gefunden')
    else:
        print(f'{namen[i]}: {ergebnisse[i]}')""")
t('''Schreibe `main()`: Sie startet in einer `TaskGroup` für jedes Element der Liste `klassen` einen Task `lade_klasse(klasse)` und gibt danach das **Dictionary** `{klasse: schueler}` zurück.
Gib `await main()` aus.''',
  given="""import asyncio

anzahl = {'5a': 26, '6b': 24, '7c': 28}

async def lade_klasse(klasse):
    await asyncio.sleep(0.1)
    return anzahl[klasse]

klassen = ['5a', '6b', '7c']
""", body="""async def main():
    tasks = {}
    async with asyncio.TaskGroup() as gruppe:
        for klasse in klassen:
            tasks[klasse] = gruppe.create_task(lade_klasse(klasse))
    ergebnis = {}
    for klasse in klassen:
        ergebnis[klasse] = tasks[klasse].result()
    return ergebnis

print(await main())""")
t('''Drei Läufer (`lauf(name, zeit)` ist vorgegeben) starten gleichzeitig als Tasks. Gib mit `wait(..., return_when=asyncio.FIRST_COMPLETED)` den Sieger aus (`Sieger: <Name>`).
Warte danach auf die anderen und gib `Alle im Ziel` aus.''',
  given="""import asyncio

async def lauf(name, zeit):
    await asyncio.sleep(zeit)
    return name
""", body="""tasks = []
for name, zeit in [('Ali', 0.2), ('Bea', 0.3), ('Cem', 0.1)]:
    tasks.append(asyncio.create_task(lauf(name, zeit)))

fertig, offen = await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)
for aufgabe in fertig:
    print('Sieger:', aufgabe.result())
await asyncio.wait(offen)
print('Alle im Ziel')""")
t('''Die Coroutine `lade(seite)` ist vorgegeben (eine Sekunde). Lade `'A'` allein. Lade dann gleichzeitig in einer `TaskGroup` `'B'`, `'C'` und `'D'`.
Gib danach die Gesamtdauer aus (`Dauer: 2 s`).''',
  given="""import asyncio
import time

async def lade(seite):
    await asyncio.sleep(1)
    print('Geladen:', seite)
""", body="""start = time.perf_counter()
await lade('A')
async with asyncio.TaskGroup() as gruppe:
    for seite in ['B', 'C', 'D']:
        gruppe.create_task(lade(seite))
print('Dauer:', round(time.perf_counter() - start), 's')""")
predict("""import asyncio

async def f(name, dauer):
    await asyncio.sleep(dauer)
    print(name)
    return name

t1 = asyncio.create_task(f('a', 0.2))
t2 = asyncio.create_task(f('b', 0.1))
print(await t1)
print(t2.done())
print(t2.result())""", erklaerung='''Beide Tasks starten gleichzeitig. `b` ist nach 0,1 Sekunden fertig und gibt `b` aus, `a` nach 0,2 Sekunden. Dann liefert `await t1` den Wert `a`, und `print` gibt ihn aus.
Danach ist `t2` längst fertig.

```
b
a
a
True
b
```''')
predict("""import asyncio

async def f(x):
    await asyncio.sleep(0.1)
    return x * 10

async def main():
    async with asyncio.TaskGroup() as gruppe:
        t1 = gruppe.create_task(f(1))
        t2 = gruppe.create_task(f(2))
    ergebnis = await asyncio.gather(f(3), f(4))
    return t1.result() + t2.result() + sum(ergebnis)

print(await main())""", erklaerung='''Die `TaskGroup` liefert `10` und `20`. Das `gather` danach liefert `[30, 40]`. Die Summe ist 10 + 20 + 30 + 40 = 100.

```
100
```''')

generate('asyncio_tasks', 'asyncio 2: Tasks', intro=INTRO, ausfuehren=AUSFUEHREN)
