#!/usr/bin/env python3
"""Curate actual bounded WeGR runs; preserve weak and negative outcomes."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import statistics
import subprocess

from auto_research.gpu_validation import validate_gpu_receipt

ROOT = Path(__file__).resolve().parents[1]
SOURCE = "1cef8401a5d4bf67f8eaccfb80c6e156e5598cc7"
METRIC = "docs/reproductions/2610.16979-wegr/metrics/public-a100-seeds42-44.json"
RECEIPT = "docs/gpu-validations/wegr-a100-20261014.json"
PATHS = ("src/auto_research/reproductions/wegr/model.py",
         "src/auto_research/reproductions/wegr/experiment.py", "scripts/run_wegr.py",
         "src/auto_research/datasets.py", "src/auto_research/reproductions/forte/experiment.py",
         "src/auto_research/reproductions/wegr/adapter.py", "src/auto_research/runtime.py")


def summarize(runs):
    if [row["seed"] for row in runs] != [42, 43, 44]:
        raise ValueError("expected three actual seeds, never duplicate a result")
    for row in runs:
        if row["method"] != "wegr" or row["device"] != "cuda" or not row["measured_locally"]:
            raise ValueError("actual WeGR CUDA execution required")
        if not row["tokenizer"]["parameters_changed"] or not row["sft"]["parameters_changed"]:
            raise ValueError("tokenizer and supervised policy must really update")
        for arm in ("exact-grpo", "dhpo"):
            trace = row["arms"][arm]["training"]
            if not trace or not all(step["gradient_norm"] > 0 for step in trace):
                raise ValueError("real optimizer updates required in both RL arms")
        if {step["horizon"] for step in row["arms"]["dhpo"]["training"]} != {1, 2, 3}:
            raise ValueError("all dynamic horizons must execute")
        if row["protocol"]["test_used_for_selection"] or not row["diagnostic_only"]:
            raise ValueError("holdout isolation and diagnostic claim required")
    if any(row["dataset"] != runs[0]["dataset"] for row in runs):
        raise ValueError("paired runs require identical public splits")
    metrics = {}
    for arm in ("sft", "exact-grpo", "dhpo"):
        for metric in ("hr_at_10", "mrr"):
            values = [row["arms"][arm]["test"][metric] for row in runs]
            metrics[f"{arm}.test.{metric}"] = {"mean": statistics.mean(values),
                                               "std": statistics.stdev(values), "n": len(values)}
    metrics["elapsed_seconds_total"] = sum(row["elapsed_seconds"] for row in runs)
    return metrics


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--cli-result", type=Path, required=True)
    args = parser.parse_args()
    runs = [json.loads((args.input / f"wegr-{seed}/result.json").read_text()) for seed in (42, 43, 44)]
    metrics = summarize(runs)
    cli = json.loads(args.cli_result.read_text())
    if cli["device"] != "cuda" or cli["seed"] != 42 or not cli["measured_locally"]:
        raise ValueError("unified CLI must actually execute the CUDA adapter")
    if cli["dataset"] != runs[0]["dataset"] or cli["arms"] != runs[0]["arms"]:
        raise ValueError("same-seed CLI and standalone experiments must agree")
    fingerprint = hashlib.sha256(json.dumps(runs[0]["dataset"], sort_keys=True).encode()).hexdigest()
    payload = {"schema_version": 2, "adapter_key": "wegr", "method": "wegr", "manifest_ref": "reproduction:wegr",
               "diagnostic_only": True, "measured_locally": True, "seeds": [42,43,44],
               "dataset": runs[0]["dataset"], "checkpoint": runs[0]["checkpoint"],
               "aggregate_metrics": metrics, "seed_results": runs,
               "evaluation_protocol": {"tier": "l2_public_dataset", "seeds": [42,43,44], "formal_comparison": False,
                                       "test_used_for_selection": False,
                                       "claim_policy": "bounded public-data mechanism diagnostic; no stable/production gain"},
               "provenance": {"code_commit": SOURCE, "artifact_path": METRIC, "dataset_fingerprint": fingerprint},
               "limitations": runs[0]["limitations"]}
    receipt = {"schema_version": 1, "adapter_key": "wegr", "validated_at": "2026-10-14",
               "accelerator": {"vendor": "NVIDIA", "model": "A100-SXM4-80GB"},
               "command": ["python", "scripts/run_wegr.py", "--dataset-dir", "data", "--device", "cuda",
                           "--seed", "42", "--output", "runs/wegr-42"], "additional_seeds": [43,44],
               "dataset": runs[0]["dataset"], "checkpoint": runs[0]["checkpoint"], "result": "passed",
               "metrics": metrics, "execution_checks": {"real_tokenizer_training": True,
                    "real_sft_training": True, "three_matched_arms": True, "all_horizons_executed": True,
                    "negative_results_retained": True, "stable_improvement_claimed": False,
                    "unified_cli_cuda_device_forwarded": True, "cli_standalone_same_seed_agreement": True},
               "additional_validated_commands": [["python", "-m", "auto_research.cli", "reproduce", "--paper", "wegr",
                    "--dataset-dir", "data", "--device", "cuda", "--cpu-threads", "4", "--seeds", "42",
                    "--budget", "smoke", "--output-dir", "runs/wegr-cli"]],
               "executed_source_sha256": {path: hashlib.sha256(subprocess.check_output(
                   ["git", "show", f"{SOURCE}:{path}"], cwd=ROOT)).hexdigest() for path in PATHS},
               "provenance": {"commit": SOURCE, "artifact_path": RECEIPT,
                              "metrics_artifact": METRIC, "checkpoint_committed": False},
               "limitations": runs[0]["limitations"]}
    errors = validate_gpu_receipt(receipt)
    if errors:
        raise ValueError(errors)
    for relative, content in ((METRIC, payload), (RECEIPT, receipt)):
        path = ROOT / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(content, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps(metrics, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
