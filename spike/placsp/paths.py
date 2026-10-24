# Lista las rutas de etiquetas (sin valores) de una entrada Atom PLACSP. Uso: python -I paths.py <fichero.atom>
import sys, xml.etree.ElementTree as ET, collections
def walk(el, prefix, out):
    tag = el.tag.split('}')[-1]
    p = prefix + '/' + tag
    if el.attrib.get('schemeName'):
        p += '[' + el.attrib['schemeName'] + ']'
    if len(el) == 0:
        out[p] += 1
    for c in el:
        walk(c, p, out)
root = ET.parse(sys.argv[1]).getroot()
out = collections.Counter()
for e in root.iter('{http://www.w3.org/2005/Atom}entry'):
    for c in e:
        walk(c, '', out)
for k, v in sorted(out.items()):
    print(v, k)
