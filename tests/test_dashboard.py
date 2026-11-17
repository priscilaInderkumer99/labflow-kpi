import pytest

pytest.importorskip("streamlit")
from streamlit.testing.v1 import AppTest  # noqa: E402

from labflow.config import ROOT  # noqa: E402


@pytest.mark.parametrize("persona", [
    "Director del laboratorio", "Responsable de calidad", "Operaciones / Bioinformática",
])
def test_dashboard_renders_each_persona_view(persona):
    at = AppTest.from_file(str(ROOT / "dashboard" / "app.py"), default_timeout=60).run()
    assert not at.exception
    at.sidebar.radio[0].set_value(persona).run()
    assert not at.exception
    assert len(at.metric) >= 4
