# Erzeugt ../content/asyncio_grundlagen.ipynb (siehe nbgen.py). Erstes Notebook der asyncio-Reihe (asynchilfe.py).
# Die Zellen laufen wie in Jupyter: `await` steht direkt in der Zelle (asyncnb.py), asyncio.run() gibt einen RuntimeError.
# Zeiten: nur ganze Sekunden mit round(), nie genauere Werte. Reihenfolgen von Ausgaben nur, wenn die Wartezeiten sich deutlich
# unterscheiden (mindestens 0.1 s) oder mit asyncio.sleep(0) gesteuert werden.
from nbgen import sec, expl, task, predict, generate
from asynchilfe import t, reihe, AUSFUEHREN

INTRO = f'''In diesem Notebook lernst du die Grundlagen von **asyncio** kennen. Damit schreibt man Programme, die **gleichzeitig warten** können,
zum Beispiel auf Webseiten, Datenbanken oder Dateien. Du lernst, was eine *Coroutine* ist, wie `async def` und `await` zusammenspielen,
wie man ein asynchrones Programm startet und wann Python zwischen mehreren Aufgaben wechselt.

Die Reihe besteht aus vier Notebooks:

{reihe('asyncio_grundlagen')}

Du solltest Schleifen, Listen, Dictionaries und Funktionen schon kennen.

**Wichtig in Jupyter:** In einer Notebook-Zelle darfst du `await` direkt hinschreiben, ohne `asyncio.run()`. Warum das so ist, erfährst du in Abschnitt 3.

Gemessene Zeiten sind nie ganz genau. Deshalb runden wir sie mit `round()` auf ganze Sekunden.

Jeder Abschnitt beginnt mit kurzen Erklärungen und Beispielen. Führe die Beispiele aus und probiere sie ruhig ein wenig aus.
Danach folgen viele kleine Übungen. Wenn etwas vorgegeben ist, steht es schon in der Codezelle.'''

# ---------------------------------------------------------------- 1
sec('Warten kostet Zeit')
expl('''#### Programme warten oft

Viele Programme verbringen die meiste Zeit **mit Warten**: auf eine Webseite, auf die Antwort einer Datenbank, auf eine Datei, auf den Drucker.
Während dieser Zeit tut der Computer nichts Nützliches.

Mit `time.sleep(sekunden)` aus dem Modul `time` kann man das Warten nachspielen: Das Programm hält die angegebene Zeit an.''',
     """import time

print('Toast wird gemacht ...')
time.sleep(1)
print('Toast ist fertig')""")
expl('''#### Zeit messen

`time.perf_counter()` ist eine Stoppuhr: Sie liefert die aktuelle Zeit in Sekunden. Nimmt man die Zeit vor und nach einem Programmstück und bildet die
Differenz, erhält man die Dauer.

Die Messung ist nie ganz genau (etwa `2.0013` Sekunden). Deshalb runden wir mit `round()` auf ganze Sekunden.''',
     """import time

start = time.perf_counter()
time.sleep(1)
time.sleep(1)
dauer = time.perf_counter() - start
print('Dauer:', round(dauer), 's')""")
expl('''#### Nacheinander warten

Drei Webseiten werden **nacheinander** geladen. Jede braucht eine Sekunde. Das Programm wartet also dreimal hintereinander.''',
     """import time

def lade_seite(name):
    print('Lade', name)
    time.sleep(1)
    print('Fertig:', name)

start = time.perf_counter()
lade_seite('Startseite')
lade_seite('Stundenplan')
lade_seite('Mensa')
print('Dauer:', round(time.perf_counter() - start), 's')""")
expl('''#### Die Idee von asyncio

Das geht besser: Während die Startseite lädt, kann man schon den Stundenplan und die Mensa-Seite anfordern. Alle drei warten dann **gleichzeitig**,
und die Gesamtdauer ist nur so lang wie die längste Wartezeit (hier eine Sekunde statt drei).

Das Modul `asyncio` macht genau das möglich. Wichtig dabei:

- asyncio hilft beim **Warten** (auf Netzwerk, Dateien, Datenbanken, Zeit), nicht beim **Rechnen**. Eine lange Rechnung wird dadurch nicht schneller.
- Es läuft nur **ein Stück Code auf einmal**. Während eine Aufgabe wartet, darf eine andere weitermachen. Es ist also nicht „parallel“, sondern **nebenläufig**:
  Die Wartezeiten überlappen sich.
- Die Aufgaben geben selbst ab, wenn sie warten müssen (mit `await`). Man nennt das **kooperatives Multitasking**.''', None)

t('''Gib `Pizza im Ofen` aus, warte **eine Sekunde** und gib dann `Pizza ist fertig` aus.''',
  given='import time\n', body="""print('Pizza im Ofen')
time.sleep(1)
print('Pizza ist fertig')""")
t('''Warte mit einer Schleife **dreimal** eine Sekunde (`time.sleep(1)`) und gib danach die Gesamtdauer aus, so wie im Beispiel oben (`Dauer: 3 s`).''',
  given='import time\n', body="""start = time.perf_counter()
for i in range(3):
    time.sleep(1)
print('Dauer:', round(time.perf_counter() - start), 's')""")
t('''Schreibe eine Funktion `drucke(dokument)`. Sie gibt `Drucke <dokument>` aus, wartet eine Sekunde und gibt dann `Fertig: <dokument>` aus.
Drucke nacheinander `'Referat'` und `'Plakat'` und gib danach die Dauer aus.''',
  given='import time\n', body="""def drucke(dokument):
    print('Drucke', dokument)
    time.sleep(1)
    print('Fertig:', dokument)

start = time.perf_counter()
drucke('Referat')
drucke('Plakat')
print('Dauer:', round(time.perf_counter() - start), 's')""")
t('''Die Funktion `hole_note()` spielt eine langsame Datenbankabfrage nach. Hole die Noten für `'Mathe'` und `'Physik'`, gib ihre **Summe** aus
(`Summe: 3`) und danach die Dauer.''',
  given="""import time

noten = {'Mathe': 2, 'Deutsch': 3, 'Physik': 1}

def hole_note(fach):
    time.sleep(1)
    return noten[fach]
""", body="""start = time.perf_counter()
a = hole_note('Mathe')
b = hole_note('Physik')
print('Summe:', a + b)
print('Dauer:', round(time.perf_counter() - start), 's')""")
t('''Die Funktion `lade(seite)` wartet eine halbe Sekunde und gibt dann `<seite> geladen` aus.
Lade alle Seiten der Liste mit einer Schleife nacheinander und gib danach die Dauer aus.''',
  given="""import time

def lade(seite):
    time.sleep(0.5)
    print(seite, 'geladen')

seiten = ['Start', 'Mensa', 'Plan', 'Hilfe']
""", body="""start = time.perf_counter()
for seite in seiten:
    lade(seite)
print('Dauer:', round(time.perf_counter() - start), 's')""")
predict("""import time

start = time.perf_counter()
time.sleep(2)
print('A')
time.sleep(1)
print('B')
print(round(time.perf_counter() - start))""", erklaerung='''Die Aufgaben laufen **nacheinander**: Erst werden 2 Sekunden gewartet, dann wird `A` ausgegeben, dann wird 1 Sekunde gewartet und `B` ausgegeben.
Die Gesamtdauer ist 2 + 1 = 3 Sekunden.

```
A
B
3
```''')
predict("""import time

start = time.perf_counter()
for sekunden in [1, 2]:
    time.sleep(sekunden)
    print('gewartet:', sekunden)
print(round(time.perf_counter() - start))""", erklaerung='''Die Schleife wartet erst 1 Sekunde, gibt `gewartet: 1` aus, wartet dann 2 Sekunden und gibt `gewartet: 2` aus.
Am Ende stehen 1 + 2 = 3 Sekunden auf der Stoppuhr.

```
gewartet: 1
gewartet: 2
3
```''')

