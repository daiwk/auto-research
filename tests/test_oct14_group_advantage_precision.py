"""Reward-centering numerical contracts; these fixtures are not GPU evidence."""
import math

import pytest
import torch

from auto_research.post_training.oct13_common import CostLedger, centered_advantages, policy_gradient_step
from auto_research.post_training.response_policy import GeneratedResponse


@pytest.mark.parametrize("reward", [0.2, 1.2, 0.3, -0.2])
@pytest.mark.parametrize("size", [7, 8, 9])
@pytest.mark.parametrize("normalize", [False, True])
def test_identical_rewards_have_exactly_zero_advantages(reward, size, normalize):
    advantages = centered_advantages([reward] * size, normalize_std=normalize)
    assert torch.equal(advantages, torch.zeros(size, dtype=advantages.dtype))


@pytest.mark.parametrize("normalize", [False, True])
@pytest.mark.parametrize("reward", [0.2, 1.2])
def test_identical_reward_group_cannot_score_or_update_policy(reward, normalize):
    class Policy:
        device = "cpu"

    class ForbiddenLedger:
        def score(self, *args, **kwargs):
            raise AssertionError("zero-information group must not enter policy scoring")

    result = policy_gradient_step(Policy(), [None] * 8, [reward] * 8, ForbiddenLedger(),
                                  normalize_std=normalize)
    assert result["optimizer_update_executed"] is False
    assert result["zero_advantage_group"] is True
    assert result["rewards"] == [reward] * 8


@pytest.mark.parametrize("rewards", [[0.2, 1.2] * 4, [0.2, 0.2, 1.2],
                                     [100000000.0, 100000001.0]])
def test_real_reward_differences_are_preserved_and_centered(rewards):
    expected = torch.tensor([r - math.fsum(rewards) / len(rewards) for r in rewards], dtype=torch.float32)
    actual = centered_advantages(rewards)
    torch.testing.assert_close(actual, expected, rtol=1e-6, atol=1e-7)
    assert bool(actual.abs().sum())


def test_std_normalization_preserves_real_signal_without_fp32_offset_cancellation():
    actual = centered_advantages([100000000.0, 100000001.0], normalize_std=True)
    torch.testing.assert_close(actual, torch.tensor([-0.5, 0.5]) / (0.5 + 1e-6))


@pytest.mark.parametrize("normalize", [False, True])
def test_decimal_reward_difference_produces_gradient_and_parameter_update(normalize):
    class Model(torch.nn.Module):
        def __init__(self):
            super().__init__()
            self.weight = torch.nn.Parameter(torch.tensor(0.))

    class Policy:
        device = "cpu"

        def __init__(self):
            self.model = Model()
            self.optimizer = torch.optim.SGD(self.model.parameters(), lr=0.1)

        def token_statistics(self, messages, tokens):
            return -1 + self.model.weight * torch.tensor(tokens, dtype=torch.float32), None

    policy, ledger = Policy(), CostLedger()
    group = [([{"role": "user", "content": "CPU fixture question only"}],
              GeneratedResponse((token,), "CPU fixture response", False)) for token in (1, 2)]
    old = [torch.tensor([-1.]), torch.tensor([-1.])]
    before = policy.model.weight.detach().clone()
    result = policy_gradient_step(policy, group, [0.2, 1.2], ledger,
                                  behavior_log_probs=old, normalize_std=normalize)
    assert result["optimizer_update_executed"] is True and result["gradient_l2_norm"] > 0
    assert not torch.equal(before, policy.model.weight)
    calls = dict(ledger.calls)
    before = policy.model.weight.detach().clone()
    skipped = policy_gradient_step(policy, group, [1.2, 1.2], ledger,
                                   behavior_log_probs=old, normalize_std=normalize)
    assert skipped["optimizer_update_executed"] is False
    assert torch.equal(before, policy.model.weight) and ledger.calls == calls


@pytest.mark.parametrize("rewards", [[1.], [float("nan"), 1.], [float("inf"), 1.],
                                     [[1., 2.], [3., 4.]], [-1e39, 1e39]])
def test_invalid_reward_groups_remain_rejected(rewards):
    with pytest.raises(ValueError):
        centered_advantages(rewards)


def test_normalization_overflow_cannot_masquerade_as_zero_information():
    with pytest.raises(ValueError, match="finite reward dispersion"):
        centered_advantages([-1e200, 1e200], normalize_std=True)
