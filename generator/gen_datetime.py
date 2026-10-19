# Erzeugt ../content/datetime.ipynb (siehe nbgen.py).
#
# date.today() und datetime.now() ändern sich ständig. Aufgaben damit sind 'free' (ohne erwartete Ausgabe).
# Alle anderen Aufgaben verwenden ein festes Datum, z. B. heute = date(2025, 3, 14).
# Monats- und Wochentagsnamen von strftime() sind englisch (C-Locale, auch in JupyterLite);
# deutsche Namen kommen deshalb immer aus eigenen Listen.
from nbgen import sec, expl, task, predict, generate


def t(text, given='', body='', kind='normal'):
    """Aufgabe, deren Lösung aus dem vorgegebenen Code plus body besteht."""
    task(text, given=given, solution=(given + '\n' + body) if given else body, kind=kind)


WT = "wochentage = ['Montag', 'Dienstag', 'Mittwoch', 'Donnerstag', 'Freitag', 'Samstag', 'Sonntag']"
MON = ("monate = ['Januar', 'Februar', 'März', 'April', 'Mai', 'Juni',\n"
       "          'Juli', 'August', 'September', 'Oktober', 'November', 'Dezember']")

INTRO = '''Mit dem Modul `datetime` kann man in Python mit **Datum und Uhrzeit** arbeiten: Daten erstellen, vergleichen,
Abstände ausrechnen, Termine verschieben, Daten schön ausgeben und aus Texten einlesen.

Jeder Abschnitt beginnt mit kurzen Erklärungen und Beispielen. Führe die Beispiele aus und probiere sie ruhig ein wenig aus.
Danach folgen viele kleine Übungen. Wenn etwas vorgegeben ist, steht es schon in der Codezelle.

Das heutige Datum ändert sich jeden Tag. Damit die erwarteten Ausgaben stimmen, ist in vielen Aufgaben ein festes Datum
als „heute“ vorgegeben, zum Beispiel `heute = date(2025, 3, 14)`. Nur bei Aufgaben mit `date.today()` oder
`datetime.now()` steht keine erwartete Ausgabe.'''

# ---------------------------------------------------------------- 1
sec('Datumsobjekte mit date')
expl('''#### Das Modul `datetime`

Das Modul `datetime` enthält mehrere **Klassen** (Datentypen). Die wichtigsten sind:

| Klasse | speichert | Beispiel |
|---|---|---|
| `date` | ein Datum | 14. März 2025 |
| `time` | eine Uhrzeit | 14:30 Uhr |
| `datetime` | Datum und Uhrzeit | 14. März 2025, 14:30 Uhr |
| `timedelta` | eine Zeitspanne | 3 Tage und 2 Stunden |

Man importiert sie meist einzeln: `from datetime import date, timedelta`.
Achtung: Die Klasse `datetime` heißt genauso wie das Modul.''',
     """from datetime import date, time, datetime, timedelta

print(date(2025, 3, 14))
print(time(14, 30))
print(datetime(2025, 3, 14, 14, 30))
print(timedelta(days=3, hours=2))""")
expl('''#### Ein Datum erstellen

`date(jahr, monat, tag)` erstellt ein Datum. Die Reihenfolge ist immer **Jahr, Monat, Tag**.

- Mit `d.year`, `d.month` und `d.day` bekommt man Jahr, Monat und Tag als ganze Zahlen.
- `print(d)` gibt das Datum in der Form `JJJJ-MM-TT` aus. Das ist das internationale **ISO-Format**.
  `str(d)` liefert denselben Text.
- Steht ein Datum in einer Liste, zeigt `print(liste)` es als `datetime.date(2025, 3, 14)` an.''',
     """from datetime import date

d = date(2025, 3, 14)
print(d)
print(d.year, d.month, d.day)
print(type(d))
print('Datum: ' + str(d))
print([d, date(2025, 12, 24)])""")
expl('''#### Das heutige Datum: `date.today()`

`date.today()` liefert das Datum von heute. Das Ergebnis ist also jeden Tag anders.''',
     """from datetime import date

heute = date.today()
print(heute)
print(heute.year)""")
expl('''#### Ungültige Daten

Ein Datum, das es nicht gibt, führt zu einem `ValueError`, zum Beispiel der 30. Februar oder der Monat 13.''',
     """from datetime import date

try:
    d = date(2025, 2, 30)
except ValueError as fehler:
    print('Fehler:', fehler)""")

t('Erstelle ein Datum mit deinem Geburtstag und gib es aus.',
  'from datetime import date',
  """geburtstag = date(2009, 5, 17)
print(geburtstag)""", kind='free')
t('Erstelle das Datum 24. Dezember 2025 und gib es aus.',
  'from datetime import date',
  """d = date(2025, 12, 24)
print(d)""")
t('Gib Jahr, Monat und Tag von `d` jeweils in einer eigenen Zeile aus.',
  'from datetime import date\nd = date(2025, 10, 3)',
  """print(d.year)
print(d.month)
print(d.day)""")
t('Gib `d` mit einem f-String in der deutschen Form `Tag.Monat.Jahr` aus wie unten.',
  'from datetime import date\nd = date(2025, 7, 4)',
  """print(f'{d.day}.{d.month}.{d.year}')""")
t('Gib `d` wie in der vorigen Aufgabe aus, aber Tag und Monat immer zweistellig. Verwende die Formatangabe `:02d`.',
  'from datetime import date\nd = date(2025, 7, 4)',
  """print(f'{d.day:02d}.{d.month:02d}.{d.year}')""")
t('Gib das heutige Datum und darunter das aktuelle Jahr aus.',
  'from datetime import date',
  """heute = date.today()
print(heute)
print(heute.year)""", kind='free')
t('Gib jedes Datum der Liste in einer eigenen Zeile aus.',
  'from datetime import date\nferien = [date(2025, 4, 14), date(2025, 7, 14), date(2025, 10, 13)]',
  """for d in ferien:
    print(d)""")
t('Gib für jedes Datum der Liste `Sommer` aus, wenn es im Juni, Juli oder August liegt, sonst `kein Sommer`.',
  'from datetime import date\ndaten = [date(2025, 1, 5), date(2025, 6, 21), date(2025, 8, 31), date(2025, 9, 1)]',
  """for d in daten:
    if d.month in [6, 7, 8]:
        print(d, 'Sommer')
    else:
        print(d, 'kein Sommer')""")
t('Zerlege `text` mit `split()` in Jahr, Monat und Tag, wandle sie mit `int()` um und erstelle daraus ein Datum. Gib es aus.',
  "from datetime import date\ntext = '2025-10-03'",
  """teile = text.split('-')
d = date(int(teile[0]), int(teile[1]), int(teile[2]))
print(d)
print(d.day)""")
t("Der Text `text` steht im deutschen Format. Erstelle daraus ein Datum und gib es aus.",
  "from datetime import date\ntext = '31.12.2025'",
  """teile = text.split('.')
d = date(int(teile[2]), int(teile[1]), int(teile[0]))
print(d)""")
t('Prüfe mit `try` und `except ValueError`, welche der Angaben (Jahr, Monat, Tag) ein gültiges Datum ergeben. Gib `gültig` oder `ungültig` aus.',
  'from datetime import date\nangaben = [(2024, 2, 29), (2025, 2, 29), (2025, 4, 31), (2025, 12, 31), (2025, 0, 1)]',
  """for j, m, tag in angaben:
    try:
        date(j, m, tag)
        print(j, m, tag, 'gültig')
    except ValueError:
        print(j, m, tag, 'ungültig')""")