# ---------------------------------------------------------------- 2
sec('Coroutinen: async def und await')
expl('''#### Eine Funktion mit `async def`

Mit `async def` statt `def` definiert man eine **Coroutinen-Funktion**. Ruft man sie auf, wird der Code darin **noch nicht ausgeführt**.
Stattdessen erhält man ein **Coroutinen-Objekt**, eine Art „Auftrag, der noch erledigt werden muss“.

Erst `await` führt die Coroutine aus und wartet, bis sie fertig ist.''',
     """async def gruss():
    print('Hallo!')

k = gruss()
print(type(k))
print('Jetzt kommt await')
await k""")
expl('''#### Direkt aufrufen mit `await`

Meistens schreibt man gleich `await gruss()`. Das ist die Kurzform für „Coroutine erzeugen und ausführen“.
In einer Notebook-Zelle darf `await` direkt stehen (in einer normalen Python-Datei geht das nicht, siehe Abschnitt 3).''',
     """async def gruss(name):
    print('Hallo', name)

await gruss('Ali')
await gruss('Bea')""")
expl('''#### Warten mit `asyncio.sleep()`

`asyncio.sleep(sekunden)` ist das Gegenstück zu `time.sleep()`. Es ist selbst eine Coroutine, deshalb muss man es mit `await` aufrufen.
Man importiert dazu das Modul `asyncio`.

Der Unterschied: `time.sleep()` hält das ganze Programm an. `asyncio.sleep()` sagt „ich warte jetzt, andere dürfen inzwischen weitermachen“.
Das sieht man ab Abschnitt 4.

`await` darf nur **innerhalb** einer `async def`-Funktion stehen (oder, wie hier, direkt in einer Notebook-Zelle).''',
     """import asyncio

async def toast():
    print('Toast wird gemacht ...')
    await asyncio.sleep(1)
    print('Toast ist fertig')

await toast()""")
expl('''#### Argumente und Rückgabewerte

Coroutinen haben Parameter und können wie normale Funktionen mit `return` einen Wert zurückgeben. Den Wert erhält man als Ergebnis von `await`.''',
     """import asyncio

noten = {'Mathe': 2, 'Deutsch': 3}

async def hole_note(fach):
    await asyncio.sleep(0.5)
    return noten[fach]

note = await hole_note('Mathe')
print('Mathe:', note)
print('Deutsch:', await hole_note('Deutsch'))""")
expl('''#### Coroutinen rufen Coroutinen auf

Innerhalb einer `async def`-Funktion kann man andere Coroutinen mit `await` aufrufen. So baut man größere Abläufe zusammen.

Achtung: Wer `await` nacheinander schreibt, wartet auch **nacheinander**. Die Gesamtdauer ist hier die Summe (2 Sekunden).
Das gleichzeitige Warten kommt in Abschnitt 4.''',
     """import asyncio
import time

async def lade(seite):
    print('Lade', seite)
    await asyncio.sleep(1)
    print('Fertig:', seite)
    return len(seite)

async def lade_beide():
    a = await lade('Start')
    b = await lade('Plan')
    return a + b

start = time.perf_counter()
summe = await lade_beide()
print('Summe:', summe)
print('Dauer:', round(time.perf_counter() - start), 's')""")
expl('''#### Fehler: `await` in einer normalen Funktion

In einer Funktion mit `def` (ohne `async`) darf kein `await` stehen. Das ist ein Syntaxfehler. Python führt dann gar nichts aus.''',
     """import asyncio

def toast():
    await asyncio.sleep(1)
    print('Toast ist fertig')""", error=SyntaxError)

predict("""async def gruss():
    print('Hallo')

print('A')
await gruss()
print('B')""", erklaerung='''`await gruss()` führt die Coroutine sofort aus und wartet, bis sie fertig ist. Die Ausgaben stehen also in der Reihenfolge des Codes.

```
A
Hallo
B
```''')
predict("""async def gruss():
    print('Hallo')

print('A')
g = gruss()
print('B')
await g
print('C')""", erklaerung='''`g = gruss()` erzeugt nur das Coroutinen-Objekt. Es wird noch nichts ausgegeben.
Erst `await g` führt den Code der Coroutine aus. Deshalb steht `Hallo` zwischen `B` und `C`.

```
A
B
Hallo
C
```''')
predict("""async def verdopple(x):
    return x * 2

k = verdopple(5)
print(type(k))
print(await k)""", erklaerung='''Ohne `await` ist `k` nur ein Coroutinen-Objekt vom Typ `coroutine`. Erst `await k` führt `verdopple(5)` aus und liefert das Ergebnis `10`.

```
<class 'coroutine'>
10
```''')
predict("""import asyncio

async def a():
    print('a1')
    await asyncio.sleep(0.1)
    print('a2')

async def b():
    print('b1')
    await a()
    print('b2')

print('start')
await b()
print('ende')""", erklaerung='''Die Ausgaben folgen dem Aufruf: `b` beginnt mit `b1`, ruft dann `a` auf (`a1`, Pause, `a2`) und macht erst danach mit `b2` weiter.

```
start
b1
a1
a2
b2
ende
```''')
predict("""import asyncio

async def f(x):
    await asyncio.sleep(0.1)
    return x * 2

async def g():
    a = await f(2)
    b = await f(a)
    return a + b

print(await g())""", erklaerung='''`a = await f(2)` ergibt `4`. Dann ist `b = await f(4)` gleich `8`. `g()` gibt `4 + 8 = 12` zurück.

```
12
```''')

