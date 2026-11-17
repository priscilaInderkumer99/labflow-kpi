# Guía de contribución

Este repositorio también es un ejercicio de **cómo se trabaja un proyecto funcional de punta a punta**. Por eso las reglas importan tanto como el código.

## Flujo de trabajo

1. Todo trabajo parte de un **issue** (plantillas: *Feature*, *Bug*, *Change request*).
2. Ramas: `feat/…`, `fix/…`, `docs/…`.
3. Commits convencionales: `feat:`, `fix:`, `docs:`, `test:`, `refactor:`, `chore:`.
4. Pull request con la plantilla completa; la CI debe estar en verde.
5. Cada release actualiza el [`CHANGELOG.md`](CHANGELOG.md) y se etiqueta (`v0.1.0`, …).

## Labels sugeridas

| Label | Uso |
|---|---|
| `must` `should` `could` | Prioridad MoSCoW del requerimiento |
| `bug` | Defecto (indicar severidad y fase de detección) |
| `change-request` | Cambio sobre un requerimiento aprobado |
| `docs` | Cambios solo de documentación |
| `uat` | Hallazgos de la ejecución de UAT |
| `risk` | Riesgo nuevo o actualizado |

## Definition of Ready (para tomar una historia)

- Tiene formato *Como / Quiero / Para* y un criterio de aceptación en Gherkin.
- Está priorizada y asociada a una persona y, si aplica, a un KPI.
- No depende de una decisión pendiente.

## Definition of Done

- [ ] Código y pruebas automatizadas (con valor esperado calculado a mano cuando es un KPI).
- [ ] La [RTM](docs/04-rtm.csv) cita el test; `test_rtm_references_existing_tests` pasa.
- [ ] El [diccionario de KPIs](docs/05-diccionario-kpis.md) y el [modelo de datos](docs/06-modelo-de-datos.md) están al día.
- [ ] Si cambia un requerimiento aprobado: registro en [`cambios.csv`](docs/registros/cambios.csv) (y ADR si altera un KPI).
- [ ] Si se encontró un defecto: registrado en [`defectos.csv`](docs/registros/defectos.csv).
- [ ] `make all` pasa y `docs/METRICAS_DEL_PROYECTO.md` está regenerado.

## Entorno local

```bash
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
make all
```
