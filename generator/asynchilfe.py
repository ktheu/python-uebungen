"""Gemeinsames für die asyncio-Notebooks (gen_asyncio_*.py): Abkürzung t(), Liste der Reihe fürs Intro, Ausführung mit Top-Level-await."""
from nbgen import task
import asyncnb

AUSFUEHREN = asyncnb.ausfuehrung()

REIHE = [
    ('asyncio_grundlagen', 'Warten, `async def`, `await`, `asyncio.run()`, erster Blick auf `gather()`'),
    ('asyncio_tasks', 'Tasks mit `create_task()`, `gather()`, `as_completed()`, `TaskGroup`'),
    ('asyncio_steuerung', 'Zeitlimits, Abbrechen, Fehler in Tasks, `Lock`, `Semaphore`, `Event`'),
    ('asyncio_anwendungen', '`Queue`, `async with`, `async for` und kleine Anwendungen'),
]


def t(text, given='', body='', kind='normal'):
    """Aufgabe, deren Lösung aus dem vorgegebenen Code plus body besteht."""
    task(text, given=given, solution=(given + '\n' + body) if given else body, kind=kind)


def reihe(aktuell):
    """Aufzählung der Notebooks der Reihe; das aktuelle ist fett."""
    zeilen = []
    for name, beschreibung in REIHE:
        marke = f'**{name}**' if name == aktuell else name
        zeilen.append(f'- {marke}: {beschreibung}')
    return '\n'.join(zeilen)