predict("""from datetime import date
d = date(2025, 1, 9)
print(d)
print(d.month + d.day)
print(str(d) + '!')
print([d])""")
predict("""from datetime import date
d = date(2025, 13, 1)
print(d)""", error=ValueError)

# ---------------------------------------------------------------- 2
sec('Wochentage und Kalenderwochen')
expl('''#### `weekday()` und `isoweekday()`

- `d.weekday()` gibt den Wochentag als Zahl zurück: **Montag = 0**, Dienstag = 1, ..., Sonntag = 6.
- `d.isoweekday()` zählt dagegen ab **Montag = 1** bis Sonntag = 7.

Für deutsche Namen nimmt man eine Liste und verwendet `weekday()` als Index.''',
     """from datetime import date

wochentage = ['Montag', 'Dienstag', 'Mittwoch', 'Donnerstag', 'Freitag', 'Samstag', 'Sonntag']
d = date(2025, 3, 14)
print(d.weekday())
print(d.isoweekday())
print(wochentage[d.weekday()])""")
expl('''#### Kalenderwochen mit `isocalendar()`

`d.isocalendar()` liefert drei Zahlen: das Jahr, die **Kalenderwoche** und den Wochentag (1 bis 7).
Man bekommt sie einzeln mit `.year`, `.week` und `.weekday` oder mit dem Index `[0]`, `[1]`, `[2]`.

Nach der Regel (ISO 8601), die auch in Deutschland gilt, beginnt eine Woche am Montag.
Die Kalenderwoche 1 ist die Woche, in der der erste Donnerstag des Jahres liegt. Deshalb kann der 1. Januar
noch zur letzten Woche des **Vorjahres** gehören.''',
     """from datetime import date

d = date(2025, 3, 14)
print(d.isocalendar().week)
print(d.isocalendar()[1])
k = date(2027, 1, 1).isocalendar()
print(k.year, k.week, k.weekday)""")

t('Gib `weekday()` und `isoweekday()` von Heiligabend 2025 aus.',
  'from datetime import date\nd = date(2025, 12, 24)',
  """print(d.weekday())
print(d.isoweekday())""")
t('Gib aus, auf welchen Wochentag der 1. Januar 2000 fiel (deutscher Name).',
  'from datetime import date\n' + WT,
  """d = date(2000, 1, 1)
print(wochentage[d.weekday()])""")
t('Gib für jedes Datum den deutschen Wochentag aus wie unten.',
  'from datetime import date\n' + WT + '\ndaten = [date(2025, 5, 1), date(2025, 10, 3), date(2025, 12, 25)]',
  """for d in daten:
    print(d, wochentage[d.weekday()])""")
t('Gib für jedes Datum `Wochenende` oder `Werktag` aus.',
  'from datetime import date\ndaten = [date(2025, 3, 14), date(2025, 3, 15), date(2025, 3, 16), date(2025, 3, 17)]',
  """for d in daten:
    if d.weekday() >= 5:
        print(d, 'Wochenende')
    else:
        print(d, 'Werktag')""")
t('Gib die Kalenderwoche von `d` aus.',
  'from datetime import date\nd = date(2025, 3, 14)',
  """print(d.isocalendar().week)""")
t('Gib für die Jahre 2025 bis 2030 aus, auf welchen Wochentag der 1. Januar fällt.',
  'from datetime import date\n' + WT,
  """for jahr in range(2025, 2031):
    print(jahr, wochentage[date(jahr, 1, 1).weekday()])""")
t('Zähle, in wie vielen Jahren von 2000 bis 2030 (einschließlich) Heiligabend auf ein Wochenende fällt.',
  'from datetime import date',
  """anzahl = 0
for jahr in range(2000, 2031):
    if date(jahr, 12, 24).weekday() >= 5:
        anzahl += 1
print(anzahl)""")
t('Gib alle Monate des Jahres 2026 aus, in denen der 13. ein Freitag ist.',
  'from datetime import date',
  """for monat in range(1, 13):
    if date(2026, monat, 13).weekday() == 4:
        print(monat)""")
t('Gib für jedes Datum Jahr und Kalenderwoche nach ISO aus. Beachte die Daten am Jahreswechsel.',
  'from datetime import date\ndaten = [date(2024, 12, 30), date(2025, 1, 1), date(2025, 12, 29), date(2027, 1, 3)]',
  """for d in daten:
    k = d.isocalendar()
    print(d, k.year, k.week)""")
t('Gib den deutschen Wochentag von heute aus.',
  'from datetime import date\n' + WT,
  """print(wochentage[date.today().weekday()])""", kind='free')
predict("""from datetime import date
d = date(2025, 3, 16)
print(d.weekday())
print(d.isoweekday())
print(d.isocalendar()[2])
print(date(2025, 3, 17).weekday())""")

# ---------------------------------------------------------------- 3
sec('Vergleichen, sortieren und replace()')
expl('''#### Daten vergleichen

Daten kann man mit `<`, `>`, `<=`, `>=`, `==` und `!=` vergleichen. **Früher** bedeutet **kleiner**.
Deshalb funktionieren auch `min()`, `max()`, `sorted()` und `sort()`.

Mit `start <= d <= ende` prüft man, ob ein Datum in einem Zeitraum liegt.''',
     """from datetime import date

a = date(2025, 3, 14)
b = date(2025, 12, 24)
print(a < b)
print(a == date(2025, 3, 14))
daten = [b, a, date(2024, 7, 1)]
print(min(daten))
for d in sorted(daten):
    print(d)""")
expl('''#### `replace()`

`d.replace(year=..., month=..., day=...)` gibt ein **neues** Datum zurück, bei dem die angegebenen Teile geändert sind.
Das alte Datum bleibt unverändert. Man muss nur angeben, was sich ändern soll.''',
     """from datetime import date

d = date(2025, 3, 14)
print(d.replace(day=1))
print(d.replace(year=2030))
print(d.replace(month=12, day=31))
print(d)""")

t('Gib das frühere der beiden Daten aus. Verwende `if` und `<`.',
  'from datetime import date\na = date(2025, 11, 3)\nb = date(2025, 9, 28)',
  """if a < b:
    print(a)
else:
    print(b)""")
t('Prüfe für jeden Termin, ob er in den Ferien liegt (`start` und `ende` gehören dazu). Gib `Ferien` oder `Schule` aus.',
  '''from datetime import date
start = date(2025, 7, 14)
ende = date(2025, 8, 26)
termine = [date(2025, 7, 13), date(2025, 7, 14), date(2025, 8, 1), date(2025, 8, 27)]''',
  """for d in termine:
    if start <= d <= ende:
        print(d, 'Ferien')
    else:
        print(d, 'Schule')""")
t('Gib die Termine sortiert aus, den frühesten zuerst.',
  'from datetime import date\ntermine = [date(2025, 6, 2), date(2025, 1, 15), date(2025, 11, 30), date(2025, 3, 8)]',
  """for d in sorted(termine):
    print(d)""")
