#!/usr/bin/env python3
"""Curate real UxSID/State-OPD/proximal runs without dropping negative outcomes."""
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
IDS = {"uxsid": "2605.09040", "state-opd": "2610.13238",
       "gppo-framework": "2610.13015", "tapo-trajectory": "2610.13020"}


def statistic(values):
    return {"mean": statistics.mean(values), "std": statistics.stdev(values), "n": len(values)}


def source_hashes(commit, paths):
    return {path: hashlib.sha256(subprocess.check_output(
        ["git", "show", f"{commit}:{path}"], cwd=ROOT)).hexdigest() for path in paths}


def summarize(key, runs):
    if any(run.get("method") != key or run.get("seed") != seed or not run.get("diagnostic_only")
           or run.get("device") != "cuda" for run, seed in zip(runs, SEEDS, strict=True)):
        raise ValueError("three actual CUDA runs with matching method/seeds are required")
    if key == "uxsid":
        if any(not all(row["parameters_changed"] for row in run["variants"].values())
               or run["cache"]["offline_online_max_abs_error"] > 1e-5 for run in runs):
            raise ValueError("actual training in every ablation and cache parity required")
        metrics = {f"{variant}.test.{metric}": statistic([
            run["variants"][variant]["test"][metric] for run in runs])
                   for variant in ("global-only", "agnostic", "ungated", "uxsid")
                   for metric in ("roc_auc", "pr_auc")}
        metrics["cache.max_abs_error"] = max(run["cache"]["offline_online_max_abs_error"] for run in runs)
        return metrics, runs[0]["dataset"], runs[0]["checkpoint"], {
            "completed_seeds": 3, "retrained_variants_per_seed": 4,
            "validation_selected_variants": [run["validation_selected_variant"] for run in runs],
            "test_selection": False, "cached_direct_parity_checked": True,
            "production_latency_measured": False}
    if key == "state-opd":
        if any(not run["parameters_changed"] or run["execution_status"] != "passed"
               or not all(step["optimizer_update_executed"] and step["gradient_l2_norm"] > 0
                          for step in run["training"])
               or any(audit["additional_actions_executed"] != 0 for audit in run["trajectory_audits"])
               for run in runs):
            raise ValueError("nonzero gradient updates and zero execution of expanded actions required")
        metrics = {f"{arm}.{metric}": statistic([run[arm][metric] for run in runs])
                   for arm in ("baseline", "method_metrics")
                   for metric in ("accuracy", "submission_rate", "mean_executed_actions")}
        return metrics, runs[0]["dataset"], {"student": runs[0]["student"], "teacher": runs[0]["teacher"]}, {
            "completed_seeds": 3, "actual_gradient_steps": [len(run["training"]) for run in runs],
            "expanded_actions_executed": 0, "same_response_prefix_supervision": True,
            "teacher_prior_reasoning_removed": True, "gold_in_policy": False, "official_test_read": False,
            "zero_validation_accuracy_retained": True}
    if any(not run["parameters_changed"] or not run["training"]
           or not all(update["gradient_l2_norm"] > 0
                      for step in run["training"] for update in step["updates"]) for run in runs):
        raise ValueError("real nonzero-advantage updates required; never curate failure.json as passed")
    metrics = {f"{arm}.accuracy": statistic([run[arm]["accuracy"] for run in runs])
               for arm in ("baseline", "method_metrics")}
    return metrics, runs[0]["dataset"], runs[0]["checkpoint"], {
        "completed_seeds": 3,
        "rollout_groups_per_seed": [len(run["training"]) for run in runs],
        "actual_gradient_steps": [sum(len(step["updates"]) for step in run["training"]) for run in runs],
        "rejected_zero_advantage_groups": [run["sampling"]["zero_advantage_groups_retained"] for run in runs],
        "generated_tokens_including_rejected_groups": [
            run["sampling"]["generated_training_tokens_including_rejected_groups"] for run in runs],
        "gold_in_policy": False, "official_test_read": False}


