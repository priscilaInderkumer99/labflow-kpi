# 03 · Requerimientos: historias de usuario y criterios de aceptación

Cada historia sigue el formato *Como / Quiero / Para* y tiene un criterio de aceptación en Gherkin.
La columna de pruebas enlaza con los tests automatizados; la fuente de verdad de la trazabilidad es [`04-rtm.csv`](../04-rtm.csv).

**Prioridad (MoSCoW):** Must = imprescindible · Should = importante · Could = deseable · Won't = fuera de esta versión.

## REQ-001 · TAT mediana de entrega

**Prioridad:** Must · **Persona:** Director · **KPI:** KPI-01 · **Línea base:** v0.1 · **Estado:** Implementado

> **Como** director del laboratorio, **quiero** ver la mediana del TAT (recepción → reporte), **para** conocer el tiempo típico de entrega.

```gherkin
Dado que hay 2 muestras completadas con TAT de 100 h y 300 h
Cuando consulto el KPI-01
Entonces veo 200 h
```

**Pruebas:** `tests/test_kpis.py::test_tat_median_and_p90` · **UAT:** UAT-01

## REQ-002 · TAT percentil 90

**Prioridad:** Must · **Persona:** Director · **KPI:** KPI-02 · **Línea base:** v0.1 · **Estado:** Implementado

> **Como** director del laboratorio, **quiero** ver el percentil 90 del TAT, **para** entender los casos lentos que la mediana esconde.

```gherkin
Dado que hay 2 muestras completadas con TAT de 100 h y 300 h
Cuando consulto el KPI-02
Entonces veo 280 h
```

**Pruebas:** `tests/test_kpis.py::test_tat_median_and_p90` · **UAT:** UAT-01

## REQ-003 · Cumplimiento de SLA (incluye abiertas vencidas)

**Prioridad:** Must · **Persona:** Director · **KPI:** KPI-03 · **Línea base:** v0.1 · **Estado:** Implementado

> **Como** director del laboratorio, **quiero** ver el % de muestras entregadas dentro de las 240 h, contando como incumplidas las abiertas ya vencidas, **para** no subestimar los atrasos por mirar solo lo ya entregado.

```gherkin
Dado 1 muestra entregada en 100 h, 1 en 300 h y 1 abierta hace 450 h
Y 1 abierta hace 50 h
Cuando consulto el KPI-03
Entonces veo 33 % y la muestra de 50 h queda excluida por no estar determinada
```

**Pruebas:** `tests/test_kpis.py::test_sla_compliance_counts_open_late_samples` · **UAT:** UAT-01

## REQ-004 · TAT por etapa y cuello de botella

**Prioridad:** Must · **Persona:** Operaciones · **KPI:** KPI-12 · **Línea base:** v0.1 · **Estado:** Implementado

> **Como** responsable de operaciones, **quiero** ver cuánto tiempo consume cada etapa y cuál concentra más, **para** priorizar dónde mejorar el proceso.

```gherkin
Dado un conjunto de muestras con REVISION como etapa más lenta
Cuando consulto el TAT por etapa
Entonces REVISION aparece como cuello de botella y los % de las etapas suman 100 %
```

**Pruebas:** `tests/test_kpis.py::test_tat_by_stage_identifies_bottleneck` · **UAT:** UAT-02

## REQ-005 · Tasa de rechazo de muestras

**Prioridad:** Should · **Persona:** Calidad · **KPI:** KPI-04 · **Línea base:** v0.1 · **Estado:** Implementado

> **Como** responsable de calidad, **quiero** ver el % de muestras rechazadas en recepción, **para** detectar problemas con los clientes o el transporte.

```gherkin
Dado 5 muestras recibidas, 1 rechazada
Cuando consulto el KPI-04
Entonces veo 20 %
```

**Pruebas:** `tests/test_kpis.py::test_rejection_rate` · **UAT:** UAT-03

## REQ-006 · Tasa de repetición (rework)

**Prioridad:** Should · **Persona:** Operaciones · **KPI:** KPI-05 · **Línea base:** v0.1 · **Estado:** Implementado

> **Como** responsable de operaciones, **quiero** ver el % de muestras con alguna etapa repetida, **para** cuantificar el retrabajo y su costo.

```gherkin
Dado 4 muestras no rechazadas, 1 con una etapa repetida
Cuando consulto el KPI-05
Entonces veo 25 %
```

**Pruebas:** `tests/test_kpis.py::test_rework_rate` · **UAT:** UAT-03

