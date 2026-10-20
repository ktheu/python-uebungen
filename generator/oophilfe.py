"""Gemeinsame Abkürzungen für die Generatoren der OOP-Reihe (gen_oop_*.py)."""
from nbgen import task, expl
from umlnb import uml_bild


def t(text, given='', body='', kind='normal', anhaenge=None, error=None):
    """Aufgabe, deren Lösung aus dem vorgegebenen Code plus body besteht."""
    task(text, given=given, solution=(given + '\n' + body) if given else body, kind=kind, anhaenge=anhaenge, error=error)


def diagramm(datei, klassen, pfeile=(), positionen=None):
    """Markdown mit Klassendiagramm und die Anhänge dazu. klassen: {name: (attribute, methoden)}."""
    return (f'\n\n![Klassendiagramm](attachment:{datei})\n\n',
            {datei: uml_bild(klassen, pfeile, positionen)})


def uml(name, attribute, methoden):
    """Diagramm einer einzelnen Klasse."""
    return diagramm(name.lower() + '.png', {name: (attribute, methoden)})


def tu(text, name, attribute, methoden, given='', body='', kind='normal', error=None):
    """Aufgabe mit dem Diagramm einer Klasse unter dem Text."""
    md, anh = uml(name, attribute, methoden)
    t(text + md, given, body, kind, anhaenge=anh, error=error)


def td(text, datei, klassen, pfeile=(), positionen=None, given='', body='', kind='normal'):
    """Aufgabe mit einem Diagramm aus mehreren Klassen."""
    md, anh = diagramm(datei, klassen, pfeile, positionen)
    t(text + md, given, body, kind, anhaenge=anh)


def eu(md, code, name, attribute, methoden, error=None):
    """Erklärung mit dem Diagramm einer Klasse am Ende des Textes."""
    d, anh = uml(name, attribute, methoden)
    expl(md + d, code, anhaenge=anh, error=error)


def ed(md, code, datei, klassen, pfeile=(), positionen=None, error=None):
    """Erklärung mit einem Diagramm aus mehreren Klassen."""
    d, anh = diagramm(datei, klassen, pfeile, positionen)
    expl(md + d, code, anhaenge=anh, error=error)
