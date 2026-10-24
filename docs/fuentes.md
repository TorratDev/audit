# Fuentes de datos: inventario (Fase 0)

Entregable de la épica #2 (sub-issues #6, #7, #8, #9). Verificado el 2026-10-24.

## Resumen de decisiones

| Fuente | Issue | Estado | Decisión |
|---|---|---|---|
| CAIB: presupuesto, liquidación y ejecución | #6 | Confirmada | Descarga HTTP directa de XLSX por entidad y clasificación (ejercicio 2024 cuadra al céntimo con el PMP publicado). Ejecución mensual en serie XLSX 2010-2026. Pendiente: discrepancia GSAI (39 M€) |
| PLACSP: contratos y contratos menores | #7 | Confirmada | Feed Atom de contratos menores de PLACSP como fuente de v1. El CSV del portal CAIB, como validación. Palma sin menores localizados (pendiente) |
| Palma y Alcúdia | #8 | Parcial | Palma: ejecución trimestral XLSX y perímetro de consolidación D004. Alcúdia: fichas PDF trimestrales de ejecución 2025–2026 y liquidación 2024 en su portal de transparencia; contratos menores solo hasta 2023 |
| CONPREL | #8, #11 | Confirmada | Fuente principal de presupuesto y liquidación municipal (definitivos 2002-2025 y avance 2025-2026) |
| BDNS | #9 | Confirmada (sin especificación oficial) | API JSON del portal (`/bdnstrans/api/concesiones/busqueda`), sin autenticación. Corrige dos datos del issue: no existe `numeroIdentificacion` y el límite de 10 req/s no se reproduce |

## Criterios de cierre de la épica (#2)

