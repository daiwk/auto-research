#!/usr/bin/env python3
"""Regenerate auditable three-seed public receipts for OneTrans-V2 and X-Rec.

Examples:
  PYTHONPATH=src python scripts/run_staged_retrieval_public.py --paper onetrans-v2 --dataset-dir data
  PYTHONPATH=src python scripts/run_staged_retrieval_public.py --paper xrec-fair --dataset-dir data
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import numpy as np

from auto_research.reproductions.onetrans_v2.experiment import reproduce_onetrans_v2
from auto_research.reproductions.xrec.experiment import reproduce_xrec_fair


ROOT = Path(__file__).resolve().parents[1]
OUTPUTS = {
    "onetrans-v2": ROOT / "docs/reproductions/2609.28589-onetrans-v2/metrics/public-seeds42-44.json",
    "xrec-fair": ROOT / "docs/reproductions/2609.29180-xrec/metrics/fair-budget-seeds42-44.json",
}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--paper", choices=tuple(OUTPUTS), required=True)
    parser.add_argument("--dataset-dir", type=Path, required=True)
    parser.add_argument("--seeds", default="42,43,44")
    args = parser.parse_args()
    seeds = tuple(int(value) for value in args.seeds.split(","))
    if not seeds or len(seeds) != len(set(seeds)):
        raise ValueError("seeds must be nonempty and unique")
    run = reproduce_onetrans_v2 if args.paper == "onetrans-v2" else reproduce_xrec_fair
    results = []
    for seed in seeds:
        result = run(args.dataset_dir, seed)
        results.append(result)
        print(f"{args.paper}: seed={seed} done", flush=True)
    fingerprint = hashlib.sha256((args.dataset_dir / "ml-1m" / "ratings.dat").read_bytes()).hexdigest()
    payload = {
        "schema_version": 2,
        "paper": "2609.28589" if args.paper == "onetrans-v2" else "2609.29180",
        "adapter": "onetrans-v2" if args.paper == "onetrans-v2" else "xrec",
        "dataset": "MovieLens 1M",
        "seeds": results,
        "metrics": {},
        "diagnostic_only": True,
        "evaluation_protocol": {
            "tier": "l1_mechanism" if args.paper == "onetrans-v2" else "l2_public_dataset",
            "seeds": list(seeds), "formal_comparison": False,
            "claim_policy": "limited-budget public proxy; no paper or production lift claim",
        },
        "provenance": {
            "artifact_path": str(OUTPUTS[args.paper].relative_to(ROOT)),
            "dataset_fingerprint": f"MovieLens-1M ratings.dat sha256:{fingerprint}",
        },
        "manifest_ref": "reproduction:onetrans-v2" if args.paper == "onetrans-v2" else "reproduction:xrec",
    }
    if args.paper == "onetrans-v2":
        for phase in ("validation", "test"):
            for key, value in results[0][phase].items():
                if isinstance(value, (int, float)):
                    values = [row[phase][key] for row in results]
                    payload["metrics"][f"{phase}_{key}_mean"] = float(np.mean(values))
                    payload["metrics"][f"{phase}_{key}_std"] = float(np.std(values))
    else:
        for phase in ("validation_recall_at_20", "test_recall_at_20", "generation_requests_per_second_cpu"):
            for key in ("xrec", "sid_ar", "u2i"):
                values = [row[phase][key] for row in results]
                payload["metrics"][f"{phase}_{key}_mean"] = float(np.mean(values))
                payload["metrics"][f"{phase}_{key}_std"] = float(np.std(values))
    output = OUTPUTS[args.paper]
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, ensure_ascii=False, indent=2, allow_nan=False) + "\n", encoding="utf-8")
    print(output.relative_to(ROOT), flush=True)


if __name__ == "__main__":
    main()