t('Gib den frühesten und den spätesten Termin aus.',
  'from datetime import date\ntermine = [date(2025, 6, 2), date(2025, 1, 15), date(2025, 11, 30), date(2025, 3, 8)]',
  """print(min(termine))
print(max(termine))""")
t('Zähle, wie viele Termine im Jahr 2024 liegen.',
  'from datetime import date\ntermine = [date(2023, 12, 31), date(2024, 1, 1), date(2024, 6, 15), date(2025, 1, 1), date(2024, 12, 31)]',
  """anzahl = 0
for d in termine:
    if d.year == 2024:
        anzahl += 1
print(anzahl)""")
t('Gib aus, wer von den beiden zuerst geboren ist.',
  'from datetime import date\ngeburtstage = {\'Anna\': date(2008, 9, 12), \'Ben\': date(2008, 3, 30)}',
  """if geburtstage['Anna'] < geburtstage['Ben']:
    print('Anna')
else:
    print('Ben')""")
t('Gib den Namen der jüngsten Person aus. Gehe dazu das Dictionary mit einer Schleife durch.',
  "from datetime import date\ngeburtstage = {'Anna': date(2008, 9, 12), 'Ben': date(2009, 1, 3), 'Cem': date(2008, 12, 24)}",
  """juengste = ''
spaetestes = date(1900, 1, 1)
for name in geburtstage:
    if geburtstage[name] > spaetestes:
        spaetestes = geburtstage[name]
        juengste = name
print(juengste)""")
t('Gib mit `replace()` den Geburtstag im Jahr 2025 aus.',
  'from datetime import date\ngeburtstag = date(2008, 9, 12)',
  """print(geburtstag.replace(year=2025))""")
t('Gib mit `replace()` den ersten Tag des Monats von `d` aus und dahinter seinen Wochentag als Zahl.',
  'from datetime import date\nd = date(2025, 3, 14)',
  """erster = d.replace(day=1)
print(erster, erster.weekday())""")
t('Prüfe, ob die Person in diesem Jahr schon Geburtstag hatte. Ersetze dazu das Jahr des Geburtstags durch das Jahr von `heute`.',
  'from datetime import date\nheute = date(2025, 3, 14)\ngeburtstag = date(2008, 9, 12)',
  """if geburtstag.replace(year=heute.year) <= heute:
    print('schon Geburtstag gehabt')
else:
    print('noch nicht')""")
t('Sortiere die Liste `daten` mit `sort()` absteigend (das späteste zuerst) und gib sie aus.',
  'from datetime import date\ndaten = [date(2025, 6, 2), date(2025, 1, 15), date(2025, 11, 30)]',
  """daten.sort(reverse=True)
for d in daten:
    print(d)""")
predict("""from datetime import date
a = date(2025, 1, 31)
b = a.replace(month=3)
print(b)
print(a)
print(a > b)
print(max(a, b).month)""")
predict("""from datetime import date
d = date(2025, 1, 31)
print(d.replace(month=2))""", error=ValueError)

# ---------------------------------------------------------------- 4
sec('Zeitspannen mit timedelta')
expl('''#### Abstand zwischen zwei Daten

Zieht man zwei Daten voneinander ab, erhält man eine **Zeitspanne** vom Typ `timedelta`.
Mit `.days` bekommt man die Anzahl der Tage als ganze Zahl.
Ist das zweite Datum später, wird die Zeitspanne negativ.''',
     """from datetime import date

a = date(2025, 3, 14)
b = date(2025, 12, 24)
abstand = b - a
print(abstand)
print(abstand.days)
print((a - b).days)
print(type(abstand))""")
expl('''#### Rechnen mit `timedelta`

`timedelta(days=..., weeks=..., hours=..., minutes=..., seconds=...)` erstellt eine Zeitspanne.

- `datum + timedelta(days=10)` ist das Datum 10 Tage später, `datum - timedelta(weeks=2)` zwei Wochen früher.
- Zeitspannen kann man addieren, mit einer Zahl multiplizieren und vergleichen.
- `td.total_seconds()` gibt die ganze Zeitspanne in Sekunden an (als Kommazahl).
- `timedelta()` ohne Argumente ist eine Zeitspanne der Länge 0. Damit kann man Zeitspannen aufsummieren.

Monate und Jahre gibt es bei `timedelta` **nicht**, weil sie unterschiedlich lang sind (siehe Abschnitt 8).''',
     """from datetime import date, timedelta

d = date(2025, 3, 14)
print(d + timedelta(days=10))
print(d - timedelta(weeks=2))
pause = timedelta(minutes=15)
print(pause * 4)
print(timedelta(hours=1) > pause)
print(timedelta(days=1).total_seconds())""")

t('Gib aus, wie viele Tage es von `heute` bis Heiligabend sind.',
  'from datetime import date\nheute = date(2025, 3, 14)\nheiligabend = date(2025, 12, 24)',
  """print((heiligabend - heute).days)""")
t('Gib aus, wie viele Tage zwischen den beiden Daten liegen.',
  'from datetime import date\na = date(2024, 1, 1)\nb = date(2025, 1, 1)',
  """print((b - a).days)""")
t('Gib das Datum aus, das 100 Tage nach `heute` liegt.',
  'from datetime import date, timedelta\nheute = date(2025, 3, 14)',
  """print(heute + timedelta(days=100))""")
t('Gib das Datum aus, das zwei Wochen vor `heute` lag.',
  'from datetime import date, timedelta\nheute = date(2025, 3, 14)',
  """print(heute - timedelta(weeks=2))""")
t('Gib aus, wie viele Tage die Person am Tag `heute` alt ist.',
  'from datetime import date\nheute = date(2025, 3, 14)\ngeburtstag = date(2008, 9, 12)',
  """print((heute - geburtstag).days)""")
t('Gib aus, wie viele Tage seit deiner Geburt vergangen sind. Verwende `date.today()`.',
  'from datetime import date',
  """geburtstag = date(2009, 5, 17)
print((date.today() - geburtstag).days)""", kind='free')
t('Gib die Daten der nächsten fünf Montage aus. Beginne bei `montag` und addiere jeweils eine Woche.',
  'from datetime import date, timedelta\nmontag = date(2025, 3, 17)',
  """d = montag
for i in range(5):
    print(d)
    d += timedelta(weeks=1)""")
t('Ein Abo beginnt am Tag `start` und läuft 30 Tage. Gib den letzten Tag des Abos aus (der Starttag zählt mit).',
  'from datetime import date, timedelta\nstart = date(2025, 2, 10)',
  """print(start + timedelta(days=29))""")
t('Gib für jeden Termin aus, wie viele Tage seit dem vorherigen Termin vergangen sind.',
  'from datetime import date\ntermine = [date(2025, 1, 6), date(2025, 2, 3), date(2025, 3, 17), date(2025, 3, 24)]',
  """for i in range(1, len(termine)):
    print(termine[i], (termine[i] - termine[i - 1]).days)""")
t('Ein Training dauert 1 Stunde und 30 Minuten. Gib aus, wie lange drei Trainings zusammen dauern, und dann, wie viele Minuten das sind.',
  'from datetime import timedelta\ntraining = timedelta(hours=1, minutes=30)',
  """gesamt = training * 3
print(gesamt)
print(gesamt.total_seconds() / 60)""")
t('Gib mit `total_seconds()` aus, wie viele Stunden eine Woche hat.',
  'from datetime import timedelta',
  """print(timedelta(weeks=1).total_seconds() / 3600)""")
