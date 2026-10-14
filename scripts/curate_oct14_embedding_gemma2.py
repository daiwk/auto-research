#!/usr/bin/env python3
"""Curate actual bounded official-checkpoint inference, never official scores."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import subprocess

from auto_research.gpu_validation import validate_gpu_receipt
from auto_research.multimodal.embedding_gemma2 import MODEL_ID, REVISION, WEIGHTS_SHA256, TRANSFORMERS_SOURCE_REVISION

ROOT = Path(__file__).resolve().parents[1]
SOURCE = "b12d469e76f3b5224b29cc5e9f5826b4a89238ca"
METRIC = "docs/multimodal-models/embeddinggemma2/metrics/coco16-a100-seed42.json"
RECEIPT = "docs/gpu-validations/embedding-gemma2-a100-20261014.json"
PATHS = ("src/auto_research/multimodal/embedding_gemma2.py",
         "src/auto_research/oct12_public_sources.py", "scripts/run_embedding_gemma2.py")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, required=True)
    args = parser.parse_args()
    run = json.loads(args.input.read_text())
    if (run["method"], run["device"], run["seed"], run["images"], run["captions"]) != ("embedding-gemma2", "cuda", 42, 16, 80):
        raise ValueError("expected actual fixed 16-image/80-caption CUDA run")
    if not run["measured_locally"] or not run["diagnostic_only"]:
        raise ValueError("bounded diagnostic classification must be retained")
    if (run["checkpoint"]["public_id"], run["checkpoint"]["revision"], run["checkpoint"]["files"]["model.safetensors"]) != (MODEL_ID, REVISION, WEIGHTS_SHA256):
        raise ValueError("fixed official checkpoint bytes required")
    if run["protocol"]["training"] or run["protocol"]["test_used_for_selection"]:
        raise ValueError("this run must not train or select on holdout")
    if set(run["metrics"]) != {"128", "256", "512", "768"} or not run["peak_memory_bytes"]:
        raise ValueError("all four predeclared dimensions and actual CUDA memory measurement required")
    metrics = {f"d{dimension}.{key}": value for dimension, row in run["metrics"].items() for key, value in row.items()}
    metrics.update(elapsed_seconds=run["elapsed_seconds"], peak_memory_bytes=run["peak_memory_bytes"])
    hashes = {path: hashlib.sha256(subprocess.check_output(["git", "show", f"{SOURCE}:{path}"], cwd=ROOT)).hexdigest() for path in PATHS}
    fingerprint = hashlib.sha256(json.dumps(run["dataset"], sort_keys=True).encode()).hexdigest()
    failure = {"commit": "eeb6a53370b24e3b5ebb9c742503426ff762e249", "result": "failed",
               "phase": "retrieval scoring after official model inference", "exception": "IndexError: image index 8 outside 8-vector matrix for 16 requested images",
               "cause": "flat image list interpreted as one multi-image sample per batch",
               "fix": "nested singleton image batches + shape consistency regression; same model/data/budget rerun"}
    payload = {**run, "schema_version": 2, "manifest_ref": "multimodal-models:embedding-gemma2", "seeds": [42],
               "aggregate_metrics": metrics, "failed_attempts": [failure],
               "evaluation_protocol": {"tier": "l2_public_dataset", "seeds": [42], "formal_comparison": False,
                   "claim_policy": "Single deterministic official-checkpoint inference on 16 public images; not full COCO or multi-seed training comparison",
                   "test_used_for_selection": False, "model_training_seeds": [], "seed_scope": "inference runtime only"},
               "provenance": {"code_commit": SOURCE, "artifact_path": METRIC, "dataset_fingerprint": fingerprint,
                              "transformers_source_revision": TRANSFORMERS_SOURCE_REVISION,
                              "executed_source_sha256": hashes, "checkpoint_committed": False}}
    receipt = {"schema_version": 1, "adapter_key": "embedding-gemma2", "validated_at": "2026-10-14",
               "accelerator": {"vendor": "NVIDIA", "model": "A100-SXM4-80GB"},
               "command": ["python", "scripts/run_embedding_gemma2.py", "--dataset-dir", "data/coco40", "--checkpoint-path", "data/embeddinggemma2",
                           "--device", "cuda", "--images", "16", "--seed", "42", "--output", "runs/embedding-gemma2-42"],
               "seed": 42, "dataset": run["dataset"], "checkpoint": run["checkpoint"], "result": "passed",
               "metrics": metrics, "executed_source_sha256": hashes, "failed_attempts": [failure],
               "provenance": {"commit": SOURCE, "artifact_path": RECEIPT, "metrics_artifact": METRIC,
                              "transformers_source_revision": TRANSFORMERS_SOURCE_REVISION, "checkpoint_committed": False},
               "limitations": run["limitations"]}
    errors = validate_gpu_receipt(receipt)
    if errors:
        raise ValueError(errors)
    for relative, content in ((METRIC, payload), (RECEIPT, receipt)):
        path = ROOT / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(content, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps(metrics))


if __name__ == "__main__":
    main()
