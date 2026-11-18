"""RISA v1 §4: exact storage, recoverable bounded read plans, fresh attention."""

from __future__ import annotations

import math
import torch
from torch import Tensor

REQUIRES_GPU_VALIDATION = True
GPU_VALIDATION_ARTIFACT = "docs/gpu-validations/risa-a100-20261118-latest.json"


def grace_priority(
    attention_mass: Tensor, previous_scores: Tensor, keep_fraction: float = 0.25
) -> Tensor:
    """Mass-only admission: running prior-score quantile, not a learned correction."""
    if previous_scores.numel() < 1 or not 0 < keep_fraction <= 1:
        raise ValueError("nonempty historical scores and valid retained fraction required")
    threshold = torch.quantile(previous_scores.float().flatten(), 1 - keep_fraction)
    return attention_mass >= threshold


def page_scores(queries: Tensor, keys: Tensor) -> Tensor:
    """max AFTER each min/max-vector dot, then SUM over queries (not QUEST's bound)."""
    if queries.ndim != 2 or keys.ndim != 3 or queries.shape[-1] != keys.shape[-1]:
        raise ValueError("[queries,width], [pages,rows,width] required")
    minimum, maximum = keys.amin(1), keys.amax(1)
    return torch.maximum(queries @ minimum.T, queries @ maximum.T).sum(0)


def read_plan(
    queries: Tensor,
    keys: Tensor,
    hot: Tensor,
    mandatory_rows: Tensor,
    *,
    fraction: float = 0.5,
    hot_cap: int = 512,
    cold_cap: int = 128,
    protect_first: int = 4,
    protect_last: int = 8,
) -> Tensor:
    """Plan fixes historical addresses only; omitted COLD values remain intact."""
    if (
        hot.shape != keys.shape[:1]
        or hot.dtype != torch.bool
        or not 0 <= fraction <= 1
        or min(hot_cap, cold_cap, protect_first, protect_last) < 0
        or mandatory_rows.dtype != torch.long
    ):
        raise ValueError("valid page state, budget and integer mandatory rows required")
    count, rows, _ = keys.shape
    if mandatory_rows.numel() and bool(
        ((mandatory_rows < 0) | (mandatory_rows >= count * rows)).any()
    ):
        raise ValueError("mandatory row outside exact store")
    score = page_scores(queries, keys)
    hot_ids = torch.where(hot)[0]
    protected = torch.cat(
        [hot_ids[:protect_first], hot_ids[-protect_last:] if protect_last else hot_ids[:0]]
    ).unique()
    eligible = hot_ids[~torch.isin(hot_ids, protected)]
    cold = torch.where(~hot)[0]
    k = (
        min(hot_cap, eligible.numel(), max(1, round(fraction * eligible.numel())))
        if eligible.numel()
        else 0
    )
    selected_hot = eligible[score[eligible].topk(k).indices] if k else eligible[:0]
    q = min(cold_cap, cold.numel())
    selected_cold = cold[score[cold].topk(q).indices] if q else cold[:0]
    pages = torch.cat([protected, selected_hot, selected_cold]).unique()
    selected_rows = (pages[:, None] * rows + torch.arange(rows, device=keys.device)).flatten()
    return torch.cat([selected_rows, mandatory_rows]).unique(sorted=True)


def planned_attention(queries: Tensor, keys: Tensor, values: Tensor, plan: Tensor) -> Tensor:
    """One shared softmax over gathered history AND mandatory current rows."""
    if keys.shape != values.shape or plan.numel() < 1 or plan.unique().numel() != plan.numel():
        raise ValueError("nonempty deduplicated legal support and matching KV required")
    k, v = keys.flatten(0, 1)[plan], values.flatten(0, 1)[plan]
    weights = (queries @ k.T / math.sqrt(queries.shape[-1])).softmax(-1)
    return weights @ v


def diagnostic(seed: int, device: str = "cpu") -> dict:
    torch.manual_seed(seed)
    keys = torch.zeros(4, 2, 3, device=device)
    keys[1, :, 0] = 4
    keys[2, :, 0] = -4
    values = torch.randn_like(keys)
    hot = torch.tensor([True, False, False, True], device=device)
    mandatory = torch.tensor([6], device=device)
    q = torch.tensor([[1.0, 0, 0]], device=device, requires_grad=True)
    options = {"hot_cap": 0, "cold_cap": 1, "protect_first": 1, "protect_last": 1}
    first = read_plan(q.detach(), keys, hot, mandatory, **options)
    second = read_plan(-q.detach(), keys, hot, mandatory, **options)
    a = planned_attention(q, keys, values, first)
    b = planned_attention(-q, keys, values, first)
    a.sum().backward()
    return {
        "seed": seed,
        "diagnostic_only": True,
        "evaluation_tier": "l1_mechanism",
        "metrics": {
            "first_read_rows": float(first.numel()),
            "second_read_rows": float(second.numel()),
        },
        "checks": {
            "cold_page_can_be_recovered_later": bool(2 in first and 4 in second and 4 not in first),
            "mandatory_current_row_kept": bool(6 in first and 6 in second),
            "plan_does_not_cache_outputs": bool(not torch.allclose(a, b)),
            "fresh_query_gradient": bool(q.grad is not None and q.grad.abs().sum() > 0),
            "exact_values_not_evicted": bool(keys[2, 0, 0] == -4),
        },
    }
