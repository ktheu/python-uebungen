"""UML-Klassendiagramme als PNG für die OOP-Notebooks (im Stil des Unterrichts, vgl. InfoKursN/adtListe/liste_uml.png).

Notation: Sichtbarkeit (+ öffentlich, - privat, # geschützt) und Typangaben, z. B. '- kontostand: float',
'+ einzahlen(betrag: float): void'. Der Konstruktor steht mit dem Klassennamen da: '+ Konto(inhaber: str)'.
Methoden ohne Rückgabewert haben den Typ void.

    png = uml_bild({'Konto': (['- inhaber: str', '- kontostand: float'],
                              ['+ Konto(inhaber: str)', '+ einzahlen(betrag: float): void'])})
    expl('... ![Klassendiagramm](attachment:konto.png)', code, anhaenge={'konto.png': png})

Mehrere Klassen: positionen={name: (x, y)} (linke obere Ecke in Zoll, y nach unten), sonst nebeneinander.
pfeile: [(von, nach, art, beschriftung)] mit art 'assoziation' (offene Pfeilspitze) oder 'vererbung' (leeres Dreieck);
beschriftung (z. B. '1..*') ist optional. von == nach zeichnet eine rekursive Assoziation als Schleife rechts oben.
"""
import io

SCHRIFT = 11          # Punkt
ZEILE = 0.22          # Zeilenhöhe in Zoll
RAND = 0.08           # Innenabstand in Zoll
ABSTAND = 1.0         # Abstand zwischen Kästen bei automatischer Anordnung (Zoll)


def _breite(text, fett=False):
    from matplotlib.textpath import TextPath
    from matplotlib.font_manager import FontProperties
    fp = FontProperties(family='DejaVu Sans', weight='bold' if fett else 'normal')
    return TextPath((0, 0), text, size=SCHRIFT, prop=fp).get_extents().width / 72


def masse(name, attribute, methoden):
    """Breite und Höhe eines Kastens in Zoll sowie die Höhen der drei Teile."""
    b = max([_breite(name, True)] + [_breite(z) for z in attribute + methoden]) + 2 * RAND + 0.1
    h_name = ZEILE + 2 * RAND
    h_attr = max(len(attribute), 0) * ZEILE + 2 * RAND
    h_meth = max(len(methoden), 0) * ZEILE + 2 * RAND
    return b, h_name + h_attr + h_meth, (h_name, h_attr, h_meth)


