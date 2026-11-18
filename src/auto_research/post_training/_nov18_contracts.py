"""Validation helpers for the source-bound Nov 18 component batch."""

from __future__ import annotations

import math
import torch


def scalar(value, name, *, lower=None, upper=None, strict_lower=False):
    if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value):
        raise ValueError(f"{name}: finite real scalar required")
    if lower is not None and (value <= lower if strict_lower else value < lower):
        raise ValueError(f"{name}: lower bound violated")
    if upper is not None and value > upper:
        raise ValueError(f"{name}: upper bound violated")
    return float(value)


def tensor(value, name, *, ndim=None, shape=None, device=None):
    if not isinstance(value, torch.Tensor) or not value.is_floating_point():
        raise ValueError(f"{name}: floating tensor required")
    if ndim is not None and value.ndim != ndim:
        raise ValueError(f"{name}: wrong rank")
    if shape is not None and value.shape != shape:
        raise ValueError(f"{name}: wrong shape")
    if device is not None and value.device != device:
        raise ValueError(f"{name}: wrong device")
    if not value.numel() or not bool(torch.isfinite(value).all()):
        raise ValueError(f"{name}: nonempty finite tensor required")
    return value


def mask(value, reference):
    if (
        not isinstance(value, torch.Tensor)
        or value.dtype != torch.bool
        or value.shape != reference.shape
        or value.device != reference.device
    ):
        raise ValueError("same-shape/device Boolean mask required")
    if not bool(value.any()):
        raise ValueError("empty supervision is not a zero-quality measurement")
    return value


def seeded(seed, device):
    if type(seed) is not int or device not in {"cpu", "cuda"}:
        raise ValueError("integer seed and explicit cpu/cuda device required")
    return torch.Generator(device="cpu").manual_seed(seed)


def receipt(seed, tier, checks, metrics):
    if type(seed) is not int or not all(type(x) is bool for x in checks.values()):
        raise ValueError("integer seed and pure Boolean checks required")
    if not all(
        isinstance(x, (int, float)) and not isinstance(x, bool) and math.isfinite(x)
        for x in metrics.values()
    ):
        raise ValueError("finite scalar metrics required")
    return {
        "seed": seed,
        "diagnostic_only": True,
        "evaluation_tier": tier,
        "checks": checks,
        "metrics": metrics,
    }
