"""MJev-Spatial native GQA readout and deterministic spatial controllers.

Independent reduced-width implementation, not a Qwen checkpoint conversion.
The final readout adds no classifier head: it owns reusable Q/K projections.
"""
from __future__ import annotations

import math

import torch
from torch import Tensor, nn
from torch.nn import functional as F


def rotary(x: Tensor, positions: Tensor) -> Tensor:
    if x.shape[-1] % 2:
        raise ValueError("even rotary head dimension required")
    frequencies = 10000. ** (-torch.arange(0, x.shape[-1], 2, device=x.device, dtype=x.dtype) / x.shape[-1])
    angle = positions[..., None, None] * frequencies
    a, b = x[..., :x.shape[-1] // 2], x[..., x.shape[-1] // 2:]
    return torch.cat((a * angle.cos() - b * angle.sin(), b * angle.cos() + a * angle.sin()), -1)


class NativeSpatialReadout(nn.Module):
    def __init__(self, width: int = 16, query_heads: int = 4, key_heads: int = 2, head_dim: int = 4,
                 *, input_norm: nn.Module | None = None, query_projection: nn.Linear | None = None,
                 key_projection: nn.Linear | None = None, query_head_norm: nn.Module | None = None,
                 key_head_norm: nn.Module | None = None):
        super().__init__()
        if min(width, query_heads, key_heads, head_dim) < 1 or query_heads % key_heads or head_dim % 2:
            raise ValueError("valid GQA dimensions and even head width required")
        self.query_heads, self.key_heads, self.head_dim = query_heads, key_heads, head_dim
        # Inject the actual final layer's objects to share its parameters, NOT
        # clone their weights or create an independent learned classifier head.
        self.norm = input_norm if input_norm is not None else nn.RMSNorm(width, eps=1e-6)
        self.query = query_projection if query_projection is not None else nn.Linear(width, query_heads * head_dim, bias=False)
        self.key = key_projection if key_projection is not None else nn.Linear(width, key_heads * head_dim, bias=False)
        self.query_norm = query_head_norm if query_head_norm is not None else nn.RMSNorm(head_dim, eps=1e-6)
        self.key_norm = key_head_norm if key_head_norm is not None else nn.RMSNorm(head_dim, eps=1e-6)
        if (self.query.in_features != width or self.query.out_features != query_heads * head_dim
                or self.key.in_features != width or self.key.out_features != key_heads * head_dim):
            raise ValueError("injected projections do not match native GQA dimensions")

    def projected(self, hidden: Tensor, decision: Tensor, ends: Tensor) -> tuple[Tensor, Tensor]:
        batch, length, _ = hidden.shape
        if (decision.shape != (batch,) or ends.ndim != 2 or ends.shape[0] != batch
                or ends.shape[1] < 1 or decision.dtype != torch.long or ends.dtype != torch.long
                or decision.device != hidden.device or ends.device != hidden.device
                or bool((decision < 0).any()) or bool((decision >= length).any())
                or bool((ends < 0).any()) or bool((ends >= decision[:, None]).any())):
            raise ValueError("candidate end indices must precede each decision marker")
        normal = self.norm(hidden)
        rows = torch.arange(batch, device=hidden.device)
        q = self.query(normal[rows, decision]).reshape(batch, 1, self.query_heads, self.head_dim)
        k = self.key(normal[rows[:, None], ends]).reshape(batch, ends.shape[1], self.key_heads, self.head_dim)
        q = self.query_norm(q)
        k = self.key_norm(k)
        return rotary(q, decision[:, None]), rotary(k, ends)

    def forward(self, hidden: Tensor, decision: Tensor, ends: Tensor) -> Tensor:
        q, k = self.projected(hidden, decision, ends)
        grouped = k.repeat_interleave(self.query_heads // self.key_heads, dim=2)
        return (q * grouped).sum(-1).mean(-1) / math.sqrt(self.head_dim)


def stage_normalized_loss(logits: list[Tensor], targets: list[int], question_ids: list[int]) -> Tensor:
    if not logits or len(logits) != len(targets) or len(logits) != len(question_ids):
        raise ValueError("aligned nonempty decisions, labels and question ids required")
    losses: dict[int, list[Tensor]] = {}
    for scores, target, question in zip(logits, targets, question_ids, strict=True):
        if scores.ndim != 1 or not 0 <= target < scores.numel() or question < 0:
            raise ValueError("invalid decision or target")
        loss = -scores.log_softmax(0)[target]
        losses.setdefault(question, []).append(loss)
    return torch.stack([torch.stack(rows).mean() for rows in losses.values()]).mean()


def encode_count(count: int) -> tuple[int, int]:
    if isinstance(count, bool) or not isinstance(count, int) or not 0 <= count <= 1023:
        raise ValueError("count must be an integer in 0..1023")
    return divmod(count, 32)


def decode_count(coarse: int, fine: int) -> int:
    if not all(isinstance(x, int) and not isinstance(x, bool) and 0 <= x < 32 for x in (coarse, fine)):
        raise ValueError("count classes must be integers in 0..31")
    return 32 * coarse + fine


def length_codebook() -> tuple[tuple[float, ...], tuple[int, ...]]:
    edges = tuple(.01 * math.expm1(j / 30 * math.log1p(16384 / .01)) for j in range(31))
    cells = tuple(next(n for n in (4, 8, 16, 32) if (b - a) / (2 * n) <= max(.01, .05 * a))
                  for a, b in zip(edges[:-1], edges[1:], strict=True))
    return edges, cells


REGION_ORDER = ((1, 0), (0, 0), (2, 0), (1, 1), (0, 1), (2, 1), (1, 2), (0, 2), (2, 2))


def refine_region(bounds: tuple[float, float, float, float], choice: int) -> tuple[float, float, float, float]:
    x0, y0, x1, y1 = bounds
    if not 0 <= x0 < x1 <= 1 or not 0 <= y0 < y1 <= 1 or not 0 <= choice < 9:
        raise ValueError("normalized nonempty bounds and legal region choice required")
    col, row = REGION_ORDER[choice]
    w, h = (x1 - x0) / 3, (y1 - y0) / 3
    return x0 + col * w, y0 + row * h, x0 + (col + 1) * w, y0 + (row + 1) * h


def crop_original(image: Tensor, bounds: tuple[float, float, float, float], size: int = 8) -> Tensor:
    """Re-encode input must come from ORIGINAL pixels, not the preceding crop."""
    if image.ndim != 3 or size < 1:
        raise ValueError("channels x height x width image and positive size required")
    x0, y0, x1, y1 = bounds
    if not 0 <= x0 < x1 <= 1 or not 0 <= y0 < y1 <= 1:
        raise ValueError("invalid bounds")
    height, width = image.shape[-2:]
    left, top = min(int(x0 * width), width - 1), min(int(y0 * height), height - 1)
    right, bottom = max(left + 1, math.ceil(x1 * width)), max(top + 1, math.ceil(y1 * height))
    return F.interpolate(image[:, top:bottom, left:right][None], (size, size), mode="bilinear", align_corners=False)[0]
