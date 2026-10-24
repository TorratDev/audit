#!/usr/bin/env bash
# Spike #9: verifica la API publica de BDNS (sin autenticacion).
# Uso: OUT=<dir_scratch> ./probe_bdns.sh      (no guarda datos en el repo)
# Requiere: bash, curl, python3. Tarda varios minutos (el servicio es lento).
set -u
B="https://www.infosubvenciones.es/bdnstrans"
API="$B/api"
OUT="${OUT:-./bdns_raw}"
mkdir -p "$OUT"
# Ruta en formato Windows (C:/...) para que python nativo la pueda abrir desde Git Bash
OUT="$(cd "$OUT" && (pwd -W 2>/dev/null || pwd))"
PAUSE="${PAUSE:-0.2}"   # pausa entre peticiones secuenciales (no es un limite confirmado)

# get NOMBRE RUTA_CON_QUERY -> guarda $OUT/NOMBRE.json, reintenta si el servicio esta en mantenimiento o no responde
get() {
  local name="$1" path="$2" try code
  for try in 1 2 3; do
    code=$(curl -s --max-time 60 -o "$OUT/$name.json" -w "%{http_code}" "$path")
    case "$code" in 000|5*) ;; *) [ "$code" = 200 ] || break ;; esac   # 4xx son respuestas validas (control), no se reintentan
    if [ "$code" = "200" ] && ! grep -q ERR_MANTENIMIENTO_BBDD "$OUT/$name.json"; then break; fi
    echo "  [aviso] $name intento $try: HTTP $code, reintentando" >&2
    sleep 10
  done
  printf '%-28s HTTP %s' "$name" "$code"
  python3 - "$OUT/$name.json" <<'PY'
import json, sys
p = sys.argv[1]
try:
    d = json.load(open(p, encoding="utf-8"))
except Exception:
    print("  (no JSON)"); sys.exit()
if isinstance(d, dict) and "content" in d:
    print(f"  totalElements={d.get('totalElements')} numberOfElements={d.get('numberOfElements')} last={d.get('last')}")
elif isinstance(d, dict):
    print("  " + json.dumps(d, ensure_ascii=False)[:160])
else:
    print(f"  lista de {len(d)} elementos")
PY
  sleep "$PAUSE"
}

echo "== 1. Documentacion Swagger"
for p in doc/swagger doc/swagger/index.html doc/swagger/swagger-ui-init.js v3/api-docs v2/api-docs openapi.json; do
  printf '%-40s %s
' "$B/$p" "$(curl -s --max-time 30 -o /dev/null -w 'HTTP %{http_code} %{content_type}' "$B/$p")"
done

echo "== 2. Organos (arbol) con vpd=GE; idAdmon: A=Autonomica, L=Local, C=Central, O=Otros"
for t in A L C O; do get "organos_$t" "$API/organos?idAdmon=$t&vpd=GE"; done
python3 - "$OUT" <<'PY'
import json, sys, os
out = sys.argv[1]
def sub(n):
    yield n
    for c in n.get("children") or []:
        yield from sub(c)
def leaves(n):
    return sorted({x["id"] for x in sub(n) if not x.get("children")})
def find(tree, pred):
    res = []
    def walk(n):
        if pred(n): res.append(n)
        for c in n.get("children") or []: walk(c)
    for n in tree: walk(n)
    return res
A = json.load(open(f"{out}/organos_A.json", encoding="utf-8"))
L = json.load(open(f"{out}/organos_L.json", encoding="utf-8"))
# Los ids de los nodos agrupadores no son unicos entre niveles: se elige por id Y posicion.
caib = [n for n in A if n.get("id") == 15 and n.get("descripcion", "").upper().endswith("ILLES BALEARS")]
ib = [n for n in L if n.get("id") == 40]          # "ILLES BALEARS / ISLAS BALEARES"
palma = [c for c in (ib[0].get("children") or []) if c.get("id") == 15] if ib else []
alcudia = [c for c in (ib[0].get("children") or []) if c.get("id") == 1372] if ib else []
sets = {"CAIB": caib, "PALMA": palma, "ALCUDIA": alcudia}
result = {}
for k, nodes in sets.items():
    ids = sorted({i for n in nodes for i in leaves(n)})
    result[k] = ids
    print(f"  {k}: nodos={[ (n['id'], n['descripcion']) for n in nodes]} hojas={len(ids)}")
json.dump(result, open(f"{out}/organ_leaves.json", "w"))
PY
IDS_CAIB=$(python3 -c "import json;print(','.join(map(str,json.load(open('$OUT/organ_leaves.json'))['CAIB'])))")
IDS_PALMA=$(python3 -c "import json;print(','.join(map(str,json.load(open('$OUT/organ_leaves.json'))['PALMA'])))")
IDS_ALC=$(python3 -c "import json;print(','.join(map(str,json.load(open('$OUT/organ_leaves.json'))['ALCUDIA'])))")

