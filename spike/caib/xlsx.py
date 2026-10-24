# Lector XLSX stdlib compartido por los scripts de la spike (sin dependencias). read_xlsx(ruta) -> {hoja: filas}
# Las celdas numéricas salen como float; el texto, como str.
import zipfile, re
import xml.etree.ElementTree as ET
NS = {'m': 'http://schemas.openxmlformats.org/spreadsheetml/2006/main',
      'r': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships'}
def read_xlsx(path):
    z = zipfile.ZipFile(path); ss = []
    if 'xl/sharedStrings.xml' in z.namelist():
        for si in ET.fromstring(z.read('xl/sharedStrings.xml')).findall('m:si', NS):
            ss.append(''.join(t.text or '' for t in si.iter('{%s}t' % NS['m'])))
    wb = ET.fromstring(z.read('xl/workbook.xml'))
    rels = {r.get('Id'): r.get('Target') for r in ET.fromstring(z.read('xl/_rels/workbook.xml.rels'))}
    out = {}
    for sh in wb.find('m:sheets', NS):
        t = rels[sh.get('{%s}id' % NS['r'])].lstrip('/')
        t = t if t.startswith('xl/') else 'xl/' + t
        rows = []
        for row in ET.fromstring(z.read(t)).findall('.//m:sheetData/m:row', NS):
            vals = {}
            for c in row.findall('m:c', NS):
                v = c.find('m:v', NS); ty = c.get('t')
                if ty == 's' and v is not None: val = ss[int(v.text)]
                elif ty == 'inlineStr': val = ''.join(x.text or '' for x in c.iter('{%s}t' % NS['m']))
                else:
                    val = v.text if v is not None else ''
                    try: val = float(val)
                    except (TypeError, ValueError): pass
                n = 0
                for ch in re.match(r'[A-Z]+', c.get('r')).group(0): n = n * 26 + ord(ch) - 64
                vals[n - 1] = val
            rows.append([vals.get(i, '') for i in range(max(vals) + 1)] if vals else [])
        out[sh.get('name')] = rows
    return out
