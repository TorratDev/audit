# Inventario de fuentes

Fase 0 del plan (#1, épica #2). Ficha por fuente con su estado de verificación.

Estados:
- **Confirmada**: verificada en la fuente oficial.
- **Confirmada por búsqueda**: dato obtenido de resultados de búsqueda web o de documentos secundarios; no abierto en origen.
- **Parcial**: algunos datos confirmados, otros pendientes.
- **Pendiente**: falta verificar (issue indicado).
- **Descartada**: con motivo.

Los ficheros de ejemplo van en Releases, no en el repositorio.

> **Nota de verificación (2026-10-24):** desde el entorno de trabajo, el proxy de salida respondió 403 al CONNECT de `www.caib.es`, `www.hacienda.gob.es`, `www.infosubvenciones.es`, `www.palma.es`, `alcudia.net`, `www.alcudia.net` y `contrataciondelestado.es`. Ninguna fuente oficial se ha podido abrir en esta revisión. Los datos de este documento proceden de búsquedas web y de los issues (#6 a #9), salvo indicación contraria, y deben comprobarse en origen. No se han descargado ficheros de muestra.

---

## CAIB (Govern de les Illes Balears)

### Presupuesto y liquidación por subconcepto económico, ejecución mensual

- **Estado:** Parcial. Cobertura temporal confirmada por búsqueda; formato de descarga pendiente (#6).
- **Acceso:** [Estadísticas presupuestarias CAIB](https://www.caib.es/sites/estadistiques/ca/estadistiques-68815), [mapa del portal](https://www.caib.es/sites/estadistiques/ca/mapa/) y "Estat d'execució del pressupost actual" en el portal de transparencia. No se ha localizado el enlace de descarga del fichero mensual.
- **Formato:** no verificado. Hay páginas de liquidación por ejercicio (p. ej. `/ca/2024_0/` y `/ca/2023_0_0/`) cuyo tipo de fichero no se ha comprobado. El catálogo de datos abiertos de la CAIB tiene datasets de IBESTAT (PC-Axis, JSON, JSON-stat), por búsqueda.
- **Granularidad:** no confirmada. Subconcepto económico, programa y entes cubiertos (Administración, organismos autónomos, ATIB, Servei de Salut) siguen pendientes de #6.
- **Cobertura temporal:** ejecución trimestral hasta julio de 2012 y mensual desde entonces (por búsqueda). Series "Evolució del pressupost 2002-2025" y "Evolució de la liquidació 2002-2024" (por búsqueda). Serie desde 2010 según #1.
- **Frecuencia:** mensual (ejecución). Latencia no verificada.
- **Licencia y autenticación:** no verificadas. La búsqueda no encontró requisito de autenticación.
- **Riesgos:** cambios de URL o de formato de las páginas (#6 pide documentarlos).

### Sector público instrumental

- **Estado:** Pendiente (#6). Sin verificar.
- **Acceso:** portal de transparencia CAIB.
- **Formato:** no verificado (#1 indicaba PDF).

### Contratos

- **Estado:** Confirmada por búsqueda. Ver #7 y la ficha de PLACSP.
- **Acceso:** toda la contratación de la CAIB y de su sector público instrumental se publica en PLACSP, según el portal de transparencia. Los contratos menores están además en el portal de transparencia desde el 24/07/2017 (datos hasta 30/09/2026, publicación al menos trimestral). Los pagos menores de 5.000 € (art. 63.4 LCSP) no se publican.
- **Datos abiertos:** conjuntos "Contratos públicos del Govern" y "Adjudicatarios de contratos públicos" en datos.gob.es y en el catálogo CAIB. Posible validación frente a PLACSP. No abiertos en esta revisión.

---

## Ajuntament de Palma

### Presupuesto y liquidación

- **Estado:** Parcial. Vía en palma.es por búsqueda; CONPREL no verificado (#8, #11).
- **Acceso:** [palma.es/ca/pressupost](https://www.palma.es/ca/pressupost), con fichas anuales desde 2008 (cuenta general, ejecución, informes de intervención). Por búsqueda.
- **Formato:** no verificado. Las fichas enlazan documentos; no se ha comprobado el tipo de fichero de la ejecución.
- **Ejecución trimestral:** el issue #2 indica un informe trimestral en .xlsx en la ficha de 2026. No se ha confirmado. La búsqueda de esta revisión no localizó el fichero, y los informes trimestrales de otros ayuntamientos son PDF. Marcar como pendiente.

### Presupuesto general (Corporación, OOAA y sociedades)

- **Estado:** Parcial. Entes según BOIB 2019/175 y propuesta de 2019 (por búsqueda). NIF no obtenidos (#8).
- **Entes:** OOAA Habitatge, IME, Escoles, IMI y Palma Activa (desglosados por capítulos sin consolidar). Empresas EMAYA, EMT-Palma, EFM y SMAP (en anexos por capítulo y área de gasto).
- **Acceso:** BOIB y palma.cat.
- **Riesgo:** duplicar transferencias internas si no se consolida.

### Contratos menores

- **Estado:** Pendiente (#8). No verificado.
- **Formato:** según #2, publicaciones trimestrales en .xlsx y .pdf en palma.es (hasta T1 2026). No verificado.

### Licitaciones

- **Estado:** Confirmada por búsqueda: solo en PLACSP (art. 347.3 LCSP). Cada ficha del perfil del contratante (perfilcontractant.palma.es) enlaza a la plataforma estatal.

### Datos abiertos propios

- **Estado:** Descartada como fuente de cifras. Los datos abiertos de SmartOffice solo cubren movilidad (GTFS de la EMT), por búsqueda.

---

## Ajuntament d'Alcúdia

### Presupuesto y liquidación

- **Estado:** Parcial. Formato PDF confirmado por URLs de documentos del tablón (por búsqueda). Contenido 2023 a 2025 pendiente de revisión (#8).
- **Formato:** PDF en alcudia.net. Presupuesto de gastos por orgánica, programa y económica. Liquidación de gastos 2021 escaneada, con créditos definitivos y disponibles, difícil de parsear. Liquidación 2024 rendida en el pleno de 2025 (por búsqueda).
- **Fuente de partida:** CONPREL (#1). Código INE 07003 (por búsqueda, pendiente de comprobar en INE).

### Portal de transparencia y perfil del contratante

- **Estado:** Pendiente (#8). La sede no se ha podido abrir.
- **Acceso:** sede `alcudia.eadministracio.cat` (eAdministració), con portal de transparència y perfil del contratante (por búsqueda previa). Contenido no verificado.

### Contratación

- **Estado:** Confirmada por búsqueda: los anuncios de licitación remiten al perfil del contratante alojado en PLACSP.
- **Advertencia:** no confundir con L'Alcúdia (València), que es otro municipio.

---

## Transversales

### PLACSP (contratos, incluidos menores)

- **Estado:** Parcial (#7). Órganos, IDs y cobertura por órgano pendientes.
- **Formato:** Atom (RFC 4287), según la especificación de sindicación v1.3 (por búsqueda; PDF no abierto).
- **Licitaciones (sin menores):** conjunto de Hacienda con actualización diaria, con agregación de plataformas autonómicas. Referencia de herramienta: OpenPLACSP.
- **Contratos menores:** conjunto propio desde 2018, por búsqueda sobre la página de Hacienda. Zips anuales desde 2018 hasta el año anterior y mensuales del año en curso. Actualización diaria. Lectura desde `contratosMenoresPerfilesContratantes.atom`, con 500 entradas por fichero y paginación con `rel="next"`.
- **Problema conocido:** en los comentarios de datos.gob.es sobre el conjunto de licitaciones (sin menores), usuarios indican que los primeros datos tienen fecha 25/08/2026 y que Hacienda está regenerando sindicaciones para recuperar ficheros no publicados. No es un aviso oficial confirmado. Comprobar las fechas de los ATOM y ZIP antes de depender de ellos.
- **Riesgo:** cobertura incompleta de contratos menores municipales (#7).

### BDNS (subvenciones con beneficiario)

- **Estado:** Parcial (#9). API REST documentada en Swagger según búsqueda. No probada en esta revisión (proxy 403).
- **Acceso:** base `https://www.infosubvenciones.es/bdnstrans/api`. Documentación Swagger en `/bdnstrans/doc/swagger`.
- **Endpoints:** `GET /concesiones/busqueda`, con `page` y `pageSize`, y filtros de fecha de registro (`fechaRegInicio`/`fechaRegFin`) o de concesión (`fechaDesde`/`fechaHasta`, DD/MM/YYYY). Otros: `organos`, `organos-codigo`, `convocatorias/busqueda`, `minimis-busqueda`, `ayudasestado-busqueda`, `grandesbeneficiarios`. Nombres de parámetros pendientes de confirmar en el Swagger.
- **Formato de respuesta:** JSON (versión 2 de la API, según el manual oficial, por búsqueda). La web exporta a PDF, XLS, CSV, JSON y XML.
- **Límite:** 10 peticiones GET por segundo por IP (por bdns-fetch, fuente secundaria). Pendiente de confirmar en documentación oficial.
- **Autenticación:** no encontrada en búsqueda. Pendiente de confirmar. Cada operación queda registrada (IP, fecha, operación y estado), según el manual.
- **Visibilidad:** las concesiones aparecen durante el año de concesión y los cuatro siguientes, y las de personas físicas solo el año siguiente (nota informativa de 2022, por búsqueda). Relevante para la decisión RGPD (#17) y para la carga histórica.
- **Alternativa:** datos.gob.es (entrada de la BDNS).
- **Reutilización:** pendiente.

### CONPREL (liquidaciones municipales)

- **Estado:** Parcial (#8, #11). Consulta web no verificada en origen.
- **Acceso:** consulta web en `serviciostelematicosext.hacienda.gob.es/SGFAL/CONPREL` (Secretaría General de Financiación Autonómica y Local).
- **Formato:** la remisión de liquidaciones es XBRL con taxonomías PENLOC-2010 y LENLOC-2010 (circular de 2011, por búsqueda). Base legal de remisión: Orden EHA/468/2007 (por búsqueda). Las clasificaciones de #11 citan la Orden EHA/3565/2008; no verificado aquí.
- **Descarga:** datos agregados en HTML, XLS y MDB en datos.gob.es (por búsqueda). Datos individuales en datos.gob.es solo hasta 2012 (presupuestos 2005-2012, liquidaciones 2002-2011, por búsqueda). Para años recientes solo hay consulta web. Descarga masiva o exportación por municipio y ejercicio: no confirmada.
- **Latencia:** las liquidaciones llegan con más de un año de retraso (según #1 y #11).
- **Hallazgo:** datos.gob.es no cubre años recientes a nivel de municipio.

---

## Decisiones pendientes

- [ ] Contratos menores: vía de acceso definitiva (PLACSP, conjunto propio de Hacienda o portal de transparencia de la CAIB), con cobertura medida frente a los portales municipales (#7).
- [ ] BDNS: confirmar en el Swagger los parámetros, la autenticación, los límites y la reutilización. Probar con un beneficiario conocido (#9).
- [ ] Lista de órganos y entes con identificadores (DIR3, código INE, NIF). Códigos INE de Palma (07040) y Alcúdia (07003) por búsqueda; DIR3 y NIF no obtenidos (#2, #7, #8).
- [ ] Palma: confirmar si la ejecución trimestral es .xlsx o PDF y si cubre los OOAA (#8).
- [ ] Alcúdia: revisar el contenido del portal eAdministració (liquidaciones 2023 a 2025, contratos menores, subvenciones) (#8).
- [ ] CAIB: formato de descarga, granularidad, entes y licencia de la ejecución mensual (#6).
- [ ] Ficheros de muestra en Release `spike-caib` y similares, y scripts de spike en `spike/` (#6, #9). No hechos.
- [ ] Verificar en origen todas las fichas marcadas como "por búsqueda", desde un entorno con acceso a los dominios oficiales.

## Fuera de alcance de la v1

Estado, otras comunidades autónomas, API pública y cruce automático contrato ↔ partida (#1).
