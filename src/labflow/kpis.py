"""Capa de KPIs. Cada función implementa una definición de docs/05-diccionario-kpis.md."""
from __future__ import annotations

import numpy as np
import pandas as pd

from . import config as C
from .dataset import Dataset


def _non_rejected(ds: Dataset) -> pd.DataFrame:
    return ds.samples[~ds.samples["rejected"].astype(bool)]


def _hours(delta: pd.Series) -> pd.Series:
    return delta.dt.total_seconds() / 3600


# ---------------------------------------------------------------- KPI-01/02: TAT
def tat_hours(ds: Dataset) -> pd.Series:
    """Horas entre recepción y emisión del reporte, solo para muestras completadas."""
    r = ds.reports.merge(ds.samples[["sample_id", "received_at"]], on="sample_id")
    return pd.Series(_hours(r["issued_at"] - r["received_at"]).to_numpy(), index=r["sample_id"].to_numpy())


def tat_summary(ds: Dataset) -> dict:
    t = tat_hours(ds)
    if t.empty:
        return {"median": np.nan, "p90": np.nan, "mean": np.nan, "n": 0}
    return {"median": float(t.median()), "p90": float(t.quantile(0.9)), "mean": float(t.mean()), "n": int(len(t))}


# ---------------------------------------------------------------- KPI-03: SLA
def sla_breakdown(ds: Dataset, sla_hours: float = C.SLA_HOURS) -> dict:
    """Cuenta muestras cumplidas / tarde / abiertas-ya-vencidas.

    Las muestras abiertas que ya superaron el SLA cuentan como incumplidas (ADR-0003):
    si solo se miraran las completadas habría sesgo de supervivencia.
    """
    s = _non_rejected(ds).set_index("sample_id")
    tat = tat_hours(ds)
    open_ids = s.index.difference(tat.index)
    age = _hours(ds.as_of - s.loc[open_ids, "received_at"])
    return {
        "on_time": int((tat <= sla_hours).sum()),
        "late_completed": int((tat > sla_hours).sum()),
        "late_open": int((age > sla_hours).sum()),
        "undetermined": int((age <= sla_hours).sum()),
    }


def sla_compliance(ds: Dataset, sla_hours: float = C.SLA_HOURS) -> float:
    b = sla_breakdown(ds, sla_hours)
    determinate = b["on_time"] + b["late_completed"] + b["late_open"]
    return b["on_time"] / determinate if determinate else float("nan")


# ---------------------------------------------------------------- KPI-12: TAT por etapa
def tat_by_stage(ds: Dataset) -> pd.DataFrame:
    e = ds.stage_events.dropna(subset=["finished_at"]).copy()
    e["hours"] = _hours(e["finished_at"] - e["started_at"])
    per_sample = e.groupby(["sample_id", "stage"])["hours"].sum().reset_index()
    out = per_sample.groupby("stage")["hours"].agg(
        mean_hours="mean", median_hours="median", p90_hours=lambda x: x.quantile(0.9), n="count"
    )
    out = out.reindex([s for s in C.STAGES if s in out.index])
    out["share"] = out["mean_hours"] / out["mean_hours"].sum()
    return out


def bottleneck_stage(ds: Dataset) -> str:
    return str(tat_by_stage(ds)["mean_hours"].idxmax())


# ---------------------------------------------------------------- KPI-04..07
def rejection_rate(ds: Dataset) -> float:
    return float(ds.samples["rejected"].astype(bool).mean())


def rework_rate(ds: Dataset) -> float:
    """Muestras (no rechazadas) con al menos una etapa repetida."""
    base = _non_rejected(ds)["sample_id"]
    repeated = ds.stage_events.loc[ds.stage_events["attempt"] > 1, "sample_id"].unique()
    return float(base.isin(repeated).mean()) if len(base) else float("nan")


def first_pass_qc_rate(ds: Dataset) -> float:
    e = ds.stage_events
    q = e[e["stage"].isin(C.QC_STAGES) & (e["attempt"] == 1) & e["outcome"].isin(["ok", "qc_fail"])]
    return float((q["outcome"] == "ok").mean()) if len(q) else float("nan")


def pipeline_success_rate(ds: Dataset) -> float:
    e = ds.stage_events
    p = e[(e["stage"] == "PIPELINE") & e["outcome"].isin(["ok", "failed"])]
    return float((p["outcome"] == "ok").mean()) if len(p) else float("nan")


