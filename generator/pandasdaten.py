"""Beispieldaten der pandas-Reihe (gen_pandas_*.py). Die Daten werden beim Generieren mit festem Seed erzeugt und als fester Text
in die Setup-Zellen geschrieben; im Notebook gibt es also keinen Zufall."""
import datetime
import math
import random

SCHUELER = '''name;klasse;alter;wohnort;mathe;deutsch;englisch;fehltage
Ali;9a;15;Tübingen;2;3;2;4
Bea;9a;14;Rottenburg;1;2;1;0
Cem;9b;15;Tübingen;3;3;4;7
Dana;9b;16;Mössingen;2;1;2;2
Emil;9a;15;Tübingen;4;3;3;12
Fiona;9c;14;Rottenburg;1;1;2;1
Gus;9c;15;Mössingen;3;4;3;5
Hanna;9b;14;Tübingen;2;2;1;0
Ida;9c;15;Tübingen;2;3;3;3
Jan;9a;16;Rottenburg;5;4;4;15
Kim;9b;15;Mössingen;1;2;2;1
Lea;9c;14;Tübingen;3;2;2;6
'''

LAENDER = '''land,kuerzel,hauptstadt,einwohner,flaeche
Baden-Württemberg,BW,Stuttgart,11280,35748
Bayern,BY,München,13370,70542
Berlin,BE,Berlin,3760,891
Brandenburg,BB,Potsdam,2570,29654
Bremen,HB,Bremen,680,419
Hamburg,HH,Hamburg,1890,755
Hessen,HE,Wiesbaden,6390,21116
Mecklenburg-Vorpommern,MV,Schwerin,1630,23295
Niedersachsen,NI,Hannover,8140,47710
Nordrhein-Westfalen,NW,Düsseldorf,18140,34112
Rheinland-Pfalz,RP,Mainz,4160,19858
Saarland,SL,Saarbrücken,990,2571
Sachsen,SN,Dresden,4090,18450
Sachsen-Anhalt,ST,Magdeburg,2180,20459
Schleswig-Holstein,SH,Kiel,2950,15804
Thüringen,TH,Erfurt,2130,16202
'''


def kiosk_csv():
    """Verkäufe eines Schulkiosks an 10 Schultagen (ausgedacht)."""
    artikel = [('Brezel', 'Backwaren', 0.80), ('Laugenstange', 'Backwaren', 1.00), ('Apfel', 'Obst', 0.50), ('Banane', 'Obst', 0.40),
               ('Wasser', 'Getränke', 1.00), ('Apfelschorle', 'Getränke', 1.50), ('Müsliriegel', 'Snacks', 1.20)]
    tage = ['Montag', 'Dienstag', 'Mittwoch', 'Donnerstag', 'Freitag']
    rnd = random.Random(7)
    zeilen = ['datum;tag;artikel;kategorie;menge;preis']
    d = datetime.date(2026, 10, 5)
    for woche in range(2):
        for i in range(5):
            tag = d + datetime.timedelta(days=7 * woche + i)
            for name, kat, preis in artikel:
                menge = rnd.randint(5, 40) + (10 if tage[i] == 'Freitag' and kat == 'Backwaren' else 0)
                zeilen.append(f'{tag.isoformat()};{tage[i]};{name};{kat};{menge};{preis:.2f}')
    return '\n'.join(zeilen) + '\n'


def wetter_csv():
    """Temperatur und Regen für jeden Tag vom 1.1. bis 30.6.2026 (ausgedacht, plausibler Jahresgang)."""
    rnd = random.Random(3)
    zeilen = ['datum,temperatur,regen']
    d = datetime.date(2026, 1, 1)
    for i in range(181):
        tag = d + datetime.timedelta(days=i)
        temp = 9 - 10 * math.cos(2 * math.pi * (i + 10) / 365) + rnd.gauss(0, 2.5)
        regen = max(0.0, rnd.gauss(-1.0, 3.5))
        zeilen.append(f'{tag.isoformat()},{temp:.1f},{regen:.1f}')
    return '\n'.join(zeilen) + '\n'


def setup_code(dateien):
    """Code der Setup-Zelle, der die Dateien {name: inhalt} anlegt."""
    teile = ['dateien = {']
    for name, inhalt in dateien.items():
        teile.append(f"    '{name}': '''{inhalt}''',")
    teile.append('}')
    teile.append('for name, inhalt in dateien.items():')
    teile.append("    with open(name, 'w', encoding='utf-8') as f:")
    teile.append('        f.write(inhalt)')
    teile.append("print('Angelegt:', ', '.join(dateien))")
    return '\n'.join(teile)
