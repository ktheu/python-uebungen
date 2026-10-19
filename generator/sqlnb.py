"""Ausführung von SQL-Zellen beim Generieren von SQL-Notebooks (Kernel xeus-sqlite in JupyterLite).

nbgen.generate(..., sprache='sqlite', ausfuehren=sql_ausfuehrung(ordner)) prüft damit alle Zellen:
- '%LOAD datei.db r' bzw. 'rw' öffnet eine Datenbank aus `ordner` (wie im Notebook-Ordner), '%CREATE datei.db' legt eine neue an.
- Jede andere Zelle ist genau EINE SQL-Anweisung (wie im Kernel). Die Verbindung bleibt über alle Zellen bestehen,
  so wie im Notebook, wenn man die Zellen der Reihe nach ausführt.
- Das Ergebnis wird als Markdown-Tabelle zurückgegeben, so wie der Kernel es anzeigt: Spaltennamen als Kopf,
  jeder Wert als Text, den SQLite selbst daraus macht (CAST AS TEXT), NULL als leere Zelle.

xeus-sqlite 0.10.0 enthält SQLite 3.49.2; Python 3.13 unter Windows SQLite 3.49.1 (gleiches Verhalten).
"""
import atexit
import os
import shutil
import sqlite3


def _text(con, wert):
    if wert is None:
        return ''
    if isinstance(wert, float):  # so, wie SQLite eine Kommazahl in Text umwandelt (z. B. 2.0, 0.333333333333333)
        return con.execute('SELECT CAST(? AS TEXT)', (wert,)).fetchone()[0]
    return str(wert)


def _zelle(text):
    return text.replace('|', '\\|') if text else ' '


def tabelle(con, cursor):
    """Ergebnis einer Abfrage als Markdown-Tabelle mit Zeilenzahl darunter ('' wenn die Anweisung nichts liefert)."""
    if cursor.description is None:
        return ''
    kopf = [d[0] for d in cursor.description]
    zeilen = cursor.fetchall()
    md = ['| ' + ' | '.join(_zelle(k) for k in kopf) + ' |', '|' + '---|' * len(kopf)]
    for z in zeilen:
        md.append('| ' + ' | '.join(_zelle(_text(con, w)) for w in z) + ' |')
    md.append('')
    md.append(f'*{len(zeilen)} Zeile{"" if len(zeilen) == 1 else "n"}*')
    return '\n'.join(md) + '\n'


def html_tabelle(con, cursor):
    """Wie tabelle(), aber als HTML-Tabelle, die linksbündig steht (Markdown-Tabellen zentriert JupyterLab)."""
    if cursor.description is None:
        return ''
    kopf = [d[0] for d in cursor.description]
    zeilen = cursor.fetchall()
    h = ['<table style="margin-left: 0">', '<tr>' + ''.join(f'<th>{k}</th>' for k in kopf) + '</tr>']
    for z in zeilen:
        h.append('<tr>' + ''.join(f'<td>{_text(con, w)}</td>' for w in z) + '</tr>')
    h.append('</table>')
    h.append('')
    h.append(f'*{len(zeilen)} Zeile{"" if len(zeilen) == 1 else "n"}*')
    return '\n'.join(h) + '\n'


# ---------------------------------------------------------------- ER-Diagramme
ZEILE = 0.55      # Höhe einer Zeile im Kasten (Dateneinheiten)
BREITE = 3.6      # Breite eines Kastens
ZOLL = 0.42       # Zoll pro Dateneinheit im Bild


def kasten_hoehe(spalten):
    return (len(spalten) + 1) * ZEILE + 0.35


