# Erzeugt ../content/asyncio_steuerung.ipynb (siehe nbgen.py). Drittes Notebook der asyncio-Reihe (asynchilfe.py, asyncnb.py).
# Regeln wie in gen_asyncio_grundlagen.py: Zeiten nur ganzzahlig mit round(), Reihenfolgen nur bei Wartezeiten, die sich um mindestens
# 0.1 s unterscheiden (oder mit asyncio.sleep(0)); keine gleichzeitig auslaufenden Wartezeiten bei Semaphore/Lock mit Ausgaben.
# Nie asyncio.run() in einer Codezelle (JupyterLite verhält sich anders als JupyterLab). Abbrechen immer mit try/except CancelledError abfangen.
# Nie Task-Objekte ausgeben (Adressen), keine Fehlertexte von eingebauten Fehlern außer selbst geschriebenen.
from nbgen import sec, expl, task, predict, generate
from asynchilfe import t, reihe, AUSFUEHREN

INTRO = f'''In diesem Notebook lernst du, wie man asynchrone Programme **steuert**: Zeitlimits setzen, Tasks abbrechen, mit Fehlern umgehen
und gemeinsam benutzte Dinge schützen und begrenzen (`Lock`, `Semaphore`, `Event`).

Die Reihe besteht aus vier Notebooks:

{reihe('asyncio_steuerung')}

Du solltest die Notebooks **asyncio_grundlagen** und **asyncio_tasks** kennen (`create_task()`, `gather()`, `TaskGroup`).
Fehler abfangen mit `try`, `except` und `finally` brauchst du ebenfalls.

Der Abschnitt über `ExceptionGroup` und `except*` ist für das **Leistungsfach** gedacht.

Gemessene Zeiten sind nie ganz genau. Deshalb runden wir sie mit `round()` auf ganze Sekunden.

Jeder Abschnitt beginnt mit kurzen Erklärungen und Beispielen. Führe die Beispiele aus und probiere sie ruhig ein wenig aus.
Danach folgen viele kleine Übungen. Wenn etwas vorgegeben ist, steht es schon in der Codezelle.'''

# ---------------------------------------------------------------- 1
sec('Zeitlimits: wait_for() und timeout()')
expl('''#### `asyncio.wait_for()`

Manchmal darf etwas nicht beliebig lange dauern, zum Beispiel das Laden einer Webseite. Mit `asyncio.wait_for(coroutine, timeout=sekunden)` setzt man ein **Zeitlimit**.
Ist die Coroutine bis dahin nicht fertig, wird sie **abgebrochen**, und es entsteht ein `TimeoutError`, den man mit `try` und `except` abfängt.''',
     """import asyncio

async def lade(seite, dauer):
    await asyncio.sleep(dauer)
    return 'Inhalt von ' + seite

try:
    text = await asyncio.wait_for(lade('Start', 0.1), timeout=0.5)
    print(text)
    text = await asyncio.wait_for(lade('Mensa', 2), timeout=0.5)
    print(text)
except TimeoutError:
    print('Zu langsam!')""")
expl('''#### `asyncio.timeout()`

Mit `async with asyncio.timeout(sekunden):` gilt das Zeitlimit für **einen ganzen Block**, in dem auch mehrere `await` stehen können.
Dauert der Block zu lange, wird er abgebrochen und der `TimeoutError` entsteht **hinter** dem Block.''',
     """import asyncio

async def schritt(nr):
    await asyncio.sleep(0.2)
    print('Schritt', nr, 'fertig')

try:
    async with asyncio.timeout(0.5):
        await schritt(1)
        await schritt(2)
        await schritt(3)
        print('Alles geschafft')
except TimeoutError:
    print('Zeit abgelaufen')""")
expl('''#### Was passiert mit der Coroutine?

Bei einem Timeout wird die Coroutine an der Stelle abgebrochen, an der sie gerade wartet. Ein `finally` in der Coroutine wird dabei noch ausgeführt, so kann sie aufräumen.''',
     """import asyncio

async def download():
    try:
        print('Download startet')
        await asyncio.sleep(2)
        print('Download fertig')
    finally:
        print('Aufräumen')

try:
    await asyncio.wait_for(download(), timeout=0.3)
except TimeoutError:
    print('Timeout')""")

predict("""import asyncio

async def f():
    await asyncio.sleep(1)
    return 'fertig'

try:
    print(await asyncio.wait_for(f(), timeout=2))
except TimeoutError:
    print('Timeout')""", erklaerung='''`f` braucht 1 Sekunde, das Limit sind 2 Sekunden. Die Coroutine wird rechtzeitig fertig, und `print` gibt ihr Ergebnis aus.

```
fertig
```''')
predict("""import asyncio

async def f():
    await asyncio.sleep(1)
    print('A')

try:
    await asyncio.wait_for(f(), timeout=0.2)
    print('B')
except TimeoutError:
    print('C')
print('D')""", erklaerung='''Das Limit (0,2 Sekunden) ist kürzer als die Wartezeit von `f`. `f` wird abgebrochen, ohne dass `A` ausgegeben wird. `B` wird übersprungen, weil der Fehler schon entstanden ist.
Der `except`-Block gibt `C` aus, danach geht es normal mit `D` weiter.

```
C
D
```''')
predict("""import asyncio

async def schritt(nr):
    await asyncio.sleep(0.2)
    print('Schritt', nr)

try:
    async with asyncio.timeout(0.5):
        await schritt(1)
        await schritt(2)
        await schritt(3)
except TimeoutError:
    print('Zeit abgelaufen')""", erklaerung='''Jeder Schritt dauert 0,2 Sekunden. Schritt 1 ist bei 0,2 und Schritt 2 bei 0,4 Sekunden fertig. Schritt 3 würde erst bei 0,6 Sekunden fertig, aber das Limit von 0,5 Sekunden ist vorher abgelaufen.

```
Schritt 1
Schritt 2
Zeit abgelaufen
```''')
t('''Die Coroutine `lade(dauer)` ist vorgegeben. Rufe sie mit `wait_for` und einem Zeitlimit von `0.5` Sekunden mit `lade(0.1)` auf und gib `Geladen` aus.
Rufe sie danach mit `lade(1)` auf. Fange den `TimeoutError` ab und gib `Zu langsam` aus.''',
  given="""import asyncio

async def lade(dauer):
    await asyncio.sleep(dauer)
""", body="""await asyncio.wait_for(lade(0.1), timeout=0.5)
print('Geladen')
try:
    await asyncio.wait_for(lade(1), timeout=0.5)
    print('Geladen')
except TimeoutError:
    print('Zu langsam')""")
t('''Die Coroutine `antwort(name, dauer)` ist vorgegeben und gibt den Namen zurück. Frage mit einem Zeitlimit von `0.3` Sekunden die Server `('A', 0.1)`, `('B', 0.5)` und `('C', 0.2)` **nacheinander**.
Gib für jeden `<name>: ok` oder `<name>: Timeout` aus.''',
  given="""import asyncio

async def antwort(name, dauer):
    await asyncio.sleep(dauer)
    return name

server = [('A', 0.1), ('B', 0.5), ('C', 0.2)]
""", body="""for name, dauer in server:
    try:
        await asyncio.wait_for(antwort(name, dauer), timeout=0.3)
        print(name + ': ok')
    except TimeoutError:
        print(name + ': Timeout')""")