t('Gib aus, wie viele ganze Wochen und restliche Tage es von `heute` bis zum Ferienbeginn sind. Verwende `//` und den Modulo-Operator `%`.',
  'from datetime import date\nheute = date(2025, 3, 14)\nferien = date(2025, 7, 14)',
  """tage = (ferien - heute).days
print(f'{tage // 7} Wochen und {tage % 7} Tage')""")
t('Gib für jede Ausleihe `zu spät` aus, wenn das Buch mehr als 28 Tage ausgeliehen war, sonst `ok`. Vergleiche mit `timedelta(days=28)`.',
  'from datetime import date, timedelta\nausleihen = [(date(2025, 1, 2), date(2025, 1, 20)), (date(2025, 2, 1), date(2025, 3, 5)), (date(2025, 3, 1), date(2025, 3, 29))]',
  """for von, bis in ausleihen:
    if bis - von > timedelta(days=28):
        print(von, bis, 'zu spät')
    else:
        print(von, bis, 'ok')""")
t('Gib alle Daten von `start` bis einschließlich `ende` aus, jedes in einer eigenen Zeile. Verwende eine `while`-Schleife.',
  'from datetime import date, timedelta\nstart = date(2025, 2, 26)\nende = date(2025, 3, 2)',
  """d = start
while d <= ende:
    print(d)
    d += timedelta(days=1)""")
predict("""from datetime import date, timedelta
print(date(2025, 3, 1) - date(2025, 2, 1))
print((date(2024, 3, 1) - date(2024, 2, 1)).days)
print(date(2025, 12, 31) + timedelta(days=1))
print(timedelta(hours=25))
print(timedelta(minutes=90) * 2)""")
predict("""from datetime import date, timedelta
print(timedelta(days=-1))
print(timedelta(hours=-1))
print((date(2025, 1, 1) - date(2025, 1, 10)).days)""")

# ---------------------------------------------------------------- 5
sec('Uhrzeiten mit time und datetime')
expl('''#### Uhrzeiten mit `time`

`time(stunde, minute, sekunde)` speichert eine Uhrzeit ohne Datum. Minute und Sekunde kann man weglassen, dann sind sie 0.
Mit `.hour`, `.minute` und `.second` bekommt man die Teile. Uhrzeiten kann man vergleichen.''',
     """from datetime import time

beginn = time(8, 15)
print(beginn)
print(beginn.hour, beginn.minute)
print(time(13, 30) > beginn)""")
expl('''#### Datum und Uhrzeit mit `datetime`

`datetime(jahr, monat, tag, stunde, minute, sekunde)` speichert einen Zeitpunkt.
Er hat alle Attribute von `date` und `time`: `.year`, ..., `.hour`, `.minute`, `.second`.

- `dt.date()` und `dt.time()` geben den Datums- bzw. Uhrzeitteil zurück.
- `datetime.combine(d, t)` setzt ein `date` und eine `time` zusammen.
- `datetime.now()` liefert den aktuellen Zeitpunkt (mit Mikrosekunden).''',
     """from datetime import date, time, datetime

dt = datetime(2025, 3, 14, 14, 30)
print(dt)
print(dt.hour, dt.minute)
print(dt.date())
print(dt.time())
print(datetime.combine(date(2025, 5, 1), time(9, 0)))
print(datetime.now())""")
expl('''#### Rechnen mit Zeitpunkten

Mit `datetime` funktioniert das Rechnen wie bei `date`, nur genauer:

- `dt + timedelta(minutes=90)` ist der Zeitpunkt 90 Minuten später, auch über Mitternacht hinweg.
- `dt2 - dt1` ist eine Zeitspanne. `total_seconds() / 60` gibt sie in Minuten an.

Mit `time` allein kann man **nicht** rechnen. Dafür nimmt man einen `datetime` mit irgendeinem Datum.''',
     """from datetime import datetime, timedelta

abfahrt = datetime(2025, 3, 14, 22, 50)
ankunft = abfahrt + timedelta(hours=1, minutes=25)
print(ankunft)
dauer = ankunft - abfahrt
print(dauer)
print(dauer.total_seconds() / 60)""")

t('Erstelle die Uhrzeit 14:30 und gib sie aus. Gib danach Stunde und Minute aus.',
  'from datetime import time',
  """t = time(14, 30)
print(t)
print(t.hour, t.minute)""")
t('Die Klausur beginnt zum Zeitpunkt `beginn` und dauert 90 Minuten. Gib das Ende aus.',
  'from datetime import datetime, timedelta\nbeginn = datetime(2025, 5, 12, 8, 0)',
  """print(beginn + timedelta(minutes=90))""")
t('Gib aus, wie viele Minuten zwischen `start` und `ziel` liegen, als ganze Zahl.',
  'from datetime import datetime\nstart = datetime(2025, 3, 14, 9, 12)\nziel = datetime(2025, 3, 14, 11, 47)',
  """print(int((ziel - start).total_seconds() / 60))""")
t('Der Nachtzug fährt um `abfahrt` los und kommt um `ankunft` an. Gib die Fahrzeit aus.',
  'from datetime import datetime\nabfahrt = datetime(2025, 3, 14, 21, 40)\nankunft = datetime(2025, 3, 15, 7, 5)',
  """print(ankunft - abfahrt)""")
t('Der Film beginnt um 20:15 Uhr und dauert 2 Stunden und 28 Minuten. Gib die Uhrzeit aus, zu der er endet.',
  'from datetime import datetime, timedelta\nbeginn = datetime(2025, 3, 14, 20, 15)',
  """ende = beginn + timedelta(hours=2, minutes=28)
print(ende.time())""")
t('''Eine Schulstunde dauert 45 Minuten, danach sind 5 Minuten Pause. Die erste Stunde beginnt um 8:00 Uhr.
Gib die Anfangszeiten der ersten sechs Stunden aus.''',
  'from datetime import datetime, timedelta\nbeginn = datetime(2025, 3, 14, 8, 0)',
  """for stunde in range(1, 7):
    print(stunde, beginn.time())
    beginn += timedelta(minutes=50)""")
t('Setze mit `datetime.combine()` das Datum und die Uhrzeit zu einem Zeitpunkt zusammen und gib ihn aus.',
  'from datetime import date, time, datetime\ntag = date(2025, 6, 20)\nuhrzeit = time(19, 30)',
  """print(datetime.combine(tag, uhrzeit))""")
t('Gib für jede Uhrzeit `Unterricht` aus, wenn sie von 8:00 bis vor 13:00 liegt, sonst `frei`.',
  'from datetime import time\nzeiten = [time(7, 45), time(8, 0), time(12, 59), time(13, 0), time(15, 30)]',
  """for z in zeiten:
    if time(8, 0) <= z < time(13, 0):
        print(z, 'Unterricht')
    else:
        print(z, 'frei')""")
t('Gib mit `datetime.now()` `Guten Morgen`, `Guten Tag` oder `Guten Abend` aus: vor 11 Uhr, vor 18 Uhr, sonst.',
  'from datetime import datetime',
  """jetzt = datetime.now()
if jetzt.hour < 11:
    print('Guten Morgen')
elif jetzt.hour < 18:
    print('Guten Tag')
else:
    print('Guten Abend')""", kind='free')
t('Gib aus, wie viele Sekunden zwischen `a` und `b` liegen.',
  'from datetime import datetime\na = datetime(2025, 3, 14, 23, 59, 30)\nb = datetime(2025, 3, 15, 0, 1, 5)',
  """print((b - a).total_seconds())""")
