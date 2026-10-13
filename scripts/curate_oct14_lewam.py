#!/usr/bin/env python3
"""Curate actual native training -> same-seed new-candidate control evidence."""
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
ARMS = ("reactive", "best_of_k", "grad")
DOC = "docs/reproductions/2610.12818-lewam/metrics"


def verify_pair(training: dict, evaluation: dict, seed: int, implementation: dict,
                train_request: dict, eval_request: dict) -> None:
    for request, phase in ((train_request, "train"), (eval_request, "eval")):
        if request.get("seed") != seed or request.get("phase") != phase or request.get("device") != "cuda":
            raise ValueError("actual worker request identity required")
    train_budget = {"train_epochs": 1, "train_steps_per_epoch": 4, "train_batch_size": 8}
    eval_budget = {"episodes": 2, "goal_offset": 50, "action_budget": 100, "proposals": 4, "gradient_steps": 5}
    if (any(train_request.get(name) != value for name, value in train_budget.items())
            or any(eval_request.get(name) != value for name, value in eval_budget.items())
            or set(eval_request.get("variants", [])) != set(ARMS)
            or not eval_request.get("trained_model_dir")
            or Path(eval_request["trained_model_dir"]) != Path(train_request["result_path"]).parent / "native-training"):
        raise ValueError("fixed actual budget and training-output candidate path required")
    for run in (training, evaluation):
        if (run.get("paper") != "lewam" or run.get("seed") != seed
                or run.get("source_revision") != PINS["lewam"] or run.get("device") != "cuda"
                or run.get("executed") is not True or run.get("diagnostic_only") is not True
                or run.get("promotion_eligible") is not False):
            raise ValueError("actual matching CUDA diagnostic identity required")
    candidate = training.get("trained_candidate", {})
    metric = training.get("variants", {}).get("joint_training", {})
    validate_training_evidence("lewam", metric, candidate.get("training_evidence", {}))
    if (candidate.get("kind") != "local-trained-candidate" or candidate.get("seed") != seed
            or candidate.get("paper") != "lewam" or candidate.get("source_revision") != PINS["lewam"]
            or set(candidate.get("files", {})) != {"lewam_best.pt", "lewam_config.json"}
            or not all(isinstance(value, str) and len(value) == 64 and set(value) <= set("0123456789abcdef")
                       for value in candidate["files"].values())
            or candidate.get("selection") != "validation only" or candidate.get("metrics") != metric
            or candidate.get("implementation_sha256") != implementation
            or evaluation.get("checkpoint") != candidate
            or training.get("dataset") != evaluation.get("dataset")
            or candidate.get("dataset") != evaluation.get("dataset")):
        raise ValueError("real selected candidate, local source and control data must match training")
    if (training.get("protocol", {}).get("epochs") != 1
            or training["protocol"].get("steps_per_epoch") != 4
            or training["protocol"].get("batch_size") != 8
            or metric.get("optimizer_updates") != 4
            or training["protocol"].get("action_flow_latent_prediction_sigreg_executed") is not True):
        raise ValueError("fixed native joint-training budget differs")
    protocol = evaluation.get("protocol", {})
    if (protocol.get("native_joint_training_reexecuted") is not True
            or protocol.get("trained_candidate_closed_loop_evaluated") is not True
            or protocol.get("public_checkpoint_executed") is not False
            or protocol.get("non_holdout") is not True or protocol.get("goal_from_training_episodes") is not True
            or protocol.get("proposals") != 4 or protocol.get("gradient_steps") != 5
            or protocol.get("episodes") != 2 or set(evaluation.get("variants", {})) != set(ARMS)):
        raise ValueError("fixed three-arm actual new-candidate control required")
    starts = evaluation.get("sampled_starts", {})
    if (len(starts.get("episodes", [])) != 2 or len(starts.get("starts", [])) != 2
            or starts.get("goal_offset") != 50):
        raise ValueError("actual matched two-episode starts and goals required")
    for arm in ARMS:
        row = evaluation["variants"][arm]
        outcomes = row.get("metrics", {}).get("episode_successes", [])
        rate = row.get("metrics", {}).get("success_rate")
        if (len(outcomes) != 2 or not all(type(value) is bool for value in outcomes)
                or type(rate) not in {int, float} or not math.isfinite(rate)
                or rate != 100 * sum(outcomes) / len(outcomes)
                or type(row.get("wall_seconds")) not in {int, float}
                or not math.isfinite(row["wall_seconds"]) or row["wall_seconds"] <= 0):
            raise ValueError("finite measured closed-loop outcomes required")