t('''Die Coroutine `schritt(nr)` ist vorgegeben (0,2 Sekunden). Führe die Schritte 1 bis 4 in einem Block `async with asyncio.timeout(0.7)` aus. Es passen nur drei Schritte hinein.
Fange den `TimeoutError` ab und gib `Abbruch` aus.''',
  given="""import asyncio

async def schritt(nr):
    await asyncio.sleep(0.2)
    print('Schritt', nr)
""", body="""try:
    async with asyncio.timeout(0.7):
        for nr in [1, 2, 3, 4]:
            await schritt(nr)
        print('Fertig')
except TimeoutError:
    print('Abbruch')""")
t('''Die Coroutine `rechne()` ist vorgegeben. Starte `rechne()` drei Mal gleichzeitig mit `gather`, jeweils mit einem eigenen Zeitlimit von 0,5 Sekunden durch `wait_for`. Eine ist zu langsam: Benutze `return_exceptions=True`
und gib für jedes Ergebnis `ok` oder `Timeout` aus (Fehler erkennst du mit `isinstance(e, TimeoutError)`).''',
  given="""import asyncio

async def rechne(dauer):
    await asyncio.sleep(dauer)
    return dauer

dauern = [0.1, 0.9, 0.2]
""", body="""aufgaben = []
for dauer in dauern:
    aufgaben.append(asyncio.wait_for(rechne(dauer), timeout=0.5))
ergebnisse = await asyncio.gather(*aufgaben, return_exceptions=True)
for e in ergebnisse:
    if isinstance(e, TimeoutError):
        print('Timeout')
    else:
        print('ok')""")
t('''Die Coroutine `download()` ist vorgegeben und räumt in einem `finally` auf. Rufe sie mit einem Zeitlimit von `0.3` auf und fange den `TimeoutError`: Es soll `Aufräumen` und danach `Timeout` ausgegeben werden.''',
  given="""import asyncio

async def download():
    try:
        await asyncio.sleep(1)
    finally:
        print('Aufräumen')
""", body="""try:
    await asyncio.wait_for(download(), timeout=0.3)
except TimeoutError:
    print('Timeout')""")
t('''Schreibe eine Funktion `antwort_oder_standard(dauer)`: Sie wartet mit `asyncio.sleep(dauer)` und gibt dann `'Antwort'` zurück, aber nur wenn das innerhalb von 0,3 Sekunden klappt (`wait_for`). Sonst gibt sie `'Standard'` zurück.
Gib das Ergebnis für `0.1` und für `1` aus.''',
  given='import asyncio\n', body="""async def antwort_oder_standard(dauer):
    try:
        await asyncio.wait_for(asyncio.sleep(dauer), timeout=0.3)
        return 'Antwort'
    except TimeoutError:
        return 'Standard'

print(await antwort_oder_standard(0.1))
print(await antwort_oder_standard(1))""")
task('''Die Zelle wartet eine volle Sekunde, obwohl höchstens `0.3` Sekunden erlaubt sind. Verbessere den Code mit `wait_for`, sodass bei Überschreiten `Zu langsam` ausgegeben wird (und die Dauer `0`).''',
     zelle="""import asyncio
import time

async def lade():
    await asyncio.sleep(1)
    return 'Inhalt'

start = time.perf_counter()
print(await lade())
print('Dauer:', round(time.perf_counter() - start), 's')""",
     solution="""import asyncio
import time

async def lade():
    await asyncio.sleep(1)
    return 'Inhalt'

start = time.perf_counter()
try:
    print(await asyncio.wait_for(lade(), timeout=0.3))
except TimeoutError:
    print('Zu langsam')
print('Dauer:', round(time.perf_counter() - start), 's')""")

# ---------------------------------------------------------------- 2
sec('Tasks abbrechen')
expl('''#### `task.cancel()`

Einen laufenden Task kann man mit `task.cancel()` **abbrechen**. Der Abbruch wird dem Task an seiner aktuellen `await`-Stelle als `asyncio.CancelledError` zugestellt.
Wartet man danach mit `await task`, entsteht dieser Fehler auch dort. Man fängt ihn ab.

`task.cancelled()` ist `True`, wenn der Task abgebrochen wurde.''',
     """import asyncio

async def lang():
    print('Start')
    await asyncio.sleep(5)
    print('Fertig')

aufgabe = asyncio.create_task(lang())
await asyncio.sleep(0.2)
aufgabe.cancel()
try:
    await aufgabe
except asyncio.CancelledError:
    print('Task wurde abgebrochen')
print('abgebrochen?', aufgabe.cancelled())""")
expl('''#### Aufräumen beim Abbruch

Die Coroutine kann den Abbruch selbst abfangen, um aufzuräumen (oder einfach mit `finally`). Wichtig: Wer `CancelledError` abfängt, muss ihn mit `raise` **weitergeben**.
Sonst läuft der Task einfach weiter, als wäre nichts gewesen.''',
     """import asyncio

async def arbeite(name):
    try:
        print(name, 'beginnt')
        await asyncio.sleep(5)
    except asyncio.CancelledError:
        print(name, 'wird abgebrochen, räumt auf')
        raise
    finally:
        print(name, 'ist beendet')

aufgabe = asyncio.create_task(arbeite('Task'))
await asyncio.sleep(0.2)
aufgabe.cancel()
try:
    await aufgabe
except asyncio.CancelledError:
    print('abgebrochen:', aufgabe.cancelled())""")
expl('''#### Alle übrigen abbrechen

Typisch ist ein Rennen: Der Schnellste gewinnt, die anderen werden abgebrochen. Mit `asyncio.wait(..., return_when=asyncio.FIRST_COMPLETED)` (siehe `asyncio_tasks`) bekommt man den ersten fertigen Task
und die noch offenen, die man dann abbricht.''',
     """import asyncio

async def lauf(name, zeit):
    try:
        await asyncio.sleep(zeit)
        return name
    except asyncio.CancelledError:
        print(name, 'aufgegeben')
        raise

tasks = []
for name, zeit in [('Ali', 0.5), ('Bea', 0.1), ('Cem', 0.8)]:
    tasks.append(asyncio.create_task(lauf(name, zeit)))

fertig, offen = await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)
for aufgabe in fertig:
    print('Sieger:', aufgabe.result())
for aufgabe in offen:
    aufgabe.cancel()
await asyncio.wait(offen)
print('Rennen beendet')""")
expl('''#### `CancelledError` ist anders

`asyncio.CancelledError` ist **kein** gewöhnlicher Fehler: Ein einfaches `except Exception:` fängt ihn nicht. Das ist Absicht, damit man einen Abbruch nicht aus Versehen verschluckt.''',
     """import asyncio

async def f():
    try:
        await asyncio.sleep(5)
    except Exception:
        print('wird nie ausgegeben')

aufgabe = asyncio.create_task(f())
await asyncio.sleep(0.1)
aufgabe.cancel()
try:
    await aufgabe
except asyncio.CancelledError:
    print('trotzdem abgebrochen')""")