t('Gib aus, wie viele Minuten von `jetzt` bis Mitternacht übrig sind. Mitternacht ist der Tag danach um 0:00 Uhr, also `time(0, 0)`.',
  'from datetime import time, datetime, timedelta\njetzt = datetime(2025, 3, 14, 21, 37)',
  """mitternacht = datetime.combine(jetzt.date() + timedelta(days=1), time(0, 0))
print(int((mitternacht - jetzt).total_seconds() / 60))""")
predict("""from datetime import datetime, timedelta
dt = datetime(2025, 12, 31, 23, 30)
print(dt + timedelta(hours=1))
print(datetime(2025, 1, 1, 12) - datetime(2025, 1, 1, 9, 15))
print(dt.date() == datetime(2025, 12, 31).date())""")
predict("""from datetime import time
print(time(10, 30) - time(9, 0))""", error=TypeError)

# ---------------------------------------------------------------- 6
sec('Formatieren mit strftime()')
expl('''#### `strftime()`

`d.strftime(format)` wandelt ein Datum oder einen Zeitpunkt in einen Text um. Im Format stehen Platzhalter mit `%`:

| Platzhalter | Bedeutung | Beispiel |
|---|---|---|
| `%d` | Tag, zweistellig | `04` |
| `%m` | Monat, zweistellig | `07` |
| `%Y` | Jahr, vierstellig | `2025` |
| `%y` | Jahr, zweistellig | `25` |
| `%H` | Stunde (00 bis 23) | `14` |
| `%I` | Stunde (01 bis 12) | `02` |
| `%p` | AM oder PM | `PM` |
| `%M` | Minute | `05` |
| `%S` | Sekunde | `09` |
| `%A` / `%a` | Wochentag englisch, lang / kurz | `Friday` / `Fri` |
| `%B` / `%b` | Monat englisch, lang / kurz | `July` / `Jul` |
| `%j` | Tag im Jahr (001 bis 366) | `185` |
| `%%` | ein Prozentzeichen | `%` |

Alle anderen Zeichen im Format werden unverändert übernommen. Die Namen sind englisch,
für deutsche Namen nimmt man eigene Listen.''',
     """from datetime import datetime

dt = datetime(2025, 7, 4, 14, 5, 9)
print(dt.strftime('%d.%m.%Y'))
print(dt.strftime('%H:%M Uhr'))
print(dt.strftime('%A, %d. %B %Y'))
print(dt.strftime('%j'))""")
expl('''#### Format im f-String und `isoformat()`

- Die Platzhalter kann man auch direkt in einem f-String angeben: `f'{d:%d.%m.%Y}'`.
- `d.isoformat()` liefert das ISO-Format als Text. Bei `datetime` steht ein `T` zwischen Datum und Uhrzeit.''',
     """from datetime import date, datetime

d = date(2025, 7, 4)
print(f'Heute ist der {d:%d.%m.%Y}.')
print(d.isoformat())
print(datetime(2025, 7, 4, 14, 5).isoformat())""")

FD = 'from datetime import datetime\ndt = datetime(2025, 12, 24, 18, 5)'
t('Gib `dt` mit `strftime()` in der Form unten aus.', FD, """print(dt.strftime('%d.%m.%Y'))""")
t('Gib `dt` mit zweistelligem Jahr aus wie unten.', FD, """print(dt.strftime('%d.%m.%y'))""")
t('Gib die Uhrzeit von `dt` aus wie unten.', FD, """print(dt.strftime('%H:%M Uhr'))""")
t('Gib `dt` in der Form unten aus.', FD, """print(dt.strftime('%d.%m.%Y um %H:%M Uhr'))""")
t('Gib `dt` mit englischem Wochentag und Monat aus wie unten.', FD, """print(dt.strftime('%A, %B %d, %Y'))""")
t('Gib die Uhrzeit von `dt` im englischen 12-Stunden-Format aus wie unten.', FD, """print(dt.strftime('%I:%M %p'))""")
t('Gib aus, der wievielte Tag des Jahres `dt` ist.', FD, """print(dt.strftime('%j'))""")
t('Gib `dt` mit einem f-String und Platzhaltern aus wie unten.', FD, """print(f'Bescherung: {dt:%d.%m.} um {dt:%H} Uhr')""")
t('Gib `dt` im ISO-Format aus.', FD, """print(dt.isoformat())""")
t('Gib `dt` mit deutschem Wochentag aus wie unten. Verwende die Liste und `strftime()`.',
  FD + '\n' + WT,
  """print(wochentage[dt.weekday()] + ', ' + dt.strftime('%d.%m.%Y'))""")
t('Gib `dt` mit deutschem Monatsnamen aus wie unten.',
  FD + '\n' + MON,
  """print(f'{dt.day}. {monate[dt.month - 1]} {dt.year}')""")
t('Erzeuge aus `dt` einen Dateinamen wie unten.', FD, """print(dt.strftime('backup_%Y%m%d_%H%M.txt'))""")
t('Gib die nächsten sieben Tage ab `start` als kleine Tabelle aus wie unten (Tag kurz auf Englisch und Datum).',
  'from datetime import date, timedelta\nstart = date(2025, 3, 14)',
  """for i in range(7):
    d = start + timedelta(days=i)
    print(d.strftime('%a %d.%m.'))""")
t('Gib das aktuelle Datum und die aktuelle Uhrzeit im deutschen Format aus.',
  'from datetime import datetime',
  """print(datetime.now().strftime('%d.%m.%Y %H:%M:%S'))""", kind='free')
predict("""from datetime import datetime
dt = datetime(2025, 1, 2, 3, 4, 5)
print(dt.strftime('%d/%m/%Y'))
print(dt.strftime('%Y%m%d'))
print(dt.strftime('%H-%M-%S'))
print(dt.strftime('%b %y'))
print(dt.strftime('100%%'))""")

# ---------------------------------------------------------------- 7
sec('Texte einlesen mit strptime() und fromisoformat()')
expl('''#### `datetime.strptime()`

`datetime.strptime(text, format)` ist das Gegenstück zu `strftime()`: Es liest einen Text mit dem angegebenen Format
und macht daraus einen `datetime`. Die Platzhalter sind dieselben wie bei `strftime()`.

- Fehlt die Uhrzeit im Text, ist sie 0:00 Uhr. Mit `.date()` bekommt man nur das Datum.
- Passt der Text nicht zum Format, entsteht ein `ValueError`.

Merkhilfe: str**f**time = **f**ormatieren, str**p**time = **p**arsen (einlesen).''',
     """from datetime import datetime

dt = datetime.strptime('24.12.2025 18:30', '%d.%m.%Y %H:%M')
print(dt)
d = datetime.strptime('24.12.2025', '%d.%m.%Y').date()
print(d)""")
expl('''#### `fromisoformat()`

Steht der Text im ISO-Format, geht es noch einfacher:

- `date.fromisoformat('2025-03-14')` liefert ein `date`,
- `datetime.fromisoformat('2025-03-14 14:30')` liefert einen `datetime`,
- `time.fromisoformat('14:30')` liefert eine `time`.''',
     """from datetime import date, time, datetime

print(date.fromisoformat('2025-03-14'))
print(datetime.fromisoformat('2025-03-14 14:30'))
print(time.fromisoformat('14:30'))""")
expl('''#### Fehler abfangen mit `try` und `except`

Ob ein Text ein gültiges Datum ist, prüft man am einfachsten mit `try` und `except ValueError`:
Der Code unter `try` wird ausgeführt. Tritt dabei ein `ValueError` auf, geht es im `except`-Teil weiter,
statt dass das Programm abbricht.''',
     """from datetime import datetime

for text in ['14.03.2025', '30.02.2025', '2025-03-14']:
    try:
        d = datetime.strptime(text, '%d.%m.%Y').date()
        print(text, 'ist', d)
    except ValueError:
        print(text, 'ist kein Datum im Format TT.MM.JJJJ')""")

