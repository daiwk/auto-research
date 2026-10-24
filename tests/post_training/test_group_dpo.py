"""Exact whole-group coefficients, microbatch replay and optimizer equivalence."""
from copy import deepcopy
import math

import pytest
import torch
from torch.nn import functional as F

from auto_research.post_training import group_dpo as gd


GROUPS = (gd.PreferenceGroup((0, 1), (2,)), gd.PreferenceGroup((0,), (3, 4, 5)))


def _oracle(u, groups, objective):
    losses = []
    for group in groups:
        p, n = [u[i] for i in group.positive], [u[i] for i in group.negative]
        if objective == "margin":
            loss = -F.logsigmoid(sum(p) / len(p) - sum(n) / len(n))
        elif objective == "mpo":
            values = torch.stack(p + n)
            loss = -values.log_softmax(0)[:len(p)].logsumexp(0)
        elif objective == "softmax":
            loss = sum(-F.logsigmoid(x - torch.stack(n).logsumexp(0)) for x in p) / len(p)
        else:
            loss = sum(-F.logsigmoid(x - y) for x in p for y in n) / (len(p) * len(n))
        losses.append(loss)
    return sum(losses) / len(groups)


@pytest.mark.parametrize("objective", gd.OBJECTIVES)
def test_coefficients_equal_independent_gradient_with_unequal_and_overlapping_groups(objective):
    u = torch.tensor([.2, -.5, .9, -.1, .8, -.4], dtype=torch.float64, requires_grad=True)
    expected = _oracle(u, GROUPS, objective)
    torch.testing.assert_close(gd.group_objective(u, GROUPS, objective), expected)
    coeff = gd.precompute_coefficients(u, GROUPS, objective)
    torch.testing.assert_close(coeff, torch.autograd.grad(expected, u)[0], rtol=1e-12, atol=1e-14)
    assert not coeff.requires_grad and abs(coeff.sum().item()) < 1e-14
    # Group 0's positive is weighted by 1/2 positives; overlapping response 0
    # also receives group 1's positive mass. NOT a flat positive average.
    torch.testing.assert_close(gd.positive_nll_weights(u, GROUPS),
                               torch.tensor([.75, .25, 0., 0., 0., 0.], dtype=u.dtype))


@pytest.mark.parametrize("objective", gd.OBJECTIVES)
@pytest.mark.parametrize("microbatch", [1, 2, 4, 6])
@pytest.mark.parametrize("optimizer_type", [torch.optim.SGD, torch.optim.AdamW])
def test_streamed_backward_matches_joint_over_multiple_optimizer_updates(objective, microbatch, optimizer_type):
    with torch.random.fork_rng():
        torch.manual_seed(3)
        features = torch.randn(6, 3, dtype=torch.float64)
        model = torch.nn.Linear(3, 4).double()
    streamed = deepcopy(model)
    labels = torch.tensor([0, 3, 1, 2, 1, 0])
    reference = torch.tensor([-1., -2., -.3, -.7, -.2, -1.5], dtype=torch.float64, requires_grad=True)
    optimizers = [optimizer_type(m.parameters(), lr=.03) for m in (model, streamed)]
    forward_sizes = []
    for _ in range(4):
        for opt in optimizers:
            opt.zero_grad(set_to_none=True)
        policy = model(features).log_softmax(-1)[torch.arange(6), labels]
        loss = _oracle(1.7 * (policy - reference.detach()), GROUPS, objective) - .4 * (.75 * policy[0] + .25 * policy[1])
        loss.backward()

        def score(indices):
            forward_sizes.append((len(indices), torch.is_grad_enabled()))
            return streamed(features[indices]).log_softmax(-1)[torch.arange(len(indices)), labels[indices]]

        audit = gd.backward_microbatched(score, reference, GROUPS, objective=objective,
                                        beta=1.7, nll_coef=.4, microbatch_size=microbatch)
        assert audit["objective_value"] == pytest.approx(float(loss.detach()), abs=1e-12)
        assert audit["max_forward_microbatch"] <= microbatch
        assert audit["coefficients_detached"] and audit["reference_detached"]
        for left, right in zip(model.parameters(), streamed.parameters()):
            torch.testing.assert_close(left.grad, right.grad, rtol=1e-11, atol=1e-13)
        for opt in optimizers:
            opt.step()
        for left, right in zip(model.parameters(), streamed.parameters()):
            torch.testing.assert_close(left, right, rtol=1e-11, atol=1e-13)
    assert reference.grad is None
    assert max(n for n, _ in forward_sizes) <= microbatch
    assert any(not grad for _, grad in forward_sizes) and any(grad for _, grad in forward_sizes)


