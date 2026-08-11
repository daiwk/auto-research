from __future__ import annotations

import numpy as np
import pickle

from auto_research.evolution import EvolutionConfig, ModelEvolutionEngine
from auto_research.evolution.engine import _paper_ids
from auto_research.evolution.models import Genome, PaperInspiration
from auto_research.evolution.planner import allowed_architectures
from auto_research.evolution.providers import get_provider
from auto_research.multimodal.data import load_cifar10_qa, load_visual_shapes
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
    architectures = allowed_architectures("micro-vlm", "query projector", [])
    assert "objective:siglip2" in architectures
    for architecture in architectures:
        if architecture.startswith("objective:"):
            continue
        model = build_micro_vlm(architecture, 32)
        assert model(images, questions).shape == (2, 9)
        expected_tokens = 4 if architecture in {
            "micro_vlm_qformer", "micro_vlm_pixelshuffle"
        } else 16
        assert model.architecture_stats()["visual_tokens"] == expected_tokens


def test_multimodal_paper_source_attribution_uses_the_selected_operator():
    papers = [
        PaperInspiration(
            "2301.12597", "BLIP-2", "https://arxiv.org/abs/2301.12597",
            "2023-01-30", "micro_vlm_qformer", "query connector", "fallback",
            executable=True,
        ),
        PaperInspiration(
            "2502.14786", "SigLIP 2", "https://arxiv.org/abs/2502.14786",
            "2025-02-20", "objective:siglip2", "sigmoid objective", "fallback",
            executable=True,
        ),
        PaperInspiration(
            "2401.02385", "TinyLlama", "https://arxiv.org/abs/2401.02385",
            "2024-01-04", "small_llm", "small language model", "fallback",
            executable=True,
        ),
    ]
    qformer = Genome(architecture="micro_vlm_qformer")
    siglip = Genome(
        architecture="micro_vlm_linear", multimodal_objective="siglip2"
    )
    assert _paper_ids(qformer, papers) == ("2301.12597",)
    assert _paper_ids(siglip, papers) == ("2502.14786",)


def test_cifar10_qa_uses_cached_official_batches_offline(tmp_path):
    extracted = tmp_path / "cifar10" / "cifar-10-batches-py"
    extracted.mkdir(parents=True)
    rng = np.random.default_rng(7)

    def write_batch(name, count):
        labels = np.arange(count) % 10
        pixels = rng.integers(0, 256, size=(count, 3072), dtype=np.uint8)
        with (extracted / name).open("wb") as handle:
            pickle.dump({b"data": pixels, b"labels": labels.tolist()}, handle)

    for index in range(1, 6):
        write_batch(f"data_batch_{index}", 20)
    write_batch("test_batch", 20)
    data = load_cifar10_qa(tmp_path, allow_network=False, maximum_examples=40)
    assert data.train.images.shape == (40, 3, 32, 32)
    assert len(data.validation.answers) == 20
    assert len(data.test.answers) == 20
    assert set(data.train.answers) == set(range(10))
    assert data.evaluation_tier == "l1_public_images"


def test_cifar10_offline_mode_requires_an_existing_cache(tmp_path):
    try:
        load_cifar10_qa(tmp_path, allow_network=False)
    except FileNotFoundError as error:
        assert "rerun once without --offline" in str(error)
    else:
        raise AssertionError("an absent offline CIFAR-10 cache must fail")


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