t('Lies `text` mit `strptime()` ein und gib das Datum (ohne Uhrzeit) aus.',
  "from datetime import datetime\ntext = '03.10.2025'",
  """d = datetime.strptime(text, '%d.%m.%Y').date()
print(d)""")
t('Lies `text` mit `strptime()` ein und gib den Zeitpunkt aus.',
  "from datetime import datetime\ntext = '24.12.2025 18:30'",
  """print(datetime.strptime(text, '%d.%m.%Y %H:%M'))""")
t('Lies `text` mit `date.fromisoformat()` ein und gib den deutschen Wochentag aus.',
  "from datetime import date\n" + WT + "\ntext = '2025-10-03'",
  """d = date.fromisoformat(text)
print(wochentage[d.weekday()])""")
t('Lies beide Daten ein und gib aus, wie viele Tage dazwischen liegen.',
  "from datetime import datetime\na = '01.09.2025'\nb = '19.12.2025'",
  """da = datetime.strptime(a, '%d.%m.%Y')
db = datetime.strptime(b, '%d.%m.%Y')
print((db - da).days)""")
t('Lies alle Daten ein, sortiere sie und gib sie wieder im deutschen Format aus.',
  "from datetime import datetime\ntexte = ['17.05.2025', '03.01.2025', '28.11.2024', '09.05.2025']",
  """daten = []
for text in texte:
    daten.append(datetime.strptime(text, '%d.%m.%Y').date())
daten.sort()
for d in daten:
    print(d.strftime('%d.%m.%Y'))""")
t('Das Datum steht im amerikanischen Format `Monat/Tag/Jahr`. Gib es im deutschen Format aus.',
  "from datetime import datetime\ntext = '07/04/2025'",
  """d = datetime.strptime(text, '%m/%d/%Y')
print(d.strftime('%d.%m.%Y'))""")
t('Lies die Zeit in `text` mit `strptime()` ein. Der Monat steht als englischer Name. Gib das Datum im ISO-Format aus.',
  "from datetime import datetime\ntext = 'March 14, 2025'",
  """print(datetime.strptime(text, '%B %d, %Y').date())""")
t('''Die ersten 19 Zeichen jeder Logzeile sind ein Zeitpunkt im ISO-Format. Lies den ersten und den letzten Zeitpunkt
mit `datetime.fromisoformat()` ein und gib aus, wie lange das Programm gelaufen ist.''',
  """from datetime import datetime
log = ['2025-03-14 12:00:01 Start',
       '2025-03-14 12:00:05 Datei geladen',
       '2025-03-14 12:41:37 Ende']""",
  """start = datetime.fromisoformat(log[0][:19])
ende = datetime.fromisoformat(log[-1][:19])
print(ende - start)""")
t('Gib für jeden Text `gültig` oder `ungültig` aus, je nachdem, ob er ein Datum im Format `TT.MM.JJJJ` ist. Verwende `try` und `except ValueError`. `strptime()` akzeptiert bei `%d` und `%m` auch einstellige Zahlen.',
  "from datetime import datetime\ntexte = ['29.02.2024', '29.02.2025', '31.04.2025', '1.5.2025', '12-05-2025']",
  """for text in texte:
    try:
        datetime.strptime(text, '%d.%m.%Y')
        print(text, 'gültig')
    except ValueError:
        print(text, 'ungültig')""")
t('Lies die Uhrzeiten mit `time.fromisoformat()` ein und gib die früheste aus.',
  "from datetime import time\ntexte = ['13:45', '08:10', '09:30', '07:55']",
  """zeiten = []
for text in texte:
    zeiten.append(time.fromisoformat(text))
print(min(zeiten))""")
predict("""from datetime import datetime
print(datetime.strptime('2025-12-24', '%d.%m.%Y'))""", error=ValueError)
predict("""from datetime import date, datetime
print(datetime.strptime('5.3.2025', '%d.%m.%Y'))
print(date.fromisoformat('2025-03-05') == datetime.strptime('5.3.2025', '%d.%m.%Y').date())""")

# ---------------------------------------------------------------- 8
sec('Monate, Jahre und das Modul calendar')
expl('''#### Monate und Jahre addieren

Weil Monate und Jahre unterschiedlich lang sind, gibt es dafür kein `timedelta`. Man rechnet selbst:

- Ein Jahr später: `d.replace(year=d.year + 1)`. Beim 29. Februar gibt das einen `ValueError`.
- Einen Monat später: Monat um 1 erhöhen. Nach Dezember kommt Januar des nächsten Jahres.
  Gibt es den Tag im neuen Monat nicht (z. B. 31. April), muss man ihn anpassen.''',
     """from datetime import date

d = date(2025, 12, 15)
if d.month == 12:
    print(d.replace(year=d.year + 1, month=1))
else:
    print(d.replace(month=d.month + 1))""")
expl('''#### Das Modul `calendar`

Das Modul `calendar` hilft bei Fragen rund um den Kalender:

- `calendar.isleap(jahr)` gibt `True` zurück, wenn `jahr` ein Schaltjahr ist.
- `calendar.monthrange(jahr, monat)` gibt ein Tupel zurück: den Wochentag des **Ersten** (0 = Montag) und die **Anzahl der Tage** im Monat.
- `calendar.month(jahr, monat)` liefert einen kleinen Monatskalender als Text (mit englischen Abkürzungen).''',
     """import calendar

print(calendar.isleap(2024), calendar.isleap(2025))
erster, tage = calendar.monthrange(2025, 2)
print(erster, tage)
print(calendar.monthrange(2024, 2)[1])
print(calendar.month(2025, 3))""")

t('Gib für jedes Jahr aus, ob es ein Schaltjahr ist.',
  'import calendar\njahre = [1900, 2000, 2024, 2025, 2100]',
  """for jahr in jahre:
    print(jahr, calendar.isleap(jahr))""")
t('Gib für jeden Monat des Jahres 2024 die Anzahl der Tage aus wie unten.',
  'import calendar',
  """for monat in range(1, 13):
    print(monat, calendar.monthrange(2024, monat)[1])""")
t('Gib den letzten Tag des Monats von `d` als Datum aus.',
  'import calendar\nfrom datetime import date\nd = date(2025, 2, 14)',
  """letzter = calendar.monthrange(d.year, d.month)[1]
print(d.replace(day=letzter))""")
t('Gib den Monatskalender für Dezember 2025 aus.',
  'import calendar',
  """print(calendar.month(2025, 12))""")
t('Gib mit `calendar.monthrange()` den deutschen Wochentag aus, auf den der 1. Februar 2026 fällt.',
  'import calendar\n' + WT,
  """print(wochentage[calendar.monthrange(2026, 2)[0]])""")
