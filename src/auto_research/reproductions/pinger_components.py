"""PinGER's exact mask, one-level prefix selection and prefix-DPO kernels.

L1 only: no tokenizer, recommender, custom sparse/cascade CUDA kernel or serving.
Teacher-forced token log-probabilities and the NTP anchor are caller supplied.
"""
from __future__ import annotations

import math

import torch
from torch import Tensor
import torch.nn.functional as F


def _integer(value, lo, hi, name):
    if isinstance(value, bool) or not isinstance(value, int) or not lo <= value <= hi:
        raise ValueError(f"{name} must be an integer in [{lo}, {hi}]")


def _scalar(value, name, *, zero=False):
    if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value) or (value < 0 if zero else value <= 0):
        raise ValueError(f"invalid {name}")


def _floating(value, name):
    if not isinstance(value, Tensor) or value.dtype not in (torch.float32, torch.float64) or not value.numel() or not torch.isfinite(value).all():
        raise ValueError(f"{name} must be finite nonempty float32/float64")


def interleaved_mask(items: int, levels: int, *, device="cpu") -> Tensor:
    """Section 3.3: [s1,...,sL,e] per item; True means visible.

    SID self-attention is allowed. NTP labels still require the caller's shift;
    this function does not construct labels or expose a target to a predictor.
    """
    _integer(items, 1, 128, "items")
    _integer(levels, 1, 32, "levels")
    size = items * (levels + 1)
    if size > 2048:
        raise ValueError("bounded reference mask supports at most 2048 positions")
    item = torch.arange(size, device=device) // (levels + 1)
    role = torch.arange(size, device=device) % (levels + 1)
    q_item, k_item = item[:, None], item[None, :]
    q_role, k_role = role[:, None], role[None, :]
    dense = (q_role == levels) & (k_role == levels) & (k_item <= q_item)
    sid = (q_role < levels) & (((k_role == levels) & (k_item < q_item)) |
                              ((k_item == q_item) & (k_role <= q_role)))
    return dense | sid


def masked_attention(q: Tensor, k: Tensor, v: Tensor, mask: Tensor) -> Tensor:
    """Dense numerical reference, not PinGER's optimized attention kernel."""
    for name, value in (("q", q), ("k", k), ("v", v)):
        _floating(value, name)
    if q.ndim != 2 or k.shape != q.shape or v.ndim != 2 or len(v) != len(k) or not (q.device == k.device == v.device) or not (q.dtype == k.dtype == v.dtype):
        raise ValueError("one equal-length Q/K sequence and aligned V required")
    if len(q) > 2048 or q.shape[-1] > 512 or v.shape[-1] > 512:
        raise ValueError("bounded dense reference: <=2048 tokens and <=512 dimensions")
    if not isinstance(mask, Tensor) or mask.dtype != torch.bool or mask.shape != (len(q), len(k)) or mask.device != q.device or not mask.any(-1).all():
        raise ValueError("nonempty visible row and colocated boolean mask required")
    scores = q @ k.T / math.sqrt(q.shape[-1])
    if not torch.isfinite(scores).all():
        raise ValueError("attention score overflow")
    result = scores.masked_fill(~mask, -torch.inf).softmax(-1) @ v
    if not torch.isfinite(result).all():
        raise ValueError("attention output overflow")
    return result


def select_prefix_candidates(parents, scores: Tensor, width: int, penalty: float, valid: Tensor | None = None):
    """Eq.5 / Appendix A.4, exactly one level, stable parent/code tie-break.

    Returns (parent-index, code-index), raw accumulated scores and selection-time
    penalized scores. Cross-level score bookkeeping is deliberately external.
    Python sequencing is a reference, not the paper's fused GPU loop.
    """
    _floating(scores, "scores")
    _scalar(penalty, "penalty", zero=True)
    _integer(width, 1, 1024, "width")
    if scores.ndim != 2 or scores.numel() > 200_000 or not isinstance(parents, (tuple, list)) or len(parents) != len(scores) or len(parents) > 512:
        raise ValueError("bounded parent-by-code scores required")
    if not parents or any(not isinstance(p, tuple) for p in parents) or len(set(parents)) != len(parents):
        raise ValueError("distinct tuple prefixes required")
    depth = len(parents[0])
    if depth > 32 or any(len(p) != depth or any(isinstance(t, bool) or not isinstance(t, int) or t < 0 for t in p) for p in parents):
        raise ValueError("equal-depth nonnegative integer prefixes required")
    if valid is None:
        valid = torch.ones_like(scores, dtype=torch.bool)
    if not isinstance(valid, Tensor) or valid.shape != scores.shape or valid.dtype != torch.bool or valid.device != scores.device or int(valid.sum()) < width:
        raise ValueError("not enough valid candidates")
    m = torch.tensor([[next((i for i, (x, y) in enumerate(zip(a, b)) if x != y), depth)
                       for b in parents] for a in parents], dtype=scores.dtype, device=scores.device)
    order = scores.masked_fill(~valid, -torch.inf).argsort(dim=-1, descending=True, stable=True)
    counts = torch.zeros(len(parents), dtype=torch.long, device=scores.device)
    penalty_sum = torch.zeros(len(parents), dtype=scores.dtype, device=scores.device)
    available = valid.sum(-1)
    selected, raw, adjusted = [], [], []
    for _ in range(width):
        at = counts.clamp(max=scores.shape[1] - 1)
        code = order.gather(1, at[:, None]).squeeze(1)
        next_scores = scores.gather(1, code[:, None]).squeeze(1) - penalty * penalty_sum
        if not torch.isfinite(next_scores[counts < available]).all():
            raise ValueError("prefix penalty overflow")
        next_scores = next_scores.masked_fill(counts >= available, -torch.inf)
        parent = int(next_scores.argmax())
        token = int(code[parent])
        selected.append((parent, token))
        raw.append(scores[parent, token])
        adjusted.append(next_scores[parent])
        counts[parent] += 1
        penalty_sum = penalty_sum + m[:, parent]
    return selected, torch.stack(raw), torch.stack(adjusted)


