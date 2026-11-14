"""Unbiased FP32-to-BF16/FP16 stochastic rounding (2611.13545, Section 2).

The returned low-precision values are not a straight-through estimator or an
optimizer. Callers keep FP32 master weights and synchronize actual rounded
weights to rollout workers. No full RL experiment is reproduced here.
"""
from __future__ import annotations

import torch
from torch import Tensor

REQUIRES_GPU_VALIDATION = True
# A receipt at this path is not claimed passed until the integration owner's run.
GPU_VALIDATION_ARTIFACT = "docs/gpu-validations/stochastic-rounding-a100-20261111.json"


def _device_identity(device: torch.device) -> tuple[str, int | None]:
    """Resolve index-less CUDA aliases against the active device, not GPU zero.

    CPU indices are aliases, while explicit CUDA indices identify distinct
    accelerators. In particular, ``cuda`` is not necessarily ``cuda:0``.
    """
    if device.type == "cuda":
        return "cuda", torch.cuda.current_device() if device.index is None else device.index
    return device.type, None


def adjacent_values(values: Tensor, dtype: torch.dtype) -> tuple[Tensor, Tensor]:
    """Bracket finite FP32 values by representable finite target values.

    Out-of-range input is rejected rather than clipping (which would bias it).
    Negative numbers, signed zero and target-format subnormals are supported.
    """
    if values.dtype != torch.float32 or values.device.type not in {"cpu", "cuda"} or dtype not in {torch.bfloat16, torch.float16}:
        raise ValueError("FP32 CPU/CUDA tensor and BF16/FP16 target required")
    if not bool(torch.isfinite(values).all()) or bool((values.abs() > torch.finfo(dtype).max).any()):
        raise ValueError("finite input inside the target finite range required")
    nearest = values.to(dtype)
    down = torch.nextafter(nearest, torch.full_like(nearest, -torch.inf))
    up = torch.nextafter(nearest, torch.full_like(nearest, torch.inf))
    lower = torch.where(nearest.float() > values, down, nearest).float()
    upper = torch.where(nearest.float() < values, up, nearest).float()
    return lower, upper


@torch.no_grad()
def stochastic_cast(values: Tensor, dtype: torch.dtype, *, generator: torch.Generator) -> Tensor:
    """Round up with (x-lower)/(upper-lower); exact values stay exact."""
    if _device_identity(generator.device) != _device_identity(values.device):
        raise ValueError("generator and input must be on the same device")
    lower, upper = adjacent_values(values, dtype)
    exact = lower == upper
    # Float64 probability arithmetic avoids underflow for FP32 subnormals.
    gap = upper.double() - lower.double()
    probability = torch.where(exact, 0., (values.double() - lower.double()) / torch.where(exact, 1., gap))
    uniform = torch.rand(values.shape, dtype=torch.float64, device=values.device, generator=generator)
    return torch.where(uniform < probability, upper, lower).to(dtype)


def diagnostic(seed: int = 42, device: str = "cpu") -> dict:
    target = torch.device(device)
    if target.type not in {"cpu", "cuda"}:
        raise ValueError("CPU or CUDA device required")
    values = torch.full((65536,), 1. + 1. / 1024, dtype=torch.float32, device=target)
    # Tensor allocation resolves an index-less target to its concrete CUDA GPU.
    generator = torch.Generator(device=values.device).manual_seed(seed)
    rounded = stochastic_cast(values, torch.bfloat16, generator=generator).float()
    lower, upper = adjacent_values(values, torch.bfloat16)
    mean_error = float((rounded.double().mean() - values[0].double()).abs())
    expected_p = 1. / 8.
    standard_error = (1. / 128.) * (expected_p * (1 - expected_p) / values.numel()) ** .5
    negative = torch.tensor([-1.0009765625, -0., 0., 1.], dtype=torch.float32, device=target)
    lo, hi = adjacent_values(negative, torch.bfloat16)
    checks = {
        "all_outputs_are_adjacent": bool(((rounded == lower) | (rounded == upper)).all()),
        "empirical_mean_within_six_standard_errors": mean_error <= 6 * standard_error,
        "round_to_nearest_would_stick": bool((values.to(torch.bfloat16).float() == 1.).all()),
        "negative_and_zero_brackets_valid": bool(((lo <= negative) & (negative <= hi)).all()),
        "exact_values_stay_exact": bool(torch.equal(stochastic_cast(negative[1:], torch.bfloat16, generator=generator).float(), negative[1:])),
    }
    return {"seed": seed, "device": str(target), "diagnostic_only": True, "evaluation_tier": "l1_mechanism",
            "metrics": {"sr_mean_absolute_bias": mean_error, "sr_mean_standard_error": standard_error, "round_to_nearest_absolute_bias": float((values.to(torch.bfloat16).float().double().mean() - values[0].double()).abs()), "rounded_upper_fraction": float((rounded == upper).float().mean()), "samples": values.numel()}, "checks": checks}
