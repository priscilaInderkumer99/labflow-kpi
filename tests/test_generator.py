import pandas as pd

from labflow.generator import generate

FORBIDDEN_COLUMNS = {"nombre", "apellido", "name", "dni", "documento", "email", "telefono", "phone", "direccion", "address"}


def test_generator_is_reproducible():
    a = generate(n_samples=80, days=30, seed=123)
    b = generate(n_samples=80, days=30, seed=123)
    c = generate(n_samples=80, days=30, seed=124)
    pd.testing.assert_frame_equal(a.samples, b.samples)
    pd.testing.assert_frame_equal(a.stage_events, b.stage_events)
    assert not a.samples.equals(c.samples)


def test_generator_has_no_real_pii_columns(synthetic):
    cols = {c.lower() for df in (synthetic.samples, synthetic.custody_events, synthetic.reports) for c in df.columns}
    assert cols.isdisjoint(FORBIDDEN_COLUMNS)
    # los identificadores de paciente son seudónimos con formato P-#####
    refs = synthetic.samples["patient_ref"].dropna()
    assert refs.str.fullmatch(r"P-\d{5}").all()
