# python-uebungen – Hinweise für Claude

Sammlung großer Python-Übungsnotebooks **zum Selbststudium** für Schülerinnen und Schüler eines Informatikkurses
(Bedingungen, Schleifen, Listen, Strings, Tupel, Sets, Dictionaries, Grids, Funktionen, Dateien, itertools, random).
Jedes Notebook: Abschnitte mit kurzen Erklärungen und ausführbaren Beispielen, danach viele kleine Übungen
(Fingerfertigkeit, Wiederholungen sind gewollt), Lösungen aufklappbar. Inhaltlich orientiert an W3Schools.
Die Notebooks laufen mit **JupyterLite** im Browser: https://ktheu.github.io/python-uebungen/

Sprache: Deutsch, Schüler werden mit „du“ angesprochen.

## Wichtigste Regel: Notebooks werden generiert

Die Notebooks in `content/` werden von den Skripten in `generator/` erzeugt. **Nie die .ipynb direkt bearbeiten**,
sondern das passende `generator/gen_<thema>.py` ändern und neu erzeugen:

```
python generator/gen_listen.py
```

Der Generator führt dabei jedes Beispiel und jede Musterlösung aus und schreibt nur, wenn alles fehlerfrei läuft
(Ausgabe endet mit `PROBLEMS: 0` und `geschrieben: ...`). Die erwarteten Ausgaben in den Aufgaben stammen aus diesen Läufen.
Ein erneuter Lauf ohne Änderung erzeugt eine byte-identische Datei (feste Zell-IDs `zelle-000`, ...).

## Die Repos und wie sie zusammenhängen

