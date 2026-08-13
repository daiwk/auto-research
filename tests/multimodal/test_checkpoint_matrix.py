import json
from pathlib import Path
import subprocess

import pytest

from auto_research.multimodal.lmms_eval import (
    LMMSEvalConfig,
    build_lmms_eval_command,
    normalize_lmms_eval_results,
    run_lmms_eval,
)
from auto_research.multimodal.matrix import load_matrix, run_checkpoint_matrix


def _inputs(tmp_path: Path):
    annotations = tmp_path / "pope.jsonl"
    annotations.write_text(
        json.dumps({"question_id": 1, "image": "1.jpg", "text": "Visible?", "label": "yes"}) + "\n",
        encoding="utf-8",
    )
    (tmp_path / "images").mkdir()
    config = tmp_path / "matrix.json"
    config.write_text(json.dumps({"cells": [{
        "name": "tiny", "family": "generative", "benchmark": "pope",
        "model_id": "example/model", "annotations": "pope.jsonl",
        "image_root": "images", "batch_sizes": [4, 1],
    }]}), encoding="utf-8")
    return config


def test_matrix_retries_oom_and_writes_comparable_report(tmp_path):
    config = _inputs(tmp_path)
    calls = []

    def runner(cfg):
        calls.append(cfg.batch_size)
        if cfg.batch_size == 4:
            raise RuntimeError("CUDA out of memory")
        cfg.output.write_text(json.dumps({"id": "1", "prediction": "yes"}) + "\n")
        return {
            "resolved_revision": "abc", "inference_seconds": 0.2,
            "seconds_per_new_prediction": 0.2, "selected_examples": 1,
            "peak_gpu_memory_mb": 123.0,
        }

    output = tmp_path / "out"
    run_checkpoint_matrix(config, output, generative_runner=runner)
    payload = json.loads((output / "matrix.json").read_text())
    assert calls == [4, 1]
    assert payload["cells"]["tiny"]["status"] == "completed"
    assert payload["cells"]["tiny"]["metrics"]["accuracy"] == 1.0
    assert payload["cells"]["tiny"]["requested_revision"] == "main"
    assert payload["cells"]["tiny"]["protocol"]["maximum_examples"] is None
    report = (output / "report.md").read_text()
    assert "只在相同 family" in report
    assert "0.2000" in report
    assert "123.0" in report

    run_checkpoint_matrix(config, output, generative_runner=runner)
    assert calls == [4, 1]


def test_matrix_rejects_duplicate_names(tmp_path):
    config = _inputs(tmp_path)
    payload = json.loads(config.read_text())
    payload["cells"].append(payload["cells"][0])
    config.write_text(json.dumps(payload))
    try:
        load_matrix(config)
    except ValueError as exc:
        assert "unique" in str(exc)
    else:
        raise AssertionError("duplicate matrix cell was accepted")


def test_matrix_rejects_unfair_comparison_group(tmp_path):
    config = _inputs(tmp_path)
    payload = json.loads(config.read_text())
    other = dict(payload["cells"][0])
    other.update({"name": "unfair", "maximum_examples": 50})
    payload["cells"].append(other)
    config.write_text(json.dumps(payload))
    with pytest.raises(ValueError, match="not budget-matched.*maximum_examples"):
        load_matrix(config)


def test_matrix_resume_rejects_config_or_seed_drift(tmp_path):
    config = _inputs(tmp_path)

    def runner(cfg):
        cfg.output.write_text(json.dumps({"id": "1", "prediction": "yes"}) + "\n")
        return {"resolved_revision": "abc", "selected_examples": 1}

    output = tmp_path / "out"
    run_checkpoint_matrix(config, output, generative_runner=runner)
    with pytest.raises(ValueError, match="config/seed changed"):
        run_checkpoint_matrix(config, output, seed=43, generative_runner=runner)


def test_mr8_public_matrix_is_full_split_and_budget_matched():
    config = Path(__file__).parents[2] / "configs/multimodal-checkpoint-matrix.mr8.json"
    cells = load_matrix(config)

    assert len(cells) == 8
    assert {
        (cell.family, cell.benchmark, cell.maximum_examples)
        for cell in cells
    } == {
        ("generative", "scienceqa", 4241),
        ("generative", "pope", 3000),
        ("retrieval", "coco-retrieval", 5000),
    }
    assert all(len(cell.revision) == 40 for cell in cells)


def test_lmms_eval_bridge_is_shell_free_and_dry_runnable(tmp_path):
    config = LMMSEvalConfig(
        model="qwen2_5_vl", model_args="pretrained=Qwen/Qwen2.5-VL-3B-Instruct",
        tasks=("mme", "mmmu_val"), output_dir=tmp_path, limit=8,
        public_model_id="Qwen/Qwen2.5-VL-3B-Instruct",
        model_revision="1" * 40,
        upstream_revision="3" * 40,
    )
    command = build_lmms_eval_command(config)
    assert command[:3] == [command[0], "-m", "lmms_eval"]
    assert "mme,mmmu_val" in command
    assert run_lmms_eval(config, dry_run=True)["status"] == "dry-run"

    seen = []
    def fake_runner(argv, **kwargs):
        seen.append((argv, kwargs))
        (tmp_path / "20260813_results.json").write_text(json.dumps({
            "results": {"mme": {"mme_perception_score,none": 120.0}},
            "n-samples": {"mme": {"effective": 8, "original": 2374}},
            "higher_is_better": {"mme": {"mme_perception_score": True}},
            "versions": {"mme": 0.0},
            "efficiency": {"overall": {"total_output_tokens": 20}},
        }), encoding="utf-8")
        return subprocess.CompletedProcess(argv, 0, stdout="ok", stderr="")
    result = run_lmms_eval(config, runner=fake_runner)
    assert result["status"] == "completed"
    assert result["tasks"][0]["metrics"]["mme_perception_score"] == 120.0
    assert result["tasks"][0]["samples"] == {"effective": 8, "original": 2374}
    assert result["model"]["revision"] == "1" * 40
    assert result["upstream"]["revision"] == "3" * 40
    assert result["efficiency"]["overall"]["total_output_tokens"] == 20
    assert (tmp_path / "summary.json").exists()
    assert seen[0][1]["check"] is True


def test_lmms_eval_normalization_does_not_leak_runtime_paths(tmp_path):
    checkpoint = tmp_path / "private" / "checkpoint"
    config = LMMSEvalConfig(
        model="qwen2_5_vl",
        model_args=f"pretrained={checkpoint},device_map=auto",
        tasks=("mmmu_val",),
        output_dir=tmp_path,
        public_model_id="Qwen/Qwen2.5-VL-3B-Instruct",
        model_revision="2" * 40,
    )
    summary = normalize_lmms_eval_results(
        {
            "results": {"mmmu_val": {"mmmu_acc,none": 0.4, "alias": "x"}},
            "n-samples": {"mmmu_val": {"effective": 900, "original": 900}},
        },
        config,
        source_file=tmp_path / "model" / "results.json",
    )
    encoded = json.dumps(summary)
    assert str(checkpoint) not in encoded
    assert summary["upstream"]["source_file"] == "results.json"
    assert summary["tasks"][0]["metrics"] == {"mmmu_acc": 0.4, "alias": "x"}


def test_lmms_eval_requires_immutable_public_revisions(tmp_path):
    with pytest.raises(ValueError, match="40-character revision"):
        build_lmms_eval_command(LMMSEvalConfig(
            model="huggingface",
            model_args="pretrained=example/model",
            tasks=("scienceqa_img",),
            output_dir=tmp_path,
            public_model_id="example/model",
            model_revision="main",
        ))
