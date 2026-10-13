#!/usr/bin/env python3
"""Actual teacher KD/layout training -> same-task new-student control evidence."""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
import math
from pathlib import Path
import statistics
import subprocess
import tarfile

from auto_research.gpu_validation import validate_gpu_receipt
from auto_research.reproductions.lewam.external import PINS, validate_training_evidence

ROOT = Path(__file__).resolve().parents[1]
SEEDS = (42, 43, 44)
DOC = "docs/reproductions/2610.13740-smolwam/metrics"


def verify_pair(training: dict, evaluation: dict, seed: int, implementation: dict,
                train_request: dict, eval_request: dict) -> None:
    for run in (training, evaluation):
        if (run.get("paper") != "smolwam" or run.get("seed") != seed or run.get("device") != "cuda"
                or run.get("source_revision") != PINS["smolwam"] or run.get("executed") is not True
                or run.get("diagnostic_only") is not True or run.get("promotion_eligible") is not False):
            raise ValueError("actual matching CUDA diagnostic identity required")
    for request, phase in ((train_request, "train"), (eval_request, "eval")):
        if request.get("seed") != seed or request.get("phase") != phase or request.get("device") != "cuda":
            raise ValueError("actual worker request identity required")
    budget = {"training_episodes": 8, "training_steps": 8, "curriculum_fraction": 0.25,
              "bank_batch_size": 2, "teacher_batch_size": 1, "training_batch_size": 1, "max_training_rows": 32}
    if (any(train_request.get(name) != value for name, value in budget.items())
            or eval_request.get("tasks") != ["libero_goal:6"] or eval_request.get("trials") != 2
            or eval_request.get("action_budget") != 300 or not eval_request.get("trained_model_dir")
            or Path(eval_request["trained_model_dir"]) != Path(train_request["result_path"]).parent / "native-training/student"):
        raise ValueError("fixed native budget and actual same-task student path required")
    candidate = training.get("trained_candidate", {})
    metric = training.get("variants", {}).get("distillation_training", {})
    validate_training_evidence("smolwam", metric, candidate.get("training_evidence", {}))
    if (candidate.get("kind") != "local-trained-candidate" or candidate.get("seed") != seed
            or candidate.get("paper") != "smolwam" or candidate.get("source_revision") != PINS["smolwam"]
            or candidate.get("selection") != "validation only" or candidate.get("metrics") != metric
            or candidate.get("implementation_sha256") != implementation
            or set(candidate.get("files", {})) != {"best.pt"}
            or not isinstance(candidate["files"]["best.pt"], str) or len(candidate["files"]["best.pt"]) != 64
            or set(candidate["files"]["best.pt"]) - set("0123456789abcdef")
            or evaluation.get("trained_candidate") != candidate or candidate.get("dataset") != training.get("dataset")):
        raise ValueError("actual selected new student, local source and training data must match")
    protocol = training.get("protocol", {})
    if (protocol.get("teacher_targets_actual_model") is not True or protocol.get("teacher_targets_cover_validation") is not True
            or protocol.get("original_source_unchanged") is not True or protocol.get("steps") != 8
            or protocol.get("layout_switch_step") != 2 or protocol.get("episodes") != 8
            or protocol.get("rows") != metric.get("real_teacher_target_rows")
            or metric.get("optimizer_updates") != 8 or metric.get("teacher_layout_updates") != 2
            or metric.get("compact_layout_updates") != 6):
        raise ValueError("actual teacher targets and both fixed native layouts required")
    adapter = training.get("latent_adapter", {})
    keys = adapter.get("tensor_keys", [])
    if (adapter.get("kind") != "derived-frozen-latent-adapter-only"
            or adapter.get("source_sha256") != training.get("pretrained_adapter_text", {}).get("files", {}).get("model.safetensors")
            or adapter.get("released_trunk_text_or_student_weights_loaded") is not False
            or not isinstance(keys, list) or not all(isinstance(name, str) for name in keys)
            or len(keys) != 62 or len(set(keys)) != 62
            or not all(name.startswith(("adapter.", "adapter_inv.")) for name in keys)
            or not any(name.startswith("adapter.") for name in keys) or not any(name.startswith("adapter_inv.") for name in keys)
            or not isinstance(adapter.get("sha256"), str) or len(adapter["sha256"]) != 64
            or set(adapter["sha256"]) - set("0123456789abcdef")):
        raise ValueError("actual complete native adapter-only provenance required")
    control = evaluation.get("protocol", {})
    if (control.get("tasks") != ["libero_goal:6"] or control.get("trials") != 2
            or not all(control.get(name) is True for name in ("world_head_executed", "teacher_distillation_retrained",
                       "layout_curriculum_retrained", "new_student_closed_loop_evaluated", "nonofficial_benchmark"))
            or set(evaluation.get("episodes", {})) != {"smolwam", "noop"}):
        raise ValueError("actual same-task new-student closed-loop required")
    starts = []
    for arm in ("smolwam", "noop"):
        episodes = evaluation["episodes"][arm]
        if (len(episodes) != 2 or any(row.get("task") != "libero_goal:6" or type(row.get("success")) is not bool
                or type(row.get("actions_executed")) is not int or not 0 < row["actions_executed"] <= 300
                or type(row.get("wall_seconds")) not in {int, float} or not math.isfinite(row["wall_seconds"])
                or row["wall_seconds"] <= 0 or type(row.get("initial_state_id")) is not int
                or type(row.get("policy_queries")) is not int
                or (row["policy_queries"] <= 0 if arm == "smolwam" else row["policy_queries"] != 0)
                for row in episodes)):
            raise ValueError("real finite policy/action episodes required")
        summary = evaluation.get("variants", {}).get(arm, {})
        if (summary.get("episodes") != 2 or summary.get("actions_executed") != sum(row["actions_executed"] for row in episodes)
                or summary.get("success_rate") != sum(row["success"] for row in episodes) / 2):
            raise ValueError("measured summaries must match actual control episodes")
        starts.append([row["initial_state_id"] for row in episodes])
    if starts[0] != starts[1] or len(set(starts[0])) != 2:
        raise ValueError("new student and no-op must share the same distinct trial initial states")
    latency = evaluation.get("latency_seconds_mean")
    if type(latency) not in {int, float} or not math.isfinite(latency) or latency <= 0:
        raise ValueError("actual finite new-student query latency required")