# ---------------------------------------------------------------- KPI-08: backlog
def backlog_by_stage(ds: Dataset) -> pd.Series:
    e = ds.stage_events
    counts = e[e["outcome"] == "in_progress"].groupby("stage").size()
    return counts.reindex(C.STAGES, fill_value=0)


# ---------------------------------------------------------------- KPI-09: custodia
def custody_completeness(ds: Dataset) -> tuple[float, pd.DataFrame]:
    """(% de muestras con custodia completa, tabla de huecos). Una muestra está completa si tiene
    un evento de custodia por cada etapa física a la que ingresó."""
    e = ds.stage_events
    expected = e[e["stage"].isin(C.PHYSICAL_STAGES) & (e["attempt"] == 1)][["sample_id", "stage"]].drop_duplicates()
    actual = ds.custody_events[["sample_id", "stage"]].drop_duplicates().assign(_has=True)
    m = expected.merge(actual, how="left", on=["sample_id", "stage"])
    m["_has"] = m["_has"].notna()
    per_sample = m.groupby("sample_id")["_has"].all()
    rate = float(per_sample.mean()) if len(per_sample) else float("nan")
    missing = m.loc[~m["_has"], ["sample_id", "stage"]].reset_index(drop=True)
    return rate, missing


# ---------------------------------------------------------------- KPI-10: metadatos
def metadata_completeness(ds: Dataset) -> float:
    cells = ds.samples[C.REQUIRED_FIELDS]
    return float(1 - cells.isna().sum().sum() / cells.size) if cells.size else float("nan")


def metadata_gaps(ds: Dataset) -> pd.DataFrame:
    s = ds.samples[["sample_id", *C.REQUIRED_FIELDS]]
    gaps = s[s[C.REQUIRED_FIELDS].isna().any(axis=1)].copy()
    gaps["campos_faltantes"] = gaps[C.REQUIRED_FIELDS].isna().apply(
        lambda r: ", ".join(r.index[r]), axis=1
    )
    return gaps[["sample_id", "campos_faltantes"]].reset_index(drop=True)


# ---------------------------------------------------------------- KPI-11: reportes
def report_error_rate(ds: Dataset) -> float:
    return float(ds.reports["corrected"].astype(bool).mean()) if len(ds.reports) else float("nan")


# ---------------------------------------------------------------- Snapshot con umbrales
# (id, nombre, unidad, objetivo, comparador)
KPI_SPECS = [
    ("KPI-01", "TAT mediana", "h", 168.0, "<="),
    ("KPI-02", "TAT p90", "h", 240.0, "<="),
    ("KPI-03", "Cumplimiento de SLA", "%", 0.95, ">="),
    ("KPI-04", "Tasa de rechazo", "%", 0.05, "<="),
    ("KPI-05", "Tasa de repetición", "%", 0.10, "<="),
    ("KPI-06", "QC aprobado a la primera", "%", 0.92, ">="),
    ("KPI-07", "Éxito del pipeline", "%", 0.97, ">="),
    ("KPI-08", "Backlog total", "muestras", None, None),
    ("KPI-09", "Cadena de custodia completa", "%", 1.00, ">="),
    ("KPI-10", "Completitud de metadatos", "%", 0.98, ">="),
    ("KPI-11", "Error de reportes", "%", 0.01, "<="),
]


def _status(value: float, target, cmp) -> str:
    if value is None or (isinstance(value, float) and np.isnan(value)):
        return "SIN DATOS"
    if target is None:
        return "INFO"
    ok = value >= target if cmp == ">=" else value <= target
    return "OK" if ok else "ALERTA"


def kpi_snapshot(ds: Dataset) -> pd.DataFrame:
    tat = tat_summary(ds)
    values = {
        "KPI-01": tat["median"],
        "KPI-02": tat["p90"],
        "KPI-03": sla_compliance(ds),
        "KPI-04": rejection_rate(ds),
        "KPI-05": rework_rate(ds),
        "KPI-06": first_pass_qc_rate(ds),
        "KPI-07": pipeline_success_rate(ds),
        "KPI-08": float(backlog_by_stage(ds).sum()),
        "KPI-09": custody_completeness(ds)[0],
        "KPI-10": metadata_completeness(ds),
        "KPI-11": report_error_rate(ds),
    }
    rows = [
        {
            "kpi_id": k, "kpi": name, "value": values[k], "unit": unit,
            "target": target, "comparator": cmp, "status": _status(values[k], target, cmp),
        }
        for k, name, unit, target, cmp in KPI_SPECS
    ]
    return pd.DataFrame(rows)
