"""Read-only curation of the frozen six-arm CV-OPD A100 diagnostic.

Prints JSON; never edits or overwrites raw results, logs, or checkpoints.
"""
from __future__ import annotations

import argparse
from hashlib import sha256
import json
import math
from pathlib import Path
from statistics import mean, stdev
import tarfile

COMMIT = "4496283ac8e37c070b8f71b20af6138526cbba15"
SEEDS = (42, 43, 44)
SOURCE_ARCHIVE_SHA256 = "f613a1a1355350d3008c36ca41186a799c09d66be82828f52e2734ac47a21cd5"
SOURCE_FILES = (
    "scripts/run_cv_opd.py", "src/auto_research/multimodal/cv_opd.py",
    "src/auto_research/post_training/local_lora.py",
    "src/auto_research/foundation_models/oct13_runtime.py",
    "src/auto_research/oct12_public_sources.py",
)
CHECKPOINT_ID = "HuggingFaceTB/SmolVLM-256M-Instruct"
CHECKPOINT_REVISION = "7e3e67edbbed1bf9888184d9df282b700a323964"
MODEL_SHA256 = "74dea5904032e5ae99a2e0eef5179e6ac0f1dedc3ab0c7c2a5d4d387c843203e"
DATASET_REVISION = "113a836d90195ee1f884e704da6304dfaaecff1f023f49b6ca93c4aaae470268"
RECORDS_SHA256 = "f23de926af9f803f1c5568eae1bb150b2e55b919fce82a66167e961e764acb00"


