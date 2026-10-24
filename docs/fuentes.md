# Inventario de fuentes

Fase 0 del plan (#1, épica #2). Ficha por fuente con su estado de verificación.

Estados: **Confirmada** (verificada), **Pendiente** (falta verificar, issue indicado), **Descartada** (con motivo).

Los ficheros de ejemplo van en Releases, no en el repositorio.

---

## CAIB (Govern de les Illes Balears)

### Presupuesto y liquidación por subconcepto económico, ejecución mensual

- **Estado:** Confirmada en cuanto a cobertura temporal; formato de descarga pendiente (#6).
- **Acceso:** [Estadísticas presupuestarias CAIB](https://www.caib.es/sites/estadistiques/ca/estadistiques-68815)
- **Formato:** pendiente (#6).
- **Granularidad:** subconcepto económico, programa, entes cubiertos (Administración, organismos autónomos, ATIB, Servei de Salut). Pendiente de confirmar.
- **Cobertura temporal:** ejecución trimestral hasta julio de 2012 y mensual desde entonces. Serie desde 2010 según #1.
- **Frecuencia:** mensual.
- **Licencia y autenticación:** pendiente.

### Sector público instrumental

- **Estado:** Pendiente (#1 indica PDF, sin verificar).
- **Acceso:** Portal de transparencia CAIB.
- **Formato:** probablemente PDF.

### Contratos

- **Estado:** Pendiente (#7).
- **Acceso:** toda la contratación de la CAIB y su sector instrumental se publica en PLACSP. Los contratos menores están además en el portal de transparencia desde el 24/07/2017.

---

## Ajuntament de Palma

### Presupuesto y liquidación

- **Estado:** Confirmada como fuente CONPREL en #1. Revisión en palma.cat pendiente (#8).
- **Acceso:** CONPREL (Hacienda). Pendiente de confirmar la vía de acceso de palma.cat.
- **Formato:** pendiente.
- **Ejecución:** trimestral en .xlsx en palma.es.

### Presupuesto general (Corporación, OOAA y sociedades)

- **Estado:** Pendiente de consolidar. Riesgo de duplicar transferencias internas.
- **Acceso:** BOIB y palma.cat.

### Contratos menores

- **Estado:** Pendiente (#8).
- **Formato:** trimestral en .xlsx/.pdf en palma.es.

### Licitaciones

- **Estado:** Confirmada: solo en PLACSP.

### Datos abiertos propios

- **Estado:** Descartada como fuente de cifras. Los datos abiertos (SmartOffice) solo cubren movilidad.

---

## Ajuntament d'Alcúdia

### Presupuesto y liquidación

- **Estado:** Pendiente (#8).
- **Formato:** PDF, publicado en alcudia.net.
- **Fuente de partida:** CONPREL (#1).

### Portal de transparencia y perfil del contratante

- **Estado:** Pendiente (#8).
- **Acceso:** sede `alcudia.eadministracio.cat`.

### Contratación

- **Estado:** Confirmada: en PLACSP.

---

## Transversales

### PLACSP (contratos, incluidos menores)

- **Estado:** Pendiente (#7).
- **Formato:** feeds ATOM (según #1).
- **Hallazgo:** los contratos menores tienen un conjunto de datos propio desde 2018 (datos abiertos de Hacienda).
- **Acceso:** [contratos menores](https://www.hacienda.gob.es/es-ES/GobiernoAbierto/Datos%20Abiertos/Paginas/ContratosMenores.aspx).

### BDNS (subvenciones con beneficiario)

- **Estado:** Pendiente (#9). Hay API REST oficial, aún sin probar.
- **Acceso:** `infosubvenciones.es/bdnstrans/api`, `GET /concesiones/busqueda`.
- **Límite:** 10 peticiones/s.
- **Autenticación:** no requerida según el hallazgo inicial; pendiente de confirmar.

### CONPREL (liquidaciones municipales)

- **Estado:** Pendiente (#11).
- **Hallazgo:** datos.gob.es solo tiene series individuales antiguas. Los años recientes solo están en la consulta web.
- **Latencia:** las liquidaciones llegan con más de un año de retraso (según #1).

---

## Decisiones pendientes

- [ ] Contratos menores: vía de acceso definitiva (PLACSP frente a conjuntos propios).
- [ ] BDNS: confirmar acceso programático y límites de uso.
- [ ] Lista de órganos y entes con identificadores (DIR3, código INE, NIF) para filtrar las fuentes.

## Fuera de alcance de la v1

Estado, otras comunidades autónomas, API pública y cruce automático contrato ↔ partida (#1).
