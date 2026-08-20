import csv
import json
from pathlib import Path
from types import SimpleNamespace

import numpy as np
import torch

from auto_research.cli import build_parser
from auto_research.multimodal.audio import AudioBenchmarkConfig, run_audio_benchmark
from auto_research.multimodal.video import VideoBenchmarkConfig, run_video_benchmark


class FakeVideoProcessor:
    def apply_chat_template(self, messages, **kwargs):
        assert messages[0]["content"][0]["type"] == "video"
        assert len(messages[0]["content"][0]["video"]) == 32
        assert kwargs["processor_kwargs"]["do_sample_frames"] is False
        assert len(kwargs["processor_kwargs"]["video_metadata"]) == 1
        return {"input_ids": torch.tensor([[1, 2]])}

    def decode(self, values, **kwargs):
        return "Answer: B"


class FakeVideoModel:
    def generate(self, input_ids, **kwargs):
        return torch.cat((input_ids, torch.tensor([[3]])), dim=1)


def test_video_checkpoint_runner_is_resumable_and_reports_three_seed_ci(tmp_path, monkeypatch):
    monkeypatch.setenv("AUTO_RESEARCH_DEVICE", "cpu")
    (tmp_path / "001.mp4").write_bytes(b"public benchmark fixture")
    annotations = tmp_path / "test.jsonl"
    annotations.write_text(json.dumps({
        "video_id": "001", "question_id": "001-1", "question": "Pick B",
        "options": "A. no B. yes", "answer": "B",
    }) + "\n", encoding="utf-8")
    config = VideoBenchmarkConfig(
        annotations=annotations, video_root=tmp_path, output_dir=tmp_path / "run",
        model_id="test/video", model_revision="immutable", seeds=(1, 2, 3),
    )
    first, _ = run_video_benchmark(
        config, processor=FakeVideoProcessor(), model=FakeVideoModel(),
        torch_module=torch,
        video_loader=lambda path, frames: (
            np.zeros((frames, 2, 2, 3)), SimpleNamespace(fps=24.0)
        ),
    )
    second, _ = run_video_benchmark(
        config, processor=FakeVideoProcessor(), model=FakeVideoModel(),
        torch_module=torch,
        video_loader=lambda path, frames: (
            np.zeros((frames, 2, 2, 3)), SimpleNamespace(fps=24.0)
        ),
    )
    assert first["metrics"]["accuracy_mean"] == 1.0
    assert first["metrics"]["accuracy_ci95_radius"] == 0.0
    assert second["metrics"]["seed_runs"][0]["accuracy"] == 1.0
    assert len(list((tmp_path / "run").glob("predictions-seed*.jsonl"))) == 3


class FakeFeatureExtractor:
    sampling_rate = 4


class FakeAudioProcessor:
    feature_extractor = FakeFeatureExtractor()

    def __call__(self, *, text=None, audio=None, **kwargs):
        if text is not None:
            return {"input_ids": torch.tensor([
                [1.0, 0.0] if "cat" in value else [0.0, 1.0] for value in text
            ])}
        value = float(np.mean(audio))
        return {"input_features": torch.tensor([[1.0, 0.0] if value > 0.5 else [0.0, 1.0]])}


class FakeAudioModel:
    def get_text_features(self, input_ids):
        return SimpleNamespace(pooler_output=input_ids)

    def get_audio_features(self, input_features):
        return SimpleNamespace(pooler_output=input_features)


def test_audio_checkpoint_runner_validates_embedding_cache_and_resume(tmp_path, monkeypatch):
    monkeypatch.setenv("AUTO_RESEARCH_DEVICE", "cpu")
    for name in ("cat.wav", "dog.wav"):
        (tmp_path / name).write_bytes(b"audio fixture")
    annotations = tmp_path / "esc50.csv"
    with annotations.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["filename", "fold", "category"])
        writer.writeheader()
        writer.writerow({"filename": "cat.wav", "fold": 1, "category": "cat"})
        writer.writerow({"filename": "dog.wav", "fold": 1, "category": "dog"})
    config = AudioBenchmarkConfig(
        annotations=annotations, audio_root=tmp_path, output_dir=tmp_path / "run",
        model_id="test/clap", model_revision="immutable",
    )
    loader = lambda path: (
        np.ones(4, dtype=np.float32) if path.name == "cat.wav"
        else np.zeros(4, dtype=np.float32), 4
    )
    first, _ = run_audio_benchmark(
        config, processor=FakeAudioProcessor(), model=FakeAudioModel(),
        torch_module=torch, audio_loader=loader,
    )
    second, _ = run_audio_benchmark(
        config, processor=FakeAudioProcessor(), model=FakeAudioModel(),
        torch_module=torch, audio_loader=loader,
    )
    assert first["metrics"]["zero_shot_top1_accuracy"] == 1.0
    assert first["cache"]["text_embedding_cache_hit"] is False
    assert second["cache"]["text_embedding_cache_hit"] is True


def test_video_audio_cli_contracts_pin_public_checkpoints():
    video = build_parser().parse_args([
        "multimodal-video-eval", "--annotations", "test.parquet",
        "--video-root", "videos",
    ])
    audio = build_parser().parse_args([
        "multimodal-audio-eval", "--annotations", "esc50.csv",
        "--audio-root", "audio",
    ])
    assert len(video.model_revision) == 40
    assert video.seeds == "42,43,44"
    assert len(audio.model_revision) == 40
