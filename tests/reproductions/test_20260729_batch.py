from __future__ import annotations

from pathlib import Path

import pytest

from auto_research.reproductions.registry import get_adapter


DATA = Path(__file__).resolve().parents[2] / "data"


@pytest.mark.parametrize(
    ("key", "stage"),
    [
        ("reco-reward", "frozen_two_tower"),
        ("twice", "click_clock_current_status"),
        ("swag-bid", "multi_window_mpc_sampling"),
        ("youtube-freshness", "serving_recency_boost"),
        ("melo", "search_index_verification"),
    ],
)
def test_latest_industrial_papers_execute_distinct_core_mechanisms(
    key: str, stage: str
):
    adapter = get_adapter(key)
    result = adapter.run(DATA, 42)
    assert adapter.paper.online_ab
    assert result["setup"]["same_split_and_candidates"] is True
    assert result["stages"][stage]
    assert set(result["relative"]) == {
        "hit_at_10_percent",
        "ndcg_at_10_percent",
        "fresh_hit_at_10_percent",
        "head_share_at_10_percent",
    }


def test_penelope_is_a_real_localized_recurrent_architecture():
    torch = pytest.importorskip("torch")
    from auto_research.evolution.llm_model import MicroLMConfig, build_micro_lm

    model = build_micro_lm(
        "penelope",
        MicroLMConfig(
            vocab_size=64,
            sequence_length=12,
            dimensions=32,
            layers=2,
            heads=4,
        ),
    )
    logits = model(torch.randint(0, 64, (2, 12)))
    assert logits.shape == (2, 12, 64)
    assert model.architecture_stats()["latent_recurrence_steps"] == 2
    assert model.architecture_stats()["full_decoder_reexecution"] == 0
