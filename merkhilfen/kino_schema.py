# Erzeugt kino_schema.png (Diagramm der Kino-Datenbank im Stil des Unterrichts) für die SQL-Merkhilfe.
#
#     py -3.13 merkhilfen/kino_schema.py
#
# Dasselbe Diagramm wie im Notebook sql_abfragen (generator/kino_db.py, generator/sqlnb.py), nur mit höherer Auflösung zum Drucken.
import os
import sys

HIER = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(HIER), 'generator'))

from kino_db import TABELLEN, BEZIEHUNGEN, POSITIONEN  # noqa: E402
from sqlnb import er_bild  # noqa: E402

with open(os.path.join(HIER, 'kino_schema.png'), 'wb') as f:
    f.write(er_bild(TABELLEN, BEZIEHUNGEN, POSITIONEN, dpi=250))
print('geschrieben: kino_schema.png')