echo "== 3. Concesiones por organo (filtro organos= con ids HOJA)"
get concesiones_caib   "$API/concesiones/busqueda?vpd=GE&organos=$IDS_CAIB&page=0&pageSize=10"
get concesiones_alcudia "$API/concesiones/busqueda?vpd=GE&organos=$IDS_ALC&page=0&pageSize=10"
echo "   control: organos=15 (id de agrupador, no de organismo) devuelve otro organismo:"
get control_organo15   "$API/concesiones/busqueda?vpd=GE&organos=15&page=0&pageSize=2"

echo "== 4. Paginacion completa (Palma, pageSize=1000): pide paginas hasta last=true"
p=0
while :; do
  get "concesiones_palma_p$p" "$API/concesiones/busqueda?vpd=GE&organos=$IDS_PALMA&page=$p&pageSize=1000"
  last=$(python3 -c "import json,sys; print(json.load(open(sys.argv[1], encoding='utf-8')).get('last', True))" "$OUT/concesiones_palma_p$p.json" 2>/dev/null || echo True)
  [ "$last" = "True" ] && break
  p=$((p+1))
  [ "$p" -lt 100 ] || { echo "  error: mas de 100 paginas" >&2; exit 1; }
done
python3 - "$OUT" <<'PY' || { echo "  error: paginas incompletas o duplicadas" >&2; exit 1; }
import json, sys, glob
out = sys.argv[1]
ids, total = [], None
files = sorted(glob.glob(f"{out}/concesiones_palma_p*.json"))
for f in files:
    d = json.load(open(f, encoding="utf-8"))   # si no es JSON, falla aqui
    ids += [c["id"] for c in d["content"]]
    total = d["totalElements"]
print(f"  paginas={len(files)} filas leidas={len(ids)} unicas={len(set(ids))} totalElements={total}")
if len(set(ids)) != total:
    sys.exit(1)
PY
get tope_pageSize_20000 "$API/concesiones/busqueda?vpd=GE&page=0&pageSize=20000"

echo "== 5. Beneficiario: NIF -> idPersona (terceros) -> concesiones"
get terceros_G07203573 "$API/terceros?busqueda=G07203573"
ID=$(python3 -c "import json;print(json.load(open('$OUT/terceros_G07203573.json'))['terceros'][0]['id'])" 2>/dev/null || echo "")
if [ -n "$ID" ]; then get concesiones_beneficiario "$API/concesiones/busqueda?vpd=GE&beneficiario=$ID&page=0&pageSize=50"; fi
get control_beneficiario_nif "$API/concesiones/busqueda?vpd=GE&beneficiario=G07203573&page=0&pageSize=1"
get control_numeroIdentificacion "$API/concesiones/busqueda?vpd=GE&numeroIdentificacion=G07203573&page=0&pageSize=1"

echo "== 6. Fechas: DD/MM/YYYY (valido) frente a ISO (rechazado)"
get fecha_concesion_ddmmyyyy "$API/concesiones/busqueda?vpd=GE&fechaDesde=01/10/2026&fechaHasta=24/10/2026&page=0&pageSize=1"
get fecha_registro_ddmmyyyy  "$API/concesiones/busqueda?vpd=GE&fechaRegInicio=01/10/2026&fechaRegFin=24/10/2026&page=0&pageSize=1"
get control_fecha_iso        "$API/concesiones/busqueda?vpd=GE&fechaDesde=2026-10-01&fechaHasta=2026-10-24&page=0&pageSize=1"

echo "== 7. Otros endpoints de busqueda"
get convocatorias_busqueda "$API/convocatorias/busqueda?vpd=GE&page=0&pageSize=1"
get minimis_busqueda       "$API/minimis/busqueda?vpd=GE&page=0&pageSize=1"
get ayudasestado_busqueda  "$API/ayudasestado/busqueda?vpd=GE&page=0&pageSize=1"
get grandesbenef_busqueda  "$API/grandesbeneficiarios/busqueda?vpd=GE&page=0&pageSize=1"
get organos_codigo_ejemplo "$API/organos/codigo?vpd=GE&codigo=A04003003"

echo "== 8. Rafaga: 20 peticiones en paralelo (10 a la vez), solo para observar 429"
seq 1 20 | xargs -P 10 -I{} sh -c "curl -s --max-time 60 -o /dev/null -w '%{http_code}\n' '$API/concesiones/busqueda?vpd=GE&page={}&pageSize=1'" | sort | uniq -c
echo "Hecho. Respuestas guardadas en $OUT"
