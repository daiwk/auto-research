from pathlib import Path

import numpy as np

from auto_research.reproductions.latest_20260915 import (
    chronicle_tokens,
    exclusive_assignment,
    pixel_penalty,
    recency_merge,
)
from auto_research.reproductions.registry import get_adapter
from auto_research.reproductions.sas_attention.model import build_tiny_sas_lm


def test_pindco_pixel_penalty_is_bounded_and_monotone():
    penalty = pixel_penalty([0.5, 1.0, 1.5], 0.7)
    assert np.all((0 <= penalty) & (penalty <= 1))
    assert np.all(np.diff(penalty) <= 0)
    assert penalty[-1] < penalty[0]


def test_mima_exclusive_assignment_is_one_to_one_and_optimal():
    assignment, cost = exclusive_assignment([[0.1, 2.0, 3.0], [4.0, 0.2, 1.0], [2.0, 3.0, 0.3]])
    assert assignment.tolist() == [0, 1, 2]
    assert len(set(assignment)) == 3
    assert np.isclose(cost, 0.6)


def test_chronicle_tokens_are_compressed_and_multi_horizon():
    features = np.eye(20)
    history = tuple(range(20))
    merged = recency_merge(features, history)
    tokens = chronicle_tokens(features, history)
    assert len(merged) < len(history)
    assert tokens.shape[0] >= 9
    assert tokens.shape[1] == features.shape[1]


def test_latest_industrial_adapters_have_evidence_and_execute():
    for key in ("pindco", "mima", "chronicle-rec"):
        adapter = get_adapter(key)
        assert adapter.paper.has_online_ab
        assert adapter.paper.online_ab[0].source_location
        result = adapter.run(Path("data"), 42)
        assert result["manifest_ref"] == f"reproduction:{key}"
        assert result["setup"]["same_split_and_candidates"] is True


def test_sas_log_gate_reaches_selector_and_reduces_attention_scope():
    import torch

    torch.manual_seed(7)
    model = build_tiny_sas_lm(
        vocab_size=32, dimensions=16, heads=2, sequence_length=24,
        block_size=4, top_k_blocks=1,
    )
    tokens = torch.randint(0, 32, (2, 24))
    loss = torch.nn.functional.cross_entropy(
        model(tokens).reshape(-1, 32), torch.roll(tokens, -1, dims=1).reshape(-1)
    )
    loss.backward()
    gradient = model.attention.selector_q.weight.grad
    assert gradient is not None
    assert float(gradient.abs().sum()) > 0
    assert 0 < model.attention.last_diagnostics["retained_attention_fraction"] < 1


def test_sas_adapter_executes_public_dataset_training():
    result = get_adapter("sas-attention").run(Path("data"), 42)
    assert result["manifest_ref"] == "reproduction:sas-attention"
    assert result["selector_training"]["selector_gradient_norm_mean"] > 0
    assert result["setup"]["frozen_backbone_during_selector_training"] is True
    assert 0 < result["routing"]["retained_attention_fraction"] < 1
