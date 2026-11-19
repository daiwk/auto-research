"""Bounded X-split ARGUS causal memory and dual-head loss (fixed-v1 Eqs1–11).

Feature embeddings, teacher training, production caching and data pipelines are
not reproduced. Training's shared causal pass is deliberately distinct from
serving's truncated recent-history pass; neither may read target feedback.
"""

from __future__ import annotations

import math
import torch
from torch import nn
from torch.nn import functional as F

REQUIRES_GPU_VALIDATION = True


def _tensor(x, rank):
    if (
        not isinstance(x, torch.Tensor)
        or x.ndim != rank
        or not x.is_floating_point()
        or not torch.isfinite(x).all()
    ):
        raise ValueError("finite floating tensor of required rank needed")


class XSplitMemory(nn.Module):
    def __init__(self, dim: int = 8, heads: int = 2, window: int = 2):
        super().__init__()
        if any(type(x) is not int or x <= 0 for x in (dim, heads, window)) or dim % heads:
            raise ValueError("positive compatible dimensions/window required")
        self.dim, self.window = dim, window
        self.compressor = nn.TransformerEncoder(
            nn.TransformerEncoderLayer(dim, heads, 2 * dim, dropout=0.0, batch_first=True),
            1,
            enable_nested_tensor=False,
        )
        self.runtime = nn.TransformerEncoder(
            nn.TransformerEncoderLayer(dim, heads, 2 * dim, dropout=0.0, batch_first=True),
            2,
            enable_nested_tensor=False,
        )
        self.decoder = nn.MultiheadAttention(dim, heads, dropout=0.0, batch_first=True)
        self.supervised = nn.Linear(2 * dim, 1)
        self.distill = nn.Linear(2 * dim, 1)

    def _encode(self, events, runtime=False):
        _tensor(events, 3)
        if events.shape[-1] != self.dim or events.shape[1] == 0:
            raise ValueError("nonempty correctly dimensioned history required")
        pos = torch.arange(events.shape[1], device=events.device)
        age = pos[:, None] - pos[None, :]
        mask = age < 0
        if runtime:
            mask = mask | (age >= self.window)
        return (self.runtime if runtime else self.compressor)(events, mask=mask)

    def decode(self, candidates, memory):
        _tensor(candidates, 3)
        _tensor(memory, 3)
        if (
            candidates.shape[0] != memory.shape[0]
            or candidates.shape[-1] != self.dim
            or memory.shape[-1] != self.dim
            or memory.shape[1] == 0
        ):
            raise ValueError("compatible candidates and nonempty memory required")
        attended, _ = self.decoder(candidates, memory, memory, need_weights=False)
        representation = torch.cat((attended, candidates), dim=-1)
        return self.supervised(representation).squeeze(-1), self.distill(representation).squeeze(-1)

    def training_target(
        self,
        events,
        candidate,
        *,
        target: int,
        compressed: int,
        recent: int,
        cached_cutoff: int | None = None,
    ):
        _tensor(events, 3)
        if (
            any(type(v) is not int or v < 0 for v in (target, compressed, recent))
            or not 0 < target < events.shape[1]
        ):
            raise ValueError("valid zero-based target and nonnegative budgets required")
        cutoff = max(0, target - recent) if cached_cutoff is None else cached_cutoff
        if type(cutoff) is not int or not compressed <= cutoff <= target:
            raise ValueError("cached prefix cannot contain target or future events")
        c, u = self._encode(events), self._encode(events, runtime=True)
        z = c[:, cutoff - compressed : cutoff] if compressed else c[:, :0]
        runtime = u[:, max(0, target - recent) : target] if recent else u[:, :0]
        return self.decode(candidate, torch.cat((z, runtime), dim=1))

    def serving(self, cached, recent_events, candidates):
        """Only supplied recent raw events are encoded here, without older context."""
        _tensor(cached, 3)
        return self.decode(
            candidates, torch.cat((cached, self._encode(recent_events, runtime=True)), dim=1)
        )


def joint_loss(
    gt_logits,
    kd_logits,
    targets,
    teacher_logits,
    *,
    smoothing: float = 0.01,
    kd_weight: float = 0.15,
):
    for x in (gt_logits, kd_logits, targets, teacher_logits):
        _tensor(x, 2)
    if (
        not all(x.shape == gt_logits.shape for x in (kd_logits, targets, teacher_logits))
        or targets.numel() == 0
        or not ((targets == 0) | (targets == 1)).all()
    ):
        raise ValueError("matched nonempty binary target tensors required")
    if (
        any(isinstance(x, bool) or not math.isfinite(x) for x in (smoothing, kd_weight))
        or not 0 <= smoothing < 1
        or kd_weight < 0
    ):
        raise ValueError("valid smoothing and nonnegative KD weight required")
    soft = targets + smoothing * (1 - targets)
    return F.binary_cross_entropy_with_logits(gt_logits, soft) + kd_weight * F.l1_loss(
        kd_logits, teacher_logits.detach()
    )


def diagnostic(seed: int, device: str = "cpu") -> dict:
    if type(seed) is not int or seed < 0 or device not in {"cpu", "cuda"}:
        raise ValueError("valid seed/device required")
    torch.manual_seed(seed)
    model = XSplitMemory().to(device)
    events = torch.randn(1, 9, 8, device=device, requires_grad=True)
    candidate = torch.randn(1, 1, 8, device=device)
    gt, kd = model.training_target(events, candidate, target=6, compressed=2, recent=2)
    teacher = torch.tensor([[0.6]], device=device, requires_grad=True)
    loss = joint_loss(gt, kd, torch.ones_like(gt), teacher)
    loss.backward()
    changed = events.detach().clone()
    changed[:, 6:] += 100
    after = model.training_target(changed, candidate, target=6, compressed=2, recent=2)[0]
    cached = model._encode(events.detach())[:, 2:4]
    candidates = torch.randn(1, 3, 8, device=device)
    batch = model.serving(cached, events.detach()[:, 4:6], candidates)[0]
    one = torch.cat(
        [
            model.serving(cached, events.detach()[:, 4:6], candidates[:, i : i + 1])[0]
            for i in range(3)
        ],
        1,
    )
    return {
        "seed": seed,
        "diagnostic_only": True,
        "evaluation_tier": "l1_mechanism",
        "checks": {
            "target_future_excluded": bool(torch.allclose(gt.detach(), after, atol=1e-6)),
            "future_zero_gradient": bool((events.grad[:, 6:] == 0).all()),
            "compressor_receives_gradient": bool(
                any(
                    p.grad is not None and p.grad.abs().sum() > 0
                    for p in model.compressor.parameters()
                )
            ),
            "teacher_detached": teacher.grad is None,
            "candidate_independence": bool(torch.allclose(batch, one, atol=1e-6)),
        },
        "metrics": {
            "fixture_loss": float(loss.detach()),
            "history_gradient_norm": float(events.grad.norm()),
        },
    }
