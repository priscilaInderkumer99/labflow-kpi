# Métricas del proyecto

> Generado automáticamente por `python -m labflow.cli project-metrics` (versión 0.1.0).
> No editar a mano: se calcula desde `docs/04-rtm.csv` y `docs/registros/`.

| Métrica | Valor | Referencia | Cómo se calcula |
|---|---|---|---|
| Requerimientos activos | 19 | — | RTM sin los descartados |
| Implementados / en backlog | 18 / 1 | — | Estado en la RTM |
| Cobertura de trazabilidad (todos) | 94.7% | > 95 % | Req. con test / activos |
| Cobertura de trazabilidad (Must) | 100.0% | 100 % | Req. Must con test / Must |
| Volatilidad de requerimientos | 17.6% | < 10–15 % | Cambios aprobados / req. de línea base |
| Defectos totales | 8 | — | `docs/registros/defectos.csv` |
| DDP (detección antes de release) | 87.5% | > 90 % | (total − post-release) / total |
| Defect leakage | 12.5% | < 5–10 % | post-release / total |
| Defectos abiertos | 0 | 0 críticos al release | Estado ≠ Cerrado |
| Pass rate de pruebas | 100.0% | ≥ 95 % | 25 tests, 0 fallidos |

Un valor por debajo de la referencia no es un error del reporte: es información para decidir.
