import math

import pytest
import torch

from auto_research.foundation_models import stochastic_rounding as sr


@pytest.mark.parametrize("seed", [42, 43, 44])
def test_diagnostic(seed):
    result = sr.diagnostic(seed)
    assert result["diagnostic_only"] is True
    assert result["evaluation_tier"] == "l1_mechanism"
    assert all(result["checks"].values())
    assert all(math.isfinite(value) for value in result["metrics"].values())


@pytest.mark.parametrize("dtype", [torch.float16, torch.bfloat16])
def test_adjacent_brackets_negative_zero_subnormal_and_maximum(dtype):
    tiny = float(torch.nextafter(torch.tensor(0., dtype=dtype), torch.tensor(1., dtype=dtype)))
    values = torch.tensor([-torch.finfo(dtype).max, -1.003, -tiny * .25, -0., 0., tiny * .25, 1.003, torch.finfo(dtype).max], dtype=torch.float32)
    lower, upper = sr.adjacent_values(values, dtype)
    assert torch.all(lower <= values) and torch.all(values <= upper)
    assert torch.isfinite(lower).all() and torch.isfinite(upper).all()
    assert torch.equal(lower.to(dtype).float(), lower)
    assert torch.equal(upper.to(dtype).float(), upper)
    exact = lower == upper
    assert torch.all((torch.nextafter(lower.to(dtype), torch.full_like(lower, torch.inf).to(dtype)).float() == upper) | exact)


def test_stochastic_cast_seeded_outputs_and_expectation_both_signs():
    values = torch.tensor([1.0009765625, -1.0009765625], dtype=torch.float32).repeat(50000, 1)
    first = sr.stochastic_cast(values, torch.bfloat16, generator=torch.Generator().manual_seed(7))
    second = sr.stochastic_cast(values, torch.bfloat16, generator=torch.Generator().manual_seed(7))
    assert torch.equal(first, second)
    assert torch.max(torch.abs(first.double().mean(0) - values[0].double())) < 7e-5
    assert (first.float() != values.to(torch.bfloat16).float()).any()


def test_exact_representables_and_no_straight_through_gradient():
    values = torch.tensor([-2., -0., 0., 1., 8.], requires_grad=True)
    result = sr.stochastic_cast(values, torch.bfloat16, generator=torch.Generator().manual_seed(5))
    assert torch.equal(result.float(), values.detach())
    assert result.requires_grad is False


@pytest.mark.parametrize("values,dtype", [(torch.tensor([float("nan")]), torch.bfloat16), (torch.tensor([1e6]), torch.float16), (torch.tensor([1.], dtype=torch.float64), torch.bfloat16), (torch.tensor([1.]), torch.float32)])
def test_invalid_or_out_of_range_is_not_silently_clipped(values, dtype):
    with pytest.raises(ValueError):
        sr.adjacent_values(values, dtype)


def test_device_alias_resolution_does_not_assume_gpu_zero(monkeypatch):
    monkeypatch.setattr(torch.cuda, "current_device", lambda: 1)
    assert sr._device_identity(torch.device("cuda")) == ("cuda", 1)
    assert sr._device_identity(torch.device("cuda:1")) == ("cuda", 1)
    assert sr._device_identity(torch.device("cuda:0")) != sr._device_identity(torch.device("cuda"))
    assert sr._device_identity(torch.device("cpu:0")) == sr._device_identity(torch.device("cpu"))
    assert sr._device_identity(torch.device("cpu")) != sr._device_identity(torch.device("cuda"))


@pytest.mark.skipif(not torch.cuda.is_available(), reason="real CUDA required")
@pytest.mark.parametrize("device", ["cuda", "cuda:0"])
def test_real_cuda_alias_and_concrete_generator(device):
    with torch.cuda.device(0):
        values = torch.tensor([1.0009765625, -1.0009765625], device=device)
        for generator_device in (torch.device("cuda"), values.device):
            result = sr.stochastic_cast(values, torch.bfloat16,
                                        generator=torch.Generator(device=generator_device).manual_seed(42))
            assert result.device == values.device
            assert torch.isfinite(result).all()
        with pytest.raises(ValueError, match="same device"):
            sr.stochastic_cast(values, torch.bfloat16, generator=torch.Generator().manual_seed(42))


@pytest.mark.skipif(torch.cuda.device_count() < 2, reason="two actual CUDA devices required")
def test_real_cuda_different_gpu_is_rejected():
    values = torch.tensor([1.0009765625], device="cuda:0")
    generator = torch.Generator(device="cuda:1").manual_seed(42)
    with pytest.raises(ValueError, match="same device"):
        sr.stochastic_cast(values, torch.bfloat16, generator=generator)