Alle liegen unter `C:\MyData\07_Kurse\`.

| Repo | sichtbar | Inhalt |
|---|---|---|
| `python-uebungen` (hier) | öffentlich | Generatoren + die 12 Notebooks, JupyterLite-Seite |
| `Infokurs_Uebungen` | öffentlich | zweite JupyterLite-Seite: Übungen zu den Unterrichtseinheiten (eigene `CLAUDE.md` dort) |
| `InfoKursCC` | **privat** | Unterrichtsstoff `<thema>/inhalte/*.ipynb`, Klausuraufgaben `<thema>/aufgaben/aufgaben.tex` mit `aufgabentex/*.tex` |
| `InfoKursN` | öffentlich | Kursseiten (eigene GitHub-Pages-Seite, Jekyll). `InfoKursN/python_uebungen/inhalte.md` verlinkt die 12 Notebooks hier. |

Früher lagen die Generatoren in `InfoKursCC/python_uebungen/` und wurden mit `copyLite.py` kopiert; das gibt es nicht mehr.

## Aufbau dieses Repos

- `generator/nbgen.py` – Bibliothek zum Bauen und Prüfen der Notebooks
- `generator/gen_<thema>.py` – ein Skript pro Notebook (nur Inhalt)
- `generator/prompt.md` – der ursprüngliche Auftrag für die Sammlung
- `content/<thema>.ipynb` – die erzeugten Notebooks, **flach** (JupyterLite hängt beim Download sonst den Ordnernamen an)
- `.github/workflows/deploy.yml` – baut bei jedem Push auf `main` die Seite aus `content/` und veröffentlicht sie
  (nur `content/` kommt auf die Seite, `generator/` nicht)
- `requirements.txt` – `jupyterlite-core==0.8.6`, `jupyterlite-pyodide-kernel==0.8.6`, `jupyter-server==2.21.1`
- `README.md` – Linktabelle (Direktlink: `https://ktheu.github.io/python-uebungen/notebooks/index.html?path=<thema>.ipynb`)

## Die Generator-API (nbgen.py)

```python
from nbgen import sec, expl, task, predict, generate, setup

sec('Listen erstellen')                       # neuer Abschnitt (## 1. ...)
expl('''#### `len()` ... Erklärung ...''',    # Erklärung (Markdown) + ausführbares Beispiel
     '''print(len([1, 2]))''')
task('Aufgabentext (Markdown)',
     given='zahlen = [1, 2, 3]',              # steht vorgegeben in der Codezelle, danach "# your code"
     solution='zahlen = [1, 2, 3]\nprint(sum(zahlen))',   # muss mit given beginnen (sonst GIVEN MISMATCH)
     kind='normal')                           # 'normal': mit erwarteter Ausgabe | 'free': ohne | 'predict'
predict('''code''', error=None)               # "Was wird ausgegeben?" – Code in der Zelle, keine erwartete Ausgabe,
                                              # keine Lösung zum Aufklappen; error=TypeError usw. für Fehler-Beispiele
setup(md, code)                               # optionale Zelle ganz oben (z. B. Beispieldateien anlegen, siehe gen_dateien.py)
generate('listen', 'Listen')                  # schreibt ../content/listen.ipynb
```

Viele Skripte definieren eine Abkürzung `t(text, given, body, kind)`, bei der die Lösung `given + body` ist.
Aufgaben werden pro Abschnitt automatisch nummeriert (`Aufgabe 3.4`).

Was im Notebook entsteht: Titel + Intro (+ Hinweis zu den aufklappbaren Lösungen), pro Abschnitt Erklärungen mit Beispielzellen,
pro Aufgabe Markdown + Codezelle + `<details>`-Block („Lösung anzeigen“, bei `kind='free'` „Beispiellösung anzeigen“).

## Inhaltliche Regeln

- Nur Code-Aufgaben. Keine Aufforderungen wie „erkläre“, „begründe“, „Was fällt dir auf?“.
- Vorhersage-Aufgaben ohne erwartete Ausgabe und ohne aufklappbare Lösung (die Kontrolle ist das Ausführen).
- Jede benutzte Funktion oder Methode wird im Notebook (oder in einem früheren Notebook der Reihe) kurz erklärt, mit Beispiel.
  Nichts verwenden, was noch nicht erklärt ist (z. B. kein `lambda` vor dem itertools-Notebook, keine Generator-Ausdrücke).
- Fachbegriffe wie im Unterricht: `%` heißt **Modulo-Operator**.
- Bei Themen, die es auch als Unterrichtseinheit gibt (z. B. Bedingungen), nicht mit den Klausuraufgaben in
  `InfoKursCC/<thema>/aufgabentex/` übereinstimmen, auch nicht als Paralleltext mit anderen Zahlen.
- Kein `input()` (Werte als Variablen vorgeben, „Teste auch mit ...“).

## Fallstricke bei erwarteten Ausgaben

- **Sets aus Zeichenketten** werden bei jedem Lauf in anderer Reihenfolge ausgegeben → in Aufgaben mit erwarteter Ausgabe
  immer `sorted(...)` verlangen. Prüfen mit zwei Läufen unter verschiedenem `PYTHONHASHSEED`, ob die Notebooks gleich bleiben.
- **Zufall**: Aufgaben ohne `random.seed()` sind `kind='free'`. Erwartete Ausgabe nur mit festem Seed und genau
  beschriebener Reihenfolge der Aufrufe.
- Kommazahlen: auf saubere Ausgaben achten (z. B. `c * 9 / 5 + 32` statt `c * 1.8 + 32`), sonst Formatangabe `:.2f` verlangen.
- Dateien: `gen_dateien.py` legt die Beispieldateien per `setup()` an; die Prüfung läuft in einem temporären Ordner.
  Immer `encoding='utf-8'` beim Öffnen.

## JupyterLite

- Python im Browser (Pyodide `v314.0.6`, laut Versionsnummer Python 3.14; `itertools.batched` geht). Kein Tkinter/turtle.
- Gespeichert wird im Browser. Wer ein Notebook schon gespeichert hat, sieht spätere Änderungen nicht
  (privates Fenster oder *Help → Clear Browser Data*). Größere Änderungen den Schülern ansagen.

## Arbeitsablauf

1. `generator/gen_<thema>.py` ändern (neues Thema: neues Skript nach dem Muster der vorhandenen).
2. `python generator/gen_<thema>.py` → `PROBLEMS: 0`. Ausgaben der Aufgaben ansehen und auf Plausibilität prüfen.
3. Bei einem neuen Notebook: Zeile in `README.md` und in `InfoKursN/python_uebungen/inhalte.md` ergänzen
   (InfoKursN ist ein eigenes Repo, dort separat committen und pushen).
4. Committen (Generator **und** Notebook) und auf `main` pushen; der Workflow baut die Seite neu (ca. 1 Minute).
   Prüfen mit `gh run list -R ktheu/python-uebungen --limit 1`.
5. Pushes, die `.github/workflows/` ändern, nur mit gh-Zugangsdaten:
   `git -c credential.helper= -c "credential.helper=!gh auth git-credential" push`

Git-Commits auf Deutsch.
