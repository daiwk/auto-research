import json
from pathlib import Path
import subprocess

from auto_research.multimodal.lmms_eval import (
    LMMSEvalConfig, build_lmms_eval_command, run_lmms_eval,
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
        return {"resolved_revision": "abc", "inference_seconds": 0.2}

    output = tmp_path / "out"
    run_checkpoint_matrix(config, output, generative_runner=runner)
    payload = json.loads((output / "matrix.json").read_text())
    assert calls == [4, 1]
    assert payload["cells"]["tiny"]["status"] == "completed"
    assert payload["cells"]["tiny"]["metrics"]["accuracy"] == 1.0
    assert "只在相同 family" in (output / "report.md").read_text()

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


def test_lmms_eval_bridge_is_shell_free_and_dry_runnable(tmp_path):
    config = LMMSEvalConfig(
        model="qwen2_5_vl", model_args="pretrained=Qwen/Qwen2.5-VL-3B-Instruct",
        tasks=("mme", "mmmu_val"), output_dir=tmp_path, limit=8,
    )
    command = build_lmms_eval_command(config)
    assert command[:3] == [command[0], "-m", "lmms_eval"]
    assert "mme,mmmu_val" in command
    assert run_lmms_eval(config, dry_run=True)["status"] == "dry-run"

    seen = []
    def fake_runner(argv, **kwargs):
        seen.append((argv, kwargs))
        return subprocess.CompletedProcess(argv, 0, stdout="ok", stderr="")
    assert run_lmms_eval(config, runner=fake_runner)["status"] == "completed"
    assert seen[0][1]["check"] is True
