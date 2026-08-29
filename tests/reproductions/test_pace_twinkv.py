from __future__ import annotations

import pytest

from auto_research.reproductions.pace_vlm.model import (
    apc_scores,
    dual_attention_saliency,
    target_resolution,
)
from auto_research.reproductions.pace_vlm.checkpoint import answer_match
from auto_research.reproductions.twinkv.checkpoint import evaluate_layer
from auto_research.reproductions.twinkv.model import (
    repair_retained_indices,
    streaming_retained_indices,
)


def test_pace_apc_preserves_more_pixels_for_diverse_features():
    torch = pytest.importorskip("torch")
    redundant = torch.ones(64, 16)
    diverse = torch.eye(16).repeat(4, 1)
    redundant_ratio, _, _ = apc_scores(redundant)
    diverse_ratio, _, _ = apc_scores(diverse)
    assert diverse_ratio > redundant_ratio
    height, width, actual = target_resolution(560, 840, retention=0.1)
    assert height % 28 == width % 28 == 0
    assert abs(actual - 0.1) < 0.02


def test_pace_ddae_favors_the_sharper_attention_source():
    torch = pytest.importorskip("torch")
    llm = torch.tensor([0.0, 0.0, 0.0, 1.0])
    vision = torch.tensor([0.1, 0.2, 0.3, 0.4])
    fused, weights = dual_attention_saliency(llm, vision)
    assert weights[0] > weights[1]
    assert fused.argmax().item() == 3


def test_twinkv_swaps_an_orphan_for_a_redundant_donor_at_fixed_budget():
    torch = pytest.importorskip("torch")
    keys = torch.eye(8)
    # Token 4 duplicates retained token 1; evicted token 3 is an orphan.
    keys[4] = keys[1]
    retained = torch.tensor([0, 1, 2, 4, 6, 7])
    repaired, diagnostics = repair_retained_indices(
        keys,
        retained,
        threshold=0.9,
        local_window=0,
        sink_tokens=1,
        recent_tokens=1,
    )
    assert len(repaired) == len(retained)
    assert 3 in repaired
    assert diagnostics.swaps >= 1


def test_twinkv_is_noop_when_selection_has_no_orphans_or_donors():
    torch = pytest.importorskip("torch")
    keys = torch.eye(6)
    retained = torch.arange(6)
    repaired, diagnostics = repair_retained_indices(
        keys, retained, threshold=0.9, local_window=0
    )
    assert torch.equal(repaired, retained)
    assert diagnostics.swaps == 0


def test_pace_checkpoint_answer_matching_is_normalized_but_not_fuzzy():
    assert answer_match("The answer is: Red.", ["red"])
    assert not answer_match("reddish", ["red"])


def test_twinkv_checkpoint_uses_the_same_budget_for_both_variants():
    from types import SimpleNamespace

    torch = pytest.importorskip("torch")
    torch.manual_seed(7)
    keys = torch.randn(1, 2, 32, 8)
    values = torch.randn(1, 2, 32, 8)
    config = SimpleNamespace(
        compression_ratio=.5, sink_tokens=2, threshold=.85,
        local_window=4, recent_tokens=8,
    )
    metrics = evaluate_layer(keys, values, config, torch)
    assert metrics["retained_tokens"] == 16
    assert -1 <= metrics["baseline_attention_cosine"] <= 1
    assert -1 <= metrics["twinkv_attention_cosine"] <= 1


def test_pace_and_twinkv_are_executable_evolve_operators():
    from auto_research.evolution.papers import discover_papers
    from auto_research.evolution.planner import allowed_architectures

    papers = discover_papers(
        "PACE TwinKV visual token KV cache", 200, False, track="llm",
    )
    mapped = {paper.arxiv_id: paper.architecture for paper in papers}
    assert mapped["2608.27206"] == "checkpoint_vlm:pace-apc"
    assert mapped["2608.27128"] == "twinkv"
    assert "checkpoint_vlm:pace-apc" in allowed_architectures(
        "vlm-checkpoint", "PACE APC", papers,
    )
    assert "twinkv" in allowed_architectures(
        "micro-llm", "TwinKV KV repair", papers,
    )

    torch = pytest.importorskip("torch")
    from auto_research.evolution.llm_model import MicroLMConfig, build_micro_lm

    model = build_micro_lm(
        "twinkv", MicroLMConfig(vocab_size=32, dimensions=16, layers=1,
                                heads=2, kv_heads=2, sequence_length=16),
    )
    logits = model(torch.randint(0, 32, (2, 16)))
    assert logits.shape == (2, 16, 32)


def test_streaming_policy_preserves_budget_sink_and_recent_tokens():
    retained = streaming_retained_indices(100, 20, sink_tokens=4)
    assert len(retained) == 20
    assert retained[:4].tolist() == [0, 1, 2, 3]
    assert retained[-1].item() == 99
