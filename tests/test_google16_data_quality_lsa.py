import inspect

import pytest
import torch

from auto_research.foundation_models.google16_data_quality_lsa import (
    closest_sft_value, context_embedding, lsa_forward, outcome_supervision_loss,
    population_initialization, rollout, sft_loss,
)


def fixture():
    torch.manual_seed(8)
    x = torch.randn(6, 5, 3, dtype=torch.float64)
    weights = torch.randn(6, 3, dtype=torch.float64)
    y = (x @ weights[..., None]).squeeze(-1)
    covariance = torch.diag(torch.tensor([1., 2., 3.], dtype=torch.float64))
    value, query_key = population_initialization(covariance, 5)
    return x, y, weights, covariance, value, query_key


def test_lsa_matches_independently_ordered_matrix_contractions():
    x, y, _, _, value, query_key = fixture()
    z = context_embedding(x, y)
    expected = torch.stack([row + value @ row @ row.T @ query_key @ row / 5 for row in z])
    torch.testing.assert_close(lsa_forward(z, value, query_key, 5), expected)


def test_population_first_step_equals_preconditioned_empirical_covariance_weight():
    x, y, weights, _, value, query_key = fixture()
    predictions = rollout(x, y, value, query_key, 1)[:, 0]
    empirical_weight = (x.transpose(-2, -1) @ y[..., None]).squeeze(-1) / 5
    expected = -empirical_weight @ value[4:7, :3].T
    torch.testing.assert_close(predictions, expected)
    assert "training_weights" not in inspect.signature(rollout).parameters
    assert weights.shape == predictions.shape


def test_outcome_loss_only_compares_final_autonomous_step():
    x, y, weights, _, value, query_key = fixture()
    value, query_key = value.requires_grad_(), query_key.requires_grad_()
    actual = outcome_supervision_loss(x, y, weights, value, query_key, 3)
    expected = (rollout(x, y, value, query_key, 3)[:, -1] - weights).square().sum() / 12
    torch.testing.assert_close(actual, expected)
    actual.backward()
    assert value.grad.norm() > 0 and query_key.grad.norm() > 0


def test_teacher_forced_sft_k_zero_is_next_target_token_loss():
    x, y, weights, _, value, query_key = fixture()
    predicted = rollout(x, y, value, query_key, 1)[:, 0]
    actual = sft_loss(x, y, weights, value, query_key, k=0, rate=.3)
    torch.testing.assert_close(actual, (predicted - .3 * weights).square().sum() / 12)


def test_closed_form_solves_normal_equations_and_preserves_initial_nullspace():
    x, y, weights, covariance, value, _ = fixture()
    x, weights = x[:2], weights[:2]
    solution = closest_sft_value(x, weights, covariance, .3)
    phi = ((x.transpose(-2, -1) @ x / 5) @ weights[..., None]).squeeze(-1).T
    torch.testing.assert_close((solution @ phi + .3 * weights.T) @ phi.T, torch.zeros(3, 3, dtype=torch.float64), atol=1e-10, rtol=0)
    nullspace = torch.eye(3, dtype=torch.float64) - phi @ torch.linalg.pinv(phi)
    torch.testing.assert_close(solution @ nullspace, value[4:7, :3] @ nullspace)


def test_nonpositive_covariance_and_rollout_steps_rejected():
    with pytest.raises((ValueError, torch.linalg.LinAlgError)):
        population_initialization(torch.tensor([[1., 2.], [2., 1.]]), 4)
    x, y, _, _, value, query_key = fixture()
    with pytest.raises(ValueError):
        rollout(x, y, value, query_key, 0)