t('''Schreibe eine Coroutinen-Funktion `hallo()`, die `Hallo Welt` ausgibt. Rufe sie mit `await` auf.''',
  body="""async def hallo():
    print('Hallo Welt')

await hallo()""")
t('''Schreibe eine Coroutine `gruss(name)`, die `Hallo <name>!` ausgibt. Rufe sie nacheinander für `'Ali'` und `'Bea'` auf.''',
  body="""async def gruss(name):
    print(f'Hallo {name}!')

await gruss('Ali')
await gruss('Bea')""")
t('''Schreibe eine Coroutine `quadrat(zahl)`, die das Quadrat der Zahl **zurückgibt**. Gib das Ergebnis für `7` aus.''',
  body="""async def quadrat(zahl):
    return zahl * zahl

print(await quadrat(7))""")
t('''Schreibe eine Coroutine `zaehle(n)`. Sie gibt die Zahlen von `1` bis `n` aus und wartet nach jeder Zahl 0,1 Sekunden mit `await asyncio.sleep(0.1)`.
Rufe sie mit `n = 3` auf.''',
  given='import asyncio\n', body="""async def zaehle(n):
    for i in range(1, n + 1):
        print(i)
        await asyncio.sleep(0.1)

await zaehle(3)""")
t('''Schreibe eine Coroutine `kaffee()`. Sie gibt `Kaffee wird gekocht` aus, wartet eine Sekunde und gibt dann `Kaffee ist fertig` aus.
Rufe sie auf und gib danach die Dauer aus.''',
  given='import asyncio\nimport time\n', body="""async def kaffee():
    print('Kaffee wird gekocht')
    await asyncio.sleep(1)
    print('Kaffee ist fertig')

start = time.perf_counter()
await kaffee()
print('Dauer:', round(time.perf_counter() - start), 's')""")
t('''Schreibe eine Coroutine `warte_und_sag(text, dauer)`. Sie wartet `dauer` Sekunden und gibt dann `text` aus.
Rufe sie nacheinander mit `('A', 0.2)` und `('B', 0.1)` auf.''',
  given='import asyncio\n', body="""async def warte_und_sag(text, dauer):
    await asyncio.sleep(dauer)
    print(text)

await warte_und_sag('A', 0.2)
await warte_und_sag('B', 0.1)""")
t('''Schreibe eine Coroutine `verdopple(x)`, die nach 0,1 Sekunden `x * 2` zurückgibt.
Verdopple damit alle Zahlen der Liste (nacheinander, in einer Schleife) und gib die Liste der Ergebnisse aus.''',
  given='import asyncio\n\nzahlen = [3, 5, 8]\n', body="""async def verdopple(x):
    await asyncio.sleep(0.1)
    return x * 2

ergebnisse = []
for z in zahlen:
    ergebnisse.append(await verdopple(z))
print(ergebnisse)""")
t('''Die Coroutine `hole_note(fach)` ist vorgegeben. Schreibe eine Coroutine `hole_alle(faecher)`, die für jedes Fach der Liste die Note holt
und alle Noten als **Liste** zurückgibt. Gib das Ergebnis für `['Mathe', 'Physik', 'Deutsch']` aus.''',
  given="""import asyncio

noten = {'Mathe': 2, 'Deutsch': 3, 'Physik': 1}

async def hole_note(fach):
    await asyncio.sleep(0.2)
    return noten[fach]
""", body="""async def hole_alle(faecher):
    ergebnis = []
    for fach in faecher:
        ergebnis.append(await hole_note(fach))
    return ergebnis

print(await hole_alle(['Mathe', 'Physik', 'Deutsch']))""")
t('''Die Coroutine `addiere(a, b)` ist vorgegeben. Schreibe eine Coroutine `summe3(a, b, c)`, die `addiere` zweimal benutzt, um `a + b + c` zu berechnen.
Gib `summe3(1, 2, 3)` aus.''',
  given="""import asyncio

async def addiere(a, b):
    await asyncio.sleep(0.1)
    return a + b
""", body="""async def summe3(a, b, c):
    zwischen = await addiere(a, b)
    return await addiere(zwischen, c)

print(await summe3(1, 2, 3))""")
t('''Schreibe eine Coroutine `lade_nutzer(nr)`, die nach 0,1 Sekunden ein Dictionary `{'nr': nr, 'name': <name>}` zurückgibt. Den Namen findest du im Dictionary `namen`.
Gib die Nutzer mit den Nummern `1` und `2` aus (jeweils eine Zeile).''',
  given="""import asyncio

namen = {1: 'Ali', 2: 'Bea', 3: 'Cem'}
""", body="""async def lade_nutzer(nr):
    await asyncio.sleep(0.1)
    return {'nr': nr, 'name': namen[nr]}

print(await lade_nutzer(1))
print(await lade_nutzer(2))""")
task('''Die Zelle soll **eine Sekunde** lang warten, aber die Dauer ist `0`: Die Pause findet gar nicht statt. Verbessere den Code.''',
     zelle="""import asyncio
import time

async def pause():
    print('Pause beginnt')
    asyncio.sleep(1)
    print('Pause vorbei')

start = time.perf_counter()
await pause()
print('Dauer:', round(time.perf_counter() - start), 's')""",
     solution="""import asyncio
import time

async def pause():
    print('Pause beginnt')
    await asyncio.sleep(1)
    print('Pause vorbei')

start = time.perf_counter()
await pause()
print('Dauer:', round(time.perf_counter() - start), 's')""")