t('Gib für jedes Jahr die Anzahl der Tage aus. Berechne sie als Abstand zwischen dem 1. Januar und dem 1. Januar des nächsten Jahres.',
  'from datetime import date\njahre = [2023, 2024, 2025]',
  """for jahr in jahre:
    print(jahr, (date(jahr + 1, 1, 1) - date(jahr, 1, 1)).days)""")
t('''Schreibe eine Funktion `plus_monat(d)`, die das Datum einen Monat später zurückgibt. Gibt es den Tag im neuen Monat nicht,
nimm den letzten Tag des Monats. Verwende `calendar.monthrange()` und `min()`.''',
  'import calendar\nfrom datetime import date\ndaten = [date(2025, 3, 14), date(2025, 1, 31), date(2025, 12, 20), date(2024, 1, 30)]',
  """def plus_monat(d):
    jahr = d.year
    monat = d.month + 1
    if monat == 13:
        jahr += 1
        monat = 1
    tag = min(d.day, calendar.monthrange(jahr, monat)[1])
    return date(jahr, monat, tag)

for d in daten:
    print(d, plus_monat(d))""")
t('''Schreibe eine Funktion `alter(geburtstag, heute)`, die das Alter in ganzen Jahren zurückgibt.
Ziehe die Jahre voneinander ab und ziehe 1 ab, wenn der Geburtstag im Jahr von `heute` noch nicht war.''',
  'from datetime import date\nheute = date(2025, 3, 14)\ngeburtstage = [date(2008, 9, 12), date(2008, 3, 14), date(2010, 1, 1)]',
  """def alter(geburtstag, heute):
    jahre = heute.year - geburtstag.year
    if geburtstag.replace(year=heute.year) > heute:
        jahre -= 1
    return jahre

for g in geburtstage:
    print(g, alter(g, heute))""")
t('Zähle, wie viele Sonntage das Jahr 2025 hat. Gehe alle Tage mit einer Schleife und `timedelta` durch.',
  'from datetime import date, timedelta',
  """d = date(2025, 1, 1)
anzahl = 0
while d.year == 2025:
    if d.weekday() == 6:
        anzahl += 1
    d += timedelta(days=1)
print(anzahl)""")
t('Gib alle Schaltjahre von 1990 bis 2030 in einer Liste aus. Verwende eine List Comprehension.',
  'import calendar',
  """print([j for j in range(1990, 2031) if calendar.isleap(j)])""")
t('Gib für jeden Geburtstag das Datum aus, an dem die Person 18 wird. Wer am 29. Februar geboren ist, wird am 1. März volljährig.',
  'from datetime import date\ngeburtstage = [date(2008, 9, 12), date(2008, 2, 29), date(2010, 1, 1)]',
  """for g in geburtstage:
    if g.month == 2 and g.day == 29:
        print(date(g.year + 18, 3, 1))
    else:
        print(g.replace(year=g.year + 18))""")
predict("""from datetime import date
d = date(2024, 2, 29)
print(d.replace(year=2028))
print(d.replace(year=2025))""", error=ValueError)
predict("""import calendar
print(calendar.isleap(2000))
erster, tage = calendar.monthrange(2025, 4)
print(erster, tage)
print(calendar.monthrange(2025, 4)[1] - calendar.monthrange(2025, 2)[1])""")

# ---------------------------------------------------------------- 9
sec('Zeitzonen und Zeitstempel')
expl('''#### Zeitzonen mit `timezone`

Bisher hatten unsere Zeitpunkte **keine** Zeitzone (man nennt sie *naiv*). Mit dem Argument `tzinfo` kann man eine angeben:

- `timezone.utc` ist die Weltzeit UTC.
- `timezone(timedelta(hours=1))` ist eine Zone mit einer Stunde Abstand zu UTC, z. B. die Winterzeit in Deutschland (MEZ).
  Die Sommerzeit (MESZ) ist `timezone(timedelta(hours=2))`.
- `dt.astimezone(zone)` rechnet einen Zeitpunkt in eine andere Zone um.

Zieht man Zeitpunkte mit Zeitzonen voneinander ab, wird der Unterschied der Zonen berücksichtigt.
Für echte Zeitzonen wie „Europe/Berlin“ mit automatischer Sommerzeit gibt es das Modul `zoneinfo`. Das lassen wir hier weg.''',
     """from datetime import datetime, timedelta, timezone

mez = timezone(timedelta(hours=1))
dt = datetime(2025, 3, 14, 12, 0, tzinfo=mez)
print(dt)
print(dt.astimezone(timezone.utc))
print(dt.astimezone(timezone(timedelta(hours=-5))))""")
expl('''#### Zeitstempel

Computer speichern Zeitpunkte oft als **Zeitstempel**: die Anzahl der Sekunden seit dem 1. Januar 1970, 0:00 Uhr UTC.

- `dt.timestamp()` gibt den Zeitstempel eines Zeitpunkts zurück (als Kommazahl).
- `datetime.fromtimestamp(zahl, tz=timezone.utc)` macht aus einem Zeitstempel wieder einen Zeitpunkt.''',
     """from datetime import datetime, timezone

dt = datetime(1970, 1, 2, tzinfo=timezone.utc)
print(dt.timestamp())
print(datetime.fromtimestamp(1700000000, tz=timezone.utc))""")

t('Rechne `dt` in UTC und in die Sommerzeit MESZ (`+2` Stunden) um und gib beide aus.',
  'from datetime import datetime, timedelta, timezone\nmez = timezone(timedelta(hours=1))\ndt = datetime(2025, 1, 15, 9, 30, tzinfo=mez)',
  """print(dt.astimezone(timezone.utc))
print(dt.astimezone(timezone(timedelta(hours=2))))""")
t('Ein Flug startet in Berlin und landet in New York (jeweils Ortszeit). Gib die Flugdauer aus.',
  '''from datetime import datetime, timedelta, timezone
berlin = timezone(timedelta(hours=1))
new_york = timezone(timedelta(hours=-5))
abflug = datetime(2025, 2, 10, 10, 0, tzinfo=berlin)
ankunft = datetime(2025, 2, 10, 13, 30, tzinfo=new_york)''',
  """print(ankunft - abflug)""")
t('Die Online-Konferenz ist in UTC angegeben. Gib für jede Stadt die Ortszeit (nur Stunde und Minute) aus wie unten.',
  '''from datetime import datetime, timedelta, timezone
konferenz = datetime(2025, 6, 2, 15, 0, tzinfo=timezone.utc)
staedte = {'Berlin': 2, 'London': 1, 'New York': -4, 'Tokio': 9}''',
  """for stadt in staedte:
    zone = timezone(timedelta(hours=staedte[stadt]))
    print(stadt, konferenz.astimezone(zone).strftime('%H:%M'))""")
t('Gib den Zeitstempel des 1. Januar 2000, 0:00 Uhr UTC aus.',
  'from datetime import datetime, timezone',
  """print(datetime(2000, 1, 1, tzinfo=timezone.utc).timestamp())""")
t('Gib den Zeitpunkt aus, der zum Zeitstempel 1000000000 gehört (in UTC).',
  'from datetime import datetime, timezone',
  """print(datetime.fromtimestamp(1000000000, tz=timezone.utc))""")