def er_bild(tabellen, beziehungen, positionen, auswahl=None, dpi=72):
    """Zeichnet ein Diagramm im Stil des Unterrichts: Kasten pro Tabelle (Name rot, Primärschlüssel unterstrichen,
    Fremdschlüssel mit ↑), Verbindungslinien mit 1 und n. Gibt PNG-Daten zurück.
    tabellen: {name: [(spalte, typ, 'PK'/'FK'/'')]}, beziehungen: [(eins, viele, anker_eins, anker_viele)],
    anker = (seite, anteil), seite 'l', 'r', 'o', 'u', anteil 0..1 entlang der Seite.
    positionen: {name: (x, y)} der linken oberen Ecke. auswahl: nur diese Tabellen (Standard: alle)."""
    import io as _io
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    from matplotlib.patches import Rectangle

    auswahl = list(tabellen) if auswahl is None else auswahl
    x0 = min(positionen[t][0] for t in auswahl) - 0.6
    x1 = max(positionen[t][0] + BREITE for t in auswahl) + 0.6
    y1 = max(positionen[t][1] for t in auswahl) + 0.4
    y0 = min(positionen[t][1] - kasten_hoehe(tabellen[t]) for t in auswahl) - 0.4
    fig = plt.figure(figsize=((x1 - x0) * ZOLL, (y1 - y0) * ZOLL), dpi=dpi)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(x0, x1)
    ax.set_ylim(y0, y1)
    ax.axis('off')
    renderer = fig.canvas.get_renderer()

    def punkt(name, anker):
        x, y = positionen[name]
        h = kasten_hoehe(tabellen[name])
        seite, a = anker
        return {'l': (x, y - a * h), 'r': (x + BREITE, y - a * h),
                'o': (x + a * BREITE, y), 'u': (x + a * BREITE, y - h)}[seite]

    for eins, viele, anker_eins, anker_viele in beziehungen:
        if eins in auswahl and viele in auswahl:
            p, q = punkt(eins, anker_eins), punkt(viele, anker_viele)
            ax.plot([p[0], q[0]], [p[1], q[1]], color='black', linewidth=1.2)
            for (ax_, ay), (bx, by), text in [(p, q, '1'), (q, p, 'n')]:
                lang = ((bx - ax_) ** 2 + (by - ay) ** 2) ** 0.5
                ax.text(ax_ + (bx - ax_) / lang * 0.35, ay + (by - ay) / lang * 0.35 + 0.25, text,
                        fontsize=11, fontweight='bold', ha='center', va='bottom')

    for name in auswahl:
        x, y = positionen[name]
        spalten = tabellen[name]
        ax.add_patch(Rectangle((x, y - kasten_hoehe(spalten)), BREITE, kasten_hoehe(spalten),
                               facecolor='white', edgecolor='black', linewidth=1.5))
        ax.text(x + 0.3, y - 0.2, name, fontsize=13, fontweight='bold', color='firebrick', va='top')
        for i, (spalte, typ, schluessel) in enumerate(spalten):
            zy = y - 0.2 - (i + 1) * ZEILE - 0.08
            if schluessel == 'FK':
                ax.text(x + 0.35, zy, '↑', fontsize=11, va='top')
            t = ax.text(x + 0.75, zy, spalte, fontsize=11, va='top')
            if schluessel == 'PK':  # unterstreichen
                bb = t.get_window_extent(renderer).transformed(ax.transData.inverted())
                ax.plot([bb.x0, bb.x1], [bb.y0 - 0.03, bb.y0 - 0.03], color='black', linewidth=1)
    buf = _io.BytesIO()
    fig.savefig(buf, format='png', dpi=dpi, metadata={'Software': None})
    plt.close(fig)
    return buf.getvalue()


def sql_ausfuehrung(ordner, html=True):
    """Gibt eine Funktion code -> (ausgabe, fehler, bilder) für nbgen zurück. ordner: dort liegen die .db-Dateien.
    html: Ergebnis als linksbündige HTML-Tabelle (sonst Markdown-Tabelle, die JupyterLab zentriert)."""
    zustand = {'con': None}

    def schliessen():
        if zustand['con'] is not None:
            zustand['con'].close()
            zustand['con'] = None

    atexit.register(schliessen)

    def ausfuehren(code):
        teile = code.split()
        try:
            if teile and teile[0].upper() == '%LOAD':
                name, modus = teile[1], (teile[2] if len(teile) > 2 else 'rw')
                quelle = os.path.join(ordner, name)
                schliessen()
                if modus == 'r':
                    zustand['con'] = sqlite3.connect(f'file:{quelle}?mode=ro', uri=True)
                else:  # Änderungen nur an einer Kopie im temporären Arbeitsordner
                    shutil.copy(quelle, name)
                    zustand['con'] = sqlite3.connect(name)
                return '', None, []
            if teile and teile[0].upper() == '%CREATE':
                schliessen()
                if os.path.exists(teile[1]):
                    os.remove(teile[1])
                zustand['con'] = sqlite3.connect(teile[1])
                return '', None, []
            con = zustand['con']
            if con is None:
                raise sqlite3.OperationalError('Please load a database to perform operations')
            cursor = con.execute(code)  # mehr als eine Anweisung -> ProgrammingError
            ausgabe = html_tabelle(con, cursor) if html else tabelle(con, cursor)
            con.commit()
            return ausgabe, None, []
        except (sqlite3.Error, IndexError) as e:
            return '', e, []

    return ausfuehren
