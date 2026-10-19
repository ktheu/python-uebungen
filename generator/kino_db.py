"""Erzeugt die Beispieldatenbank content/kino.db für das SQL-Notebook (gen_sql_abfragen.py).

Die Daten sind erfunden und werden mit festem Seed erzeugt. Die Datei wird nur neu geschrieben,
wenn sich der Inhalt geändert hat (Vergleich über iterdump()), damit Git keine unnötigen Änderungen sieht.

Außerdem stehen hier die Tabellen, Beziehungen und Positionen für die Diagramme (er_bild()).
"""
import os
import random
import sqlite3

SCHEMA = """
CREATE TABLE film (
    film_id INTEGER PRIMARY KEY,
    titel TEXT NOT NULL,
    genre TEXT NOT NULL,
    jahr INTEGER NOT NULL,
    dauer INTEGER NOT NULL,
    fsk INTEGER NOT NULL
);
CREATE TABLE saal (
    saal_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    plaetze INTEGER NOT NULL,
    ausstattung TEXT NOT NULL
);
CREATE TABLE vorstellung (
    vorstellung_id INTEGER PRIMARY KEY,
    film_id INTEGER NOT NULL REFERENCES film(film_id),
    saal_id INTEGER NOT NULL REFERENCES saal(saal_id),
    datum TEXT NOT NULL,
    uhrzeit TEXT NOT NULL,
    preis REAL NOT NULL
);
CREATE TABLE kunde (
    kunde_id INTEGER PRIMARY KEY,
    vorname TEXT NOT NULL,
    nachname TEXT NOT NULL,
    geburtsjahr INTEGER NOT NULL,
    wohnort TEXT NOT NULL,
    email TEXT
);
CREATE TABLE ticket (
    ticket_id INTEGER PRIMARY KEY,
    vorstellung_id INTEGER NOT NULL REFERENCES vorstellung(vorstellung_id),
    kunde_id INTEGER NOT NULL REFERENCES kunde(kunde_id),
    reihe INTEGER NOT NULL,
    platz INTEGER NOT NULL,
    ermaessigt INTEGER NOT NULL
);
"""

# Für die ER-Diagramme: Spalten mit Typ und Schlüssel, Beziehungen (1:n)
TABELLEN = {
    'film': [('film_id', 'int', 'PK'), ('titel', 'text', ''), ('genre', 'text', ''), ('jahr', 'int', ''),
             ('dauer', 'int', ''), ('fsk', 'int', '')],
    'saal': [('saal_id', 'int', 'PK'), ('name', 'text', ''), ('plaetze', 'int', ''), ('ausstattung', 'text', '')],
    'vorstellung': [('vorstellung_id', 'int', 'PK'), ('film_id', 'int', 'FK'), ('saal_id', 'int', 'FK'),
                    ('datum', 'text', ''), ('uhrzeit', 'text', ''), ('preis', 'real', '')],
    'kunde': [('kunde_id', 'int', 'PK'), ('vorname', 'text', ''), ('nachname', 'text', ''),
              ('geburtsjahr', 'int', ''), ('wohnort', 'text', ''), ('email', 'text', '')],
    'ticket': [('ticket_id', 'int', 'PK'), ('vorstellung_id', 'int', 'FK'), ('kunde_id', 'int', 'FK'),
               ('reihe', 'int', ''), ('platz', 'int', ''), ('ermaessigt', 'int', '')],
}
BEZIEHUNGEN = [  # (Tabelle auf der 1-Seite, Tabelle auf der n-Seite, Anker 1-Seite, Anker n-Seite), siehe sqlnb.er_bild()
    ('film', 'vorstellung', ('r', 0.5), ('l', 0.3)),
    ('saal', 'vorstellung', ('r', 0.5), ('l', 0.75)),
    ('vorstellung', 'ticket', ('r', 0.5), ('l', 0.5)),
    ('kunde', 'ticket', ('l', 0.5), ('r', 0.5)),
]
POSITIONEN = {'film': (0, 9.5), 'saal': (0, 4.3), 'vorstellung': (5.6, 8.4), 'ticket': (11.2, 8.4), 'kunde': (16.8, 9.5)}

