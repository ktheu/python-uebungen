"""UML-Klassendiagramme als PNG für die OOP-Notebooks (im Stil des Unterrichts, vgl. InfoKursN/adtListe/liste_uml.png).

Notation: Sichtbarkeit (+ öffentlich, - privat, # geschützt) und Typangaben, z. B. '- kontostand: float',
'+ einzahlen(betrag: float): void'. Der Konstruktor steht mit dem Klassennamen da: '+ Konto(inhaber: str)'.
Methoden ohne Rückgabewert haben den Typ void. Klassenattribute und Klassenmethoden werden in UML unterstrichen:
Dafür schreibt man 'static ' vor den Eintrag ('static - anzahl: int').

    png = uml_bild({'Konto': (['- inhaber: str', '- kontostand: float'],
                              ['+ Konto(inhaber: str)', '+ einzahlen(betrag: float): void'])})
    expl('... ![Klassendiagramm](attachment:konto.png)', code, anhaenge={'konto.png': png})

Mehrere Klassen: positionen={name: (x, y)} (linke obere Ecke in Zoll, y nach unten), sonst nebeneinander.
pfeile: [(von, nach, art, text_ziel, text_start)] mit art
  'assoziation'  gerichtete Assoziation (Linie mit offener Pfeilspitze bei nach),
  'ungerichtet'  Assoziation in beide Richtungen (Linie ohne Spitze),
  'vererbung'    Vererbung (leeres Dreieck bei der Oberklasse nach).
text_ziel/text_start (z. B. Multiplizitäten '1', '0..*') sind optional. von == nach zeichnet eine rekursive Assoziation
als Schleife rechts oben. Linien gehen waagrecht (Kästen nebeneinander) oder senkrecht (übereinander).
"""
import io

SCHRIFT = 11          # Punkt
ZEILE = 0.22          # Zeilenhöhe in Zoll
RAND = 0.08           # Innenabstand in Zoll
ABSTAND = 1.2         # Abstand zwischen Kästen bei automatischer Anordnung (Zoll)
STATIC = 'static '


def _breite(text, fett=False):
    from matplotlib.textpath import TextPath
    from matplotlib.font_manager import FontProperties
    fp = FontProperties(family='DejaVu Sans', weight='bold' if fett else 'normal')
    return TextPath((0, 0), text, size=SCHRIFT, prop=fp).get_extents().width / 72


def _ohne_static(z):
    return z[len(STATIC):] if z.startswith(STATIC) else z


