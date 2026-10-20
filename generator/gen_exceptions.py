# Erzeugt ../content/exceptions.ipynb (siehe nbgen.py).
#
# Die Unterrichtseinheit "fehler" (InfoKursCC) behandelt Fehlerarten und den Debugger, aber kein try/except.
# Die Beispiele hier sind bewusst andere als in InfoKursCC/fehler/aufgabentex (keine Zeilen wie 5 / 0, int("abc"), a[3]).
# Fehlermeldungen (str(e)) sind in Python 3.13 und 3.14 gleich; geprüft mit pyodide_check.
# Eingaben kommen nie von input(), sondern aus Listen wie eingaben = ['12', 'zwölf', ...].
from nbgen import sec, expl, task, predict, generate, setup


def t(text, given='', body='', kind='normal'):
    """Aufgabe, deren Lösung aus dem vorgegebenen Code plus body besteht."""
    task(text, given=given, solution=(given + '\n' + body) if given else body, kind=kind)


INTRO = '''In diesem Notebook geht es um **Fehler** in Python-Programmen und darum, wie ein Programm mit ihnen umgehen kann:
Fehlermeldungen lesen, Fehler mit `try` und `except` abfangen, mit `else` und `finally` aufräumen, selbst Fehler
auslösen mit `raise` und eigene Fehlertypen anlegen.

Einen Fehler, der während der Ausführung auftritt, nennt man auch **Ausnahme** (englisch *exception*).

Du solltest Bedingungen, Schleifen, Listen, Strings, Dictionaries und Funktionen schon kennen.

Jeder Abschnitt beginnt mit kurzen Erklärungen und Beispielen. Führe die Beispiele aus und probiere sie ruhig ein wenig aus.
Manche Beispiele enden absichtlich mit einer Fehlermeldung. Danach folgen viele kleine Übungen.
Wenn etwas vorgegeben ist, steht es schon in der Codezelle.'''

setup('''#### Beispieldateien anlegen

**Führe diese Zelle zuerst aus.** Sie legt im aktuellen Ordner zwei Dateien an, mit denen im Abschnitt über Dateien gearbeitet wird.
Wie man Dateien schreibt, musst du hier noch nicht verstehen.''',
      r"""dateien = {
    'temperaturen.txt': '18.5\n21\nkaputt\n19.5\n\n23\n-\n20\n',
    'punkte.csv': 'name;punkte\nAli;17\nBea;zwanzig\nCem;12\nDana\nEmil;9\n',
}
for name, inhalt in dateien.items():
    with open(name, 'w', encoding='utf-8') as f:
        f.write(inhalt)
print('Angelegt:', ', '.join(dateien))""")

# ---------------------------------------------------------------- 1
sec('Fehlermeldungen lesen')
expl('''#### Syntaxfehler und Laufzeitfehler

- Ein **Syntaxfehler** (`SyntaxError`, `IndentationError`) verstößt gegen die Regeln der Sprache. Python führt dann **gar nichts**
  aus, auch nicht die Zeilen davor.
- Ein **Laufzeitfehler** (eine Ausnahme) tritt erst während der Ausführung auf. Alles davor wurde schon ausgeführt,
  danach bricht das Programm ab.

Die Fehlermeldung (der *Traceback*) liest man **von unten**: In der letzten Zeile stehen der **Fehlertyp** und eine
Beschreibung, darüber die Zeile, in der der Fehler aufgetreten ist.''',
     """preise = [2.5, 1.2, 3.0]
print('Anfang')
print(preise[5])
print('Ende')""", error=IndexError)
expl('''#### Die wichtigsten Fehlertypen

| Fehlertyp | tritt auf, wenn ... | Beispiel |
|---|---|---|
| `NameError` | ein Name (Variable, Funktion) nicht bekannt ist | `print(summe)` ohne `summe = ...` |
| `TypeError` | ein Wert den falschen **Typ** hat | `'Note: ' + 2` |
| `ValueError` | der Typ stimmt, aber der **Wert** nicht passt | `int('2,5')` |
| `IndexError` | ein Index zu groß ist | `'abc'[7]` |
| `KeyError` | ein Schlüssel im Dictionary fehlt | `{'a': 1}['b']` |
| `ZeroDivisionError` | durch 0 geteilt wird | `10 % 0` |
| `AttributeError` | es eine Methode oder ein Attribut nicht gibt | `[1, 2].upper()` |
| `FileNotFoundError` | eine Datei nicht existiert | `open('fehlt.txt')` |''',
     """noten = {'Mathe': 2, 'Deutsch': 3}
print(noten['Physik'])""", error=KeyError)

predict("""zahlen = [4, 8, 15]
print(zahlen[len(zahlen)])""", error=IndexError)
predict("""alter = 16
print('Ich bin ' + alter + ' Jahre alt')""", error=TypeError)
predict("""print(float('3,14'))""", error=ValueError)
predict("""farben = {'rot': '#ff0000', 'blau': '#0000ff'}
print(farben['grün'])""", error=KeyError)
predict("""wort = 'Hallo'
print(wort.reverse())""", error=AttributeError)
predict("""kinder = 0
kekse = 12
print(kekse // kinder)""", error=ZeroDivisionError)
predict("""def flaeche(a, b):
    return a * b

print(flache(3, 4))""", error=NameError)
predict("""print('eins')
print('zwei')
x = len(42)
print('drei')""", error=TypeError)
predict("""werte = ['3', '4']
print(sum(werte))""", error=TypeError)
predict("""print(int('17') + 1)
print(int('17.0'))""", error=ValueError)
t('''Der folgende Code bricht mit einem `TypeError` ab:
```python
punkte = 17
print('Du hast ' + punkte + ' Punkte')
```
Schreibe ihn so, dass er fehlerfrei läuft (wandle die Zahl mit `str()` um).''',
  body="""punkte = 17
print('Du hast ' + str(punkte) + ' Punkte')""")
t('''Der folgende Code bricht mit einem `IndexError` ab, weil `range()` einen Schritt zu weit geht:
```python
woerter = ['eins', 'zwei', 'drei']
for i in range(len(woerter) + 1):
    print(i, woerter[i])
```
Schreibe ihn so, dass er alle Wörter mit ihrem Index ausgibt.''',
  body="""woerter = ['eins', 'zwei', 'drei']
for i in range(len(woerter)):
    print(i, woerter[i])""")
t('''Der folgende Code bricht mit einem `KeyError` ab:
```python
lager = {'Äpfel': 12, 'Birnen': 5}
print(lager['Kiwis'])
```
Schreibe ihn mit `get()` so, dass er für fehlende Sorten `0` ausgibt.''',
  body="""lager = {'Äpfel': 12, 'Birnen': 5}
print(lager.get('Kiwis', 0))""")
t('''Der folgende Code bricht mit einem `ValueError` ab, weil die Zahl ein Komma enthält:
```python
preis = '4,99'
print(float(preis) * 2)
```
Ersetze das Komma vor dem Umwandeln mit `replace()` durch einen Punkt, damit `9.98` ausgegeben wird.''',
  body="""preis = '4,99'
print(float(preis.replace(',', '.')) * 2)""")

