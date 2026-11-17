# ADR-0002 · Datos sintéticos con generador reproducible

- **Estado:** aceptado
- **Contexto:** no se pueden publicar datos de pacientes ni de un laboratorio real, y el repositorio es público.
- **Decisión:** generar datos sintéticos con una semilla fija (`seed=42`) y parámetros declarados en `config.py`. Solo se usan seudónimos (`P-#####`). Una prueba automática impide que aparezcan columnas de datos personales (REQ-015).
- **Consecuencias:**
  - ✅ Resultados reproducibles y sin riesgo de privacidad.
  - ⚠️ Los parámetros son supuestos, no mediciones: las conclusiones sobre «dónde está el cuello de botella» son una demostración, no un hallazgo (riesgo R-03).
- **Cómo se evoluciona:** al contar con datos reales anonimizados, reemplazar el generador por un conector y conservar las validaciones y los KPIs.