# ---------------------------------------------------------------- 3
sec('Programme starten: asyncio.run() und await im Notebook')
expl('''#### In einer Python-Datei: `asyncio.run()`

In einer normalen Python-Datei (`.py`) darf `await` **nicht** einfach so in einer Zeile stehen, denn dort läuft noch nichts, was warten könnte.
Man schreibt deshalb das ganze Programm in eine Coroutine, meist `main()` genannt, und startet sie mit `asyncio.run()`:

```python
import asyncio

async def main():
    print('Hallo')
    await asyncio.sleep(1)
    print('Tschüss')

asyncio.run(main())
```

`asyncio.run(coroutine)` startet die **Event-Loop**, das ist die Schleife, die alle Coroutinen ausführt. Sie läuft, bis die Coroutine fertig ist, und gibt deren Rückgabewert zurück.
Man ruft `asyncio.run()` nur **einmal** auf, ganz unten im Programm.

Das kannst du in einer Python-Datei ausprobieren (zum Beispiel in Thonny oder VS Code), aber nicht in diesem Notebook (siehe unten).''', None)
expl('''#### Im Notebook: direkt `await`

Ein Jupyter-Notebook hat die Event-Loop schon gestartet. Deshalb darf man hier `await` direkt in eine Zelle schreiben.
Dasselbe Programm sieht im Notebook so aus:''',
     """import asyncio

async def main():
    print('Hallo')
    await asyncio.sleep(1)
    print('Tschüss')

await main()""")
expl('''#### Fehler: `asyncio.run()` im Notebook

Weil die Loop im Notebook schon läuft, kann `asyncio.run()` keine zweite starten. Das gibt einen `RuntimeError`:
`asyncio.run() cannot be called from a running event loop`.

**Merke:** In einer `.py`-Datei `asyncio.run(main())`, in einem Notebook `await main()`.''',
     """import asyncio

async def main():
    print('Hallo')

asyncio.run(main())""", error=RuntimeError)
expl('''#### `main()` als Einstieg

Das Programm besteht aus einer Coroutine `main()`, die die anderen Coroutinen aufruft. Auch im Notebook ist diese Struktur sinnvoll:
Der Code lässt sich später fast unverändert in eine `.py`-Datei übernehmen. Man ersetzt nur `await main()` durch `asyncio.run(main())`.''',
     """import asyncio

async def lade(seite):
    await asyncio.sleep(0.2)
    print('Geladen:', seite)

async def main():
    for seite in ['Start', 'Plan', 'Mensa']:
        await lade(seite)
    print('Alles geladen')

await main()""")

predict("""import asyncio

async def main():
    print('Hallo')

print('Start')
asyncio.run(main())
print('Ende')""", error=RuntimeError, erklaerung='''`Start` wird noch ausgegeben. Dann bricht `asyncio.run(main())` mit einem `RuntimeError` ab, weil im Notebook die Event-Loop schon läuft.
`Hallo` und `Ende` erscheinen nicht. Im Notebook schreibt man stattdessen `await main()`.''')
predict("""import asyncio

async def main():
    print('1')
    await asyncio.sleep(0.1)
    print('2')
    return 'fertig'

ergebnis = await main()
print('3')
print(ergebnis)""", erklaerung='''`await main()` führt `main` ganz aus (`1`, Pause, `2`) und liefert den Rückgabewert `'fertig'`. Erst danach geht es mit `3` weiter.

```
1
2
3
fertig
```''')
t('''Schreibe eine Coroutine `main()`. Sie gibt `Start` aus, wartet 0,5 Sekunden und gibt `Ende` aus. Starte sie so, wie man es **im Notebook** macht.''',
  given='import asyncio\n', body="""async def main():
    print('Start')
    await asyncio.sleep(0.5)
    print('Ende')

await main()""")
task('''Dieser Code stammt aus einer Python-Datei und gibt im Notebook einen `RuntimeError`:
```python
import asyncio

async def main():
    print('Hallo aus main')

asyncio.run(main())
```
Schreibe ihn so, dass er im Notebook läuft.''',
     solution="""import asyncio

async def main():
    print('Hallo aus main')

await main()""")
t('''Die Coroutine `gruss(name)` ist vorgegeben. Schreibe `main()`: Sie begrüßt alle Namen der Liste nacheinander. Starte `main()` im Notebook.''',
  given="""import asyncio

async def gruss(name):
    await asyncio.sleep(0.1)
    print('Hallo', name)

namen = ['Ali', 'Bea', 'Cem']
""", body="""async def main():
    for name in namen:
        await gruss(name)

await main()""")
t('''Schreibe `main()` als Countdown: Sie gibt `3`, `2`, `1` aus (jeweils nach einer Pause von 0,2 Sekunden mit `asyncio.sleep`) und danach `Start!`. Starte `main()`.''',
  given='import asyncio\n', body="""async def main():
    for zahl in [3, 2, 1]:
        print(zahl)
        await asyncio.sleep(0.2)
    print('Start!')

await main()""")
t('''Schreibe `main()`, die mit `await` die Summe `zahlen[0] + zahlen[1] + zahlen[2]` berechnet, indem sie dreimal `hole(i)` aufruft,
und die Summe **zurückgibt**. Speichere das Ergebnis von `await main()` in `ergebnis` und gib es aus.''',
  given="""import asyncio

zahlen = [10, 20, 30]

async def hole(i):
    await asyncio.sleep(0.1)
    return zahlen[i]
""", body="""async def main():
    summe = 0
    for i in range(3):
        summe += await hole(i)
    return summe

ergebnis = await main()
print(ergebnis)""")
t('''Schreibe `lade_fach(fach)`: Die Coroutine wartet 0,2 Sekunden und gibt den Text `<fach>: geladen` **zurück**.
`main()` ruft sie für alle Fächer der Liste auf, gibt jeden zurückgegebenen Text aus und danach `Stundenplan komplett`. Starte `main()`.''',
  given='import asyncio\n\nfaecher = [\'Mathe\', \'Physik\', \'Kunst\']\n', body="""async def lade_fach(fach):
    await asyncio.sleep(0.2)
    return fach + ': geladen'

async def main():
    for fach in faecher:
        print(await lade_fach(fach))
    print('Stundenplan komplett')

await main()""")

