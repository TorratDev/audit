# Spike desechable: suma "Crèdit ordenat" (obligaciones reconocidas) por capítulo desde el dataset abierto PPP_DSP_2002-2024_LIQ. Uso: python -I check_opendata.py <ppp_dsp_liq.xlsx> <año>
import sys, os
from collections import defaultdict
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from xlsx import read_xlsx
rows = list(read_xlsx(sys.argv[1]).values())[0]
year = float(sys.argv[2])
cab = rows[0]
def col(nombre):
    if nombre not in cab: raise ValueError(f'no encuentro la columna "{nombre}"')
    return cab.index(nombre)
C_ANO, C_SECTOR, C_CONS, C_CAP, C_OBL = col('Exercici'), col('Sector'), col('Consolida'), col('Capítol'), col("Crèdit ordenat")
by = defaultdict(float); byc = defaultdict(lambda: defaultdict(float)); cons = defaultdict(lambda: defaultdict(float))
for r in rows[1:]:
    if not r or r[C_ANO] != year: continue
    v = r[C_OBL] if C_OBL < len(r) else ''
    if v == '': v = 0.0
    if not isinstance(v, float): raise ValueError(f'importe no numérico: {v!r} en fila {r[:4]}')
    cap = str(r[C_CAP])[:1] if r[C_CAP] else '?'
    by[cap] += v; byc[r[C_SECTOR]][cap] += v; cons[r[C_CONS]][cap] += v
print('Capítulos totales (todas las filas de la hoja, Crèdit ordenat):')
for k in sorted(by): print(f'  {k} {by[k]:,.2f}')
print('Total', f'{sum(by.values()):,.2f}')
print('Por sector (suma capítulos):', {s: round(sum(v.values()), 2) for s, v in byc.items()})
print('Valores de "Consolida":', {k: round(sum(v.values()), 2) for k, v in cons.items()})
