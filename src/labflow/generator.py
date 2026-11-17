"""Generador de datos SINTÉTICOS del flujo de laboratorio (reproducible con `seed`).

No contiene datos personales reales: solo seudónimos (patient_ref) generados al azar.
"""
from __future__ import annotations

import math

import numpy as np
import pandas as pd

from . import config as C
from .dataset import Dataset

CLIENTS = ["Hospital Central", "Clínica Norte", "Instituto Genómica", "Centro Oncológico", "Laboratorio Regional"]
SAMPLE_TYPES = ["sangre", "saliva", "tejido FFPE", "ADN extraído"]
REJECT_REASONS = ["volumen insuficiente", "etiqueta ilegible", "sin consentimiento", "muestra hemolizada"]
HANDLERS = ["tec_01", "tec_02", "tec_03", "tec_04"]


def _hours(rng: np.random.Generator, stage: str) -> float:
    mean, sigma = C.STAGE_PARAMS[stage]
    mu = math.log(mean) - sigma**2 / 2  # así la media de la lognormal = `mean`
    return float(rng.lognormal(mu, sigma))


def generate(n_samples: int = 600, days: int = 90, seed: int = 42, as_of: str = "2026-01-31") -> Dataset:
    rng = np.random.default_rng(seed)
    as_of_ts = pd.Timestamp(as_of)
    start = as_of_ts - pd.Timedelta(days=days)

    samples, events, custody, reports = [], [], [], []

    for i in range(1, n_samples + 1):
        sid = f"S-{i:06d}"
        received = start + pd.Timedelta(hours=float(rng.uniform(0, days * 24)))
        rejected = bool(rng.random() < C.P_REJECT)
        urgent = rng.random() < C.URGENT_SHARE
        factor = C.URGENT_FACTOR if urgent else 1.0
        collection = (received - pd.Timedelta(hours=float(rng.uniform(24, 72)))).normalize()

        row = {
            "sample_id": sid,
            "batch_id": f"B-{received.isocalendar().week:02d}",
            "client": CLIENTS[int(rng.integers(len(CLIENTS)))],
            "sample_type": SAMPLE_TYPES[int(rng.integers(len(SAMPLE_TYPES)))],
            "priority": "urgente" if urgent else "normal",
            "patient_ref": f"P-{int(rng.integers(10_000, 99_999))}",
            "collection_date": collection,
            "consent_flag": True,
            "received_at": received,
            "rejected": rejected,
            "reject_reason": REJECT_REASONS[int(rng.integers(len(REJECT_REASONS)))] if rejected else None,
        }
        if rng.random() < C.P_META_MISSING:  # inyecta un hueco de metadatos
            row[C.REQUIRED_FIELDS[int(rng.integers(len(C.REQUIRED_FIELDS)))]] = None
        samples.append(row)

        t = received
        stopped = False
        for stage in C.STAGES:
            attempt = 1
            while True:
                s = t
                e = s + pd.Timedelta(hours=_hours(rng, stage) * factor)
                outcome = "ok"
                if stage == "RECEPCION" and rejected:
                    outcome = "rejected"
                elif stage in C.QC_STAGES and attempt == 1 and rng.random() < C.P_QC_FAIL:
                    outcome = "qc_fail"
                elif stage == "PIPELINE" and attempt < 3 and rng.random() < C.P_PIPELINE_FAIL:
                    outcome = "failed"

                # Custodia: se registra al ENTRAR a una etapa física (con una pequeña tasa de omisiones)
                if attempt == 1 and stage in C.PHYSICAL_STAGES and rng.random() >= C.P_CUSTODY_GAP:
                    custody.append((sid, stage, s, HANDLERS[int(rng.integers(len(HANDLERS)))]))

                if e > as_of_ts:  # todavía en curso a la fecha de corte
                    events.append((sid, stage, attempt, s, pd.NaT, "in_progress"))
                    stopped = True
                    break
                events.append((sid, stage, attempt, s, e, outcome))
                t = e
                if outcome in ("qc_fail", "failed"):
                    attempt += 1
                    continue
                break
            if stopped or outcome == "rejected":
                stopped = True
                break

        if not stopped:  # completó todas las etapas: se emitió el reporte
            reports.append((sid, t, bool(rng.random() < C.P_REPORT_ERROR)))

    return Dataset(
        samples=pd.DataFrame(samples),
        stage_events=pd.DataFrame(
            events, columns=["sample_id", "stage", "attempt", "started_at", "finished_at", "outcome"]
        ),
        custody_events=pd.DataFrame(custody, columns=["sample_id", "stage", "moved_at", "handler"]),
        reports=pd.DataFrame(reports, columns=["sample_id", "issued_at", "corrected"]),
        as_of=as_of_ts,
    )
