import pandas as pd
import pytest

from labflow import kpis


def test_tat_median_and_p90(tiny):
    s = kpis.tat_summary(tiny)
    assert s["n"] == 2
    assert s["median"] == pytest.approx(200.0)  # mediana de 100 h y 300 h
    assert s["p90"] == pytest.approx(280.0)


def test_sla_compliance_counts_open_late_samples(tiny):
    b = kpis.sla_breakdown(tiny)
    assert b == {"on_time": 1, "late_completed": 1, "late_open": 1, "undetermined": 1}
    # S1 cumple; S2 y S4 incumplen; S5 aún no se puede determinar y se excluye
    assert kpis.sla_compliance(tiny) == pytest.approx(1 / 3)


def test_tat_by_stage_identifies_bottleneck(tiny):
    stage = kpis.tat_by_stage(tiny)
    assert kpis.bottleneck_stage(tiny) == "REVISION"
    assert stage["share"].sum() == pytest.approx(1.0)


def test_rejection_rate(tiny):
    assert kpis.rejection_rate(tiny) == pytest.approx(1 / 5)


def test_rework_rate(tiny):
    # De 4 muestras no rechazadas, solo S2 repitió etapas
    assert kpis.rework_rate(tiny) == pytest.approx(1 / 4)


def test_first_pass_qc_rate(tiny):
    # Intentos 1 de EXTRACCION/LIBRERIA finalizados: S1x2, S2x2 (1 falla), S4x2 y S5x2 (EXT y LIB) = 8; 1 falla
    assert kpis.first_pass_qc_rate(tiny) == pytest.approx(7 / 8)


def test_pipeline_success_rate(tiny):
    # Pipeline finalizados: S1 ok, S2 failed, S2 ok, S4 ok = 3 de 4 ok
    assert kpis.pipeline_success_rate(tiny) == pytest.approx(3 / 4)


def test_backlog_by_stage(tiny):
    b = kpis.backlog_by_stage(tiny)
    assert b["REVISION"] == 1 and b["SECUENCIACION"] == 1
    assert b.sum() == 2


def test_report_error_rate(tiny):
    assert kpis.report_error_rate(tiny) == pytest.approx(0.5)


def test_kpi_snapshot_flags_alerts(tiny):
    snap = kpis.kpi_snapshot(tiny).set_index("kpi_id")
    assert snap.loc["KPI-03", "status"] == "ALERTA"   # SLA 33 % < 95 %
    assert snap.loc["KPI-08", "status"] == "INFO"     # backlog no tiene objetivo
    assert snap["status"].isin(["OK", "ALERTA", "INFO", "SIN DATOS"]).all()


def test_kpis_on_empty_reports_do_not_crash(tiny):
    empty = tiny.__class__(tiny.samples, tiny.stage_events, tiny.custody_events,
                           tiny.reports.iloc[0:0], tiny.as_of)
    assert pd.isna(kpis.tat_summary(empty)["median"])
    assert pd.isna(kpis.report_error_rate(empty))
