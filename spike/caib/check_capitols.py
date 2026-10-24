# Spike desechable: suma obligaciones reconocidas por capítulo (1-9) y compara con el total de la hoja PMP publicada. Uso: python -I check_capitols.py <dir_liq> <año>
import sys, os, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from xlsx import read_xlsx
def capitulos(filas):
    """Suma la columna B (Consolidat) de las filas 'N.- ...'. Falla si una cifra no es número."""
    chap = {}
    for r in filas:
        if len(r) > 1 and isinstance(r[0], str) and re.match(r'^[1-9]\.- ', r[0]):
            if not isinstance(r[1], float):
                raise ValueError(f'valor no numérico en "{r[0]}": {r[1]!r}')
            chap[r[0][:2]] = chap.get(r[0][:2], 0) + r[1]
    return chap
if __name__ == '__main__':
    d = sys.argv[1]
    eco = list(read_xlsx(os.path.join(d, 'CAIB_ECO_G_202312_ca.xlsx')).values())[0]  # ojo: el 2024 viene con nombre _202312
    chap = capitulos(eco)
    print('Capítulos (Consolidat, col B):')
    for k in sorted(chap): print(f'  {k} {chap[k]:,.2f}')
    print(f'Suma capítulos 1-9 consolidado: {sum(chap.values()):,.2f}')
    pmp = list(read_xlsx(os.path.join(d, 'CAIB_PMP_202412_ca.xlsx')).values())[0]
    for r in pmp:
        if r and isinstance(r[0], str) and r[0].startswith('Total despeses'):
            print(f'PMP {r[0]}: consolidado={r[1]:,.2f}')
