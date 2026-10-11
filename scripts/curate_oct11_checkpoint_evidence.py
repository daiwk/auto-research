#!/usr/bin/env python3
"""Archive measured, scoped checkpoint diagnostics with sanitized provenance."""
from __future__ import annotations

import argparse
from copy import deepcopy
import hashlib
import json
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[1]
PAPERS = {
    "vfold": ("foundation-models", "2610.12338", ["foundation/vfold.py", "foundation/vfold_cache.py"],
              "run_vfold_checkpoint.py"),
    "recal": ("post-training", "2610.11332", ["post_training/recal.py"], "run_recal_checkpoint.py"),
    "zcpo": ("post-training", "2610.12161", ["post_training/oct11_objectives.py", "post_training/oct11_checkpoint.py"],
             "run_zcpo_checkpoint.py"),
    "opd-learning-signals": ("post-training", "2610.11247", ["post_training/learning_signals.py"],
                             "run_opd_learning_signals.py"),
}


def summarize(key, report):
    if report.get("adapter_key") != key or not report.get("diagnostic_only") or report.get("seed") != 42:
        raise ValueError("matching diagnostic runtime artifact required")
    if key == "vfold":
        by_example = {}
        for row in report["rows"]:
            by_example.setdefault(row["example"], {})[row["recipe"]] = row
        comparable = []
        for example, pair in by_example.items():
            full, folded = pair["full"], pair["vfold"]
            if full["cache_tokens"] == folded["cache_tokens"]:
                comparable.append({"example": example, "cache_tokens": full["cache_tokens"],
                                   "full_bytes": full["persistent_cache_bytes"],
                                   "vfold_bytes": folded["persistent_cache_bytes"],
                                   "reduction_fraction": 1 - folded["persistent_cache_bytes"] / full["persistent_cache_bytes"]})
        if not comparable or report["exact_fold_relative_logit_error"] > .02:
            raise ValueError("successful function check and same-length memory comparisons required")
        return {"bf16_fold_relative_logit_error": report["exact_fold_relative_logit_error"],
                "matched_length_cache_examples": len(comparable),
                "matched_length_cache_reduction_mean": sum(x["reduction_fraction"] for x in comparable) / len(comparable)}, comparable
    if key == "recal":
        rows = report["rows"]
        if {r["recipe"] for r in rows} != {"base-wanda", "recal-wanda"} or len({r["retained_width"] for r in rows}) != 1:
            raise ValueError("paired recipes at the same physical width required")
        for row in rows:
            if row["adapter_delta_l2"] <= 0 or not row["opd_history"] or not all(h["gradient_l2"] > 0 for h in row["opd_history"]):
                raise ValueError("actual recovery updates required")
        return {r["recipe"]: {"retained_width": r["retained_width"],
                               "parameters_after_pruning": r["parameters_after_pruning"],
                               "adapter_delta_l2": r["adapter_delta_l2"], **r["stages"]} for r in rows}, []
    if key == "zcpo":
        metrics = report["metrics"]
        if metrics["active_groups"] != sum(bool(h["active"]) for h in report["history"]) or metrics["adapter_parameter_delta_l2"] <= 0:
            raise ValueError("verified active updates and parameter movement required")
        return metrics, []
    rows = report["rows"]
    if len(report["layerwise_prompt_cka"]) != len(report["representation_positions"]) or len(report["representation_positions"]) != 37:
        raise ValueError("all 37 Qwen3 hidden-state positions required")
    if not rows or not all(r["pre_clip_gradient_l2"] > 0 for r in rows):
        raise ValueError("real gradients required")
    return {"steps": len(rows), "first_residual": rows[0]["top16_residual_global_token_mean"],
            "last_residual": rows[-1]["top16_residual_global_token_mean"],
            "lora_parameter_delta_l2": report["parameter_statistics"]["delta_l2"],
            "representation_positions": 37,
            "prompt_cka_min": min(report["layerwise_prompt_cka"])}, []