t('Gib aus, wie viele Tage zwischen den beiden Zeitstempeln liegen. Wandle sie dazu in Zeitpunkte um.',
  'from datetime import datetime, timezone\na = 1700000000\nb = 1735689600',
  """da = datetime.fromtimestamp(a, tz=timezone.utc)
db = datetime.fromtimestamp(b, tz=timezone.utc)
print((db - da).days)""")
predict("""from datetime import datetime, timezone
a = datetime(2025, 1, 1, 12, 0)
b = datetime(2025, 1, 1, 12, 0, tzinfo=timezone.utc)
print(a < b)""", error=TypeError)

# ---------------------------------------------------------------- 10
sec('Gemischte Übungen')
t('''Gib einen Monatskalender für März 2025 mit deutschen Abkürzungen aus wie unten. Verwende `calendar.monthrange()`.
Jeder Tag nimmt drei Zeichen ein (`f'{tag:3d}'`), vor dem Ersten stehen entsprechend viele Leerzeichen.''',
  'import calendar\njahr = 2025\nmonat = 3',
  """erster, anzahl = calendar.monthrange(jahr, monat)
print(' Mo Di Mi Do Fr Sa So')
zeile = '   ' * erster
for tag in range(1, anzahl + 1):
    zeile += f'{tag:3d}'
    if (erster + tag) % 7 == 0:
        print(zeile)
        zeile = ''
if zeile != '':
    print(zeile)""")
t('''Gib für jede Person aus, an welchem Datum ihr nächster Geburtstag ist und in wie vielen Tagen.
War der Geburtstag dieses Jahr schon, ist der nächste im kommenden Jahr. Ist er heute, sind es 0 Tage.''',
  "from datetime import date\nheute = date(2025, 3, 14)\ngeburtstage = {'Anna': date(2008, 9, 12), 'Ben': date(2009, 1, 3), 'Cem': date(2008, 3, 14)}",
  """for name in geburtstage:
    naechster = geburtstage[name].replace(year=heute.year)
    if naechster < heute:
        naechster = naechster.replace(year=heute.year + 1)
    print(name, naechster, (naechster - heute).days)""")
t('Zähle die Werktage (Montag bis Freitag) von `start` bis einschließlich `ende`.',
  'from datetime import date, timedelta\nstart = date(2025, 3, 1)\nende = date(2025, 3, 31)',
  """anzahl = 0
d = start
while d <= ende:
    if d.weekday() < 5:
        anzahl += 1
    d += timedelta(days=1)
print(anzahl)""")
t('''Der 4. Advent ist der letzte Sonntag vor dem 25. Dezember. Berechne ihn für 2025 und gib danach alle vier Adventssonntage aus.
Tipp: Gehe vom 24. Dezember so lange einen Tag zurück, bis es ein Sonntag ist.''',
  'from datetime import date, timedelta',
  """d = date(2025, 12, 24)
while d.weekday() != 6:
    d -= timedelta(days=1)
for i in range(3, -1, -1):
    print(d - timedelta(weeks=i))""")
t('Muttertag ist der zweite Sonntag im Mai. Gib ihn für die Jahre 2025 bis 2028 aus.',
  'from datetime import date, timedelta',
  """for jahr in range(2025, 2029):
    d = date(jahr, 5, 1)
    while d.weekday() != 6:
        d += timedelta(days=1)
    print(d + timedelta(weeks=1))""")
t('Ein Bus fährt ab 6:00 Uhr alle 20 Minuten, der letzte fährt um 8:00 Uhr. Gib alle Abfahrtszeiten aus wie unten.',
  'from datetime import datetime, timedelta',
  """abfahrt = datetime(2025, 3, 14, 6, 0)
while abfahrt <= datetime(2025, 3, 14, 8, 0):
    print(abfahrt.strftime('%H:%M'))
    abfahrt += timedelta(minutes=20)""")
t('''Die Arbeitszeiten stehen als Paare (Beginn, Ende) im Format `HH:MM`. Berechne die gesamte Arbeitszeit und gib sie aus.
Lies die Zeiten mit `datetime.strptime()` ein.''',
  "from datetime import datetime, timedelta\nzeiten = [('08:00', '12:15'), ('13:00', '16:45'), ('18:30', '19:10')]",
  """gesamt = timedelta()
for beginn, ende in zeiten:
    b = datetime.strptime(beginn, '%H:%M')
    e = datetime.strptime(ende, '%H:%M')
    gesamt += e - b
print(gesamt)""")
t('Wandle die Sekundenzahl mit `timedelta(seconds=...)` in die Form `Stunden:Minuten:Sekunden` um und gib sie aus.',
  'from datetime import timedelta\nsekunden = [59, 3723, 86399, 90061]',
  """for s in sekunden:
    print(s, timedelta(seconds=s))""")
t('Die Laufzeiten der Lieder stehen als `Minuten:Sekunden`. Gib die Gesamtlaufzeit des Albums aus.',
  "from datetime import timedelta\nlieder = ['3:45', '4:12', '2:58', '5:31', '3:09']",
  """gesamt = timedelta()
for lied in lieder:
    m, s = lied.split(':')
    gesamt += timedelta(minutes=int(m), seconds=int(s))
print(gesamt)""")
t('Zähle mit einem Dictionary, auf welche Wochentage die Geburtstage im Jahr 2025 fallen. Gib das Dictionary aus.',
  "from datetime import date\n" + WT + "\ngeburtstage = [date(2008, 9, 12), date(2009, 1, 3), date(2008, 3, 14), date(2007, 12, 24), date(2008, 6, 1)]",
  """anzahl = {}
for g in geburtstage:
    tag = wochentage[g.replace(year=2025).weekday()]
    anzahl[tag] = anzahl.get(tag, 0) + 1
print(anzahl)""")
t('''Erstelle einen Plan für die Hausaufgaben: Ab `start` gibt es jeden zweiten Werktag (Mo bis Fr) eine Aufgabe.
Gib die ersten sechs Termine mit deutschem Wochentag aus. Zähle dabei nur Werktage.''',
  'from datetime import date, timedelta\n' + WT + '\nstart = date(2025, 3, 14)',
  """d = start
werktag = 0
termine = 0
while termine < 6:
    if d.weekday() < 5:
        if werktag % 2 == 0:
            print(wochentage[d.weekday()], d.strftime('%d.%m.%Y'))
            termine += 1
        werktag += 1
    d += timedelta(days=1)""")
t('Gib aus, wie viele Stunden, Minuten und Sekunden es von jetzt bis Mitternacht sind.',
  'from datetime import time, datetime, timedelta',
  """jetzt = datetime.now()
mitternacht = datetime.combine(jetzt.date() + timedelta(days=1), time(0, 0))
rest = int((mitternacht - jetzt).total_seconds())
print(rest // 3600, 'Stunden', rest % 3600 // 60, 'Minuten', rest % 60, 'Sekunden')""", kind='free')
t('Gib aus, an welchem Datum du 10000 Tage alt bist, und welcher Wochentag das ist.',
  'from datetime import date, timedelta\n' + WT,
  """geburtstag = date(2009, 5, 17)
d = geburtstag + timedelta(days=10000)
print(d, wochentage[d.weekday()])""", kind='free')
predict("""from datetime import date, timedelta
d = date(2025, 2, 28)
print(d + timedelta(days=1))
print((d + timedelta(days=1)).strftime('%d.%m.'))
print((date(2025, 12, 25) - d).days // 7)
print(d.replace(day=1).weekday())""")

generate('datetime', 'Datum und Uhrzeit mit datetime', INTRO)
