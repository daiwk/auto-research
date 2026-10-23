import math

import pytest
import torch

from auto_research.post_training.userarena_optd import diagnostic, optd_loss, trust_region_teacher


def inputs():
    torch.manual_seed(13)
    a = torch.randn(2, 3, 5, dtype=torch.float64, requires_grad=True)
    b = torch.randn_like(a, requires_grad=True)
    c = torch.randn_like(a, requires_grad=True)
    m = torch.tensor([[True, True, True], [True, False, False]])
    g = torch.randn(2, 4, 5, dtype=torch.float64, requires_grad=True)
    y = torch.tensor([[0, 1, 2, 3], [2, -1, -1, -1]])
    gm = torch.tensor([[True, True, True, True], [True, False, False, False]])
    return a, b, c, m, g, y, gm


def test_geometric_path_reference_and_largest_feasible_coefficient():
    _, base, intent, mask, *_ = inputs()
    result = trust_region_teacher(base, intent, mask, epsilon=.02)
    q0, qz = base.detach().softmax(-1), intent.detach().softmax(-1)
    coefficient = result["lambda"]
    expected = q0.pow(1 - coefficient[..., None]) * qz.pow(coefficient[..., None])
    expected /= expected.sum(-1, keepdim=True)
    torch.testing.assert_close(result["log_target"][mask].exp(), expected[mask])
    assert bool((result["kl_from_unconditioned"][mask] <= .02).all())
    # One grid cell above every non-endpoint feasible lower bound is infeasible.
    higher = (coefficient + 1 / 256).clamp_max(1)
    q = ((1 - higher[..., None]) * q0.log() + higher[..., None] * qz.log()).softmax(-1)
    kl = (q * (q.log() - q0.log())).sum(-1)
    assert bool((kl[mask & (coefficient < 1)] > .02).all())


def test_endpoints_and_zero_budget():
    _, base, intent, mask, *_ = inputs()
    full = trust_region_teacher(base, intent, mask, epsilon=100., lambda_max=.7)
    assert bool((full["lambda"][mask] == .7).all())
    zero = trust_region_teacher(base, intent, mask, epsilon=0.)
    torch.testing.assert_close(zero["log_target"][mask], base.detach().log_softmax(-1)[mask])
    same = trust_region_teacher(base, base, mask, epsilon=0.)
    assert bool((same["lambda"][mask] == 1).all())
    assert not full["log_target"].requires_grad


def test_per_state_means_and_independent_gradients():
    args = inputs()
    loss, audit = optd_loss(*args, beta=.3, gamma=.2)
    current, base, intent, mask, gt, gold, gm = args
    p, q = current.softmax(-1), audit["log_target"].exp()
    mixture = .3 * q + .7 * p
    jsd = .3 * (q * (q.log() - mixture.log())).sum(-1) + .7 * (p * (p.log() - mixture.log())).sum(-1)
    expected_dist = (jsd[0].mean() + jsd[1, 0]) / 2
    expected_gt = (-gt[0].log_softmax(-1)[torch.arange(4), gold[0]].mean() - gt[1, 0].log_softmax(-1)[gold[1, 0]]) / 2
    expected = expected_dist + .2 * expected_gt
    torch.testing.assert_close(loss, expected)
    grads = torch.autograd.grad(expected, (current, gt), retain_graph=True)
    loss.backward()
    torch.testing.assert_close(current.grad, grads[0])
    torch.testing.assert_close(gt.grad, grads[1])
    assert base.grad is intent.grad is None
    assert bool((current.grad[~mask] == 0).all())
    assert bool((gt.grad[~gm] == 0).all())
    assert not torch.isclose(expected_dist, jsd[mask].mean())


def test_padding_nan_ignored_but_active_nan_rejected():
    args = list(inputs())
    for index in (0, 1, 2):
        args[index] = args[index].detach().masked_fill(~args[3][..., None], float("nan"))
    args[4] = args[4].detach().masked_fill(~args[6][..., None], float("nan"))
    loss, _ = optd_loss(*args)
    assert loss.isfinite()
    args[0][0, 0, 0] = float("nan")
    with pytest.raises(ValueError, match="finite active"):
        optd_loss(*args)


@pytest.mark.parametrize("kwargs", [{"epsilon": -1}, {"epsilon": math.inf}, {"lambda_max": 1.1},
                                   {"bisection_steps": 0}, {"bisection_steps": True}])
def test_invalid_trust_configuration(kwargs):
    _, base, intent, mask, *_ = inputs()
    with pytest.raises(ValueError):
        trust_region_teacher(base, intent, mask, **kwargs)


@pytest.mark.parametrize("kwargs", [{"beta": 0}, {"beta": 1}, {"gamma": -1}, {"gamma": math.nan}])
def test_invalid_objective_configuration(kwargs):
    with pytest.raises(ValueError):
        optd_loss(*inputs(), **kwargs)


def test_empty_rows_invalid_targets_and_misaligned_teacher():
    args = list(inputs())
    args[3][1] = False
    with pytest.raises(ValueError, match="nonempty-per-state"):
        optd_loss(*args)
    args = list(inputs())
    args[5][0, 0] = 5
    with pytest.raises(ValueError, match="grounding targets"):
        optd_loss(*args)
    args = list(inputs())
    args[1] = args[1][:, :2]
    with pytest.raises(ValueError, match="same rollout"):
        optd_loss(*args)


def test_seeded_diagnostics():
    for seed in (42, 43, 44):
        result = diagnostic(seed)
        assert all(result["checks"].values())
        assert result["metrics"]["loss_after"] < result["metrics"]["loss_before"]


def test_finite_coefficient_that_overflows_compute_dtype_rejected():
    logits = torch.zeros(1, 1, 5, dtype=torch.float32)
    mask = torch.ones(1, 1, dtype=torch.bool)
    gold = torch.zeros(1, 1, dtype=torch.long)
    with pytest.raises(ValueError, match="representable"):
        optd_loss(logits, logits, logits, mask, logits, gold, mask, gamma=1e40)