def curate(key, report, *, commit, split=None):
    report = deepcopy(report)
    metrics, comparisons = summarize(key, report)
    if split is not None:
        # A post-run digest attestation does not pretend the old runner loaded
        # a split manifest. Its executed data hashes must match the manifest.
        hashes = report["dataset"]
        if split.get("source_split") != "train" or split.get("test_opened") is not False:
            raise ValueError("training-only source required")
        if any(hashes[f"{name}_sha256"] != split["partition_sha256"][name] for name in ("train", "validation")):
            raise ValueError("executed partitions differ from the training-only manifest")
        report["post_run_split_attestation"] = split
    elif not report.get("split_provenance", {}).get("verified"):
        raise ValueError("verified training-only holdout provenance required")
    domain, paper, sources, script = PAPERS[key]
    metric_path = f"docs/{domain}/{paper}-{key}/metrics/checkpoint-a100-seed42.json"
    receipt_path = f"docs/gpu-validations/{key}-a100-20261011.json"
    sources = [f"src/auto_research/{s}" for s in sources] + [f"scripts/{script}"]
    hashes = {s: hashlib.sha256(subprocess.check_output(["git", "show", f"{commit}:{s}"], cwd=ROOT)).hexdigest()
              for s in sources}
    checkpoint = report.get("checkpoint") or {"student": report["student"], "teacher": report["teacher"],
                                             "revision": report["student"]["revision"]}
    dataset = report.get("dataset") or {"id": report["split_provenance"]["source_id"],
                                       "revision": report["split_provenance"]["source_revision"]}
    # Model responses are raw runtime data, not stable metric artifacts.
    if key == "vfold":
        report["rows"] = [{k: v for k, v in row.items() if k != "response"} for row in report["rows"]]
    payload = {"schema_version": 2, "manifest_ref": f"{domain}:{key}", "method": key,
               "dataset": dataset["id"], "seeds": [42], "metrics": metrics,
               "seed_results": [{"seed": 42, **metrics}],
               "evaluation_protocol": {"tier": "l1_mechanism", "formal_comparison": False,
                                       "diagnostic_only": True, "test_read": False,
                                       "seeds": [42],
                                       "claim_policy": "bounded real-checkpoint diagnostic, not benchmark gain"},
               "runtime_details": report, "matched_length_cache_comparisons": comparisons,
               "provenance": {"original_code_commit": commit, "artifact_path": metric_path,
                              "dataset_fingerprint": hashlib.sha256(json.dumps(
                                  report.get("split_provenance") or split, sort_keys=True).encode()).hexdigest()}}
    command = ["python", f"scripts/{script}"]
    if key == "opd-learning-signals":
        command += ["--student-path", "checkpoints/student", "--teacher-path", "checkpoints/teacher",
                    "--student-id", report["student"]["id"], "--student-revision", report["student"]["revision"],
                    "--teacher-id", report["teacher"]["id"], "--teacher-revision", report["teacher"]["revision"],
                    "--steps", "3", "--max-tokens", "128", "--representation-prompts", "8"]
    else:
        command += ["--checkpoint-path", "checkpoints/qwen3-4b", "--checkpoint-id", checkpoint["id"],
                    "--checkpoint-revision", checkpoint["revision"]]
    if key == "vfold":
        command += ["--calibration-examples", "32", "--validation-examples", "4", "--max-tokens", "256"]
    elif key == "recal":
        command += ["--calibration-examples", "4", "--opd-steps", "4", "--max-tokens", "512",
                    "--validation-examples", "4", "--keep-ratio", "0.75"]
    elif key == "zcpo":
        command += ["--steps", "24", "--max-tokens", "256", "--group", "4", "--validation-examples", "8"]
    command += ["--dataset-revision", dataset["revision"], "--train-path", "data/gsm8k-holdout/train.jsonl",
                "--validation-path", "data/gsm8k-holdout/validation.jsonl", "--seed", "42", "--device", "cuda",
                "--output", f"runs/{key}-42.json"]
    if split is None:
        command += ["--split-manifest", "data/gsm8k-holdout/split.json"]
    receipt = {"schema_version": 1, "adapter_key": key, "validated_at": "2026-10-11",
               "accelerator": {"vendor": "NVIDIA", "model": "A100-SXM4-80GB"},
               "command": command, "dataset": dataset, "checkpoint": checkpoint,
               "result": "passed", "evaluation_tier": "l1_mechanism", "metrics": metrics,
               "executed_source_sha256": hashes, "limitations": report.get("limitations", [report.get("claim_scope")]),
               "provenance": {"commit": commit, "artifact_path": receipt_path,
                              "metrics_artifact": metric_path, "checkpoint_committed": False}}
    return {metric_path: payload, receipt_path: receipt}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--kind", choices=PAPERS, required=True)
    p.add_argument("--input", type=Path, required=True)
    p.add_argument("--source-commit", required=True)
    p.add_argument("--split-manifest", type=Path)
    a = p.parse_args()
    commit = subprocess.check_output(["git", "rev-parse", a.source_commit], cwd=ROOT, text=True).strip()
    split = json.loads(a.split_manifest.read_text()) if a.split_manifest else None
    for relative, payload in curate(a.kind, json.loads(a.input.read_text()), commit=commit, split=split).items():
        path = ROOT / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(payload, ensure_ascii=False, allow_nan=False, indent=2) + "\n")


if __name__ == "__main__":
    main()