predict("""import asyncio

async def f():
    print('A')
    await asyncio.sleep(1)
    print('B')

aufgabe = asyncio.create_task(f())
await asyncio.sleep(0.2)
aufgabe.cancel()
try:
    await aufgabe
except asyncio.CancelledError:
    print('C')
print(aufgabe.cancelled())""", erklaerung='''Der Task beginnt mit `A` und wartet dann 1 Sekunde. Nach 0,2 Sekunden wird er abgebrochen, `B` kommt nie. `await aufgabe` löst den `CancelledError` aus (`C`). `cancelled()` ist `True`.

```
A
C
True
```''')
predict("""import asyncio

async def f():
    try:
        await asyncio.sleep(1)
    finally:
        print('X')

aufgabe = asyncio.create_task(f())
await asyncio.sleep(0.1)
aufgabe.cancel()
try:
    await aufgabe
except asyncio.CancelledError:
    print('Y')""", erklaerung='''Beim Abbruch wird zuerst das `finally` der Coroutine ausgeführt (`X`). Danach kommt der `CancelledError` bei `await aufgabe` an (`Y`).

```
X
Y
```''')
predict("""import asyncio

async def f():
    await asyncio.sleep(0.1)
    return 'ok'

aufgabe = asyncio.create_task(f())
await asyncio.sleep(0.5)
aufgabe.cancel()
print(aufgabe.cancelled())
print(aufgabe.result())""", erklaerung='''Der Task war nach 0,1 Sekunden schon fertig. `cancel()` kommt zu spät und ändert nichts: `cancelled()` ist `False`, und `result()` liefert `ok`.

```
False
ok
```''')
t('''Die Coroutine `lang()` ist vorgegeben. Starte sie als Task, warte `0.2` Sekunden, brich den Task ab und fange den `CancelledError` ab. Gib `Abgebrochen` und dann `aufgabe.cancelled()` aus.''',
  given="""import asyncio

async def lang():
    await asyncio.sleep(5)
    print('wird nie ausgegeben')
""", body="""aufgabe = asyncio.create_task(lang())
await asyncio.sleep(0.2)
aufgabe.cancel()
try:
    await aufgabe
except asyncio.CancelledError:
    print('Abgebrochen')
print(aufgabe.cancelled())""")
t('''Schreibe eine Coroutine `zaehle()`, die in einer Endlosschleife (`while True:`) die Zahlen `1`, `2`, `3`, ... ausgibt und nach jeder 0,2 Sekunden wartet.
Starte sie als Task, warte `0.5` Sekunden (es erscheinen drei Zahlen), brich sie dann ab und gib `Gestoppt` aus.''',
  given='import asyncio\n', body="""async def zaehle():
    n = 1
    while True:
        print(n)
        n += 1
        await asyncio.sleep(0.2)

aufgabe = asyncio.create_task(zaehle())
await asyncio.sleep(0.5)
aufgabe.cancel()
try:
    await aufgabe
except asyncio.CancelledError:
    print('Gestoppt')""")
t('''Die Coroutine `arbeit(name)` ist vorgegeben und räumt in einem `finally` auf. Starte sie als Task, breche sie nach `0.2` Sekunden ab und fange den `CancelledError`.
Die Ausgabe zeigt zuerst das Aufräumen, dann `Abbruch gemeldet`.''',
  given="""import asyncio

async def arbeit(name):
    try:
        await asyncio.sleep(5)
    finally:
        print(name, 'räumt auf')
""", body="""aufgabe = asyncio.create_task(arbeit('Task A'))
await asyncio.sleep(0.2)
aufgabe.cancel()
try:
    await aufgabe
except asyncio.CancelledError:
    print('Abbruch gemeldet')""")
t('''Die Coroutine `lauf(name, zeit)` ist vorgegeben. Starte die Läufer `('Ali', 0.5)`, `('Bea', 0.1)` und `('Cem', 0.8)` als Tasks. Warte mit `FIRST_COMPLETED`, gib `Sieger: <Name>` aus
und brich dann alle noch offenen Tasks ab. Warte mit `await asyncio.wait(offen)`, bis sie beendet sind, und gib dann `Rennen beendet` aus.''',
  given="""import asyncio

async def lauf(name, zeit):
    await asyncio.sleep(zeit)
    return name
""", body="""tasks = []
for name, zeit in [('Ali', 0.5), ('Bea', 0.1), ('Cem', 0.8)]:
    tasks.append(asyncio.create_task(lauf(name, zeit)))

fertig, offen = await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)
for aufgabe in fertig:
    print('Sieger:', aufgabe.result())
for aufgabe in offen:
    aufgabe.cancel()
await asyncio.wait(offen)
print('Rennen beendet')""")
t('''Starte zwei Tasks `lade('A', 0.1)` und `lade('B', 2)` (die Coroutine `lade(name, dauer)` ist vorgegeben und gibt den Namen zurück). Warte `0.5` Sekunden. Gib dann für beide Tasks aus, ob sie `done()` sind,
und breche danach nur die nicht fertigen ab (`if not aufgabe.done():`). Gib am Ende `cancelled()` für beide aus.''',
  given="""import asyncio

async def lade(name, dauer):
    await asyncio.sleep(dauer)
    return name
""", body="""t1 = asyncio.create_task(lade('A', 0.1))
t2 = asyncio.create_task(lade('B', 2))
await asyncio.sleep(0.5)
print(t1.done(), t2.done())
for aufgabe in [t1, t2]:
    if not aufgabe.done():
        aufgabe.cancel()
await asyncio.wait([t2])
print(t1.cancelled(), t2.cancelled())""")
task('''Der Task fängt den Abbruch ab, gibt aber `CancelledError` nicht weiter. Deshalb läuft er nach dem `cancel()` einfach weiter und die Zelle gibt `cancelled? False` aus.
Verbessere die Coroutine so, dass der Abbruch klappt (`cancelled? True`).''',
     zelle="""import asyncio

async def arbeit():
    try:
        await asyncio.sleep(5)
    except asyncio.CancelledError:
        print('räume auf')

aufgabe = asyncio.create_task(arbeit())
await asyncio.sleep(0.1)
aufgabe.cancel()
try:
    await aufgabe
except asyncio.CancelledError:
    pass
print('cancelled?', aufgabe.cancelled())""",
     solution="""import asyncio

async def arbeit():
    try:
        await asyncio.sleep(5)
    except asyncio.CancelledError:
        print('räume auf')
        raise

aufgabe = asyncio.create_task(arbeit())
await asyncio.sleep(0.1)
aufgabe.cancel()
try:
    await aufgabe
except asyncio.CancelledError:
    pass
print('cancelled?', aufgabe.cancelled())""")

# ---------------------------------------------------------------- 3
sec('Fehler in Tasks')
expl('''#### Wiederholung: Fehler beim `await`

Wirft die Coroutine eines Tasks einen Fehler, kommt er beim `await task` an und lässt sich mit `try` und `except` abfangen.
Zusätzlich kann man mit `task.exception()` nachsehen, **ob** der Task mit einem Fehler beendet wurde. Das geht erst, wenn der Task fertig ist:
`task.exception()` gibt den Fehler zurück oder `None`, wenn es keinen gab.''',
     """import asyncio

async def teile(a, b):
    await asyncio.sleep(0.1)
    if b == 0:
        raise ValueError('Division durch null')
    return a / b

t1 = asyncio.create_task(teile(6, 3))
t2 = asyncio.create_task(teile(1, 0))
await asyncio.wait([t1, t2])

print(t1.exception())
print(type(t2.exception()).__name__, t2.exception())
print(t1.result())""")
expl('''#### Ein Fehler in einer `TaskGroup`

Ohne `return_exceptions=True` wirft `gather` den **ersten** Fehler. Die anderen Aufgaben laufen aber weiter, ohne dass man es merkt.
Mit der `TaskGroup` ist das sauberer: Geht ein Task schief, werden alle anderen in der Gruppe **abgebrochen**.''',
     """import asyncio

async def langsam():
    try:
        await asyncio.sleep(1)
        print('langsam fertig')
    except asyncio.CancelledError:
        print('langsam wurde abgebrochen')
        raise

async def kaputt():
    await asyncio.sleep(0.1)
    raise ValueError('kaputt')

try:
    async with asyncio.TaskGroup() as gruppe:
        gruppe.create_task(langsam())
        gruppe.create_task(kaputt())
except ExceptionGroup:
    print('Die Gruppe hat einen Fehler gemeldet')""")
