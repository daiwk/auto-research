#!/usr/bin/env python3
"""Curate bounded, real PIVOT arms without promoting short-run accuracy."""
from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[1]
SOURCES = ["scripts/run_pivot_checkpoint.py"] + [
    f"src/auto_research/post_training/{name}.py" for name in
    ("pivot_checkpoint", "pivot_intent", "oct11_objectives", "oct10_checkpoint")
] + ["src/auto_research/public_holdout.py"]


def validate_evaluation(value, count):
    rows = value["rows"]
    if len(rows) != count or value["examples"] != count or not count:
        raise ValueError("matched nonempty validation budgets required")
    for key, field in (("accuracy", "correct"), ("parse_rate", "valid_prediction"),
                       ("eos_completion_fraction", "ended_with_eos")):
        if not math.isclose(value[key], sum(r[field] for r in rows) / count):
            raise ValueError("evaluation aggregates disagree with retained outcomes")
    if any(r["tokens"] < 1 or (r["correct"] and not r["valid_prediction"]) for r in rows):
        raise ValueError("invalid response accounting")


def summarize(report):
    if (report.get("adapter_key") != "pivot" or report.get("diagnostic_only") is not True
            or report.get("test_read") is not False or not report.get("split_provenance", {}).get("verified")):
        raise ValueError("real train-only diagnostic with verified split required")
    protocol = report["protocol"]
    if (not protocol["shared_warmup_and_reset"] or not protocol["full_vocabulary_kl"]
            or protocol["reference"] != "frozen shared warmup adapters"
            or protocol["validation_selection"] or protocol["kl_beta"] != .001):
        raise ValueError("shared state, full-vocabulary KL and isolated selection required")
    for checkpoint in (report["student"], report["teacher"]):
        if not checkpoint.get("id") or len(checkpoint.get("revision", "")) != 40:
            raise ValueError("immutable public model revisions required")
    budget = report["budgets"]
    b, g, steps = budget["batch_size"], budget["group"], budget["steps"]
    if min(b, g) < 2 or steps < 4 or budget["max_tokens"] < 512 or budget["sft_epochs"] != 2:
        raise ValueError("meaningful routing/group budget and shared two-epoch SFT required")
    if (len(report["sft_history"]) != budget["sft_epochs"] * budget["training_examples"]
            or len(report["opd_warmup_history"]) != budget["warmup_steps"]
            or not report["sft_history"] or not report["opd_warmup_history"]):
        raise ValueError("shared warmup execution is incomplete")
    if not all(math.isfinite(r["loss"]) and r["gradient_l2"] > 0 for r in report["sft_history"]):
        raise ValueError("real teacher-response SFT updates required")
    n = budget["validation_examples"]
    for evaluation in (report["baseline"], report["shared_warmup_validation"]):
        validate_evaluation(evaluation, n)
    metrics = {}
    if [arm["recipe"] for arm in report["arms"]] != ["opd", "global", "pivot"]:
        raise ValueError("all three arms in fixed order required")
    mixed = False
    for arm in report["arms"]:
        recipe, history = arm["recipe"], arm["history"]
        if len(history) != steps or not math.isfinite(arm["adapter_delta_l2"]) or arm["adapter_delta_l2"] <= 0:
            raise ValueError("budget-matched real parameter changes required")
        heterogeneous = 0
        routed_prompts = 0
        for index, record in enumerate(history, 1):
            routes = record["routed_grpo"]
            rewards = record["rewards"]
            if (record["step"] != index or record["recipe"] != recipe or len(routes) != b
                    or len(rewards) != b or any(len(row) != g for row in rewards)
                    or len(record["acquisition_scores"]) != b):
                raise ValueError("unaligned executed batch/step/reward records")
            ratio = .5 * (1 - math.cos(math.pi * index / steps))
            expected = (0 if recipe == "opd" else b * int(index > steps // 2)
                        if recipe == "global" else math.floor(ratio * b + 1e-10))
            if sum(routes) != expected:
                raise ValueError("executed route differs from fixed recipe/schedule")
            if recipe == "pivot":
                expected_indices = sorted(range(b), key=lambda i: (record["acquisition_scores"][i], i))[:expected]
                if {i for i, routed in enumerate(routes) if routed} != set(expected_indices):
                    raise ValueError("PIVOT did not route lowest teacher perplexities")
                mixed |= 0 < sum(routes) < b
            if (not math.isfinite(record["loss"]) or not math.isfinite(record["gradient_l2"])
                    or record["active"] != (record["gradient_l2"] > 0)
                    or not 0 <= record["truncated_rollouts"] <= b * g or record["response_tokens"] < b * g):
                raise ValueError("invalid update/truncation accounting")
            heterogeneous += sum(bool(routed and max(row) > min(row)) for routed, row in zip(routes, rewards))
            routed_prompts += sum(routes)
        validate_evaluation(arm["validation"], n)
        metrics[recipe] = {
            "validation_accuracy": arm["validation"]["accuracy"],
            "validation_parse_rate": arm["validation"]["parse_rate"],
            "validation_eos_completion_fraction": arm["validation"]["eos_completion_fraction"],
            "validation_examples": n, "adapter_parameter_delta_l2": arm["adapter_delta_l2"],
            "active_steps": sum(r["active"] for r in history), "routed_grpo_prompts": routed_prompts,
            "grpo_reward_heterogeneous_groups": heterogeneous,
            "truncated_training_rollouts": sum(r["truncated_rollouts"] for r in history),
        }
    if not mixed:
        raise ValueError("at least one actually mixed OPD/GRPO minibatch required")
    return metrics


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--input", type=Path, required=True)
    p.add_argument("--source-commit", required=True)
    a = p.parse_args()
    report = json.loads(a.input.read_text())
    metrics = summarize(report)
    commit = subprocess.check_output(["git", "rev-parse", a.source_commit], cwd=ROOT, text=True).strip()
    hashes = {s: hashlib.sha256(subprocess.check_output(["git", "show", f"{commit}:{s}"], cwd=ROOT)).hexdigest()
              for s in SOURCES}
    metric_path = "docs/post-training/2610.11167-pivot/metrics/checkpoint-a100-seed42.json"
    receipt_path = "docs/gpu-validations/pivot-a100-20261011.json"
    limitations = ["single-seed few-example intent mechanism diagnostic, not benchmark gains",
                   "q/v LoRA rather than original full-parameter finetuning",
                   "77 label names without unavailable author intent definitions",
                   "fixed half-budget global transition and equal post-warmup learning rates; no test selection",
                   "reward-homogeneous GRPO groups and response truncations retained"]
    command = ["python", "scripts/run_pivot_checkpoint.py"]
    for key, value in (("student-path", "checkpoints/qwen2.5-0.5b"), ("teacher-path", "checkpoints/qwen2.5-7b"),
                       ("student-id", report["student"]["id"]), ("student-revision", report["student"]["revision"]),
                       ("teacher-id", report["teacher"]["id"]), ("teacher-revision", report["teacher"]["revision"]),
                       ("dataset-revision", report["dataset"]["revision"]),
                       ("train-path", "data/pivot-banking77/train.jsonl"),
                       ("validation-path", "data/pivot-banking77/validation.jsonl"),
                       ("split-manifest", "data/pivot-banking77/split.json"), ("seed", report["seed"]),
                       ("device", "cuda"), ("output", "runs/pivot-42.json")):
        command.extend(["--" + key, str(value)])
    for key, value in report["budgets"].items():
        command.extend(["--" + key.replace("_", "-"), str(value)])
    provenance = {"commit": commit, "artifact_path": receipt_path,
                  "metrics_artifact": metric_path, "checkpoint_committed": False}
    receipt = {"schema_version": 1, "adapter_key": "pivot", "validated_at": "2026-10-11",
               "accelerator": {"vendor": "NVIDIA", "model": "A100-SXM4-80GB"}, "command": command,
               "dataset": report["dataset"], "checkpoint": {"student": report["student"], "teacher": report["teacher"]},
               "result": "passed", "evaluation_tier": "l1_mechanism", "metrics": metrics,
               "limitations": limitations, "executed_source_sha256": hashes, "provenance": provenance}
    metric = {"schema_version": 2, "manifest_ref": "post-training:pivot", "method": "pivot",
              "dataset": report["dataset"]["id"], "seeds": [report["seed"]], "metrics": metrics,
              "evaluation_protocol": {"tier": "l1_mechanism", "diagnostic_only": True,
                                      "formal_comparison": False, "test_read": False, "seeds": [report["seed"]],
                                      "claim_policy": "actual bounded routing/training, not benchmark improvement"},
              "runtime_details": report, "limitations": limitations,
              "provenance": {"original_code_commit": commit, "artifact_path": metric_path,
                             "executed_source_sha256": hashes,
                             "dataset_fingerprint": hashlib.sha256(json.dumps(report["split_provenance"], sort_keys=True).encode()).hexdigest()}}
    for relative, payload in ((metric_path, metric), (receipt_path, receipt)):
        target = ROOT / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(json.dumps(payload, ensure_ascii=False, indent=2, allow_nan=False) + "\n")


if __name__ == "__main__":
    main()
