"""FM-Mamba v1 Eqs7–14: stable native 2D reference, not PSD fused kernels."""

from __future__ import annotations

import torch
from torch import Tensor

REQUIRES_GPU_VALIDATION = True
GPU_VALIDATION_ARTIFACT = "docs/gpu-validations/fm-mamba-a100-20261118-latest.json"


def coefficients(
    a1: Tensor, a2: Tensor, ratio: Tensor, delta1: Tensor, delta2: Tensor, margin: float = 0.1
) -> tuple[Tensor, Tensor, Tensor, Tensor, Tensor]:
    if (
        a1.ndim != 1
        or a2.shape != a1.shape
        or ratio.shape != a1.shape
        or delta1.shape != delta2.shape
        or not 0 < margin < 1
        or not all(bool(torch.isfinite(x).all()) for x in (a1, a2, ratio, delta1, delta2))
        or bool(((a1 >= 0) | (a2 >= 0) | (ratio >= 0) | (ratio == -2)).any())
        or bool(((delta1 <= 0) | (delta2 <= 0)).any())
    ):
        raise ValueError("negative diagonal rates, ratio<0 except -2, positive steps required")
    constrained = ratio < -2
    if bool(constrained.any()):
        logarithm = -torch.log1p(2 / ratio[constrained])
        bound1 = (logarithm / a2[constrained].abs()).min()
        bound2 = (logarithm / a1[constrained].abs()).min()
        delta1 = delta1.clamp(max=(1 - margin) * bound1)
        delta2 = delta2.clamp(max=(1 - margin) * bound2)
    d1, d2 = delta1[..., None], delta2[..., None]
    c1, c2 = (a2 * d1).exp(), (a1 * d2).exp()
    integral1, integral2 = torch.expm1(a2 * d1) / a2, torch.expm1(a1 * d2) / a1
    c0 = integral1 * integral2 * (a1 * a2 * (1 + ratio)) - c1 * c2
    return c1, c2, c0, delta1, delta2


def stable_frozen_coefficients(c1: Tensor, c2: Tensor, c0: Tensor) -> Tensor:
    """Paper's frozen-position criterion, NOT a global switched-field proof."""
    return (c2.abs() < 1) & ((c1 + c0).abs() < 1 - c2) & ((c1 - c0).abs() < 1 + c2)


def scan(
    injection: Tensor, c1: Tensor, c2: Tensor, c0: Tensor, *, wavefront: bool = True
) -> Tensor:
    if injection.ndim != 3 or any(x.shape != injection.shape for x in (c1, c2, c0)):
        raise ValueError("matching [height,width,state] tensors required")
    height, width, _ = injection.shape
    if min(height, width) < 1:
        raise ValueError("nonempty grid required")
    zero = torch.zeros_like(injection[0, 0])
    states = {}
    ordering = (
        [
            (i, d - i)
            for d in range(height + width - 1)
            for i in range(max(0, d - width + 1), min(height, d + 1))
        ]
        if wavefront
        else [(i, j) for i in range(height) for j in range(width)]
    )
    for i, j in ordering:
        states[i, j] = (
            c1[i, j] * states.get((i - 1, j), zero)
            + c2[i, j] * states.get((i, j - 1), zero)
            + c0[i, j] * states.get((i - 1, j - 1), zero)
            + injection[i, j]
        )
    return torch.stack([torch.stack([states[i, j] for j in range(width)]) for i in range(height)])


def diagnostic(seed: int, device: str = "cpu") -> dict:
    torch.manual_seed(seed)
    a1 = torch.tensor([-1.0, -2.0], dtype=torch.float64, device=device)
    a2 = torch.tensor([-0.7, -1.3], dtype=torch.float64, device=device)
    ratio = torch.tensor([-3.0, -1.0], dtype=torch.float64, device=device)
    delta = torch.full((4, 5), 4.0, dtype=torch.float64, device=device)
    c1, c2, c0, bounded1, _ = coefficients(a1, a2, ratio, delta, delta)
    injected = torch.randn(4, 5, 2, dtype=torch.float64, device=device, requires_grad=True)
    parallel = scan(injected, c1, c2, c0)
    serial = scan(injected, c1, c2, c0, wavefront=False)
    without_diagonal = scan(injected, c1, c2, torch.zeros_like(c0))
    parallel.square().sum().backward()
    return {
        "seed": seed,
        "diagnostic_only": True,
        "evaluation_tier": "l1_mechanism",
        "metrics": {
            "wavefront_max_error": float((parallel - serial).abs().max().detach()),
            "projected_max_step": float(bounded1.max()),
        },
        "checks": {
            "wavefront_matches_serial": bool(torch.equal(parallel, serial)),
            "strict_frozen_position_stability": bool(stable_frozen_coefficients(c1, c2, c0).all()),
            "diagonal_predecessor_not_dropped": bool(
                not torch.allclose(parallel, without_diagonal)
            ),
            "recurrence_has_gradient": bool(
                injected.grad is not None and injected.grad.abs().sum() > 0
            ),
        },
    }
