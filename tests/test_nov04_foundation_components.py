"""Independent formula checks for ProLand and GAVAGAI, no capability scores."""
import inspect
import math

import pytest
import torch

from auto_research.foundation_models import gavagai as ga
from auto_research.foundation_models import proland as pl


@pytest.mark.parametrize("module", [pl, ga])
@pytest.mark.parametrize("seed", [42, 43, 44])
def test_diagnostics(module, seed):
    result = module.diagnostic(seed, "cpu")
    assert result["diagnostic_only"] is True
    assert result["seed"] == seed
    assert all(type(value) is bool and value for value in result["checks"].values()), result
    assert all(type(value) in (int, float) and math.isfinite(value) for value in result["metrics"].values())
    assert module.REQUIRES_GPU_VALIDATION is True


@pytest.mark.parametrize("rank_deficient", [False, True])
def test_proland_dense_algorithm_one_reference_and_momentum_reprojection(rank_deficient):
    torch.manual_seed(3)
    b, a = torch.randn(6, 2, dtype=torch.float64), torch.randn(2, 5, dtype=torch.float64)
    if rank_deficient:
        b[:, 1] = 2 * b[:, 0]
        a[1] = 3 * a[0]
    momentum, dense_h = None, torch.zeros(6, 5, dtype=b.dtype)
    # Verify arbitrary-rank exact realization at the rank-deficient point.
    # Repeated floating-point perturbations near a rank change make the exact
    # pseudoinverse ill-conditioned; that is not a stable rank-deficient oracle.
    for _ in range(1 if rank_deficient else 3):
        g = torch.randn_like(dense_h)
        pb, pa = b @ torch.linalg.pinv(b), torch.linalg.pinv(a) @ a
        projection = lambda z: pb @ z + z @ pa - pb @ z @ pa
        dense_h = .8 * projection(dense_h) + .2 * projection(g)
        j = .8 * dense_h + .2 * projection(g)
        u, s, vh = torch.linalg.svd(j, full_matrices=False)
        tol = torch.finfo(s.dtype).eps * max(j.shape) * s.max()
        y = (u * (s > tol)[None]) @ vh
        da = torch.linalg.pinv(b) @ y
        db = (torch.eye(6) - pb) @ y @ torch.linalg.pinv(a)
        expected_b = b - .003 * db - .001 * b @ (b.T @ b - torch.eye(2))
        expected_a = a - .003 * da
        new_b, new_a, momentum = pl.step(b, a, g @ a.T, b.T @ g, momentum,
                                        gamma=.003, beta=.8, rho=.001)
        assert torch.allclose(momentum.left @ momentum.right.T, dense_h, atol=1e-10, rtol=1e-10)
        assert torch.allclose(new_b, expected_b, atol=1e-10, rtol=1e-10)
        assert torch.allclose(new_a, expected_a, atol=1e-10, rtol=1e-10)
        assert torch.allclose(b.T @ db, torch.zeros(2, 2, dtype=b.dtype), atol=1e-9)
        assert torch.allclose(b @ da + db @ a, projection(y), atol=1e-9)
        b, a = new_b, new_a


def test_proland_real_autograd_gradients_and_simultaneous_landing():
    torch.manual_seed(7)
    b = torch.randn(5, 2, dtype=torch.float64, requires_grad=True)
    a = torch.randn(2, 4, dtype=torch.float64, requires_grad=True)
    target = torch.randn(5, 4, dtype=torch.float64)
    objective = (b @ a - target).square().mean()
    grad_b, grad_a = torch.autograd.grad(objective, (b, a))
    new_b, new_a, _ = pl.step(b, a, grad_b, grad_a, gamma=.01, rho=.001)
    assert not new_b.requires_grad and not new_a.requires_grad
    assert not torch.equal(b, new_b) and not torch.equal(a, new_a)
    zero_b, zero_a, _ = pl.step(b, a, torch.zeros_like(b), torch.zeros_like(a), rho=.03)
    assert torch.equal(zero_a, a)
    assert torch.allclose(zero_b, b - .03 * b @ (b.T @ b - torch.eye(2)))


def test_proland_zero_factors_and_zero_core_do_not_invent_polar_directions():
    b, a = torch.zeros(4, 2), torch.zeros(2, 3)
    nb, na, state = pl.step(b, a, torch.zeros_like(b), torch.zeros_like(a))
    assert torch.equal(nb, b) and torch.equal(na, a)
    assert torch.count_nonzero(state.left @ state.right.T) == 0


@pytest.mark.parametrize("bad", [-1., float("nan"), float("inf")])
def test_proland_configuration_rejection(bad):
    b, a = torch.ones(3, 1), torch.ones(1, 4)
    with pytest.raises(ValueError):
        pl.step(b, a, b, a, gamma=bad)
    with pytest.raises(ValueError):
        pl.step(b, a, b, a, rho=bad)


