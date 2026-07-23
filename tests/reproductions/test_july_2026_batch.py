from types import SimpleNamespace

import numpy as np
import pytest

from auto_research.reproductions.july_2026_common import JulyRankingConfig
from auto_research.reproductions.off_context_grpo.model import train_grpo
from auto_research.reproductions.registry import get_adapter


P0_P1_KEYS = (
    "tsgr",
    "whale",
    "ramp",
    "dynamic-rubric",
    "off-context-grpo",
    "tmallgs",
    "long-history-transformer",
    "downstream-rewards",
)


def test_july_p0_p1_metadata_and_selection_gate():
    for key in P0_P1_KEYS:
        paper = get_adapter(key).paper
        assert paper.published
        assert paper.organization
        assert paper.url == f"https://arxiv.org/abs/{paper.arxiv_id}"
    for key in (
        "tsgr",
        "whale",
        "ramp",
        "tmallgs",
        "long-history-transformer",
        "downstream-rewards",
    ):
        assert get_adapter(key).paper.has_online_ab
    assert get_adapter("dynamic-rubric").paper.selection_exception


@pytest.mark.parametrize(
    ("builder_path", "builder_name"),
    (
        ("auto_research.reproductions.whale.model", "build_whale"),
        ("auto_research.reproductions.tmallgs.model", "build_tmallgs"),
        (
            "auto_research.reproductions.long_history_transformer.model",
            "build_long_history_model",
        ),
    ),
)
def test_new_transformer_models_produce_full_catalog_scores(builder_path, builder_name):
    torch = pytest.importorskip("torch")
    module = __import__(builder_path, fromlist=[builder_name])
    builder = getattr(module, builder_name)
    data = SimpleNamespace(
        item_count=31,
        item_features=np.eye(31, 7, dtype=np.float32),
    )
    config = JulyRankingConfig(
        dimensions=12,
        heads=3,
        layers=1,
        sequence_length=8,
        batch_size=2,
        steps=1,
    )
    model = builder(data, config)
    output = model(torch.randint(0, data.item_count, (2, config.sequence_length)))
    logits = output["logits"] if isinstance(output, dict) else output
    assert logits.shape == (2, data.item_count)


def test_off_context_sampling_increases_reward_bearing_groups():
    rng = np.random.default_rng(7)
    examples = []
    for _ in range(40):
        features = rng.normal(size=(8, 6))
        examples.append({"features": features, "gold": int(rng.integers(8))})
    _, vanilla = train_grpo(examples, steps=80, seed=42, off_context=False)
    _, guided = train_grpo(examples, steps=80, seed=42, off_context=True)
    assert guided["successful_reward_group_rate"] > vanilla["successful_reward_group_rate"]
    assert guided["mean_importance_correction"] != 1.0


def test_ramp_exposes_personalized_and_restricted_inference_paths():
    torch = pytest.importorskip("torch")
    from auto_research.reproductions.ramp.model import build_privacy_ranker

    data = SimpleNamespace(
        item_count=31,
        item_features=np.eye(31, 7, dtype=np.float32),
    )
    config = JulyRankingConfig(
        dimensions=12,
        heads=3,
        layers=1,
        sequence_length=8,
        batch_size=2,
        steps=1,
    )
    model = build_privacy_ranker(data, config, ramp=True)
    histories = torch.randint(0, data.item_count, (2, config.sequence_length))
    personalized = model(histories, mode="personalized")["logits"]
    restricted = model(histories, mode="non_personalized")["logits"]
    assert personalized.shape == restricted.shape == (2, data.item_count)
    assert not torch.allclose(personalized, restricted)
