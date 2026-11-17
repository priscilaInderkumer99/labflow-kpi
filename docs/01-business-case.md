# 01 · Business case

> Escenario **ficticio**: *GenoLab*, un laboratorio de genómica clínica que secuencia paneles y exomas. Todos los datos del repositorio son sintéticos.

## 1. Contexto y problema

GenoLab promete entregar cada reporte en **10 días corridos** (240 h) desde la recepción de la muestra. Hoy entre el **15 % y el 20 %** de los reportes se entrega tarde y nadie puede decir en qué etapa se pierde el tiempo. Además:

- Las repeticiones por fallas de QC y los reprocesos del pipeline se descubren al final del mes, no cuando ocurren.
- Los huecos de cadena de custodia y de metadatos aparecen recién durante las auditorías.
- Cada área lleva su propia planilla con definiciones distintas de «muestra completada» o «dentro de plazo».

**Consecuencia:** el director decide sin datos confiables, calidad llega a las auditorías con sorpresas y operaciones apaga incendios.

## 2. Objetivos (SMART)

| # | Objetivo | Medida de éxito |
|---|---|---|
| O1 | Visibilizar el TAT total y por etapa en un dashboard | Disponible con datos al corte diario; identifica la etapa que concentra más del 30 % del tiempo |
| O2 | Unificar la definición de los KPIs críticos | 12 KPIs con definición, fórmula, dueño y umbral en el [diccionario](05-diccionario-kpis.md) |
| O3 | Detectar inconsistencias de datos antes de calcular KPIs | ≥ 7 validaciones automáticas, ejecutadas en cada build |
| O4 | Hacer el proyecto auditable | Cobertura de trazabilidad Must = 100 %, verificada por CI |

> **Qué no es un objetivo:** mejorar el TAT. Este proyecto *mide y expone*; mejorar el proceso es una decisión posterior del negocio.

## 3. Alcance

**Dentro (v1.0)**
- Modelo de datos del flujo recepción → reporte y generador de datos sintéticos.
- Capa de KPIs, validaciones de calidad de datos y dashboard por persona.
- Documentación funcional completa, plan de pruebas/UAT y registro de riesgos.

**Fuera (v1.0)**
- Integración con un LIMS real o con instrumentos (ver CR-004, rechazado).
- Datos de pacientes reales, interpretación clínica de variantes, facturación.
- Alertas en tiempo real y notificaciones (posible v2).

## 4. Stakeholders

| Rol | Interés | Influencia | Cómo participa |
|---|---|---|---|
| Director del laboratorio | Cumplir SLA, decidir inversiones | Alta | Patrocinador; aprueba alcance y KPIs |
| Responsable de calidad | Auditorías, trazabilidad, integridad de datos | Alta | Dueño de KPIs de calidad; ejecuta UAT |
| Responsable de operaciones | Flujo de trabajo, carga y capacidad | Media | Dueño de KPIs de proceso |
| Bioinformático | Estabilidad del pipeline | Media | Provee eventos de pipeline; valida KPI-07 |
| Analista funcional (vos) | Que lo construido responda a la necesidad | — | Relevamiento, especificación, UAT, métricas |

## 5. Supuestos y restricciones

- **Supuestos:** existe un registro de eventos por etapa con fecha de inicio/fin; el SLA es de 240 h corridas (no hábiles).
- **Restricciones:** sin datos reales ni acceso a sistemas productivos; stack open source; documentación en español.

## 6. Beneficios esperados y cómo se medirían

| Beneficio | Indicador | Línea base (sintética) | Meta |
|---|---|---|---|
| Menos tiempo armando reportes manuales | Horas/mes de consolidación | A medir con el equipo | −80 % |
| Detección temprana de retrabajo | Tiempo hasta detectar una repetición | Fin de mes | Mismo día |
| Preparación de auditorías | % de muestras con custodia completa | Sin dato | ≥ 99 % |

**Costo de oportunidad (referencia):** si 16 % de 600 muestras/trimestre se retrasa y cada retraso cuesta *X* en penalidades o reprocesos, el costo trimestral es `≈ 96 · X`. El ROI se calcula como `(beneficio − costo) / costo`.

## 7. Criterios de éxito de la v1.0

1. Todos los requerimientos *Must* implementados, trazados y con UAT aceptado.
2. 0 defectos críticos o altos abiertos.
3. `make all` corre de punta a punta en una máquina limpia.
4. La documentación permite que una persona nueva entienda el sistema en menos de 30 minutos.

## 8. Riesgos principales

Ver el [registro de riesgos](08-registro-de-riesgos.md): ambigüedad en las definiciones de KPI, sesgo de supervivencia en el SLA y scope creep son los de mayor prioridad.
