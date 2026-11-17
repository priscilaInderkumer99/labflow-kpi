# 05 · Diccionario de KPIs

Una única definición por KPI. Los objetivos viven en [`kpis.KPI_SPECS`](../src/labflow/kpis.py) y son los del laboratorio ficticio: cambiarlos es un **cambio de requerimiento** (ver [control de cambios](control-de-cambios.md)).

| ID | KPI | Definición | Fórmula | Dueño | Objetivo | Req. |
|---|---|---|---|---|---|---|
| KPI-01 | TAT mediana | Horas típicas entre recepción y emisión del reporte | `mediana(emisión − recepción)` en muestras completadas | Director | ≤ 168 h | REQ-001 |
| KPI-02 | TAT p90 | Horas por debajo de las cuales se entrega el 90 % | `percentil 90` del TAT | Director | ≤ 240 h | REQ-002 |
| KPI-03 | Cumplimiento de SLA | % de muestras entregadas en ≤ 240 h | `en plazo / (en plazo + fuera de plazo + abiertas vencidas)` | Director | ≥ 95 % | REQ-003 |
| KPI-04 | Tasa de rechazo | % de muestras rechazadas en recepción | `rechazadas / recibidas` | Calidad | ≤ 5 % | REQ-005 |
| KPI-05 | Tasa de repetición | % de muestras con alguna etapa repetida | `muestras con intento > 1 / muestras no rechazadas` | Operaciones | ≤ 10 % | REQ-006 |
| KPI-06 | QC a la primera | % de controles de laboratorio aprobados en el 1.er intento | `aprobados 1.er intento / controles 1.er intento finalizados` | Calidad | ≥ 92 % | REQ-007 |
| KPI-07 | Éxito del pipeline | % de corridas finalizadas sin fallo | `corridas ok / corridas finalizadas` | Bioinformática | ≥ 97 % | REQ-008 |
| KPI-08 | Backlog | Muestras en curso por etapa a la fecha de corte | `conteo de eventos «in_progress» por etapa` | Operaciones | informativo | REQ-009 |
| KPI-09 | Cadena de custodia | % de muestras con un registro de traslado por cada etapa física | `muestras completas / muestras con etapas físicas` | Calidad | 100 % | REQ-010 |
| KPI-10 | Completitud de metadatos | % de campos obligatorios completos | `1 − celdas vacías / celdas obligatorias` | Calidad | ≥ 98 % | REQ-011 |
| KPI-11 | Error de reportes | % de reportes corregidos tras emitirse | `reportes corregidos / reportes emitidos` | Calidad | ≤ 1 % | REQ-012 |
| KPI-12 | TAT por etapa | Horas promedio, mediana y p90 por etapa, y su % del total | `suma de horas por muestra y etapa → agregación por etapa` | Operaciones | vectorial | REQ-004 |

## Reglas de cálculo (decisiones que evitan malentendidos)

1. **Corte temporal**: todos los KPIs se calculan a la fecha de corte `as_of`; nada posterior existe.
2. **SLA sin sesgo de supervivencia (ADR-0003)**: una muestra abierta que ya superó las 240 h cuenta como incumplida. Una abierta que aún está en plazo *no se puede determinar* y se excluye del denominador.
3. **Horas corridas**: el SLA y el TAT usan horas de calendario, no hábiles.
4. **Repeticiones**: el TAT por etapa suma todos los intentos de una misma etapa para cada muestra.
5. **Rechazadas**: no entran en TAT, SLA ni repetición; sí en la tasa de rechazo.
6. **Custodia**: se exige un registro por cada etapa física a la que la muestra ingresó (primer intento), incluso si la etapa sigue en curso.
7. **KPI-12 es vectorial**: no tiene un único valor ni semáforo; se interpreta como tabla/gráfico.

## Cómo agregar un KPI nuevo

1. Redactar la historia de usuario y su criterio de aceptación.
2. Agregarlo a este diccionario y a la RTM.
3. Implementarlo en `kpis.py` con su prueba (la RTM debe citarla).
4. Registrar el cambio si altera el alcance aprobado.
