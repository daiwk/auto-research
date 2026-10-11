"""V-CoLA's actual Gated-DeltaNet state-readout scores and visual merging.

Eq.2/6/7/8/10 of arXiv:2610.11251. This reference recurrence prioritizes
auditable equivalence, not the author's accelerated chunk-parallel kernel.
"""
from __future__ import annotations

from dataclasses import dataclass

import torch
from torch.nn import functional as F


def cosine_distance(a, b):
    return ((1 - F.cosine_similarity(a, b, dim=-1, eps=1e-8)) / 2).clamp(0, 1)


@dataclass
class StateScores:
    importance: torch.Tensor
    uniqueness: torch.Tensor
    combined: torch.Tensor
    recurrent_output: torch.Tensor
    final_state: torch.Tensor


def delta_state_scores(query, key, value, log_decay, beta, *, window=(0, 4), mix=.1):
    """Use checkpoint q/k/v/g/beta, never hidden-state similarity as a proxy.

    State convention here is [key,value], the transpose of the paper's S. This
    is the convention used by Transformers/FLA Qwen3.5 kernels. Query probes
    follow Eq.7; Appendix A's shifted-*key* variant is not silently substituted.
    """
    if query.shape != key.shape or query.ndim != 4 or value.shape[:3] != key.shape[:3]:
        raise ValueError("expected aligned [batch,sequence,head,dimension] q/k/v")
    if log_decay.shape != key.shape[:3] or beta.shape != log_decay.shape:
        raise ValueError("unaligned checkpoint gates")
    if key.shape[1] < 1 or not all(bool(torch.isfinite(x).all()) for x in (query, key, value)):
        raise ValueError("actual checkpoint q/k/v must be nonempty and finite")
    left, right = window
    if not left <= 0 < right or not 0 <= mix <= 1:
        raise ValueError("invalid pseudo-query window or uniqueness weight")
    if not bool(torch.isfinite(log_decay).all()) or bool((log_decay > 0).any()):
        raise ValueError("checkpoint log decay must be finite and nonpositive")
    if not bool(((beta >= 0) & (beta <= 1)).all()):
        raise ValueError("write gate must be in [0,1]")
    # Qwen/FLA use rsqrt(sum(x^2)+eps), not F.normalize's max(norm,eps).
    # The distinction is material for shallow random/tiny q/k magnitudes.
    q = query.float() * torch.rsqrt(query.float().square().sum(-1, keepdim=True) + 1e-6)
    k = key.float() * torch.rsqrt(key.float().square().sum(-1, keepdim=True) + 1e-6)
    v = value.float()
    batch, length, heads, kd = k.shape
    state = torch.zeros(batch, heads, kd, v.shape[-1], device=k.device)
    unique, output = [], []
    for t in range(length):
        probes = q[:, max(0, t + left):min(length, t + right)].transpose(1, 2)
        before = probes @ state
        state = state * log_decay[:, t].float().exp()[:, :, None, None]
        recalled = (state * k[:, t, :, :, None]).sum(-2)
        delta = (v[:, t] - recalled) * beta[:, t, :, None].float()
        state = state + k[:, t, :, :, None] * delta[:, :, None, :]
        after = probes @ state
        unique.append(cosine_distance(after, before).mean((1, 2)))
        output.append((state * (q[:, t] / kd**.5)[:, :, :, None]).sum(-2))
    retained = torch.einsum("bthk,bhkv->bthv", k, state)
    importance = 1 - cosine_distance(retained, v).mean(-1)
    uniqueness = torch.stack(unique, 1)
    return StateScores(importance, uniqueness, (1 - mix) * importance + mix * uniqueness,
                       torch.stack(output, 1), state)


def importance_chunks(scores, count):
    """Appendix A CDF-nearest balanced-mass boundaries; no empty chunks.

    The paper's Eq.9 is a combinatorial objective. Its practical appendix uses
    cumulative-importance quantiles. We likewise choose nearest prefix-mass
    boundaries with monotone nonempty constraints, not top-k token pruning.
    """
    if scores.ndim != 1 or not 1 <= count <= len(scores):
        raise ValueError("nonempty one-dimensional scores and legal chunk count required")
    if not bool(torch.isfinite(scores).all()) or bool((scores < 0).any()):
        raise ValueError("importance scores must be finite/nonnegative")
    mass = scores.double()
    if float(mass.sum()) == 0:
        mass = torch.ones_like(mass)
    cumulative = torch.cat((mass.new_zeros(1), mass.cumsum(0)))
    boundaries = [0]
    for index in range(1, count):
        low, high = boundaries[-1] + 1, len(scores) - (count - index)
        target = cumulative[-1] * index / count
        candidates = cumulative[low:high + 1]
        boundaries.append(low + int((candidates - target).abs().argmin()))
    boundaries.append(len(scores))
    return list(zip(boundaries[:-1], boundaries[1:], strict=True))


def merge_visual_tokens(hidden, positions, visual_mask, scores, *, remain_rate=.5, temperature=1.):
    """Physically shorten one contiguous image-token block after layer one.

    Text states/absolute 3D positions are untouched. Each merged visual token
    receives the original highest-scoring member's mRoPE position (an explicit
    backend choice, not a claim about unspecified author position handling).
    """
    if hidden.ndim != 3 or hidden.shape[0] != 1 or positions.shape != (3, 1, hidden.shape[1]):
        raise ValueError("reference backend supports batch one and original 3D positions")
    if visual_mask.shape != (hidden.shape[1],) or scores.shape != visual_mask.shape:
        raise ValueError("token mask/score shape mismatch")
    if not 0 < remain_rate <= 1 or temperature <= 0:
        raise ValueError("invalid compression ratio/temperature")
    ids = visual_mask.nonzero().flatten()
    if not len(ids) or not torch.equal(ids, torch.arange(int(ids[0]), int(ids[-1]) + 1, device=ids.device)):
        raise ValueError("only a single contiguous nonempty image block is supported")
    start, stop = int(ids[0]), int(ids[-1]) + 1
    count = max(1, round(len(ids) * remain_rate))
    chunks = importance_chunks(scores[ids], count)
    values, anchors = [], []
    for a, b in chunks:
        members = ids[a:b]
        weights = (scores[members].float() / temperature).softmax(0)
        values.append((hidden[:, members].float() * weights[None, :, None]).sum(1).to(hidden.dtype))
        anchors.append(int(members[int(scores[members].argmax())]))
    merged = torch.stack(values, 1)
    indices = torch.tensor([*range(start), *anchors, *range(stop, hidden.shape[1])], device=ids.device)
    result = torch.cat((hidden[:, :start], merged, hidden[:, stop:]), 1)
    mask = torch.zeros(result.shape[1], device=ids.device, dtype=torch.bool)
    mask[start:start + count] = True
    return result, positions[:, :, indices], mask, {"original_visual_tokens": len(ids),
        "merged_visual_tokens": count, "chunk_sizes": [b - a for a, b in chunks],
        "anchor_indices": anchors}


def early_exit_visual(hidden, positions, visual_mask):
    keep = ~visual_mask
    if not bool(keep.any()):
        raise ValueError("early exit cannot remove the entire sequence")
    return hidden[:, keep], positions[:, :, keep], torch.zeros(int(keep.sum()), dtype=torch.bool,
                                                               device=hidden.device)
