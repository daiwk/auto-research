import pytest
import torch

from auto_research.post_training.learning_signals import (
    cross_fitted_occupancy, learning_signal_proxy, linear_cka, mean_pool_prompt,
    occupancy_surrogate, parameter_displacement, topk_residual,
)


def test_negative_truncated_loss_does_not_become_fake_positive_kl():
    s = torch.tensor([[[0., 0., 0.]]], requires_grad=True)
    t = torch.tensor([[[4., -4., -4.]]])
    loss = topk_residual(s, t, torch.ones(1, 1, dtype=torch.bool), topk=1)
    assert float(loss.detach()) < 0
    assert learning_signal_proxy(loss, 2.) is None
    assert learning_signal_proxy(2., 3.) == 2.25


def test_cross_fitted_estimator_uses_opposite_folds_and_keeps_invalid_denominator():
    scores = torch.tensor([[1., 2., 3., 4.]], requires_grad=True)
    losses = torch.tensor([[2., 4., 8., 10.]], requires_grad=True)
    h0, h1 = occupancy_surrogate(losses, scores)
    h0.backward(retain_graph=True)
    torch.testing.assert_close(scores.grad, torch.tensor([[-3.5, -2.5, 0., 0.]]))
    assert losses.grad is None
    assert cross_fitted_occupancy([torch.tensor([1.])], [torch.tensor([-1.])],
                                  [torch.tensor([2.])], [torch.tensor([3.])])["alpha"] is None
    result = cross_fitted_occupancy([torch.tensor([2.])], [torch.tensor([4.])],
                                    [torch.tensor([6.])], [torch.tensor([8.])])
    assert result["alpha"] == 2.5


def test_cka_centers_prompts_and_is_rotation_scale_invariant_not_identity_claim():
    torch.manual_seed(15)
    x = torch.randn(12, 4)
    q = torch.linalg.qr(torch.randn(4, 4))[0]
    assert linear_cka(x, 3 * x @ q + 10) == pytest.approx(1., abs=1e-6)
    assert linear_cka(torch.ones(12, 4), x) is None
    h = torch.tensor([[[1., 2.], [3., 4.], [999., 999.]]])
    torch.testing.assert_close(mean_pool_prompt(h, torch.tensor([[1, 1, 0]])), torch.tensor([[2., 3.]]))


def test_global_displacement_counts_tied_weights_once_not_mean_of_ratios():
    a, b = torch.ones(3), torch.ones(3) * 2
    result = parameter_displacement({"embed": a, "head": a}, {"embed": b, "head": b})
    assert result["unique_parameter_entries"] == 3
    assert result["relative_displacement"] == 1.
    with pytest.raises(ValueError, match="parameter space"):
        parameter_displacement({"a": a}, {"b": b})