def test_first_order_only_stale_coefficients_and_local_group_normalization_are_wrong():
    u = torch.tensor([.2, -.5, .9, -.1, .8, -.4], dtype=torch.float64, requires_grad=True)
    coefficients = gd.precompute_coefficients(u, GROUPS)
    original = _oracle(u, GROUPS, "all_pairs")
    surrogate = (coefficients * u).sum()
    assert abs(float((original - surrogate).detach())) > .1  # NOT a value-preserving surrogate.
    moved = (u.detach() + torch.tensor([2., 0., -2., 1., -.5, .8])).requires_grad_()
    new_grad = torch.autograd.grad(_oracle(moved, GROUPS, "all_pairs"), moved)[0]
    assert (new_grad - coefficients).abs().max() > .05  # Must refresh every update.
    local_only = gd.precompute_coefficients(u[:3], (GROUPS[0],))
    # It ignores group 1's contribution at shared response 0 and the global /2.
    assert (local_only - coefficients[:3]).abs().max() > .02


@pytest.mark.parametrize("objective", gd.OBJECTIVES)
def test_extreme_scores_and_half_precision_remain_finite(objective):
    values = torch.tensor([-10000., -9999., 10000., 9999., -10000., 0.], requires_grad=True)
    coeff = gd.precompute_coefficients(values, GROUPS, objective)
    # The independent log-softmax oracle subtracts values around +/-10000;
    # evaluate it in float64 so its own cancellation is not our error budget.
    expected = torch.autograd.grad(_oracle(values.double(), GROUPS, objective), values)[0]
    assert coeff.isfinite().all()
    torch.testing.assert_close(coeff, expected, rtol=1e-5, atol=1e-7)
    half = gd.precompute_coefficients(values.half(), GROUPS, objective)
    assert half.dtype == torch.float32 and half.isfinite().all()


def test_replay_rejects_stochastic_or_changed_state_before_optimizer_step():
    parameter = torch.nn.Parameter(torch.arange(6, dtype=torch.float64))
    calls = 0

    def score(indices):
        nonlocal calls
        calls += 1
        return parameter[indices] + (.1 if torch.is_grad_enabled() else 0.)

    with pytest.raises(ValueError, match="replay changed"):
        gd.backward_microbatched(score, torch.zeros(6), GROUPS)
    assert parameter.grad is None and calls == 7  # six no-grad reads, first replay rejected.


@pytest.mark.parametrize("groups", [(), (gd.PreferenceGroup((), (0,)),),
    (gd.PreferenceGroup((0,), (0, 1)),), (gd.PreferenceGroup((0,), (6,)),),
    (gd.PreferenceGroup((0,), (1,)),)])
def test_invalid_or_incomplete_groups_rejected(groups):
    with pytest.raises(ValueError):
        gd.precompute_coefficients(torch.zeros(6), groups)


@pytest.mark.parametrize("kwargs", [{"beta": 0}, {"beta": math.inf}, {"nll_coef": -1},
                                   {"microbatch_size": 0}, {"microbatch_size": True}])
def test_invalid_backward_arguments_rejected(kwargs):
    with pytest.raises(ValueError):
        gd.backward_microbatched(lambda indices: torch.zeros(len(indices)), torch.zeros(6), GROUPS, **kwargs)


def test_diagnostic_has_real_updates_and_no_capability_metrics():
    record = gd.diagnostic(42)
    assert all(record["checks"].values())
    assert record["metrics"]["surrogate_optimizer_updates"] == 24
    assert not any("accuracy" in name or "success" in name for name in record["metrics"])