# ---------------------------------------------------------------- 2
sec('try und except')
expl('''#### Fehler abfangen

Mit `try` und `except` kann ein Programm auf einen Fehler reagieren, statt abzubrechen:

```python
try:
    # Code, bei dem ein Fehler auftreten kann
except ValueError:
    # wird nur ausgeführt, wenn im try-Block ein ValueError auftritt
```

- Tritt im `try`-Block ein Fehler auf, springt Python **sofort** in den passenden `except`-Block.
  Die restlichen Zeilen im `try`-Block werden übersprungen.
- Tritt kein Fehler auf, wird der `except`-Block übersprungen.
- In beiden Fällen geht es danach **normal weiter**.''',
     """text = 'zwölf'
try:
    zahl = int(text)
    print('Die Zahl ist', zahl)
except ValueError:
    print(text, 'ist keine Zahl')
print('Das Programm läuft weiter')""")
expl('''#### Nur bestimmte Fehler abfangen

Hinter `except` steht der **Fehlertyp**. Abgefangen wird nur dieser Typ. Ein anderer Fehler bricht das Programm weiterhin ab.
Das ist gewollt: Man soll nur die Fehler abfangen, mit denen man rechnet. Ein Tippfehler im Programm (z. B. ein `NameError`)
soll nicht einfach verschwinden.''',
     """try:
    print(int('7') + zahl)
except ValueError:
    print('keine Zahl')""", error=NameError)
expl('''#### Die Fehlermeldung verwenden: `as`

Mit `except ValueError as e:` steht der Fehler in der Variablen `e`. `print(e)` gibt die Beschreibung des Fehlers aus.''',
     """try:
    int('drei')
except ValueError as e:
    print('Fehler:', e)""")

t('Wandle `text` mit `int()` in eine Zahl um und gib das Doppelte aus. Fange einen `ValueError` ab und gib dann `Das ist keine Zahl.` aus. Teste auch mit `text = \'21\'`.',
  "text = 'einundzwanzig'",
  """try:
    zahl = int(text)
    print(zahl * 2)
except ValueError:
    print('Das ist keine Zahl.')""")
t('Teile `a` durch `b` und gib das Ergebnis aus. Fange einen `ZeroDivisionError` ab und gib dann `Division durch 0 ist nicht erlaubt.` aus. Teste auch mit `b = 4`.',
  "a = 10\nb = 0",
  """try:
    print(a / b)
except ZeroDivisionError:
    print('Division durch 0 ist nicht erlaubt.')""")
t('Gib das Element von `tage` mit dem Index `i` aus. Fange einen `IndexError` ab und gib dann `Index 9 gibt es nicht.` aus (mit dem Wert von `i`).',
  "tage = ['Mo', 'Di', 'Mi', 'Do', 'Fr']\ni = 9",
  """try:
    print(tage[i])
except IndexError:
    print(f'Index {i} gibt es nicht.')""")
t('Gib die Telefonnummer von `name` aus. Fange einen `KeyError` ab und gib dann `Bea ist nicht im Telefonbuch.` aus.',
  "telefon = {'Ali': '0711 123', 'Cem': '0151 999'}\nname = 'Bea'",
  """try:
    print(telefon[name])
except KeyError:
    print(f'{name} ist nicht im Telefonbuch.')""")
t('Wandle `text` mit `float()` um und gib die Zahl aus. Fange den `ValueError` mit `as e` ab und gib `Fehler:` und die Fehlermeldung aus.',
  "text = '3,5'",
  """try:
    print(float(text))
except ValueError as e:
    print('Fehler:', e)""")
t('''Versuche, `text` mit `int()` umzuwandeln. Gelingt es, soll `zahl` den umgewandelten Wert haben, sonst den Wert `0`.
Gib danach `zahl + 1` aus. Teste mit `'41'` und mit `'vier'`.''',
  "text = 'vier'",
  """try:
    zahl = int(text)
except ValueError:
    zahl = 0
print(zahl + 1)""")
t('Gib für jedes Element von `eingaben` entweder das Quadrat der Zahl aus oder `xyz ist keine ganze Zahl` (mit dem Text).',
  "eingaben = ['4', '7', 'acht', '2.5', '-3']",
  """for e in eingaben:
    try:
        z = int(e)
        print(z * z)
    except ValueError:
        print(e, 'ist keine ganze Zahl')""")
expl('''#### `pass`: nichts tun

Ein `except`-Block darf nicht leer sein. Soll beim Fehler einfach gar nichts passieren, schreibt man `pass`.''',
     """for e in ['1', 'a', '2']:
    try:
        print(int(e))
    except ValueError:
        pass""")
t('Berechne die Summe aller Elemente von `eingaben`, die sich mit `int()` umwandeln lassen. Die anderen werden übersprungen. Gib die Summe aus.',
  "eingaben = ['12', 'x', '8', '', '30', 'zehn', '-5']",
  """summe = 0
for e in eingaben:
    try:
        summe += int(e)
    except ValueError:
        pass
print(summe)""")
t('Sammle alle Elemente von `eingaben`, die sich mit `float()` in eine Zahl umwandeln lassen, als Zahlen in einer Liste und gib sie aus. Für die anderen schreibst du `pass`.',
  "eingaben = ['1.5', 'zwei', '3', '4,5', '-0.25', '']",
  """zahlen = []
for e in eingaben:
    try:
        zahlen.append(float(e))
    except ValueError:
        pass
print(zahlen)""")
t('Zähle, wie viele Elemente von `eingaben` **keine** gültigen ganzen Zahlen sind. Gib die Anzahl aus.',
  "eingaben = ['7', 'sieben', '07', '7.0', ' 7 ', 'VII']",
  """fehler = 0
for e in eingaben:
    try:
        int(e)
    except ValueError:
        fehler += 1
print(fehler)""")
t('''Teile 100 nacheinander durch jede Zahl in `teiler` und gib das Ergebnis aus. Bei 0 gib stattdessen `durch 0 geht nicht` aus.''',
  "teiler = [4, 0, 8, 0, 5]",
  """for d in teiler:
    try:
        print(100 / d)
    except ZeroDivisionError:
        print('durch 0 geht nicht')""")
t('''Gib für jedes Wort in `woerter` den Buchstaben mit dem Index 4 aus. Ist das Wort zu kurz, gib `(zu kurz)` aus.''',
  "woerter = ['Python', 'Hund', 'Elefant', 'Igel', 'Banane']",
  """for w in woerter:
    try:
        print(w[4])
    except IndexError:
        print('(zu kurz)')""")
predict("""try:
    print('A')
    x = int('B')
    print('C')
except ValueError:
    print('D')
print('E')""")
predict("""try:
    print('A')
    x = int('5')
    print('C')
except ValueError:
    print('D')
print('E')""")
predict("""try:
    werte = [1, 2, 3]
    print(werte[3])
except ValueError:
    print('falscher Wert')
print('fertig')""", error=IndexError)
predict("""summe = 0
for t in ['5', 'x', '10', '2y']:
    try:
        summe += int(t)
        print('ok', summe)
    except ValueError:
        print('nicht', t)
print(summe)""")