# ---------------------------------------------------------------- 4
sec('Gleichzeitig warten mit gather()')
expl('''#### `asyncio.gather()`

Mit `await asyncio.gather(c1, c2, c3)` werden mehrere Coroutinen **gleichzeitig** gestartet. `gather` wartet, bis **alle** fertig sind.
Die Gesamtdauer ist deshalb nur so lang wie die längste einzelne Wartezeit.

Im Beispiel dauert `Start` zwei Sekunden und `Plan` eine Sekunde. Man sieht: Beide beginnen sofort, `Plan` ist zuerst fertig, und alles zusammen dauert
nur 2 Sekunden (statt 3 bei `await` nacheinander).

In diesem Notebook lernst du nur den Einstieg. Im nächsten Notebook (`asyncio_tasks`) folgt mehr dazu.''',
     """import asyncio
import time

async def lade(seite, dauer):
    print('Lade', seite)
    await asyncio.sleep(dauer)
    print('Fertig:', seite)

start = time.perf_counter()
await asyncio.gather(lade('Start', 2), lade('Plan', 1))
print('Dauer:', round(time.perf_counter() - start), 's')""")
expl('''#### Die Ergebnisse von `gather()`

`gather` gibt eine **Liste** mit den Rückgabewerten zurück, und zwar in der Reihenfolge der **Argumente**, nicht in der Reihenfolge, in der die Coroutinen fertig werden.''',
     """import asyncio

async def verdopple(zahl, dauer):
    await asyncio.sleep(dauer)
    print('fertig:', zahl)
    return zahl * 2

ergebnisse = await asyncio.gather(verdopple(1, 0.3), verdopple(2, 0.1), verdopple(3, 0.2))
print(ergebnisse)""")
expl('''#### Viele Coroutinen aus einer Liste

Hat man viele Coroutinen, erzeugt man sie in einer Schleife und sammelt sie in einer Liste. Es wird dabei noch nichts ausgeführt.
Mit `gather(*liste)` übergibt man dann alle auf einmal. Der Stern `*` entpackt die Liste in einzelne Argumente
(`gather(*[a, b])` ist dasselbe wie `gather(a, b)`).''',
     """import asyncio
import time

async def lade(seite):
    await asyncio.sleep(1)
    return len(seite)

seiten = ['Start', 'Plan', 'Mensa', 'Hilfe']
aufgaben = []
for seite in seiten:
    aufgaben.append(lade(seite))

start = time.perf_counter()
ergebnisse = await asyncio.gather(*aufgaben)
print(ergebnisse)
print('Dauer:', round(time.perf_counter() - start), 's')""")

predict("""import asyncio

async def sag(text, dauer):
    await asyncio.sleep(dauer)
    print(text)

await asyncio.gather(sag('eins', 0.2), sag('zwei', 0.1))
print('drei')""", erklaerung='''Beide Coroutinen starten gleichzeitig. `zwei` wartet nur 0,1 Sekunden und wird deshalb vor `eins` (0,2 Sekunden) ausgegeben.
`gather` wartet, bis beide fertig sind. Erst dann folgt `drei`.

```
zwei
eins
drei
```''')
predict("""import asyncio

async def f(x, dauer):
    await asyncio.sleep(dauer)
    return x

ergebnisse = await asyncio.gather(f('a', 0.2), f('b', 0.1))
print(ergebnisse)""", erklaerung='''`b` ist zuerst fertig, aber die Liste folgt der Reihenfolge der Argumente: zuerst das Ergebnis von `f('a', ...)`, dann das von `f('b', ...)`.

```
['a', 'b']
```''')
predict("""import asyncio
import time

async def sag(text, dauer):
    await asyncio.sleep(dauer)
    print(text)

start = time.perf_counter()
await sag('A', 1)
await asyncio.gather(sag('B', 1), sag('C', 1))
print(round(time.perf_counter() - start))""", erklaerung='''`A` wird zuerst allein ausgeführt (1 Sekunde). Danach warten `B` und `C` gleichzeitig (zusammen nur 1 Sekunde). Gesamtdauer: 1 + 1 = 2 Sekunden.
`B` und `C` sind gleichzeitig fertig, `B` wurde zuerst gestartet und kommt deshalb zuerst.

```
A
B
C
2
```''')
t('''Die Coroutinen `toast()` und `ei()` sind vorgegeben (jede wartet eine Sekunde). Starte beide mit `gather` gleichzeitig und gib danach die Dauer aus.''',
  given="""import asyncio
import time

async def toast():
    print('Toast wird gemacht')
    await asyncio.sleep(1)
    print('Toast fertig')

async def ei():
    print('Ei wird gekocht')
    await asyncio.sleep(1)
    print('Ei fertig')
""", body="""start = time.perf_counter()
await asyncio.gather(toast(), ei())
print('Dauer:', round(time.perf_counter() - start), 's')""")
t('''Die Coroutine `drucke(dokument)` ist vorgegeben. Drucke `'Referat'`, `'Plakat'` und `'Brief'` **gleichzeitig** und gib danach die Dauer aus.''',
  given="""import asyncio
import time

async def drucke(dokument):
    print('Drucke', dokument)
    await asyncio.sleep(1)
    print('Fertig:', dokument)
""", body="""start = time.perf_counter()
await asyncio.gather(drucke('Referat'), drucke('Plakat'), drucke('Brief'))
print('Dauer:', round(time.perf_counter() - start), 's')""")
t('''Die Coroutine `quadrat(z)` ist vorgegeben. Berechne die Quadrate von `1`, `2`, `3` und `4` mit **einem** `gather`-Aufruf und gib die Ergebnisliste aus.''',
  given="""import asyncio

async def quadrat(z):
    await asyncio.sleep(0.1)
    return z * z
""", body="""ergebnisse = await asyncio.gather(quadrat(1), quadrat(2), quadrat(3), quadrat(4))
print(ergebnisse)""")
t('''Die Coroutine `laenge(wort)` ist vorgegeben. Erzeuge in einer Schleife eine Liste `aufgaben` mit einer Coroutine für jedes Wort der Liste `woerter`.
Führe alle mit `gather(*aufgaben)` aus und gib die Ergebnisliste aus.''',
  given="""import asyncio

async def laenge(wort):
    await asyncio.sleep(0.1)
    return len(wort)

woerter = ['Schule', 'Pause', 'Mathe', 'Informatik']
""", body="""aufgaben = []
for wort in woerter:
    aufgaben.append(laenge(wort))

ergebnisse = await asyncio.gather(*aufgaben)
print(ergebnisse)""")
t('''Die Coroutine `lade(seite)` ist vorgegeben (eine Sekunde Wartezeit). Lade `'A'`, `'B'` und `'C'` zuerst **nacheinander** und gib `nacheinander: <Dauer>` aus.
Lade sie dann **gleichzeitig** mit `gather` und gib `gleichzeitig: <Dauer>` aus.''',
  given="""import asyncio
import time

async def lade(seite):
    await asyncio.sleep(1)
    return seite
""", body="""start = time.perf_counter()
await lade('A')
await lade('B')
await lade('C')
print('nacheinander:', round(time.perf_counter() - start))

start = time.perf_counter()
await asyncio.gather(lade('A'), lade('B'), lade('C'))
print('gleichzeitig:', round(time.perf_counter() - start))""")
task('''Die drei Seiten werden nacheinander geladen und das dauert drei Sekunden. Verbessere den Code mit `gather`, sodass alles gleichzeitig läuft (Dauer: `1`).''',
     zelle="""import asyncio
import time

async def lade(seite):
    await asyncio.sleep(1)
    print('Geladen:', seite)

start = time.perf_counter()
await lade('Start')
await lade('Plan')
await lade('Mensa')
print('Dauer:', round(time.perf_counter() - start), 's')""",
     solution="""import asyncio
import time

async def lade(seite):
    await asyncio.sleep(1)
    print('Geladen:', seite)

start = time.perf_counter()
await asyncio.gather(lade('Start'), lade('Plan'), lade('Mensa'))
print('Dauer:', round(time.perf_counter() - start), 's')""")
t('''Die Coroutine `sag(text, dauer)` ist vorgegeben. Starte gleichzeitig `('C', 0.3)`, `('A', 0.1)` und `('B', 0.2)`. Ausgegeben wird nach Wartezeit sortiert: `A`, `B`, `C`.''',
  given="""import asyncio

async def sag(text, dauer):
    await asyncio.sleep(dauer)
    print(text)
""", body="""await asyncio.gather(sag('C', 0.3), sag('A', 0.1), sag('B', 0.2))""")
t('''Die Coroutine `hole_punkte(name)` ist vorgegeben. Hole die Punkte von `'Ali'`, `'Bea'` und `'Cem'` mit `gather` und gib die **Summe** der Punkte aus (`sum()`).''',
  given="""import asyncio

punkte = {'Ali': 12, 'Bea': 17, 'Cem': 9}

async def hole_punkte(name):
    await asyncio.sleep(0.1)
    return punkte[name]
""", body="""ergebnisse = await asyncio.gather(hole_punkte('Ali'), hole_punkte('Bea'), hole_punkte('Cem'))
print(sum(ergebnisse))""")
t('''Hole mit `gather` die Punkte aller Namen der Liste `namen` (Schleife und `gather(*aufgaben)`). Gib dann für jeden Namen eine Zeile `<name>: <punkte>` aus.
Die Ergebnisliste hat dieselbe Reihenfolge wie `namen`.''',
  given="""import asyncio

punkte = {'Ali': 12, 'Bea': 17, 'Cem': 9, 'Dana': 14}

async def hole_punkte(name):
    await asyncio.sleep(0.1)
    return punkte[name]

namen = ['Dana', 'Ali', 'Cem']
""", body="""aufgaben = []
for name in namen:
    aufgaben.append(hole_punkte(name))
ergebnisse = await asyncio.gather(*aufgaben)

for i in range(len(namen)):
    print(f'{namen[i]}: {ergebnisse[i]}')""")

