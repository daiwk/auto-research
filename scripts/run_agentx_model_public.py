#!/usr/bin/env python3
"""Run the public AgentX-Model mechanism audit on cached MovieLens-1M."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from auto_research.agent_research.agentx_model_public import run_public_benchmark


def _dataset_fingerprint(root: Path) -> str:
    digest = hashlib.sha256()
    for name in ("ratings.dat", "movies.dat"):
        path = root / "ml-1m" / name
        digest.update(name.encode("utf-8"))
        with path.open("rb") as stream:
            for chunk in iter(lambda: stream.read(1024 * 1024), b""):
                digest.update(chunk)
    return f"sha256:{digest.hexdigest()}"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dataset-dir", type=Path, default=Path("data"))
    parser.add_argument("--seeds", default="42,43,44")
    parser.add_argument("--budget", type=int, default=2)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    seeds = [int(value) for value in args.seeds.split(",")]
    runs = [run_public_benchmark(args.dataset_dir, seed=seed, budget=args.budget)
            for seed in seeds]
    try:
        artifact_path = args.output.resolve().relative_to(ROOT).as_posix() if args.output else "stdout"
    except ValueError:
        artifact_path = "external output"
    metrics = {
        "baseline_validation_auc_mean": float(np.mean([run["baseline_validation_auc"] for run in runs])),
        "diagnose_pcoc_absolute_error_before_mean": float(np.mean([
            abs(run["diagnose"]["validation_pcoc_before"] - 1) for run in runs
        ])),
        "diagnose_pcoc_absolute_error_after_mean": float(np.mean([
            abs(run["diagnose"]["validation_pcoc_after"] - 1) for run in runs
        ])),
    }
    for policy in ("fixed", "random", "parent-greedy"):
        metrics[f"{policy}_best_validation_auc_mean"] = float(np.mean([
            run["policies"][policy]["best_validation_auc"] for run in runs
        ]))
        metrics[f"{policy}_selected_test_auc_mean"] = float(np.mean([
            run["policies"][policy]["selected_test_auc"] for run in runs
        ]))
    payload = {
        "schema_version": 2,
        "diagnostic_only": True,
        "evaluation_protocol": {
            "tier": "l1_mechanism_diagnostic",
            "formal_comparison": False,
            "claim_policy": "Fixed public graph and short budget; not a general scheduler comparison or production replication.",
            "seeds": seeds,
        },
        "paper": "https://arxiv.org/abs/2609.30001",
        "manifest_ref": "agent-research:agentx-model-replay",
        "dataset": "MovieLens-1M",
        "seeds": seeds,
        "provenance": {
            "artifact_path": artifact_path,
            "dataset_fingerprint": _dataset_fingerprint(args.dataset_dir),
        },
        "metrics": metrics,
        "runs": runs,
    }
    rendered = json.dumps(payload, ensure_ascii=False, indent=2, allow_nan=False) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8")
        print(f"wrote {args.output}")
    else:
        print(rendered)


if __name__ == "__main__":
    main()