def uml_bild(klassen, pfeile=(), positionen=None, dpi=100):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    from matplotlib.patches import Rectangle, Polygon

    groesse = {n: masse(n, a, m) for n, (a, m) in klassen.items()}
    if positionen is None:
        positionen, x = {}, 0.0
        for n in klassen:
            positionen[n] = (x, 0.0)
            x += groesse[n][0] + ABSTAND
    # Kästen: (x0, y_oben, x1, y_unten) in einem Koordinatensystem mit y nach oben (y = -y_position)
    box = {n: (positionen[n][0], -positionen[n][1], positionen[n][0] + groesse[n][0],
               -positionen[n][1] - groesse[n][1]) for n in klassen}
    x0 = min(b[0] for b in box.values()) - 0.15
    x1 = max(b[2] for b in box.values()) + 0.15
    y1 = max(b[1] for b in box.values()) + 0.15
    y0 = min(b[3] for b in box.values()) - 0.15
    for von, nach, *_ in pfeile:
        if von == nach:  # Schleife braucht Platz rechts und oben
            x1 = max(x1, box[von][2] + 0.5)
            y1 = max(y1, box[von][1] + 0.5)
    fig = plt.figure(figsize=(x1 - x0, y1 - y0), dpi=dpi)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(x0, x1)
    ax.set_ylim(y0, y1)
    ax.axis('off')

    for n, (attribute, methoden) in klassen.items():
        bx0, by1, bx1, by0 = box[n]
        h_name, h_attr, h_meth = groesse[n][2]
        ax.add_patch(Rectangle((bx0, by0), bx1 - bx0, by1 - by0, facecolor='white', edgecolor='black', linewidth=1.3, zorder=2))
        ax.text((bx0 + bx1) / 2, by1 - h_name / 2, n, fontsize=SCHRIFT, fontweight='bold', ha='center', va='center',
                family='DejaVu Sans', zorder=3)
        y = by1 - h_name
        ax.plot([bx0, bx1], [y, y], color='black', linewidth=1, zorder=3)
        for i, z in enumerate(attribute):
            ax.text(bx0 + RAND + 0.05, y - RAND - (i + 0.5) * ZEILE, z, fontsize=SCHRIFT, va='center', family='DejaVu Sans', zorder=3)
        y -= h_attr
        ax.plot([bx0, bx1], [y, y], color='black', linewidth=1, zorder=3)
        for i, z in enumerate(methoden):
            ax.text(bx0 + RAND + 0.05, y - RAND - (i + 0.5) * ZEILE, z, fontsize=SCHRIFT, va='center', family='DejaVu Sans', zorder=3)

    def spitze(p, q, art):
        """Pfeilspitze bei q, Linie kommt von p."""
        dx, dy = q[0] - p[0], q[1] - p[1]
        l = (dx * dx + dy * dy) ** 0.5
        ux, uy = dx / l, dy / l
        a, b = 0.16, 0.08
        links = (q[0] - a * ux - b * uy, q[1] - a * uy + b * ux)
        rechts = (q[0] - a * ux + b * uy, q[1] - a * uy - b * ux)
        if art == 'vererbung':
            ax.add_patch(Polygon([q, links, rechts], closed=True, facecolor='white', edgecolor='black', linewidth=1.2, zorder=4))
        else:
            ax.plot([links[0], q[0], rechts[0]], [links[1], q[1], rechts[1]], color='black', linewidth=1.2, zorder=4)

    for pf in pfeile:
        von, nach, art = pf[0], pf[1], pf[2]
        text = pf[3] if len(pf) > 3 else ''
        a, b = box[von], box[nach]
        if von == nach:
            xr, yo = a[2], a[1]
            ym = (a[1] + a[3]) / 2
            xm = (a[0] + a[2]) / 2 + (a[2] - a[0]) / 4
            pts = [(xr, ym), (xr + 0.35, ym), (xr + 0.35, yo + 0.35), (xm, yo + 0.35), (xm, yo)]
            ax.plot([p[0] for p in pts], [p[1] for p in pts], color='black', linewidth=1.2, zorder=1)
            spitze(pts[-2], pts[-1], art)
            if text:
                ax.text(xm + 0.08, yo + 0.08, text, fontsize=SCHRIFT - 1, family='DejaVu Sans', va='bottom')
            continue
        if a[2] <= b[0] or b[2] <= a[0]:  # nebeneinander: waagrecht von Seite zu Seite
            ym = (max(a[3], b[3]) + min(a[1], b[1])) / 2
            if not (max(a[3], b[3]) < ym < min(a[1], b[1])):
                ym = (a[1] + a[3]) / 2
            p = (a[2], ym) if a[2] <= b[0] else (a[0], ym)
            q = (b[0], ym) if a[2] <= b[0] else (b[2], ym)
        else:  # übereinander: senkrecht
            xm = (max(a[0], b[0]) + min(a[2], b[2])) / 2
            p = (xm, a[3]) if a[3] >= b[1] else (xm, a[1])
            q = (xm, b[1]) if a[3] >= b[1] else (xm, b[3])
        ax.plot([p[0], q[0]], [p[1], q[1]], color='black', linewidth=1.2, zorder=1)
        spitze(p, q, art)
        if text:
            if p[1] == q[1]:
                ax.text(q[0] - 0.1 if q[0] > p[0] else q[0] + 0.1, q[1] + 0.06, text, fontsize=SCHRIFT - 1,
                        ha='right' if q[0] > p[0] else 'left', va='bottom', family='DejaVu Sans')
            else:
                ax.text(q[0] + 0.08, q[1] + (0.1 if q[1] > p[1] else -0.1), text, fontsize=SCHRIFT - 1,
                        va='top' if q[1] > p[1] else 'bottom', family='DejaVu Sans')

    buf = io.BytesIO()
    fig.savefig(buf, format='png', dpi=dpi, metadata={'Software': None})
    plt.close(fig)
    return buf.getvalue()


if __name__ == '__main__':  # Probebild
    import sys
    png = uml_bild({'Konto': (['- inhaber: str', '- kontostand: float'],
                              ['+ Konto(inhaber: str)', '+ einzahlen(betrag: float): void', '+ get_kontostand(): float']),
                    'Person': (['+ name: str', '+ mutter: Person'], ['+ Person(name: str)']),
                    'Sparkonto': (['- zinssatz: float'], ['+ Sparkonto(inhaber: str, zinssatz: float)'])},
                   [('Konto', 'Person', 'assoziation', '1'), ('Person', 'Person', 'assoziation', '0..1'),
                    ('Sparkonto', 'Konto', 'vererbung')],
                   positionen={'Konto': (0, 0), 'Person': (4.2, 0.3), 'Sparkonto': (0, 2.3)})
    open(sys.argv[1], 'wb').write(png)
