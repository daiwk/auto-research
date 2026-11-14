from dataclasses import FrozenInstanceError
import math

import pytest

from auto_research.post_training.emoreward import (
    ReferenceTrace,
    RewardMemory,
    build_reward_memory,
    diagnostic,
    fuse_reward,
)


def test_equations_nine_and_ten_match_hand_calculation():
    # x=(0,1), y=(1,3): population covariance 0.5, sigma_x*sigma_y 0.5.
    # The second provider is constant, so centered correlations are +/-0.4.
    memory = build_reward_memory(
        [ReferenceTrace("r", (0.0, 0.2), 1.0), ReferenceTrace("r", (1.0, 0.2), 3.0)],
        provider_count=2, temperature=0.5, cap=1.0, minimum_support=2, epsilon=0.125,
    )
    expected = (math.exp(0.8), math.exp(-0.8))
    assert memory.multipliers("r") == pytest.approx(expected)
    denominator = 0.25 * expected[0] + 0.75 * expected[1]
    assert memory.weights((0.25, 0.75), "r") == pytest.approx(
        (0.25 * expected[0] / denominator, 0.75 * expected[1] / denominator)
    )
    assert memory.weights((1.0, 0.0), "r") == (1.0, 0.0)


def test_sign_regime_clipping_and_global_fallback():
    rows = [
        ReferenceTrace("a", (0.0, 1.0), 0.0), ReferenceTrace("a", (1.0, 0.0), 1.0),
        ReferenceTrace("b", (1.0, 0.0), 0.0), ReferenceTrace("b", (0.0, 1.0), 1.0),
        ReferenceTrace("rare", (0.5, 0.5), 0.5),
    ]
    memory = build_reward_memory(rows, provider_count=2, minimum_support=2, cap=0.2)
    positive, negative = math.exp(0.2), math.exp(-0.2)
    assert memory.multipliers("a") == (positive, negative)
    assert memory.multipliers("b") == (negative, positive)
    assert memory.multipliers("rare") == memory.multipliers("unknown") == (1.0, 1.0)


def test_equation_eight_threshold_before_normalizing_and_no_masked_evidence():
    opts = dict(scores=(0.5, 0.0, 1.0), gates=(0.5, 1.0, 0.0),
                base_weights=(0.25, 0.25, 0.5), context="r", video_reward=0.5,
                gate_threshold=0.25, epsilon=0.125)
    memory = RewardMemory(3, (2.0, 4.0, 100.0))
    result = fuse_reward(**opts, memory=memory)
    # First a=0.25 is strictly excluded; even a very large prior cannot unmask third.
    assert result.active_weights == (0.0, 1.0, 0.0)
    assert result.emotion_reward == 0.0
    assert result.total_reward == 0.25
    opts["gate_threshold"] = 0.125
    assert fuse_reward(**opts, memory=memory).emotion_reward == pytest.approx(0.125 / 1.375)


def test_cold_start_and_frozen_tables():
    raw = {"r": [2.0, 0.5]}
    memory = RewardMemory(2, contexts=raw)
    raw["r"][0] = 500
    assert memory.multipliers("r") == (2.0, 0.5)
    with pytest.raises(TypeError):
        memory.contexts["r"] = (1.0, 1.0)
    with pytest.raises(FrozenInstanceError):
        memory.global_multipliers = (3.0, 3.0)
    opts = dict(scores=(1.0, 0.0), gates=(0.0, 0.0), base_weights=(0.5, 0.5),
                context="r", video_reward=0.4)
    assert fuse_reward(**opts) == fuse_reward(**opts, memory=build_reward_memory([], provider_count=2))
    assert fuse_reward(**opts).total_reward == pytest.approx(0.2)


def test_rejects_malformed_traces_and_device():
    with pytest.raises(ValueError, match="trace width"):
        build_reward_memory([ReferenceTrace("a", (0.0,), 1.0)], provider_count=2)
    with pytest.raises(ValueError, match="reference outcome"):
        build_reward_memory([ReferenceTrace("a", (0.0,), math.nan)], provider_count=1)
    with pytest.raises(ValueError, match="base weights"):
        fuse_reward(scores=(0.1,), gates=(1.0,), base_weights=(0.1,), context="a", video_reward=0.0)
    with pytest.raises(ValueError, match="CPU-only"):
        diagnostic(42, "cuda")
    outputs = [diagnostic(seed) for seed in (42, 43, 44)]
    assert all(row["evaluation_tier"] == "l1_mechanism" and all(row["checks"].values()) for row in outputs)
    assert len({row["metrics"]["reference_mean_outcome"] for row in outputs}) == len(outputs)