# ---------------------------------------------------------------- 3
sec('Mehrere Fehlertypen')
expl('''#### Mehrere `except`-Blöcke

Ein `try` kann mehrere `except`-Blöcke haben. Python nimmt den **ersten**, dessen Fehlertyp passt.
Mehrere Fehlertypen kann man auch in **einem** Block zusammenfassen, als Tupel: `except (ValueError, ZeroDivisionError):`''',
     """for text in ['4', 'vier', '0']:
    try:
        print(12 / int(text))
    except ValueError:
        print(text, 'ist keine Zahl')
    except ZeroDivisionError:
        print('Teilen durch 0 geht nicht')

for text in ['4', 'vier', '0']:
    try:
        print(12 / int(text))
    except (ValueError, ZeroDivisionError):
        print('ungültig:', text)""")
expl('''#### `Exception` fängt fast alles

`except Exception as e:` fängt jeden normalen Fehler. Den Namen des Fehlertyps erhält man mit `type(e).__name__`
(`type(e)` kennst du schon, `.__name__` ist der Name des Typs als Text).

`Exception` ist praktisch, um Fehler zu **melden**, aber man sieht dann nicht mehr, *welcher* Fehler gemeint war.
Steht `except Exception` zusammen mit anderen Blöcken, muss er als **letzter** kommen, sonst kommen die anderen nie dran.''',
     """aufgaben = ['10 / 0', 'int("x")', '[1][2]', '{}["a"]']
for code in aufgaben:
    try:
        eval(code)
    except Exception as e:
        print(code, '->', type(e).__name__)""")
expl('''#### Was ist `eval()`?

`eval(text)` führt einen Python-**Ausdruck**, der als Text gegeben ist, aus und gibt sein Ergebnis zurück.
Hier ist es praktisch, um viele kleine Fehler auszuprobieren. In echten Programmen benutzt man `eval()` fast nie,
weil damit beliebiger Code ausgeführt werden kann.''',
     """print(eval('3 + 4 * 2'))
print(eval('len("Hallo")'))""")

t('''Teile `gesamt` durch die Zahl in `text`. Gib bei einem `ValueError` `Keine Zahl!` aus und bei einem
`ZeroDivisionError` `Nicht durch 0!`. Verwende zwei `except`-Blöcke. Teste mit `'0'`, `'null'` und `'4'`.''',
  "gesamt = 24\ntext = '0'",
  """try:
    print(gesamt / int(text))
except ValueError:
    print('Keine Zahl!')
except ZeroDivisionError:
    print('Nicht durch 0!')""")
t('''Gib für jedes Element von `eingaben` aus, wie viele Kekse jedes von `int(e)` Kindern bekommt, wenn 30 Kekse gerecht
verteilt werden (`30 // anzahl`). Fange `ValueError` und `ZeroDivisionError` **in einem** `except`-Block ab und gib dann `ungültig: ...` aus.''',
  "eingaben = ['3', 'drei', '0', '7', '']",
  """for e in eingaben:
    try:
        print(30 // int(e))
    except (ValueError, ZeroDivisionError):
        print('ungültig:', e)""")
t('''Gib für jeden Index in `indizes` das Element aus `zahlen` aus. Gib bei einem `IndexError` `kein Element` und
bei einem `TypeError` `kein Index` aus (ein Index muss eine ganze Zahl sein).''',
  "zahlen = [10, 20, 30]\nindizes = [0, 5, '1', -1, 1.0]",
  """for i in indizes:
    try:
        print(zahlen[i])
    except IndexError:
        print('kein Element')
    except TypeError:
        print('kein Index')""")
t('''Führe jeden Ausdruck in `ausdruecke` mit `eval()` aus und gib das Ergebnis aus. Bei einem Fehler gib den Ausdruck,
einen Pfeil und den Namen des Fehlertyps aus, in der Form `1 / 0 -> ZeroDivisionError`.''',
  "ausdruecke = ['2 ** 10', '1 / 0', 'int(\"1e3\")', '\"ab\" * 3', '\"ab\" * \"c\"', '[1, 2].index(5)', 'max([])']",
  """for a in ausdruecke:
    try:
        print(eval(a))
    except Exception as e:
        print(a, '->', type(e).__name__)""")
t('''Zähle mit einem Dictionary, welcher Fehlertyp bei den Ausdrücken in `ausdruecke` wie oft auftritt. Ausdrücke ohne Fehler zählen
unter `kein Fehler`. Gib das Dictionary aus.''',
  "ausdruecke = ['int(\"x\")', '7 // 0', 'float(\"2.5\")', '\"abc\"[3]', 'int(\"\")', '{}[0]', '5 % 0', 'abs(-3)']",
  """anzahl = {}
for a in ausdruecke:
    try:
        eval(a)
        name = 'kein Fehler'
    except Exception as e:
        name = type(e).__name__
    anzahl[name] = anzahl.get(name, 0) + 1
print(anzahl)""")
t('''Die Daten in `daten` sind Paare aus einem Namen und einer Punktzahl als Text. Berechne für jedes Paar den Anteil an
`maximal` Punkten in Prozent (ganzzahlig mit `//`). Bei einem Fehler gib den Namen und den Fehlertyp aus,
in der Form `Bea: ValueError`. Teste auch, was passiert, wenn `maximal = 0` ist.''',
  "daten = [('Ali', '18'), ('Bea', 'achtzehn'), ('Cem', '9')]\nmaximal = 20",
  """for name, text in daten:
    try:
        print(name, int(text) * 100 // maximal)
    except Exception as e:
        print(f'{name}: {type(e).__name__}')""")
predict("""for x in ['6', 'sechs', '0']:
    try:
        print(60 // int(x))
    except ZeroDivisionError:
        print('null')
    except ValueError:
        print('text')""")
predict("""try:
    d = {'a': 1}
    print(d['a'] + d['b'])
except (IndexError, KeyError):
    print('nicht gefunden')""")
predict("""try:
    print(len(5))
except Exception as e:
    print(type(e).__name__)""")
predict("""try:
    zahl = int('1.5')
except Exception:
    print('allgemein')
except ValueError:
    print('Wert')""")

# ---------------------------------------------------------------- 4
sec('else und finally')
expl('''#### `else`: nur wenn es keinen Fehler gab

Ein `else`-Block nach den `except`-Blöcken wird nur ausgeführt, wenn im `try`-Block **kein** Fehler aufgetreten ist.
So bleibt der `try`-Block kurz: Darin steht nur die Zeile, die schiefgehen kann.''',
     """for text in ['8', 'acht']:
    try:
        zahl = int(text)
    except ValueError:
        print(text, 'ist ungültig')
    else:
        print('Das Doppelte ist', zahl * 2)""")
expl('''#### `finally`: auf jeden Fall

Ein `finally`-Block wird **immer** ausgeführt: wenn alles geklappt hat, wenn ein Fehler abgefangen wurde und sogar, wenn ein Fehler
**nicht** abgefangen wird (dann erst `finally`, danach der Abbruch). Er ist für Aufräumarbeiten gedacht, z. B. eine Meldung „fertig“.

Die Reihenfolge ist immer `try` – `except` – `else` – `finally`.''',
     """for text in ['5', 'fünf']:
    try:
        zahl = int(text)
    except ValueError:
        print('Fehler')
    else:
        print('Zahl', zahl)
    finally:
        print('geprüft:', text)""")

