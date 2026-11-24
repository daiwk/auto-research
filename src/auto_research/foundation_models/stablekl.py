"""StableKL fixed-v1 Exponential Rewrite core, FP32 CPU only.

Section4/B.1/B.4, not the complete upstream package: no strict/certified
rounding, extreme-range mantissa arithmetic, other18-family sweep, F.kl_div
or logits path. First-order analytic autograd gradients are supplied.
"""

from decimal import Decimal, localcontext
import math

import torch
from torch.autograd.function import once_differentiable

REQUIRES_GPU_VALIDATION = False


def _validate(a, b):
    if (not isinstance(a, torch.Tensor) or not isinstance(b, torch.Tensor)
            or a.dtype != torch.float32 or b.dtype != a.dtype
            or a.device.type != "cpu" or b.device != a.device
            or a.shape != b.shape or not a.numel()
            or not torch.isfinite(a).all() or not torch.isfinite(b).all()
            or not (a > 0).all() or not (b > 0).all()):
        raise ValueError("matched nonempty finite positive FP32 CPU rates required")
    x, ratio = (b - a) / a, b / a
    if not torch.isfinite(x).all() or not torch.isfinite(ratio).all() or not (ratio > 0).all():
        raise ValueError("extreme/underflowing rate ratios are outside this component")


class _ExponentialKL(torch.autograd.Function):
    @staticmethod
    def forward(ctx, a, b):
        x = (b - a) / a
        inside = (x >= -.75) & (x <= 3.)
        xs = torch.where(inside, x, torch.zeros_like(x))
        denominator = 2. + xs
        s = xs / denominator
        z = s * s
        q = torch.full_like(x, 1. / 35.)  # K=17, coefficient1/(2K+1)
        for k in range(16, 0, -1):
            q = q * z + 1. / (2 * k + 1)
        series = xs * xs / denominator - 2. * (s * z) * q
        above = x > 3.
        log = torch.where(above, torch.log1p(torch.where(above, x, torch.zeros_like(x))),
                          torch.log(b / a))
        value = torch.where(inside, series, x - log).clamp_min(0.)
        zero = torch.zeros_like(x)
        gp, gq = (zero - x) / a, x / b
        if not torch.isfinite(value).all() or not torch.isfinite(gp).all() or not torch.isfinite(gq).all():
            raise ValueError("nonfinite result/gradient is outside the ordinary-range component")
        ctx.save_for_backward(gp, gq)
        return value

    @staticmethod
    @once_differentiable
    def backward(ctx, incoming):
        gp, gq = ctx.saved_tensors
        return incoming * gp, incoming * gq


def exponential_kl(rate_p, rate_q):
    """KL(Exp(rate_p)||Exp(rate_q)), element-wise, no broadcasting/reduction."""
    _validate(rate_p, rate_q)
    return _ExponentialKL.apply(rate_p, rate_q)


def decimal_reference(rate_p, rate_q):
    """Independent 80-digit reference for stored scalar bit patterns, not a certificate."""
    with localcontext() as context:
        context.prec = 80
        a, b = Decimal.from_float(float(rate_p)), Decimal.from_float(float(rate_q))
        ratio = b / a
        return float(ratio - Decimal(1) - ratio.ln())


def diagnostic(seed=42, device="cpu"):
    if type(seed) is not int or device != "cpu":
        raise ValueError("integer seed and CPU-only device required")
    generator = torch.Generator().manual_seed(seed)
    p = torch.ones(32, requires_grad=True)
    q = (1. + torch.randint(1, 9, (32,), generator=generator) * torch.finfo(torch.float32).eps).requires_grad_()
    value = exponential_kl(p, q)
    value.sum().backward()
    reference = torch.tensor([decimal_reference(a, b) for a, b in zip(p.detach(), q.detach(), strict=True)], dtype=torch.float64)
    ratio = q.detach() / p.detach()
    official_formula = -ratio.log() + ratio - 1.
    relative = ((value.double() - reference).abs() / reference).max().item()
    a, b = torch.ones(4, requires_grad=True), torch.ones(4, requires_grad=True)
    identity = exponential_kl(a, b)
    identity.sum().backward()
    checks = {
        "nearby_distinct_rates_have_positive_kl": bool((value > 0).all()),
        "rewrite_agrees_with_decimal_reference": relative < 2e-6,
        "clamping_cannot_recover_naive_spurious_zeros": bool((official_formula.clamp_min(0) == 0).all()),
        "analytic_rate_gradients_match_stored_input_reference": bool(torch.allclose(p.grad.double(), (p.detach().double()-q.detach().double())/p.detach().double().square(), rtol=2e-6, atol=0) and torch.allclose(q.grad.double(), (q.detach().double()-p.detach().double())/(p.detach().double()*q.detach().double()), rtol=2e-6, atol=0)),
        "identity_value_and_first_gradients_are_exact_positive_zero": bool(torch.count_nonzero(identity) == 0 and torch.count_nonzero(a.grad) == 0 and torch.count_nonzero(b.grad) == 0 and not torch.signbit(identity).any() and not torch.signbit(a.grad).any() and not torch.signbit(b.grad).any()),
    }
    metrics = {"max_relative_error_vs_decimal": float(relative),
               "min_positive_synthetic_kl": float(value.min().item()),
               "naive_zero_fraction": float((official_formula == 0).float().mean().item())}
    if not all(math.isfinite(x) for x in metrics.values()):
        raise ValueError("nonfinite diagnostic metric")
    return {"seed": seed, "device": device, "evaluation_tier": "l1_mechanism",
            "diagnostic_only": True, "checks": checks, "metrics": metrics}
