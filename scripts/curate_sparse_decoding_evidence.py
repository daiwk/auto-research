#!/usr/bin/env python3
"""Curate real sparse CUDA execution without converting truncation into success."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[1]
SOURCES = ["scripts/run_sparse_decoding_public.py"] + [
    f"src/auto_research/foundation/{name}.py" for name in
    ("sparse_decoding", "sparse_decoding_cuda", "sparse_decoding_triton")
]
SOURCES += ["src/auto_research/public_holdout.py", "src/auto_research/post_training/oct10_checkpoint.py"]
RECIPES = ("dense", "fixed-text-wanda-bitmask", "decode-wanda-bitmask")


def summarize(report):
    if (report.get("adapter_key") != "sparse-decoding" or not report.get("diagnostic_only")
            or not report.get("split_provenance", {}).get("verified") or report.get("test_read") is not False):
        raise ValueError("verified train-only real-checkpoint diagnostic required")
    if len(report["kernel_checks"]) != 4 or any(k["relative_error"] > .005 or k["metadata_bits_per_nonzero"] != 2
                                                for k in report["kernel_checks"]):
        raise ValueError("all four real CUDA patterns and bitmask metadata checks required")
    counts = report["calibration"]["counts"]
    expected = sum(r["decode_calls"] for r in report["calibration"]["generations"])
    if not counts or expected < 1 or set(counts.values()) != {expected} or not report["calibration"]["prefill_excluded"]:
        raise ValueError("decoded-only calibration counts do not match executed generations")
    if not report.get("warmup") or report.get("max_tokens", 0) < 512:
        raise ValueError("shape warmup and explicit long generation budget required")
    metrics = {}
    cases = None
    for recipe in RECIPES:
        rows = [r for r in report["rows"] if r["recipe"] == recipe]
        ids = {r["example"] for r in rows}
        if not rows or len(ids) != len(rows) or (cases is not None and ids != cases):
            raise ValueError("same unique validation cases required across recipes")
        cases = ids
        for row in rows:
            if (row["truncated"] == row["ended_with_eos"] or row["tokens"] < 1
                    or row["decode_calls"] != row["tokens"] - 1 or row["decode_seconds"] <= 0):
                raise ValueError("invalid EOS/budget/call accounting")
        metrics[recipe] = {
            "validation_examples": len(rows),
            "bounded_exact_match": sum(r["correct"] for r in rows) / len(rows),
            "eos_completion_fraction": sum(r["ended_with_eos"] for r in rows) / len(rows),
            "truncated_examples": sum(r["truncated"] for r in rows),
            "generated_tokens_per_second": sum(r["tokens"] for r in rows) / sum(r["decode_seconds"] for r in rows),
        }
    sparse_rows = [r for r in report["rows"] if r["recipe"] == "decode-wanda-bitmask"]
    if report["sparse_calls"] != len(counts) * (1 + sum(r["decode_calls"] for r in sparse_rows)):
        raise ValueError("checkpoint-wide actual kernel calls differ from warmup plus validation")
    if not any(r["ended_with_eos"] for r in report["rows"] if r["recipe"] == "dense"):
        raise ValueError("all-truncated baseline is not meaningful quality evidence")
    return metrics


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--input", type=Path, required=True)
    p.add_argument("--source-commit", required=True)
    a = p.parse_args()
    report = json.loads(a.input.read_text())
    metrics = summarize(report)
    commit = subprocess.check_output(["git", "rev-parse", a.source_commit], cwd=ROOT, text=True).strip()
    hashes = {s: hashlib.sha256(subprocess.check_output(["git", "show", f"{commit}:{s}"], cwd=ROOT)).hexdigest() for s in SOURCES}
    metric_path = "docs/foundation-models/2610.12327-sparse-decoding/metrics/checkpoint-a100-seed42.json"
    receipt_path = "docs/gpu-validations/sparse-decoding-a100-20261011.json"
    limitations = ["Wanda alternative backend, not original SparseGPT experiments",
                  "independent Triton bitmask SpMV, no original kernel speedup claim",
                  "four held-out GSM8K questions; retain every truncation and negative outcome",
                  "dense pruned prefill copy retained; packed bytes are not model memory savings",
                  "single seed mechanism diagnostic, not formal benchmark improvement",
                  "different generated lengths; throughput is descriptive, not matched-output acceleration"]
    metric = {"schema_version": 2, "manifest_ref": "foundation-models:sparse-decoding", "method": "sparse-decoding",
              "dataset": report["dataset"]["id"], "seeds": [report["seed"]], "metrics": metrics,
              "evaluation_protocol": {"tier": "l1_mechanism", "diagnostic_only": True,
                                      "formal_comparison": False, "test_read": False, "seeds": [report["seed"]],
                                      "claim_policy": "bounded actual CUDA mechanism diagnostic; not benchmark improvement"},
              "runtime_details": report, "limitations": limitations,
              "provenance": {"original_code_commit": commit, "artifact_path": metric_path,
                             "executed_source_sha256": hashes,
                             "dataset_fingerprint": hashlib.sha256(json.dumps(report["split_provenance"], sort_keys=True).encode()).hexdigest()}}
    command = ["python", "scripts/run_sparse_decoding_public.py", "--checkpoint-path", "checkpoints/qwen3-4b",
               "--checkpoint-id", report["checkpoint"]["id"], "--checkpoint-revision", report["checkpoint"]["revision"],
               "--train-path", "data/gsm8k-holdout/train.jsonl", "--validation-path", "data/gsm8k-holdout/validation.jsonl",
               "--split-manifest", "data/gsm8k-holdout/split.json", "--dataset-revision", report["dataset"]["revision"],
               "--output", "runs/sparse-decoding-42-512.json", "--calibration-examples", "4", "--validation-examples", "4",
               "--max-tokens", str(report["max_tokens"]), "--seed", str(report["seed"])]
    receipt = {"schema_version": 1, "adapter_key": "sparse-decoding", "validated_at": "2026-10-11",
               "accelerator": {"vendor": "NVIDIA", "model": "A100-SXM4-80GB"}, "command": command,
               "dataset": report["dataset"], "checkpoint": report["checkpoint"], "result": "passed",
               "evaluation_tier": "l1_mechanism", "metrics": metrics, "limitations": limitations,
               "executed_source_sha256": hashes,
               "provenance": {"commit": commit, "artifact_path": receipt_path, "metrics_artifact": metric_path,
                              "checkpoint_committed": False}}
    for relative, payload in ((metric_path, metric), (receipt_path, receipt)):
        target = ROOT / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(json.dumps(payload, ensure_ascii=False, indent=2, allow_nan=False) + "\n")


if __name__ == "__main__":
    main()
