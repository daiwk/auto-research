"""Independent scalar/gradient checks; not LLM capability evaluation."""

import numpy as np
import pytest
import torch

from auto_research.post_training import bait_reward_defense as bait
from auto_research.post_training import lgpo
from auto_research.post_training import safety_budget_cgrpo as budget


def test_lgpo_sequence_average_boundary_and_all_sequence_denominator():
    logp = torch.tensor(
        [[-0.1, -0.2], [-0.01, -0.01], [-2.0, -1.0]], dtype=torch.float64, requires_grad=True
    )
    advantage = torch.tensor(
        [[2.0, 2.0], [-3.0, -3.0], [-1.0, -1.0]], dtype=torch.float64, requires_grad=True
    )
    mask = torch.ones_like(logp, dtype=torch.bool)
    objective, retained = lgpo.loss(logp, advantage, mask)
    assert retained.tolist() == [True, False, True]
    assert objective.item() == pytest.approx(-((-0.1 - 0.2) * 2 + (-2 - 1) * -1) / 3)
    objective.backward()
    assert torch.allclose(
        logp.grad, torch.tensor([[-2 / 3, -2 / 3], [0.0, 0.0], [1 / 3, 1 / 3]], dtype=torch.float64)
    )
    assert advantage.grad is None


def test_lgpo_padding_has_no_gate_or_gradient_effect():
    logp = torch.tensor([[-0.2, -10.0]], dtype=torch.float64, requires_grad=True)
    objective, retained = lgpo.loss(logp, torch.ones_like(logp), torch.tensor([[True, False]]))
    assert retained.tolist() == [True]
    assert objective.item() == pytest.approx(0.2)
    objective.backward()
    assert logp.grad.tolist() == [[-1.0, 0.0]]


def test_lgpo_gates_both_advantage_signs_and_all_gated_is_differentiable():
    logp = torch.tensor([[-0.01], [-0.01]], requires_grad=True)
    objective, retained = lgpo.loss(
        logp, torch.tensor([[1.0], [-1.0]]), torch.ones_like(logp, dtype=torch.bool)
    )
    assert not retained.any()
    objective.backward()
    assert objective.item() == 0
    assert (logp.grad == 0).all()


@pytest.mark.parametrize("bad", [float("nan"), float("inf"), 0.1, True])
def test_lgpo_invalid_threshold(bad):
    with pytest.raises(ValueError):
        lgpo.loss(
            torch.tensor([[-1.0]]),
            torch.ones(1, 1),
            torch.ones(1, 1, dtype=torch.bool),
            threshold=bad,
        )


@pytest.mark.parametrize("bad", [float("nan"), 0.1])
def test_lgpo_invalid_log_probability(bad):
    with pytest.raises(ValueError):
        lgpo.loss(torch.tensor([[bad]]), torch.ones(1, 1), torch.ones(1, 1, dtype=torch.bool))


def test_lgpo_empty_valid_sequence_rejected():
    with pytest.raises(ValueError):
        lgpo.loss(torch.tensor([[-1.0]]), torch.ones(1, 1), torch.zeros(1, 1, dtype=torch.bool))


def test_pav_merges_ties_before_weighted_adjacent_violations():
    # At x=.1, tie mean=3/4; pooling the next zero (weight2) yields 1/2.
    mapping = budget.fit_isotonic(
        [0.8, 0.1, 0.2, 0.1], [1, 1, 0, 0], weights=[1, 3, 2, 1], split="train"
    )
    assert mapping.x == (0.1, 0.2, 0.8)
    assert mapping.y == pytest.approx((0.5, 0.5, 1.0))
    assert mapping.predict([0.0, 0.1, 0.1999, 0.2, 0.7999, 0.8, 1.0]).tolist() == [
        0.5,
        0.5,
        0.5,
        0.5,
        0.5,
        1.0,
        1.0,
    ]


@pytest.mark.parametrize("split", ["validation", "test", "Train"])
def test_calibration_refuses_evaluation_split(split):
    with pytest.raises(ValueError):
        budget.fit_isotonic([0.1, 0.2], [0, 1], split=split)


