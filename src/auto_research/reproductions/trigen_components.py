"""TriGen v1 Eqs.4--8, bounded differentiable condition kernels, not a model."""
from __future__ import annotations

import math

import torch
from torch import nn

REQUIRES_GPU_VALIDATION = True


def tail_inject(history, trigger, repetitions):
    if (history.ndim != 3 or trigger.shape != (history.shape[0], history.shape[2])
            or not isinstance(repetitions, int) or not 0 <= repetitions <= history.shape[1]):
        raise ValueError("invalid fixed-context tail injection")
    return torch.cat((history[:, repetitions:], trigger[:, None].expand(-1, repetitions, -1)), dim=1)


def rotary(x, positions, base=10000.0):
    """Adjacent even/odd RoPE on supplied queries/keys, not input embeddings."""
    if x.shape[-1] % 2 or positions.ndim != 1 or positions.shape[0] != x.shape[-2]:
        raise ValueError("even width and one position per token required")
    frequencies = base ** (-torch.arange(0, x.shape[-1], 2, device=x.device, dtype=x.dtype) / x.shape[-1])
    angle = positions.to(x)[:, None] * frequencies
    even, odd = x[..., ::2], x[..., 1::2]
    return torch.stack((even * angle.cos() - odd * angle.sin(),
                        even * angle.sin() + odd * angle.cos()), dim=-1).flatten(-2)


class DualPathConditioner(nn.Module):
    """Pristine-history attention, pooled router, separate per-level PFFNs.

    The paper leaves MLP internals unspecified. The local two-layer GELU MLP is
    an explicit configurable implementation choice, not recovered author code.
    Padding masks are required when input history contains padding.
    """
    def __init__(self, dim, levels, hidden_dim=None):
        super().__init__()
        self.dim, self.levels = dim, levels
        self.trigger_queries = nn.Parameter(torch.randn(levels, dim, dim) / math.sqrt(dim))
        self.default_queries = nn.Parameter(torch.randn(levels, dim) / math.sqrt(dim))
        self.key, self.value = nn.Linear(dim, dim, bias=False), nn.Linear(dim, dim, bias=False)
        self.router = nn.Linear(2 * dim, levels)
        self.pffns = nn.ModuleList(nn.Sequential(nn.Linear(dim, hidden_dim or 2 * dim), nn.GELU(),
                                               nn.Linear(hidden_dim or 2 * dim, dim)) for _ in range(levels))

    def forward(self, pristine_history, trigger, valid_mask=None):
        h = pristine_history
        if h.ndim != 3 or trigger.shape != (h.shape[0], self.dim) or h.shape[2] != self.dim:
            raise ValueError("invalid pristine history or trigger")
        if valid_mask is None:
            valid_mask = torch.ones(h.shape[:2], dtype=torch.bool, device=h.device)
        if valid_mask.shape != h.shape[:2] or valid_mask.dtype != torch.bool or not valid_mask.any(1).all():
            raise ValueError("each history needs at least one visible behavior")
        keys, values = self.key(h), self.value(h)
        tq = torch.einsum("lij,bj->bli", self.trigger_queries, trigger)
        hq = self.default_queries[None].expand(h.shape[0], -1, -1)

        def attend(queries):
            scores = (queries @ keys.transpose(-1, -2)) / math.sqrt(self.dim)
            return scores.masked_fill(~valid_mask[:, None], -torch.inf).softmax(-1) @ values

        t, baseline = attend(tq), attend(hq)
        weights = self.router(torch.cat((t.mean(1), baseline.mean(1)), -1)).sigmoid()
        fused = weights[..., None] * t + (1 - weights[..., None]) * baseline
        projected = torch.stack([mlp(fused[:, level]) for level, mlp in enumerate(self.pffns)], 1)
        return projected, weights, t, baseline


def condition_decoder_inputs(prefix_embeddings, bos_embedding, condition):
    """Eq.8 accepts observed prefix embeddings only, not future SID/gold labels."""
    if (condition.ndim != 3 or prefix_embeddings.shape != (condition.shape[0], condition.shape[1] - 1, condition.shape[2])
            or bos_embedding.shape != (condition.shape[0], condition.shape[2])):
        raise ValueError("expected BOS plus exactly L-1 observed prefix embeddings")
    return torch.cat((bos_embedding[:, None], prefix_embeddings), 1) + condition


def diagnostic(seed=42, device="cpu"):
    torch.manual_seed(seed)
    h = torch.randn(2, 5, 4, device=device)
    t = torch.randn(2, 4, device=device)
    model = DualPathConditioner(4, 3).to(device)
    condition, weights, _, baseline = model(h, t)
    other, other_weights, _, other_baseline = model(h, -t)
    target = torch.zeros_like(condition)
    loss = (condition - target).square().mean()
    loss.backward()
    injected = tail_inject(h, t, 2)
    q, k = torch.randn(1, 5, 4, device=device), torch.randn(1, 5, 4, device=device)
    positions = torch.arange(5, device=device)
    scores = rotary(q, positions) @ rotary(k, positions).transpose(-1, -2)
    shifted = rotary(q, positions + 7) @ rotary(k, positions + 7).transpose(-1, -2)
    decoder = condition_decoder_inputs(torch.zeros(2, 2, 4, device=device), t, condition)
    return {"seed": seed, "diagnostic_only": True, "evaluation_tier": "l1_mechanism",
            "checks": {"fixed_context_tail": injected.shape == h.shape and torch.equal(injected[:, -1], t)
                       and torch.equal(injected[:, :3], h[:, 2:]),
                       "history_path_trigger_independent": torch.equal(baseline, other_baseline),
                       "input_dependent_router": not torch.allclose(weights, other_weights),
                       "position_specific_parameters": len({id(m[0].weight) for m in model.pffns}) == 3,
                       "rope_relative_positions": torch.allclose(scores, shifted, atol=2e-6),
                       "bos_conditioning": torch.allclose(decoder[:, 0], t + condition[:, 0]),
                       "all_parameters_receive_finite_gradients": all(p.grad is not None and torch.isfinite(p.grad).all().item()
                                                                 for p in model.parameters()),
                       "trigger_changes_condition": not torch.allclose(condition, other)},
            "metrics": {"diagnostic_loss": float(loss.detach()),
                        "router_mean": float(weights.detach().mean()),
                        "rope_max_error": float((scores - shifted).abs().max())}}
