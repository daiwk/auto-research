from __future__ import annotations

import json
from pathlib import Path

import torch

from auto_research.cli import build_parser
from auto_research.multimodal.checkpoint import (
    CheckpointPredictionConfig,
    generate_checkpoint_predictions,
    normalize_prediction,
    prediction_metadata_path,
    resolve_scienceqa_image,
    scienceqa_prompt,
)


class _FakeProcessor:
    def apply_chat_template(self, messages, **kwargs):
        assert messages[0]["role"] == "user"
        return "rendered prompt"

    def __call__(self, **kwargs):
        return {"input_ids": torch.tensor([[1, 2]])}

    def decode(self, tokens, **kwargs):
        return "Answer: B"


class _FakeModel:
    def generate(self, input_ids, **kwargs):
        return torch.cat((input_ids, torch.tensor([[3, 4]])), dim=1)


def test_scienceqa_prompt_and_official_image_layout(tmp_path):
    image = tmp_path / "test" / "17" / "image.png"
    image.parent.mkdir(parents=True)
    image.write_bytes(b"test fixture; image decoding is covered by the optional dependency run")
    row = {
        "question": "What color?",
        "hint": "Look at the square.",
        "choices": ["red", "blue"],
    }
    prompt = scienceqa_prompt(row)
    assert "Context: Look at the square." in prompt
    assert "A. red\nB. blue" in prompt
    assert resolve_scienceqa_image(tmp_path, "test", "17", "image.png") == image


def test_prediction_normalization_is_strict():
    assert normalize_prediction("scienceqa", "The answer is (C).", ("a", "b", "c")) == "C"
    assert normalize_prediction("scienceqa", "blue", ("red", "blue")) == "B"
    assert normalize_prediction("pope", "No, it is not.") == "no"
    assert normalize_prediction("scienceqa", "an explanation", ("a", "b")) == "__invalid__"


def test_checkpoint_predictions_are_resumable_and_record_provenance(tmp_path, monkeypatch):
    monkeypatch.setenv("AUTO_RESEARCH_DEVICE", "cpu")
    annotations = tmp_path / "scienceqa"
    annotations.mkdir()
    (annotations / "problems.json").write_text(json.dumps({
        "1": {
            "question": "Pick blue",
            "choices": ["red", "blue"],
            "answer": 1,
        },
    }))
    (annotations / "pid_splits.json").write_text(json.dumps({"test": ["1"]}))
    output = tmp_path / "predictions.jsonl"
    config = CheckpointPredictionConfig(
        benchmark="scienceqa",
        annotations=annotations,
        image_root=tmp_path,
        output=output,
        model_id="example/model",
        revision="immutable-sha",
    )
    first = generate_checkpoint_predictions(
        config, processor=_FakeProcessor(), model=_FakeModel(), torch_module=torch
    )
    second = generate_checkpoint_predictions(
        config, processor=_FakeProcessor(), model=_FakeModel(), torch_module=torch
    )
    rows = [json.loads(line) for line in output.read_text().splitlines()]
    assert rows == [{
        "id": "1",
        "prediction": "B",
        "raw_prediction": "Answer: B",
        "model_id": "example/model",
        "model_revision": "immutable-sha",
        "seed": 42,
        "prediction_valid": True,
    }]
    assert first["new_predictions"] == 1
    assert second["new_predictions"] == 0
    metadata = json.loads(prediction_metadata_path(output).read_text())
    assert metadata["resolved_revision"] == "immutable-sha"
    assert metadata["deterministic_decoding"] is True


def test_multimodal_predict_cli_contract():
    args = build_parser().parse_args([
        "multimodal-predict", "--benchmark", "scienceqa",
        "--annotations", "scienceqa", "--image-root", "images",
        "--output", "predictions.jsonl", "--device", "cpu",
        "--checkpoint-path", "checkpoint",
    ])
    assert args.model_id == "HuggingFaceTB/SmolVLM2-256M-Video-Instruct"
    assert args.max_new_tokens == 16
    assert args.checkpoint_path == Path("checkpoint")
    assert args.device == "cpu"


def test_resume_rejects_a_different_checkpoint(tmp_path, monkeypatch):
    monkeypatch.setenv("AUTO_RESEARCH_DEVICE", "cpu")
    annotations = tmp_path / "scienceqa"
    annotations.mkdir()
    (annotations / "problems.json").write_text(json.dumps({
        "1": {"question": "pick", "choices": ["x", "y"], "answer": 1},
    }))
    (annotations / "pid_splits.json").write_text(json.dumps({"test": ["1"]}))
    output = tmp_path / "predictions.jsonl"
    output.write_text(json.dumps({
        "id": "1", "prediction": "B", "model_id": "another/model",
        "model_revision": "immutable-sha",
    }) + "\n")
    config = CheckpointPredictionConfig(
        benchmark="scienceqa", annotations=annotations, image_root=tmp_path,
        output=output, model_id="example/model", revision="immutable-sha",
    )
    import pytest
    with pytest.raises(ValueError, match="model mismatch"):
        generate_checkpoint_predictions(
            config, processor=_FakeProcessor(), model=_FakeModel(), torch_module=torch
        )


def test_committed_scienceqa_checkpoint_result_is_auditable():
    path = Path(__file__).parents[1] / (
        "docs/multimodal-models/metrics/scienceqa-smolvlm2-256m-500.json"
    )
    payload = json.loads(path.read_text())
    assert payload["evaluated_examples"] == 500
    assert payload["formal_comparison"] is False
    assert payload["metadata"]["checkpoint_committed"] is False
    assert payload["metadata"]["model_revision"] == (
        "067788b187b95ebe7b2e040b3e4299e342e5b8fd"
    )
    assert payload["aggregate_metrics"]["accuracy"]["mean"] == 0.568
    assert payload["aggregate_metrics"]["parse_rate"]["mean"] == 0.998
