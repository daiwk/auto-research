#!/usr/bin/env python3
"""Regenerate auditable multi-seed artifacts for the 2026-09-15 industrial batch."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import statistics
import subprocess

from auto_research.reproductions.latest_20260915 import reproduce
from auto_research.reproductions.sas_attention.experiment import reproduce_sas_attention


ROOT = Path(__file__).resolve().parents[1]
SEEDS = (42, 43, 44)
REPRODUCTIONS = {
    "pindco": "2609.11943-pindco",
    "mima": "2609.12842-mima",
    "chronicle-rec": "2609.12375-chronicle-rec",
}


def _aggregate(rows: list[dict]) -> dict[str, float]:
    common = set.intersection(*(set(row) for row in rows))
    result = {}
    for name in sorted(common):
        values = [row[name] for row in rows]
        if all(isinstance(value, (int, float)) and not isinstance(value, bool) for value in values):
            numbers = [float(value) for value in values]
            result[f"{name}_mean"] = statistics.fmean(numbers)
            result[f"{name}_std"] = statistics.stdev(numbers)
    return result


def main() -> None:
    commit = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    command = "PYTHONPATH=src python scripts/generate_sep_15_2026_artifacts.py"
    for method, slug in REPRODUCTIONS.items():
        runs = [reproduce(method, ROOT / "data", seed) for seed in SEEDS]
        fingerprint = hashlib.sha256(json.dumps([run["setup"] for run in runs], sort_keys=True).encode()).hexdigest()
        output = ROOT / f"docs/reproductions/{slug}/metrics/movielens-100k-seeds42-44.json"
        output.parent.mkdir(parents=True, exist_ok=True)
        payload = {
            "schema_version": 2, "method": method, "dataset": "MovieLens 100K",
            "seeds": list(SEEDS), "runs": runs,
            "aggregate_metrics": _aggregate([run["method"] for run in runs]),
            "manifest_ref": f"reproduction:{method}",
            "evaluation_protocol": {"tier": "l2_public_dataset", "seeds": list(SEEDS), "formal_comparison": True,
                "claim_policy": "public CPU mechanism comparison; not a production KPI reproduction"},
            "provenance": {"commit": commit, "command": command, "dataset_fingerprint": fingerprint,
                "artifact_path": str(output.relative_to(ROOT))},
        }
        output.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    sas_runs = [reproduce_sas_attention(ROOT / "data", seed) for seed in SEEDS]
    sas_output = ROOT / "docs/reproductions/2609.13141-sas-attention/metrics/wikitext-2-seeds42-44.json"
    sas_output.parent.mkdir(parents=True, exist_ok=True)
    sas_rows = [{
        "dense_test_perplexity": run["test"]["dense"]["perplexity"],
        "sas_test_perplexity": run["test"]["sas"]["perplexity"],
        "test_ppl_change_vs_dense_percent": run["relative"]["test_ppl_change_vs_dense_percent"],
        "retained_attention_fraction": run["routing"]["retained_attention_fraction"],
        "selector_gradient_norm_mean": run["selector_training"]["selector_gradient_norm_mean"],
    } for run in sas_runs]
    sas_payload = {
        "schema_version": 2,
        "method": "sas-attention",
        "dataset": "WikiText-2",
        "seeds": list(SEEDS),
        "runs": sas_runs,
        "aggregate_metrics": _aggregate(sas_rows),
        "manifest_ref": "reproduction:sas-attention",
        "evaluation_protocol": {
            "tier": "l2_public_dataset",
            "seeds": list(SEEDS),
            "formal_comparison": True,
            "selection_split": "train selector; inspect validation; evaluate isolated test",
            "claim_policy": "CPU reference mechanism comparison; no Triton throughput claim",
        },
        "provenance": {
            "commit": commit,
            "command": command,
            "dataset_fingerprint": hashlib.sha256(
                json.dumps([run["setup"] for run in sas_runs], sort_keys=True).encode()
            ).hexdigest(),
            "artifact_path": str(sas_output.relative_to(ROOT)),
        },
    }
    sas_output.write_text(json.dumps(sas_payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