## REQ-007 · QC de laboratorio aprobado a la primera

**Prioridad:** Must · **Persona:** Calidad · **KPI:** KPI-06 · **Línea base:** v0.1 · **Estado:** Implementado

> **Como** responsable de calidad, **quiero** ver el % de controles de extracción y librería aprobados al primer intento, **para** evaluar la calidad del proceso de laboratorio.

```gherkin
Dado 8 controles de primer intento finalizados, 1 fallido
Cuando consulto el KPI-06
Entonces veo 87,5 %
```

**Pruebas:** `tests/test_kpis.py::test_first_pass_qc_rate` · **UAT:** UAT-03

## REQ-008 · Éxito del pipeline bioinformático

**Prioridad:** Should · **Persona:** Bioinformática · **KPI:** KPI-07 · **Línea base:** v0.1 · **Estado:** Implementado

> **Como** bioinformático, **quiero** ver el % de corridas del pipeline que terminan bien, **para** detectar inestabilidad antes de que impacte el TAT.

```gherkin
Dado 4 corridas finalizadas, 1 fallida
Cuando consulto el KPI-07
Entonces veo 75 %
```

**Pruebas:** `tests/test_kpis.py::test_pipeline_success_rate` · **UAT:** UAT-04

## REQ-009 · Backlog por etapa

**Prioridad:** Must · **Persona:** Operaciones · **KPI:** KPI-08 · **Línea base:** v0.1 · **Estado:** Implementado

> **Como** responsable de operaciones, **quiero** ver cuántas muestras hay en curso en cada etapa, **para** detectar acumulaciones y balancear carga.

```gherkin
Dado 1 muestra en curso en REVISION y 1 en SECUENCIACION
Cuando consulto el backlog
Entonces veo 1 y 1, y 0 en las demás etapas
```

**Pruebas:** `tests/test_kpis.py::test_backlog_by_stage` · **UAT:** UAT-04

## REQ-010 · Cadena de custodia completa

**Prioridad:** Must · **Persona:** Calidad · **KPI:** KPI-09 · **Línea base:** v0.1 · **Estado:** Implementado

> **Como** responsable de calidad, **quiero** ver el % de muestras con custodia completa y la lista de huecos, **para** corregir brechas antes de una auditoría.

```gherkin
Dado 5 muestras de las cuales 1 no tiene registro de traslado en LIBRERIA
Cuando consulto el KPI-09
Entonces veo 80 % y la lista con la muestra y la etapa faltante
```

**Pruebas:** `tests/test_custody_kpi.py::test_custody_completeness_reports_missing_samples`, `tests/test_custody_kpi.py::test_custody_is_100_percent_when_no_gaps` · **UAT:** UAT-05

## REQ-011 · Completitud de metadatos

**Prioridad:** Must · **Persona:** Calidad · **KPI:** KPI-10 · **Línea base:** v0.1 · **Estado:** Implementado

> **Como** responsable de calidad, **quiero** ver el % de campos obligatorios completos y qué muestras tienen huecos, **para** asegurar que cada resultado sea interpretable.

```gherkin
Dado 5 muestras con 5 campos obligatorios y 1 campo vacío
Cuando consulto el KPI-10
Entonces veo 96 % y el detalle muestra qué campo falta y en qué muestra
```

**Pruebas:** `tests/test_quality.py::test_metadata_completeness_kpi` · **UAT:** UAT-05

## REQ-012 · Tasa de error de reportes

**Prioridad:** Should · **Persona:** Calidad · **KPI:** KPI-11 · **Línea base:** v0.1 · **Estado:** Implementado

> **Como** responsable de calidad, **quiero** ver el % de reportes corregidos tras su emisión, **para** medir la calidad del entregable final.

```gherkin
Dado 2 reportes emitidos, 1 corregido
Cuando consulto el KPI-11
Entonces veo 50 %
```

**Pruebas:** `tests/test_kpis.py::test_report_error_rate` · **UAT:** UAT-06

## REQ-013 · Validaciones automáticas de calidad de datos

**Prioridad:** Must · **Persona:** Calidad · **KPI:** — · **Línea base:** v0.1 · **Estado:** Implementado

> **Como** responsable de calidad, **quiero** que el sistema valide unicidad, fechas y referencias antes de calcular KPIs, **para** no tomar decisiones con datos inconsistentes.

```gherkin
Dado un dataset con un sample_id duplicado
Cuando ejecuto las validaciones
Entonces falla «sample_id único» y se informa cuántos duplicados hay
```

