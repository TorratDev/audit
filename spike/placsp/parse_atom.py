# Lee todos los .atom de un directorio (PLACSP sindicación), deduplica por <id> (gana el <updated> más reciente)
# y vuelca un CSV con campos clave. Uso: python -I parse_atom.py <dir> <salida.csv>
# Falla con error si un fichero no se puede leer: nunca descarta filas en silencio.
import sys, os, csv, glob, datetime, xml.etree.ElementTree as ET
A = '{http://www.w3.org/2005/Atom}'
OLDEST = datetime.datetime.min.replace(tzinfo=datetime.timezone.utc)
def first(e, path):
    parts = path.split('/')
    cur = [e]
    for t in parts:
        nxt = []
        for c in cur:
            for x in c:
                if x.tag.split('}')[-1] == t:
                    nxt.append(x)
        cur = nxt
    return (cur[0].text or '').strip() if cur and cur[0].text else ''
def allvals(e, path):
    parts = path.split('/')
    cur = [e]
    for t in parts:
        cur = [x for c in cur for x in c if x.tag.split('}')[-1] == t]
    return [((x.text or '').strip(), x.attrib.get('schemeName', '')) for x in cur]
def entry_row(en):
    cfs = None
    for c in en:
        if c.tag.split('}')[-1] == 'ContractFolderStatus':
            cfs = c
    if cfs is None:
        return None
    ident = first(en, 'id')
    row = {
        'id': ident,
        'updated': first(en, 'updated'),
        'expediente': first(cfs, 'ContractFolderID'),
        'estado': first(cfs, 'ContractFolderStatusCode'),
        'titulo': first(en, 'title'),
        'link': next((x.attrib.get('href', '') for x in en if x.tag == A + 'link'), ''),
        'resumen': first(en, 'summary'),
        'organo': first(cfs, 'LocatedContractingParty/Party/PartyName/Name'),
        'nif_organo': '', 'dir3_organo': '', 'id_plataforma': first(cfs, 'LocatedContractingParty/Party/PartyIdentification/ID'),
        'perfil': first(cfs, 'LocatedContractingParty/BuyerProfileURIID'),
        'tipo_contrato': first(cfs, 'ProcurementProject/TypeCode'),
        'subtipo': first(cfs, 'ProcurementProject/SubTypeCode'),
        'procedimiento': first(cfs, 'TenderingProcess/ProcedureCode'),
        'cpv': '', 'importe_sin_iva': first(cfs, 'ProcurementProject/BudgetAmount/TaxExclusiveAmount'),
        'importe_con_iva': first(cfs, 'ProcurementProject/BudgetAmount/TotalAmount'),
        'adjudicatario': first(cfs, 'TenderResult/WinningParty/PartyName/Name'),
        'nif_adjudicatario': '',
        'importe_adj_sin_iva': first(cfs, 'TenderResult/AwardedTenderedProject/LegalMonetaryTotal/TaxExclusiveAmount'),
        'importe_adj_con_iva': first(cfs, 'TenderResult/AwardedTenderedProject/LegalMonetaryTotal/PayableAmount'),
        'fecha_adjudicacion': first(cfs, 'TenderResult/AwardDate'),
        'fecha_formalizacion': first(cfs, 'TenderResult/Contract/IssueDate'),
        'resultado': first(cfs, 'TenderResult/ResultCode'),
        'n_lotes': str(len(list(x for x in cfs if x.tag.split('}')[-1] == 'ProcurementProjectLot'))),
    }
    # identificadores del órgano (nivel Party, no ParentLocatedParty)
    ids = allvals(cfs, 'LocatedContractingParty/Party/PartyIdentification/ID')
    row['dir3_organo'] = next((v for v, s in ids if s == 'DIR3'), '')
    row['nif_organo'] = next((v for v, s in ids if s == 'NIF'), '')
    # CPV: primer ItemClassificationCode del proyecto principal
    cpvs = allvals(cfs, 'ProcurementProject/RequiredCommodityClassification/ItemClassificationCode')
    row['cpv'] = cpvs[0][0] if cpvs else ''
    nifs = allvals(cfs, 'TenderResult/WinningParty/PartyIdentification/ID')
    row['nif_adjudicatario'] = next((v for v, s in nifs if s == 'NIF'), '')
    return row
def updated_utc(u):
    # como texto falla: 00:30+02:00 parece posterior a 01:10+01:00 aunque sea antes en UTC
    return datetime.datetime.fromisoformat(u).astimezone(datetime.timezone.utc) if u else OLDEST
def main(d, out):
    files = sorted(glob.glob(os.path.join(d, '*.atom')))
    if not files:
        sys.exit(f'error: no hay ficheros .atom en {d}')
    best = {}
    n_raw = 0
    for f in files:
        try:
            root = ET.parse(f).getroot()
        except ET.ParseError as ex:
            sys.exit(f'error: {os.path.basename(f)} no se puede leer ({ex}); no se escribe CSV')
        for en in root.iter(A + 'entry'):
            n_raw += 1
            r = entry_row(en)
            if r is None: continue
            k = r['id']
            if k not in best or updated_utc(r['updated']) > updated_utc(best[k]['updated']):
                best[k] = r
    if not best:
        sys.exit(f'error: ninguna entrada con ContractFolderStatus en {d}')
    cols = list(next(iter(best.values())).keys())
    with open(out, 'w', newline='', encoding='utf-8') as fh:
        w = csv.DictWriter(fh, fieldnames=cols); w.writeheader()
        for r in best.values(): w.writerow(r)
    print(f'archivos={len(files)} entradas_brutas={n_raw} entradas_unicas={len(best)} -> {out}')
if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
