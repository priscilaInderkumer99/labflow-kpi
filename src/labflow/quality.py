"""Validaciones de calidad de datos (ver REQ-013). Devuelven una tabla legible por personas."""
from __future__ import annotations

import pandas as pd

from . import config as C
from .dataset import Dataset
from .kpis import metadata_completeness

STAGE_ORDER = {s: i for i, s in enumerate(C.STAGES)}


def _row(name: str, passed: bool, severity: str, detail: str) -> dict:
    return {"check": name, "passed": bool(passed), "severity": severity, "detail": detail}


def run_all(ds: Dataset, metadata_threshold: float = 0.98) -> pd.DataFrame:
    s, e, c, r = ds.samples, ds.stage_events, ds.custody_events, ds.reports
    checks = []

    dup = int(s["sample_id"].duplicated().sum())
    checks.append(_row("sample_id único", dup == 0, "error", f"{dup} duplicados"))

    bad_stage = int((~e["stage"].isin(C.STAGES)).sum())
    checks.append(_row("etapas válidas", bad_stage == 0, "error", f"{bad_stage} eventos con etapa desconocida"))

    orphan_e = int((~e["sample_id"].isin(s["sample_id"])).sum())
    orphan_c = int((~c["sample_id"].isin(s["sample_id"])).sum())
    orphan_r = int((~r["sample_id"].isin(s["sample_id"])).sum())
    checks.append(
        _row("integridad referencial", orphan_e + orphan_c + orphan_r == 0, "error",
             f"huérfanos: eventos={orphan_e}, custodia={orphan_c}, reportes={orphan_r}")
    )

    done = e.dropna(subset=["finished_at"])
    inverted = int((done["finished_at"] < done["started_at"]).sum())
    checks.append(_row("fin >= inicio en cada etapa", inverted == 0, "error", f"{inverted} eventos con fechas invertidas"))

    ev = e.assign(_ord=e["stage"].map(STAGE_ORDER)).sort_values(["sample_id", "started_at"])
    prev_end = ev.groupby("sample_id")["finished_at"].shift()
    overlap = int((ev["started_at"] < prev_end).sum())
    checks.append(_row("etapas sin solapamiento", overlap == 0, "error", f"{overlap} solapamientos"))

    merged = r.merge(s[["sample_id", "received_at"]], on="sample_id")
    before = int((merged["issued_at"] < merged["received_at"]).sum())
    checks.append(_row("reporte posterior a la recepción", before == 0, "error", f"{before} reportes anteriores a la recepción"))

    future = int((e["started_at"] > ds.as_of).sum() + (r["issued_at"] > ds.as_of).sum())
    checks.append(_row("sin fechas futuras", future == 0, "error", f"{future} fechas posteriores al corte {ds.as_of:%Y-%m-%d}"))

    comp = metadata_completeness(ds)
    checks.append(_row("completitud de metadatos", comp >= metadata_threshold, "warning", f"{comp:.1%} (umbral {metadata_threshold:.0%})"))

    return pd.DataFrame(checks)


def assert_valid(ds: Dataset) -> pd.DataFrame:
    """Lanza ValueError si falla alguna validación de severidad 'error'."""
    res = run_all(ds)
    failed = res[(~res["passed"]) & (res["severity"] == "error")]
    if not failed.empty:
        raise ValueError("Validaciones de datos fallidas:\n" + failed.to_string(index=False))
    return res