t('''Wandle `text` in eine ganze Zahl um. Gib bei einem Fehler `ungültige Eingabe` aus. Gib im `else`-Block aus,
ob die Zahl gerade oder ungerade ist (`gerade`/`ungerade`). Teste mit `'17'`, `'18'` und `'1 7'`.''',
  "text = '17'",
  """try:
    zahl = int(text)
except ValueError:
    print('ungültige Eingabe')
else:
    if zahl % 2 == 0:
        print('gerade')
    else:
        print('ungerade')""")
t('''Gib für jedes Element von `eingaben` entweder `xyz ist ungültig` aus oder (im `else`-Block) die Zahl mit 19 % Mehrwertsteuer
mit zwei Nachkommastellen. Gib im `finally`-Block jedes Mal `---` aus.''',
  "eingaben = ['10', 'zehn', '2.50']",
  """for e in eingaben:
    try:
        preis = float(e)
    except ValueError:
        print(e, 'ist ungültig')
    else:
        print(f'{preis * 1.19:.2f}')
    finally:
        print('---')""")
t('''Schlage jeden Namen aus `gesucht` in `noten` nach. Gib bei einem fehlenden Namen `Ida: keine Note` aus,
sonst im `else`-Block `Ali: 2`. Zähle außerdem in einem `finally`-Block, wie viele Namen nachgeschlagen wurden, und gib
die Anzahl am Ende aus.''',
  "noten = {'Ali': 2, 'Bea': 1, 'Cem': 3}\ngesucht = ['Ali', 'Ida', 'Cem', 'Tom']",
  """anzahl = 0
for name in gesucht:
    try:
        note = noten[name]
    except KeyError:
        print(f'{name}: keine Note')
    else:
        print(f'{name}: {note}')
    finally:
        anzahl += 1
print(anzahl)""")
t('''Zähle, wie viele Elemente von `eingaben` gültige Kommazahlen sind und wie viele nicht. Erhöhe den Zähler `gueltig` im
`else`-Block und `ungueltig` im `except`-Block. Gib beide Zähler aus.''',
  "eingaben = ['1.5', '2,5', '3', 'drei', '.5', '1e2', '']",
  """gueltig = 0
ungueltig = 0
for e in eingaben:
    try:
        float(e)
    except ValueError:
        ungueltig += 1
    else:
        gueltig += 1
print(gueltig, ungueltig)""")
predict("""try:
    x = int('3')
except ValueError:
    print('A')
else:
    print('B')
finally:
    print('C')""")
predict("""try:
    x = int('drei')
except ValueError:
    print('A')
else:
    print('B')
finally:
    print('C')""")
predict("""try:
    print('start')
    x = [1, 2][2]
except KeyError:
    print('Schlüssel')
finally:
    print('aufräumen')
print('ende')""", error=IndexError)

# ---------------------------------------------------------------- 5
sec('Fehler in Funktionen und Schleifen')
expl('''#### Fehler wandern nach oben

Tritt in einer Funktion ein Fehler auf und wird er dort **nicht** abgefangen, bricht die Funktion ab und der Fehler geht an die
Stelle, an der die Funktion aufgerufen wurde. Dort kann man ihn abfangen. Der Traceback zeigt dann alle beteiligten Aufrufe.''',
     """def mittelwert(liste):
    return sum(liste) / len(liste)

try:
    print(mittelwert([2, 4, 9]))
    print(mittelwert([]))
except ZeroDivisionError:
    print('Leere Liste hat keinen Mittelwert')""")
expl('''#### Eine Funktion, die den Fehler selbst abfängt

Oft fängt eine Funktion den Fehler selbst ab und gibt dann einen besonderen Wert zurück, z. B. `None`.
Mit `if ergebnis is None:` prüft man danach, ob es geklappt hat.''',
     """def als_zahl(text):
    try:
        return int(text)
    except ValueError:
        return None

for t in ['42', 'zweiundvierzig']:
    z = als_zahl(t)
    if z is None:
        print(t, '-> ungültig')
    else:
        print(t, '->', z)""")
expl('''#### So lange versuchen, bis es klappt

Mit `while True:` und `break` kann man es so lange versuchen, bis eine Eingabe gültig ist. Hier kommen die „Eingaben“
aus einer Liste, wie wenn jemand nacheinander verschiedene Dinge eintippt.

`repr(text)` gibt den Text **mit** Anführungszeichen zurück. So sieht man auch einen leeren Text `''` oder Leerzeichen.''',
     """eingaben = ['abc', '', '15', '20']
nr = 0
while True:
    text = eingaben[nr]
    nr += 1
    try:
        alter = int(text)
        break
    except ValueError:
        print(repr(text), 'ist ungültig, nochmal')
print('Alter:', alter)""")

t('''Schreibe eine Funktion `sicher_teilen(a, b)`, die `a / b` zurückgibt und bei einer Division durch 0 `None`.
Gib `sicher_teilen(7, 2)` und `sicher_teilen(7, 0)` aus.''',
  body="""def sicher_teilen(a, b):
    try:
        return a / b
    except ZeroDivisionError:
        return None

print(sicher_teilen(7, 2))
print(sicher_teilen(7, 0))""")
t('''Schreibe eine Funktion `als_float(text, standard)`, die `text` als Kommazahl zurückgibt. Lässt sich `text` nicht umwandeln,
soll sie `standard` zurückgeben. Gib `als_float('2.5', 0)`, `als_float('zwei', 0)` und `als_float('', -1)` aus.''',
  body="""def als_float(text, standard):
    try:
        return float(text)
    except ValueError:
        return standard

print(als_float('2.5', 0))
print(als_float('zwei', 0))
print(als_float('', -1))""")
t('''Schreibe eine Funktion `element(liste, i)`, die `liste[i]` zurückgibt und `'-'`, wenn es diesen Index nicht gibt.
Gib damit für die Indizes 0 bis 4 die Elemente von `planeten` in einer Zeile aus (mit `end=' '`).''',
  "planeten = ['Merkur', 'Venus', 'Erde']",
  """def element(liste, i):
    try:
        return liste[i]
    except IndexError:
        return '-'

for i in range(5):
    print(element(planeten, i), end=' ')
print()""")
t('''Die Funktion `mittelwert()` ist vorgegeben. Rufe sie für jede Liste in `listen` auf und gib den Mittelwert aus.
Fange den Fehler bei der leeren Liste **beim Aufruf** ab und gib dann `leer` aus.''',
  "def mittelwert(liste):\n    return sum(liste) / len(liste)\n\nlisten = [[1, 2, 3], [], [10, 20]]",
  """for liste in listen:
    try:
        print(mittelwert(liste))
    except ZeroDivisionError:
        print('leer')""")
t('''Die Funktion `preis_mit_rabatt()` ist vorgegeben. Rufe sie für jedes Paar in `tests` auf. Gib das Ergebnis aus oder,
bei einem Fehler, den Namen des Fehlertyps. (Bei einem Text statt einer Zahl entsteht ein `TypeError`.)''',
  "def preis_mit_rabatt(preis, prozent):\n    return preis - preis * prozent / 100\n\ntests = [(80, 25), (80, '25'), ('80', 25), (50, 10)]",
  """for preis, prozent in tests:
    try:
        print(preis_mit_rabatt(preis, prozent))
    except Exception as e:
        print(type(e).__name__)""")
