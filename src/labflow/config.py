"""Parámetros del negocio y del generador. Cambiar un valor aquí es un cambio de requerimiento:
registrarlo en docs/control-de-cambios.md."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = ROOT / "data" / "synthetic"
DOCS_DIR = ROOT / "docs"

# Etapas del flujo, en orden
STAGES = ["RECEPCION", "EXTRACCION", "LIBRERIA", "SECUENCIACION", "PIPELINE", "REVISION", "REPORTE"]
PHYSICAL_STAGES = ("RECEPCION", "EXTRACCION", "LIBRERIA", "SECUENCIACION")  # requieren custodia
QC_STAGES = ("EXTRACCION", "LIBRERIA")  # etapas con control de calidad de laboratorio

SLA_HOURS = 240  # 10 días desde la recepción hasta el reporte

# (duración media en horas, sigma de la lognormal). REVISION es el cuello de botella por diseño.
STAGE_PARAMS = {
    "RECEPCION": (3, 0.4),
    "EXTRACCION": (18, 0.4),
    "LIBRERIA": (30, 0.4),
    "SECUENCIACION": (48, 0.35),
    "PIPELINE": (8, 0.5),
    "REVISION": (78, 1.0),
    "REPORTE": (4, 0.4),
}

# Probabilidades del generador sintético
P_REJECT = 0.03
P_QC_FAIL = 0.045
P_PIPELINE_FAIL = 0.04
P_CUSTODY_GAP = 0.015
P_META_MISSING = 0.025
P_REPORT_ERROR = 0.015
URGENT_SHARE = 0.15
URGENT_FACTOR = 0.7

# Metadatos obligatorios por muestra (solo seudónimos; nunca datos personales reales)
REQUIRED_FIELDS = ["patient_ref", "sample_type", "collection_date", "client", "consent_flag"]