# ---------------------------------------------------------------- 5
sec('Wann wechselt asyncio?')
expl('''#### Die Event-Loop

Alle Coroutinen werden von **einer** Event-Loop ausgeführt, immer nur eine zur selben Zeit. Die Loop wechselt nur an einer Stelle zur nächsten Coroutine:
wenn die aktuelle bei einem `await` **warten muss**. Dann sagt die Coroutine gewissermaßen: „Ich warte noch, macht inzwischen woanders weiter.“

Ein Vergleich: Eine Lehrerin betreut mehrere Schüler. Sagt einer „Ich überlege noch“, geht sie zum nächsten. Sie wird nicht schneller, aber sie steht nie wartend herum.

Folgen:

- Ohne `await` gibt eine Coroutine die Kontrolle nie ab. Alle anderen müssen warten, bis sie fertig ist.
- Zwischen zwei `await` läuft eine Coroutine ohne Unterbrechung durch.''', None)
expl('''#### Wechsel sichtbar machen mit `asyncio.sleep(0)`

`await asyncio.sleep(0)` wartet keine Zeit, gibt aber die Kontrolle ab: Die Loop kann eine andere Coroutine weiterlaufen lassen.
Damit sieht man, wie die Coroutinen sich abwechseln.''',
     """import asyncio

async def zaehle(name):
    for i in range(1, 4):
        print(name, i)
        await asyncio.sleep(0)

await asyncio.gather(zaehle('A'), zaehle('B'))""")
expl('''#### Ohne `await` kein Wechsel

Fehlt das `await` in der Schleife, läuft erst `A` komplett durch und danach `B`.''',
     """import asyncio

async def zaehle(name):
    for i in range(1, 4):
        print(name, i)

await asyncio.gather(zaehle('A'), zaehle('B'))""")
expl('''#### Blockieren mit `time.sleep()`

`time.sleep()` ist **kein** `await`: Es hält das ganze Programm an, auch alle anderen Coroutinen. Das gleichzeitige Warten geht dadurch verloren.
Im Beispiel dauert es zwei Sekunden, und die Ausgaben stehen nacheinander.

**Merke:** In einer `async def`-Funktion nie `time.sleep()` benutzen, sondern `await asyncio.sleep()`. Genauso blockieren lange Rechnungen ohne `await`.''',
     """import asyncio
import time

async def lade(seite):
    print('Lade', seite)
    time.sleep(1)
    print('Fertig:', seite)

start = time.perf_counter()
await asyncio.gather(lade('A'), lade('B'))
print('Dauer:', round(time.perf_counter() - start), 's')""")
expl('''#### asyncio hilft nur beim Warten

Eine Coroutine, die lange **rechnet** (zum Beispiel alle Primzahlen bis einer Million sucht), wird durch asyncio nicht schneller und blockiert die anderen.
asyncio ist für Aufgaben gedacht, bei denen die meiste Zeit **gewartet** wird: Netzwerk, Dateien, Datenbanken, Zeitschaltuhren.
Für schwere Rechnungen gibt es andere Werkzeuge (z. B. mehrere Prozesse). Die sind nicht Thema dieser Reihe.''', None)

