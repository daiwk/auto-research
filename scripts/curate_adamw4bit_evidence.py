#!/usr/bin/env python3
"""Curate measured public results and a sanitized receipt; never invent scores."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[1]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--source-commit", required=True)
    args = parser.parse_args()
    payload = json.loads(args.input.read_text())
    assert payload["test_read_after_selection"]
    assert {row["seed"] for row in payload["rows"]} == {42, 43, 44}
    assert len(payload["rows"]) == 9
    assert all(row["steps"] == 200 for row in payload["rows"])
    assert all(("selected_test_loss" in row) == (row["recipe"] == payload["selected_recipe"])
               for row in payload["rows"])
    payload["adapter_key"] = "adamw4bit"
    payload["seeds"] = [42, 43, 44]
    commit = subprocess.check_output(["git", "rev-parse", args.source_commit], cwd=ROOT, text=True).strip()
    payload["code_commit"] = commit
    target = ROOT / "docs/foundation-models/2610.12444-adamw4bit/metrics/public-wikitext.json"
    payload["schema_version"] = 2
    payload["manifest_ref"] = "foundation-models:adamw4bit"
    payload["evaluation_protocol"] = {
        "tier": payload["evaluation_tier"], "seeds": [42, 43, 44],
        "diagnostic_only": True, "formal_comparison": False,
        "claim_policy": payload["claim_scope"],
    }
    payload["provenance"] = {
        "original_code_commit": commit, "artifact_path": str(target.relative_to(ROOT)),
        "dataset_fingerprint": hashlib.sha256(json.dumps(payload["dataset"], sort_keys=True).encode()).hexdigest(),
    }
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(payload, indent=2) + "\n")
    artifact = "docs/gpu-validations/adamw4bit-a100-20261011.json"
    sources = ("src/auto_research/foundation/adamw4bit.py", "scripts/run_adamw4bit_public.py")
    receipt = {
        "schema_version": 1, "adapter_key": "adamw4bit", "validated_at": "2026-10-11",
        "accelerator": {"vendor": "NVIDIA", "model": "A100-SXM4-80GB"},
        "command": ["python", "scripts/run_adamw4bit_public.py", "--data", "data/wikitext-2",
                    "--output", "runs/adamw4bit-public.json", "--steps", "200", "--seeds",
                    "42,43,44", "--device", "cuda"],
        "dataset": payload["dataset"],
        "checkpoint": {**payload["checkpoint"], "revision": "random initialization seeds 42,43,44"},
        "result": "passed", "evaluation_tier": payload["evaluation_tier"],
        "metrics": {"seeds": payload["seeds"], "validation_loss_mean": payload["validation_means"],
                    "persistent_moment_bytes": {r["recipe"]: r["persistent_moment_bytes"]
                                                for r in payload["rows"]}},
        "executed_source_sha256": {s: hashlib.sha256(subprocess.check_output(
            ["git", "show", f"{commit}:{s}"], cwd=ROOT)).hexdigest() for s in sources},
        "limitations": [payload["claim_scope"], "Both quantized recipes lost to FP32 validation loss",
                        "Persistent moment storage is not end-to-end peak memory or latency"],
        "provenance": {"commit": commit, "artifact_path": artifact,
                       "metrics_artifact": str(target.relative_to(ROOT)), "checkpoint_committed": False},
    }
    (ROOT / artifact).write_text(json.dumps(receipt, indent=2) + "\n")


if __name__ == "__main__":
    main()
