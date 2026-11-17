"""Dashboard de LabFlow KPI. Una vista por persona (REQ-016).

Ejecutar:  streamlit run dashboard/app.py
"""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd
import streamlit as st

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from labflow import config as C  # noqa: E402
from labflow import kpis, quality  # noqa: E402
from labflow.dataset import Dataset  # noqa: E402
from labflow.generator import generate  # noqa: E402

st.set_page_config(page_title="LabFlow KPI", page_icon="🧬", layout="wide")

# KPIs que ve cada persona (ver docs/02-personas-y-procesos.md)
PERSONAS = {
    "Director del laboratorio": ["KPI-01", "KPI-02", "KPI-03", "KPI-05", "KPI-08"],
    "Responsable de calidad": ["KPI-06", "KPI-09", "KPI-10", "KPI-11", "KPI-04"],
    "Operaciones / Bioinformática": ["KPI-05", "KPI-07", "KPI-08", "KPI-06"],
}
ICON = {"OK": "🟢", "ALERTA": "🔴", "INFO": "⚪", "SIN DATOS": "⚫"}


@st.cache_resource
def get_dataset() -> Dataset:
    try:
        return Dataset.load(C.DATA_DIR)
    except FileNotFoundError:
        return generate()


def fmt(row: pd.Series) -> str:
    v = row["value"]
    if pd.isna(v):
        return "n/d"
    return f"{v:,.0f} {row['unit']}" if row["unit"] in ("h", "muestras") else f"{v:.1%}"


def target_text(row: pd.Series) -> str | None:
    if pd.isna(row["target"]):
        return None
    t = f"{row['target']:.0%}" if row["unit"] == "%" else f"{row['target']:g} {row['unit']}"
    return f"objetivo {row['comparator']} {t}"


ds = get_dataset()
snap = kpis.kpi_snapshot(ds).set_index("kpi_id")

st.title("🧬 LabFlow KPI")
st.caption(f"Datos sintéticos · corte al {ds.as_of:%d/%m/%Y} · {len(ds.samples)} muestras")

persona = st.sidebar.radio("Vista", list(PERSONAS))
st.sidebar.markdown("**Semáforo**: 🟢 cumple · 🔴 fuera de umbral · ⚪ informativo")
st.sidebar.info("Las definiciones y fórmulas están en `docs/05-diccionario-kpis.md`.")

st.subheader(persona)
ids = PERSONAS[persona]
cols = st.columns(len(ids))
for col, kid in zip(cols, ids):
    r = snap.loc[kid]
    col.metric(f"{ICON[r['status']]} {r['kpi']}", fmt(r), help=target_text(r))
    if target_text(r):
        col.caption(target_text(r))

st.divider()

if persona.startswith("Director"):
    left, right = st.columns(2)
    stage = kpis.tat_by_stage(ds)
    left.markdown(f"**¿Dónde se va el tiempo?** Cuello de botella: `{kpis.bottleneck_stage(ds)}`")
    left.bar_chart(stage["mean_hours"].rename("horas promedio por etapa"))
    b = kpis.sla_breakdown(ds)
    right.markdown("**Cumplimiento de SLA (muestras determinadas)**")
    right.dataframe(
        pd.DataFrame(
            {"Estado": ["En plazo", "Completadas fuera de plazo", "Abiertas ya vencidas", "Aún en plazo (excluidas)"],
             "Muestras": [b["on_time"], b["late_completed"], b["late_open"], b["undetermined"]]}
        ),
        hide_index=True,
        use_container_width=True,
    )
    tat = kpis.tat_hours(ds)
    st.markdown("**Distribución del TAT (horas)**")
    st.bar_chart(pd.cut(tat, bins=range(0, int(tat.max()) + 24, 24)).value_counts().sort_index().rename("muestras").reset_index(drop=True))

elif persona.startswith("Responsable"):
    rate, missing = kpis.custody_completeness(ds)
    left, right = st.columns(2)
    left.markdown(f"**Cadena de custodia: huecos detectados** ({len(missing)} registros)")
    left.dataframe(missing, hide_index=True, use_container_width=True, height=260)
    right.markdown("**Metadatos incompletos**")
    right.dataframe(kpis.metadata_gaps(ds), hide_index=True, use_container_width=True, height=260)
    st.markdown("**Validaciones de calidad de datos**")
    checks = quality.run_all(ds)
    checks["resultado"] = checks["passed"].map({True: "✅", False: "❌"})
    st.dataframe(checks[["resultado", "check", "severity", "detail"]], hide_index=True, use_container_width=True)

else:
    left, right = st.columns(2)
    left.markdown("**Backlog por etapa (muestras en curso)**")
    left.bar_chart(kpis.backlog_by_stage(ds).rename("muestras"))
    right.markdown("**Tiempo por etapa (media, mediana, p90)**")
    right.dataframe(kpis.tat_by_stage(ds).round(1), use_container_width=True)
    st.markdown("**Todos los KPIs**")
    show = snap.reset_index()[["kpi_id", "kpi", "value", "unit", "target", "status"]]
    st.dataframe(show, hide_index=True, use_container_width=True)
