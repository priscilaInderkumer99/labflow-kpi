import pandas as pd
import pytest

from labflow import kpis, quality


def test_metadata_completeness_kpi(tiny):
    # 5 muestras x 5 campos obligatorios = 25 celdas; S2 tiene patient_ref vacío => 24/25
    assert kpis.metadata_completeness(tiny) == pytest.approx(24 / 25)
    gaps = kpis.metadata_gaps(tiny)
    assert gaps.to_dict("records") == [{"sample_id": "S2", "campos_faltantes": "patient_ref"}]


def test_quality_checks_pass_on_generated_data(synthetic):
    res = quality.run_all(synthetic)
    assert res[res["severity"] == "error"]["passed"].all()
    quality.assert_valid(synthetic)  # no debe lanzar


def test_quality_detects_duplicate_ids(synthetic):
    bad = synthetic.__class__(
        pd.concat([synthetic.samples, synthetic.samples.iloc[[0]]]),
        synthetic.stage_events, synthetic.custody_events, synthetic.reports, synthetic.as_of,
    )
    res = quality.run_all(bad).set_index("check")
    assert not res.loc["sample_id único", "passed"]
    with pytest.raises(ValueError):
        quality.assert_valid(bad)


def test_quality_detects_inverted_dates(synthetic):
    ev = synthetic.stage_events.copy()
    idx = ev.index[ev["finished_at"].notna()][0]
    ev.loc[idx, "finished_at"] = ev.loc[idx, "started_at"] - pd.Timedelta(hours=1)
    bad = synthetic.__class__(synthetic.samples, ev, synthetic.custody_events, synthetic.reports, synthetic.as_of)
    res = quality.run_all(bad).set_index("check")
    assert not res.loc["fin >= inicio en cada etapa", "passed"]