t('''Simuliere eine Eingabe: Nimm nacheinander die Texte aus `eingaben`, bis einer eine ganze Zahl von 1 bis 6 ist.
Gib für ungültige Texte `ungültig: ...` aus und am Ende `Gewürfelt: ...`. Ist der Text eine Zahl, aber nicht von 1 bis 6, ist er auch ungültig.''',
  "eingaben = ['sechs', '0', '7', '4', '2']",
  """nr = 0
while True:
    text = eingaben[nr]
    nr += 1
    try:
        zahl = int(text)
    except ValueError:
        print('ungültig:', text)
        continue
    if 1 <= zahl <= 6:
        break
    print('ungültig:', text)
print('Gewürfelt:', zahl)""")
t('''Wie viele Versuche braucht die Person, bis sie eine gültige Kommazahl eingibt? Nimm die Texte nacheinander aus `eingaben`
und gib am Ende die Zahl und die Anzahl der Versuche aus, in der Form `1.75 nach 4 Versuchen`.''',
  "eingaben = ['eins', '1,75', '1.75m', '1.75', '2']",
  """versuche = 0
for text in eingaben:
    versuche += 1
    try:
        zahl = float(text)
        break
    except ValueError:
        pass
print(f'{zahl} nach {versuche} Versuchen')""")
t('''Schreibe eine Funktion `summe_gueltiger(texte)`, die die Summe aller Texte zurückgibt, die ganze Zahlen sind, und dazu eine
Liste der ungültigen Texte. Gib beides für `daten` aus.''',
  "daten = ['3', 'drei', '10', '1.5', '-2', 'x']",
  """def summe_gueltiger(texte):
    summe = 0
    ungueltig = []
    for t in texte:
        try:
            summe += int(t)
        except ValueError:
            ungueltig.append(t)
    return summe, ungueltig

s, u = summe_gueltiger(daten)
print(s)
print(u)""")
t('''Die Zeilen in `zeilen` haben die Form `Name:Alter`. Erstelle ein Dictionary von Namen zu Alter (als Zahl). Zeilen ohne `:`
(beim Entpacken entsteht ein `ValueError`) oder mit ungültigem Alter (auch ein `ValueError`) werden übersprungen und gemeldet,
in der Form `übersprungen: ...`. Gib am Ende das Dictionary aus.''',
  "zeilen = ['Ali:16', 'Bea:siebzehn', 'Cem:15', 'Dana', 'Emil:17:x', 'Fiona:14']",
  """alter = {}
for z in zeilen:
    try:
        name, a = z.split(':')
        alter[name] = int(a)
    except ValueError:
        print('übersprungen:', z)
print(alter)""")
predict("""def f(x):
    print('f', x)
    return 10 // x

try:
    print(f(5))
    print(f(0))
    print(f(2))
except ZeroDivisionError:
    print('Fehler')""")
predict("""def teste(text):
    try:
        return int(text)
    except ValueError:
        return -1

print(teste('8') + teste('acht'))""")

# ---------------------------------------------------------------- 6
sec('Fehler bei Dateien')
expl('''#### `FileNotFoundError`

Gibt es eine Datei nicht, wirft `open()` einen `FileNotFoundError`. Den fängt man wie jeden anderen Fehler ab.
Die Setup-Zelle ganz oben hat die Dateien `temperaturen.txt` und `punkte.csv` angelegt.''',
     """for name in ['temperaturen.txt', 'fehlt.txt']:
    try:
        with open(name, encoding='utf-8') as f:
            print(name, 'hat', len(f.readlines()), 'Zeilen')
    except FileNotFoundError:
        print(name, 'gibt es nicht')""")

t('Öffne die Datei `name` und gib ihren Inhalt aus. Gibt es die Datei nicht, gib `Datei notizen.txt nicht gefunden` aus.',
  "name = 'notizen.txt'",
  """try:
    with open(name, encoding='utf-8') as f:
        print(f.read())
except FileNotFoundError:
    print(f'Datei {name} nicht gefunden')""")
t('''Gib für jeden Dateinamen in `namen` aus, wie viele Zeilen die Datei hat, oder `fehlt`, wenn es sie nicht gibt.
Form: `punkte.csv: 6`.''',
  "namen = ['punkte.csv', 'noten.txt', 'temperaturen.txt']",
  """for name in namen:
    try:
        with open(name, encoding='utf-8') as f:
            print(f'{name}: {len(f.readlines())}')
    except FileNotFoundError:
        print(f'{name}: fehlt')""")
t('''In `temperaturen.txt` steht in jeder Zeile eine Temperatur, aber einige Zeilen sind kaputt oder leer. Lies die Datei,
wandle jede Zeile mit `float()` um und sammle die gültigen Werte. Gib die Liste und den Mittelwert mit einer Nachkommastelle aus.''',
  body="""werte = []
with open('temperaturen.txt', encoding='utf-8') as f:
    for zeile in f:
        try:
            werte.append(float(zeile))
        except ValueError:
            pass
print(werte)
print(f'{sum(werte) / len(werte):.1f}')""")
t('''Lies `temperaturen.txt` und gib für jede ungültige Zeile ihre Nummer (ab 1) und ihren Inhalt mit `repr()` aus,
in der Form `Zeile 3: 'kaputt'`. Entferne vorher mit `strip()` den Zeilenumbruch.''',
  body="""with open('temperaturen.txt', encoding='utf-8') as f:
    for nr, zeile in enumerate(f, 1):
        zeile = zeile.strip()
        try:
            float(zeile)
        except ValueError:
            print(f'Zeile {nr}: {repr(zeile)}')""")
t('''`punkte.csv` hat eine Kopfzeile und dann Zeilen der Form `name;punkte`. Manche Zeilen sind fehlerhaft.
Berechne die Summe der gültigen Punkte und gib die Namen (bzw. Zeilen) mit Fehler in der Form `Fehler in Zeile: Dana` aus.
Überspringe die Kopfzeile mit `f.readline()`.''',
  body="""summe = 0
with open('punkte.csv', encoding='utf-8') as f:
    f.readline()
    for zeile in f:
        zeile = zeile.strip()
        try:
            name, punkte = zeile.split(';')
            summe += int(punkte)
        except ValueError:
            print('Fehler in Zeile:', zeile)
print(summe)""")
t('''Schreibe eine Funktion `zeilen_zaehlen(name)`, die die Anzahl der Zeilen der Datei zurückgibt und `-1`, wenn es sie nicht gibt.
Gib `zeilen_zaehlen('punkte.csv')` und `zeilen_zaehlen('gibtsnicht.txt')` aus.''',
  body="""def zeilen_zaehlen(name):
    try:
        with open(name, encoding='utf-8') as f:
            return len(f.readlines())
    except FileNotFoundError:
        return -1

print(zeilen_zaehlen('punkte.csv'))
print(zeilen_zaehlen('gibtsnicht.txt'))""")

# ---------------------------------------------------------------- 7
sec('Selbst Fehler auslösen mit raise')
expl('''#### `raise`

Mit `raise` löst man **selbst** einen Fehler aus. Das macht man in Funktionen, die mit einem Wert nichts anfangen können:
`raise ValueError('Beschreibung')`. Wer die Funktion aufruft, kann den Fehler dann mit `try` und `except` abfangen.

Welcher Typ passt? `ValueError` für einen falschen Wert, `TypeError` für einen falschen Typ.''',
     """def wurzel(x):
    if x < 0:
        raise ValueError('x darf nicht negativ sein')
    return x ** 0.5

print(wurzel(16))
try:
    print(wurzel(-4))
except ValueError as e:
    print('Fehler:', e)""")
