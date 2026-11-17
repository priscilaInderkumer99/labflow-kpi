"""Métricas del PROPIO proyecto: aplica las métricas de analista funcional al repo."""
from __future__ import annotations

import re
import xml.etree.ElementTree as ET
from pathlib import Path

import pandas as pd

from . import __version__


def load_rtm(path: Path | str) -> pd.DataFrame:
    return pd.read_csv(path, dtype=str).fillna("")


def _active(rtm: pd.DataFrame) -> pd.DataFrame:
    return rtm[rtm["estado"] != "Descartado"]


def traceability_coverage(rtm: pd.DataFrame, priority: str | None = None) -> float:
    """Requerimientos activos con al menos un test asociado / requerimientos activos."""
    a = _active(rtm)
    if priority:
        a = a[a["prioridad"] == priority]
    return float((a["test_id"].str.strip() != "").mean()) if len(a) else float("nan")


def requirement_volatility(rtm: pd.DataFrame, cambios: pd.DataFrame) -> float:
    """Cambios aprobados posteriores a la línea base / requerimientos de la línea base (v0.1)."""
    base = int((rtm["baseline"] == "v0.1").sum())
    approved = int((cambios["estado"] == "Aprobado").sum())
    return approved / base if base else float("nan")


def defect_metrics(defectos: pd.DataFrame) -> dict:
    total = len(defectos)
    leaked = int((defectos["detectado_en"] == "post-release").sum())
    return {
        "total": total,
        "leaked": leaked,
        "ddp": (total - leaked) / total if total else float("nan"),
        "leakage": leaked / total if total else float("nan"),
        "open": int((defectos["estado"] != "Cerrado").sum()),
    }


def junit_pass_rate(path: Path | str) -> dict | None:
    p = Path(path)
    if not p.exists():
        return None
    root = ET.parse(p).getroot()
    suites = [root] if root.tag == "testsuite" else list(root.iter("testsuite"))
    tests = sum(int(s.get("tests", 0)) for s in suites)
    bad = sum(int(s.get("failures", 0)) + int(s.get("errors", 0)) for s in suites)
    skipped = sum(int(s.get("skipped", 0)) for s in suites)
    executed = tests - skipped
    return {"tests": tests, "failed": bad, "skipped": skipped,
            "pass_rate": (executed - bad) / executed if executed else float("nan")}


def referenced_tests(rtm: pd.DataFrame) -> list[tuple[str, str, str]]:
    """Devuelve (req_id, archivo, función) para cada test citado en la RTM."""
    out = []
    for _, row in rtm.iterrows():
        for ref in filter(None, (x.strip() for x in row["test_id"].split(";"))):
            path, _, func = ref.partition("::")
            out.append((row["req_id"], path, func))
    return out


def check_rtm_integrity(rtm: pd.DataFrame, root: Path | str) -> list[str]:
    """Lista de problemas: archivos o funciones de test que la RTM cita pero no existen."""
    root, problems = Path(root), []
    for req, path, func in referenced_tests(rtm):
        f = root / path
        if not f.exists():
            problems.append(f"{req}: no existe el archivo {path}")
        elif not re.search(rf"^def {re.escape(func)}\(", f.read_text(encoding="utf-8"), re.M):
            problems.append(f"{req}: no existe {func} en {path}")
    return problems


def _pct(x: float) -> str:
    return "n/d" if pd.isna(x) else f"{x:.1%}"


def render_markdown(rtm, cambios, defectos, junit) -> str:
    d = defect_metrics(defectos)
    a = _active(rtm)
    by_status = a["estado"].value_counts().to_dict()
    lines = [
        "# Métricas del proyecto",
        "",
        f"> Generado automáticamente por `python -m labflow.cli project-metrics` (versión {__version__}).",
        "> No editar a mano: se calcula desde `docs/04-rtm.csv` y `docs/registros/`.",
        "",
        "| Métrica | Valor | Referencia | Cómo se calcula |",
        "|---|---|---|---|",
        f"| Requerimientos activos | {len(a)} | — | RTM sin los descartados |",
        f"| Implementados / en backlog | {by_status.get('Implementado', 0)} / {by_status.get('Backlog', 0)} | — | Estado en la RTM |",
        f"| Cobertura de trazabilidad (todos) | {_pct(traceability_coverage(rtm))} | > 95 % | Req. con test / activos |",
        f"| Cobertura de trazabilidad (Must) | {_pct(traceability_coverage(rtm, 'Must'))} | 100 % | Req. Must con test / Must |",
        f"| Volatilidad de requerimientos | {_pct(requirement_volatility(rtm, cambios))} | < 10–15 % | Cambios aprobados / req. de línea base |",
        f"| Defectos totales | {d['total']} | — | `docs/registros/defectos.csv` |",
        f"| DDP (detección antes de release) | {_pct(d['ddp'])} | > 90 % | (total − post-release) / total |",
        f"| Defect leakage | {_pct(d['leakage'])} | < 5–10 % | post-release / total |",
        f"| Defectos abiertos | {d['open']} | 0 críticos al release | Estado ≠ Cerrado |",
    ]
    if junit:
        lines.append(
            f"| Pass rate de pruebas | {_pct(junit['pass_rate'])} | ≥ 95 % | {junit['tests']} tests, {junit['failed']} fallidos |"
        )
    else:
        lines.append("| Pass rate de pruebas | n/d | ≥ 95 % | Ejecutar `make test` antes |")
    lines += ["", "Un valor por debajo de la referencia no es un error del reporte: es información para decidir."]
    return "\n".join(lines) + "\n"