def test_gavagai_cap_inequality_not_balanced_column_equalities():
    cost = torch.tensor([[0., 2., 3.], [0., 1., 4.]], dtype=torch.float64)
    capacities = torch.tensor([.8, .7], dtype=cost.dtype)
    plan = ga.capped_transport(cost, capacities, iterations=512)
    assert torch.allclose(plan.sum(1), torch.ones(2, dtype=cost.dtype), atol=1e-12)
    # Visual columns need not spend their capacities. Nothing is uncapped.
    assert bool((plan[:, 1:].sum(0) < capacities / 2).all())
    assert float(plan[:, 0].sum()) > 1.9


def test_gavagai_independent_symmetric_active_cap_solution_and_permutation():
    cost = torch.tensor([[0., -.03], [0., -.03]], dtype=torch.float64)
    plan = ga.capped_transport(cost, cost.new_tensor([.5]), iterations=512)
    expected = cost.new_tensor([[.75, .25], [.75, .25]])
    assert torch.allclose(plan, expected, atol=1e-12)
    permutation = torch.tensor([1, 0])
    assert torch.allclose(ga.capped_transport(cost[permutation], cost.new_tensor([.5]), iterations=512), plan[permutation])


def test_gavagai_multiple_visual_caps_zero_cap_and_log_domain_extremes():
    cost = torch.tensor([[100., -100., 100.], [-100., 100., -100.]], dtype=torch.float64)
    capacity = cost.new_tensor([0., 1.2])
    plan = ga.capped_transport(cost, capacity)
    assert bool(torch.isfinite(plan).all())
    assert bool((plan[:, 1] == 0).all())
    assert bool((plan[:, 1:].sum(0) <= capacity + 1e-12).all())
    # A deliberately active, strongly preferred visual column does not converge
    # in a fixed eight iterations. The API must expose, not repair, this residual.
    slow_cost = cost.new_tensor([[0., -10.], [0., -10.]])
    slow = ga.capped_transport(slow_cost, cost.new_tensor([.5]))
    assert float((slow.sum(1) - 1).abs().max()) > 1e-3
    assert float(slow[:, 1].sum()) <= .5 + 1e-12


def test_gavagai_envelope_gradient_sum_and_no_plan_gradient():
    cost = torch.tensor([[.1, .2], [.3, .4]], dtype=torch.float64, requires_grad=True)
    plan = torch.tensor([[.8, .2], [.6, .4]], dtype=cost.dtype, requires_grad=True)
    ce = cost.new_tensor(.9, requires_grad=True)
    result = ga.alignment_objective(cost, plan, ce)
    expected = ce + .1 * (cost * plan.detach()).sum() + .01 * (.7 - .6)
    assert torch.allclose(result["total"], expected)
    result["total"].backward()
    assert torch.allclose(cost.grad, .1 * plan.detach())
    assert plan.grad is None and ce.grad.item() == 1
    assert not result["nothing_penalty"].requires_grad


def test_gavagai_real_embeddings_nothing_head_update_and_external_prior():
    torch.manual_seed(6)
    model = ga.ReferentialAlignment(4).double()
    words = torch.randn(3, 4, dtype=torch.float64, requires_grad=True)
    regions = torch.randn(2, 4, dtype=torch.float64, requires_grad=True)
    capacities = words.new_tensor([1.1, 1.1])
    old = model.nothing_head[0].weight.detach().clone()
    optimizer = torch.optim.SGD(model.parameters(), lr=.01)
    out = model(words, regions, capacities, words.new_tensor(.5), iterations=128)
    out["total"].backward()
    assert words.grad.abs().sum() > 0 and regions.grad.abs().sum() > 0
    assert model.nothing_head[0].weight.grad.abs().sum() > 0
    optimizer.step()
    assert not torch.equal(old, model.nothing_head[0].weight)
    assert not out["plan"].requires_grad
    assert "gold" not in inspect.signature(model.forward).parameters


@pytest.mark.parametrize("bad", [-1., float("nan"), float("inf")])
def test_gavagai_rejects_invalid_capacities_and_epsilon(bad):
    cost = torch.zeros(3, 2)
    with pytest.raises(ValueError):
        ga.capped_transport(cost, cost.new_tensor([bad]))
    with pytest.raises(ValueError):
        ga.capped_transport(cost, cost.new_ones(1), epsilon=bad)


def test_gavagai_rejects_wrong_shapes_nonfinite_and_zero_embeddings():
    with pytest.raises(ValueError):
        ga.capped_transport(torch.zeros(3, 1), torch.zeros(0))
    with pytest.raises(ValueError):
        ga.capped_transport(torch.zeros(3, 2), torch.ones(1), iterations=True)
    model = ga.ReferentialAlignment(2)
    with pytest.raises(ValueError, match="zero-norm"):
        model(torch.zeros(1, 2), torch.ones(2, 2), torch.ones(2), torch.tensor(1.))
