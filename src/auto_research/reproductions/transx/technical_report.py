"""Bounded exact operators from TransX report §5.2 and Appendix A (2610.20913).

This is separate from the old NumPy illustrative scorer. It implements exact
multi-cutoff pooling/gradient sharing and row-wise Adagrad, not LinkedIn serving.
"""
from __future__ import annotations

from dataclasses import dataclass

import torch
from torch import Tensor


@dataclass(frozen=True)
class PoolState:
    maximum: Tensor
    normalizer: Tensor
    weighted: Tensor

    @classmethod
    def from_tokens(cls, values: Tensor, scores: Tensor) -> PoolState:
        if values.ndim != 2 or scores.shape != values.shape[:1] or not len(values):
            raise ValueError("nonempty values[N,D] and scores[N] required")
        maximum = scores.max()
        weights = (scores - maximum).exp()
        return cls(maximum, weights.sum(), (weights[:, None] * values).sum(0))

    def merge(self, other: PoolState) -> PoolState:
        maximum = torch.maximum(self.maximum, other.maximum)
        left = (self.maximum - maximum).exp()
        right = (other.maximum - maximum).exp()
        return PoolState(maximum, left * self.normalizer + right * other.normalizer,
                         left * self.weighted + right * other.weighted)

    def readout(self) -> Tensor:
        return self.weighted / self.normalizer


def memory_layout(cutoffs: list[int], *, length: int, local_width: int,
                  global_blocks: int) -> list[tuple[list[tuple[int, int]], tuple[int, int]]]:
    if length < 0 or local_width < 1 or global_blocks < 1:
        raise ValueError("invalid memory budget")
    layouts = []
    for cutoff in cutoffs:
        if type(cutoff) is not int or not 0 <= cutoff <= length:
            raise ValueError("cutoffs must be integer prefix lengths in [0,L]")
        before = max(0, cutoff - local_width)
        count = min(before, global_blocks)
        boundaries = [i * before // count for i in range(count + 1)] if count else [0]
        blocks = list(zip(boundaries[:-1], boundaries[1:], strict=True))
        layouts.append((blocks, (before, cutoff)))
    return layouts


def multi_cutoff_memory(values: Tensor, scores: Tensor, cutoffs: list[int], *,
                        local_width: int = 4, global_blocks: int = 3,
                        shared: bool = True) -> tuple[list[Tensor], dict[str, int]]:
    """Reuse atomic segment sufficient states, with identical gradients to direct pooling.

    All segmentation depends on supplied prefix lengths, never label/candidate
    values. Atomic states are built once; a memoized binary interval tree merges
    them. Candidate fanout can consume each materialized memory without encoding
    the history again. No assertion of distributed speedup is made.
    """
    if values.ndim != 2 or scores.shape != values.shape[:1]:
        raise ValueError("values[N,D] and scores[N] required")
    layouts = memory_layout(cutoffs, length=len(values), local_width=local_width, global_blocks=global_blocks)
    intervals = {block for blocks, _ in layouts for block in blocks}
    boundaries = sorted({index for block in intervals for index in block})
    cache: dict[tuple[int, int], PoolState] = {}
    atomic_tokens = 0
    if shared:
        for start, end in zip(boundaries[:-1], boundaries[1:], strict=True):
            cache[(start, end)] = PoolState.from_tokens(values[start:end], scores[start:end])
            atomic_tokens += end - start

    def read(start: int, end: int) -> PoolState:
        key = (start, end)
        if key in cache:
            return cache[key]
        interior = [x for x in boundaries if start < x < end]
        if not interior:
            result = PoolState.from_tokens(values[start:end], scores[start:end])
        else:
            middle = interior[len(interior) // 2]
            result = read(start, middle).merge(read(middle, end))
        cache[key] = result
        return result

    output = []
    for blocks, (start, end) in layouts:
        global_values = [(read(a, b) if shared else PoolState.from_tokens(values[a:b], scores[a:b])).readout()
                         for a, b in blocks]
        global_tensor = torch.stack(global_values) if global_values else values[:0]
        output.append(torch.cat((global_tensor, values[start:end]), 0))
    return output, {"atomic_tokens_pooled": atomic_tokens if shared else 0,
                    "direct_tokens_pooled": sum(b - a for blocks, _ in layouts for a, b in blocks),
                    "events": len(cutoffs), "unique_global_blocks": len(intervals)}


class RowWiseAdagrad(torch.optim.Optimizer):
    """Appendix A.1; coalesce logical-step sparse gradients BEFORE squaring."""
    def __init__(self, params, lr: float = 0.01, eps: float = 1e-8):
        if lr <= 0 or eps <= 0:
            raise ValueError("positive learning rate and epsilon required")
        super().__init__(params, {"lr": lr, "eps": eps})

    @torch.no_grad()
    def step(self, closure=None):
        loss = None
        if closure is not None:
            with torch.enable_grad():
                loss = closure()
        for group in self.param_groups:
            for parameter in group["params"]:
                if parameter.ndim != 2:
                    raise ValueError("row-wise Adagrad only accepts embedding matrices")
                if parameter.grad is None:
                    continue
                gradient = parameter.grad
                if not gradient.is_sparse or gradient.sparse_dim() != 1:
                    raise ValueError("use row-sparse complete logical-step gradients")
                gradient = gradient.coalesce()
                indices, values = gradient.indices()[0], gradient.values()
                state = self.state[parameter]
                if "sum" not in state:
                    state["sum"] = torch.zeros(parameter.shape[0], device=parameter.device, dtype=parameter.dtype)
                accumulator = state["sum"]
                accumulator.index_add_(0, indices, values.square().mean(-1))
                update = values / (accumulator[indices].sqrt()[:, None] + group["eps"])
                parameter.index_add_(0, indices, update, alpha=-group["lr"])
        return loss
