from __future__ import annotations

import numpy as np

from auto_research.evolution import EvolutionConfig, ModelEvolutionEngine
from auto_research.evolution.planner import allowed_architectures
from auto_research.evolution.providers import get_provider
from auto_research.multimodal.data import load_visual_shapes
from auto_research.multimodal.model import build_micro_vlm


def test_visual_shapes_is_deterministic_and_pixel_dependent():
    first, second = load_visual_shapes(), load_visual_shapes()
    assert np.array_equal(first.train.images, second.train.images)
    assert first.train.images.shape == (480, 3, 32, 32)
    assert set(first.train.questions) == {0, 1, 2}
    assert len(set(first.train.answers)) == 9


def test_all_micro_vlm_connectors_execute():
    import torch

    images = torch.zeros(2, 3, 32, 32)
    questions = torch.tensor([0, 2])
    for architecture in allowed_architectures("micro-vlm", "query projector", []):
        model = build_micro_vlm(architecture, 32)
        assert model(images, questions).shape == (2, 9)
        assert model.architecture_stats()["visual_tokens"] == 16


def test_micro_vlm_provider_runs_complete_evolution(tmp_path):
    config = EvolutionConfig(
        model="micro-vlm",
        dataset="visual-shapes",
        direction="compare MLP and query connectors",
        output_dir=tmp_path / "runs",
        generations=1,
        population=2,
        steps=3,
        seeds=(42,),
        llm_dimensions=32,
        llm_batch_size=8,
        allow_network=False,
    )
    assert get_provider("micro-vlm").track == "llm"
    result, run_dir = ModelEvolutionEngine(config, project_dir=tmp_path).run()
    assert result.dataset_summary["offline"] is True
    assert result.champion_test is not None
    assert "visual_dependency_delta" in result.champion_test
    assert (run_dir / "report.md").exists()
    assert "打乱图" in (run_dir / "report.md").read_text(encoding="utf-8")
    assert "rendered train images" in (run_dir / "index.html").read_text(encoding="utf-8")
