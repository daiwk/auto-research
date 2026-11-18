"""Spool v1 §3: exact recorded-input affine summaries, not full-backbone replay."""

from __future__ import annotations

import torch
from torch import Tensor

REQUIRES_GPU_VALIDATION = True
GPU_VALIDATION_ARTIFACT = "docs/gpu-validations/spool-a100-20261118-latest.json"


def merge(left: tuple[Tensor, Tensor], right: tuple[Tensor, Tensor]) -> tuple[Tensor, Tensor]:
    """Residual chronological composition: left THEN right, never commuted."""
    d1, b1 = left
    d2, b2 = right
    return d1 + d2 + d1 @ d2, b1 + b1 @ d2 + b2


def apply(summary: tuple[Tensor, Tensor], state: Tensor) -> Tensor:
    d, b = summary
    return state + state @ d + b


def gdn_summary(keys: Tensor, values: Tensor, alpha: Tensor, beta: Tensor) -> tuple[Tensor, Tensor]:
    if (
        keys.ndim != 2
        or values.ndim != 2
        or keys.shape[0] != values.shape[0]
        or alpha.shape != keys.shape[:1]
        or beta.shape != alpha.shape
    ):
        raise ValueError("[T,Dk], [T,Dv], [T] gates required")
    if not all(bool(torch.isfinite(x).all()) for x in (keys, values, alpha, beta)):
        raise ValueError("finite recorded coefficients required")
    eye = torch.eye(keys.shape[-1], device=keys.device, dtype=keys.dtype)
    result = (torch.zeros_like(eye), values.new_zeros(values.shape[-1], keys.shape[-1]))
    for key, value, a, b in zip(keys, values, alpha, beta):
        transition = a * (eye - b * key[:, None] @ key[None])
        result = merge(result, (transition - eye, b * value[:, None] @ key[None]))
    return result


class WindowTree:
    """Cyclic segment tree with explicit expiry and O(log W) chronological queries."""

    def __init__(self, capacity: int, prototype: tuple[Tensor, Tensor]):
        if capacity < 1:
            raise ValueError("positive window required")
        self.capacity, self.size = capacity, 1 << (capacity - 1).bit_length()
        self.identity = tuple(torch.zeros_like(x) for x in prototype)
        self.tree = [self.identity for _ in range(2 * self.size)]
        self.head = self.length = 0

    def expire(self, count: int = 1) -> None:
        if not 0 <= count <= self.length:
            raise ValueError("expiry exceeds retained window")
        self.head = (self.head + count) % self.capacity
        self.length -= count

    def append(self, summary: tuple[Tensor, Tensor]) -> None:
        if self.length == self.capacity:
            self.expire()
        index = (self.head + self.length) % self.capacity + self.size
        self.tree[index] = summary
        while index > 1:
            index //= 2
            self.tree[index] = merge(self.tree[2 * index], self.tree[2 * index + 1])
        self.length += 1

    def _range(self, start: int, end: int) -> tuple[Tensor, Tensor]:
        left = right = self.identity
        start += self.size
        end += self.size
        while start < end:
            if start % 2:
                left = merge(left, self.tree[start])
                start += 1
            if end % 2:
                end -= 1
                right = merge(self.tree[end], right)
            start //= 2
            end //= 2
        return merge(left, right)

    def state(self, anchor: Tensor) -> Tensor:
        end = self.head + self.length
        first = self._range(self.head, min(end, self.capacity))
        summary = (
            merge(first, self._range(0, end - self.capacity)) if end > self.capacity else first
        )
        return apply(summary, anchor)


def diagnostic(seed: int, device: str = "cpu") -> dict:
    torch.manual_seed(seed)
    anchor = torch.randn(3, 4, device=device, dtype=torch.float64)
    summaries = []
    for _ in range(9):
        keys = torch.nn.functional.normalize(
            torch.randn(3, 4, device=device, dtype=anchor.dtype), dim=-1
        )
        values = torch.randn(3, 3, device=device, dtype=anchor.dtype)
        summaries.append(
            gdn_summary(
                keys,
                values,
                torch.full((3,), 0.98, device=device),
                torch.full((3,), 0.1, device=device),
            )
        )
    tree = WindowTree(4, summaries[0])
    maximum = 0.0
    for index, summary in enumerate(summaries):
        tree.append(summary)
        replay = anchor
        for retained in summaries[max(0, index - 3) : index + 1]:
            replay = apply(retained, replay)
        maximum = max(maximum, float((tree.state(anchor) - replay).abs().max()))
    ordered = apply(merge(summaries[0], summaries[1]), anchor)
    reversed_order = apply(merge(summaries[1], summaries[0]), anchor)
    return {
        "seed": seed,
        "diagnostic_only": True,
        "evaluation_tier": "l1_mechanism",
        "metrics": {"window_replay_max_error": maximum},
        "checks": {
            "cyclic_window_matches_recorded_replay": maximum < 1e-10,
            "order_is_not_commutative": bool(not torch.allclose(ordered, reversed_order)),
            "expired_blocks_excluded": tree.length == 4,
        },
    }