def masse(name, attribute, methoden):
    """Breite und Höhe eines Kastens in Zoll sowie die Höhen der drei Teile."""
    b = max([_breite(name, True)] + [_breite(_ohne_static(z)) for z in attribute + methoden]) + 2 * RAND + 0.1
    h_name = ZEILE + 2 * RAND
    h_attr = len(attribute) * ZEILE + 2 * RAND
    h_meth = len(methoden) * ZEILE + 2 * RAND
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
            x1 = max(x1, box[von][2] + 0.9)
            y1 = max(y1, box[von][1] + 0.55)
    fig = plt.figure(figsize=(x1 - x0, y1 - y0), dpi=dpi)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(x0, x1)
    ax.set_ylim(y0, y1)
    ax.axis('off')

    def zeile(x, y, z):
        text = _ohne_static(z)
        ax.text(x, y, text, fontsize=SCHRIFT, va='center', family='DejaVu Sans', zorder=3)
        if z.startswith(STATIC):
            ax.plot([x, x + _breite(text)], [y - 0.085, y - 0.085], color='black', linewidth=0.9, zorder=3)

    for n, (attribute, methoden) in klassen.items():
        bx0, by1, bx1, by0 = box[n]
        h_name, h_attr, h_meth = groesse[n][2]
        ax.add_patch(Rectangle((bx0, by0), bx1 - bx0, by1 - by0, facecolor='white', edgecolor='black', linewidth=1.3, zorder=2))
        ax.text((bx0 + bx1) / 2, by1 - h_name / 2, n, fontsize=SCHRIFT, fontweight='bold', ha='center', va='center',
                family='DejaVu Sans', zorder=3)
        y = by1 - h_name
        ax.plot([bx0, bx1], [y, y], color='black', linewidth=1, zorder=3)
        for i, z in enumerate(attribute):
            zeile(bx0 + RAND + 0.05, y - RAND - (i + 0.5) * ZEILE, z)
        y -= h_attr
        ax.plot([bx0, bx1], [y, y], color='black', linewidth=1, zorder=3)
        for i, z in enumerate(methoden):
            zeile(bx0 + RAND + 0.05, y - RAND - (i + 0.5) * ZEILE, z)

    def spitze(p, q, art):
        """Pfeilspitze bei q, Linie kommt von p."""
        if art == 'ungerichtet':
            return
        dx, dy = q[0] - p[0], q[1] - p[1]
        l = (dx * dx + dy * dy) ** 0.5
        ux, uy = dx / l, dy / l
        a, b = (0.2, 0.11) if art == 'vererbung' else (0.16, 0.08)
        links = (q[0] - a * ux - b * uy, q[1] - a * uy + b * ux)
        rechts = (q[0] - a * ux + b * uy, q[1] - a * uy - b * ux)
        if art == 'vererbung':
            ax.add_patch(Polygon([q, links, rechts], closed=True, facecolor='white', edgecolor='black', linewidth=1.2, zorder=4))
        else:
            ax.plot([links[0], q[0], rechts[0]], [links[1], q[1], rechts[1]], color='black', linewidth=1.2, zorder=4)

    def beschriften(p, q, text):
        """Text in der Nähe des Endpunkts q der Linie p -> q."""
        if not text:
            return
        if p[1] == q[1]:  # waagrecht: über der Linie
            rechts = q[0] > p[0]
            ax.text(q[0] - 0.22 if rechts else q[0] + 0.22, q[1] + 0.05, text, fontsize=SCHRIFT - 1,
                    ha='right' if rechts else 'left', va='bottom', family='DejaVu Sans')
        else:  # senkrecht: rechts neben der Linie
            oben = q[1] > p[1]
            ax.text(q[0] + 0.12, q[1] - 0.04 if oben else q[1] + 0.04, text, fontsize=SCHRIFT - 1,
                    va='top' if oben else 'bottom', family='DejaVu Sans')

    for pf in pfeile:
        von, nach, art = pf[0], pf[1], pf[2]
        text_ziel = pf[3] if len(pf) > 3 else ''
        text_start = pf[4] if len(pf) > 4 else ''
        a, b = box[von], box[nach]
        if von == nach:
            xr, yo = a[2], a[1]
            ym = (a[1] + a[3]) / 2
            xm = a[2] - min(0.4, (a[2] - a[0]) / 4)
            pts = [(xr, ym), (xr + 0.4, ym), (xr + 0.4, yo + 0.4), (xm, yo + 0.4), (xm, yo)]
            ax.plot([p[0] for p in pts], [p[1] for p in pts], color='black', linewidth=1.2, zorder=1)
            spitze(pts[-2], pts[-1], art)
            if text_ziel:
                ax.text(xr + 0.48, (ym + yo + 0.4) / 2, text_ziel, fontsize=SCHRIFT - 1, family='DejaVu Sans', va='center')
            continue
        if a[3] >= b[1] or b[3] >= a[1]:  # übereinander (senkrechter Abstand): senkrecht, wenn nötig mit Knick
            a_oben = a[3] >= b[1]  # a liegt über b
            ya = a[3] if a_oben else a[1]
            yb = b[1] if a_oben else b[3]
            lo, hi = max(a[0], b[0]), min(a[2], b[2])
            if hi - lo >= 0.3:  # überlappen waagrecht genug: gerade Linie
                xm = (lo + hi) / 2
                pts = [(xm, ya), (xm, yb)]
            else:  # Knick: von der Mitte von a senkrecht, quer, senkrecht in b
                xa = (a[0] + a[2]) / 2
                xb = min(max(xa, b[0] + 0.3), b[2] - 0.3)
                ym = ya + (yb - ya) * 0.4  # näher an a, damit über b Platz für die Pfeilspitze bleibt
                pts = [(xa, ya), (xa, ym), (xb, ym), (xb, yb)]
        else:  # nebeneinander: waagrecht von Seite zu Seite
            unten, oben = max(a[3], b[3]), min(a[1], b[1])
            ym = (unten + oben) / 2 if unten < oben else (a[1] + a[3]) / 2
            pts = [(a[2], ym) if a[2] <= b[0] else (a[0], ym), (b[0], ym) if a[2] <= b[0] else (b[2], ym)]
        ax.plot([p[0] for p in pts], [p[1] for p in pts], color='black', linewidth=1.2, zorder=1)
        spitze(pts[-2], pts[-1], art)
        beschriften(pts[-2], pts[-1], text_ziel)
        beschriften(pts[1], pts[0], text_start)

    buf = io.BytesIO()
    fig.savefig(buf, format='png', dpi=dpi, metadata={'Software': None})
    plt.close(fig)
    return buf.getvalue()


if __name__ == '__main__':  # Probebild
    import sys
    png = uml_bild({'Konto': (['- inhaber: str', '- kontostand: float', 'static - anzahl: int'],
                              ['+ Konto(inhaber: str)', '+ einzahlen(betrag: float): void', 'static + get_anzahl(): int']),
                    'Person': (['+ name: str', '+ mutter: Person'], ['+ Person(name: str)']),
                    'Sparkonto': (['- zinssatz: float'], ['+ Sparkonto(inhaber: str, zinssatz: float)']),
                    'Bank': (['- konten: list'], ['+ Bank()'])},
                   [('Konto', 'Person', 'assoziation', '1'), ('Person', 'Person', 'assoziation', '0..1'),
                    ('Sparkonto', 'Konto', 'vererbung'), ('Bank', 'Sparkonto', 'ungerichtet', '0..*', '1')],
                   positionen={'Konto': (0, 0), 'Person': (4.4, 0.3), 'Sparkonto': (0, 2.6), 'Bank': (4.4, 2.6)})
    open(sys.argv[1], 'wb').write(png)