def test_raw_base_and_calibrated_penalty_are_separate():
    flat = budget.IsotonicMap((0.0, 1.0), (0.25, 0.25))
    result = budget.two_channel_reward(
        [[0.1, 0.9], [0.9, 0.1]],
        [[0.3, 0.8], [0.2, 0.7]],
        [[0.2, 0.6], [0.8, 0.4]],
        [True, False],
        [2.0, 3.0],
        harm_map=flat,
        refusal_map=flat,
    )
    np.testing.assert_allclose(
        result["base"], [[0.9, 0.1], [0.65 * 0.8 + 0.35 * 0.8, 0.65 * 0.4 + 0.35 * 0.3]]
    )
    np.testing.assert_allclose(result["penalty"], [[0.5, 0.5], [0.75, 0.75]])
    np.testing.assert_allclose(result["reward"], result["base"] - result["penalty"])


def test_unscaled_advantage_retains_multiplier_while_total_zscore_cancels():
    p = np.array([[0.1, 0.3, 0.9]])
    a0, a2 = budget.unscaled_advantage(1 - p), budget.unscaled_advantage(1 - 3 * p)
    np.testing.assert_allclose(a2, 3 * a0)
    np.testing.assert_allclose(a2 / a2.std(), a0 / a0.std())
    with pytest.raises(ValueError):
        budget.unscaled_advantage([[1.0]])


def test_dual_explicit_ema_and_projection():
    lam, ema = budget.update_dual([0.5, 1.0], [0.2, 0.9], [0.8, 0.1], [0.4, 0.5])
    np.testing.assert_allclose(ema, [0.38, 0.66])
    np.testing.assert_allclose(lam, [0.49, 1.08])
    projected, _ = budget.update_dual([0.0, 10.0], [0.0, 1.0], [0.0, 1.0], [1.0, 0.0])
    assert projected.tolist() == [0.0, 10.0]


@pytest.mark.parametrize(
    "scores,labels,weights",
    [([0.1, np.nan], [0, 1], None), ([0.1, 0.2], [0, 0.5], None), ([0.1, 0.2], [0, 1], [1, 0])],
)
def test_pav_invalid_inputs(scores, labels, weights):
    with pytest.raises(ValueError):
        budget.fit_isotonic(scores, labels, weights=weights, split="train")


def test_bait_scalar_means_and_whole_group_flip():
    rewards = np.array([[7.0, 1.0, 3.0], [1.0, 5.0, 7.0], [4.0, 2.0, 6.0]])
    mask = np.array([[True, False, False]] * 3)
    original = rewards.copy()
    result = bait.transform_rewards(rewards, mask)
    assert result.divergence == (5.0, -5.0, 0.0)
    assert result.detected == (True, False, True)
    assert result.transformed_rewards == ((-7.0, -1.0, -3.0), (1.0, 5.0, 7.0), (-4.0, -2.0, -6.0))
    assert result.policy_only_rewards == ((-1.0, -3.0), (5.0, 7.0), (-2.0, -6.0))
    np.testing.assert_array_equal(rewards, original)


@pytest.mark.parametrize("mask", [[[False, False]], [[True, True]], [[1, 0]]])
def test_bait_undefined_or_nonboolean_partition_rejected(mask):
    with pytest.raises(ValueError):
        bait.transform_rewards([[1.0, 2.0]], mask)


def test_bait_nonfinite_rewards_rejected():
    with pytest.raises(ValueError):
        bait.transform_rewards([[np.inf, 1.0]], [[True, False]])


@pytest.mark.parametrize("seed", [42, 43, 44])
@pytest.mark.parametrize("module", [lgpo, budget, bait])
def test_cpu_diagnostics(module, seed):
    payload = module.diagnostic(seed, device="cpu")
    assert payload["diagnostic_only"] and payload["evaluation_tier"] == "l1_mechanism"
    assert all(payload["checks"].values())
    assert all(np.isfinite(value) for value in payload["metrics"].values())


def test_gpu_gate_is_explicit_and_only_for_torch_loss():
    assert lgpo.REQUIRES_GPU_VALIDATION is True
    assert budget.REQUIRES_GPU_VALIDATION is False
    assert bait.REQUIRES_GPU_VALIDATION is False