expl('''#### ExceptionGroup und `except*` (Leistungsfach)

Die `TaskGroup` bricht beim **ersten** Fehler alle anderen Tasks ab. Scheitern mehrere Tasks aber **im selben Augenblick**, bündelt die Gruppe ihre Fehler in einer **`ExceptionGroup`**.
Die Fehler stehen in `.exceptions`.

Mit `except*` (mit Stern) fängt man bestimmte Fehlertypen aus der Gruppe heraus. Ein `except*`-Block bekommt eine Gruppe, die nur die passenden Fehler enthält.
Es dürfen mehrere `except*`-Blöcke nacheinander stehen, auch für verschiedene Typen.

Im Beispiel werfen die Tasks sofort einen Fehler, ohne vorher zu warten. Damit sind alle drei im selben Augenblick gescheitert.''',
     """import asyncio

async def wirf(fehler):
    raise fehler

try:
    async with asyncio.TaskGroup() as gruppe:
        gruppe.create_task(wirf(ValueError('Wert falsch')))
        gruppe.create_task(wirf(KeyError('Schlüssel')))
        gruppe.create_task(wirf(ValueError('noch ein Wert')))
except* ValueError as gruppe_v:
    print('ValueError:', len(gruppe_v.exceptions))
    for fehler in gruppe_v.exceptions:
        print(' ', fehler)
except* KeyError as gruppe_k:
    print('KeyError:', len(gruppe_k.exceptions))""")

predict("""import asyncio

async def f(x):
    await asyncio.sleep(0.1)
    if x == 0:
        raise ValueError('null')
    return x

t1 = asyncio.create_task(f(5))
t2 = asyncio.create_task(f(0))
await asyncio.wait([t1, t2])
print(t1.exception())
print(type(t2.exception()).__name__)""", erklaerung='''Beide Tasks sind fertig. `t1` hatte keinen Fehler: `exception()` gibt `None` zurück. Bei `t2` ist es ein `ValueError`.

```
None
ValueError
```''')
predict("""import asyncio

async def gut():
    try:
        await asyncio.sleep(1)
        print('gut fertig')
    except asyncio.CancelledError:
        print('gut abgebrochen')
        raise

async def schlecht():
    await asyncio.sleep(0.1)
    raise ValueError('x')

try:
    async with asyncio.TaskGroup() as gruppe:
        gruppe.create_task(gut())
        gruppe.create_task(schlecht())
except* ValueError:
    print('ValueError gefangen')
print('Ende')""", erklaerung='''Nach 0,1 Sekunden scheitert `schlecht`. Die Gruppe bricht daraufhin `gut` ab (`gut abgebrochen`). Danach melden `except*` den `ValueError` (`ValueError gefangen`), und das Programm geht weiter.
`gut fertig` wird nie ausgegeben.

```
gut abgebrochen
ValueError gefangen
Ende
```''')
t('''Die Coroutine `hole(name)` ist vorgegeben (wirft `KeyError` für unbekannte Namen). Starte Tasks für `'Ali'` und `'Zoe'`, warte mit `asyncio.wait` auf beide und gib mit `exception()` für jeden Task `<name>: ok` oder `<name>: Fehler` aus.''',
  given="""import asyncio

punkte = {'Ali': 12, 'Bea': 17}

async def hole(name):
    await asyncio.sleep(0.1)
    return punkte[name]
""", body="""namen = ['Ali', 'Zoe']
tasks = []
for name in namen:
    tasks.append(asyncio.create_task(hole(name)))
await asyncio.wait(tasks)

for i in range(len(namen)):
    if tasks[i].exception() is None:
        print(namen[i] + ': ok')
    else:
        print(namen[i] + ': Fehler')""")
t('''Die Coroutinen `gut()` und `kaputt()` sind vorgegeben. Starte beide in einer `TaskGroup` und fange mit `except ExceptionGroup:` den Fehler ab. Gib dann `Fehler in der Gruppe` aus.''',
  given="""import asyncio

async def gut():
    await asyncio.sleep(0.5)

async def kaputt():
    await asyncio.sleep(0.1)
    raise ValueError('kaputt')
""", body="""try:
    async with asyncio.TaskGroup() as gruppe:
        gruppe.create_task(gut())
        gruppe.create_task(kaputt())
except ExceptionGroup:
    print('Fehler in der Gruppe')""")
t('''Die Coroutine `teile(a, b)` ist vorgegeben. Starte `teile(1, 0)` und `teile(4, 2)` in einer `TaskGroup`. Fange den `ZeroDivisionError` mit `except*` ab und gib `Division durch null` aus.''',
  given="""import asyncio

async def teile(a, b):
    await asyncio.sleep(0.1)
    return a / b
""", body="""try:
    async with asyncio.TaskGroup() as gruppe:
        gruppe.create_task(teile(1, 0))
        gruppe.create_task(teile(4, 2))
except* ZeroDivisionError:
    print('Division durch null')""")
t('''Die Coroutine `wirf(fehler)` ist vorgegeben und wirft sofort den übergebenen Fehler. Starte in einer `TaskGroup` drei Tasks, die `ValueError('a')`, `KeyError('b')` und `ValueError('c')` werfen.
Gib mit `except* ValueError` die **Anzahl** der `ValueError` aus (`ValueError: 2`) und mit `except* KeyError` die Anzahl der `KeyError`.''',
  given="""import asyncio

async def wirf(fehler):
    raise fehler
""", body="""try:
    async with asyncio.TaskGroup() as gruppe:
        gruppe.create_task(wirf(ValueError('a')))
        gruppe.create_task(wirf(KeyError('b')))
        gruppe.create_task(wirf(ValueError('c')))
except* ValueError as g:
    print('ValueError:', len(g.exceptions))
except* KeyError as g:
    print('KeyError:', len(g.exceptions))""")
t('''Die Coroutine `lade(seite, dauer)` ist vorgegeben (wirft nach der Wartezeit einen `ValueError`, wenn der Name leer ist). Lade die Seiten aus `daten` in einer `TaskGroup`.
Gib im `except*`-Block `Fehler beim Laden` aus. Gib danach die Ergebnisse der Tasks aus, die erfolgreich waren (`aufgabe.done() and not aufgabe.cancelled() and aufgabe.exception() is None`).
Der Task für `'Plan'` wird abgebrochen, weil der Fehler früher auftritt.''',
  given="""import asyncio

async def lade(seite, dauer):
    await asyncio.sleep(dauer)
    if seite == '':
        raise ValueError('leerer Name')
    return len(seite)

daten = [('Start', 0.1), ('', 0.3), ('Plan', 0.6)]
""", body="""tasks = []
try:
    async with asyncio.TaskGroup() as gruppe:
        for seite, dauer in daten:
            tasks.append(gruppe.create_task(lade(seite, dauer)))
except* ValueError:
    print('Fehler beim Laden')

for aufgabe in tasks:
    if aufgabe.done() and not aufgabe.cancelled() and aufgabe.exception() is None:
        print(aufgabe.result())""")