def curate(raw_dir: Path, source_archive: Path) -> dict:
    assert sha256(source_archive.read_bytes()).hexdigest() == SOURCE_ARCHIVE_SHA256
    with tarfile.open(source_archive) as archive:
        source_hashes = {}
        for name in SOURCE_FILES:
            member = archive.extractfile(name)
            assert member is not None
            source_hashes[name] = sha256(member.read()).hexdigest()
    rows, protocols, identities, commands = [], [], [], []
    expected_files = set()
    for arm, weight in (("main", 0.1), ("without-cdl", 0.0)):
        for seed in SEEDS:
            stem = f"cv-opd-{arm}-seed{seed}"
            names = [stem + suffix for suffix in (".json", ".status.json", ".stdout.log", ".stderr.log")]
            expected_files.update(names)
            report = json.loads((raw_dir / names[0]).read_text())
            status = json.loads((raw_dir / names[1]).read_text())
            command = status["command"]

            def flag(name):
                return command[command.index(name) + 1]

            assert status["returncode"] == 0 and status["commit"] == COMMIT
            assert status["output_exists"] and status["failure"] is None
            assert status["accelerator"] == "NVIDIA A100-SXM4-80GB"
            assert command[1] == "scripts/run_cv_opd.py" and flag("--device") == "cuda"
            assert int(flag("--seed")) == seed == report["seed"]
            assert int(flag("--steps")) == 16 and int(flag("--batch-size")) == 1
            assert int(flag("--rollouts")) == 8 and int(flag("--max-new-tokens")) == 16
            assert float(flag("--contrastive-weight")) == weight
            assert flag("--checkpoint-id") == report["checkpoint"]["id"] == CHECKPOINT_ID
            assert flag("--checkpoint-revision") == report["checkpoint"]["revision"] == CHECKPOINT_REVISION
            assert report["checkpoint"]["file_sha256"]["model.safetensors"] == MODEL_SHA256
            assert flag("--dataset-id") == report["dataset"]["id"] == "COCO2017/train2017"
            assert flag("--dataset-revision") == report["dataset"]["revision"] == DATASET_REVISION
            assert report["dataset"]["records_sha256"] == RECORDS_SHA256
            assert report["dataset"]["input_file_sha256"]["records.jsonl"] == RECORDS_SHA256
            assert report["dataset"]["source_split"] == "train2017"
            assert report["dataset"]["local_holdout_is_not_official_test"]
            assert report["successful_parameter_update"]
            assert report["optimizer_updates"] > 0 and report["parameter_delta_l2"] > 0
            assert math.isfinite(report["parameter_delta_l2"])
            assert report["diagnostic_only"] and not report["promotion_eligible"]
            assert report["test_isolated_from_selection"] and report["dataset"]["all_input_hashes_verified"]
            assert len(report["history"]) == len(report["rollout_attempts"]) == 16
            assert all(attempt["rollouts"] == 8 for attempt in report["rollout_attempts"])
            assert len({attempt["id"] for attempt in report["rollout_attempts"]}) == 16
            assert [item["step"] for item in report["history"]] == list(range(16))
            assert [item["step"] for item in report["rollout_attempts"]] == list(range(16))
            assert report["optimizer_updates"] == sum(bool(item["updated"]) for item in report["history"])
            assert report["total_training_rollout_tokens"] == sum(item["generated_tokens"] for item in report["rollout_attempts"])
            assert all(report[name]["examples"] == 8 for name in ("baseline_validation", "final_validation", "final_test"))
            assert all(0 <= report[name]["accuracy"] <= 1 for name in ("baseline_validation", "final_validation", "final_test"))
            assert all(0 <= crop["iou"] <= .1 for item in report["history"] for crop in item.get("crops", []))
            identities.append((report["checkpoint"], report["dataset"]))
            protocols.append(report["task_protocol"])
            assert all(item == identities[0] for item in identities)
            assert all(item == protocols[0] for item in protocols)
            assert report["task_protocol"]["training_class_counts"] == {
                name: 2 for name in ("person", "cat", "dog", "car", "bus", "bird", "horse", "bicycle")}
            assert not report["task_protocol"]["gold_in_policy_prompt"]
            assert not report["task_protocol"]["bbox_in_full_image_student_prompt"]
            assert report["task_protocol"]["positive_negative_teacher_same_question"]
            sanitized = list(command)
            sanitized[0] = "python"
            for name, role in (("--checkpoint", "PUBLIC_CHECKPOINT"),
                               ("--records", "PUBLIC_COCO_DIAGNOSTIC/records.jsonl"),
                               ("--output", "RAW_RESULT")):
                sanitized[sanitized.index(name) + 1] = role
            commands.append({"arm": arm, "seed": seed, "command": sanitized})
            history, attempts = report["history"], report["rollout_attempts"]
            rows.append({
                "arm": arm, "seed": seed, "contrastive_weight": weight,
                "baseline_validation_accuracy": report["baseline_validation"]["accuracy"],
                "validation_accuracy": report["final_validation"]["accuracy"],
                "test_accuracy": report["final_test"]["accuracy"],
                "optimizer_updates": report["optimizer_updates"],
                "parameter_delta_l2": report["parameter_delta_l2"],
                "training_rollout_tokens": report["total_training_rollout_tokens"],
                "sampled_training_rollouts": sum(item["rollouts"] for item in attempts),
                "correct_training_rollouts": sum(item["correct_rollouts"] for item in attempts),
                "retained_samples": sum(bool(item["retained"]) for item in attempts),
                "gated_tokens": sum(item.get("gated_tokens", 0) for item in history),
                "valid_tokens_in_updated_trajectories": sum(item.get("valid_tokens", 0) for item in history),
                "crop_failures": len(report["crop_failures"]),
                "unweighted_cdl_nonzero_steps": sum(item.get("cdl", 0) > 0 for item in history),
                "maximum_crop_iou": max(crop["iou"] for item in history for crop in item.get("crops", [])),
                "elapsed_seconds": status["elapsed_seconds"],
                "started_at": status["started_at"], "finished_at": status["finished_at"],
            })
    assert set(path.name for path in raw_dir.glob("cv-opd-*")) == expected_files
    pairs = []
    for seed in SEEDS:
        main = next(row for row in rows if row["seed"] == seed and row["arm"] == "main")
        control = next(row for row in rows if row["seed"] == seed and row["arm"] == "without-cdl")
        assert main["baseline_validation_accuracy"] == control["baseline_validation_accuracy"]
        pairs.append({"seed": seed, **{
            name + "_main_minus_without_cdl": main[name] - control[name]
            for name in ("test_accuracy", "validation_accuracy", "optimizer_updates", "training_rollout_tokens")}})

    def aggregate(values):
        return {"mean": mean(values), "sample_std": stdev(values)}

    summaries = {arm: {name: aggregate([row[name] for row in rows if row["arm"] == arm])
                       for name in ("baseline_validation_accuracy", "validation_accuracy", "test_accuracy",
                                    "optimizer_updates", "parameter_delta_l2", "training_rollout_tokens",
                                    "correct_training_rollouts", "gated_tokens", "elapsed_seconds")}
                 for arm in ("main", "without-cdl")}
    summaries["paired_differences"] = {
        name: aggregate([pair[name] for pair in pairs]) for name in pairs[0] if name != "seed"}
    return {"code_commit": COMMIT, "seeds": list(SEEDS), "per_seed": rows,
            "paired_differences": pairs, "aggregate": summaries,
            "checkpoint": identities[0][0], "dataset": identities[0][1], "task_protocol": protocols[0],
            "sanitized_commands": commands,
            "command_redaction": "Only executable, checkpoint, records, and output machine paths replaced by public roles.",
            "source_archive_sha256": SOURCE_ARCHIVE_SHA256,
            "actual_source_files_sha256": source_hashes,
            "raw_files_sha256": {name: sha256((raw_dir / name).read_bytes()).hexdigest()
                                 for name in sorted(expected_files)}}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--raw-dir", type=Path, required=True)
    parser.add_argument("--source-archive", type=Path, required=True)
    args = parser.parse_args()
    print(json.dumps(curate(args.raw_dir, args.source_archive), ensure_ascii=False, indent=2))