expl('''#### Fehler weitergeben

Ein `raise` ohne etwas dahinter im `except`-Block gibt den abgefangenen Fehler **weiter**. So kann man einen Fehler melden
und trotzdem abbrechen.''',
     """try:
    int('zehn')
except ValueError:
    print('Melde: ungültige Zahl')
    raise""", error=ValueError)
expl('''#### `isinstance()`

`isinstance(wert, int)` prüft, ob `wert` vom Typ `int` ist. Mit einem Tupel prüft man mehrere Typen: `isinstance(wert, (int, float))`.''',
     """print(isinstance(5, int))
print(isinstance('5', int))
print(isinstance(2.5, (int, float)))""")

t('''Schreibe eine Funktion `setze_note(note)`, die die Note zurückgibt, wenn sie von 1 bis 6 ist, und sonst einen `ValueError` mit
der Meldung `Note muss zwischen 1 und 6 liegen` auslöst. Rufe sie für jede Zahl in `tests` auf und gib das Ergebnis oder `Fehler: ...` aus.''',
  "tests = [2, 7, 6, 0]",
  """def setze_note(note):
    if note < 1 or note > 6:
        raise ValueError('Note muss zwischen 1 und 6 liegen')
    return note

for n in tests:
    try:
        print(setze_note(n))
    except ValueError as e:
        print('Fehler:', e)""")
t('''Schreibe eine Funktion `kreisflaeche(r)`, die bei negativem Radius einen `ValueError` mit der Meldung `negativer Radius: -2`
(mit dem Wert) auslöst und sonst `3.14 * r * r` zurückgibt. Gib `kreisflaeche(10)` aus und fange den Fehler bei `kreisflaeche(-2)` ab.''',
  body="""def kreisflaeche(r):
    if r < 0:
        raise ValueError(f'negativer Radius: {r}')
    return 3.14 * r * r

print(kreisflaeche(10))
try:
    print(kreisflaeche(-2))
except ValueError as e:
    print(e)""")
t('''Schreibe eine Funktion `verdopple(x)`, die einen `TypeError` mit der Meldung `Zahl erwartet` auslöst, wenn `x` kein `int` und kein
`float` ist (prüfe mit `isinstance()`), und sonst `2 * x` zurückgibt. Teste mit allen Werten in `tests`.''',
  "tests = [4, 2.5, '4', [4]]",
  """def verdopple(x):
    if not isinstance(x, (int, float)):
        raise TypeError('Zahl erwartet')
    return 2 * x

for x in tests:
    try:
        print(verdopple(x))
    except TypeError as e:
        print(e)""")
t('''Schreibe eine Funktion `abheben(konto, betrag)`, die den neuen Kontostand zurückgibt. Ist `betrag` nicht positiv, soll sie einen
`ValueError('Betrag muss positiv sein')` auslösen, ist zu wenig Geld auf dem Konto, einen `ValueError('Kontostand zu niedrig')`.
Hebe nacheinander die Beträge in `abhebungen` ab und gib nach jedem Versuch den Kontostand oder die Fehlermeldung aus.''',
  "konto = 100\nabhebungen = [30, -5, 80, 50, 20]",
  """def abheben(konto, betrag):
    if betrag <= 0:
        raise ValueError('Betrag muss positiv sein')
    if betrag > konto:
        raise ValueError('Kontostand zu niedrig')
    return konto - betrag

for b in abhebungen:
    try:
        konto = abheben(konto, b)
        print(konto)
    except ValueError as e:
        print(e)""")
t('''Schreibe eine Funktion `pruefe_passwort(pw)`, die einen `ValueError` auslöst, wenn das Passwort kürzer als 8 Zeichen ist
(`zu kurz`) oder keine Ziffer enthält (`keine Ziffer`). Sonst gibt sie `True` zurück. Teste mit allen Passwörtern in `tests`,
in der Form `abc: zu kurz`.''',
  "tests = ['abc', 'geheimnis', 'geheim42', 'a1']",
  """def pruefe_passwort(pw):
    if len(pw) < 8:
        raise ValueError('zu kurz')
    ziffer = False
    for z in pw:
        if z.isdigit():
            ziffer = True
    if not ziffer:
        raise ValueError('keine Ziffer')
    return True

for pw in tests:
    try:
        print(f'{pw}: {pruefe_passwort(pw)}')
    except ValueError as e:
        print(f'{pw}: {e}')""")
t('''Schreibe eine Funktion `uhrzeit(text)`, die einen Text wie `'14:05'` in ein Tupel `(14, 5)` umwandelt. Sind Stunde oder Minute
außerhalb von 0–23 bzw. 0–59, löst sie `ValueError('ungültige Uhrzeit')` aus. (Fehlt der Doppelpunkt oder sind es keine Zahlen,
entsteht beim Entpacken oder bei `int()` ohnehin ein `ValueError`.) Gib für jeden Text in `tests` das Tupel oder `ungültig: ...` aus.''',
  "tests = ['14:05', '25:00', '7:30', 'halb acht', '12:60']",
  """def uhrzeit(text):
    h, m = text.split(':')
    h = int(h)
    m = int(m)
    if h < 0 or h > 23 or m < 0 or m > 59:
        raise ValueError('ungültige Uhrzeit')
    return (h, m)

for text in tests:
    try:
        print(uhrzeit(text))
    except ValueError:
        print('ungültig:', text)""")
task('''Wandle jedes Element von `eingaben` mit `int()` um. Bei einem Fehler gib `Problem mit: ...` aus und gib den Fehler dann mit
`raise` weiter, sodass das Programm abbricht. (Die Zelle endet also mit einer Fehlermeldung, nach `Problem mit: 3x`.)''',
  given="eingaben = ['1', '2', '3x', '4']",
  solution="""eingaben = ['1', '2', '3x', '4']
for e in eingaben:
    try:
        print(int(e))
    except ValueError:
        print('Problem mit:', e)
        raise""", error=ValueError)
predict("""def pruefe(x):
    if x > 10:
        raise ValueError('zu groß')
    return x

for x in [3, 12, 7]:
    try:
        print(pruefe(x))
    except ValueError as e:
        print(e)""")
predict("""def f(x):
    if not isinstance(x, int):
        raise TypeError('int erwartet')
    return x + 1

print(f(1))
print(f('1'))
print(f(2))""", error=TypeError)

# ---------------------------------------------------------------- 8
sec('Eigene Fehlertypen und assert')
expl('''#### Eigene Fehlertypen

Einen eigenen Fehlertyp legt man mit **zwei Zeilen** an (eine *Klasse*, mehr musst du hier darüber nicht wissen):

```python
class KontoFehler(Exception):
    pass
```

Danach kann man `raise KontoFehler('...')` und `except KontoFehler:` genau wie bei den eingebauten Fehlern verwenden.
Der Vorteil: Man fängt gezielt die Fehler des eigenen Programms ab und nicht versehentlich andere.''',
     """class LagerFehler(Exception):
    pass

def entnehmen(bestand, anzahl):
    if anzahl > bestand:
        raise LagerFehler(f'nur noch {bestand} da')
    return bestand - anzahl

try:
    print(entnehmen(10, 3))
    print(entnehmen(10, 30))
except LagerFehler as e:
    print('Lagerproblem:', e)""")
