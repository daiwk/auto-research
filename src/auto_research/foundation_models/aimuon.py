"""AIMuon Algorithm 1 matrix update; no pretrained model or training campaign.

Five BF16 Newton--Schulz iterations are the paper's practical approximation,
not its exact polar-factor stationarity theorem. Matrix parameters only.
"""

from __future__ import annotations

import math

import torch

REQUIRES_GPU_VALIDATION = True


def _matrix(value):
    if value.ndim != 2 or not value.is_floating_point() or not torch.isfinite(value).all():
        raise ValueError("a finite floating-point matrix is required")


def ns5(value):
    """Appendix C's five-step BF16 polar approximation, including transpose."""
    _matrix(value)
    x = value.to(torch.bfloat16)
    if not torch.isfinite(x).all():
        raise ValueError("matrix exceeds the paper's BF16 execution range")
    transpose = x.shape[0] > x.shape[1]
    if transpose:
        x = x.T
    norm = x.norm()
    if not torch.isfinite(norm):
        raise ValueError("BF16 normalization overflows")
    x = x / norm.clamp_min(1e-7)
    for _ in range(5):
        a = x @ x.T
        b = -4.7750 * a + 2.0315 * (a @ a)
        x = 3.4445 * x + b @ x
    if not torch.isfinite(x).all():
        raise ValueError("nonfinite Newton--Schulz result")
    return (x.T if transpose else x).to(value.dtype)


def direction(gradient, momentum, *, correction=1.0, epsilon=1e-12):
    """Separate transforms, Eq19 estimates, then Eq20--21 RMS matching."""
    _matrix(gradient)
    _matrix(momentum)
    if gradient.shape != momentum.shape or gradient.device != momentum.device:
        raise ValueError("gradient and updated momentum must match")
    if not math.isfinite(correction) or correction < 0 or not math.isfinite(epsilon) or epsilon <= 0:
        raise ValueError("finite nonnegative correction and positive epsilon required")
    residual = gradient - momentum
    dm, de = ns5(momentum), ns5(residual)
    nm = (momentum.float() * dm.float()).sum().abs()
    ne = (residual.float() * de.float()).sum().abs()
    weight = correction * ne / (nm + epsilon)
    combined = nm * (dm.float() + weight * de.float())
    scale = 0.2 * math.sqrt(max(gradient.shape))
    update = scale * dm.float().norm() * combined / (combined.norm() + epsilon)
    if not torch.isfinite(update).all():
        raise ValueError("nonfinite spectral update")
    return update.to(gradient.dtype)


def step_matrix(parameter, gradient, previous_momentum, *, lr=0.01, beta=0.95,
                correction=1.0, weight_decay=0.0, epsilon=1e-12):
    """Functional matrix-only Algorithm 1; no bias correction or Nesterov."""
    for value in (parameter, gradient, previous_momentum):
        _matrix(value)
    if any(x.shape != parameter.shape or x.device != parameter.device for x in (gradient, previous_momentum)):
        raise ValueError("matrix shapes/devices must match")
    if (not math.isfinite(beta) or not 0 <= beta < 1
            or not math.isfinite(lr) or lr < 0
            or not math.isfinite(weight_decay) or weight_decay < 0):
        raise ValueError("invalid EMA, learning rate or weight decay")
    momentum = beta * previous_momentum + (1 - beta) * gradient
    update = direction(gradient, momentum, correction=correction, epsilon=epsilon)
    result = (1 - lr * weight_decay) * parameter - lr * update
    if not torch.isfinite(result).all():
        raise ValueError("nonfinite parameter update")
    return result, momentum


def diagnostic(seed=42, device="cpu"):
    if device not in {"cpu", "cuda"}:
        raise ValueError("cpu or cuda required")
    generator = torch.Generator(device="cpu").manual_seed(seed)
    gradient = torch.randn(8, 12, generator=generator).to(device)
    momentum = torch.randn(8, 12, generator=generator).to(device)
    update = direction(gradient, momentum)
    muon = 0.2 * math.sqrt(12) * ns5(momentum)
    mixed = ns5(momentum + gradient - momentum)
    mixed = mixed * update.norm() / mixed.norm().clamp_min(1e-8)
    zero = torch.zeros_like(gradient)
    target = torch.randn(8, 12, generator=generator).to(device)
    parameter, state = torch.zeros_like(target), torch.zeros_like(target)
    initial = float((parameter - target).square().mean().item())
    for _ in range(20):
        parameter = parameter.detach().requires_grad_(True)
        loss = (parameter - target).square().mean()
        grad, = torch.autograd.grad(loss, parameter)
        with torch.no_grad():
            parameter, state = step_matrix(parameter, grad, state, lr=0.05)
    final = float((parameter - target).square().mean().item())
    no_residual = direction(gradient, momentum, correction=0)
    return {
        "seed": seed, "diagnostic_only": True, "evaluation_tier": "l1_mechanism",
        "checks": {
            "actual_autograd_quadratic_decreases": final < initial,
            "separate_transforms_differ_from_pre_mixing": bool((update - mixed).norm().item() > 1e-3),
            "rms_matches_same_momentum_muon": bool(torch.allclose(update.norm(), muon.norm(), rtol=2e-5, atol=1e-6)),
            "zero_correction_recovers_muon": bool(torch.allclose(no_residual, muon, rtol=2e-5, atol=1e-6)),
            "zero_gradient_and_momentum_stay_zero": bool(torch.equal(direction(zero, zero), zero)),
            "transpose_path_retains_shape": ns5(gradient.T).shape == gradient.T.shape,
            "all_finite": bool(torch.isfinite(parameter).all()),
        },
        "metrics": {"initial_quadratic_loss": initial, "final_quadratic_loss": final,
                    "update_frobenius_norm": float(update.norm().item()),
                    "premix_direction_gap": float((update - mixed).norm().item())},
    }
