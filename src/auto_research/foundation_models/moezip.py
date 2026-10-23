"""MoEZip routing-aware KV selection, arXiv:2610.30206v1, Sec. 3/App. C.

Independent formula implementation: upstream 197959dbae2adfab7ec233f584ce951b827e04cc
contains README/LICENSE only. Caller supplies prefill instruction statistics and
a base scorer; this module neither loads a language model nor reads answer tokens.
"""
from __future__ import annotations

from dataclasses import dataclass
import math

import torch
from torch import Tensor

REQUIRES_GPU_VALIDATION = True
GPU_VALIDATION_ARTIFACT = "docs/gpu-validations/moezip-a100-20261023.json"


def _finite(value: Tensor, ndim: int, name: str) -> None:
    if value.ndim != ndim or min(value.shape) < 1 or not value.is_floating_point():
        raise ValueError(f"{name} must be nonempty floating rank {ndim}")
    if not bool(torch.isfinite(value).all()):
        raise ValueError(f"{name} must be finite")


def fisher_trace(gates: Tensor, router: str = "softmax") -> Tensor:
    """Fisher trace in logit coordinates, not hidden-state/Jacobian curvature."""
    if gates.ndim < 1 or min(gates.shape) < 1 or not gates.is_floating_point():
        raise ValueError("nonempty floating router gates required")
    if not bool(torch.isfinite(gates).all()) or bool(((gates < 0) | (gates > 1)).any()):
        raise ValueError("router probabilities must be finite and in [0,1]")
    if router == "softmax":
        if not torch.allclose(gates.sum(-1), torch.ones_like(gates[..., 0]), atol=1e-5, rtol=1e-5):
            raise ValueError("softmax gates must sum to one")
        return (1 - gates.square().sum(-1)).clamp_min(0)
    if router == "sigmoid":
        return (gates * (1 - gates)).sum(-1)
    raise ValueError("router must be softmax or sigmoid")


@dataclass(frozen=True)
class RoutingSelection:
    indices: Tensor  # [cache layer, head, retained position], in original order
    anchors: Tensor
    routing_scores: Tensor
    fragility: Tensor
    fragile_fraction: float
    anchor_count: int


@torch.no_grad()
def select_cache(gates: Tensor, instruction_attention: Tensor, base_scores: Tensor,
                 budget: int, *, router: str = "softmax", rho_min: float = .05,
                 rho_max: float = .25, min_anchors: int = 32,
                 max_anchors: int = 128) -> RoutingSelection:
    """Reserve global routing anchors then fill each head from its base scorer.

    Gates: [MoE layer,instruction,expert]. Attention: [same MoE layer,head,
    same instruction,context]. Base scores may cover additional dense layers.
    Attention is a prefix slice of a causal softmax: row mass may be below one.
    The App. C 32/128 bounds are additionally capped by B (necessary for tiny B).
    Ties resolve to lower context position, an explicit local reproducibility rule.
    """
    _finite(gates, 3, "gates")
    _finite(instruction_attention, 4, "instruction attention")
    _finite(base_scores, 3, "base scores")
    if gates.device != instruction_attention.device or gates.device != base_scores.device:
        raise ValueError("statistics must share a device")
    if instruction_attention.shape[0] != gates.shape[0] or instruction_attention.shape[2] != gates.shape[1]:
        raise ValueError("MoE layer/instruction dimensions do not align")
    length = instruction_attention.shape[-1]
    if base_scores.shape[-1] != length or not isinstance(budget, int) or not 0 <= budget <= length:
        raise ValueError("budget must be an integer in [0,context length]")
    if bool((instruction_attention < 0).any()) or bool((instruction_attention.sum(-1) > 1 + 1e-5).any()):
        raise ValueError("attention must be a nonnegative softmax prefix slice")
    if not (math.isfinite(rho_min) and math.isfinite(rho_max) and 0 <= rho_min <= rho_max <= 1):
        raise ValueError("anchor ratios must satisfy 0 <= min <= max <= 1")
    if not 0 <= min_anchors <= max_anchors:
        raise ValueError("invalid anchor bounds")
    fragility = fisher_trace(gates, router)
    maximum = 1 - 1 / gates.shape[-1] if router == "softmax" else gates.shape[-1] / 4
    fraction = float((fragility > .85 * maximum).to(torch.float64).mean())
    raw_count = math.floor(budget * (rho_min + (rho_max - rho_min) * fraction))
    count = min(budget, max(min_anchors, min(max_anchors, raw_count)))
    scores = (instruction_attention.amax(1) * fragility[..., None]).sum((0, 1))
    anchors = scores.argsort(descending=True, stable=True)[:count]
    available = torch.ones(length, device=gates.device, dtype=torch.bool)
    available[anchors] = False
    remaining_positions = torch.arange(length, device=gates.device)[available]
    ranking = base_scores[..., available].argsort(dim=-1, descending=True, stable=True)
    fill = remaining_positions[ranking[..., :budget - count]]
    repeated_anchors = anchors.expand(*base_scores.shape[:2], count)
    indices = torch.cat((repeated_anchors, fill), -1).sort(-1).values
    return RoutingSelection(indices, anchors.sort().values, scores, fragility, fraction, count)


