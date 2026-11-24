"""DCA fixed-v2 text-formula GRN-v3 and independent-Q/K/V attention core.

This is not a complete decoder block or pretraining implementation. We follow
Section3.1's displayed b + ReLU(w^T G) equation, not Figure3's differently
ordered normalization/activation diagram. Routing weights are not softmax.
"""

import math

import torch
from torch import nn

REQUIRES_GPU_VALIDATION = True


def _positive(value):
    if type(value) is not int or value < 1:
        raise ValueError("positive integer dimensions required")
    return value


def history_stack(history, keep_last=None):
    """Chronological [input, f1,...] -> newest-first G; no cumulative states.

    Limited history retains input and last-k outputs, with one unweighted sum
    of all intermediate outputs. It is not a sliding-window eviction policy.
    """
    if not isinstance(history, (tuple, list)) or not history:
        raise ValueError("nonempty chronological layer-output history required")
    if keep_last is not None and (type(keep_last) is not int or keep_last < 0):
        raise ValueError("keep_last must be None or a nonnegative integer")
    first = history[0]
    if not isinstance(first, torch.Tensor) or first.ndim < 1 or not first.is_floating_point():
        raise ValueError("floating layer outputs required")
    if any(not isinstance(x, torch.Tensor) or x.shape != first.shape
           or x.device != first.device or x.dtype != first.dtype
           or not torch.isfinite(x).all() for x in history):
        raise ValueError("finite matched shape/device/dtype outputs required")
    if keep_last is None or len(history) <= keep_last + 1:
        chosen = list(reversed(history))
    else:
        tail = history[len(history)-keep_last:] if keep_last else []
        middle = history[1:len(history)-keep_last] if keep_last else history[1:]
        chosen = list(reversed(tail)) + [torch.stack(middle).sum(0), first]
    return torch.stack(chosen, dim=-2)


class GRN3(nn.Module):
    """Section3.1: static feature/source weights plus input-dependent ReLU."""

    def __init__(self, width, sources):
        super().__init__()
        self.width, self.sources = _positive(width), _positive(sources)
        self.base = nn.Parameter(torch.ones(sources, width))
        self.dynamic = nn.Parameter(torch.zeros(width))

    def forward(self, stack):
        if (stack.ndim < 2 or stack.shape[-2:] != (self.sources, self.width)
                or stack.dtype != self.base.dtype or stack.device != self.base.device
                or not torch.isfinite(stack).all()):
            raise ValueError("finite matching [..., sources, width] stack required")
        scores = torch.einsum("...sd,d->...s", stack, self.dynamic).relu()
        return (stack * (self.base + scores.unsqueeze(-1))).sum(-2)


class DCAAttention(nn.Module):
    """Three independent GRN3s, then ordinary causal token attention.

    Per-Q/K/V LayerNorm follows Figure4. No layer softmax, shared QK route,
    feed-forward stage, outer residual rewiring, KV cache or dropout is added.
    """

    def __init__(self, width, sources, heads=2):
        super().__init__()
        self.width, self.heads = _positive(width), _positive(heads)
        if width % heads:
            raise ValueError("width must be divisible by heads")
        self.routes = nn.ModuleList([GRN3(width, sources) for _ in range(3)])
        self.norms = nn.ModuleList([nn.LayerNorm(width) for _ in range(3)])
        self.projections = nn.ModuleList([nn.Linear(width, width, bias=False) for _ in range(3)])
        self.output = nn.Linear(width, width, bias=False)

    def routed_inputs(self, stack):
        if stack.ndim != 4 or min(stack.shape[:2]) < 1:
            raise ValueError("nonempty [batch, tokens, sources, width] stack required")
        return tuple(route(stack) for route in self.routes)

    def forward(self, stack):
        batch, tokens = stack.shape[:2]
        dim = self.width // self.heads
        routed = self.routed_inputs(stack)
        q, k, v = [projection(norm(x)).reshape(batch, tokens, self.heads, dim).transpose(1, 2)
                   for x, projection, norm in zip(routed, self.projections, self.norms, strict=True)]
        logits = (q @ k.transpose(-1, -2)) / math.sqrt(dim)
        future = torch.ones(tokens, tokens, dtype=torch.bool, device=stack.device).triu(1)
        weights = logits.masked_fill(future, -torch.inf).softmax(-1)
        return self.output((weights @ v).transpose(1, 2).reshape(batch, tokens, self.width))


def diagnostic(seed=42, device="cpu"):
    if type(seed) is not int or device not in ("cpu", "cuda"):
        raise ValueError("integer seed and cpu/cuda device required")
    generator = torch.Generator().manual_seed(seed)
    history = [torch.randn(2, 5, 8, generator=generator).to(device) for _ in range(6)]
    stack = history_stack(history, keep_last=2)
    with torch.random.fork_rng(devices=[]):
        torch.manual_seed(seed)
        model = DCAAttention(8, 4).to(device)
    routed = model.routed_inputs(stack)
    init_matches = all(torch.allclose(x, torch.stack(history).sum(0), atol=1e-6) for x in routed)
    initial_loss = model(stack).square().mean()
    initial_loss.backward()
    zero_init_gradient = all(torch.count_nonzero(r.dynamic.grad) == 0 for r in model.routes)
    model.zero_grad(set_to_none=True)
    with torch.no_grad():
        model.routes[0].base[0] += .2
        for route in model.routes:
            route.dynamic.fill_(.05)
    changed = model.routed_inputs(stack)
    # A Q-only static intervention cannot change the independently routed K/V.
    with torch.no_grad():
        reference_k, reference_v = changed[1].clone(), changed[2].clone()
        model.routes[0].base[1] -= .3
    after_q_change = model.routed_inputs(stack)
    out = model(stack)
    out.square().mean().backward()
    modified = stack.clone()
    modified[:, -1] += 20
    with torch.no_grad():
        causal_gap = float((model(modified)[:, :-1] - out.detach()[:, :-1]).abs().max().item())
    checks = {
        "ones_zero_init_recovers_residual_sum": bool(init_matches),
        "middle_bucket_preserves_unweighted_sum": bool(torch.allclose(stack.sum(-2), torch.stack(history).sum(0), atol=1e-6)),
        "qkv_routes_have_distinct_parameters": len({r.base.data_ptr() for r in model.routes}) == 3,
        "q_only_intervention_leaves_kv_unchanged": bool(torch.equal(after_q_change[1], reference_k) and torch.equal(after_q_change[2], reference_v)),
        "nonzero_dynamic_weights_receive_gradients": all(r.dynamic.grad is not None and torch.isfinite(r.dynamic.grad).all() and r.dynamic.grad.abs().sum() > 0 for r in model.routes),
        "zero_relu_init_gradient_is_explicit": bool(zero_init_gradient),
        "future_tokens_do_not_change_prefix": causal_gap < 1e-6,
    }
    return {"seed": seed, "device": device, "diagnostic_only": True,
            "evaluation_tier": "l1_mechanism", "checks": {k: bool(v) for k, v in checks.items()},
            "metrics": {"synthetic_output_rms": float(out.square().mean().sqrt().item()),
                        "causal_prefix_max_gap": causal_gap,
                        "retained_history_sources": stack.shape[-2]}}