**Pruebas:** `tests/test_quality.py::test_quality_checks_pass_on_generated_data`, `tests/test_quality.py::test_quality_detects_duplicate_ids`, `tests/test_quality.py::test_quality_detects_inverted_dates` · **UAT:** UAT-07

## REQ-014 · Datos sintéticos reproducibles

**Prioridad:** Should · **Persona:** Equipo · **KPI:** — · **Línea base:** v0.1 · **Estado:** Implementado

> **Como** miembro del equipo, **quiero** regenerar exactamente los mismos datos con la misma semilla, **para** reproducir resultados y depurar.

```gherkin
Dado la misma semilla y parámetros
Cuando genero dos veces el dataset
Entonces ambos son idénticos; con otra semilla difieren
```

**Pruebas:** `tests/test_generator.py::test_generator_is_reproducible` · **UAT:** N/A

## REQ-015 · Sin datos personales reales (privacidad)

**Prioridad:** Must · **Persona:** Calidad · **KPI:** — · **Línea base:** v0.5 · **Estado:** Implementado

> **Como** responsable de calidad, **quiero** que los datos contengan solo seudónimos y ninguna columna de datos personales, **para** cumplir privacidad y poder publicar el repositorio.

```gherkin
Dado un dataset generado
Cuando reviso sus columnas
Entonces no hay nombre, documento, email ni teléfono y patient_ref sigue el formato P-#####
```

**Pruebas:** `tests/test_generator.py::test_generator_has_no_real_pii_columns` · **UAT:** UAT-07

## REQ-016 · Dashboard con una vista por persona

**Prioridad:** Must · **Persona:** Todos · **KPI:** — · **Línea base:** v0.1 · **Estado:** Implementado

> **Como** usuario del laboratorio, **quiero** una vista con solo los KPIs relevantes para mi rol, **para** encontrar rápido lo que necesito sin ruido.

```gherkin
Dado que abro el dashboard
Cuando elijo la vista «Responsable de calidad»
Entonces veo los KPIs de calidad con semáforo y sus objetivos
```

**Pruebas:** `tests/test_dashboard.py::test_dashboard_renders_each_persona_view` · **UAT:** UAT-08

## REQ-017 · Trazabilidad verificada por CI

**Prioridad:** Should · **Persona:** Equipo · **KPI:** — · **Línea base:** v0.1 · **Estado:** Implementado

> **Como** líder del proyecto, **quiero** que la integración continua falle si la RTM cita un test inexistente, **para** mantener la trazabilidad confiable.

```gherkin
Dado una RTM que cita un test que no existe
Cuando corre la integración continua
Entonces el build falla indicando el requerimiento y el test faltante
```

**Pruebas:** `tests/test_project_metrics.py::test_rtm_references_existing_tests` · **UAT:** N/A

## REQ-018 · Semáforo de KPIs contra objetivo

**Prioridad:** Should · **Persona:** Director · **KPI:** — · **Línea base:** v0.1 · **Estado:** Implementado

> **Como** director del laboratorio, **quiero** que cada KPI muestre OK o ALERTA según su objetivo, **para** ver de un vistazo qué atender.

```gherkin
Dado un SLA de 33 % y un objetivo de 95 %
Cuando consulto el snapshot de KPIs
Entonces KPI-03 aparece en ALERTA y el backlog como informativo
```

**Pruebas:** `tests/test_kpis.py::test_kpi_snapshot_flags_alerts` · **UAT:** UAT-06

## REQ-019 · Exportar CSV de muestras con custodia incompleta

**Prioridad:** Could · **Persona:** Calidad · **KPI:** KPI-09 · **Línea base:** v0.5 · **Estado:** Backlog

> **Como** responsable de calidad, **quiero** exportar la lista de huecos de custodia a CSV, **para** enviarla al equipo de laboratorio para su corrección.

```gherkin
Dado que hay huecos de custodia
Cuando presiono «Exportar»
Entonces descargo un CSV con muestra, etapa y fecha
```

**Pruebas:** _sin prueba asociada todavía_

## REQ-020 · Integración con un LIMS real

**Prioridad:** Won't · **Persona:** Director · **KPI:** — · **Línea base:** v0.5 · **Estado:** Descartado

> **Como** director del laboratorio, **quiero** conectar el dashboard al LIMS productivo, **para** eliminar la carga manual.

```gherkin
(Fuera de alcance de la versión 1: ver CR-004 y docs/01-business-case.md)
```

**Pruebas:** _sin prueba asociada todavía_
