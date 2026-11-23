"""VFD/RA-GRPO numeric controls without visual agents or policy training."""
import numpy as np
import pytest

from auto_research.agent_research.r2_tool_redundancy import (
    REQUIRES_GPU_VALIDATION, FrozenThresholds, WarmupWindow, calibrate_thresholds, clipped_objective,
    diagnostic, redundancy_aware_advantages, trajectory_cost, visual_feedback_dependency,
)


def test_vfd_scores_same_text_under_actual_and_three_alternatives():
    assert visual_feedback_dependency([-.2, -.4], [[-.8, -.6]] * 3) == pytest.approx(.4)
    assert visual_feedback_dependency([-.2, -.4], [[-.2, -.4]] * 3) == 0
    assert visual_feedback_dependency([-.8, -.6], [[-.2, -.4]] * 3) == pytest.approx(-.4)


def test_threshold_uses_only_reasoning_warmup_and_stays_source_specific():
    thresholds = calibrate_thresholds([WarmupWindow("a", x) for x in (.1, .2, .4, .8)]
                                     + [WarmupWindow("a", -100, False), WarmupWindow("b", 10)])
    assert thresholds.for_source("a") == pytest.approx(.19)
    assert thresholds.for_source("b") == 10
    with pytest.raises(ValueError):
        thresholds.for_source("test-unseen-source")
    with pytest.raises(ValueError):
        calibrate_thresholds([WarmupWindow("a", 1, False)])


def test_low_dependency_is_strict_and_none_means_unavailable_complete_score():
    assert trajectory_cost([.3], total_calls=1, category="Challenging", threshold=.3, seed=1)[0] == 0
    assert trajectory_cost([.299], total_calls=1, category="Challenging", threshold=.3, seed=1)[0] == 1
    assert trajectory_cost([None], total_calls=1, category="Challenging", threshold=.3, seed=1)[0] == 1
    assert trajectory_cost([], total_calls=2, category="Tool-Independent", threshold=.3, seed=1)[0] == 1
    assert trajectory_cost([], total_calls=2, category="Tool-Beneficial", threshold=.3, seed=1)[0] == 0


def test_one_uniform_call_estimator_seeded_sampling_sanity():
    # For two low-dependency calls out of three, M*z takes0 or3; expectation2.
    costs = []
    selected_indices = set()
    for seed in range(300):
        cost, index = trajectory_cost([.1, .2, .5], total_calls=3,
                                      category="Tool-Beneficial", threshold=.3, seed=seed)
        costs.append(cost)
        selected_indices.add(index)
    assert selected_indices == {0, 1, 2}
    assert set(costs) == {0., 3.}
    # This is a broad deterministic sanity check, not a stochastic accuracy claim.
    assert abs(np.mean(costs) - 2) < .25


def test_efficiency_only_compares_correct_and_uses_fixed_budget():
    advantage = redundancy_aware_advantages([1, 1, 0, 0], [0, 4, 0, 100], call_budget=4)
    np.testing.assert_allclose(advantage["efficiency"], [.5, -.5, 0, 0])
    np.testing.assert_allclose(advantage["outcome"], np.array([.5, .5, -.5, -.5]) / (np.std([1, 1, 0, 0], ddof=1) + 1e-8))
    assert advantage["combined"][0] > advantage["combined"][1]
    assert advantage["combined"][2] == advantage["combined"][3]


def test_no_correct_single_correct_equal_cost_and_all_equal_reward():
    assert not redundancy_aware_advantages([0, 0], [0, 1])["efficiency"].any()
    assert not redundancy_aware_advantages([1, 0], [3, 0])["efficiency"].any()
    assert not redundancy_aware_advantages([1, 1], [3, 3])["efficiency"].any()
    assert not redundancy_aware_advantages([1, 1], [3, 3])["outcome"].any()


def test_clipping_handles_negative_advantage_and_per_trajectory_mask_means():
    assert clipped_objective([[1.5], [.5]], [1, -1]) == pytest.approx(.2)
    # Positive: min(1.5,1.2)=1.2; negative: min(-.5,-.8)=-.8.
    mask = np.array([[True, False], [True, True]])
    assert clipped_objective([[1, 999], [1, 1]], [2, -1], mask=mask) == .5
    assert clipped_objective([[1, 1e308], [1, 1]], [2, -1], mask=mask) == .5


def test_frozen_threshold_constructor_cannot_bypass_finite_unique_contract():
    for values in ((('a', float('nan')),), (('a', 1), ('a', 2)), [('a', 1)]):
        with pytest.raises(ValueError):
            FrozenThresholds(values)


@pytest.mark.parametrize("call", [
    lambda: visual_feedback_dependency([], [[]]),
    lambda: visual_feedback_dependency([.1], [[-.1]]),
    lambda: visual_feedback_dependency([-.1], [[-.2, -.3]]),
    lambda: trajectory_cost([float("nan")], total_calls=1, category="Challenging", threshold=0, seed=0),
    lambda: trajectory_cost([0, 0], total_calls=1, category="Challenging", threshold=0, seed=0),
    lambda: redundancy_aware_advantages([1], [0]),
    lambda: redundancy_aware_advantages([1, .5], [0, 0]),
    lambda: redundancy_aware_advantages([1, 0], [-1, 0]),
    lambda: clipped_objective([[1], [1]], [1, 0], mask=np.array([[False], [True]])),
    lambda: clipped_objective([[1e308], [1]], [1e308, 0]),
])
def test_invalid_or_overflowing_contracts_rejected(call):
    with pytest.raises(ValueError):
        call()


def test_cpu_diagnostic_contract():
    assert REQUIRES_GPU_VALIDATION is False
    for seed in (42, 43, 44):
        result = diagnostic(seed)
        assert result["seed"] == seed and result["diagnostic_only"] is True
        assert result["evaluation_tier"] == "l1_mechanism" and all(result["checks"].values())
        assert result["training_executed"] is False and result["visual_agent_evaluation_executed"] is False
    with pytest.raises(ValueError):
        diagnostic(42, "cuda")
