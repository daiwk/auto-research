"""CuE (2603.23301): feature pooling, cumulative MI, prototypes and steering.

SAE extraction and mutual-information estimation remain external. In particular,
no arbitrary binning estimator is substituted for an unspecified upstream one.
This component operates at one residual layer; global feature selection must be
mapped to the appropriate layer/decoder by its caller.
"""
from __future__ import annotations

import math
from collections.abc import Sequence

import torch

REQUIRES_GPU_VALIDATION = True


def _finite(x: torch.Tensor, ndim: int):
    if not isinstance(x, torch.Tensor) or x.ndim != ndim or not x.is_floating_point() or not torch.isfinite(x).all():
        raise ValueError("finite floating tensor with the declared rank required")
    if any(n == 0 for n in x.shape):
        raise ValueError("empty axes are not valid cultural evidence")


def max_pool_features(activations: torch.Tensor, token_mask: torch.Tensor) -> torch.Tensor:
    _finite(activations, 3)
    if token_mask.shape != activations.shape[:2] or token_mask.dtype != torch.bool or token_mask.device != activations.device:
        raise ValueError("same-device Boolean [assertion,token] mask required")
    if not token_mask.any(dim=1).all():
        raise ValueError("each assertion must contain a valid token")
    return activations.masked_fill(~token_mask[..., None], -torch.inf).max(dim=1).values


def select_cumulative_mi(mi: torch.Tensor, rho: float = .1) -> torch.Tensor:
    _finite(mi, 1)
    if not math.isfinite(rho) or not 0 < rho <= 1 or (mi < 0).any() or mi.sum() <= 0:
        raise ValueError("nonnegative nonzero MI and 0 < cumulative fraction <= 1 required")
    order = torch.argsort(mi, descending=True, stable=True)
    target = rho * mi.sum()
    count = int(torch.searchsorted(mi[order].cumsum(0), target).item()) + 1
    return order[:min(count, mi.numel())]


def country_prototypes(features: torch.Tensor, labels: Sequence[str]) -> tuple[tuple[str, ...], torch.Tensor]:
    _finite(features, 2)
    if len(labels) != features.shape[0] or any(not isinstance(c, str) or not c for c in labels):
        raise ValueError("one nonempty culture label per assertion required")
    countries = tuple(sorted(set(labels)))
    if len(countries) < 2:
        raise ValueError("target-vs-other-country steering requires at least two countries")
    return countries, torch.stack([features[[i for i, label in enumerate(labels) if label == c]].mean(0) for c in countries])


def steering_direction(prototypes: torch.Tensor, target: int, decoder: torch.Tensor) -> torch.Tensor:
    _finite(prototypes, 2)
    _finite(decoder, 2)
    if prototypes.shape[0] < 2 or type(target) is not int or not 0 <= target < prototypes.shape[0]:
        raise ValueError("valid target among at least two country prototypes required")
    if decoder.shape[0] != prototypes.shape[1] or decoder.device != prototypes.device or decoder.dtype != prototypes.dtype:
        raise ValueError("matching [selected_features,residual_dim] decoder rows required")
    others = torch.cat((prototypes[:target], prototypes[target+1:]), dim=0).mean(0)
    return (prototypes[target] - others) @ decoder


def apply_steering(hidden: torch.Tensor, direction: torch.Tensor, alpha: float) -> torch.Tensor:
    if not isinstance(hidden, torch.Tensor) or hidden.ndim < 1 or not torch.isfinite(hidden).all():
        raise ValueError("finite residual tensor required")
    _finite(direction, 1)
    if hidden.shape[-1] != direction.numel() or hidden.device != direction.device or hidden.dtype != direction.dtype or not math.isfinite(alpha):
        raise ValueError("matching residual dimension/device/dtype and finite alpha required")
    return hidden + alpha * direction


def diagnostic(seed: int = 42, device: str = "cpu") -> dict:
    if type(seed) is not int:
        raise ValueError("integer seed required")
    generator = torch.Generator(device="cpu").manual_seed(seed)
    activations = torch.rand(4, 3, 4, generator=generator, dtype=torch.float64).to(device)
    mask = torch.ones(4, 3, dtype=torch.bool, device=device); mask[:, -1] = False
    pooled = max_pool_features(activations, mask)
    mi = torch.tensor([.6, .25, .10, .05], dtype=torch.float64, device=device)
    selected = select_cumulative_mi(mi, .7)
    countries, proto = country_prototypes(pooled[:, selected], ["A", "B", "B", "C"])
    decoder = torch.randn(2, 3, generator=generator, dtype=torch.float64).to(device)
    direction = steering_direction(proto, 0, decoder)
    hidden = torch.zeros(2, 3, dtype=torch.float64, device=device)
    output = apply_steering(hidden, direction, .5)
    expected = (proto[0] - (proto[1] + proto[2]) / 2) @ decoder
    checks = {"cumulative_mi_not_feature_count": selected.tolist() == [0, 1],
              "token_padding_excluded": bool(torch.equal(pooled, activations[:, :2].max(1).values)),
              "country_not_example_weighted_baseline": bool(torch.allclose(direction, expected)),
              "residual_addition_exact": bool(torch.allclose(output, .5 * expected.expand_as(output))),
              "country_labels_preserved": countries == ("A", "B", "C")}
    return {"seed": seed, "device": str(device), "diagnostic_only": True, "evaluation_tier": "l1_mechanism",
            "metrics": {"selected_features": selected.numel(), "direction_norm": float(direction.norm().item()),
                        "steering_formula_error": float((direction-expected).abs().max().item()), "pretrained_model_calls": 0}, "checks": checks}
