# Vuelca las primeras filas de cada hoja de un .xlsx. Uso: python -I xlsx_dump.py fichero.xlsx [max_filas]
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from xlsx import read_xlsx
n = int(sys.argv[2]) if len(sys.argv) > 2 else 15
for hoja, filas in read_xlsx(sys.argv[1]).items():
    print(f'=== hoja "{hoja}" filas={len(filas)}')
    for f in filas[:n]:
        print(' | '.join('' if v == '' else str(v) for v in f))
