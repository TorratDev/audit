#!/usr/bin/env bash
# Spike desechable: descarga los ficheros de liquidación, presupuesto y ejecución mensual de la CAIB.
# No necesita cookies ni sesión: archivopub.do redirige (302) a /sites/estadistiques/f/<id>, y el parámetro ctrl se ignora.
# Uso: fetch_caib.sh <dir_salida> <slug_liquidacion> <slug_presupuesto> <slug_ejecucion>
# Ej.:  fetch_caib.sh ./dl 2024_0 2024_p execucia_pressupost_2010-2026
set -u
OUT=$1; LIQ=$2; PRES=$3; EXEC=$4
B=https://www.caib.es/sites/estadistiques/ca
get_page() { # $1 = slug de la página del portal, $2 = carpeta destino
  mkdir -p "$2"
  curl -sL -m 60 "$B/$1/" | sed 's/\r//g' \
    | sed -n 's/.*archivopub\.do?ctrl=\(MCRST[0-9A-Z]*\)&amp;id=\([0-9]*\).*/\1 \2/p' | sort -u \
    | while read -r ctrl id; do
        (cd "$2" && curl -sL -m 120 -OJ "$B/archivopub.do?ctrl=$ctrl&id=$id") || echo "fallo: $id" >&2
      done
}
get_page "$LIQ" "$OUT/liquidacion"
get_page "$PRES" "$OUT/presupuesto"
get_page "$EXEC" "$OUT/ejecucion"
n=$(find "$OUT" -type f | wc -l)
[ "$n" -gt 0 ] || { echo "error: no se descargo ningun fichero (¿cambio la web?)" >&2; exit 1; }
echo "ficheros descargados: $n"
ls -R "$OUT" | head -100