# ---------------------------------------------------------------- 4
sec('Lock: gemeinsame Daten schützen')
expl('''#### Das Problem: gemeinsame Daten

Mehrere Coroutinen greifen oft auf **dieselben Daten** zu, zum Beispiel auf einen Kontostand. Das ist heikel, wenn zwischen **Lesen** und **Schreiben** ein `await` liegt:
Währenddessen kann eine andere Coroutine dieselben Daten lesen.

Im Beispiel heben zwei Personen gleichzeitig Geld von einem Konto mit 100 € ab (30 € und 50 €). Es müssten 20 € übrig bleiben.''',
     """import asyncio

konto = {'stand': 100}

async def abheben(betrag):
    stand = konto['stand']
    await asyncio.sleep(0.1)
    konto['stand'] = stand - betrag

await asyncio.gather(abheben(30), abheben(50))
print('Kontostand:', konto['stand'])""")
expl('''#### Die Lösung: `asyncio.Lock`

Ein `Lock` (Sperre) sorgt dafür, dass immer nur **eine** Coroutine im geschützten Bereich ist. Man benutzt es mit `async with sperre:`.
Wer die Sperre nicht bekommt, wartet, bis sie frei ist. Die Wartenden kommen in der Reihenfolge dran, in der sie angekommen sind.

Man legt das `Lock` **einmal** an und teilt es zwischen den Coroutinen.''',
     """import asyncio

konto = {'stand': 100}
sperre = asyncio.Lock()

async def abheben(betrag):
    async with sperre:
        stand = konto['stand']
        await asyncio.sleep(0.1)
        konto['stand'] = stand - betrag

await asyncio.gather(abheben(30), abheben(50))
print('Kontostand:', konto['stand'])""")
expl('''#### Wartende sehen

Während eine Coroutine die Sperre hält, stehen die anderen am Eingang. Man sieht es an den Ausgaben.''',
     """import asyncio

sperre = asyncio.Lock()

async def schalter(name):
    print(name, 'stellt sich an')
    async with sperre:
        print(name, 'wird bedient')
        await asyncio.sleep(0.2)
        print(name, 'ist fertig')

await asyncio.gather(schalter('Ali'), schalter('Bea'), schalter('Cem'))""")
expl('''#### Wann braucht man ein `Lock`?

Nur wenn zwischen dem Lesen und dem Schreiben ein `await` liegt. Code ohne `await` in der Mitte kann nicht unterbrochen werden, dort braucht man kein `Lock`.
Ein `Lock` macht außerdem alles im geschützten Bereich **nacheinander**: Bei vielen Coroutinen geht dort die Gleichzeitigkeit verloren, deshalb schützt man nur das Nötigste.''', None)

predict("""import asyncio

zaehler = {'n': 0}

async def erhoehe():
    wert = zaehler['n']
    await asyncio.sleep(0.1)
    zaehler['n'] = wert + 1

await asyncio.gather(erhoehe(), erhoehe(), erhoehe())
print(zaehler['n'])""", erklaerung='''Alle drei Coroutinen lesen zuerst `0`, dann warten sie. Danach schreibt jede `0 + 1`, also `1`. Zwei Erhöhungen gehen verloren.

```
1
```''')
predict("""import asyncio

zaehler = {'n': 0}
sperre = asyncio.Lock()

async def erhoehe():
    async with sperre:
        wert = zaehler['n']
        await asyncio.sleep(0.1)
        zaehler['n'] = wert + 1

await asyncio.gather(erhoehe(), erhoehe(), erhoehe())
print(zaehler['n'])""", erklaerung='''Mit dem `Lock` kommt immer nur eine Coroutine auf einmal in den Block. Jede liest den Stand, den die vorige geschrieben hat. Das Ergebnis ist `3`.

```
3
```''')
predict("""import asyncio

sperre = asyncio.Lock()

async def f(name):
    async with sperre:
        print(name, 'drin')
        await asyncio.sleep(0.1)
        print(name, 'raus')

await asyncio.gather(f('a'), f('b'))""", erklaerung='''`a` bekommt die Sperre zuerst. Erst wenn `a` den Block verlässt, darf `b` hinein. Die Blöcke laufen also nacheinander.

```
a drin
a raus
b drin
b raus
```''')
t('''Das Dictionary `lager` enthält 10 Stück. Die Coroutine `verkaufe(anzahl)` liest den Bestand, wartet 0,1 Sekunden und schreibt `bestand - anzahl` zurück. Lege ein `Lock` an und schütze damit das Lesen und Schreiben.
Verkaufe gleichzeitig `3` und `4` Stück und gib den Bestand aus (`Bestand: 3`).''',
  given='import asyncio\n\nlager = {\'bestand\': 10}\n', body="""sperre = asyncio.Lock()

async def verkaufe(anzahl):
    async with sperre:
        bestand = lager['bestand']
        await asyncio.sleep(0.1)
        lager['bestand'] = bestand - anzahl

await asyncio.gather(verkaufe(3), verkaufe(4))
print('Bestand:', lager['bestand'])""")
t('''Schreibe eine Coroutine `kasse(name)`, die mit einem gemeinsamen `Lock` `<name> wird bedient` ausgibt, `0.2` Sekunden wartet und `<name> ist fertig` ausgibt.
Lasse `'Ali'`, `'Bea'` und `'Cem'` gleichzeitig zur Kasse gehen.''',
  given='import asyncio\n', body="""sperre = asyncio.Lock()

async def kasse(name):
    async with sperre:
        print(name, 'wird bedient')
        await asyncio.sleep(0.2)
        print(name, 'ist fertig')

await asyncio.gather(kasse('Ali'), kasse('Bea'), kasse('Cem'))""")
t('''Fünf Coroutinen tragen sich gleichzeitig in die Liste `eintraege` ein. Jede liest zuerst die Länge der Liste (`laenge = len(eintraege)`), wartet 0,1 Sekunden und hängt dann `laenge + 1` an.
Schütze den Ablauf mit einem `Lock`. Gib die Liste aus (`[1, 2, 3, 4, 5]`).''',
  given='import asyncio\n\neintraege = []\n', body="""sperre = asyncio.Lock()

async def eintragen():
    async with sperre:
        laenge = len(eintraege)
        await asyncio.sleep(0.1)
        eintraege.append(laenge + 1)

aufgaben = []
for i in range(5):
    aufgaben.append(eintragen())
await asyncio.gather(*aufgaben)
print(eintraege)""")
task('''Zwei Personen überweisen gleichzeitig Geld auf dasselbe Konto. Es sollten 100 + 20 + 30 = 150 € herauskommen, aber die Zelle gibt `Kontostand: 130` aus.
Verbessere den Code mit einem `Lock`.''',
     zelle="""import asyncio

konto = {'stand': 100}

async def einzahlen(betrag):
    stand = konto['stand']
    await asyncio.sleep(0.1)
    konto['stand'] = stand + betrag

await asyncio.gather(einzahlen(20), einzahlen(30))
print('Kontostand:', konto['stand'])""",
     solution="""import asyncio

konto = {'stand': 100}
sperre = asyncio.Lock()

async def einzahlen(betrag):
    async with sperre:
        stand = konto['stand']
        await asyncio.sleep(0.1)
        konto['stand'] = stand + betrag

await asyncio.gather(einzahlen(20), einzahlen(30))
print('Kontostand:', konto['stand'])""")
t('''Die Coroutine `arbeite(name)` benutzt das vorgegebene `Lock` und braucht darin 1 Sekunde. Starte drei Coroutinen gleichzeitig und gib die Gesamtdauer aus (`Dauer: 3 s`, weil sie nacheinander im Block sind).''',
  given="""import asyncio
import time

sperre = asyncio.Lock()

async def arbeite(name):
    async with sperre:
        await asyncio.sleep(1)
""", body="""start = time.perf_counter()
await asyncio.gather(arbeite('a'), arbeite('b'), arbeite('c'))
print('Dauer:', round(time.perf_counter() - start), 's')""")