def compress_cache(keys: Tensor, values: Tensor, selection: RoutingSelection) -> tuple[Tensor, Tensor]:
    """Gather actual K/V rows; return indices separately to preserve position IDs."""
    _finite(keys, 4, "keys")
    _finite(values, 4, "values")
    if keys.shape[:3] != values.shape[:3] or keys.shape[:2] != selection.indices.shape[:2]:
        raise ValueError("cache and selection shapes do not align")
    if keys.device != values.device or keys.device != selection.indices.device:
        raise ValueError("cache and selection must share a device")
    index = selection.indices
    if index.numel() and (int(index.min()) < 0 or int(index.max()) >= keys.shape[2]):
        raise ValueError("selection outside cache")
    return (keys.gather(2, index[..., None].expand(*index.shape, keys.shape[-1])),
            values.gather(2, index[..., None].expand(*index.shape, values.shape[-1])))


def diagnostic(seed: int, device: str = "cpu") -> dict:
    """Generated-tensor L1 check with explicit Fisher and real KV gathering."""
    import hashlib
    generator = torch.Generator(device=device).manual_seed(seed)
    attention = torch.randn(2, 3, 8, 512, generator=generator, device=device).softmax(-1)
    logits = torch.randn(2, 8, 8, generator=generator, device=device)
    gates = logits.softmax(-1)
    base = torch.randn(2, 3, 512, generator=generator, device=device)
    k = torch.randn(2, 3, 512, 8, generator=generator, device=device)
    v = torch.randn(2, 3, 512, 6, generator=generator, device=device)
    result = select_cache(gates, attention, base, 256)
    ck, cv = compress_cache(k, v, result)
    reference = torch.zeros(512, device=device)
    for layer in range(2):
        for token in range(8):
            explicit_fisher = torch.diag(gates[layer, token]) - gates[layer, token, :, None] * gates[layer, token, None, :]
            reference += attention[layer, :, token].amax(0) * torch.trace(explicit_fisher)
    error = float((reference - result.routing_scores).abs().max())
    anchors_present = all(bool(torch.isin(result.anchors, row).all()) for row in result.indices.flatten(0, 1))
    uniform = select_cache(torch.full_like(gates, 1 / 8), attention, base, 256)
    peaked_gates = torch.zeros_like(gates)
    peaked_gates[..., 0] = 1
    peaked = select_cache(peaked_gates, attention, base, 256)
    sigmoid = select_cache(logits.sigmoid(), attention, base, 256, router="sigmoid")
    checks = {"explicit_fisher_reference": error <= 2e-5,
              "all_anchors_present": anchors_present,
              "actual_kv_gather_shapes": ck.shape == (2, 3, 256, 8) and cv.shape == (2, 3, 256, 6),
              "exact_budget_and_uniqueness": all(len(row.unique()) == 256 for row in result.indices.flatten(0, 1)),
              "adaptive_anchor_bounds": uniform.anchor_count == 64 and peaked.anchor_count == 32,
              "sigmoid_path_budget": sigmoid.indices.shape == (2, 3, 256)}
    if not all(checks.values()):
        raise RuntimeError("MoEZip selection/reference mismatch")
    return {"seed": seed, "checks": checks, "metrics": {"explicit_fisher_score_max_abs_error": error,
            "all_anchors_present": anchors_present, "retained_rows_per_head": result.indices.shape[-1],
            "anchor_count": result.anchor_count, "fragile_fraction": result.fragile_fraction,
            "uniform_router_anchor_count": uniform.anchor_count,
            "peaked_router_anchor_count": peaked.anchor_count,
            "sigmoid_anchor_count": sigmoid.anchor_count},
            "data_sha256": hashlib.sha256(logits.cpu().numpy().tobytes() + attention.cpu().numpy().tobytes()).hexdigest()}
