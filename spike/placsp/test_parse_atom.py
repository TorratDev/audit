# Pruebas mínimas: python -I test_parse_atom.py  (sale con error si algo falla)
import os, subprocess, sys, tempfile, csv
HERE = os.path.dirname(os.path.abspath(__file__))
def atom(entries):
    body = ''.join(f'''<entry xmlns="http://www.w3.org/2005/Atom" xmlns:cac-place-ext="x" xmlns:cac="x" xmlns:cbc="x">
<id>{i}</id><updated>{u}</updated><title>{t}</title>
<cac-place-ext:ContractFolderStatus><cbc:ContractFolderID>{t}</cbc:ContractFolderID></cac-place-ext:ContractFolderStatus></entry>''' for i, u, t in entries)
    return f'<?xml version="1.0" encoding="UTF-8"?><feed xmlns="http://www.w3.org/2005/Atom">{body}</feed>'
def run(files):
    d = tempfile.mkdtemp(); out = os.path.join(d, 'out.csv')
    for name, text in files.items():
        open(os.path.join(d, name), 'w', encoding='utf-8').write(text)
    p = subprocess.run([sys.executable, '-I', os.path.join(HERE, 'parse_atom.py'), d, out], capture_output=True, text=True)
    rows = list(csv.DictReader(open(out, encoding='utf-8'))) if p.returncode == 0 else None
    return p.returncode, rows
# 1) misma licitación en dos zonas horarias: gana la más tardía en UTC (01:10 UTC, no 00:30)
code, rows = run({'a.atom': atom([('X', '2026-10-25T02:30:00+02:00', 'vieja')]),
                  'b.atom': atom([('X', '2026-10-25T02:10:00+01:00', 'nueva')])})
assert code == 0 and [r['titulo'] for r in rows] == ['nueva'], (code, rows)
# 2) fichero roto: error, no CSV con filas perdidas
code, rows = run({'a.atom': atom([('Y', '2026-01-01T00:00:00+01:00', 'ok')]), 'b.atom': '<feed><entry>'})
assert code != 0 and rows is None
# 3) carpeta sin .atom: error
code, rows = run({})
assert code != 0
print('ok: 3 pruebas pasan')
