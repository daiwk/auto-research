"""DNA Eq2-13 small real attention stack with request-shared history updates.

    No HHFT tokenizer, private CTR training or claimed online gain is included.
"""

from __future__ import annotations

from dataclasses import dataclass
import math

import torch
from torch import nn
from torch.nn import functional as F

REQUIRES_GPU_VALIDATION = True


class SwiGLU(nn.Module):
    def __init__(self, width):
        super().__init__()
        self.gate = nn.Linear(width, 2 * width)
        self.value = nn.Linear(width, 2 * width)
        self.out = nn.Linear(2 * width, width)

    def forward(self, x):
        return self.out(F.silu(self.gate(x)) * self.value(x))


class Read(nn.Module):
    def __init__(self, width, heads, tokens):
        super().__init__()
        self.norm = nn.LayerNorm(width)
        self.query = nn.Linear(width, width)
        self.out = nn.Linear(width, width)
        self.ffnorm = nn.LayerNorm(width)
        self.ff = nn.ModuleList(SwiGLU(width) for _ in range(tokens))
        self.heads = heads
        self.q_scale = nn.Parameter(torch.ones(heads))
        self.k_scale = nn.Parameter(torch.ones(heads))

    def forward(self, x, keys, values, valid):
        q = self.query(self.norm(x)).unflatten(-1, (self.heads, -1)).transpose(1, 2)
        context = attend(q, keys, values, valid, self.q_scale, self.k_scale)
        y = x + self.out(context)
        normalized = self.ffnorm(y)
        return y + torch.stack([f(normalized[:, i]) for i, f in enumerate(self.ff)], dim=1)


def attend(q, k, v, valid, q_scale, k_scale):
    """L2 QKNorm per head; learned scales, followed by Eq5 sqrt(d_h)."""
    q = F.normalize(q, dim=-1) * q_scale[None, :, None, None]
    k = F.normalize(k, dim=-1) * k_scale[None, :, None, None]
    logits = q @ k.transpose(-2, -1) / math.sqrt(q.shape[-1])
    if valid is not None:
        logits = logits.masked_fill(~valid[:, None, None, :], -torch.inf)
    return (logits.softmax(-1) @ v).transpose(1, 2).flatten(-2)


class Layer(nn.Module):
    def __init__(self, width, heads, groups, request_tokens, candidate_tokens, update):
        super().__init__()
        self.heads, self.width, self.request_tokens = heads, width, request_tokens
        self.k = nn.ModuleList(nn.Linear(width, width) for _ in range(groups))
        self.v = nn.ModuleList(nn.Linear(width, width) for _ in range(groups))
        self.request_read = Read(width, heads, request_tokens)
        self.candidate_read = Read(width, heads, candidate_tokens)
        self.updating = update
        if update:
            self.seqnorm = nn.LayerNorm(width)
            self.request_norm = nn.LayerNorm(width)
            self.seqquery = nn.ModuleList(nn.Linear(width, width) for _ in range(groups))
            # Composite projections mix all request tokens, not per-token Linear(d,d).
            self.uk = nn.Linear(request_tokens * width, request_tokens * width)
            self.uv = nn.Linear(request_tokens * width, request_tokens * width)
            self.update_out = nn.Linear(width, width)
            self.update_ffnorm = nn.LayerNorm(width)
            self.update_ff = nn.ModuleList(SwiGLU(width) for _ in range(groups))
            self.update_q_scale = nn.Parameter(torch.ones(heads))
            self.update_k_scale = nn.Parameter(torch.ones(heads))

    def grouped(self, x, group_ids, maps):
        result = torch.zeros_like(x)
        for i, layer in enumerate(maps):
            positions = group_ids == i
            result[:, positions] = layer(x[:, positions])
        return result

    def split(self, x):
        return x.unflatten(-1, (self.heads, -1)).transpose(1, 2)

    def kv(self, sequence, group_ids):
        return self.split(self.grouped(sequence, group_ids, self.k)), self.split(self.grouped(sequence, group_ids, self.v))

    def update(self, sequence, request, group_ids, valid):
        q = self.split(self.grouped(self.seqnorm(sequence), group_ids, self.seqquery))
        u = self.request_norm(request).flatten(1)
        shape = (request.shape[0], self.request_tokens, self.width)
        k, v = self.split(self.uk(u).reshape(shape)), self.split(self.uv(u).reshape(shape))
        context = attend(q, k, v, None, self.update_q_scale, self.update_k_scale)
        x = sequence + self.update_out(context)
        x = x + self.grouped(self.update_ffnorm(x), group_ids, self.update_ff)
        return x.masked_fill(~valid[..., None], 0)


@dataclass
class RequestCache:
    keys_values: list
    request: torch.Tensor
    sequence: torch.Tensor
    valid: torch.Tensor
    updates: int


