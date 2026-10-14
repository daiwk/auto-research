"""Independent implementation of OAL, arXiv:2610.13674 Eqs. 2/5/6/7.

Dense pairwise evaluation is retained for small differentiable calibration;
the equivalent recurrent readout has no token-by-token attention matrix.
No unlicensed upstream code or model-specific precomputed factors are copied.
"""
from __future__ import annotations

import math

import torch
from torch import Tensor, nn


def contribution(q: Tensor, k: Tensor) -> Tensor:
    """Equal-weight per-prompt causal absolute QK contribution, Eq. 2.

    q/k are [batch, head, token, dimension], already post-RoPE and GQA-expanded.
    """
    if q.shape != k.shape or q.ndim != 4:
        raise ValueError("matched BHTD post-RoPE Q/K required")
    length = q.shape[-2]
    pairs = length * (length + 1) / 2
    # |q_i k_j| = |q_i| |k_j|; prefix sum avoids N^2 materialization.
    return (q.abs() * k.abs().cumsum(-2)).sum(-2) / (pairs * math.sqrt(q.shape[-1]))


def group_dimensions(prompt_scores: Tensor, *, tail: float = .25,
                     bootstrap: int = 1000, ratio: float = 1.5,
                     support: float = .9, minimum: int = 2, seed: int = 42) -> Tensor:
    """Appendix B stable ordering, fixed-order prompt bootstrap and fallback.

    Scores are [prompt, head, dimension]. All natural cuts are retained; there
    is no artificial group cap or boundary-spacing constraint.
    """
    if prompt_scores.ndim != 3 or not 0 < tail <= 1 or bootstrap < 1:
        raise ValueError("prompt/head/dimension scores and valid grouping settings required")
    prompts, heads, dimensions = prompt_scores.shape
    if not prompts or not 1 <= minimum <= dimensions:
        raise ValueError("nonempty prompts and feasible minimum groups required")
    generator = torch.Generator(device=prompt_scores.device).manual_seed(seed)
    samples = torch.randint(prompts, (bootstrap, prompts), generator=generator,
                            device=prompt_scores.device)
    resampled = prompt_scores[samples].mean(1)
    mean = prompt_scores.mean(0)
    maps = []
    for head in range(heads):
        order = torch.argsort(mean[head], stable=True)
        ordered = mean[head, order]
        scores = resampled[:, head, order]
        start = max(1, dimensions - math.ceil(tail * dimensions))
        candidates = list(range(start, dimensions))
        if len(candidates) < minimum - 1:
            raise ValueError("tail has insufficient candidate cuts for minimum groups")
        statistics = []
        for cut in candidates:
            gap = float(ordered[cut] / ordered[cut - 1].clamp_min(1e-12))
            separation = scores[:, cut:].amin(-1) / scores[:, :cut].amax(-1).clamp_min(1e-12)
            probability = float((separation >= ratio).float().mean())
            statistics.append((cut, probability, gap))
        cuts = {cut for cut, probability, gap in statistics if gap >= ratio and probability >= support}
        ranked = sorted(statistics, key=lambda item: (-item[1], -item[2]))
        for cut, _, _ in ranked:
            if len(cuts) >= minimum - 1:
                break
            cuts.add(cut)
        result = torch.empty(dimensions, dtype=torch.long, device=prompt_scores.device)
        endpoints = [0, *sorted(cuts), dimensions]
        for group, (a, b) in enumerate(zip(endpoints[:-1], endpoints[1:])):
            result[order[a:b]] = group
        maps.append(result)
    return torch.stack(maps)


