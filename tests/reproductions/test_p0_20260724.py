from pathlib import Path

import numpy as np

from auto_research.evolution.llm_model import MicroLMConfig, build_micro_lm
from auto_research.reproductions.barge.model import (
    BARGEConfig, build_barge, train_osq_ids,
)
from auto_research.reproductions.registry import get_adapter


DATA = Path(__file__).resolve().parents[2] / "data"


def test_p0_adapters_are_registered_with_required_evidence():
    barge = get_adapter("barge")
    assert barge.paper.has_online_ab
    assert {entry.metric for entry in barge.paper.online_ab} == {
        "CTR", "click UV", "total reading time",
    }
    assert get_adapter("mobius-rope").paper.track == "llm"
    assert get_adapter("naju").paper.track == "llm"


def test_osq_rotation_is_orthogonal_and_dual_ids_cover_catalog():
    features = np.random.default_rng(42).normal(size=(40, 8)).astype(np.float32)
    config = BARGEConfig(
        codebook_size=4, osq_steps=2, training_steps=1, batch_size=4
    )
    (left, right), diagnostics = train_osq_ids(features, config, 42)
    assert left.shape == right.shape == (40, config.codebooks + 1)
    assert diagnostics["orthogonality_error"] < 1e-5
    model = build_barge(left, right, config)
    assert model.ids_a.shape[0] == len(features)


def test_mobius_and_naju_are_real_causal_lm_architectures():
    import torch

    config = MicroLMConfig(
        vocab_size=64, dimensions=32, layers=1, heads=4, sequence_length=12
    )
    tokens = torch.randint(0, 64, (2, 12))
    for architecture in ("mobius_rope", "naju"):
        model = build_micro_lm(architecture, config)
        assert model(tokens).shape == (2, 12, 64)
    stats = build_micro_lm("naju", config)
    stats(tokens)
    values = stats.sequence_mixer_stats()
    assert 0 < values["forget_mean"] < 1
    assert 0 < values["write_mean"] < 1
