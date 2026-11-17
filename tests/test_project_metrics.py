import pandas as pd
import pytest

from labflow import project_metrics as pm
from labflow.config import ROOT


def _rtm(rows):
    return pd.DataFrame(rows, columns=["req_id", "prioridad", "estado", "test_id", "baseline"])


def test_traceability_coverage_calculation():
    rtm = _rtm([
        ("REQ-001", "Must", "Implementado", "tests/a.py::test_x", "v0.1"),
        ("REQ-002", "Must", "Implementado", "", "v0.1"),
        ("REQ-003", "Could", "Backlog", "", "v0.1"),
        ("REQ-004", "Won't", "Descartado", "", "v0.1"),  # no cuenta
    ])
    assert pm.traceability_coverage(rtm) == pytest.approx(1 / 3)
    assert pm.traceability_coverage(rtm, "Must") == pytest.approx(1 / 2)


def test_requirement_volatility_and_defect_metrics():
    rtm = _rtm([("R1", "Must", "Implementado", "x", "v0.1"), ("R2", "Must", "Implementado", "x", "v0.1"),
                ("R3", "Must", "Implementado", "x", "v0.5")])
    cambios = pd.DataFrame({"estado": ["Aprobado", "Rechazado"]})
    assert pm.requirement_volatility(rtm, cambios) == pytest.approx(1 / 2)
    d = pm.defect_metrics(pd.DataFrame({"detectado_en": ["desarrollo", "UAT", "post-release", "desarrollo"],
                                         "estado": ["Cerrado"] * 4}))
    assert d["ddp"] == pytest.approx(0.75) and d["leakage"] == pytest.approx(0.25)


def test_rtm_references_existing_tests():
    """La trazabilidad se verifica en CI: cada test citado en la RTM debe existir."""
    rtm = pm.load_rtm(ROOT / "docs" / "04-rtm.csv")
    assert pm.check_rtm_integrity(rtm, ROOT) == []