FILME = [
    (1, 'Der Leuchtturm am Ende der Welt', 'Drama', 2024, 112, 12),
    (2, 'Galaxis Express', 'Science-Fiction', 2025, 128, 12),
    (3, 'Pinguine auf Abwegen', 'Animation', 2025, 89, 0),
    (4, 'Die letzte Spur', 'Krimi', 2023, 104, 16),
    (5, 'Sommer in Lissabon', 'Komödie', 2024, 97, 6),
    (6, 'Robo-Ritter', 'Animation', 2024, 92, 6),
    (7, 'Tiefsee – Das unbekannte Blau', 'Dokumentation', 2025, 85, 0),
    (8, 'Kettenreaktion', 'Action', 2025, 131, 16),
    (9, 'Das Geheimnis der alten Mühle', 'Familie', 2023, 95, 6),
    (10, 'Nachtzug nach Wien', 'Krimi', 2025, 118, 12),
    (11, 'Wolkenkratzer', 'Action', 2023, 124, 16),
    (12, 'Planet der Pilze', 'Science-Fiction', 2024, 109, 12),
    (13, 'Omas großes Abenteuer', 'Komödie', 2025, 101, 0),
    (14, 'Schattenspiel', 'Horror', 2024, 99, 18),
    (15, 'Die Bienenkönigin', 'Dokumentation', 2023, 78, 0),
    (16, 'Funkstille', 'Drama', 2025, 116, 12),
    (17, 'Mission Mondbasis', 'Science-Fiction', 2025, 135, 12),
    (18, 'Der Fluch von Burg Eisenstein', 'Horror', 2025, 94, 16),
    (19, 'Fußballfieber', 'Komödie', 2024, 93, 6),
    (20, 'Ein Koffer voller Träume', 'Drama', 2022, 121, 12),     # läuft nicht
    (21, 'Zeitreise für Anfänger', 'Komödie', 2025, 105, 12),     # läuft nicht
]

SAELE = [
    (1, 'Großer Saal', 220, 'IMAX'),
    (2, 'Blauer Saal', 140, '3D'),
    (3, 'Roter Saal', 90, 'Standard'),
    (4, 'Lounge', 40, 'Lounge'),
]
AUFSCHLAG = {'IMAX': 3.0, '3D': 2.0, 'Standard': 0.0, 'Lounge': 6.0}

KUNDEN = [
    (1, 'Lena', 'Hoffmann', 2009, 'Münster', 'lena.h@example.de'),
    (2, 'Jonas', 'Becker', 2008, 'Greven', 'jonas.becker@example.de'),
    (3, 'Mia', 'Schulz', 2011, 'Münster', None),
    (4, 'Paul', 'Wagner', 1975, 'Telgte', 'p.wagner@example.de'),
    (5, 'Emma', 'Fischer', 1982, 'Münster', 'emma.fischer@example.de'),
    (6, 'Ben', 'Weber', 2007, 'Senden', None),
    (7, 'Sophie', 'Meyer', 1990, 'Münster', 'sophie.m@example.de'),
    (8, 'Noah', 'Schneider', 2010, 'Havixbeck', None),
    (9, 'Hannah', 'Koch', 1968, 'Greven', 'hannah.koch@example.de'),
    (10, 'Elias', 'Richter', 1999, 'Münster', 'elias.r@example.de'),
    (11, 'Lea', 'Klein', 2006, 'Telgte', 'lea.klein@example.de'),
    (12, 'Finn', 'Wolf', 2012, 'Münster', None),
    (13, 'Marie', 'Schröder', 1955, 'Münster', 'marie.schroeder@example.de'),
    (14, 'Luca', 'Neumann', 2004, 'Senden', 'luca.n@example.de'),
    (15, 'Clara', 'Schwarz', 1987, 'Greven', 'clara.schwarz@example.de'),
    (16, 'Felix', 'Zimmermann', 2009, 'Münster', 'felix.z@example.de'),
    (17, 'Ida', 'Braun', 1979, 'Havixbeck', None),
    (18, 'Leon', 'Krüger', 2002, 'Münster', 'leon.krueger@example.de'),
    (19, 'Ella', 'Hofmann', 2010, 'Telgte', None),
    (20, 'Anton', 'Hartmann', 1961, 'Münster', 'anton.hartmann@example.de'),
    (21, 'Frieda', 'Lange', 1995, 'Greven', 'frieda.lange@example.de'),
    (22, 'Theo', 'Schmitt', 2008, 'Münster', 'theo.s@example.de'),
    (23, 'Lina', 'Werner', 1972, 'Senden', None),        # kauft kein Ticket
    (24, 'Karl', 'Krause', 1948, 'Münster', None),        # kauft kein Ticket
]