predict("""import asyncio

async def zaehle(name):
    for i in range(1, 3):
        print(name, i)

await asyncio.gather(zaehle('X'), zaehle('Y'))""", erklaerung='''In `zaehle` steht kein `await`. Die Coroutine `X` läuft deshalb ohne Unterbrechung durch, erst danach kommt `Y` an die Reihe.

```
X 1
X 2
Y 1
Y 2
```''')
predict("""import asyncio

async def a():
    print('a1')
    await asyncio.sleep(0)
    print('a2')

async def b():
    print('b1')
    print('b2')

await asyncio.gather(a(), b())""", erklaerung='''`a` beginnt und gibt `a1` aus. Bei `await asyncio.sleep(0)` gibt sie die Kontrolle ab, und `b` läuft los. `b` hat kein `await` und gibt `b1` und `b2` aus.
Danach macht `a` mit `a2` weiter.

```
a1
b1
b2
a2
```''')
predict("""import asyncio
import time

async def langsam():
    print('langsam Start')
    time.sleep(0.3)
    print('langsam Ende')

async def flott():
    print('flott Start')
    await asyncio.sleep(0.1)
    print('flott Ende')

await asyncio.gather(langsam(), flott())""", erklaerung='''`langsam` startet zuerst und benutzt `time.sleep()`. Das gibt die Kontrolle nicht ab: Die Coroutine `flott` kommt erst dran, wenn `langsam` ganz fertig ist.

```
langsam Start
langsam Ende
flott Start
flott Ende
```''')
predict("""import asyncio
import time

async def langsam():
    print('langsam Start')
    time.sleep(0.3)
    print('langsam Ende')

async def flott():
    print('flott Start')
    await asyncio.sleep(0.1)
    print('flott Ende')

await asyncio.gather(flott(), langsam())""", erklaerung='''Jetzt startet `flott` zuerst und wartet mit `await asyncio.sleep(0.1)`. Dabei gibt sie die Kontrolle ab, und `langsam` beginnt.
`langsam` blockiert 0,3 Sekunden. In dieser Zeit sind die 0,1 Sekunden von `flott` längst vorbei. Sobald `langsam` fertig ist, macht `flott` weiter.

```
flott Start
langsam Start
langsam Ende
flott Ende
```''')
t('''Schreibe eine Coroutine `zaehle(name)`, die `<name> 1` und `<name> 2` ausgibt, mit `await asyncio.sleep(0)` nach jeder Ausgabe.
Starte `'A'`, `'B'` und `'C'` mit `gather`. Die drei sollen sich abwechseln.''',
  given='import asyncio\n', body="""async def zaehle(name):
    for i in range(1, 3):
        print(name, i)
        await asyncio.sleep(0)

await asyncio.gather(zaehle('A'), zaehle('B'), zaehle('C'))""")
t('''Schreibe eine Coroutine `laeufer(name, runden)`, die für jede Runde `<name> Runde <nr>` ausgibt (mit `await asyncio.sleep(0)` nach jeder Runde).
Starte gleichzeitig `laeufer('Ali', 2)` und `laeufer('Bea', 4)`.''',
  given='import asyncio\n', body="""async def laeufer(name, runden):
    for nr in range(1, runden + 1):
        print(name, 'Runde', nr)
        await asyncio.sleep(0)

await asyncio.gather(laeufer('Ali', 2), laeufer('Bea', 4))""")
task('''Die beiden Bestellungen sollen gleichzeitig laufen (Dauer: `1` Sekunde), brauchen aber zwei Sekunden. Verbessere die Coroutine `bestelle`.''',
     zelle="""import asyncio
import time

async def bestelle(name):
    print(name, 'bestellt')
    time.sleep(1)
    print(name, 'bekommt sein Essen')

start = time.perf_counter()
await asyncio.gather(bestelle('Ali'), bestelle('Bea'))
print('Dauer:', round(time.perf_counter() - start), 's')""",
     solution="""import asyncio
import time

async def bestelle(name):
    print(name, 'bestellt')
    await asyncio.sleep(1)
    print(name, 'bekommt sein Essen')

start = time.perf_counter()
await asyncio.gather(bestelle('Ali'), bestelle('Bea'))
print('Dauer:', round(time.perf_counter() - start), 's')""")
t('''Schreibe eine Coroutine `bestelle(name)`. Sie gibt `<name> bestellt` aus, wartet eine Sekunde (mit `asyncio.sleep`) und gibt `<name> bekommt Essen` aus.
Lasse `'Ali'`, `'Bea'` und `'Cem'` gleichzeitig bestellen und gib die Dauer aus.''',
  given='import asyncio\nimport time\n', body="""async def bestelle(name):
    print(name, 'bestellt')
    await asyncio.sleep(1)
    print(name, 'bekommt Essen')

start = time.perf_counter()
await asyncio.gather(bestelle('Ali'), bestelle('Bea'), bestelle('Cem'))
print('Dauer:', round(time.perf_counter() - start), 's')""")
t('''Die Coroutine `pausenglocke()` gibt nach 0,2 Sekunden `Pause!` aus. Die Coroutine `unterricht()` gibt zweimal `Unterricht` aus mit `await asyncio.sleep(0.15)` danach.
Starte beide gleichzeitig. Die Ausgabe ist `Unterricht`, `Unterricht`, `Pause!`: Die Pause beginnt, während der Unterricht noch wartet.''',
  given='import asyncio\n', body="""async def pausenglocke():
    await asyncio.sleep(0.2)
    print('Pause!')

async def unterricht():
    for i in range(2):
        print('Unterricht')
        await asyncio.sleep(0.15)

await asyncio.gather(pausenglocke(), unterricht())""")

