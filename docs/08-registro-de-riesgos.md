# 08 · Registro de riesgos (FMEA simplificado)

**RPN = Severidad × Ocurrencia × Detección**, cada factor de 1 a 10 (en *Detección*, 10 = muy difícil de detectar). Se atacan primero los RPN más altos.

| ID | Riesgo | Causa | Efecto | S | O | D | **RPN** | Mitigación | Estado |
|---|---|---|---|---|---|---|---|---|---|
| R-02 | Sesgo de supervivencia en el SLA | Solo se miden las muestras ya entregadas | El SLA parece mejor de lo que es | 8 | 6 | 5 | **240** | Contar las abiertas vencidas como incumplidas (ADR-0003, CR-002) y probarlo con un dataset mínimo | Mitigado |
| R-07 | Crecimiento del alcance (scope creep) | Pedidos de nuevos KPIs o integraciones | Retraso y pérdida de foco | 6 | 6 | 4 | **144** | Control de cambios con análisis de impacto; MoSCoW; rechazar fuera de alcance (CR-004) | Activo |
| R-01 | Definiciones de KPI ambiguas | Cada área entiende «completada» a su manera | Discusiones y números en conflicto | 7 | 5 | 4 | **140** | Diccionario único con fórmula y dueño; revisión con stakeholders | Mitigado |
| R-03 | Datos sintéticos poco realistas | Parámetros inventados | Conclusiones que no se sostienen con datos reales | 5 | 6 | 4 | **120** | Documentar supuestos; parámetros en `config.py`; contrastar con datos reales cuando existan | Aceptado |
| R-08 | Mala interpretación del dashboard | Sin contexto del objetivo ni de la fórmula | Decisiones erróneas | 5 | 4 | 6 | **120** | Objetivo visible en cada KPI; enlace al diccionario; UAT con usuarios | Activo |
| R-05 | Regresión silenciosa de un KPI | Cambio de código sin prueba | KPI incorrecto en producción | 7 | 5 | 3 | **105** | Pruebas con valores esperados calculados a mano; CI obligatoria | Mitigado |
| R-04 | Metadatos incompletos sin alerta | Validación ausente | Resultados no interpretables | 8 | 4 | 3 | **96** | KPI-10 y validación con umbral; lista de huecos en el dashboard | Mitigado |
| R-06 | Filtración de datos personales reales | Alguien carga datos reales al repo | Incumplimiento de privacidad | 10 | 2 | 3 | **60** | Solo seudónimos; prueba automática de columnas prohibidas (REQ-015); `.gitignore` de datos | Mitigado |

## Cómo se usa

- Se revisa al inicio de cada hito y cuando un cambio lo afecta.
- Un riesgo mitigado deja evidencia (ADR, prueba o CR) y se vuelve a puntuar: el RPN residual debería bajar.
- Los riesgos nuevos se agregan con su RPN antes de decidir.
