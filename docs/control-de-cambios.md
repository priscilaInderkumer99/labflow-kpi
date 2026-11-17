# Control de cambios

> ⚠️ Los registros de `docs/registros/` son **ejemplos ilustrativos** para mostrar el proceso. Reemplazalos por los cambios y defectos reales a medida que desarrolles el proyecto.

## Proceso

1. **Solicitud**: se abre un issue con la plantilla *Change request* (qué cambia y por qué).
2. **Análisis de impacto**: requerimientos, KPIs, pruebas y documentos afectados; esfuerzo estimado.
3. **Decisión**: Aprobado / Rechazado / Diferido, con el motivo. Los cambios aprobados se registran en [`registros/cambios.csv`](registros/cambios.csv).
4. **Implementación**: se actualizan la RTM, el diccionario de KPIs y los tests en el mismo pull request.
5. **Verificación**: la CI debe pasar y `make metrics` actualiza las métricas del proyecto.

Un cambio que altera el comportamiento de un KPI requiere además un ADR (ver [`adr/`](adr/)).

## Registro de cambios

| CR | Fecha | Req. | Tipo | Descripción | Estado |
|---|---|---|---|---|---|
| CR-001 | 2026-11-23 | REQ-015 | Agregado | Agregar requisito de privacidad: solo seudónimos, sin columnas de datos personales | **Aprobado** |
| CR-002 | 2026-11-30 | REQ-003 | Modificado | El SLA cuenta como incumplidas las muestras abiertas ya vencidas | **Aprobado** |
| CR-003 | 2026-12-02 | REQ-019 | Agregado | Exportar a CSV las muestras con custodia incompleta | **Aprobado** |
| CR-004 | 2026-12-05 | REQ-020 | Agregado | Integrar con un LIMS productivo | **Rechazado** |

La **volatilidad de requerimientos** se calcula automáticamente en [`METRICAS_DEL_PROYECTO.md`](METRICAS_DEL_PROYECTO.md): cambios aprobados posteriores a la línea base v0.1, divididos por los requerimientos de esa línea base.
