#!/usr/bin/env python3
"""Generate deterministic three-seed artifacts for the Sep-21 paper batch."""

from __future__ import annotations

import json
from pathlib import Path
import statistics
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from auto_research.agent_research import AgentResearchConfig, AgentResearchRunner
from auto_research.reproductions.latest_20260921 import reproduce_evopilot

METHODS = {
    "autoviewmem": "2609.21940-autoviewmem",
    "mace": "2609.21533-mace",
    "arenaflow": "2609.21378-arenaflow",
    "graphskillevo": "2609.21749-graphskillevo",
}
SEEDS = (42, 43, 44)


def aggregate(rows):
    output = {}
    for key in sorted(set.intersection(*(set(row) for row in rows))):
        values = [row[key] for row in rows]
        if all(isinstance(value, (int, float)) and not isinstance(value, bool) for value in values):
            output[f"{key}_mean"] = statistics.fmean(map(float, values))
            output[f"{key}_std"] = statistics.stdev(map(float, values))
    return output


def main():
    for method, directory in METHODS.items():
        rows = []
        for seed in SEEDS:
            result, _ = AgentResearchRunner(AgentResearchConfig(
                method=method, episodes=36, seed=seed,
                output_dir=ROOT / "runs" / "agent-research",
            )).run()
            numeric = {
                key: value for key, value in result.diagnostics.items()
                if isinstance(value, (int, float)) and not isinstance(value, bool)
            }
            rows.append({"seed": seed, **result.metrics, **numeric})
        artifact = ROOT / "docs" / "agent-research" / directory / "metrics" / "mechanism-seeds42-44.json"
        artifact.parent.mkdir(parents=True, exist_ok=True)
        payload = {
            "schema_version": 2,
            "method": method,
            "dataset": "deterministic observation-only mechanism mini-suite",
            "seeds": list(SEEDS),
            "runs": rows,
            "aggregate_metrics": aggregate(rows),
            "manifest_ref": f"agent-research:{method}",
            "evaluation_protocol": {
                "tier": "l1_mechanism", "seeds": list(SEEDS),
                "formal_comparison": False, "diagnostic_only": True,
                "claim_policy": "paper-scale and policy-training claims excluded",
            },
            "provenance": {
                "commit": "working tree before commit",
                "command": "PYTHONPATH=src python scripts/generate_sep_21_agent_artifacts.py",
                "artifact_path": artifact.relative_to(ROOT).as_posix(),
                "dataset_fingerprint": "observation-mini-suite-v1",
            },
        }
        artifact.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n")

    rows = []
    for seed in SEEDS:
        result = reproduce_evopilot(ROOT / "data", seed)
        rows.append({
            "seed": seed,
            **{
                f"baseline_{key}": float(value)
                for key, value in result["baseline"].items()
                if isinstance(value, (int, float)) and not isinstance(value, bool)
            },
            **{
                f"method_{key}": float(value)
                for key, value in result["method"].items()
                if isinstance(value, (int, float)) and not isinstance(value, bool)
            },
            "hit_at_10_relative_percent": (
                100.0 * (
                    result["method"]["hit_at_10"]
                    / result["baseline"]["hit_at_10"] - 1.0
                )
            ),
            "validation_only_alpha": result["stages"]["validation_only_alpha"],
            "historical_mismatch_rejected": result["stages"]["historical_mismatch_rejected"],
            "matched_comparison_admitted": result["stages"]["matched_comparison_admitted"],
        })
    artifact = ROOT / "docs/reproductions/2609.21257-evopilot/metrics/movielens-100k-seeds42-44.json"
    artifact.parent.mkdir(parents=True, exist_ok=True)
    artifact.write_text(json.dumps({
        "schema_version": 2,
        "method": "evopilot",
        "dataset": "MovieLens 100K",
        "seeds": list(SEEDS),
        "runs": rows,
        "aggregate_metrics": aggregate(rows),
        "manifest_ref": "recommendation:evopilot",
        "evaluation_protocol": {
            "tier": "l2_public_dataset", "seeds": list(SEEDS),
            "formal_comparison": True, "diagnostic_only": False,
            "claim_policy": (
                "matched public comparison; negative results retained; "
                "paper-scale and production VDD claims excluded"
            ),
        },
        "provenance": {
            "commit": "working tree before commit",
            "command": "PYTHONPATH=src python scripts/generate_sep_21_agent_artifacts.py",
            "artifact_path": artifact.relative_to(ROOT).as_posix(),
            "dataset_fingerprint": "movielens-100k-compact-temporal-v1",
        },
    }, ensure_ascii=False, indent=2) + "\n")


if __name__ == "__main__":
    main()