def curate(key, directory, commit):
    runs = [json.loads((directory / f"{key}-{seed}" / "result.json").read_text()) for seed in SEEDS]
    metrics, dataset, checkpoint, checks = summarize(key, runs)
    controls = {}
    if key in {"gppo-framework", "tapo-trajectory"}:
        control_runs = [json.loads((directory / f"grpo-control-{seed}" / "result.json").read_text())
                        for seed in SEEDS]
        control_metrics, control_dataset, control_checkpoint, control_checks = summarize("grpo-control", control_runs)
        if dataset != control_dataset or checkpoint != control_checkpoint:
            raise ValueError("GRPO control must use the same verified inputs")
        for run, control in zip(runs, control_runs, strict=True):
            for field in ("steps", "group", "max_tokens", "inner_updates", "learning_rate"):
                if run["protocol"][field] != control["protocol"][field]:
                    raise ValueError(f"control budget mismatch: {field}")
            if run["baseline"] != control["baseline"]:
                raise ValueError("paired control must start at the same measured initial student")
        metrics["grpo_control.validation.accuracy"] = control_metrics["method_metrics.accuracy"]
        metrics["paired_accuracy_difference_vs_grpo"] = statistic([
            run["method_metrics"]["accuracy"] - control["method_metrics"]["accuracy"]
            for run, control in zip(runs, control_runs, strict=True)])
        controls["grpo-control"] = {"seed_results": control_runs, "execution_checks": control_checks,
                                    "matched_upper_bound_budget": True, "matched_actual_compute": False}
        checks["independent_grpo_control_completed"] = True
    artifact = f"docs/reproductions/{IDS[key]}-{key}/metrics/public-a100-seeds42-44.json"
    receipt_path = f"docs/gpu-validations/{key}-a100-20261013.json"
    limitations = ["Three-seed bounded mechanism diagnostic, not a stable capability/production gain claim.",
                   "Original-paper results are not copied into measured local metrics."]
    if key == "uxsid":
        paths = ["scripts/run_uxsid.py", "src/auto_research/reproductions/uxsid/model.py",
                 "src/auto_research/reproductions/uxsid/experiment.py", "src/auto_research/oct12_public_sources.py",
                 "src/auto_research/reproductions/forte/experiment.py", "src/auto_research/datasets.py"]
        command = ["python", "scripts/run_uxsid.py", "--dataset-dir", "data", "--encoder-path",
                   "checkpoints/qwen2.5-0.5b", "--device", "cuda", "--seed", "42", "--epochs", "3",
                   "--batch-size", "256", "--max-history", "256", "--output", "runs/uxsid-42"]
        limitations += ["MovieLens observed-rating classification, not XLong/KuaiRec or advertising CTR.",
                        "Local text-only semantic encoding and explicit hybrid codebook replace private multimodal/LETTER protocol."]
    elif key == "state-opd":
        paths = ["scripts/run_state_opd.py", "src/auto_research/reproductions/state_opd/checkpoint.py",
                 "src/auto_research/reproductions/state_opd/algorithm.py",
                 "src/auto_research/reproductions/state_opd/environment.py"]
        command = ["python", "scripts/run_state_opd.py", "--student-path", "checkpoints/qwen2.5-0.5b",
                   "--student-id", "Qwen/Qwen2.5-0.5B-Instruct", "--student-revision", checkpoint["student"]["revision"],
                   "--teacher-path", "checkpoints/qwen2.5-7b", "--teacher-id", "Qwen/Qwen2.5-7B-Instruct",
                   "--teacher-revision", checkpoint["teacher"]["revision"], "--device", "cuda", "--seed", "42",
                   "--steps", "2", "--max-turns", "3", "--max-tokens", "256", "--multiplicity", "2",
                   "--concentration", "2", "--validation-examples", "8", "--output", "runs/state-opd-42"]
        limitations += ["Public arithmetic tool episodes, not ALFWorld/ScienceWorld/WebShop.",
                        "All measured before/after validation accuracies are zero; actual updates do not establish task improvement.",
                        "Baseline here is the initial student, not a separately trained full-history OPD control."]
    else:
        paths = ["scripts/run_proximal_papers.py", "src/auto_research/post_training/proximal_checkpoint.py",
                 f"src/auto_research/reproductions/{key.replace('-', '_')}/objective.py"]
        command = ["python", "scripts/run_proximal_papers.py", "--method", key,
                   "--student-path", "checkpoints/qwen2.5-0.5b", "--student-id", "Qwen/Qwen2.5-0.5B-Instruct",
                   "--student-revision", checkpoint["revision"], "--device", "cuda", "--seed", "42",
                   "--steps", "3", "--group", "4", "--max-tokens", "512", "--inner-updates", "2",
                   "--max-task-attempts", "16", "--validation-examples", "8", "--output", f"runs/{key}-42"]
        limitations += ["Eight holdout questions and three updates are not the original large-model benchmark.",
                        "Sampling rejections are counted; equal optimizer steps are not equal total compute."]
    if key != "uxsid":
        paths += ["src/auto_research/post_training/response_policy.py", "src/auto_research/post_training/oct10_checkpoint.py",
                  "src/auto_research/oct12_public_sources.py", "src/auto_research/public_holdout.py"]
        command += ["--train-path", "data/gsm8k-holdout/train.jsonl", "--validation-path",
                    "data/gsm8k-holdout/validation.jsonl", "--split-manifest", "data/gsm8k-holdout/split.json",
                    "--dataset-revision", dataset["source_revision"]]
    fingerprint = hashlib.sha256(json.dumps(dataset, sort_keys=True).encode()).hexdigest()
    payload = {"schema_version": 2, "adapter_key": key, "method": key, "manifest_ref": f"reproduction:{key}",
               "diagnostic_only": True, "measured_locally": True, "seeds": list(SEEDS), "dataset": dataset,
               "checkpoint": checkpoint, "aggregate_metrics": metrics, "seed_results": runs,
               "controls": controls,
               "evaluation_protocol": {"tier": "l2_public_dataset", "seeds": list(SEEDS),
                                       "formal_comparison": False, "test_used_for_selection": False,
                                       "claim_policy": "scoped mechanism diagnostic; do not claim stable capability or production uplift"},
               "provenance": {"code_commit": commit, "artifact_path": artifact,
                              "dataset_fingerprint": fingerprint}, "limitations": limitations}
    receipt = {"schema_version": 1, "adapter_key": key, "validated_at": "2026-10-13",
               "accelerator": {"vendor": "NVIDIA", "model": "A100-SXM4-80GB"}, "command": command,
               "additional_seeds": list(SEEDS[1:]), "dataset": dataset, "checkpoint": checkpoint,
               "result": "passed", "metrics": metrics, "execution_checks": checks, "limitations": limitations,
               "executed_source_sha256": source_hashes(commit, paths),
               "provenance": {"commit": commit, "artifact_path": receipt_path,
                              "metrics_artifact": artifact, "checkpoint_committed": False}}
    errors = validate_gpu_receipt(receipt)
    if errors:
        raise ValueError(errors)
    for relative, content in ((artifact, payload), (receipt_path, receipt)):
        path = ROOT / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(content, ensure_ascii=False, indent=2) + "\n")
    return {"key": key, "metrics": metrics, "checks": checks}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--key", choices=IDS, required=True)
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--executed-commit", required=True)
    args = parser.parse_args()
    print(json.dumps(curate(args.key, args.input, args.executed_commit), indent=2))


if __name__ == "__main__":
    main()