# ---------------------------------------------------------------- 5
sec('Semaphore: die Zahl der Gleichzeitigen begrenzen')
expl('''#### `asyncio.Semaphore`

Manchmal sollen **mehrere**, aber nicht **beliebig viele** Coroutinen gleichzeitig arbeiten: zum Beispiel höchstens zwei Downloads auf einmal, damit der Server nicht überlastet wird.
Eine `Semaphore(n)` lässt höchstens `n` Coroutinen gleichzeitig in den Block. Sie benutzt man wie das `Lock` mit `async with`.
Ein `Lock` ist eine Semaphore mit `n = 1`.

Im Beispiel dürfen von vier Aufgaben nur zwei gleichzeitig laufen. Die Ausgabe zeigt, wann die nächste dran ist.''',
     """import asyncio

platz = asyncio.Semaphore(2)

async def arbeite(name, dauer):
    async with platz:
        print(name, 'beginnt')
        await asyncio.sleep(dauer)
        print(name, 'fertig')

await asyncio.gather(arbeite('A', 0.2), arbeite('B', 0.4), arbeite('C', 0.3), arbeite('D', 0.3))""")
expl('''#### Die Dauer

Vier Aufgaben zu je einer Sekunde brauchen mit einer `Semaphore(2)` zwei Sekunden: Es laufen immer zwei gleichzeitig, danach die nächsten zwei.
Mit `Semaphore(1)` wären es vier Sekunden, mit `Semaphore(4)` nur eine.''',
     """import asyncio
import time

async def arbeite(platz):
    async with platz:
        await asyncio.sleep(1)

for n in [1, 2, 4]:
    platz = asyncio.Semaphore(n)
    start = time.perf_counter()
    aufgaben = []
    for i in range(4):
        aufgaben.append(arbeite(platz))
    await asyncio.gather(*aufgaben)
    print('Semaphore', n, '- Dauer:', round(time.perf_counter() - start), 's')""")
expl('''#### Wie viele sind gerade drin?

Mit einem Zähler kann man prüfen, dass die Grenze eingehalten wird. Der Zähler wird beim Betreten größer und beim Verlassen kleiner. Wir merken uns den höchsten Wert.''',
     """import asyncio

platz = asyncio.Semaphore(3)
zaehler = {'aktiv': 0, 'maximum': 0}

async def arbeite():
    async with platz:
        zaehler['aktiv'] += 1
        if zaehler['aktiv'] > zaehler['maximum']:
            zaehler['maximum'] = zaehler['aktiv']
        await asyncio.sleep(0.1)
        zaehler['aktiv'] -= 1

aufgaben = []
for i in range(10):
    aufgaben.append(arbeite())
await asyncio.gather(*aufgaben)
print('Höchstens gleichzeitig:', zaehler['maximum'])""")

predict("""import asyncio
import time

platz = asyncio.Semaphore(2)

async def f():
    async with platz:
        await asyncio.sleep(1)

start = time.perf_counter()
await asyncio.gather(f(), f(), f(), f())
print(round(time.perf_counter() - start))""", erklaerung='''Zwei Aufgaben dürfen gleichzeitig in den Block. Sie brauchen 1 Sekunde. Danach folgen die anderen zwei, wieder 1 Sekunde. Zusammen sind es 2 Sekunden.

```
2
```''')
predict("""import asyncio
import time

platz = asyncio.Semaphore(1)

async def f():
    async with platz:
        await asyncio.sleep(1)

start = time.perf_counter()
await asyncio.gather(f(), f(), f())
print(round(time.perf_counter() - start))""", erklaerung='''Eine `Semaphore(1)` verhält sich wie ein `Lock`: Die drei Aufgaben laufen nacheinander, 3 Sekunden.

```
3
```''')
predict("""import asyncio
import time

platz = asyncio.Semaphore(5)

async def f():
    async with platz:
        await asyncio.sleep(1)

start = time.perf_counter()
await asyncio.gather(f(), f(), f())
print(round(time.perf_counter() - start))""", erklaerung='''Es sind 5 Plätze frei, aber nur 3 Aufgaben da. Alle drei laufen gleichzeitig: 1 Sekunde.

```
1
```''')
t('''Die Coroutine `lade(nr)` ist vorgegeben (eine Sekunde, ohne Ausgabe). Lege eine `Semaphore(2)` an und benutze sie in `lade_begrenzt(nr)`. Lade damit sechs Seiten (`range(6)`) gleichzeitig.
Gib die Dauer aus (`Dauer: 3 s`).''',
  given="""import asyncio
import time

async def lade(nr):
    await asyncio.sleep(1)
""", body="""platz = asyncio.Semaphore(2)

async def lade_begrenzt(nr):
    async with platz:
        await lade(nr)

start = time.perf_counter()
aufgaben = []
for nr in range(6):
    aufgaben.append(lade_begrenzt(nr))
await asyncio.gather(*aufgaben)
print('Dauer:', round(time.perf_counter() - start), 's')""")
t('''Die Coroutine `arbeite(name, dauer)` ist vorgegeben (sie wartet `dauer` Sekunden). Schreibe `begrenzt(name, dauer)`, die `arbeite` in einer `Semaphore(2)` ausführt und dabei `<name> beginnt` und `<name> fertig` ausgibt.
Starte gleichzeitig `('A', 0.2)`, `('B', 0.4)`, `('C', 0.3)`, `('D', 0.3)`.''',
  given="""import asyncio

async def arbeite(name, dauer):
    await asyncio.sleep(dauer)
""", body="""platz = asyncio.Semaphore(2)

async def begrenzt(name, dauer):
    async with platz:
        print(name, 'beginnt')
        await arbeite(name, dauer)
        print(name, 'fertig')

await asyncio.gather(begrenzt('A', 0.2), begrenzt('B', 0.4), begrenzt('C', 0.3), begrenzt('D', 0.3))""")
t('''Zehn Aufgaben laufen mit einer `Semaphore(4)`. Zähle mit dem Dictionary `zaehler` mit, wie viele gleichzeitig im Block sind (`aktiv`) und wie hoch der Wert maximal war (`maximum`), und gib das Maximum aus (`Höchstens gleichzeitig: 4`).''',
  given="""import asyncio

zaehler = {'aktiv': 0, 'maximum': 0}
platz = asyncio.Semaphore(4)
""", body="""async def arbeite():
    async with platz:
        zaehler['aktiv'] += 1
        if zaehler['aktiv'] > zaehler['maximum']:
            zaehler['maximum'] = zaehler['aktiv']
        await asyncio.sleep(0.1)
        zaehler['aktiv'] -= 1

aufgaben = []
for i in range(10):
    aufgaben.append(arbeite())
await asyncio.gather(*aufgaben)
print('Höchstens gleichzeitig:', zaehler['maximum'])""")
t('''Vergleiche die Dauer für acht Aufgaben (je eine Sekunde, `arbeite(platz)` ist vorgegeben) mit `Semaphore(2)`, `Semaphore(4)` und `Semaphore(8)`. Gib für jede eine Zeile `<n>: <Dauer> s` aus (`2: 4 s` usw.).''',
  given="""import asyncio
import time

async def arbeite(platz):
    async with platz:
        await asyncio.sleep(1)
""", body="""for n in [2, 4, 8]:
    platz = asyncio.Semaphore(n)
    start = time.perf_counter()
    aufgaben = []
    for i in range(8):
        aufgaben.append(arbeite(platz))
    await asyncio.gather(*aufgaben)
    print(f'{n}: {round(time.perf_counter() - start)} s')""")
task('''Es sollen höchstens **zwei** Drucker gleichzeitig laufen, aber alle vier Dokumente werden zusammen gedruckt (Dauer: `1` statt `2`). Verbessere den Code mit einer `Semaphore`.''',
     zelle="""import asyncio
import time

async def drucke(nr):
    await asyncio.sleep(1)

start = time.perf_counter()
await asyncio.gather(drucke(1), drucke(2), drucke(3), drucke(4))
print('Dauer:', round(time.perf_counter() - start), 's')""",
     solution="""import asyncio
import time

platz = asyncio.Semaphore(2)

async def drucke(nr):
    async with platz:
        await asyncio.sleep(1)

start = time.perf_counter()
await asyncio.gather(drucke(1), drucke(2), drucke(3), drucke(4))
print('Dauer:', round(time.perf_counter() - start), 's')""")

