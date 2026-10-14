#!/usr/bin/env python3
"""Curate the executed no-extra-forward diffusion diagnostic, retaining collapse."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import statistics
import subprocess

from auto_research.gpu_validation import validate_gpu_receipt

ROOT = Path(__file__).resolve().parents[1]
SEEDS = (42, 43, 44)
SOURCE_PATHS = (
    "scripts/run_doublecat_semicat.py",
    "src/auto_research/foundation_models/doublecat_semicat.py",
    "src/auto_research/foundation_models/oct13_runtime.py",
    "src/auto_research/oct12_public_sources.py",
)


def summarize(runs):
    for seed, run in zip(SEEDS, runs, strict=True):
        if run["seed"] != seed or run["paper"] != "2610.13834" or not run["diagnostic_only"]:
            raise ValueError("expected three immutable diagnostic runs")
        if run["self_conditioning"] or run["checkpoint"]["revision"] != "doublecat-semicat-byte-dit-v2-no-extra-forward-core":
            raise ValueError("legacy extra-forward runs cannot validate the corrected core")
        if run["dataset"] != runs[0]["dataset"] or not run["test_isolated_from_selection"]:
            raise ValueError("verified identical splits and isolated test required")
        if any(run[field] != value for field, value in {
            "steps": 40, "sequence_length": 32, "width": 64, "layers": 2,
        }.items()):
            raise ValueError("this receipt only covers the actual declared bounded protocol")
        for result in run["results"].values():
            calls = result["actual_denoiser_forward_calls"]
            if (result["parameter_delta_l2"] <= 0 or result["standard_self_conditioning_steps"] != 0
                    or calls["training"] != {"total": run["steps"], "with_grad": run["steps"], "no_grad": 0}):
                raise ValueError("actual single-forward updates and declared sampling calls required")
            if calls["sampling"]["total"] != 32 or result["sampling"]["nfe"] != 32:
                raise ValueError("sampling NFE mismatch")
        if any(run["results"][method]["sampled_byte_entropy"] != 0 for method in ("onehot", "doublecat")):
            raise ValueError("do not copy the measured collapse limitation into different runs")
    return {
        f"{method}.{metric}": {"mean": statistics.mean(values), "std": statistics.stdev(values), "n": 3}
        for method in ("onehot", "doublecat", "semicat")
        for metric in ("test_denoising_ce_t05", "sampled_byte_entropy", "parameter_delta_l2")
        for values in [[run["results"][method][metric] for run in runs]]
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--executed-commit", required=True)
    args = parser.parse_args()
    commit = subprocess.check_output(["git", "rev-parse", args.executed_commit], cwd=ROOT, text=True).strip()
    runs = [json.loads((args.input / f"doublecat-semicat-v2-{seed}.json").read_text()) for seed in SEEDS]
    metrics = summarize(runs)
    artifact = "docs/reproductions/2610.13834-doublecat-semicat/metrics/public-a30-seeds42-44.json"
    receipt_path = "docs/gpu-validations/doublecat-semicat-a30-20261013.json"
    limitations = ["Small random-initialized byte-vocabulary WikiText-2 core-mechanism diagnostic.",
                   "Denoising CE is not exact likelihood, generative perplexity or reasoning accuracy.",
                   "One-hot and DoubleCat collapse to spaces in all three measured seeds; retained as a negative result.",
                   "No stable quality, scaling, serving or original-paper benchmark gain is claimed."]
    payload = {"schema_version": 2, "method": "doublecat-semicat", "adapter_key": "doublecat-semicat",
               "manifest_ref": "reproduction:doublecat-semicat", "diagnostic_only": True,
               "measured_locally": True, "seeds": list(SEEDS), "dataset": runs[0]["dataset"],
               "checkpoint": runs[0]["checkpoint"], "aggregate_metrics": metrics, "seed_results": runs,
               "evaluation_protocol": {"tier": "l1_mechanism", "formal_comparison": False,
                   "seeds": list(SEEDS), "test_used_for_selection": False,
                   "claim_policy": "three-seed mechanism diagnostic; no formal language-quality comparison"},
               "provenance": {"code_commit": commit, "artifact_path": artifact,
                   "dataset_fingerprint": hashlib.sha256(json.dumps(runs[0]["dataset"], sort_keys=True).encode()).hexdigest()},
               "limitations": limitations}
    receipt = {"schema_version": 1, "adapter_key": "doublecat-semicat", "validated_at": "2026-10-13",
               "accelerator": {"vendor": "NVIDIA", "model": "A30"},
               "command": ["python", "scripts/run_doublecat_semicat.py", "--data", "data/wikitext",
                   "--dataset-id", "Salesforce/wikitext", "--dataset-revision", runs[0]["dataset"]["revision"],
                   "--device", "cuda", "--steps", "40", "--sequence-length", "32", "--batch-size", "4",
                   "--width", "64", "--layers", "2", "--nfe", "32", "--no-self-conditioning",
                   "--seed", "42", "--output", "runs/doublecat-semicat-v2-42.json"],
               "additional_seeds": list(SEEDS[1:]), "dataset": runs[0]["dataset"],
               "checkpoint": runs[0]["checkpoint"], "result": "passed", "metrics": metrics,
               "execution_checks": {"real_cuda_execution": True, "completed_seeds": 3,
                   "training_forward_calls_per_variant_seed": 40, "extra_self_conditioning_forwards": 0,
                   "sampling_forward_calls_per_variant_seed": 32, "actual_parameter_changes_checked": True,
                   "negative_generation_collapse_retained": True}, "limitations": limitations,
               "executed_source_sha256": {path: hashlib.sha256(subprocess.check_output(
                   ["git", "show", f"{commit}:{path}"], cwd=ROOT)).hexdigest() for path in SOURCE_PATHS},
               "provenance": {"commit": commit, "artifact_path": receipt_path,
                   "metrics_artifact": artifact, "checkpoint_committed": False}}
    if errors := validate_gpu_receipt(receipt):
        raise ValueError(errors)
    for relative, content in ((artifact, payload), (receipt_path, receipt)):
        destination = ROOT / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(json.dumps(content, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps(metrics, indent=2))


if __name__ == "__main__":
    main()