class GroupedQuadratic(nn.Module):
    def __init__(self, groups: Tensor, epsilon: float = 1e-6):
        super().__init__()
        if groups.ndim != 2 or epsilon <= 0 or int(groups.min()) != 0:
            raise ValueError("nonnegative head/dimension group map and epsilon > 0 required")
        self.register_buffer("groups", groups.long())
        self.epsilon = epsilon
        count = int(groups.max()) + 1
        factors = torch.zeros(groups.shape[0], count + 1, count + 1, device=groups.device)
        factors[:, 0, 0] = 1
        # Embedded positive second-order Taylor 1+s+.5s^2.
        factors[:, 1:, 0] = .5
        factors[:, 1:, 1] = .5
        self.factors = nn.Parameter(factors)

    def coefficients(self) -> tuple[Tensor, Tensor, Tensor]:
        lower = self.factors.tril()
        gram = lower @ lower.transpose(-1, -2)
        heads = torch.arange(len(self.groups), device=self.groups.device)[:, None]
        ids = self.groups + 1
        constant = self.epsilon + gram[:, 0, 0]
        linear = 2 * gram[heads, 0, ids]
        quadratic = gram[heads[..., None], ids[..., None], ids[:, None, :]]
        return constant, linear, quadratic

    def kernel(self, q: Tensor, k: Tensor) -> Tensor:
        pieces = []
        for group in range(self.factors.shape[-1] - 1):
            mask = (self.groups == group).to(q.dtype)
            pieces.append(torch.einsum("bhid,bhjd->bhij", q * mask[None, :, None], k)
                          / math.sqrt(q.shape[-1]))
        products = torch.stack([torch.ones_like(pieces[0]), *pieces], -1)
        transformed = torch.einsum("bhijg,hgf->bhijf", products.float(), self.factors.tril())
        return self.epsilon + transformed.square().sum(-1)

    def forward(self, q: Tensor, k: Tensor, v: Tensor, attention_mask: Tensor | None = None) -> Tensor:
        weights = self.kernel(q, k)
        causal = torch.arange(q.shape[-2], device=q.device)[:, None] >= torch.arange(k.shape[-2], device=k.device)[None]
        weights = weights * causal
        if attention_mask is not None:
            allowed = attention_mask if attention_mask.dtype == torch.bool else attention_mask >= 0
            weights = weights.masked_fill(~allowed, 0)
        if (weights.sum(-1) == 0).any():
            raise ValueError("each OAL query needs at least one unmasked causal key")
        weights = weights / weights.sum(-1, keepdim=True)
        return torch.einsum("bhij,bhjv->bhiv", weights, v.float())

    def recurrent(self, q: Tensor, k: Tensor, v: Tensor) -> Tensor:
        """Exact dimension-pair HD statistics, Eqs. 5/6, O(N d^2 dv)."""
        if q.shape != k.shape or q.shape[:3] != v.shape[:3]:
            raise ValueError("aligned BHTD/BHTV inputs required")
        batch, heads, length, dim = q.shape
        values = torch.cat((v.float(), torch.ones_like(v[..., :1])), -1)
        h0 = q.new_zeros(batch, heads, values.shape[-1], dtype=torch.float32)
        h1 = q.new_zeros(batch, heads, dim, values.shape[-1], dtype=torch.float32)
        h2 = q.new_zeros(batch, heads, dim, dim, values.shape[-1], dtype=torch.float32)
        a, b, c = self.coefficients()
        outputs = []
        for index in range(length):
            key, query, value = k[:, :, index].float(), q[:, :, index].float(), values[:, :, index]
            h0 = h0 + value
            h1 = h1 + key[..., :, None] * value[..., None, :]
            h2 = h2 + key[..., :, None, None] * key[..., None, :, None] * value[..., None, None, :]
            readout = (a[None, :, None] * h0
                       + torch.einsum("hd,bhd,bhdv->bhv", b, query, h1) / math.sqrt(dim)
                       + torch.einsum("hde,bhd,bhe,bhdev->bhv", c, query, query, h2) / dim)
            outputs.append(readout[..., :-1] / readout[..., -1:].clamp_min(1e-12))
        return torch.stack(outputs, dim=-2)


class QwenOALAttention(nn.Module):
    """Qwen2 attention conversion, preserving original QKV/RoPE/GQA/o_proj.

    Small-block training uses the dense exact kernel; autoregressive KV-cache
    serving is intentionally unsupported, not silently replaced by softmax.
    """
    def __init__(self, original: nn.Module, kernel: GroupedQuadratic):
        super().__init__()
        self.original, self.kernel = original, kernel

    def forward(self, hidden_states: Tensor, position_embeddings=None,
                attention_mask=None, past_key_values=None, past_key_value=None,
                **kwargs):
        if past_key_values is not None or past_key_value is not None:
            raise ValueError("OAL reference conversion does not implement serving cache")
        if position_embeddings is None:
            raise ValueError("post-RoPE positional embeddings are required")
        q, k, v = qwen_states(self.original, hidden_states, position_embeddings)
        output = self.kernel(q, k, v, attention_mask=attention_mask).to(hidden_states.dtype)
        output = output.transpose(1, 2).reshape(*hidden_states.shape[:-1], -1)
        return self.original.o_proj(output), None


def qwen_states(attention, hidden: Tensor, position_embeddings) -> tuple[Tensor, Tensor, Tensor]:
    from transformers.models.qwen2.modeling_qwen2 import apply_rotary_pos_emb, repeat_kv

    shape = (*hidden.shape[:-1], -1, attention.head_dim)
    q = attention.q_proj(hidden).view(shape).transpose(1, 2)
    k = attention.k_proj(hidden).view(shape).transpose(1, 2)
    v = attention.v_proj(hidden).view(shape).transpose(1, 2)
    q, k = apply_rotary_pos_emb(q, k, *position_embeddings)
    groups = q.shape[1] // k.shape[1]
    return q, repeat_kv(k, groups), repeat_kv(v, groups)


def install_lora(model: nn.Module, rank: int = 8, alpha: float = 16., dropout: float = .05) -> None:
    """Appendix F.2 q/k/v/o LoRA in every layer, including retained softmax."""
    if rank < 1:
        raise ValueError("positive rank required")
    model.requires_grad_(False)

    class LowRank(nn.Module):
        def __init__(self, base):
            super().__init__()
            self.base = base
            self.a = nn.Parameter(torch.empty(rank, base.in_features, device=base.weight.device))
            self.b = nn.Parameter(torch.zeros(base.out_features, rank, device=base.weight.device))
            nn.init.kaiming_uniform_(self.a, a=math.sqrt(5))
            self.dropout = nn.Dropout(dropout)

        def forward(self, x):
            update = torch.nn.functional.linear(
                torch.nn.functional.linear(self.dropout(x.float()), self.a), self.b)
            return self.base(x) + (update * (alpha / rank)).to(x.dtype)

    count = 0
    for module in list(model.modules()):
        for name, child in list(module.named_children()):
            if name in ("q_proj", "k_proj", "v_proj", "o_proj") and isinstance(child, nn.Linear):
                setattr(module, name, LowRank(child))
                count += 1
    if not count:
        raise ValueError("no native attention projections matched")
