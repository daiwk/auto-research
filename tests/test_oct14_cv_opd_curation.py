"""Portable curation contracts: synthetic evidence, never the ignored runs/ tree."""
from hashlib import sha256
import importlib.util
import io
import json
from pathlib import Path
import tarfile

import pytest


SPEC = importlib.util.spec_from_file_location(
    "cv_curation", Path(__file__).resolve().parents[1] / "scripts/curate_oct14_cv_opd.py")
curation = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(curation)


@pytest.fixture
def evidence(tmp_path, monkeypatch):
    archive = tmp_path / "source.tar"
    with tarfile.open(archive, "w") as bundle:
        for name in curation.SOURCE_FILES:
            data = b"synthetic source fixture\n"
            info = tarfile.TarInfo(name)
            info.size = len(data)
            bundle.addfile(info, io.BytesIO(data))
    monkeypatch.setattr(curation, "SOURCE_ARCHIVE_SHA256", sha256(archive.read_bytes()).hexdigest())
    raw = tmp_path / "raw"
    raw.mkdir()
    for arm, weight in (("main", .1), ("without-cdl", 0.)):
        for seed in curation.SEEDS:
            stem = f"cv-opd-{arm}-seed{seed}"
            command = ["python", "scripts/run_cv_opd.py"]
            for flag, value in {
                "checkpoint": "fixture-model", "checkpoint-id": curation.CHECKPOINT_ID,
                "checkpoint-revision": curation.CHECKPOINT_REVISION,
                "records": "fixture-records", "dataset-id": "COCO2017/train2017",
                "dataset-revision": curation.DATASET_REVISION, "device": "cuda",
                "steps": 16, "batch-size": 1, "rollouts": 8, "max-new-tokens": 16,
                "contrastive-weight": weight, "seed": seed, "output": "fixture-result",
            }.items():
                command.extend(["--" + flag, str(value)])
            report = {
                "seed": seed, "successful_parameter_update": True, "optimizer_updates": 16,
                "parameter_delta_l2": .01, "diagnostic_only": True, "promotion_eligible": False,
                "test_isolated_from_selection": True, "crop_failures": [],
                "total_training_rollout_tokens": 128,
                "history": [{"step": step, "updated": True, "cdl": .1,
                             "crops": [{"iou": .05}]} for step in range(16)],
                "rollout_attempts": [{"step": step, "id": str(step), "rollouts": 8,
                                      "generated_tokens": 8, "correct_rollouts": 1,
                                      "retained": True} for step in range(16)],
                "checkpoint": {"id": curation.CHECKPOINT_ID, "revision": curation.CHECKPOINT_REVISION,
                               "file_sha256": {"model.safetensors": curation.MODEL_SHA256}},
                "dataset": {"id": "COCO2017/train2017", "revision": curation.DATASET_REVISION,
                            "records_sha256": curation.RECORDS_SHA256,
                            "input_file_sha256": {"records.jsonl": curation.RECORDS_SHA256},
                            "source_split": "train2017", "all_input_hashes_verified": True,
                            "local_holdout_is_not_official_test": True},
                "task_protocol": {"training_class_counts": {name: 2 for name in
                                  ("person", "cat", "dog", "car", "bus", "bird", "horse", "bicycle")},
                                  "gold_in_policy_prompt": False, "bbox_in_full_image_student_prompt": False,
                                  "positive_negative_teacher_same_question": True},
            }
            for name in ("baseline_validation", "final_validation", "final_test"):
                report[name] = {"accuracy": .125, "examples": 8}
            status = {"command": command, "commit": curation.COMMIT, "returncode": 0,
                      "accelerator": "NVIDIA A100-SXM4-80GB", "output_exists": True,
                      "failure": None, "elapsed_seconds": 1., "started_at": "2026-10-13T00:00:00Z",
                      "finished_at": "2026-10-13T00:00:01Z"}
            (raw / (stem + ".json")).write_text(json.dumps(report))
            (raw / (stem + ".status.json")).write_text(json.dumps(status))
            (raw / (stem + ".stdout.log")).write_text("fixture stdout\n")
            (raw / (stem + ".stderr.log")).write_text("")
    return raw, archive


def test_curates_six_arms_and_hashes_without_local_experiment_dependency(evidence):
    result = curation.curate(*evidence)
    assert len(result["per_seed"]) == 6
    assert len(result["raw_files_sha256"]) == 24
    assert set(result["actual_source_files_sha256"]) == set(curation.SOURCE_FILES)
    assert result["aggregate"]["paired_differences"]["test_accuracy_main_minus_without_cdl"]["mean"] == 0
    assert all(row["sampled_training_rollouts"] == 128 for row in result["per_seed"])


@pytest.mark.parametrize("mutation", ["steps", "weight", "zero-update", "source-commit", "checkpoint", "dataset", "model-hash", "crop-iou", "nan-update"])
def test_rejects_wrong_protocol_or_identity(evidence, mutation):
    raw, archive = evidence
    path = raw / "cv-opd-main-seed42.status.json"
    status = json.loads(path.read_text())
    report_path = raw / "cv-opd-main-seed42.json"
    report = json.loads(report_path.read_text())
    if mutation in ("steps", "weight"):
        flag = "--steps" if mutation == "steps" else "--contrastive-weight"
        status["command"][status["command"].index(flag) + 1] = "17" if mutation == "steps" else "0.2"
    elif mutation == "zero-update":
        report["optimizer_updates"] = 0
    elif mutation == "source-commit":
        status["commit"] = "0" * 40
    elif mutation == "checkpoint":
        report["checkpoint"]["revision"] = "0" * 40
    elif mutation == "model-hash":
        report["checkpoint"]["file_sha256"]["model.safetensors"] = "0" * 64
    elif mutation == "crop-iou":
        report["history"][0]["crops"][0]["iou"] = .2
    elif mutation == "nan-update":
        report["parameter_delta_l2"] = float("nan")
    else:
        report["dataset"]["records_sha256"] = "0" * 64
    path.write_text(json.dumps(status))
    report_path.write_text(json.dumps(report))
    with pytest.raises(AssertionError):
        curation.curate(raw, archive)


def test_rejects_different_source_archive(evidence):
    raw, archive = evidence
    archive.write_bytes(archive.read_bytes() + b"source changed")
    with pytest.raises(AssertionError):
        curation.curate(raw, archive)
