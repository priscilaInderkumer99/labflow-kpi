# ADR-0003 · El SLA cuenta las muestras abiertas ya vencidas

- **Estado:** aceptado (origen: CR-002, DEF-004)
- **Contexto:** la primera versión del KPI-03 calculaba el cumplimiento solo sobre muestras ya entregadas. Una muestra atascada en revisión durante 20 días no afectaba el KPI hasta que se entregaba, por lo que el SLA parecía mejor de lo real (sesgo de supervivencia).
- **Decisión:** las muestras abiertas cuyo tiempo desde la recepción ya superó el SLA cuentan como **incumplidas**. Las abiertas que aún están en plazo no se pueden determinar y se excluyen del denominador.
- **Consecuencias:**
  - ✅ El KPI refleja la realidad y reacciona apenas una muestra se vence.
  - ⚠️ Una muestra vencida que luego se entrega pasa de «abierta vencida» a «completada fuera de plazo»: sigue contando como incumplida, así que el KPI no mejora artificialmente al cerrarla. El desglose del dashboard muestra los cuatro grupos para que se entienda.
- **Verificación:** `test_sla_compliance_counts_open_late_samples`.
