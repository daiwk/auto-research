#!/usr/bin/env python3
"""Run the FLVM public-data concept diagnostic with a matched multitask control."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from auto_research.reproductions.flvm.experiment import load_data, run_on_data

ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset-dir", type=Path, default=Path("data"))
    parser.add_argument("--steps", type=int, default=300)
    parser.add_argument("--seeds", default="42,43,44")
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    data = load_data(args.dataset_dir)
    seeds = [int(value) for value in args.seeds.split(",")]
    if not seeds or args.steps < 1:
        raise ValueError("provide at least one seed and one training step")
    results = [run_on_data(data, seed=seed, steps=args.steps) for seed in seeds]
    args.output.parent.mkdir(parents=True, exist_ok=True)
    try:
        artifact_path = str(args.output.resolve().relative_to(ROOT))
    except ValueError:
        artifact_path = str(args.output.resolve())
    payload = {
        "schema_version": 2,
        "manifest_ref": "reproduction:flvm",
        "status": "completed_public_diagnostic",
        "diagnostic_only": True,
        "paper_result_reproduced": False,
        "seeds": seeds,
        "evaluation_protocol": {
            "tier": "l1_mechanism",
            "seeds": seeds,
            "formal_comparison": False,
            "claim_policy": "public proxy mechanisms only; sparse negative signal and no production satisfaction labels",
        },
        "provenance": {
            "artifact_path": artifact_path,
            "dataset_fingerprint": data.source_sha256,
        },
        "runs": results,
    }
    args.output.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n",
                           encoding="utf-8")


if __name__ == "__main__":
    main()
