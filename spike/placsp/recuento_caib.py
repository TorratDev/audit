# Compara contratos menores CAIB: CSV del portal de transparencia vs filas PLACSP (sindicación mensual).
# Uso: python -I recuento_caib.py <caib_menores.csv> <menores_AAAAMM.csv> [<menores_AAAAMM.csv> ...]
# Los CSV de PLACSP los genera parse_atom.py. Cruce por número de expediente (no hay ID común).
import sys, csv, collections
caib = list(csv.DictReader(open(sys.argv[1], encoding='utf-8-sig'), delimiter=';'))
placsp = {}
for f in sys.argv[2:]:
    for r in csv.DictReader(open(f, encoding='utf-8')):
        # órganos CAIB: DIR3 A04*, o NIF de los que no traen DIR3 (ABAQUA, Q0700507G)
        if r['dir3_organo'].startswith('A04') or r['nif_organo'] == 'Q0700507G':
            placsp.setdefault(r['expediente'].strip(), r)
print('CAIB portal filas:', len(caib), '| PLACSP CAIB expedientes distintos:', len(placsp))
for mes in sorted(set(r['DATA DARRER ANUNCI PLATAFORMA'][3:10] for r in caib)):
    exps = set(r['EXPEDIENT'].strip() for r in caib if r['DATA DARRER ANUNCI PLATAFORMA'][3:10] == mes)
    print(f'mes {mes}: portal={len(exps)} exp. encontrados en PLACSP={len(exps & set(placsp))}')
print('solo en PLACSP (no en portal):', len(set(placsp) - set(r['EXPEDIENT'].strip() for r in caib)))
