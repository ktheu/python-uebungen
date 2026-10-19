// Startet Pyodide, lädt die importierten Pakete und führt inner.py mit den Zellen aus der JSON-Datei aus.
// Aufruf über pruefen.py:  node check.mjs zellen.json
import { loadPyodide } from 'pyodide';
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const hier = path.dirname(fileURLToPath(import.meta.url));
const zellen = fs.readFileSync(process.argv[2], 'utf-8');
const py = await loadPyodide();
const alleCodes = JSON.parse(zellen).map(z => z.code).join('\n');
await py.loadPackagesFromImports(alleCodes, { messageCallback: () => {} });
py.globals.set('zellen_json', zellen);
py.runPython(fs.readFileSync(path.join(hier, 'inner.py'), 'utf-8'));
console.log(py.globals.get('ergebnis'));