# ---------------------------------------------------------------- 6
sec('Gemischte Übungen')
t('''Die Coroutine `bestelle(gericht)` ist vorgegeben und gibt den Preis zurück. Bestelle `'Pizza'`, `'Salat'` und `'Suppe'` gleichzeitig, gib die **Gesamtsumme** (`Summe: <betrag>`)
und die Dauer aus.''',
  given="""import asyncio
import time

preise = {'Pizza': 5, 'Salat': 3, 'Suppe': 2}

async def bestelle(gericht):
    await asyncio.sleep(1)
    return preise[gericht]
""", body="""start = time.perf_counter()
ergebnisse = await asyncio.gather(bestelle('Pizza'), bestelle('Salat'), bestelle('Suppe'))
print('Summe:', sum(ergebnisse))
print('Dauer:', round(time.perf_counter() - start), 's')""")
t('''Schreibe `main()`, die für alle Klassen der Liste mit `lade_stundenplan(klasse)` den Stundenplan holt (gleichzeitig mit `gather`) und danach
für jede Klasse eine Zeile `<klasse>: <anzahl> Stunden` ausgibt. Starte `main()` im Notebook.''',
  given="""import asyncio

stunden = {'5a': 28, '6b': 30, '7c': 32}

async def lade_stundenplan(klasse):
    await asyncio.sleep(0.2)
    return stunden[klasse]

klassen = ['5a', '6b', '7c']
""", body="""async def main():
    aufgaben = []
    for klasse in klassen:
        aufgaben.append(lade_stundenplan(klasse))
    ergebnisse = await asyncio.gather(*aufgaben)
    for i in range(len(klassen)):
        print(f'{klassen[i]}: {ergebnisse[i]} Stunden')

await main()""")
t('''Zwei Küchenuhren laufen gleichzeitig. `uhr(name, schritte, takt)` gibt für jeden Schritt `<name> <schritt>` aus und wartet danach `takt` Sekunden.
Starte `uhr('A', 3, 0.1)` und `uhr('B', 2, 0.25)` gleichzeitig. Die Ausgaben der beiden Uhren mischen sich.''',
  given='import asyncio\n', body="""async def uhr(name, schritte, takt):
    for schritt in range(1, schritte + 1):
        print(name, schritt)
        await asyncio.sleep(takt)

await asyncio.gather(uhr('A', 3, 0.1), uhr('B', 2, 0.25))""")
t('''Die Coroutine `lade(seite)` ist vorgegeben (eine Sekunde, gibt die Länge des Namens zurück). Lade `'Start'` allein. Lade danach gleichzeitig `'Plan'` und `'Mensa'`.
Gib die Summe der **drei** Längen und die Gesamtdauer aus.''',
  given="""import asyncio
import time

async def lade(seite):
    await asyncio.sleep(1)
    return len(seite)
""", body="""start = time.perf_counter()
a = await lade('Start')
b, c = await asyncio.gather(lade('Plan'), lade('Mensa'))
print('Summe:', a + b + c)
print('Dauer:', round(time.perf_counter() - start), 's')""")
t('''Schreibe `main()`: Sie startet mit `gather` gleichzeitig die Coroutinen `waehle(name)` für alle Namen der Liste und gibt das **Dictionary** zurück,
das jedem Namen sein Ergebnis zuordnet. Gib `await main()` aus.''',
  given="""import asyncio

lieblingsfach = {'Ali': 'Mathe', 'Bea': 'Kunst', 'Cem': 'Sport'}

async def waehle(name):
    await asyncio.sleep(0.1)
    return lieblingsfach[name]

namen = ['Ali', 'Bea', 'Cem']
""", body="""async def main():
    aufgaben = []
    for name in namen:
        aufgaben.append(waehle(name))
    ergebnisse = await asyncio.gather(*aufgaben)
    ergebnis = {}
    for i in range(len(namen)):
        ergebnis[namen[i]] = ergebnisse[i]
    return ergebnis

print(await main())""")
task('''Die Zelle soll fünf Dokumente gleichzeitig drucken und dann `Fertig` ausgeben. Sie dauert aber fünf Sekunden und gibt die Meldungen erst am Schluss gesammelt aus.
Beseitige das Problem (Dauer: `1`).''',
     zelle="""import asyncio
import time

async def drucke(nr):
    time.sleep(1)
    print('Dokument', nr)

start = time.perf_counter()
await asyncio.gather(drucke(1), drucke(2), drucke(3), drucke(4), drucke(5))
print('Fertig')
print('Dauer:', round(time.perf_counter() - start), 's')""",
     solution="""import asyncio
import time

async def drucke(nr):
    await asyncio.sleep(1)
    print('Dokument', nr)

start = time.perf_counter()
await asyncio.gather(drucke(1), drucke(2), drucke(3), drucke(4), drucke(5))
print('Fertig')
print('Dauer:', round(time.perf_counter() - start), 's')""")
predict("""import asyncio

async def f(name, dauer):
    print(name, 'Start')
    await asyncio.sleep(dauer)
    print(name, 'Ende')
    return name

async def main():
    ergebnisse = await asyncio.gather(f('x', 0.2), f('y', 0.1))
    print(ergebnisse)
    ergebnis = await f('z', 0.1)
    print(ergebnis)

await main()""", erklaerung='''In `gather` starten `x` und `y` sofort. `y` ist nach 0,1 Sekunden fertig, `x` nach 0,2 Sekunden. Die Ergebnisliste hat die Reihenfolge der Argumente (`x`, `y`).
Danach läuft `z` allein.

```
x Start
y Start
y Ende
x Ende
['x', 'y']
z Start
z Ende
z
```''')
predict("""import asyncio

async def a():
    for i in range(2):
        print('a', i)
        await asyncio.sleep(0)

async def b():
    print('b')

async def main():
    await a()
    await asyncio.gather(a(), b())

await main()""", erklaerung='''Zuerst läuft `await a()` allein: `a 0`, `a 1` (der Wechsel bei `sleep(0)` bringt nichts, es gibt keine andere Coroutine).
Danach laufen `a` und `b` gleichzeitig: `a` beginnt mit `a 0` und gibt bei `sleep(0)` ab, `b` gibt `b` aus, dann folgt `a 1`.

```
a 0
a 1
a 0
b
a 1
```''')

generate('asyncio_grundlagen', 'asyncio 1: Grundlagen', intro=INTRO, ausfuehren=AUSFUEHREN)