def curate(directory: Path, commit: str, source_archive: Path) -> dict:
    paths = ["src/auto_research/reproductions/lewam/external.py", *[
        f"src/auto_research/reproductions/smolwam/{name}.py" for name in ("algorithm", "training", "worker")]]
    hashes = {}
    with tarfile.open(source_archive) as archive:
        for name in paths:
            packed = archive.extractfile(name).read()
            if packed != subprocess.check_output(["git", "show", f"{commit}:{name}"], cwd=ROOT):
                raise ValueError("source archive differs from actual executed commit")
            hashes[name] = hashlib.sha256(packed).hexdigest()
    implementation = {name.removeprefix("src/auto_research/reproductions/"): digest for name, digest in hashes.items()}
    pairs, walls = [], []
    for seed in SEEDS:
        training, evaluation = [json.loads((directory / f"smolwam-{phase}-seed{seed}.json").read_text()) for phase in ("train", "candidate")]
        requests = [json.loads((directory / f"smolwam-{phase}-request-seed{seed}.json").read_text()) for phase in ("train", "candidate")]
        verify_pair(training, evaluation, seed, implementation, *requests)
        completions = [row["wall_seconds"] for line in (directory / f"smolwam-seed{seed}-launch.log").read_text().splitlines()
                       if line.startswith("{") for row in [json.loads(line)] if row.get("completed") is True]
        if (len(completions) != 1 or type(completions[0]) not in {int, float}
                or not math.isfinite(completions[0]) or not 0 < completions[0] <= 1800):
            raise ValueError("actual train-control total wall must stay within 1800 seconds")
        pairs.append((training, evaluation))
        walls.append(completions[0])
    metrics = {f"{arm}.success_rate": {"mean": statistics.mean(values), "std": statistics.stdev(values), "n": 3}
               for arm in ("smolwam", "noop") for values in [[evaluation["variants"][arm]["success_rate"] for _, evaluation in pairs]]}
    raw = {}
    for seed in SEEDS:
        for phase in ("train", "candidate"):
            name = f"smolwam-{phase}-seed{seed}.json"
            content = (directory / name).read_bytes()
            relative = f"{DOC}/raw/native-student-{commit[:8]}/{name}"
            target = ROOT / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            if target.exists() and target.read_bytes() != content:
                raise FileExistsError("immutable raw evidence differs")
            target.write_bytes(content)
            raw[f"{phase}-{seed}"] = {"artifact_path": relative, "sha256": hashlib.sha256(content).hexdigest()}
    checks = {"actual_teacher_target_rows": [training["variants"]["distillation_training"]["real_teacher_target_rows"] for training, _ in pairs],
              "actual_optimizer_updates": [training["variants"]["distillation_training"]["optimizer_updates"] for training, _ in pairs],
              "teacher_layout_updates": [2] * 3, "compact_layout_updates": [6] * 3,
              "train_and_control_total_wall_seconds": walls, "actual_all_defining_losses_and_gradients_finite": True,
              "new_selected_student_strictly_loaded": True, "matched_goal6_initial_states_and_noop": True,
              "adapter_only_no_published_student_injection": True, "diagnostic_only": True, "promotion_eligible": False}
    limitations = ["One task, eight demos and eight optimizer steps replace original multi-task 5000-step training.",
                   "Released frozen latent adapters/BERT cache reused; not retrained.",
                   "Bounded matched libero_goal:6 trials, not original 400-episode benchmark or a formal comparison.",
                   "World output executed but not scored against true future; no teacher closed-loop comparison."]
    artifact, receipt_path = f"{DOC}/native-student-a100-seeds42-44.json", "docs/gpu-validations/oct13-smolwam-a100.json"
    budget = {"training_episodes": 8, "training_steps": 8, "layout_steps": [2, 6], "max_training_rows": 32,
              "tasks": ["libero_goal:6"], "trials": 2, "action_budget": 300, "total_wall_limit_seconds": 1800}
    payload = {"schema_version": 2, "adapter_key": "smolwam", "manifest_ref": "reproduction:smolwam", "seeds": list(SEEDS), "diagnostic_only": True,
               "promotion_eligible": False, "measured_locally": True, "aggregate_metrics": metrics,
               "seed_results": [{"training": training, "candidate_control": evaluation} for training, evaluation in pairs],
               "raw_artifacts": raw, "execution_checks": checks, "dataset": pairs[0][0]["dataset"],
               "evaluation_protocol": {"tier": "l2_public_dataset", "seeds": list(SEEDS), "formal_comparison": False, "budget": budget,
                                       "claim_policy": "scaled single-task teacher distillation and closed-loop diagnostic; no stable improvement claim"},
               "provenance": {"code_commit": commit, "artifact_path": artifact,
                              "dataset_fingerprint": hashlib.sha256(json.dumps(pairs[0][0]["dataset"], sort_keys=True).encode()).hexdigest()},
               "limitations": limitations}
    commands = [["python", "scripts/run_oct13_robotics.py", "--paper", "smolwam", "--phase", phase,
                 "--config", f"data/smolwam-{label}.json", "--seed", str(seed), "--output", f"runs/smolwam-{label}-seed{seed}.json"]
                for seed in SEEDS for phase, label in (("train", "train"), ("eval", "candidate"))]
    receipt = {"schema_version": 1, "adapter_key": "smolwam", "validated_at": datetime.now(timezone.utc).isoformat(),
               "accelerator": {"vendor": "NVIDIA", "model": "NVIDIA A100-SXM4-80GB"}, "command": commands[0], "commands": commands,
               "seeds": list(SEEDS), "dataset": {"demonstrations": pairs[0][0]["dataset"], "control": pairs[0][1]["dataset"]},
               "checkpoint": {"teacher": pairs[0][0]["teacher"], "frozen_adapter_text": pairs[0][0]["pretrained_adapter_text"],
                              "vae": pairs[0][1]["vae"], "new_students": {str(seed): evaluation["trained_candidate"]
                                  for seed, (_, evaluation) in zip(SEEDS, pairs, strict=True)}},
               "result": "passed", "metrics": metrics, "config": budget, "execution_checks": checks, "raw_artifacts": raw,
               "executed_source_sha256": hashes, "executed_source_archive_sha256": hashlib.sha256(source_archive.read_bytes()).hexdigest(),
               "provenance": {"commit": commit, "artifact_path": receipt_path, "metrics_artifact": artifact, "checkpoint_committed": False},
               "limitations": limitations}
    if errors := validate_gpu_receipt(receipt):
        raise ValueError(errors)
    for relative, document in ((artifact, payload), (receipt_path, receipt)):
        target = ROOT / relative
        if target.exists():
            raise FileExistsError("immutable curated evidence exists")
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(json.dumps(document, ensure_ascii=False, indent=2, allow_nan=False) + "\n")
    return checks


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--executed-commit", required=True)
    parser.add_argument("--source-archive", type=Path, required=True)
    args = parser.parse_args()
    print(json.dumps(curate(args.input, args.executed_commit, args.source_archive), indent=2))