expl('''#### `assert`

`assert bedingung, 'Meldung'` prüft eine Bedingung, von der man **sicher** ist, dass sie stimmen muss. Ist sie falsch, gibt es
einen `AssertionError` mit der Meldung. `assert` ist zum Testen des **eigenen** Programms gedacht, z. B. um eine Funktion
zu prüfen. Für falsche Eingaben von außen nimmt man `raise`.''',
     """def quadrat(x):
    return x * x

assert quadrat(3) == 9
assert quadrat(-2) == 4
print('Alle Tests bestanden')
assert quadrat(0) == 1, 'quadrat(0) ist falsch'""", error=AssertionError)

t('''Lege einen Fehlertyp `AlterFehler` an. Schreibe eine Funktion `pruefe_alter(alter)`, die bei einem Alter unter 0 oder über 130
`AlterFehler('unmögliches Alter: ...')` auslöst und sonst das Alter zurückgibt. Teste mit allen Werten in `tests`.''',
  "tests = [15, -3, 42, 200]",
  """class AlterFehler(Exception):
    pass

def pruefe_alter(alter):
    if alter < 0 or alter > 130:
        raise AlterFehler(f'unmögliches Alter: {alter}')
    return alter

for a in tests:
    try:
        print(pruefe_alter(a))
    except AlterFehler as e:
        print(e)""")
t('''Lege einen Fehlertyp `ZugFehler` an. Schreibe eine Funktion `setze(feld, nr)` für ein Tic-Tac-Toe-Feld (Liste mit 9 Einträgen),
die `'X'` an Position `nr` setzt. Ist `nr` nicht von 0 bis 8, löst sie `ZugFehler('kein Feld')` aus, ist das Feld schon belegt,
`ZugFehler('besetzt')`. Führe die Züge in `zuege` aus, gib bei einem Fehler die Meldung aus und am Ende das Feld.''',
  "feld = ['.'] * 9\nzuege = [4, 4, 9, 0, 8]",
  """class ZugFehler(Exception):
    pass

def setze(feld, nr):
    if nr < 0 or nr > 8:
        raise ZugFehler('kein Feld')
    if feld[nr] != '.':
        raise ZugFehler('besetzt')
    feld[nr] = 'X'

for nr in zuege:
    try:
        setze(feld, nr)
    except ZugFehler as e:
        print(nr, e)
print(feld)""")
t('''Der Fehlertyp `BestellFehler` und die Funktion `bestellen()` sind vorgegeben. Bestelle nacheinander alles aus `bestellungen`.
Fange **nur** `BestellFehler` ab und gib dann `nicht möglich: ...` aus, sonst `bestellt: ...`. Gib am Ende das Lager aus.''',
  "class BestellFehler(Exception):\n    pass\n\nlager = {'Brezel': 5, 'Brötchen': 10}\n\n"
  "def bestellen(artikel, anzahl):\n    if artikel not in lager:\n        raise BestellFehler(f'{artikel} gibt es nicht')\n"
  "    if lager[artikel] < anzahl:\n        raise BestellFehler(f'nur {lager[artikel]} {artikel} da')\n    lager[artikel] -= anzahl\n\n"
  "bestellungen = [('Brezel', 3), ('Croissant', 1), ('Brezel', 3), ('Brötchen', 10)]",
  """for artikel, anzahl in bestellungen:
    try:
        bestellen(artikel, anzahl)
        print('bestellt:', anzahl, artikel)
    except BestellFehler as e:
        print('nicht möglich:', e)
print(lager)""")
expl('''Hier deckt ein Test einen Fehler auf: `groesste` beginnt mit 0, deshalb ist das Maximum negativer Zahlen falsch.''',
     """def maximum(liste):
    groesste = 0
    for x in liste:
        if x > groesste:
            groesste = x
    return groesste

assert maximum([3, 9, 2]) == 9
assert maximum([-5, -2, -8]) == -2, 'negatives Maximum falsch'""", error=AssertionError)
t('''Schreibe die Funktion `maximum()` aus dem Beispiel darüber so, dass `groesste` mit dem ersten Element der Liste beginnt.
Teste sie mit `assert`: `maximum([3, 9, 2])` soll 9 sein, `maximum([-5, -2, -8])` soll -2 sein und `maximum([7])` soll 7 sein.
Gib danach `alle Tests bestanden` aus.''',
  body="""def maximum(liste):
    groesste = liste[0]
    for x in liste:
        if x > groesste:
            groesste = x
    return groesste

assert maximum([3, 9, 2]) == 9
assert maximum([-5, -2, -8]) == -2
assert maximum([7]) == 7
print('alle Tests bestanden')""")
t('''Schreibe eine Funktion `quersumme(n)` und teste sie mit drei `assert`-Anweisungen: `quersumme(123) == 6`, `quersumme(9) == 9`
und `quersumme(1000) == 1`. Gib danach `ok` aus.''',
  body="""def quersumme(n):
    s = 0
    while n > 0:
        s += n % 10
        n = n // 10
    return s

assert quersumme(123) == 6
assert quersumme(9) == 9
assert quersumme(1000) == 1
print('ok')""")
predict("""class ZuKlein(Exception):
    pass

def pruefe(x):
    if x < 5:
        raise ZuKlein(x)
    return x

for x in [7, 2, 9]:
    try:
        print(pruefe(x))
    except ZuKlein as e:
        print('zu klein:', e)""")
predict("""x = 5
assert x > 3, 'x zu klein'
print('A')
assert x > 7, 'x zu klein'
print('B')""", error=AssertionError)

# ---------------------------------------------------------------- 9
sec('Gemischte Übungen')
t('''Ein kleiner Taschenrechner: Jede Aufgabe in `aufgaben` hat die Form `Zahl Operator Zahl` (mit Leerzeichen).
Berechne sie mit `+`, `-`, `*`, `/`. Bei einem unbekannten Operator löse `ValueError('unbekannter Operator')` aus.
Gib das Ergebnis oder bei einem `ValueError` `Fehler: ...` mit der Meldung aus, bei einer Division durch 0 `Fehler: Division durch 0`.
(Bei falscher Form entsteht beim Entpacken ein `ValueError`.)''',
  "aufgaben = ['3 + 4', '10 / 4', '7 / 0', '2 ^ 3', 'drei * 2', '6 * 7']",
  """def rechne(text):
    a, op, b = text.split()
    a = float(a)
    b = float(b)
    if op == '+':
        return a + b
    if op == '-':
        return a - b
    if op == '*':
        return a * b
    if op == '/':
        return a / b
    raise ValueError('unbekannter Operator')

for aufgabe in aufgaben:
    try:
        print(aufgabe, '=', rechne(aufgabe))
    except ZeroDivisionError:
        print(aufgabe, 'Fehler: Division durch 0')
    except ValueError as e:
        print(aufgabe, 'Fehler:', e)""")
