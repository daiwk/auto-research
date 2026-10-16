"""Independent DropKV Eq. 3/Algorithm 1 reference, not a fused serving kernel."""
from __future__ import annotations

from dataclasses import dataclass
import math

import torch
from torch import Tensor
import torch.nn.functional as F


@dataclass(frozen=True)
class DropKVResult:
    scores: Tensor
    evicted_indices: Tensor
    attention: Tensor
    outputs: Tensor


def drop_kv_scores(queries: Tensor, keys: Tensor, values: Tensor, *, eviction_count: int,
                   pooling_kernel: int = 1) -> DropKVResult:
    """Score a tail-aligned causal observation window with grouped-query attention.

    Q is [batch,query_heads,window,dim], K/V are [batch,kv_heads,cache,dim].
    Query-head squared perturbations are averaged within each physical KV head.
    Recent window entries are never evicted. This materializes reference tensors;
    it deliberately does not claim the paper's Triton memory/latency properties.
    """
    if (queries.ndim != 4 or keys.ndim != 4 or values.shape != keys.shape or
            queries.shape[0] != keys.shape[0] or queries.shape[-1] != keys.shape[-1] or
            keys.shape[1] < 1 or queries.shape[1] < 1 or queries.shape[1] % keys.shape[1]):
        raise ValueError("expected compatible Q [B,Hq,W,D], K/V [B,Hkv,N,D] with Hq divisible by Hkv")
    if any(not x.is_floating_point() or x.device != queries.device for x in (queries, keys, values)):
        raise ValueError("floating inputs on one device required")
    if any(not bool(torch.isfinite(x).all()) for x in (queries, keys, values)):
        raise ValueError("nonfinite input")
    batch, query_heads, window, dim = queries.shape
    kv_heads, length = keys.shape[1:3]
    if not (0 < window < length and dim > 0 and batch > 0):
        raise ValueError("a nonempty window strictly shorter than cache is required")
    if (isinstance(eviction_count, bool) or not isinstance(eviction_count, int) or
            not 0 <= eviction_count <= length - window):
        raise ValueError("eviction_count must fit the unprotected prefix")
    if not isinstance(pooling_kernel, int) or pooling_kernel < 1 or pooling_kernel % 2 != 1:
        raise ValueError("pooling_kernel must be a positive odd integer")
    dtype = torch.float64 if queries.dtype == torch.float64 else torch.float32
    groups = query_heads // kv_heads
    k = keys.to(dtype).repeat_interleave(groups, dim=1)
    v = values.to(dtype).repeat_interleave(groups, dim=1)
    q = queries.to(dtype)
    positions = torch.arange(length, device=q.device)
    causal = positions[None, :] <= (length - window + torch.arange(window, device=q.device))[:, None]
    logits = (q @ k.transpose(-1, -2) / math.sqrt(dim)).masked_fill(~causal, -torch.inf)
    probability = logits.softmax(-1)
    # Exact removal is undefined when a probability rounds to one; never hide
    # the singularity behind an epsilon that changes the defining score.
    if bool((probability >= 1).any()):
        raise ValueError("degenerate rounded-one attention; exact singleton eviction is undefined")
    outputs = probability @ v
    residual_squared = (outputs.unsqueeze(-2) - v.unsqueeze(-3)).square().sum(-1)
    per_query = (probability / (1 - probability)).square() * residual_squared
    per_head = per_query.sum(-2).reshape(batch, kv_heads, groups, length).mean(-2)
    pooled = F.max_pool1d(per_head.reshape(-1, 1, length), pooling_kernel,
                         stride=1, padding=pooling_kernel // 2).reshape_as(per_head)
    protected = positions >= length - window
    scores = pooled.masked_fill(protected, torch.inf)
    evicted = scores.topk(eviction_count, largest=False, dim=-1).indices
    return DropKVResult(scores, evicted, probability, outputs)
