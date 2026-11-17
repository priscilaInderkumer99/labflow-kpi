import pandas as pd
import pytest

from labflow import kpis


def test_custody_completeness_reports_missing_samples(tiny):
    rate, missing = kpis.custody_completeness(tiny)
    # 5 muestras entraron a etapas físicas; solo S2 tiene un hueco (LIBRERIA)
    assert rate == pytest.approx(4 / 5)
    assert missing.to_dict("records") == [{"sample_id": "S2", "stage": "LIBRERIA"}]


def test_custody_is_100_percent_when_no_gaps(tiny):
    full = tiny.stage_events[
        tiny.stage_events["stage"].isin(["RECEPCION", "EXTRACCION", "LIBRERIA", "SECUENCIACION"])
        & (tiny.stage_events["attempt"] == 1)
    ]
    custody = full[["sample_id", "stage", "started_at"]].rename(columns={"started_at": "moved_at"})
    custody = custody.assign(handler="tec_01")
    ds = tiny.__class__(tiny.samples, tiny.stage_events, custody, tiny.reports, tiny.as_of)
    rate, missing = kpis.custody_completeness(ds)
    assert rate == 1.0 and missing.empty
    assert isinstance(missing, pd.DataFrame)
