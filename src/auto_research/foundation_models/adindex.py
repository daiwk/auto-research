"""Small tensor reference for ADIndex v1 equations 4, 6--14, not a serving kernel."""
from __future__ import annotations

import torch
from torch import Tensor, nn

REQUIRES_GPU_VALIDATION = True
GPU_VALIDATION_ARTIFACT = "docs/gpu-validations/adindex-a100-20261111.json"


def _topk(scores: Tensor, count: int) -> Tensor:
    if type(count) is not int or count < 1 or count > scores.shape[-1]:
        raise ValueError("positive budget must fit the visible prefix")
    return torch.argsort(scores, dim=-1, descending=True, stable=True)[..., :count]


def teacher_distribution(scores: Tensor, bank_size: int, temperature: float = 3.0) -> Tensor:
    """Restrict input to s<=anchor BEFORE calling; max normalized query probabilities."""
    if (scores.ndim != 2 or min(scores.shape) < 1 or not torch.isfinite(scores).all()
            or not 0 < temperature < float("inf")):
        raise ValueError("finite [group, anchor-visible keys] scores and positive temperature required")
    frozen = scores.detach()
    standardized = (frozen - frozen.mean(-1, keepdim=True)) / frozen.std(
        -1, correction=0, keepdim=True).clamp_min(1e-6)
    maxima = (standardized / temperature).softmax(-1).amax(0)
    support = _topk(maxima, bank_size)
    target = torch.zeros_like(maxima).scatter(0, support, maxima[support])
    return target / target.sum()


def rope_at(query: Tensor, position: int) -> Tensor:
    if query.shape[-1] % 2 or position < 0:
        raise ValueError("even head dimension and nonnegative anchor required")
    frequency = 10000.0 ** (-torch.arange(0, query.shape[-1], 2,
                                        device=query.device, dtype=query.dtype) / query.shape[-1])
    angle = position * frequency
    even, odd = query[..., 0::2], query[..., 1::2]
    return torch.stack((even * angle.cos() - odd * angle.sin(),
                        even * angle.sin() + odd * angle.cos()), -1).flatten(-2)


class GroupIndexer(nn.Module):
    """Only W_pool, W_Q^S and W_G^S train; cached backbone inputs/keys stay frozen."""

    def __init__(self, latent_dim: int, hidden_dim: int, heads: int, head_dim: int):
        super().__init__()
        if min(latent_dim, hidden_dim, heads, head_dim) < 1 or head_dim % 2:
            raise ValueError("positive dimensions and an even rotary head dimension required")
        self.heads, self.head_dim = heads, head_dim
        self.pool = nn.Linear(3 * latent_dim, latent_dim, bias=False)
        self.query = nn.Linear(latent_dim, heads * head_dim, bias=False)
        self.gate = nn.Linear(hidden_dim, heads, bias=False)
        with torch.no_grad():
            self.pool.weight.zero_()
            self.pool.weight[:, 2 * latent_dim:].copy_(torch.eye(latent_dim))

    def scores(self, latents: Tensor, hidden: Tensor, keys: Tensor, anchor: int) -> Tensor:
        if (latents.ndim != 2 or hidden.ndim != 2 or keys.ndim != 2
                or len(latents) != len(hidden) or len(keys) != anchor + 1
                or keys.shape[-1] != self.head_dim):
            raise ValueError("group features and ONLY the anchor-visible key prefix are required")
        latents, hidden, keys = latents.detach(), hidden.detach(), keys.detach()
        pooled = self.pool(torch.cat((latents.amax(0), latents.amin(0), latents.mean(0))))
        query = rope_at(self.query(pooled).view(self.heads, self.head_dim), anchor)
        gate = self.gate(hidden.mean(0)).sigmoid()
        return (gate[:, None] * (query @ keys.T).relu()).sum(0)

    def forward(self, latents: Tensor, hidden: Tensor, keys: Tensor, anchor: int) -> Tensor:
        return self.scores(latents, hidden, keys, anchor).softmax(-1)


