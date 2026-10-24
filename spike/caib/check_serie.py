# Spike desechable: compara la fila "Desembre" del año (serie mensual acumulada, miles de €) con los capítulos consolidados de la liquidación (€). Uso: python -I check_serie.py <dir_liq> <dir_exec> <año>
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from xlsx import read_xlsx
from check_capitols import capitulos
def columna(cab, nombre, desde):
    """Índice de la columna con ese nombre a partir de 'desde' (hay nombres repetidos: 'Transf. Corrents')."""
    for j in range(desde, len(cab)):
        if cab[j] == nombre:
            return j
    raise ValueError(f'no encuentro la columna "{nombre}" en la cabecera')
liq_dir, exec_dir, year = sys.argv[1], sys.argv[2], sys.argv[3]
ser = list(read_xlsx(os.path.join(exec_dir, 'Serie_d_ingressos_i_despeses_2010-2026.xlsx')).values())[0]
cab = ser[6]                    # fila con los nombres de columna
gc = columna(ser[5], 'DESPESES CORRENTS', 0)   # cabecera de grupo
gk = columna(ser[5], 'DESPESES DE CAPITAL', gc)
cols = {'1': columna(cab, 'Despeses de personal', gc), '2': columna(cab, 'Despeses corr. bens', gc),
        '3': columna(cab, 'Despeses financeres', gc), '4': columna(cab, 'Transf. Corrents', gc),
        '6': columna(cab, 'Inversions reals', gk), '7': columna(cab, 'Transf. de capital', gk)}
i = next(k for k, r in enumerate(ser) if r and r[0] == float(year))
dec = next(r for r in ser[i:] if r and isinstance(r[0], str) and r[0].startswith('Desembre'))
print(f'{year} fila: {dec[0]}')
liq = list(read_xlsx(os.path.join(liq_dir, 'CAIB_ECO_G_202312_ca.xlsx')).values())[0]
chap = {k[0]: v for k, v in capitulos(liq).items()}
for k, j in cols.items():
    if not isinstance(dec[j], float): raise ValueError(f'serie no numérica en capítulo {k}: {dec[j]!r}')
    diff = dec[j] * 1000 - chap[k]
    print(f'ch{k}: liquidacion={chap[k]:,.2f}  serie={dec[j]*1000:,.2f}  dif={diff:,.2f}')
