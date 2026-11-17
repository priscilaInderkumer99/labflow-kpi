"""Contenedor de tablas + lectura/escritura en CSV."""
from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

import pandas as pd

TABLES = ("samples", "stage_events", "custody_events", "reports")
DATE_COLS = {
    "samples": ["received_at", "collection_date"],
    "stage_events": ["started_at", "finished_at"],
    "custody_events": ["moved_at"],
    "reports": ["issued_at"],
}


@dataclass
class Dataset:
    samples: pd.DataFrame
    stage_events: pd.DataFrame
    custody_events: pd.DataFrame
    reports: pd.DataFrame
    as_of: pd.Timestamp

    def save(self, folder: Path | str) -> Path:
        folder = Path(folder)
        folder.mkdir(parents=True, exist_ok=True)
        for name in TABLES:
            getattr(self, name).to_csv(folder / f"{name}.csv", index=False)
        (folder / "meta.json").write_text(json.dumps({"as_of": self.as_of.isoformat()}))
        return folder

    @classmethod
    def load(cls, folder: Path | str) -> "Dataset":
        folder = Path(folder)
        tables = {
            name: pd.read_csv(folder / f"{name}.csv", parse_dates=DATE_COLS[name]) for name in TABLES
        }
        as_of = pd.Timestamp(json.loads((folder / "meta.json").read_text())["as_of"])
        return cls(as_of=as_of, **tables)