t('''Die Noten in `eingaben` kommen aus einem Formular. Wandle jede in eine Zahl um. Gültig sind nur ganze Zahlen von 1 bis 6.
Sammle die gültigen Noten und gib sie aus, dann den Durchschnitt mit zwei Nachkommastellen und die Anzahl der ungültigen Eingaben.''',
  "eingaben = ['2', '1', 'sehr gut', '7', '3', '', '2', '0', '5']",
  """noten = []
ungueltig = 0
for e in eingaben:
    try:
        n = int(e)
    except ValueError:
        ungueltig += 1
        continue
    if 1 <= n <= 6:
        noten.append(n)
    else:
        ungueltig += 1
print(noten)
print(f'{sum(noten) / len(noten):.2f}')
print(ungueltig)""")
t('''Im Dictionary `bestand` steht, wie viele Teile von jedem Artikel da sind. Die Liste `abfragen` enthält Artikelnamen.
Gib für jede Abfrage den Bestand aus. Für unbekannte Artikel gib `unbekannt` aus. Verwende `try`/`except KeyError`
(nicht `get()` oder `in`) und zähle die unbekannten Abfragen.''',
  "bestand = {'Schraube': 120, 'Mutter': 80, 'Dübel': 0}\nabfragen = ['Mutter', 'Nagel', 'Dübel', 'Haken', 'Schraube']",
  """unbekannt = 0
for a in abfragen:
    try:
        print(a, bestand[a])
    except KeyError:
        print(a, 'unbekannt')
        unbekannt += 1
print(unbekannt)""")
t('''Die Messreihe `messungen` enthält Paare aus Strecke (in m) und Zeit (in s) als Text. Berechne für jedes Paar die Geschwindigkeit
in m/s mit einer Nachkommastelle. Fehlerhafte Paare (keine Zahl oder Zeit 0) werden mit `ungültig` gemeldet.
Gib am Ende die größte gültige Geschwindigkeit aus.''',
  "messungen = [('100', '12.5'), ('100', '0'), ('200', '25'), ('hundert', '13'), ('50', '5.5')]",
  """schnellste = 0
for strecke, zeit in messungen:
    try:
        v = float(strecke) / float(zeit)
    except (ValueError, ZeroDivisionError):
        print('ungültig')
    else:
        print(f'{v:.1f}')
        if v > schnellste:
            schnellste = v
print(f'{schnellste:.1f}')""")
t('''Schreibe eine Funktion `datum(text)`, die einen Text wie `'24.12.2026'` in ein Tupel `(24, 12, 2026)` umwandelt.
Sie soll `ValueError('ungültiger Monat')` auslösen, wenn der Monat nicht von 1 bis 12 ist, und `ValueError('ungültiger Tag')`,
wenn der Tag nicht von 1 bis 31 ist. Gib für jeden Text in `tests` das Tupel oder `text: Meldung` aus.''',
  "tests = ['24.12.2026', '31.13.2026', '0.5.2026', '1.1', 'x.2.2026', '15.8.2026']",
  """def datum(text):
    t, m, j = text.split('.')
    t = int(t)
    m = int(m)
    j = int(j)
    if m < 1 or m > 12:
        raise ValueError('ungültiger Monat')
    if t < 1 or t > 31:
        raise ValueError('ungültiger Tag')
    return (t, m, j)

for text in tests:
    try:
        print(datum(text))
    except ValueError as e:
        print(f'{text}: {e}')""")
t('''Ein Roboter läuft auf einem 5×5-Feld (Zeilen und Spalten 0 bis 4) und startet bei `(2, 2)`. Die Befehle in `befehle` sind
`'N'`, `'S'`, `'O'`, `'W'` (Norden ist Zeile − 1). Lege einen Fehlertyp `WandFehler` an. Schreibe eine Funktion `schritt(pos, befehl)`,
die die neue Position zurückgibt, bei einem unbekannten Befehl `ValueError` auslöst und beim Verlassen des Feldes `WandFehler`.
Bei einem Fehler bleibt der Roboter stehen. Gib nach jedem Befehl die Position oder die Art des Fehlers (`Wand` / `unbekannt`) aus.''',
  "befehle = ['N', 'N', 'N', 'O', 'X', 'O', 'O', 'S']",
  """class WandFehler(Exception):
    pass

def schritt(pos, befehl):
    z, s = pos
    if befehl == 'N':
        z -= 1
    elif befehl == 'S':
        z += 1
    elif befehl == 'O':
        s += 1
    elif befehl == 'W':
        s -= 1
    else:
        raise ValueError(befehl)
    if z < 0 or z > 4 or s < 0 or s > 4:
        raise WandFehler()
    return (z, s)

pos = (2, 2)
for b in befehle:
    try:
        pos = schritt(pos, b)
        print(pos)
    except WandFehler:
        print('Wand')
    except ValueError:
        print('unbekannt')""")
t('''Für jede Zeile in `zeilen` (Form `Produkt;Menge;Preis`) soll der Gesamtpreis `Menge * Preis` berechnet werden.
Gib für jede Zeile den Gesamtpreis mit zwei Nachkommastellen oder `Zeile 3 fehlerhaft` (Zeilennummer ab 1) aus.
Am Ende gib die Summe aller gültigen Gesamtpreise aus.''',
  "zeilen = ['Heft;3;1.20', 'Stift;2;0.80', 'Lineal;eins;1.50', 'Mappe;2', 'Radierer;4;0.35']",
  """summe = 0
for nr, z in enumerate(zeilen, 1):
    try:
        produkt, menge, preis = z.split(';')
        gesamt = int(menge) * float(preis)
    except ValueError:
        print(f'Zeile {nr} fehlerhaft')
    else:
        print(f'{gesamt:.2f}')
        summe += gesamt
print(f'{summe:.2f}')""")
t('''Schreibe eine Funktion `fehlerart(code)`, die einen Ausdruck mit `eval()` ausführt und `'ok'` zurückgibt, wenn kein Fehler auftritt,
sonst den Namen des Fehlertyps. Ordne damit jedem Ausdruck in `ausdruecke` seine Fehlerart zu und gib die Ausdrücke gruppiert nach
Fehlerart aus: erst die Fehlerart, dann eine Liste der Ausdrücke (Fehlerarten alphabetisch).''',
  "ausdruecke = ['1 + 1', '1 / 0', '\"a\" + 1', '[][0]', 'int(\"a\")', '2 % 0', 'len(3)', 'abs(-1)', '\"abc\".find(1)']",
  """def fehlerart(code):
    try:
        eval(code)
        return 'ok'
    except Exception as e:
        return type(e).__name__

gruppen = {}
for a in ausdruecke:
    art = fehlerart(a)
    if art not in gruppen:
        gruppen[art] = []
    gruppen[art].append(a)
for art in sorted(gruppen):
    print(art, gruppen[art])""")
predict("""ergebnis = []
for x in ['4', '0', 'a', '2']:
    try:
        ergebnis.append(8 // int(x))
    except ZeroDivisionError:
        ergebnis.append('null')
    except ValueError:
        continue
    finally:
        ergebnis.append('|')
print(ergebnis)""")
predict("""def f(x):
    try:
        return 10 / x
    except ZeroDivisionError:
        return 'unendlich'
    finally:
        print('f fertig')

print(f(4))
print(f(0))""")

generate('exceptions', 'Fehler und Ausnahmen (Exceptions)', INTRO)