class DNA(nn.Module):
    def __init__(self, width=8, heads=2, groups=2, request_tokens=2, candidate_tokens=2, depth=2):
        super().__init__()
        if any(type(v) is not int or v <= 0 for v in (width, heads, groups, request_tokens, candidate_tokens, depth)) or width % heads:
            raise ValueError("positive divisible dimensions required")
        self.width, self.groups = width, groups
        self.request_tokens, self.candidate_tokens = request_tokens, candidate_tokens
        self.layers = nn.ModuleList(Layer(width, heads, groups, request_tokens, candidate_tokens, i < depth - 1)
                                    for i in range(depth))
        self.head = nn.Sequential(nn.Linear(width, width), nn.SiLU(), nn.Linear(width, 1))

    def prepare_request(self, sequence, request, group_ids, valid):
        if (sequence.ndim != 3 or sequence.shape[-1] != self.width
                or request.shape != (sequence.shape[0], self.request_tokens, self.width)
                or valid.shape != sequence.shape[:2] or valid.dtype != torch.bool
                or group_ids.shape != (sequence.shape[1],) or group_ids.dtype != torch.long
                or (group_ids < 0).any() or (group_ids >= self.groups).any()
                or not valid.any(-1).all()):
            raise ValueError("invalid token/group/mask shapes or empty history")
        if not torch.isfinite(sequence).all() or not torch.isfinite(request).all():
            raise ValueError("finite explicit tokens required")
        sequence = sequence.masked_fill(~valid[..., None], 0)
        cache = []
        updates = 0
        for layer in self.layers:
            keys, values = layer.kv(sequence, group_ids)
            cache.append((keys, values))
            request = layer.request_read(request, keys, values, valid)
            if layer.updating:
                sequence = layer.update(sequence, request, group_ids, valid)
                updates += 1
        return RequestCache(cache, request, sequence, valid, updates)

    def score(self, cache, candidates):
        b, n, tokens, width = candidates.shape
        if (b != cache.request.shape[0] or n < 1 or tokens != self.candidate_tokens
                or width != self.width or not torch.isfinite(candidates).all()):
            raise ValueError("invalid candidate tokens")
        x = candidates.flatten(0, 1)
        valid = cache.valid.repeat_interleave(n, dim=0)
        for layer, (k, v) in zip(self.layers, cache.keys_values, strict=True):
            x = layer.candidate_read(x, k.repeat_interleave(n, dim=0), v.repeat_interleave(n, dim=0), valid)
        request = cache.request.repeat_interleave(n, dim=0)
        pooled = torch.cat([x, request], dim=1).mean(1)
        return self.head(pooled).reshape(b, n)

    def forward(self, sequence, request, candidates, group_ids, valid):
        return self.score(self.prepare_request(sequence, request, group_ids, valid), candidates)


def diagnostic(seed, device="cpu"):
    if type(seed) is not int or device not in {"cpu", "cuda"}:
        raise ValueError("integer seed and CPU/CUDA required")
    torch.manual_seed(seed)
    model = DNA(depth=3).to(device)
    s = torch.randn(1, 5, 8, device=device, requires_grad=True)
    u = torch.randn(1, 2, 8, device=device, requires_grad=True)
    f = torch.randn(1, 3, 2, 8, device=device)
    groups = torch.tensor([0, 0, 1, 1, 1], device=device)
    valid = torch.tensor([[True, True, True, True, False]], device=device)
    cache = model.prepare_request(s, u, groups, valid)
    y = model.score(cache, f)
    changed = s.detach().clone(); changed[:, -1] = 1e6
    padded = model(changed, u.detach(), f, groups, valid)
    pieces = torch.cat([model.score(cache, f[:, i:i+1]) for i in range(3)], dim=1)
    changed_request = u.detach().clone()
    changed_request[..., 0] += .7
    other = model.prepare_request(s, changed_request, groups, valid)
    loss = F.binary_cross_entropy_with_logits(y, torch.tensor([[0., 1., 0.]], device=device))
    loss.backward()
    checks = {"padding_invariant": torch.allclose(y, padded, atol=1e-6),
              "batched_equals_shared_single_candidates": torch.allclose(y, pieces, atol=1e-6),
              "final_layer_no_update": cache.updates == 2,
              "request_changes_sequence": not torch.allclose(cache.sequence, other.sequence),
              "padded_sequence_zero": (cache.sequence[:, -1] == 0).all().item(),
              "history_and_request_gradients": bool(s.grad.abs().sum() > 0 and u.grad.abs().sum() > 0),
              "finite_backward": bool(torch.isfinite(s.grad).all() and torch.isfinite(u.grad).all())}
    return {"seed": seed, "diagnostic_only": True, "evaluation_tier": "l1_mechanism",
            "checks": checks, "metrics": {"fixture_bce": loss.item(),
                                           "history_gradient_l1": s.grad.abs().sum().item(),
                                           "updates": cache.updates}}
