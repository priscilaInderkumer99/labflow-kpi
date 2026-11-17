import pandas as pd
import pytest

from labflow.dataset import Dataset
from labflow.generator import generate

T0 = pd.Timestamp("2026-01-01 08:00")
AS_OF = pd.Timestamp("2026-01-20 08:00")  # 19 días después de T0


def _ev(sid, stage, start_h, end_h, outcome="ok", attempt=1):
    s = T0 + pd.Timedelta(hours=start_h)
    e = pd.NaT if end_h is None else T0 + pd.Timedelta(hours=end_h)
    return (sid, stage, attempt, s, e, outcome)


@pytest.fixture(scope="session")
def tiny() -> Dataset:
    """Dataset mínimo y determinista con resultados esperados conocidos.

    S1: completada en 100 h (en plazo)       S2: completada en 300 h (fuera de plazo)
    S3: rechazada en recepción               S4: abierta desde hace 450 h (vencida)
    S5: abierta desde hace 50 h (aún en plazo; excluida del SLA)
    """
    recv = {"S1": 0, "S2": 0, "S3": 0, "S4": 0}
    recv_s5 = (AS_OF - pd.Timedelta(hours=50) - T0).total_seconds() / 3600
    # S4 recibida 450 h antes del corte (≈ 18,75 días)
    recv["S4"] = (AS_OF - pd.Timedelta(hours=450) - T0).total_seconds() / 3600
    recv["S5"] = recv_s5

    def sample(sid, rejected=False, **over):
        row = {
            "sample_id": sid, "batch_id": "B-01", "client": "Hospital Central", "sample_type": "sangre",
            "priority": "normal", "patient_ref": f"P-{sid}", "collection_date": T0.normalize(),
            "consent_flag": True, "received_at": T0 + pd.Timedelta(hours=recv[sid]),
            "rejected": rejected, "reject_reason": "etiqueta ilegible" if rejected else None,
        }
        row.update(over)
        return row

    samples = pd.DataFrame(
        [sample("S1"), sample("S2", patient_ref=None), sample("S3", rejected=True), sample("S4"), sample("S5")]
    )

    events = [
        # S1: sin repeticiones
        _ev("S1", "RECEPCION", 0, 4), _ev("S1", "EXTRACCION", 4, 20), _ev("S1", "LIBRERIA", 20, 40),
        _ev("S1", "SECUENCIACION", 40, 70), _ev("S1", "PIPELINE", 70, 78), _ev("S1", "REVISION", 78, 96),
        _ev("S1", "REPORTE", 96, 100),
        # S2: QC falla en extracción (repetición) y pipeline falla una vez
        _ev("S2", "RECEPCION", 0, 4), _ev("S2", "EXTRACCION", 4, 20, "qc_fail"),
        _ev("S2", "EXTRACCION", 20, 40, attempt=2), _ev("S2", "LIBRERIA", 40, 70),
        _ev("S2", "SECUENCIACION", 70, 120), _ev("S2", "PIPELINE", 120, 130, "failed"),
        _ev("S2", "PIPELINE", 130, 140, attempt=2), _ev("S2", "REVISION", 140, 296), _ev("S2", "REPORTE", 296, 300),
        # S3: rechazada
        _ev("S3", "RECEPCION", 0, 2, "rejected"),
    ]
    # S4: en curso en REVISION desde hace tiempo
    s4 = recv["S4"]
    events += [
        _ev("S4", "RECEPCION", s4, s4 + 3), _ev("S4", "EXTRACCION", s4 + 3, s4 + 20),
        _ev("S4", "LIBRERIA", s4 + 20, s4 + 40), _ev("S4", "SECUENCIACION", s4 + 40, s4 + 90),
        _ev("S4", "PIPELINE", s4 + 90, s4 + 100), _ev("S4", "REVISION", s4 + 100, None, "in_progress"),
    ]
    # S5: en curso en SECUENCIACION
    s5 = recv["S5"]
    events += [
        _ev("S5", "RECEPCION", s5, s5 + 2), _ev("S5", "EXTRACCION", s5 + 2, s5 + 15),
        _ev("S5", "LIBRERIA", s5 + 15, s5 + 30), _ev("S5", "SECUENCIACION", s5 + 30, None, "in_progress"),
    ]
    stage_events = pd.DataFrame(
        events, columns=["sample_id", "stage", "attempt", "started_at", "finished_at", "outcome"]
    )

    # Custodia: S2 sin registro en LIBRERIA; el resto completo (S3: solo recepción)
    cust = []
    for _, r in stage_events[stage_events["stage"].isin(["RECEPCION", "EXTRACCION", "LIBRERIA", "SECUENCIACION"])
                             & (stage_events["attempt"] == 1)].iterrows():
        if (r["sample_id"], r["stage"]) == ("S2", "LIBRERIA"):
            continue
        cust.append((r["sample_id"], r["stage"], r["started_at"], "tec_01"))
    custody = pd.DataFrame(cust, columns=["sample_id", "stage", "moved_at", "handler"])

    reports = pd.DataFrame(
        [("S1", T0 + pd.Timedelta(hours=100), False), ("S2", T0 + pd.Timedelta(hours=300), True)],
        columns=["sample_id", "issued_at", "corrected"],
    )
    return Dataset(samples, stage_events, custody, reports, AS_OF)


@pytest.fixture(scope="session")
def synthetic() -> Dataset:
    return generate(n_samples=300, days=60, seed=7)
