# 07 · Plan de pruebas y UAT

## 1. Estrategia

| Nivel | Qué valida | Quién | Dónde |
|---|---|---|---|
| Unitarias | Cada fórmula de KPI con un dataset mínimo de resultado conocido | Desarrollo | `tests/` (pytest, en cada push) |
| Calidad de datos | Reglas de negocio BR-01…BR-08 sobre el dataset generado | Desarrollo | `labflow.cli validate` y `tests/test_quality.py` |
| Integración | Pipeline completo: generar → validar → calcular KPIs → dashboard | Desarrollo | CI |
| **UAT** | Que el sistema resuelve el problema del usuario | Usuarios clave | Este documento |

El dataset mínimo (`tests/conftest.py`, fixture `tiny`) tiene 5 muestras diseñadas para que cada KPI tenga un valor esperado calculable a mano. Es la «verdad conocida» contra la que se prueba cada fórmula.

## 2. Entorno y datos de prueba

- Entorno reproducible: `pip install -e ".[dev]"` + `make all`.
- Datos: `python -m labflow.cli generate --seed 42` (600 muestras, 90 días, corte 2026-01-31).
- Navegadores / dispositivos: la UI es Streamlit; se prueba en escritorio con un navegador actual.

## 3. Criterios de entrada y salida

**Entrada a UAT:** pruebas automatizadas en verde; 0 defectos críticos abiertos; dashboard desplegado localmente; datos de prueba cargados.

**Salida (go / no-go):**
- 100 % de los escenarios *Must* aceptados.
- ≥ 95 % de los escenarios totales aceptados.
- 0 defectos críticos o altos abiertos; los medios y bajos con plan y fecha.

**Severidad de defectos:** *Crítico* = datos o KPI erróneos sin alerta · *Alto* = funcionalidad Must no usable · *Medio* = funciona con una molestia · *Bajo* = cosmético.

## 4. Casos de UAT

> **Estado de ejecución:** plantilla lista. Completá la columna *Resultado* al ejecutar cada caso con los usuarios y guardá la evidencia (captura o nota) en `docs/img/uat/`.

| ID | Persona | Escenario | Pasos | Resultado esperado | Req. | Resultado |
|---|---|---|---|---|---|---|
| UAT-01 | Director | Ver tiempos de entrega y SLA | 1. Abrir vista *Director*. 2. Leer KPI-01, 02 y 03. 3. Revisar el desglose del SLA | TAT y SLA visibles con unidades y objetivo; las abiertas vencidas aparecen como incumplidas | REQ-001/002/003 | Pendiente |
| UAT-02 | Director / Operaciones | Encontrar el cuello de botella | 1. Ver «¿Dónde se va el tiempo?». 2. Identificar la etapa destacada | Se nombra la etapa con mayor tiempo y los % por etapa suman 100 % | REQ-004 | Pendiente |
| UAT-03 | Calidad | Revisar rechazo, repetición y QC | 1. Abrir vista *Calidad*. 2. Leer KPI-04 y KPI-06. 3. En *Operaciones* leer KPI-05 | Los tres KPIs se muestran con semáforo | REQ-005/006/007 | Pendiente |
| UAT-04 | Operaciones | Ver backlog y éxito del pipeline | 1. Abrir vista *Operaciones*. 2. Leer backlog por etapa y KPI-07 | Gráfico de backlog con las 7 etapas; KPI-07 visible | REQ-008/009 | Pendiente |
| UAT-05 | Calidad | Encontrar huecos de custodia y metadatos | 1. Vista *Calidad*. 2. Revisar tablas de huecos | Cada hueco muestra muestra, etapa o campo faltante | REQ-010/011 | Pendiente |
| UAT-06 | Director / Calidad | Interpretar alertas y errores de reporte | 1. Identificar KPIs en rojo. 2. Leer KPI-11 | Los KPIs fuera de objetivo se distinguen claramente; el objetivo se ve al pasar el mouse | REQ-012/018 | Pendiente |
| UAT-07 | Calidad | Confiar en la calidad de los datos | 1. Revisar la tabla de validaciones. 2. Verificar que no hay datos personales | Todas las validaciones *error* en ✅; solo seudónimos | REQ-013/015 | Pendiente |
| UAT-08 | Todas | Navegar por vista de rol | 1. Cambiar entre las 3 vistas | Cada vista muestra solo los KPIs de su rol, sin errores | REQ-016 | Pendiente |

## 5. Gestión de defectos

Cada defecto se registra en [`registros/defectos.csv`](registros/defectos.csv) con requerimiento, severidad y fase de detección. Esto alimenta el **DDP** y el **defect leakage** de [`METRICAS_DEL_PROYECTO.md`](METRICAS_DEL_PROYECTO.md).

## 6. Aceptación

| Nombre | Rol | Decisión | Fecha |
|---|---|---|---|
| _(completar)_ | Director del laboratorio | Aceptado / Aceptado con observaciones / Rechazado | |
| _(completar)_ | Responsable de calidad | Aceptado / Aceptado con observaciones / Rechazado | |