def prefix_dpo_loss(chosen: Tensor, rejected: Tensor, reference_chosen: Tensor,
                    reference_rejected: Tensor, ntp_anchor: Tensor, *, beta=0.1, weight=1.0) -> Tensor:
    """Eq.6: sum all prefix losses, then retain the external NTP anchor."""
    _scalar(beta, "beta")
    _scalar(weight, "weight", zero=True)
    rows = (chosen, rejected, reference_chosen, reference_rejected)
    for value in (*rows, ntp_anchor):
        _floating(value, "log-probabilities/anchor")
    if chosen.ndim != 2 or chosen.numel() > 100_000 or any(v.shape != chosen.shape or v.device != chosen.device or v.dtype != chosen.dtype for v in rows):
        raise ValueError("aligned batch-by-level log probabilities required")
    if any((v > 0).any() for v in rows) or ntp_anchor.ndim != 0 or ntp_anchor.device != chosen.device or ntp_anchor.dtype != chosen.dtype or ntp_anchor < 0:
        raise ValueError("log probabilities <=0 and nonnegative scalar anchor required")
    margin = (chosen - rejected).cumsum(-1) - (reference_chosen.detach() - reference_rejected.detach()).cumsum(-1)
    if not torch.isfinite(margin).all():
        raise ValueError("prefix margin overflow")
    loss = ntp_anchor + weight * F.softplus(-beta * margin).sum(-1).mean()
    if not torch.isfinite(loss):
        raise ValueError("loss overflow")
    return loss


def diagnostic(seed=42, device="cpu"):
    generator = torch.Generator(device=device).manual_seed(seed)
    dtype = torch.float64
    items, levels, dim = 5, 3, 8
    n = items * (levels + 1)
    x = torch.randn(n, dim, generator=generator, dtype=dtype, device=device)
    mask = interleaved_mask(items, levels, device=device)
    dense = torch.arange(levels, n, levels + 1, device=device)
    full, compact = x.clone(), x[dense].clone()
    causal = torch.ones(items, items, device=device, dtype=torch.bool).tril()
    for _ in range(2):
        w = torch.randn(dim, dim, generator=generator, dtype=dtype, device=device) * 0.1
        full = full + masked_attention(full @ w, full, full, mask)
        compact = compact + masked_attention(compact @ w, compact, compact, causal)
    invariance = float((full[dense] - compact).abs().max())
    wrong_mask = torch.ones_like(mask).tril()
    wrong = x + masked_attention(x, x, x, wrong_mask)
    correct = x + masked_attention(x, x, x, mask)
    mask_gap = float((wrong[dense] - correct[dense]).abs().max())
    scores = torch.tensor([[6., 5.9, 1.], [5.8, 5.7, 0.], [5.6, 5.5, -1.]], device=device, dtype=dtype)
    parents = [(0, 0), (0, 1), (1, 0)]
    greedy, _, _ = select_prefix_candidates(parents, scores, 3, 0.)
    spread, _, _ = select_prefix_candidates(parents, scores, 3, 1.)
    policy = torch.randn(2, 4, 2, generator=generator, dtype=dtype, device=device).requires_grad_()
    reference = torch.randn(2, 4, 2, generator=generator, dtype=dtype, device=device).requires_grad_()
    optimizer = torch.optim.SGD([policy], lr=0.05)

    def loss():
        lp, ref = policy.log_softmax(-1), reference.log_softmax(-1)
        return prefix_dpo_loss(lp[..., 0], lp[..., 1], ref[..., 0], ref[..., 1], -lp[..., 0].mean(), beta=0.2)

    before = loss()
    optimizer.zero_grad()
    before.backward()
    gradient = float(policy.grad.norm())
    optimizer.step()
    after = loss()
    lp = policy.detach().log_softmax(-1)
    ref = reference.detach().log_softmax(-1)
    last_only = -lp[..., 0].mean() + F.softplus(-0.2 * ((lp[..., 0] - lp[..., 1]) - (ref[..., 0] - ref[..., 1])).sum(-1)).mean()
    metrics = {"dense_compaction_max_error": invariance, "causal_mask_negative_control_gap": mask_gap,
               "greedy_selected_parents": len({i for i, _ in greedy}), "penalized_selected_parents": len({i for i, _ in spread}),
               "loss_before": float(before.detach()), "loss_after": float(after.detach()), "actor_gradient_norm": gradient,
               "last_prefix_only_loss_gap": float((after.detach() - last_only).abs()), "pretrained_model_calls": 0}
    checks = {"dense_stream_invariant": invariance < 1e-10, "ordinary_causal_mask_is_not_equivalent": mask_gap > 1e-6,
              "zero_penalty_matches_top_width": greedy == [(0, 0), (0, 1), (1, 0)],
              "prefix_penalty_changes_parent_spread": len({i for i, _ in spread}) > len({i for i, _ in greedy}),
              "prefix_sum_not_last_level_only": metrics["last_prefix_only_loss_gap"] > 1e-6,
              "actual_actor_update": metrics["loss_after"] < metrics["loss_before"] and gradient > 0,
              "frozen_reference": reference.grad is None, "no_model_or_serving_calls": True}
    return {"seed": seed, "metrics": metrics, "checks": checks}
