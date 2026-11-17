"""CLI: python -m labflow.cli {generate,kpis,validate,project-metrics}"""
from __future__ import annotations

import argparse
import sys

import pandas as pd

from . import config as C
from . import kpis, quality
from . import project_metrics as pm
from .dataset import Dataset
from .generator import generate


def _load(args) -> Dataset:
    try:
        return Dataset.load(args.data)
    except FileNotFoundError:
        sys.exit(f"No hay datos en {args.data}. Ejecutá primero: python -m labflow.cli generate")


def _fmt(row) -> str:
    v = row["value"]
    if pd.isna(v):
        return "n/d"
    return f"{v:.1f} {row['unit']}" if row["unit"] in ("h", "muestras") else f"{v:.1%}"


def main(argv=None) -> int:
    p = argparse.ArgumentParser(prog="labflow")
    p.add_argument("--data", default=str(C.DATA_DIR), help="carpeta con los CSV")
    sub = p.add_subparsers(dest="cmd", required=True)

    g = sub.add_parser("generate", help="genera datos sintéticos")
    g.add_argument("--n", type=int, default=600)
    g.add_argument("--days", type=int, default=90)
    g.add_argument("--seed", type=int, default=42)
    sub.add_parser("kpis", help="muestra el snapshot de KPIs")
    sub.add_parser("validate", help="corre las validaciones de calidad de datos")
    m = sub.add_parser("project-metrics", help="calcula las métricas del propio proyecto")
    m.add_argument("--junit", default=str(C.ROOT / "reports" / "junit.xml"))

    args = p.parse_args(argv)

    if args.cmd == "generate":
        ds = generate(n_samples=args.n, days=args.days, seed=args.seed)
        out = ds.save(args.data)
        print(f"{len(ds.samples)} muestras · {len(ds.reports)} reportes · guardado en {out}")
        return 0

    if args.cmd == "kpis":
        ds = _load(args)
        snap = kpis.kpi_snapshot(ds)
        for _, r in snap.iterrows():
            if pd.isna(r["target"]):
                tgt = ""
            elif r["unit"] == "%":
                tgt = f"(objetivo {r['comparator']} {r['target']:.0%})"
            else:
                tgt = f"(objetivo {r['comparator']} {r['target']:g} {r['unit']})"
            print(f"{r['kpi_id']}  {r['kpi']:<30} {_fmt(r):>12}  {r['status']:<9} {tgt}")
        print(f"\nCuello de botella: {kpis.bottleneck_stage(ds)}")
        return 0

    if args.cmd == "validate":
        res = quality.run_all(_load(args))
        print(res.to_string(index=False))
        failed = res[(~res["passed"]) & (res["severity"] == "error")]
        return 1 if len(failed) else 0

    if args.cmd == "project-metrics":
        docs = C.DOCS_DIR
        md = pm.render_markdown(
            pm.load_rtm(docs / "04-rtm.csv"),
            pd.read_csv(docs / "registros" / "cambios.csv", dtype=str).fillna(""),
            pd.read_csv(docs / "registros" / "defectos.csv", dtype=str).fillna(""),
            pm.junit_pass_rate(args.junit),
        )
        (docs / "METRICAS_DEL_PROYECTO.md").write_text(md, encoding="utf-8")
        print(md)
        return 0
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