# ---------------------------------------------------------------- 6
sec('Event: auf ein Signal warten')
expl('''#### `asyncio.Event`

Ein `Event` ist ein **Signal**. Coroutinen können mit `await ereignis.wait()` darauf warten. Sobald jemand `ereignis.set()` aufruft, werden **alle Wartenden** freigegeben.
Das Signal bleibt gesetzt: Wer später `wait()` aufruft, wartet nicht mehr. `ereignis.is_set()` fragt den Zustand ab, `ereignis.clear()` setzt das Signal zurück.

Typisches Beispiel: der Startschuss bei einem Rennen.''',
     """import asyncio

startschuss = asyncio.Event()

async def laeufer(name):
    print(name, 'wartet')
    await startschuss.wait()
    print(name, 'läuft')

async def starter():
    await asyncio.sleep(0.3)
    print('Los!')
    startschuss.set()

await asyncio.gather(laeufer('Ali'), laeufer('Bea'), starter())""")
expl('''#### `is_set()`, `set()` und `clear()`''',
     """import asyncio

signal = asyncio.Event()
print(signal.is_set())
signal.set()
print(signal.is_set())
await signal.wait()
print('wait() hat nicht gewartet')
signal.clear()
print(signal.is_set())""")
expl('''#### Ein Event als Zeichen „Daten sind da“

Eine Coroutine lädt Daten, eine andere wartet darauf. Das `Event` meldet, wann die Daten bereit sind.''',
     """import asyncio

daten = []
bereit = asyncio.Event()

async def lade():
    await asyncio.sleep(0.2)
    daten.append('Stundenplan')
    bereit.set()

async def zeige():
    await bereit.wait()
    print('Zeige:', daten[0])

await asyncio.gather(zeige(), lade())""")

predict("""import asyncio

signal = asyncio.Event()

async def a():
    print('a wartet')
    await signal.wait()
    print('a weiter')

async def b():
    await asyncio.sleep(0.1)
    print('b setzt')
    signal.set()

await asyncio.gather(a(), b())""", erklaerung='''`a` beginnt und wartet. `b` wartet 0,1 Sekunden, gibt `b setzt` aus und setzt das Signal. Danach läuft `a` weiter.

```
a wartet
b setzt
a weiter
```''')
predict("""import asyncio

signal = asyncio.Event()
signal.set()

async def f():
    print('1')
    await signal.wait()
    print('2')

await f()
print(signal.is_set())""", erklaerung='''Das Signal ist schon gesetzt. `wait()` wartet dann nicht, `f` läuft in einem Zug durch. Das Signal bleibt gesetzt.

```
1
2
True
```''')
predict("""import asyncio

signal = asyncio.Event()

async def a(name):
    await signal.wait()
    print(name)

async def b():
    await asyncio.sleep(0.1)
    signal.set()

await asyncio.gather(a('x'), a('y'), a('z'), b())""", erklaerung='''Alle drei warten auf dasselbe Signal. Sobald `b` es setzt, werden alle freigegeben, und zwar in der Reihenfolge, in der sie zu warten begonnen haben.

```
x
y
z
```''')
t('''Schreibe eine Coroutine `laeufer(name)`, die `<name> wartet` ausgibt, mit `await startschuss.wait()` auf das Signal wartet und dann `<name> läuft` ausgibt.
Eine Coroutine `starter()` wartet `0.2` Sekunden, gibt `Los!` aus und setzt das Signal. Starte `'Ali'`, `'Bea'`, `'Cem'` und `starter()` gleichzeitig.''',
  given='import asyncio\n\nstartschuss = asyncio.Event()\n', body="""async def laeufer(name):
    print(name, 'wartet')
    await startschuss.wait()
    print(name, 'läuft')

async def starter():
    await asyncio.sleep(0.2)
    print('Los!')
    startschuss.set()

await asyncio.gather(laeufer('Ali'), laeufer('Bea'), laeufer('Cem'), starter())""")
t('''Das Signal `gruen` ist vorgegeben. Gib mit `is_set()` seinen Zustand aus (`False`), setze es mit `set()`, gib den Zustand erneut aus (`True`), setze es mit `clear()` zurück und gib den Zustand noch einmal aus (`False`).''',
  given='import asyncio\n\ngruen = asyncio.Event()\n', body="""print(gruen.is_set())
gruen.set()
print(gruen.is_set())
gruen.clear()
print(gruen.is_set())""")
t('''Die Coroutine `lade()` ist vorgegeben und setzt das Signal `bereit`, wenn die Daten da sind. Schreibe `zeige()`, die wartet, bis das Signal gesetzt ist, und dann den Inhalt von `daten` ausgibt (`Daten: Mensaplan`).
Starte beide mit `gather`.''',
  given="""import asyncio

daten = []
bereit = asyncio.Event()

async def lade():
    await asyncio.sleep(0.2)
    daten.append('Mensaplan')
    bereit.set()
""", body="""async def zeige():
    await bereit.wait()
    print('Daten:', daten[0])

await asyncio.gather(zeige(), lade())""")
t('''Zwei Köche (`'Ali'` und `'Bea'`) warten mit `await zutaten_da.wait()`, bis der Einkäufer die Zutaten geholt hat. Der Einkäufer braucht `0.3` Sekunden, gibt `Zutaten sind da` aus und setzt das Signal.
Jeder Koch gibt danach `<name> kocht` aus. Starte alle drei gleichzeitig (Einkäufer zuletzt in `gather`).''',
  given='import asyncio\n\nzutaten_da = asyncio.Event()\n', body="""async def koch(name):
    await zutaten_da.wait()
    print(name, 'kocht')

async def einkaeufer():
    await asyncio.sleep(0.3)
    print('Zutaten sind da')
    zutaten_da.set()

await asyncio.gather(koch('Ali'), koch('Bea'), einkaeufer())""")
t('''Das Signal `ende` ist vorgegeben. Die Coroutine `zaehle()` gibt in einer Schleife `while not ende.is_set():` immer wieder eine Zahl `1`, `2`, ... aus und wartet nach jeder Zahl `0.2` Sekunden.
Die Coroutine `stopper()` setzt nach `0.5` Sekunden das Signal. Starte beide gleichzeitig (drei Zahlen erscheinen). Gib danach `Ende` aus.''',
  given='import asyncio\n\nende = asyncio.Event()\n', body="""async def zaehle():
    n = 1
    while not ende.is_set():
        print(n)
        n += 1
        await asyncio.sleep(0.2)

async def stopper():
    await asyncio.sleep(0.5)
    ende.set()

await asyncio.gather(zaehle(), stopper())
print('Ende')""")
task('''Der Läufer wartet auf ein Signal, aber niemand setzt es: Die Zelle wird nach einem Zeitlimit mit `Zeit abgelaufen` beendet. Verbessere den Code, damit `starter()` das Signal wirklich setzt und `Ali läuft` ausgegeben wird.''',
     zelle="""import asyncio

signal = asyncio.Event()

async def laeufer():
    await signal.wait()
    print('Ali läuft')

async def starter():
    await asyncio.sleep(0.1)
    print('Los!')

try:
    await asyncio.wait_for(asyncio.gather(laeufer(), starter()), timeout=0.5)
except TimeoutError:
    print('Zeit abgelaufen')""",
     solution="""import asyncio

signal = asyncio.Event()

async def laeufer():
    await signal.wait()
    print('Ali läuft')

async def starter():
    await asyncio.sleep(0.1)
    print('Los!')
    signal.set()

try:
    await asyncio.wait_for(asyncio.gather(laeufer(), starter()), timeout=0.5)
except TimeoutError:
    print('Zeit abgelaufen')""")