def curate(directory: Path, commit: str, source_archive: Path) -> dict:
    paths = [f"src/auto_research/reproductions/lewam/{name}.py"
             for name in ("external", "algorithm", "training", "worker")]
    source_hashes = {}
    with tarfile.open(source_archive) as archive:
        for name in paths:
            packed = archive.extractfile(name).read()
            if packed != subprocess.check_output(["git", "show", f"{commit}:{name}"], cwd=ROOT):
                raise ValueError("source archive differs from actual executed commit")
            source_hashes[name] = hashlib.sha256(packed).hexdigest()
    implementation = {name.removeprefix("src/auto_research/reproductions/"): digest
                      for name, digest in source_hashes.items()}
    pairs, walls = [], []
    for seed in SEEDS:
        training = json.loads((directory / f"lewam-train-seed{seed}.json").read_text())
        evaluation = json.loads((directory / f"lewam-candidate-seed{seed}.json").read_text())
        train_request = json.loads((directory / f"lewam-train-request-seed{seed}.json").read_text())
        eval_request = json.loads((directory / f"lewam-candidate-request-seed{seed}.json").read_text())
        verify_pair(training, evaluation, seed, implementation, train_request, eval_request)
        completions = []
        for line in (directory / f"lewam-seed{seed}-launch.log").read_text().splitlines():
            if line.startswith("{"):
                row = json.loads(line)
                if row.get("completed") is True:
                    completions.append(row.get("wall_seconds"))
        if (len(completions) != 1 or type(completions[0]) not in {int, float}
                or not math.isfinite(completions[0]) or not 0 < completions[0] <= 1800):
            raise ValueError("actual successful train-control total wall must stay within 1800 seconds")
        walls.append(completions[0])
        pairs.append((training, evaluation))
    metrics = {f"{arm}.success_rate": {"mean": statistics.mean(values), "std": statistics.stdev(values), "n": 3}
               for arm in ARMS for values in [[evaluation["variants"][arm]["metrics"]["success_rate"]
                                               for _, evaluation in pairs]]}
    raw = {}
    for seed in SEEDS:
        for phase in ("train", "candidate"):
            name = f"lewam-{phase}-seed{seed}.json"
            content = (directory / name).read_bytes()
            relative = f"{DOC}/raw/native-candidate-{commit[:8]}/{name}"
            target = ROOT / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            if target.exists() and target.read_bytes() != content:
                raise FileExistsError("immutable raw evidence differs")
            target.write_bytes(content)
            raw[f"{phase}-{seed}"] = {"artifact_path": relative, "sha256": hashlib.sha256(content).hexdigest()}
    checks = {"native_training_seeds": 3, "new_candidate_control_seeds": 3,
              "actual_optimizer_updates": [training["variants"]["joint_training"]["optimizer_updates"] for training, _ in pairs],
              "actual_nonzero_gradient_updates": [training["variants"]["joint_training"]["nonzero_gradient_updates"] for training, _ in pairs],
              "parameter_sample_delta_l2": [training["variants"]["joint_training"]["parameter_sample_delta_l2"] for training, _ in pairs],
              "defining_action_latent_sigreg_losses_finite": True,
              "new_selected_checkpoint_loaded_strictly": True,
              "matched_initial_states_and_goals_across_three_controls": True,
              "closed_loop_episodes_per_seed_per_control": 2,
              "train_and_control_total_wall_seconds": walls,
              "public_checkpoint_used_as_new_candidate": False,
              "diagnostic_only": True, "promotion_eligible": False}
    limitations = ["Bounded native 1-epoch, 4-batch training, not original 50-epoch training.",
                   "Goals sampled from training trajectories; no held-out test or formal capability comparison.",
                   "Two episodes per seed/control, 100-step budget, 4 proposals and 5 gradient steps.",
                   "Dataset Robosuite metadata 1.4.1 vs author-required runtime 1.5.1 mismatch warning retained."]
    artifact = f"{DOC}/native-candidate-a100-seeds42-44.json"
    receipt_path = "docs/gpu-validations/oct13-lewam-a100.json"
    payload = {"schema_version": 2, "adapter_key": "lewam", "manifest_ref": "reproduction:lewam", "seeds": list(SEEDS),
               "diagnostic_only": True, "promotion_eligible": False, "measured_locally": True,
               "aggregate_metrics": metrics, "seed_results": [{"training": training, "candidate_control": evaluation}
                                                               for training, evaluation in pairs],
               "raw_artifacts": raw, "execution_checks": checks, "dataset": pairs[0][0]["dataset"],
               "evaluation_protocol": {"tier": "l2_public_dataset", "seeds": list(SEEDS), "formal_comparison": False,
                                       "claim_policy": "scaled train-derived-goal mechanism diagnostic; no stable improvement claim",
                                       "budget": {"epochs": 1, "batches": 4, "batch_size": 8,
                                                  "episodes": 2, "action_budget": 100, "proposals": 4, "gradient_steps": 5}},
               "provenance": {"code_commit": commit, "artifact_path": artifact,
                              "dataset_fingerprint": hashlib.sha256(json.dumps(pairs[0][0]["dataset"], sort_keys=True).encode()).hexdigest()},
               "limitations": limitations}
    receipt = {"schema_version": 1, "adapter_key": "lewam", "validated_at": datetime.now(timezone.utc).isoformat(),
               "accelerator": {"vendor": "NVIDIA", "model": "NVIDIA A100-SXM4-80GB"},
               "command": ["python", "scripts/run_oct13_robotics.py", "--paper", "lewam", "--phase", "train",
                           "--config", "data/lewam-train.json", "--seed", "42", "--output", "runs/lewam-train-seed42.json"],
               "commands": [["python", "scripts/run_oct13_robotics.py", "--paper", "lewam", "--phase", phase,
                             "--config", f"data/lewam-{label}.json", "--seed", str(seed), "--output", f"runs/lewam-{label}-seed{seed}.json"]
                            for seed in SEEDS for phase, label in (("train", "train"), ("eval", "candidate"))],
               "seeds": list(SEEDS), "dataset": pairs[0][0]["dataset"],
               "checkpoint": {str(seed): evaluation["checkpoint"] for seed, (_, evaluation) in zip(SEEDS, pairs, strict=True)},
               "result": "passed", "metrics": metrics, "config": payload["evaluation_protocol"]["budget"],
               "execution_checks": checks, "raw_artifacts": raw, "executed_source_sha256": source_hashes,
               "executed_source_archive_sha256": hashlib.sha256(source_archive.read_bytes()).hexdigest(),
               "provenance": {"commit": commit, "artifact_path": receipt_path, "metrics_artifact": artifact,
                              "checkpoint_committed": False}, "limitations": limitations}
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
