import math

import pytest
import torch

from auto_research.foundation_models.aimuon import diagnostic, direction, ns5, step_matrix


@pytest.mark.parametrize("seed", [42, 43, 44])
def test_real_matrix_diagnostic(seed):
    assert all(diagnostic(seed)["checks"].values())


def test_ns_transposes_and_uses_five_fixed_polynomial_steps():
    g = torch.Generator().manual_seed(4)
    x = torch.randn(9, 4, generator=g)
    reference = x.to(torch.bfloat16).T
    reference /= reference.norm().clamp_min(1e-7)
    for _ in range(5):
        gram = reference @ reference.T
        reference = 3.4445 * reference + (-4.7750 * gram + 2.0315 * (gram @ gram)) @ reference
    assert torch.equal(ns5(x), reference.T.float())
    assert torch.equal(ns5(torch.zeros_like(x)), torch.zeros_like(x))


def test_ema_is_not_bias_corrected_or_nesterov_and_decay_is_decoupled():
    p = torch.ones(3, 2)
    g = torch.tensor([[1., 2.], [2., 3.], [-1., 4.]])
    previous = torch.zeros_like(g)
    result, state = step_matrix(p, g, previous, lr=.02, beta=.8, weight_decay=.1)
    assert torch.allclose(state, .2*g)
    assert torch.allclose(result, .998*p-.02*direction(g, state))
    assert torch.equal(previous, torch.zeros_like(g))


def test_small_gradient_uses_paper_epsilon_not_adamw_epsilon():
    generator = torch.Generator().manual_seed(7)
    gradient = torch.randn(8, 12, generator=generator)*1e-9
    momentum = torch.randn(8, 12, generator=generator)*1e-9
    dm, de = ns5(momentum), ns5(gradient-momentum)
    nm = (momentum*dm).sum().abs()
    ne = ((gradient-momentum)*de).sum().abs()
    combined = nm*(dm+ne/(nm+1e-12)*de)
    expected = .2*math.sqrt(12)*dm.norm()*combined/(combined.norm()+1e-12)
    actual = direction(gradient, momentum)
    assert torch.allclose(actual, expected, rtol=1e-6, atol=1e-7)
    assert not torch.allclose(actual, direction(gradient, momentum, epsilon=1e-8))


def test_rms_preserves_relative_residual_weights_not_final_polar_structure():
    g = torch.Generator().manual_seed(8)
    gradient, momentum = torch.randn(5, 7, generator=g), torch.randn(5, 7, generator=g)
    a, b = direction(gradient, momentum, correction=.1), direction(gradient, momentum, correction=2.)
    assert not torch.allclose(a, b)
    expected = .2*math.sqrt(7)*ns5(momentum).norm()
    assert torch.allclose(a.norm(), expected, rtol=2e-5)
    assert torch.allclose(b.norm(), expected, rtol=2e-5)


@pytest.mark.parametrize("kw", [{"beta": 1}, {"lr": -1}, {"correction": -1}, {"epsilon": 0}, {"weight_decay": math.inf}])
def test_invalid_hyperparameters_rejected(kw):
    x = torch.ones(2, 3)
    with pytest.raises(ValueError):
        step_matrix(x, x, torch.zeros_like(x), **kw)


def test_nonfinite_and_nonmatrix_rejected():
    with pytest.raises(ValueError):
        ns5(torch.ones(3))
    with pytest.raises(ValueError):
        ns5(torch.tensor([[math.nan]]))
    with pytest.raises(ValueError):
        direction(torch.ones(2, 3), torch.ones(3, 2))
    with pytest.raises(ValueError):
        ns5(torch.full((2, 2), 1e100, dtype=torch.float64))