# ---------------------------------------------------------------- 7
sec('Gemischte Übungen')
t('''Die Coroutine `lade(seite, dauer)` ist vorgegeben. Lade die Seiten `('Start', 0.1)`, `('Plan', 0.9)` und `('Mensa', 0.2)` gleichzeitig. Jede darf höchstens `0.5` Sekunden brauchen (`wait_for`).
Gib für jede Seite `<seite>: geladen` oder `<seite>: zu langsam` aus (`gather` mit `return_exceptions=True`).''',
  given="""import asyncio

async def lade(seite, dauer):
    await asyncio.sleep(dauer)
    return seite

daten = [('Start', 0.1), ('Plan', 0.9), ('Mensa', 0.2)]
""", body="""aufgaben = []
for seite, dauer in daten:
    aufgaben.append(asyncio.wait_for(lade(seite, dauer), timeout=0.5))
ergebnisse = await asyncio.gather(*aufgaben, return_exceptions=True)

for i in range(len(daten)):
    if isinstance(ergebnisse[i], TimeoutError):
        print(daten[i][0] + ': zu langsam')
    else:
        print(daten[i][0] + ': geladen')""")
t('''Sechs Downloads laufen mit höchstens zwei gleichzeitig (`Semaphore(2)`). Jeder dauert 1 Sekunde (`asyncio.sleep(1)`), ohne Ausgabe. Beim gesamten Ablauf gilt ein Zeitlimit von `2.2` Sekunden (`asyncio.timeout`); sechs Downloads brauchen aber drei Sekunden.
Gib `Alles geladen` aus oder, wenn die Zeit nicht reicht, `Zeit abgelaufen`. Vor dem Block merkst du dir die Zeit. Gib danach die gerundete Dauer aus (`Dauer: 2 s`).''',
  given='import asyncio\nimport time\n', body="""platz = asyncio.Semaphore(2)

async def download(nr):
    async with platz:
        await asyncio.sleep(1)

start = time.perf_counter()
try:
    async with asyncio.timeout(2.2):
        aufgaben = []
        for nr in range(6):
            aufgaben.append(download(nr))
        await asyncio.gather(*aufgaben)
    print('Alles geladen')
except TimeoutError:
    print('Zeit abgelaufen')
print('Dauer:', round(time.perf_counter() - start), 's')""")
t('''Starte als Task eine Coroutine `ticker()`, die jede `0.2` Sekunden `tick` ausgibt (Endlosschleife). Das Hauptprogramm wartet `0.5` Sekunden (dreimal `tick`), bricht den Ticker dann ab (`CancelledError` abfangen) und gibt `Ticker gestoppt` aus.''',
  given='import asyncio\n', body="""async def ticker():
    while True:
        print('tick')
        await asyncio.sleep(0.2)

aufgabe = asyncio.create_task(ticker())
await asyncio.sleep(0.5)
aufgabe.cancel()
try:
    await aufgabe
except asyncio.CancelledError:
    print('Ticker gestoppt')""")
t('''Zwei Coroutinen `schreiber(name)` fügen mit `await asyncio.sleep(0.1)` zwischen Lesen und Schreiben einen Eintrag in ein Dictionary `log` ein: `log['zeilen'] = log['zeilen'] + 1`.
Schütze das mit einem `Lock`. Starte zehn Schreiber gleichzeitig und gib `Zeilen: 10` aus.''',
  given='import asyncio\n\nlog = {\'zeilen\': 0}\nsperre = asyncio.Lock()\n', body="""async def schreiber(name):
    async with sperre:
        wert = log['zeilen']
        await asyncio.sleep(0.1)
        log['zeilen'] = wert + 1

aufgaben = []
for i in range(10):
    aufgaben.append(schreiber(i))
await asyncio.gather(*aufgaben)
print('Zeilen:', log['zeilen'])""")
t('''Drei Schüler warten mit `await pause.wait()` auf das Pausenzeichen. Nach `0.2` Sekunden setzt der Gong (`gong()`) das Signal. Jeder Schüler gibt danach `<name> geht raus` aus.
Die Schüler `['Ali', 'Bea', 'Cem']` erzeugst du in einer Schleife. Der Gong steht zuletzt in `gather`.''',
  given='import asyncio\n\npause = asyncio.Event()\n', body="""async def schueler(name):
    await pause.wait()
    print(name, 'geht raus')

async def gong():
    await asyncio.sleep(0.2)
    print('Gong!')
    pause.set()

aufgaben = []
for name in ['Ali', 'Bea', 'Cem']:
    aufgaben.append(schueler(name))
aufgaben.append(gong())
await asyncio.gather(*aufgaben)""")
t('''Die Coroutine `kocht(gericht, dauer)` ist vorgegeben (sie wartet `dauer` Sekunden und gibt `gericht` zurück). Zwei Köche (`Semaphore(2)`) bereiten vier Gerichte in einer `TaskGroup` zu: `('Suppe', 0.1)`, `('Pizza', 0.3)`, `('Salat', 0.1)`, `('Nudeln', 0.2)`.
Gib nach dem Block die Gerichte in der Reihenfolge der Liste aus (ein Gericht pro Zeile).''',
  given="""import asyncio

async def kocht(gericht, dauer):
    await asyncio.sleep(dauer)
    return gericht

menue = [('Suppe', 0.1), ('Pizza', 0.3), ('Salat', 0.1), ('Nudeln', 0.2)]
""", body="""koeche = asyncio.Semaphore(2)

async def begrenzt(gericht, dauer):
    async with koeche:
        return await kocht(gericht, dauer)

tasks = []
async with asyncio.TaskGroup() as gruppe:
    for gericht, dauer in menue:
        tasks.append(gruppe.create_task(begrenzt(gericht, dauer)))

for aufgabe in tasks:
    print(aufgabe.result())""")
predict("""import asyncio

async def f(name, dauer):
    try:
        await asyncio.sleep(dauer)
        print(name, 'fertig')
    except asyncio.CancelledError:
        print(name, 'abgebrochen')
        raise

t1 = asyncio.create_task(f('a', 0.1))
t2 = asyncio.create_task(f('b', 1))
await asyncio.sleep(0.3)
t2.cancel()
try:
    await t2
except asyncio.CancelledError:
    print('t2 weg')
await t1
print(t1.cancelled(), t2.cancelled())""", erklaerung='''`a` ist nach 0,1 Sekunden fertig. Nach 0,3 Sekunden wird `b` abgebrochen: Zuerst meldet die Coroutine selbst den Abbruch (`b abgebrochen`), dann kommt der `CancelledError` beim `await t2` an (`t2 weg`).
`await t1` kehrt sofort zurück, weil `t1` schon fertig ist.

```
a fertig
b abgebrochen
t2 weg
False True
```''')
predict("""import asyncio

sperre = asyncio.Lock()
liste = []

async def f(x):
    async with sperre:
        liste.append(x)
        await asyncio.sleep(0.1)
        liste.append(x * 10)

await asyncio.gather(f(1), f(2))
print(liste)""", erklaerung='''Wegen des `Lock` läuft zuerst `f(1)` komplett durch (`1`, `10`), danach `f(2)` (`2`, `20`).

```
[1, 10, 2, 20]
```''')

generate('asyncio_steuerung', 'asyncio 3: Steuerung', intro=INTRO, ausfuehren=AUSFUEHREN)