TAGE = ['2026-11-02', '2026-11-03', '2026-11-04', '2026-11-05', '2026-11-06', '2026-11-07', '2026-11-08']


def vorstellungen(rng):
    """Spielplan einer Woche: pro Tag 6 bis 8 Vorstellungen, nie zwei gleichzeitig im selben Saal."""
    laufen = [f[0] for f in FILME if f[0] not in (20, 21)]
    zeiten = ['14:30', '17:00', '20:00', '22:30']
    liste = []
    nr = 1
    for tag in TAGE:
        belegt = set()
        anzahl = rng.randint(6, 8)
        while len(belegt) < anzahl:
            saal = rng.choice(SAELE)
            zeit = rng.choice(zeiten)
            if (saal[0], zeit) in belegt:
                continue
            belegt.add((saal[0], zeit))
            film = rng.choice(laufen)
            preis = 9.5 + AUFSCHLAG[saal[3]]
            if tag == '2026-11-03':      # Kinotag am Dienstag
                preis -= 2.0
            if zeit == '14:30':
                preis -= 1.0
            liste.append((nr, film, saal[0], tag, zeit, preis))
            nr += 1
    liste.sort(key=lambda v: (v[3], v[4], v[2]))
    return [(i + 1,) + v[1:] for i, v in enumerate(liste)]


def tickets(rng, vorst):
    fsk = {f[0]: f[5] for f in FILME}
    plaetze = {s[0]: s[2] for s in SAELE}
    kaeufer = [k for k in KUNDEN if k[0] not in (23, 24)]
    liste = []
    nr = 1
    for v in vorst:
        erlaubt = [k for k in kaeufer if 2026 - k[3] >= fsk[v[1]]]
        anzahl = rng.randint(0, 6)
        besetzt = set()
        for k in rng.sample(erlaubt, anzahl):
            reihen = plaetze[v[2]] // 20
            while True:
                sitz = (rng.randint(1, reihen), rng.randint(1, 20))
                if sitz not in besetzt:
                    break
            besetzt.add(sitz)
            ermaessigt = 1 if 2026 - k[3] < 18 or 2026 - k[3] >= 65 else 0
            liste.append((nr, v[0], k[0], sitz[0], sitz[1], ermaessigt))
            nr += 1
    return liste


def erzeuge(pfad):
    """Schreibt die Datenbank nach pfad (nur wenn sich der Inhalt geändert hat). Gibt True zurück, wenn geschrieben wurde."""
    rng = random.Random(2026)
    vorst = vorstellungen(rng)
    tick = tickets(rng, vorst)
    neu = sqlite3.connect(':memory:')
    neu.executescript(SCHEMA)
    neu.executemany('INSERT INTO film VALUES (?, ?, ?, ?, ?, ?)', FILME)
    neu.executemany('INSERT INTO saal VALUES (?, ?, ?, ?)', SAELE)
    neu.executemany('INSERT INTO vorstellung VALUES (?, ?, ?, ?, ?, ?)', vorst)
    neu.executemany('INSERT INTO kunde VALUES (?, ?, ?, ?, ?, ?)', KUNDEN)
    neu.executemany('INSERT INTO ticket VALUES (?, ?, ?, ?, ?, ?)', tick)
    neu.commit()
    inhalt_neu = list(neu.iterdump())
    if os.path.exists(pfad):
        alt = sqlite3.connect(pfad)
        inhalt_alt = list(alt.iterdump())
        alt.close()
        if inhalt_alt == inhalt_neu:
            neu.close()
            return False
        os.remove(pfad)
    ziel = sqlite3.connect(pfad)
    neu.backup(ziel)
    ziel.close()
    neu.close()
    return True


def er_bild(auswahl=None):
    """Diagramm der Datenbank (oder nur der Tabellen in auswahl) als PNG-Daten, im Stil des Unterrichts."""
    from sqlnb import er_bild as zeichnen
    return zeichnen(TABELLEN, BEZIEHUNGEN, POSITIONEN, auswahl)

if __name__ == '__main__':
    ziel = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'content', 'kino.db')
    print('geschrieben' if erzeuge(ziel) else 'unverändert', ziel)