- [x] Cada fuente de la tabla del plan (#1) queda confirmada o descartada con motivo. Descartes: datos.gob.es de CONPREL para años recientes; IBESTAT JSON-stat (es de consells insulars, no de la CAIB); web services BDNS 2.0 (solo para remitir datos).
- [x] Decisión documentada sobre contratos menores (PLACSP feed) y sobre la vía de acceso a BDNS (API del portal).
- [~] Lista de órganos y sus identificadores (DIR3, código INE, NIF). Parcial: códigos INE confirmados (Palma 07040, Alcúdia 07003); DIR3 y NIF observados en los feeds de PLACSP y en el árbol de BDNS, pero el catálogo DIR3 completo no se ha consultado y varios NIF de sociedades de Palma siguen sin verificar.

## Pendiente antes de dar la épica por cerrada

- Ficheros de ejemplo en una Release `spike-caib` (acción pública: no realizada, requiere confirmación).
- Licencia exacta de reutilización de PLACSP, BDNS y el portal CAIB (no localizada en las páginas revisadas).
- Palma: publica muy pocos contratos menores en PLACSP (31 entradas en 2019, 8 en 2024). Sus menores están en el XLSX trimestral (~3.000 filas al año), que pasa a ser la fuente de Palma; sin NIF, así que el cruce con entidades será por nombre.
- Palma: NIF de EMAYA, EFM, SMAP, PMH-RIBA, PMEI; confirmar el perímetro en registro.

---

## CAIB — Presupuesto, liquidación y ejecución

Ficha de inventario (issue #6, epic #2). Ejercicio de referencia: 2024 (cerrado). Verificado el 2026-10-24.

### URL de acceso y documentación

- Portal de estadísticas: https://www.caib.es/sites/estadistiques/ca/estadistiques-68815 (ejecución del ejercicio corriente). Mapa: https://www.caib.es/sites/estadistiques/ca/mapa/
- Páginas por ejercicio (slugs irregulares, no hay patrón fiable):
  - Presupuesto: `/ca/2024_p/`, `/ca/2025_p/`, `/ca/2026_p/` (prórroga)…
  - Liquidación: `/ca/2024_0/`, `/ca/2023_0_0/`, `/ca/2019p/`, `/ca/liquidacio_2018/`, `/ca/2013-70783/` (con sufijo de id en algunos años)…
  - Ejecución mensual 2010-2026: `/ca/execucia_pressupost_2010-2026/`
  - Series: `/ca/evolucio_de_la_liquidacio_2002-2024/` (descargada: ficheros `CONSOLIDAT_`, `AGIB_`, `ATIB_`, `SSIB_2002-2024_*`) y `/ca/evolucio_del_pressupost_-2020-2025/` (no descargada).
- Descarga: `/ca/archivopub.do?ctrl=<token>&id=<id>` redirige (302) a `https://www.caib.es/sites/estadistiques/f/<id>`. La URL estable es la de `/f/<id>`. Ver `spike/caib/fetch_caib.sh`.
- Portal de transparencia (mismo contenido, sin ficheros propios): https://caib.es/sites/transparencia/ca/liquidacia_execucia_i_evolucia/
- Dataset abierto (CKAN, `intranet.caib.es/opendatacataleg`):
  - "Partides Pressuposts Liquidats Despeses Comunitat Autònoma de les Illes Balears": XLSX, 2002-2024, 33 MB. URL: `.../resource/df3ddac7-b025-4e0d-abd1-21cc9eb70a3a/download/ppp_dsp_liq.xlsx`. Es la fuente más completa (ver granularidad).
  - "Partides Pressupost Inicial Despeses 2024-2025 …": CSV (UTF-8, CRLF, separador coma).
  - Catálogo IBESTAT (PCAXIS / JSON / JSON-stat): "Liquidación presupuesto por Consejo Insular…" es de los consells insulars, no de la CAIB. Descartado para esta ficha.

### Formato y codificación

- Liquidación 2024 y presupuesto 2024: un XLSX por entidad × tipo de clasificación (≈28-29 ficheros por año; hay además un PNG de cabecera, ignorable).
  - Liquidación: `{CAIB|AGIB|ATIB|SSIB}_{ECO|ORG|FUN|PPP|PMP|EFT}_{G|I}_{AAAAMM}_ca.xlsx`. `G` = gastos, `I` = ingresos. `PMP` = principales magnitudes. `EFT` = estructura de financiación.
  - Presupuesto: `AGCAIB_2024_{D|I}_…`, `ATIB_2024_…`, `SSIB_2024_…`, `CONSOLIDAT_2024_…`. `D` = despeses, `I` = ingressos.
  - Hojas con cabeceras en varias filas. Importes en **euros** con decimales.
- Serie mensual de ejecución (`Serie_d_ingressos_i_despeses_2010-2026.xlsx`): una hoja, una fila por periodo, bloques anuales. Importes en **miles de euros** (cabecera "Unitat: Milers d'euros"). Valores **acumulados** dentro del año.
- Dataset abierto `ppp_dsp_liq.xlsx`: una hoja `PPP_DSP_2002-2024_LIQ`, 176.388 filas × 40 columnas, euros, una fila por partida presupuestaria.
- Codificación: texto UTF-8 dentro del XLSX (acentos catalanes). En consola de Windows aparece mal; hay que forzar salida UTF-8 para inspeccionarlo.

### Granularidad y entes cubiertos

- Entes: `CAIB` = consolidado (AGIB + ATIB + SSIB − transferencias internas). `AGIB` = Administració General **incluidos los OOAA** (secciones 73-79: IBDona, Agència de Salut Pública, SOIB, IBESTAT, EBAP, Institut Balear de Seguretat i Salut Laboral…). `ATIB` = sección 50. `SSIB` = sección 60 (Servei de Salut).
- **Renombrado en 2024 (datos abiertos):** `SSIB` aparece como `IBSA` en el dataset abierto de 2024. `AGIB` aparece como `CAIB` en ese mismo dataset.
- Clasificaciones:
  - Económica hasta subconcepto (`ECO`).
  - Orgánica por sección y centro gestor (`ORG`).
  - Funcional por grupo, función, subfunción y programa (`FUN`, sin cruce por capítulo).
  - **Cruce funcional × económico × orgánico:** existe a nivel de partida en `PPP` (`AGIB_PPP_G`, `ATIB_PPP_G`, `SSIB_PPP_G`) y en el dataset abierto. No hay PPP consolidado en los ficheros de liquidación 2024; hay que sumar entes.
- Ejecución mensual: solo agregada consolidada por capítulo económico (1-9). No desglosa por ente ni por función.
- Sector público instrumental: en las fuentes de estadística no aparece; solo en el dataset abierto, sector `GSAI` (Secció 65, "Gestió Sanitària i Assistencial de les Illes Balears"). Ver problemas. El portal de transparencia tiene las secciones "Ens del sector públic instrumental autonòmic" y "Pressuposts dels ens…" (`/sites/transparencia/ca/1131_ens_del_sector_pablic_instrumental_autonamic/` y `/pressuposts_dels_ens_del_sector_public_instrumental_autonomic/`), pero su listado de entes y ficheros no aparece en el HTML estático (probablemente se carga con JavaScript). Completitud **no verificada**: hace falta navegador.

### Cobertura temporal y frecuencia/latencia

- Liquidación: anual, 2002-2024 (páginas por año; dataset abierto 2002-2024).
- Presupuesto: anual, 2002-2026 (2026 es prórroga).
- Serie anual 2002-2024 (liquidación consolidada, `CONSOLIDAT_2002-2024_Principals_magnituds_pressupostaries.xlsx`): totales desde 2002. Es la única fuente anual con dato anterior a 2010.
- Ejecución mensual: serie 2010-2026 acumulada. Trimestral hasta 2012 (en la hoja, Trimestre 1 y 2 de 2012) y mensual desde julio de 2012 (el portal dice «fins al mes de juliol de 2012»). No se ha encontrado ejecución infra-anual anterior a 2010 (**no verificado**).
- Latencia observada:
  - Liquidación 2024: "actualitzada novembre 2025" (≈11 meses tras cierre).
  - Ejecución: "darrera actualització octubre 2026 (execució de setembre 2026)" (≈1 mes). Próxima actualización: noviembre 2026.
  - Presupuesto 2024: página "actualitzada gener 2024".

### Licencia y autenticación

- Sin autenticación, sin sesión (no hace falta cookie; `JSESSIONID` se emite pero no es necesario), sin formularios ni CAPTCHA.
- Dataset abierto: metadatos `schema:license = cc-by` (versión no indicada). Dataset IBESTAT de consells: CC BY 3.0 ES.
- Ficheros del portal de estadísticas: la página de aviso legal (`legal.html`) no contiene texto de licencia de datos; solo aparece código de terceros. Licencia **no verificada**. Tratar como datos públicos a confirmar con el responsable del portal.

### Ficheros de ejemplo (no commitear)

Ruta local, en scratchpad (`C:/Users/Troll/AppData/Local/Temp/claude/C--Users-Troll-Documents-github-audit/d8ef6bbf-395b-4794-92ba-ea1e9495bd0f/scratchpad/caib/dl/`). Adjuntar luego a la Release `spike-caib`:
- `liq2024/` (28 XLSX de liquidación 2024, incluye `CAIB_ECO_G_202312_ca.xlsx`, ver problemas)
- `pres2024/` (29 ficheros de presupuesto 2024)
- `exec/Serie_d_ingressos_i_despeses_2010-2026.xlsx` (serie mensual, 62 KB)
- `od/ppp_dsp_liq.xlsx` (dataset abierto 2002-2024, 33 MB)
- `od/head.csv` (cabecera del CSV de presupuesto 2024-2025, descarga parcial)

Scripts de la spike (en `spike/caib/`, no commiteados): `fetch_caib.sh` (descarga por páginas), `xlsx_dump.py` (volcado stdlib), `check_capitols.py`, `check_serie.py`, `check_opendata.py` (verificaciones).

### Problemas conocidos y riesgo de cambio

- **Nombre de fichero engañoso:** en la página de liquidación 2024 aparece `CAIB_ECO_G_202312_ca.xlsx`, pero su contenido es 2024 (cuadra con el PMP de 2024). No fiarse del nombre; verificar contenido.
- **Slugs de página irregulares:** `2024_0` (liquidación) frente a `2024_p` (presupuesto); cambian al cambiar de ejercicio. Riesgo alto de romper scraping por página. Preferir los ids `/f/<id>` (estables) o el dataset abierto.
- **Token `ctrl` ignorado:** la descarga funciona con cualquier `ctrl`. Conviene no depender de él.
- **Dos formatos de hoja distintos:** en `CAIB_ECO_G` las columnas son entes; en `AGIB_ECO_G` son créditos (inicial, modificaciones, definitivo, disposición, ordenado…). La columna "Crèdit ordenat" es la de obligaciones reconocidas. Su posición cambia por fichero.
- **Unidades distintas:** liquidación y dataset abierto en euros; serie mensual en miles de euros.
- **Serie con periodos mezclados:** filas "Trimestre N" hasta 2012, "Mes" después; el sufijo "(P)" o "(A)" indica provisional o definitivo; los valores son acumulados.
- **Discrepancia de consolidación (GSAI):** en el dataset abierto 2024, `GSAI` (Secció 65, 39.053.259,34 € de obligaciones: cap. 1 30.706.336,11; cap. 2 8.273.233,64; cap. 6 73.689,59) tiene `Consolida = Sí`. En los ficheros de liquidación y en la serie no aparece. Sin GSAI el total cuadra exactamente; con GSAI hay 39 M€ de diferencia. La serie anual 2002-2024 (consolidado) también excluye GSAI: operaciones corrientes 2024 = 5.321.648.203,87 €, igual que el PMP. **Recomendación: excluir GSAI** de la ingesta, pendiente de confirmación de la decisión.
- **Cambio de nombre de entes:** SSIB ↔ IBSA (2024, abierto). Mantener una tabla de equivalencias.
- **Ficheros grandes y de nombre dinámico:** el dataset abierto pesa 33 MB; cada año cambia el nombre (`_202412`, `_202312`…).
- **Host `intranet.caib.es`:** los datos abiertos cuelgan de un dominio de intranet. Riesgo de que deje de ser accesible desde fuera de la red corporativa (no ocurre hoy desde este entorno).
- **Mojibake en consola:** no es problema del fichero, pero los scripts de volcado deben usar UTF-8.

### Verificación

Comparaciones hechas con los datos descargados (euros, 2024):

- **Liquidación consolidada por capítulo vs totales publicados (PMP 2024).** Suma de obligaciones reconocidas (`CAIB_ECO_G`, columna Consolidat), cap. 1 a 9:
  - 1 Personal: 2.152.719.012,43
  - 2 Bienes corrientes: 1.062.094.229,20
  - 3 Financieros: 145.607.881,96
  - 4 Transferencias corrientes: 1.961.227.080,28
  - 5 Fondo de contingencia: 0,00
  - 6 Inversiones reales: 221.813.888,87
  - 7 Transferencias de capital: 647.315.491,50
  - 8 Activos financieros: 21.043.059,65
  - 9 Pasivos financieros: 923.077.607,01
  - **Total: 7.134.898.250,90.** Operaciones corrientes 5.321.648.203,87 y de capital 869.129.380,37 cuadran con el PMP publicado (diferencia 0,00).
- **Serie mensual 2024 (diciembre acumulado, en miles) vs liquidación:** capítulos 1, 2, 3, 4, 6 y 7 coinciden al céntimo (diferencia 0,00).
- **Dataset abierto 2024 (`Crèdit ordenat`), filtro `Consolida = Sí` y sin GSAI:** total 7.134.898.250,90 y capítulos iguales a los anteriores. Con GSAI el total es 7.173.951.510,24 (ver discrepancia). `Consolida = No` suma 2.379.168.128,54, igual a la diferencia entre total de entes (9.514.066.379,44) y consolidado: las transferencias internas se eliminan bien.
- **Cruce PPP vs ECO por ente (AGIB):** suma de partidas de `AGIB_PPP_G` en "Crèdit ordenat" por capítulo cuadra con la columna AGIB de `CAIB_ECO_G` (ej. cap. 1 1.028.950.791,13). El total de `AGIB_PPP_G` es 7.129.845.638,07, igual que la columna AGIB; en el dataset abierto ese mismo importe aparece como sector `CAIB`.

- **Segundo año, 2023 (PMP 2023 `CAIB_PMP_202312_ca.xlsx` vs serie anual 2002-2024):** total consolidado de operaciones corrientes 4.828.463.821,06 € en ambas fuentes; capítulo 1 Personal 1.993.213.016,55 € en ambas. Diferencia 0,00.

**No verificado:** ejecución infra-anual anterior a 2010; capítulos 6 a 9 de la serie anual 2002-2024 (solo se cruzaron corrientes); completitud del sector instrumental (requiere navegador); texto de licencia del portal de estadísticas; serie "Evolució del pressupost 2020-2025" (no descargada).

---

## PLACSP — Contratos (incluidos menores)

Estado: investigación v1 completada el 2026-10-24 (issue TorratDev/audit#7). Muestra medida: ficheros mensuales de diciembre de 2025 y enero de 2026. Pendiente de confirmar: ver "Pendiente de confirmar".

### URL de acceso y documentación

- Licitaciones (perfiles del contratante, sin menores): https://www.hacienda.gob.es/es-ES/GobiernoAbierto/Datos%20Abiertos/Paginas/LicitacionesContratante.aspx
  - Índice: `https://contrataciondelsectorpublico.gob.es/sindicacion/sindicacion_643/licitacionesPerfilesContratanteCompleto3.atom`
- Agregación de plataformas autonómicas (sin menores): https://www.hacienda.gob.es/es-ES/GobiernoAbierto/Datos%20Abiertos/Paginas/LicitacionesAgregacion.aspx
  - Índice: `.../sindicacion/sindicacion_1044/PlataformasAgregadasSinMenores.atom`
- Contratos menores (perfiles del contratante): https://www.hacienda.gob.es/es-ES/GobiernoAbierto/Datos%20Abiertos/Paginas/ContratosMenores.aspx
  - Índice: `https://contrataciondelsectorpublico.gob.es/sindicacion/sindicacion_1143/contratosMenoresPerfilesContratantes.atom`
  - Zips: `.../sindicacion_1143/contratosMenoresPerfilesContratantes_AAAA.zip` (anuales desde 2018) y `..._AAAAMM.zip` (mensuales del año en curso).
- Especificación de sindicación y reutilización, versión 1.3 (documento fechado 05/08/2020): https://www.hacienda.gob.es/Documentacion/Publico/D.G.%20PATRIMONIO/Plataforma_Contratacion/especificacion-sindicacion-1-3.pdf
- Referencia de herramienta: OpenPLACSP (DGPE), citada en el issue.

### Formato y encoding

- Atom 1.0 (RFC 4287) con extensiones XML propias de PLACSP (espacios `cac-place-ext` / CODICE 2.x). Cada `<entry>` contiene el expediente completo en `ContractFolderStatus`.
- Encoding UTF-8 (declarado en la cabecera XML).
- Paginación: máximo 500 entradas por fichero; la siguiente página se referencia en `atom:link[@rel="next"]`. Dentro de un zip, la cadena empieza en el fichero índice (`contratosMenoresPerfilesContratantes.atom`) y cada fichero enlaza con el anterior.
- Tamaño: el zip mensual de enero de 2026 ocupa 25,6 MB con 104 ficheros XML; el de diciembre de 2025 ocupa 31,4 MB con 119 ficheros.

### Granularidad, órganos cubiertos e identificadores

Granularidad: una entrada = un anuncio/versión de un expediente. Una misma licitación aparece tantas veces como cambios tuvo (ver "Problemas conocidos"). El identificador de la entrada es la URL `https://contrataciondelestado.es/sindicacion/datosAbiertosMenores/<n>`.

Identificadores que emplea PLACSP para el órgano (`LocatedContractingParty/Party/PartyIdentification`): `DIR3` (cuando existe), `NIF` y `ID_PLATAFORMA` (el ID de perfil de la plataforma, que suele coincidir con el DIR3 en administraciones y con el NIF en empresas).

| Órgano | DIR3 | NIF | ID plataforma | Observaciones |
|---|---|---|---|---|
| Govern de les Illes Balears (CAIB), Administració general | A04003003 | S0711001H (observado como ID plataforma en algunas consejerías) | A04003003 / S0711001H | Consejerías. Publica en PLACSP directamente. |
| Servei de Salut de les Illes Balears (IB-Salut) | A04003754 | — | A04003754 | Mayor volumen de menores CAIB (90 en enero de 2026). |
| Consorcio de Transportes de Mallorca | A04003678 | — | A04003678 | Ente con DIR3 de la CAIB. |
| Institut Balear de la Natura (IBANAT) | A04013548 | — | A04013548 | OA. |
| Serveis Ferroviaris de Mallorca (SFM) | A04013561 | — | A04013561 | |
| Ports de les Illes Balears | A04013624 | — | A04013624 | |
| Ente Públic de Radiotelevisió de les Illes Balears (IB3) | A04013626 | — | A04013626 | |
| Servei d'Ocupació de les Illes Balears (SOIB) | A04013537 | S0711001H | S0711001H | |
| Escola Balear d'Administració Pública (EBAP) | A04013584 | — | A04013584 | |
| Institut Cartogràfic i Geogràfic de les Illes Balears (ICGIB) | A04013562 | — | A04013562 | |
| Institut d'Estudis Baleàrics | A04013612 | — | A04013612 | |
| Fundació Institut d'Investigació Sanitària IISIB | A04005606 | — | A04005606 | Fundación pública. |
| Fundació Banc de Sang i Teixits | A04005605 | — | A04005605 | |
| Fundació de atención y apoyo a la dependencia y promoción de la autonomía personal de les Illes Balears | A04005599 | — | A04005599 | |
| Serveis de Millora Agrària i Pesquera | A04013544 | — | A04013544 | |
| Conselleria de Educación y Universidades | A04013523 | — | A04013523 | |
| Agència Balear de l'Aigua i de la Qualitat Ambiental | sin DIR3 en la muestra | Q0700507G | Q0700507G | Órgano sin DIR3 en la feed. |
| Ajuntament de Palma | L01070407 | P0704000I | 30867220130482 | Licitaciones: 67 expedientes en enero de 2026. Publica menores en PLACSP de forma esporádica con el DIR3 `L01070407`, también usado por sus OOAA (Junta de Gobierno, Gerencia del IMI y Patronat de l'Habitatge): 31 entradas en 2019, 20 en 2021, 15 en 2023, 8 en 2024, 1 en marzo de 2025 y 0 en jun-2025, nov-2025, dic-2025 y ene-2026 (conteo de entradas, no de expedientes únicos). El DIR3 `L01070645` no se ha verificado y no se usa. |
| Empresa Municipal de Transports Urbans de Palma (EMT) | sin DIR3 | A07152515 | A07152515 | Menores publicados en enero de 2026 (9). |
| EMAYA | sin DIR3 | A07000029 | A07000029 | Aparece solo en 1 entrada de menores de enero de 2026. |
| MERCAPALMA | EA0008394 | A07021751 | A07021751 | Mercado, sociedad municipal de Palma (50 menores en enero). |
| Ajuntament d'Alcúdia | L01070033 | P0700300G | L01070033 | Licitaciones: 16 expedientes en enero de 2026. Menores: 1 en enero de 2026 (CN-17/2025 EE0262/2025, adjudicado 2025-11-12, 14.950 € sin IVA). |

Esta tabla es una lista de identificadores **observados** en los ficheros. No se ha consultado el catálogo DIR3 completo (`directorio3`): los OOAA y sociedades listadas son los que aparecen en la muestra, no un inventario completo. Las sociedades municipales de Alcúdia y los OOAA del Ayuntamiento de Palma quedan por confirmar.

Órgano de la CAIB en el portal de transparencia: en el CSV del portal figuran 96 órganos distintos (campo `ÒRGAN CONTRACTACIÓ`), con nombres de consejerías y entes, sin códigos.

### Cobertura temporal y frecuencia

- Licitaciones (`LicitacionesPerfilesContratanteCompleto3`): anuales desde 2012 (zip) y mensuales del año en curso. Actualización diaria del día anterior. La cobertura no es homogénea entre órganos, porque cada uno empezó a publicar en PLACSP en fechas distintas.
- Agregación: anuales desde 2016 y mensuales del año en curso.
- Contratos menores: anuales desde 2018 y mensuales del año en curso. Actualización diaria. El zip mensual contiene las actualizaciones del mes anterior (p. ej. `_202601` contiene actualizaciones de enero de 2026) y el mes en curso se actualiza hasta el día previo.
- Medidos: diciembre de 2025 (58.857 entradas únicas) y enero de 2026 (51.456 entradas únicas; 46.044 expedientes distintos).
- Portal de transparencia CAIB (menores): desde 24/07/2017 hasta 30/09/2026 en el CSV; trimestral como mínimo. Antes de esa fecha (06/2008–07/2017) solo está en la plataforma antigua de la CAIB.

### Licencia y autenticación

- Acceso anónimo por HTTPS, sin autenticación ni API key.
- Licencia: no localizada en las páginas de Hacienda revisadas (sólo se citan los avisos legales generales). Para v1 se asume reutilización libre conforme a la Ley 37/2007 de reutilización de la información del sector público, pero **debe verificarse antes de publicar datos derivados**.
- Protección de datos: los NIF de personas físicas aparecen **sin enmascarar** en PLACSP (p. ej. adjudicatario de Alcúdia). El portal de la CAIB enmascara parcialmente DNI/NIE (y sustituye por "****" los que tienen errores). La ingesta debe tratar estos campos como datos personales.

### Decisión para contratos menores

**Fuente elegida para v1: PLACSP, feed de contratos menores** (`contratosMenoresPerfilesContratantes`), por tres motivos:

1. Es la fuente oficial y homogénea para todos los órganos del ámbito (CAIB, Palma, Alcúdia), con el mismo esquema que las licitaciones.
2. La CAIB publica sus menores en PLACSP: los datos del portal de transparencia son una exportación de la misma plataforma (el propio portal indica que "tota l'activitat ... es publica a la PLACSP").
3. Permite trazar cada entrada con su `updated` y su enlace al perfil.

El **CSV del portal de transparencia de la CAIB** se usa como validación y como complemento para el periodo 2017–2018 (antes del feed de PLACSP). Tiene campos adicionales (PIME, fondos UE, número de ofertas) y un registro de anuncios que cubre más años.

**Limitaciones aceptadas en v1:**
- Los pagos menores de 5.000 € (despesa menor, art. 63.4 LCSP) **no se publican** ni en PLACSP ni en el portal de la CAIB. El feed no sirve para medir este gasto.
- Antes de 2018 no hay feed de PLACSP para menores. Para la CAIB, el portal cubre desde 2017; para el resto de órganos no hay fuente equivalente en v1.
- Palma: publica pocos menores en PLACSP y ha dejado de hacerlo casi por completo desde 2025 (ver tabla de órganos). Los trimestrales de Palma en XLSX (#8) siguen siendo la fuente más completa para sus menores; comparar ambas fuentes antes de dar Palma por cubierta.
- Los menores pueden publicarse con retraso ("publicación trimestral" en la CAIB).

### Campos disponibles

Los campos siguen la estructura del feed de menores; "% relleno" es sobre las 51.456 entradas de enero de 2026.

| Campo de la ficha | Ruta en el Atom | % relleno (ene-2026) |
|---|---|---|
| Expediente | `ContractFolderStatus/ContractFolderID` | 100 % |
| Estado | `ContractFolderStatusCode` (en menores: RES) | 100 % |
| Título | `title` | 100 % |
| Enlace | `link[@href]` (deeplink del perfil) | 100 % |
| Fecha de actualización | `updated` | 100 % |
| Órgano | `LocatedContractingParty/Party/PartyName/Name` | 100 % |
| DIR3 órgano | `Party/PartyIdentification/ID[DIR3]` | 84,9 % |
| NIF órgano | `Party/PartyIdentification/ID[NIF]` | 100 % |
| ID plataforma | `Party/PartyIdentification/ID[ID_PLATAFORMA]` | 100 % |
| Tipo de contrato | `ProcurementProject/TypeCode` (1 suministros, 2 servicios, 3 obras, 7, 8: inferido de la distribución, no verificado en la lista de códigos) | 100 % |
| Subtipo | `ProcurementProject/SubTypeCode` | 97 % |
| Procedimiento | `TenderingProcess/ProcedureCode` (6 en todas las entradas de menores) | 100 % |
| CPV | `ProcurementProject/RequiredCommodityClassification/ItemClassificationCode` (primer código) | 39 % |
| Importe sin IVA (presupuesto) | `ProcurementProject/BudgetAmount/TaxExclusiveAmount` | 100 % |
| Importe con IVA (presupuesto) | `ProcurementProject/BudgetAmount/TotalAmount` | 100 % |
| Adjudicatario | `TenderResult/WinningParty/PartyName/Name` | 99,8 % |
| NIF adjudicatario | `TenderResult/WinningParty/PartyIdentification/ID[NIF]` (y `[OTROS]` para extranjeros) | 83,5 % |
| Importe adjudicado sin IVA | `TenderResult/AwardedTenderedProject/LegalMonetaryTotal/TaxExclusiveAmount` | 99,8 % |
| Importe adjudicado con IVA | `.../LegalMonetaryTotal/PayableAmount` | 99,8 % |
| Fecha de adjudicación | `TenderResult/AwardDate` | 100 % |
| Fecha de formalización | `TenderResult/Contract/IssueDate` | 4,1 % |
| Resultado | `TenderResult/ResultCode` | 100 % |
| Número de lotes | `ProcurementProjectLot` (solo conteo) | 0,2 % de entradas con lotes (107 de 51.456) |

Campos que no aparecen en el feed de menores: número de ofertas recibidas (sí aparece, `ReceivedTenderQuantity`, pero no se ha medido), PIME, financiación UE (`FundingProgramCode`, presente en muchos registros pero sin medir), y el detalle de lotes (solo se cuenta el número). El feed no tiene campo de fecha de publicación del anuncio separado de `updated`.

### Problemas conocidos

- **Versiones duplicadas**: la sindicación contiene varias versiones de un mismo expediente. Enero de 2026 tiene 51.681 entradas brutas, 51.456 IDs únicos y 46.044 expedientes distintos. La spec (apartado 3.3) indica que la versión más reciente de la entrada agrupa todos los datos, pero "en determinadas situaciones excepcionales" pueden eliminarse entradas antiguas. Para ingesta: deduplicar por `id` y quedarse con el `updated` mayor, y deduplicar por expediente para contar contratos.
- **Entradas regeneradas**: Hacienda ha regenerado sindicaciones fallidas a posteriori (issue #7). Un zip antiguo puede no coincidir con el actual; se recomienda descargar de nuevo el mes en curso y reprocesar.
- **Lotes**: un expediente con varios lotes aparece como una entrada con `ProcurementProjectLot` repetido. No se ha comprobado si el importe total del expediente coincide con la suma de lotes. Para importes por lote hay que leer `ProcurementProjectLot/ProcurementProject/BudgetAmount` y `AwardedTenderedProject/ProcurementProjectLotID`.
- **Publicación limitada de menores**: solo se publican los contratos marcados como menores por el órgano; los importes < 5.000 € de la CAIB no se publican; en el portal de la CAIB las convocatorias con concurrencia abierta aparecen en la categoría "contratos", no en "menores".
- **Periodos no homogéneos**: el feed de licitaciones no cubre igual a todos los órganos (cada uno empezó en fechas distintas).
- **Fechas**: `updated` se emite con zona horaria (+01:00 / +02:00). Convertir a UTC antes de comparar.
- **Campos nulos**: CPV solo en 39 % de los menores; fecha de formalización solo en 4 %.
- **Caracteres**: el texto aparece con sustitución (`�`) en algunas consolas; el XML es UTF-8 válido.

### Recuento (muestra)

Scripts en `spike/placsp/` (sin datos): `parse_atom.py` (lee todos los `.atom` de un directorio, deduplica y vuelca CSV), `recuento_caib.py` (cruce por expediente con el CSV de la CAIB) y `paths.py` (lista rutas de etiquetas).

**CAIB, contratos menores:**

| Mes (fecha de último anuncio en portal) | Portal CAIB (expedientes) | Encontrados en PLACSP (ficheros dic-25 y ene-26) |
|---|---|---|
| 12/2025 | 151 | 148 (98 %) |
| 01/2026 | 134 | 131 (98 %) |

- Portal CAIB: 16.711 filas, de 24/07/2017 a 30/09/2026 (2017: 890; 2018: 2.596; 2019: 1.834; 2020: 1.586; 2021: 1.585; 2022: 1.832; 2023: 1.632; 2024: 1.859; 2025: 1.649; 2026 hasta 30/09: 1.248).
- PLACSP menores de enero de 2026 con DIR3 A04: 152 entradas, 152 expedientes; por órgano: IB-Salut 90, IISIB 13, Consejería de Educación y Universidades 6, otros.
- Los expedientes del portal no encontrados en PLACSP son 3 (dic) y 3 (ene). Las diferencias probablemente se deben a que el portal fecha por último anuncio y PLACSP por fecha de actualización en el mes; no se han investigado los casos concretos.

Referencia de cobertura: la prueba de dic-2025 y ene-2026 es sobre dos meses. Además, **año 2023** (aproximado): 1.625 expedientes distintos en el portal (filas con fecha de último anuncio en 2023) frente a 1.504 expedientes CAIB en el feed anual 2023 de PLACSP. Se encuentra el 91,7 % del portal; hay 14 expedientes de PLACSP que no están en el portal. El cruce es aproximado porque el portal fecha por último anuncio y el feed por actualización, así que los expedientes de 2023 que se actualizaron en 2024 pueden faltar. Con la misma limitación, la cobertura de 2018–2022 y 2024 no se ha medido.

**Alcúdia (L01070033):** 16 expedientes de licitación y 1 menor en enero de 2026. No hay portal propio que contrastar en v1.

**Palma (L01070407):** 67 expedientes de licitación en enero de 2026. Menores: ver tabla de órganos; cobertura muy baja y decreciente.

### Pendiente de confirmar

- Palma: los menores de 2025–2026 sí se publican, en el XLSX trimestral (ver sección Palma). Pendiente: si el XLSX es completo; no hay total oficial con que contrastarlo.
- Si la agregación de plataformas (`PlataformasAgregadasSinMenores`) contiene históricos de la CAIB anteriores a 2017: la versión actual del feed (283 entradas) no incluye órganos de la CAIB, pero no se han revisado los zips antiguos.
- Licencia exacta de reutilización (no localizada en las páginas revisadas).
- Catálogo DIR3 completo para CAIB, Palma y Alcúdia, incluidos sus OOAA y sociedades (no se consultó el directorio oficial; la lista de la tabla es la observada).
- Cobertura completa 2018–2026 (solo se han medido dos meses).
- Lista oficial de códigos de `TypeCode` y `ProcedureCode` (las interpretaciones son inferidas).

---

# Fragmento para docs/fuentes.md: Palma, Alcúdia y CONPREL

Fecha de verificación: 2026-10-24. Lo no comprobado directamente va marcado como "no verificado".

## Palma — Presupuesto, ejecución y contratos

**Portal y URLs**
- Presupuesto e información: `https://palma.es/ca/pressupost` y la ficha `https://palma.es/ca/-/informaci%C3%B3-comptable-i-pressupost%C3%A0ria-2026`.
- Presupuesto 2026: aprobación inicial en el Ple de 18/11/2025. Aprobación definitiva publicada en BOIB 170, de 23/12/2025 (PDF descargado desde `palma.es/documents/39028/19699840/...`).
- Ejecución trimestral 2026 del Ajuntament: `palma.es/ca/-/execuci%C3%B3-1er-trimestre-ajuntament-de-palma-2026` (1T) y `www.palma.es/ca/-/execuci%C3%B3-2on-trimestre-ajuntament-de-palma-2026` (2T).
- Ejecución trimestral de OOAA y entidades dependientes: `palma.es/ca/-/execuci%C3%B3-del-pressupost-1er-trimestre-2026-organismes` (1T) y la página equivalente de 2T.
- Contratos menores (trimestrales): `palma.es/es/publicacions-trimestrals-de-contractes-menors`, en XLSX y PDF. Hay ficheros hasta el 3T 2026 (la issue decía hasta el 1T).
  - **XLSX verificado (15 trimestres, 1T 2023 a 3T 2026):** una hoja por trimestre, nombre `Ct Menors {n}T {año}`. Cuatro columnas: `Data` (fecha serie de Excel), `Import` (euros; no se sabe si incluye IVA), `EMPRESA ADJUDICATÀRIA` y `OBJECTE CONTRACTE`. **No tiene NIF, expediente ni órgano**, así que el cruce con `entidades` (#17) será por nombre.
  - Volumen medido (filas con importe, importe total):

    | Año | 1T | 2T | 3T | 4T |
    |---|---|---|---|---|
    | 2023 | 876 / 1,56 M€ | 903 / 1,24 M€ | 553 / 0,73 M€ | 874 / 1,04 M€ |
    | 2024 | 760 / 1,54 M€ | 678 / 1,22 M€ | 601 / 1,17 M€ | 1.091 / 1,59 M€ |
    | 2025 | 872 / 1,95 M€ | 890 / 1,92 M€ | 513 / 1,08 M€ | 757 / 1,33 M€ |
    | 2026 | 645 / 1,66 M€ | 589 / 1,37 M€ | 601 / 1,31 M€ | — |

  - **Comparación con PLACSP:** PLACSP tiene 15 entradas de Palma en 2023 y 8 en 2024 (entradas, no expedientes únicos), frente a unas 3.200 y 3.100 filas del XLSX en esos años. Como PLACSP apenas recoge menores de Palma, el XLSX es la fuente de referencia para ellos. No se sabe si el XLSX es completo: no hay un total oficial de contratos menores con que contrastarlo.
- Perfil del contratante: `perfilcontractant.palma.es`. Las licitaciones van a PLACSP.
- Subvenciones: sección "Registre de subvencions" en palma.es y convocatorias en BOIB con referencia BDNS. Contenido concreto de la sección: no verificado.

**Formato de la ejecución trimestral (verificado con descarga)**
- Formato XLSX, un fichero por entidad y trimestre. Descargados y abiertos: Ajuntament 1T 2026, Ajuntament 2T 2026, IME 1T 2026 e IME 2T 2026.
- Hojas (iguales en 1T y 2T, salvo una variante): `Formularios`, `F.1.1.1` (resumen por capítulos económicos), `F.1.1.2` a `F.1.1.5` (desglose de ingresos y gastos corrientes y de capital), `F.1.1.8` (remanente de tesorería), `F.1.1.9` (calendario de tesorería), `F.1.1.12` (plantilla y retribuciones), `F.1.1.13` y `F.1.1.14` (deuda viva y perfil de vencimiento), `F.1.1.B1` (ajustes SEC). En 1T aparece `F.1.1.18` y en 2T `F.1.1.17` (beneficios fiscales).
- Estructura: modelo de formularios F.1.x de la IGAE.
- Unidad: euros. Columnas: previsiones iniciales, previsión definitiva a final de ejercicio, derechos o obligaciones reconocidas netas acumulados al cierre del trimestre, recaudación o pagos líquidos, ejercicios cerrados y estimación a 31/12. La columna "Desviación (B)/(A)-1" se calcula contra la estimación a 31/12 (columna H), no contra el presupuesto inicial.
- Totales Ajuntament (euros): gastos iniciales 626.670.394,00. Obligaciones reconocidas acumuladas 84.167.486,38 en 1T y 213.892.642,31 en 2T. Derechos reconocidos netos 45.080.762,23 en 1T y 202.415.671,65 en 2T.
- Totales IME (euros): gastos iniciales 31.550.251,67. Obligaciones 3.479.842,19 en 1T y 9.049.209,32 en 2T.
- Estabilidad: entre 1T y 2T la estructura de hojas, filas y columnas es la misma. Sólo cambia la numeración de una hoja de anexo (F.1.1.17 / F.1.1.18).
- Cobertura de OOAA: se publican XLSX separados para IME, Palma Activa, PMEI, PMH-RIBA, Palau de Congressos, Fundació Turisme Palma y Fundació Pilar i Joan Miró (1T y 2T verificados por enlace; descargados sólo IME). Ficheros de 3T y 4T de 2026: no publicados en la página consultada.
- Datos 2025 y anteriores en este formato: no verificado.

**Presupuesto de referencia (BOIB y anexo de consolidación)**
- Ajuntament 2026 (ingresos y gastos iniciales): 626.670.394,00 €. Coincide con el XLSX.
- OOAA sin consolidar 2026 (ingresos): 59.278.504,33 €. Desglose por entidad (Habitatge, IME, Escoles, Palma Activa): BOIB 2025/170, `caib.es/eboibfront/pdf/ca/2025/170/1209438`.
- Estado de consolidación 2026 (anexo D004, verificado en descarga): gastos sin consolidar 1.078.388.694,04 €, consolidados 950.529.710,57 €. Ingresos sin consolidar 1.050.606.363,06 €, consolidados 922.747.379,59 €. Es la referencia para #12.

**Entidades del presupuesto general (perímetro de consolidación 2026, según D004)**

| Entidad | Tipo | NIF | Fuente y estado |
|---|---|---|---|
| Ajuntament de Palma | Entidad principal | P0704000I | Verificado en D004 |
| Institut Municipal de l'Esport (IME) | OOAA | ESP5701504B (identificador de directorio) | Directorio B2Brouter; formato dudoso. No verificado en registro |
| Agència de Desenvolupament Local (Palma Activa) | OOAA | ESP5790005B (identificador de directorio) | Directorio B2Brouter. No verificado en registro |
| Patronat Municipal de l'Habitatge i Rehabilitació Integral de Barris (PMH-RIBA) | OOAA | No verificado | Perímetro verificado en D004 y BOIB |
| Patronat Municipal d'Escoles d'Infants (PMEI) | OOAA | No verificado | Perímetro verificado en D004 y BOIB |
| Empresa Municipal d'Aigües i Clavegueram, S.A. (EMAYA) | Sociedad 100 % municipal | No verificado | Perímetro verificado en D004 |
| Empresa Funerària Municipal, S.A. (EFM) | Sociedad 100 % municipal | No verificado | Perímetro verificado en D004. La issue la llama "Empresa Financera": el nombre correcto es Funerària |
| Empresa Municipal de Transports Urbans de Palma, S.A. (EMT-Palma) | Sociedad 100 % municipal | A07152515 | Búsqueda web, varias fuentes (convenios y anuncios TED). Verificar en registro |
| Societat Municipal d'Aparcaments i Projectes, S.A. (SMAP) | Sociedad 100 % municipal | No verificado | Perímetro verificado en D004 |
| Fundació Pilar i Joan Miró | Fuera del perímetro de consolidación 2026 | No verificado | Aparece en la ejecución de OOAA 1T 2026 |
| Fundació Turisme Palma | Fuera del perímetro de consolidación 2026 | No verificado | Aparece en la ejecución de OOAA 1T 2026 |
| Palau de Congressos | Fuera del perímetro de consolidación 2026 | No verificado | Aparece en la ejecución de OOAA 1T 2026 |
| MERCAPALMA | Fuera del perímetro de consolidación 2026 | No verificado | Aparece en la lista de aprobación inicial 2026 |

- "IMI" (issue): no aparece en los documentos de 2026 revisados. No verificado; probablemente ya no existe.

**Frecuencia**: trimestral y acumulada. Contratos menores, trimestrales. Presupuesto, al aprobarse.
**Problemas**: nombres de anexos que cambian entre trimestres; columna de desviación calculada contra la estimación a 31/12; OOAA en ficheros separados (hay que sumarlos para consolidar); no hay datos económicos abiertos (ver abajo).
**Datos abiertos**: `smartoffice.palma.es/-/open-data` ofrece movilidad (GTFS de la EMT). Datos económicos: no verificado en detalle (según la issue, no hay).

## Alcúdia — Presupuesto, ejecución, liquidación y contratos menores

Verificado el 2026-10-24 en `alcudia.eadministracio.cat/transparency` (portal de transparencia de la sede electrónica, eAdministració).

### Acceso y formato

- Portal: https://alcudia.eadministracio.cat/transparency. Es una aplicación Wicket: el contenido se carga con JavaScript y no se lee con `curl`. La navegación fue con el navegador (categorías, subcategorías y listados de documentos).
- Los documentos se ven en `alcudia.eadministracio.cat/preview-document/<id>`, que muestra un visor PDF con `/preview/pdf/<token>.pdf`. Ese PDF devuelve **403** fuera de la sesión del navegador, incluso desde el propio navegador; por eso **no se han descargado** los ficheros. Pendiente: confirmar un canal de descarga.
- Contratación: perfil del contratante en PLACSP (sin cambios).
- Tablón de anuncios con PDF de presupuesto y liquidación en `alcudia.net` (ver abajo).

### Inventario del portal (recuentos del 2026-10-24)

| Sección | Contenido | Documentos |
|---|---|---|
| 3.1.1 Pressupostos | Presupuestos por año: 2018 (1), 2019 (1), 2020 (2), 2021 (2), 2022 (26), 2023 (1), 2024 (46), 2025 (47), 2026 (48) | 174 |
| 3.1.2 Modificacions pressupostàries | — | 1.248 |
| 3.1.3 Execució pressupostària | Ejecución trimestral 2025 (34 docs: 4 trimestres) y 2026 (17) | 51 |
| 3.3 Liquidació | 2022 (11), 2023 (0), 2024 (8). **2025 no publicada** | 19 |
| 6.1 Relació trimestral de contractes menors | Años 2016 a 2023 (1–4 docs por año). **Nada de 2024 a 2026** | 18 |
| 4. Ajudes i subvencions | Revisada (ver abajo) | 146 |

### Presupuesto (3.1.1, verificado en el portal)

- Carpeta por año con el mismo esquema: memoria de alcaldía, gráficos de gastos consolidados, resumen consolidado y, por entidad, resumen, memoria, gráficos de gastos e ingresos y estado de gastos e ingresos. Entidades: **Ajuntament**, **EMSA** (sociedad mercantil) y **CP** (Consorci Pollentia, desde 2025).
- **Presupuestos prorrogados desde 2022:** las carpetas de 2024, 2025 y 2026 tienen un documento "PRESSUPOST PRORROGAT" (2022 para 2024; 2024 para 2025; 2025 para 2026). Es decir, no consta ningún presupuesto nuevo aprobado y en vigor desde 2022 en este portal.
- **Presupuesto 2024:** solo consta el anuncio de aprobación inicial publicado en el BOIB (carpeta 2024). **La aprobación definitiva no aparece** y está en conflicto con la búsqueda previa (que citaba aprobación definitiva tras el pleno de 11/07/2024). No resuelto.
- Recuentos del portal: 2022 (26 docs), 2023 (1), 2024 (46), 2025 (47), 2026 (48). El número de documentos es alto porque cada entidad sube varios PDF por ejercicio.
- Formato: PDF. No se han leído las cifras; la carpeta de 2025 incluye "RESUM PRESSUPOST CONSOLIDAT 2025", que es el documento de referencia para cuadrar la consolidación. Sin descarga no se puede comprobar.
- Consecuencia para el proyecto: los datos de presupuesto de Alcúdia de 2023 a 2026 son prorrogados o provisionales, así que el dato de "crédito inicial" no equivale a un presupuesto aprobado en esos años. Hay que documentarlo en el modelo (#24) para que no se confunda con un presupuesto vigente.

### Ejecución trimestral (3.1.3)

- Cada trimestre incluye varias fichas PDF de la estructura IGAE (modelo F.1.x / F.3.x), igual que las de Palma: `F.1.1.1` resumen por clasificación económica, `F.1.2.x` balance y cuenta de pérdidas y ganancias, `F.1.3.x`, `F.3.2` estabilidad, `F.3.3` regla de gasto y `F.3.4` nivel de endeudamiento.
- Entidades: Ajuntament, EMSA, Biblioteca y Pollentia. En el 4T 2025 hay 9 documentos.
- Creación de los PDF: 02-feb-2026 (4T 2025). Latencia de unas cinco semanas desde el cierre del trimestre.
- **No verificado:** contenido numérico, si son PDF con capa de texto y si la estructura se mantiene entre trimestres. Sin descarga no se puede comprobar.

### Liquidación (3.3) y presupuesto

- **Liquidación 2024** publicada para el Ajuntament y el Consorci Pollentia. Ambas aprobadas por decreto en 2025 (DECRET 2025-0694 y 2025-0695). Fecha exacta de publicación no verificada, así que la latencia no se puede calcular con precisión: más de la mitad del año siguiente al ejercicio.
- **Liquidación 2025** no publicada a 2026-10-24.
- Los PDF de presupuesto y liquidación de `alcudia.net/export/sites/default/ajuntament/ca/documentos/tauler_anuncis/` (presupuesto de gastos 2022, liquidación de gastos 2021 y bases de ejecución 2022) se verificaron antes: la liquidación 2021 tiene capa de texto (generada por ABSIS, no escaneada). Las filas largas se parten en varias líneas.

### Subvenciones (sección 4, verificado)

- 146 documentos repartidos en 10 subcategorías (los 146 cuadran con la suma de contadores; "Veure'n més" no añade nada): Bons Viu Alcúdia (42), Projecte RestauraAlcúdia (3), Subvencions centres escolars (19), Beques llibres curs (25), Subvencions nominatives (4), Ajuts econòmics estudis superiors (34), Sa Rua (1), Pla estratègic de subvencions (7), Entitats esportives (6), Pla de subvencions de façanes (5).
- Estructura de cada convocatoria: bases publicadas en el BOIB (con referencia de extracto), certificado de acuerdo, listas provisionales y definitivas con informe de la comisión de valoración, y convenios. Las listas de beneficiarios, al parecer, están en PDF adjuntos (no leídos).
- Subvenciones nominativas: solo convenios (2024: 2 documentos; 2025: 2, p. ej. "Sarau alcudienc" y "Colla de Geganters"). Sin importes en los títulos.
- Convocatorias con código BDNS: no visible en los títulos. Para cruzar con BDNS hay que leer los PDF o buscar por órgano en la API de BDNS (`organos`: Alcúdia = ids 2378–2382, ver sección BDNS).
- **Riesgo RGPD:** las becas de libros y los ajustes para estudios superiores son ayudas a personas físicas. Si las listas PDF incluyen nombres, ya están publicadas en el portal; la ingesta no debe ampliar esa exposición sin decidir qué se guarda (#17).
- **Pendiente:** leer al menos una lista de beneficiarios (solo cuando haya canal de descarga, ver arriba) y comprobar si BDNS tiene las mismas concesiones de Alcúdia (232 según la API).

### Contratos menores

- La relación trimestral del portal de transparencia **termina en 2023**.
- PLACSP, en cambio, tiene 1 contrato menor de Alcúdia en enero de 2026 (ver sección PLACSP).
- Consecuencia: para Alcúdia no hay fuente completa de menores de 2024 a 2026 en ninguno de los dos canales. Limitación de v1 a documentar.

### Calidad del dato (caso de control)

- Presupuesto y ejecución: PDF, un documento por entidad y trimestre; cifras sueltas en cada ficha.
- Liquidación: PDF con capa de texto; sin formato de datos.
- Menores: relación trimestral en PDF (no se ha revisado el formato) y solo hasta 2023.
- Latencia observada: ejecución del 4T 2025 creada el 02-feb-2026; liquidación 2024 aprobada en 2025.
- Riesgo: la sección "Pressuposts" tiene 2024 con 46 documentos y 2025 con 47 para un mismo ejercicio; hay que distinguir aprobación inicial, definitiva y modificaciones.

### Pendiente

- Canal de descarga de los PDF del visor (el 403 bloquea la descarga).
- Contenido numérico de la ejecución trimestral 2025 y 2026.
- Denominaciones completas de EMSA y Biblioteca (el portal solo las muestra abreviadas).

---

## CONPREL — Entidades locales

Verificado el 2026-10-24 en `serviciostelematicosext.hacienda.gob.es/SGFAL/CONPREL`.

### Acceso

- **Consulta web** de datos definitivos por ejercicio (2002–2025) y tipo (presupuestos o liquidaciones). Municipio a municipio, con el máximo desglose.
- **Descarga directa sin autenticación** (GET normal, verificado por cabeceras y descarga):
  - Excel de avance y definitivos: `/Consulta/DescargaFichero?CCAA=&TipoDato=<Presupuestos|Liquidaciones>&Ejercicio=<año>&TipoPublicacion=<Avance|Definitiva>`. Ejemplos: `EL2025CT.xlsx` (avance 2025, 3,3 MB) y `EL2024C00.xlsx` (liquidación 2024 definitiva, 0,6 MB).
  - Base de datos Access por ejercicio, todos los municipios: `TipoPublicacion=Access`. Ejemplo: `Liquidaciones2024.zip` (52 MB), que contiene `Liquidaciones2024.accdb` (445 MB sin comprimir).
- **Existencia de ficheros Access por año** (sondeo de cabeceras, 2026-10-24): presupuestos 2002–2004 devuelven HTTP 500 (sin fichero), 2005–2025 HTTP 200. Liquidaciones 2002–2021 HTTP 200. Liquidaciones 2022–2025: no concluyente (el sondeo no terminó).
- Los ficheros Excel con `CCAA=` vacío son el total nacional y por CCAA. Sus hojas `Parametros` vienen con códigos (`cdcta`, `cdfgr`) y sin etiquetas: no sirven sin la nota metodológica (`/Consulta/DescargaFicheroMetodologico?idFichero=…`, no descargada).

### Latencia (fechas de los propios ficheros)

- Liquidación 2024 definitiva (Excel, última modificación): 22/12/2025, unos 12 meses después del cierre.
- Liquidación 2025 avance (Excel, última modificación): 29/09/2026, unos 9 meses después del cierre. La página dice "actualizado 30/09/2026".
- Presupuesto 2026 avance: publicado el mismo día, 30/09/2026 (no es un dato cerrado).

### Municipios de interés (Palma 07040, Alcúdia 07003)

- **No verificado en datos.** Para leer el municipio hay que abrir el `.accdb`. En esta máquina no hay motor Access instalado (no existe el proveedor `Microsoft.ACE.OLEDB` ni `Microsoft.Jet.OLEDB`, y el driver ODBC de Access no abre el `.accdb` desde PowerShell). Hace falta instalar el Access Database Engine o usar una herramienta de lectura; ambas cosas requieren tu permiso.

### Datos.gob.es

- Catálogo `e05250001`: la ficha de datos individuales responde 200. El rango de años que indicaba el issue (individuales 2005–2012) no se ha verificado.

### Riesgos y pendiente

- El Access es un único fichero por año de cientos de MB: la ingesta debe descargarlo, comprobar su tamaño y tratarlo como dato bruto versionado (#13).
- Excel sin etiquetas: hace falta la nota metodológica antes de usarlos.
- Pendiente: leer el `.accdb` de 2024 (Palma y Alcúdia), comprobar la cobertura de 2022–2025 en liquidaciones, y conseguir la nota metodológica.

---

## Decisión

- CONPREL como única fuente: no recomendada sin matiz. Cubre 2002 a 2025 (definitivos) y el avance 2025 y 2026, pero no da datos trimestrales, contratos menores ni subvenciones.
- Recomendación: CONPREL como fuente principal de presupuesto y liquidación municipal. Fuente propia complementaria para (a) la ejecución trimestral 2026 de Palma (XLSX), más reciente, y (b) la consolidación de Palma con el anexo D004 y BOIB 2025/170, como referencia de #12. Alcúdia no tiene canal estructurado verificado; el parseo de PDF es el plan B.
- Entidades dependientes de Palma con NIF (perímetro de consolidación 2026):
  - Ajuntament de Palma: P0704000I (verificado).
  - IME: ESP5701504B (identificador de directorio, formato dudoso; no verificado).
  - Palma Activa: ESP5790005B (identificador de directorio; no verificado).
  - PMH-RIBA: no verificado.
  - PMEI: no verificado.
  - EMAYA: no verificado.
  - EFM: no verificado.
  - EMT-Palma: A07152515 (búsqueda web; verificar en registro).
  - SMAP: no verificado.
- Pendiente antes de #11: confirmar NIF de OOAA y sociedades en registro o AEAT. Decidir si entran las fundaciones (Pilar i Joan Miró, Turisme Palma, Palau de Congressos, MERCAPALMA), que quedan fuera de D004.

---

## BDNS — Subvenciones y ayudas

**Estado de la vía:** confirmada para concesiones (JSON, sin autenticación ni captcha observados). Matices: la especificación Swagger no se ha podido descargar, y el NIF de las personas físicas va enmascarado (ver RGPD). Los nombres de parámetros proceden del propio frontend del portal, que usa la misma API.

### URL de acceso y documentación

- Base de la API: `https://www.infosubvenciones.es/bdnstrans/api`. Hay también réplicas en `www.infosubvenciones.gob.es`, `www.pap.hacienda.gob.es` y `www.subvenciones.gob.es`, detectadas en el bundle del portal.
- Documentación: `https://www.infosubvenciones.es/bdnstrans/doc/swagger`. La página carga la UI de Swagger, pero el JSON de la especificación no se ha localizado en `v2/api-docs`, `v3/api-docs`, `openapi.json` ni `swagger.json`. Todas devuelven el shell HTML de la SPA. Pendiente de confirmar.
- Web services BDNS 2.0 (PDF de Hacienda): son para que los órganos remitan datos, no para consultar. Descartados.

### Vía elegida

**API JSON del portal** (`/api/concesiones/busqueda`), no exportación ni datos.gob.es.

Motivos:
- Devuelve JSON paginado con filtros por órgano, fecha y beneficiario. La exportación del portal (CSV/XLS) no permite paginar ni filtrar de forma reproducible.
- Permite sincronización incremental con `fechaRegInicio`/`fechaRegFin`.
- datos.gob.es no sirve como fuente de ingesta: la ficha del catálogo (`e05250001-base-de-datos-nacional-de-subvenciones`) responde 302 a `mantenimiento.red.es`, así que no se ha podido verificar.

### Formato

JSON (UTF-8). La respuesta de búsqueda es un objeto con `content` (filas), `totalElements`, `totalPages`, `numberOfElements`, `last`, `first`, `pageable` y un campo `advertencia` con el aviso de reutilización. Los errores de validación devuelven `{"codigo":"ERR_VALIDACION","errores":[...]}` con HTTP 400. Las caídas devuelven `{"codigo":"ERR_MANTENIMIENTO_BBDD", ...}`.

### Parámetros de `GET /concesiones/busqueda`

| Parámetro | Valor | Estado |
|---|---|---|
| `vpd` | `GE` (portal general) | Verificado. Se usa en todas las consultas. |
| `page` | índice desde 0 | Verificado |
| `pageSize` | entero | Verificado. El máximo efectivo es **10 000**: con 20 000 devuelve 10 000. |
| `organos` | lista separada por comas de **ids hoja** del árbol de órganos | Verificado |
| `beneficiario` | **idPersona numérico** (no NIF) | Verificado. Con NIF devuelve 400. |
| `fechaDesde`, `fechaHasta` | fecha de concesión, `DD/MM/YYYY` | Verificado. Con ISO `YYYY-MM-DD` devuelve 400. |
| `fechaRegInicio`, `fechaRegFin` | fecha de registro en BDNS, `DD/MM/YYYY` | Verificado |
| `numeroIdentificacion` | citado en el issue | **No existe**: se ignora en silencio y devuelve el total sin filtrar |
| `codConcesion`, `tipoAdministracion`, `regiones`, `descripcion`, `order`, `direccion` | filtros observados en el frontend | No probados individualmente |

Para buscar por beneficiario: `GET /terceros?busqueda=<NIF>` devuelve `{"terceros":[{"id":idPersona,"descripcion":"NIF - NOMBRE"}]}`. Ese `id` es el valor de `beneficiario`.

Árbol de órganos: `GET /organos?idAdmon=<A|L|C|O>&vpd=GE` (A = autonómica, L = local, C = central, O = otros). Sin `vpd` la petición se rechaza (400, o una página HTML "Acceso Denegado" con HTTP 200; ver riesgos). Cada nodo tiene `id`, `descripcion` y `children`. `GET /organos/codigo?codigo=<DIR3>` devuelve `ids` y `tipoAdmon`. No verificado con un DIR3 real: los tres códigos probados devolvieron 204.

**Atención:** el filtro `organos` debe recibir los ids **hoja** del árbol. Los ids de nodos agrupadores no son únicos entre niveles: `organos=15` devuelve la Diputación de Almería (6 829 concesiones), no Palma ni CAIB.

### Campos de la respuesta

| Campo | Contenido |
|---|---|
| `id` | id interno de la concesión |
| `codConcesion` | código de concesión (`SB…`) |
| `numeroConvocatoria` | código BDNS de la convocatoria |
| `idConvocatoria` | id interno de la convocatoria |
| `convocatoria` | título de la convocatoria |
| `descripcionCooficial` | descripción en lengua cooficial, si existe |
| `beneficiario` | `"NIF NOMBRE"` (persona jurídica); `"***NNNN** NOMBRE"` (persona física) |
| `idPersona` | id del beneficiario (valor del filtro `beneficiario`) |
| `importe`, `ayudaEquivalente` | importe concedido y ayuda equivalente (euros) |
| `fechaConcesion` | fecha de concesión (ISO) |
| `fechaAlta` | fecha de alta en BDNS |
| `instrumento` | tipo de instrumento (p. ej. subvención en dinero) |
| `urlBR` | enlace a la publicación oficial de la convocatoria (BOE/DOCM…). Es el "enlace" del issue. |
| `tieneProyecto`, `codigoInvente` | indicadores auxiliares |
| `nivel1`, `nivel2`, `nivel3` | nivel de administración, comunidad/región y órgano concedente |

Pendiente de confirmar: si `urlBR` apunta siempre a la publicación de la convocatoria o a la resolución de concesión individual.

### Paginación y límites

- Paginación completa verificada: Palma (filtro de 8 ids hoja) devuelve **2 358** filas en 3 páginas de 1 000 (1 000 + 1 000 + 358), todas únicas.
- `totalElements` es el total real del filtro. Sin filtro, el total de concesiones es **30 469 842**.
- Página profunda: `page=2999&pageSize=10` responde HTTP 200 en unos 7 s. No se ha encontrado tope de offset en el rango probado.
- **Límite de tasa: no confirmado.** 20 peticiones en paralelo (10 a la vez) devolvieron 20 × HTTP 200, sin 429. El límite de 10 req/s que cita el issue (según bdns-fetch) no se ha podido reproducir. Las peticiones secuenciales tardan entre 0,3 y 1,6 s.
- **Sin captcha ni autenticación** en ninguna de las pruebas.

### Órganos cubiertos (ids hoja)

| Órgano | Nodo del árbol | Hojas | Concesiones (total del filtro) |
|---|---|---|---|
| CAIB (Govern de les Illes Balears y entidades) | `A` → id 15 "ILLES BALEARS" | 115 | 168 401 |
| Ajuntament de Palma | `L` → id 40 → id 15 "PALMA" (Ayuntamiento = 2200) | 8 (2200, 2205–2211) | 2 358 |
| Ajuntament d'Alcúdia | `L` → id 40 → id 1372 "ALCÚDIA" (Ayuntamiento = 2378) | 5 (2378–2382) | 232 |

Las hojas de la CAIB son consejerías, direcciones generales, agencias y fundaciones. El script las obtiene del árbol en ejecución y no las fija a mano.

### RGPD: personas físicas

- **NIF:** enmascarado en la respuesta, con formato `***NNNN**` (se muestran 4 dígitos centrales). En la muestra de Palma hay 124 filas de persona física enmascarada de 2 378. Las personas jurídicas aparecen con NIF completo (2 254 filas).
- **Nombre:** aparece completo (p. ej. "DAVID PAMIES AUBALAT"). Este es el dato que requiere decisión en #17.
- **Conservación publicada:** la FAQ del portal (preguntas 402 y 512) indica que las concesiones a personas físicas se mantienen publicadas durante el año de concesión y el siguiente. Las de personas jurídicas, durante el año de concesión y los 4 siguientes. La muestra de Palma es coherente: las filas de persona física enmascaradas son de 2025 (100) y 2026 (14).
- Consecuencia para #17: el NIF llega ya ofuscado, pero el nombre de la persona física sí se publica. Hay que decidir si se almacena, se pseudonimiza o se excluye en la ingesta.

### Reutilización (licencia)

- No se ha identificado una licencia explícita (p. ej. CC BY) en el portal ni en el bundle. La página de aviso legal (`/bdnstrans/GE/es/avisolegal`) es una SPA y no se ha podido leer su texto.
- Texto de la propia API (`advertencia`): la reutilización está "sujeta a una serie de restricciones y consideraciones legales". Los datos son dinámicos y pueden corregirse, insertarse o eliminarse. La Administración puede restringir el acceso a la API ante "manifiesto abuso", "riesgos de seguridad" o "uso fraudulento", con referencia a las buenas prácticas de datos abiertos de datos.gob.es.
- **Pendiente:** licencia exacta y condiciones de atribución. Hay que confirmarlas antes de publicar datos derivados.

### Riesgos conocidos

- **Mantenimiento y caídas:** se observaron respuestas `ERR_MANTENIMIENTO_BBDD` y timeouts de 50 s en `concesiones/busqueda`. La primera página de Palma no respondió hasta el tercer intento. La ingesta necesita reintentos con espera.
- **Acceso denegado con HTTP 200:** `organos?idAdmon=A` sin `vpd` devolvió una página HTML "Acceso Denegado" (WAF de IGAE) con código 200. El cliente debe validar que la respuesta es JSON, no solo el código HTTP.
- **Ids de órganos:** el filtro `organos` con ids de agrupador devuelve otro organismo sin error. Los ids deben salir de las hojas.
- **Filtros que no existen:** `numeroIdentificacion` se ignora en silencio y devuelve el total sin filtrar. Un cliente que lo use puede descargar 30 millones de filas.
- **Formato de fechas estricto:** ISO da 400. Hay que usar DD/MM/YYYY.
- **Datos dinámicos:** las cifras cambian a diario (fechaAlta de hoy: 2026-10-24).
- **Sin SLA ni contrato** y posibilidad de restricción de acceso por abuso (ver reutilización).

### Verificación

Script: `spike/bdns/probe_bdns.sh` (uso: `OUT=<dir> bash spike/bdns/probe_bdns.sh`). Guarda el JSON crudo en la carpeta indicada, fuera del repo. Crudos de esta ejecución: `scratchpad/bdns/raw/`.

Ejecución del 2026-10-24:

| Prueba | Resultado |
|---|---|
| Swagger (6 rutas) | Todas HTTP 200 `text/html` (shell de la SPA). Sin JSON de especificación. |
| `organos` idAdmon A/L/C/O con vpd=GE | 19 / 50 / 22 / 215 nodos raíz |
| CAIB, filtro de 115 hojas | totalElements = 168 401 |
| Palma, filtro de 8 hojas | totalElements = 2 358. Páginas 1 000 + 1 000 + 358 = 2 358 únicas. |
| Alcúdia, filtro de 5 hojas | totalElements = 232 |
| Control `organos=15` (agrupador) | totalElements = 6 829 (otro organismo) |
| Beneficiario G07203573 (Federación de Asociaciones de Vecinos de Palma, id 6832108) | 8 concesiones |
| Control `beneficiario=G07203573` (NIF) | HTTP 400 ERR_VALIDACION |
| Control `numeroIdentificacion=G07203573` | totalElements = 30 469 842 (se ignora) |
| Fecha concesión 01/10/2026–24/10/2026 | 206 910 |
| Fecha registro 01/10/2026–24/10/2026 | 505 870 |
| Fecha en ISO | HTTP 400 ERR_VALIDACION |
| `pageSize=20000` | devuelve 10 000 filas |
| Total sin filtro | 30 469 842 |
| Ráfaga de 20 peticiones (10 en paralelo) | 20 × HTTP 200, sin 429 |
| Otros endpoints de búsqueda (totales) | convocatorias 660 393; minimis 4 375 137; ayudasestado 6 578 150; grandesbeneficiarios 152 318 |

Diferencias con el issue #9: (1) el Swagger no se ha podido descargar; (2) no existe `numeroIdentificacion`; (3) el límite de 10 req/s no se ha reproducido; (4) la ficha de datos.gob.es no responde en la URL indicada.
