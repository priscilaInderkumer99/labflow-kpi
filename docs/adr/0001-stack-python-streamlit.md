# ADR-0001 · Stack: Python + pandas + Streamlit

- **Estado:** aceptado
- **Contexto:** el proyecto debe ser ejecutable por cualquier persona en minutos, legible para un perfil funcional/bioinformático y fácil de probar.
- **Decisión:** Python 3.10+, pandas para la capa de KPIs, Streamlit para el dashboard y pytest para las pruebas. Los CSV son el formato de intercambio.
- **Consecuencias:**
  - ✅ Un solo lenguaje habitual en bioinformática; arranque con `pip install -e ".[dev]"`.
  - ✅ El dashboard se prueba automáticamente con `streamlit.testing`.
  - ⚠️ pandas no escala a millones de eventos; si fuera necesario, migrar la capa de KPIs a SQL/DuckDB sin cambiar el diccionario.
- **Alternativas consideradas:** dbt + Metabase (más cercano a un entorno de datos real, pero más pesado de instalar para una entrevista); Power BI (no reproducible desde el repositorio).