def forward_kl(target: Tensor, student: Tensor) -> Tensor:
    """Forward KL(T||S), excluding zero teacher mass instead of logging zero."""
    active = target > 0
    return (target[active] * (target[active].log() - student[active].log())).sum()


def refine_indices(query_scores: Tensor, bank: Tensor, *, anchor: int, query: int,
                   final_k: int, bank_budget: int, complete_group: bool = True) -> Tensor:
    if (query_scores.ndim != 1 or not 0 <= anchor <= query < len(query_scores)
            or final_k < 1 or bank_budget < 1):
        raise ValueError("valid causal positions and positive budgets required")
    if anchor + 1 <= bank_budget or not complete_group:
        candidates = torch.arange(query + 1, device=query_scores.device)
    else:
        if bank.ndim != 1 or len(bank) != bank_budget or torch.any((bank < 0) | (bank > anchor)):
            raise ValueError("shared bank must contain exactly the anchor-visible budget")
        candidates = torch.unique(torch.cat((bank, torch.arange(
            anchor + 1, query + 1, device=query_scores.device))), sorted=True)
    return candidates[_topk(query_scores[candidates], min(final_k, len(candidates)))]


def union_capacity(topk_sets: list[set[int]], group_size: int) -> int:
    if group_size < 1 or len(topk_sets) < group_size:
        raise ValueError("at least one complete calibration group required")
    return max(len(set().union(*topk_sets[i:i + group_size]))
               for i in range(0, len(topk_sets) - group_size + 1, group_size))


def diagnostic(seed: int, device: str = "cpu") -> dict:
    if device not in {"cpu", "cuda"} or (device == "cuda" and not torch.cuda.is_available()):
        raise ValueError("available CPU or actual CUDA device required")
    torch.manual_seed(seed)
    model = GroupIndexer(12, 10, 2, 8).to(device)
    latents = torch.randn(4, 12, device=device, requires_grad=True)
    hidden = torch.randn(4, 10, device=device, requires_grad=True)
    keys = torch.randn(32, 8, device=device, requires_grad=True)
    frozen_scores = torch.randn(4, 32, device=device)
    target = teacher_distribution(frozen_scores, 12)
    initial_pool_mean = torch.allclose(model.pool(torch.cat((
        latents.amax(0), latents.amin(0), latents.mean(0)))), latents.mean(0))
    optimizer = torch.optim.AdamW(model.parameters(), lr=0.025, weight_decay=0.0)
    before = float(forward_kl(target, model(latents, hidden, keys, 31)).detach())
    for _ in range(64):
        optimizer.zero_grad()
        loss = forward_kl(target, model(latents, hidden, keys, 31))
        loss.backward()
        optimizer.step()
    after = float(forward_kl(target, model(latents, hidden, keys, 31)).detach())
    bank = _topk(model.scores(latents, hidden, keys, 31).detach(), 12)
    full_scores = torch.linspace(0, 1, 40, device=device)
    selected = refine_indices(full_scores, bank, anchor=31, query=34, final_k=4, bank_budget=12)
    short = refine_indices(full_scores, bank, anchor=3, query=5, final_k=2, bank_budget=12)
    return {
        "seed": seed, "diagnostic_only": True, "evaluation_tier": "l1_mechanism",
        "metrics": {"training_kl_before": before, "training_kl_after": after,
                    "teacher_support": int((target > 0).sum()), "selected_tokens": len(selected),
                    "calibration_union_capacity": union_capacity([{0, 1}, {1, 2}, {0, 2}, {2, 3}], 2)},
        "checks": {"mean_initialized_pool": bool(initial_pool_mean),
                   "teacher_target_normalized": bool(torch.allclose(target.sum(), target.new_tensor(1.0))),
                   "student_kl_optimized": after < before,
                   "backbone_inputs_and_keys_frozen": all(x.grad is None for x in (latents, hidden, keys)),
                   "post_anchor_tokens_retained": {32, 33, 34} <= set(selected.cpu().tolist()),
                   "causal_indices_only": bool(torch.all(selected <= 34)),
                   "short_prefix_fallback": short.cpu().tolist() == [5, 4]},
    }
