#!/usr/bin/env python3
"""Regenerate auditable multi-seed artifacts for the 2026-09-12 batch."""

from __future__ import annotations

from dataclasses import asdict
import hashlib
import json
from pathlib import Path
import statistics
import subprocess

from auto_research.agent_research import AgentResearchConfig, AgentResearchRunner
from auto_research.post_training import PostTrainingConfig, PostTrainingRunner
from auto_research.reproductions.latest_20260912 import reproduce


ROOT = Path(__file__).resolve().parents[1]
SEEDS = (42, 43, 44)
POST_TRAINING = {
    "oprd": "2609.08798-oprd",
    "route-opd": "2609.08337-route-opd",
    "compass-opd": "2609.10154-compass-opd",
    "probe-erpo": "2609.09135-probe-erpo",
}
AGENTS = {
    "procedural-graphs": "2609.09153-procedural-graphs",
    "memforest": "2609.08273-memforest",
    "feedback-scaffold": "2609.08404-feedback-scaffold",
    "maple": "2609.11636-maple",
}
REPRODUCTIONS = {
    "unirec": "2609.11052-unirec",
    "sequenceo1": "2609.08443-sequenceo1",
    "baff": "2609.08725-baff",
}


def _write(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n")


def _aggregate(rows: list[dict]) -> dict[str, float]:
    common = set.intersection(*(set(row) for row in rows))
    result = {}
    for name in sorted(common):
        values = [row[name] for row in rows]
        if not all(isinstance(value, (int, float)) and not isinstance(value, bool) for value in values):
            continue
        numbers = [float(value) for value in values]
        result[f"{name}_mean"] = statistics.fmean(numbers)
        result[f"{name}_std"] = statistics.stdev(numbers)
    return result


def main() -> None:
    commit = subprocess.check_output(
        ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True
    ).strip()
    provenance = {
        "commit": commit,
        "command": "PYTHONPATH=src python scripts/generate_sep_12_2026_artifacts.py",
    }
    for method, slug in POST_TRAINING.items():
        runs = []
        for seed in SEEDS:
            result, _ = PostTrainingRunner(PostTrainingConfig(
                algorithm=method, dataset="arithmetic-smoke", steps=100,
                maximum_examples=192, seed=seed, allow_network=False,
                output_dir=ROOT / "runs/post-training",
            )).run()
            runs.append({**asdict(result), "relative_accuracy": result.relative_accuracy})
        _write(ROOT / f"docs/post-training/{slug}/metrics/arithmetic-smoke-seeds42-44.json", {
            "schema_version": 2, "method": method, "dataset": "arithmetic-smoke",
            "seeds": list(SEEDS), "runs": runs,
            "aggregate_metrics": _aggregate([run["final"] for run in runs]),
            "manifest_ref": "post-training:arithmetic-smoke-seeds42-44",
            "evaluation_protocol": {"tier": "l1_mechanism", "seeds": list(SEEDS),
                "formal_comparison": False,
                "claim_policy": "candidate-policy mechanism diagnostic; not a full-parameter LLM result"},
            "provenance": provenance,
        })

    for method, slug in AGENTS.items():
        runs = []
        for seed in SEEDS:
            result, _ = AgentResearchRunner(AgentResearchConfig(
                method=method, benchmark="evomem-mini", episodes=120,
                memory_size=24, seed=seed,
                output_dir=ROOT / "runs/agent-research",
            )).run()
            runs.append(asdict(result))
        _write(ROOT / f"docs/agent-research/{slug}/metrics/mini-suite-seeds42-44.json", {
            "schema_version": 2, "method": method, "dataset": "evomem-mini",
            "seeds": list(SEEDS), "runs": runs,
            "aggregate_metrics": _aggregate([run["metrics"] for run in runs]),
            "manifest_ref": "agent-research:evomem-mini-seeds42-44",
            "evaluation_protocol": {"tier": "l1_mechanism", "seeds": list(SEEDS),
                "formal_comparison": False,
                "claim_policy": "public-observation parser diagnostic; no hidden gold or tool execution"},
            "provenance": provenance,
        })

    for method, slug in REPRODUCTIONS.items():
        runs = [reproduce(method, ROOT / "data", seed) for seed in SEEDS]
        metric_rows = [run["method"] for run in runs]
        dataset = runs[0]["dataset"]["name"]
        fingerprint = hashlib.sha256(json.dumps(
            [run["setup"] for run in runs], sort_keys=True, default=str
        ).encode()).hexdigest()
        filename = (
            "controlled-rtb-seeds42-44.json" if method == "baff"
            else "movielens-100k-seeds42-44.json"
        )
        _write(ROOT / f"docs/reproductions/{slug}/metrics/{filename}", {
            "schema_version": 2, "method": method, "dataset": dataset,
            "seeds": list(SEEDS), "runs": runs,
            "aggregate_metrics": _aggregate(metric_rows),
            "manifest_ref": f"reproduction:{method}",
            "evaluation_protocol": {"tier": "l1_mechanism" if method == "baff" else "l2_public_dataset",
                "seeds": list(SEEDS), "formal_comparison": method != "baff",
                "claim_policy": "public CPU mechanism comparison; not a production KPI reproduction"},
            "provenance": {**provenance, "dataset_fingerprint": fingerprint},
        })


if __name__ == "__main__":
    main()
