import math

import pytest
import torch

from auto_research.foundation_models.stablekl import decimal_reference, diagnostic, exponential_kl


@pytest.mark.parametrize("q", [.001, .25, .2501, .5, 1., 1.0001, 3.999, 4., 4.001, 1000.])
def test_three_branches_against_independent_high_precision_stored_input_reference(q):
    a, b = torch.tensor(1.), torch.tensor(q)
    actual = exponential_kl(a, b).item()
    reference = decimal_reference(a, b)
    assert actual == pytest.approx(reference, rel=2e-6, abs=1e-20)
    assert actual >= 0


def test_near_equality_spurious_zero_is_not_repaired_by_clamping():
    a, b = torch.tensor(1., requires_grad=True), torch.tensor(1.0001, requires_grad=True)
    ratio = b / a
    naive = (-ratio.log() + ratio - 1.).clamp_min(0.)
    stable = exponential_kl(a, b)
    assert naive.item() == 0. and stable.item() > 0
    stable.backward()
    stored_a, stored_b = a.detach().item(), b.detach().item()
    x = (stored_b - stored_a) / stored_a
    assert a.grad.item() == pytest.approx(-x / stored_a, rel=2e-6)
    assert b.grad.item() == pytest.approx(x / stored_b, rel=2e-6)


def test_identity_forward_and_analytic_backward_are_exact_positive_zero():
    a = torch.tensor([.5, 1., 2., 4.], requires_grad=True)
    b = a.detach().clone().requires_grad_()
    value = exponential_kl(a, b)
    value.sum().backward()
    for result in (value, a.grad, b.grad):
        assert torch.count_nonzero(result) == 0
        assert not torch.signbit(result).any()


def test_first_order_gradients_for_both_rate_parameters():
    a = torch.tensor([.5, 1., 4.], requires_grad=True)
    b = torch.tensor([2., 3., .25], requires_grad=True)
    incoming = torch.tensor([.5, -2., 3.])
    exponential_kl(a, b).backward(incoming)
    x = (b.detach().double() - a.detach().double()) / a.detach().double()
    torch.testing.assert_close(a.grad.double(), incoming.double() * -x / a.detach().double(), rtol=2e-6, atol=0)
    torch.testing.assert_close(b.grad.double(), incoming.double() * x / b.detach().double(), rtol=2e-6, atol=0)


def test_same_working_precision_output_no_silent_fp64_promotion():
    a, b = torch.tensor([1.]), torch.tensor([1.0001])
    result = exponential_kl(a, b)
    assert result.dtype == a.dtype == torch.float32
    assert result.device.type == "cpu"


@pytest.mark.parametrize("a,b", [(0., 1.), (-1., 1.), (1., math.inf), (math.nan, 1.),
                                (torch.finfo(torch.float32).tiny, torch.finfo(torch.float32).max)])
def test_invalid_or_extreme_rate_ranges_are_rejected(a, b):
    with pytest.raises(ValueError):
        exponential_kl(torch.tensor(a), torch.tensor(b))


def test_unadvertised_dtype_shapes_and_cuda_device_are_rejected():
    with pytest.raises(ValueError):
        exponential_kl(torch.ones(2, dtype=torch.float64), torch.ones(2, dtype=torch.float64))
    with pytest.raises(ValueError):
        exponential_kl(torch.ones(2), torch.ones(1))
    with pytest.raises(ValueError):
        exponential_kl(torch.tensor([]), torch.tensor([]))
    with pytest.raises(ValueError):
        diagnostic(42, "cuda")


@pytest.mark.parametrize("seed", [42, 43, 44])
def test_cpu_only_diagnostic(seed):
    result = diagnostic(seed)
    assert result["diagnostic_only"] and result["evaluation_tier"] == "l1_mechanism"
    assert result["checks"] and all(result["checks"].values())
    assert all(math.isfinite(value) for value in result["metrics"].values())
