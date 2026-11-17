# 09 · Validación «lite» (inspirada en GxP / CSV)

> **Aclaración honesta:** este documento muestra *cómo pensar* la validación de un sistema computarizado en un laboratorio regulado. **No** es una validación formal ni afirma cumplimiento de CLIA, ISO 15189, 21 CFR Part 11 o GAMP 5: el proyecto usa datos sintéticos y no está pensado para uso clínico.

## 1. Del requerimiento a la evidencia

| Fase de validación | Qué se espera | Su equivalente en este repo |
|---|---|---|
| **URS** (requisitos del usuario) | Qué necesita el usuario y por qué | [01-business-case](01-business-case.md), [historias de usuario](03-requerimientos/historias-de-usuario.md) |
| **FRS / FDS** (especificación funcional) | Qué hace el sistema y con qué reglas | [Diccionario de KPIs](05-diccionario-kpis.md), [modelo de datos](06-modelo-de-datos.md) |
| **Matriz de trazabilidad** | Cada requisito ligado a su prueba | [`04-rtm.csv`](04-rtm.csv), verificada por `test_rtm_references_existing_tests` |
| **IQ** (calificación de instalación) | El entorno se instala como está especificado | `pip install -e ".[dev]"` y CI en matriz de versiones de Python |
| **OQ** (calificación operacional) | El sistema funciona según la especificación | Tests unitarios con valores esperados calculados a mano |
| **PQ** (calificación de desempeño) | Funciona en uso real | [UAT](07-plan-de-pruebas-uat.md) con datos representativos |
| **Control de cambios** | Todo cambio se evalúa, aprueba y re-verifica | [Control de cambios](control-de-cambios.md) + ADRs + CI |
| **Gestión de riesgos** | Riesgos identificados y mitigados | [FMEA](08-registro-de-riesgos.md) |

## 2. Integridad de datos (ALCOA+)

| Principio | Cómo se refleja |
|---|---|
| **A**tribuible | Cada traslado de muestra registra el responsable (`handler`); cada cambio de código queda en Git con autor |
| **L**egible | Datos en CSV y documentación en Markdown, abiertos y versionados |
| **C**ontemporáneo | Cada evento guarda su fecha y hora al ocurrir; el corte `as_of` es explícito |
| **O**riginal | Los CSV generados son la fuente; los KPIs se recalculan, nunca se editan a mano |
| **E**xacto | Validaciones BR-01…BR-08 y pruebas automáticas |
| **C**ompleto | KPI-09 (custodia) y KPI-10 (metadatos) miden la completitud |
| **C**onsistente | Una única definición por KPI en el diccionario |
| **D**uradero / **D**isponible | Repositorio versionado; `make all` regenera todo |

## 3. Lo que faltaría en un entorno regulado real

- Firmas electrónicas y control de acceso por roles con revisión periódica.
- *Audit trail* a nivel de registro (quién cambió qué dato y cuándo), no solo a nivel de código.
- Procedimientos operativos (SOPs) aprobados y capacitación documentada.
- Validación sobre datos reales con protocolos firmados y desviaciones gestionadas (CAPA).
- Evaluación del proveedor de cada componente (software de terceros, nube).
