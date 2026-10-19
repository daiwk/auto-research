"""Budget Muon's defining global MM allocation and two-sided polar oracle.

arXiv:2610.23571, Algorithm 1. This small-matrix implementation uses an exact
SVD polar factor, not the paper's approximate five-step production kernel.
It supports paired two-layer MLP matrices; it is not full LLaMA training.
"""
from __future__ import annotations

import math
from collections.abc import Iterable

import torch


def polar(matrix: torch.Tensor) -> torch.Tensor:
    """Canonical partial polar factor; zero singular directions remain zero."""
    if matrix.ndim != 2 or min(matrix.shape) < 1 or matrix.dtype not in (torch.float32, torch.float64):
        raise ValueError("nonempty FP32/FP64 matrix required")
    if not bool(torch.isfinite(matrix).all()):
        raise ValueError("finite matrix required")
    u, values, vh = torch.linalg.svd(matrix, full_matrices=False)
    threshold = torch.finfo(matrix.dtype).eps * max(matrix.shape) * values.max()
    return (u * (values > threshold).to(matrix.dtype)[None]) @ vh


def allocate_budget(scores: torch.Tensor, budget: float, *, alpha: float = .5,
                    floor: float = 1e-6) -> torch.Tensor:
    """Solve Eq.8 over *all blocks jointly*, including zero-score ties.

    Bisection is performed in log-lambda space. Zero-score channels receive the
    floor unless the budget exceeds all positive channels' capacity; any excess
    is shared among zero-score ties, also a valid maximizer of the surrogate.
    """
    if scores.ndim != 1 or scores.numel() == 0 or scores.dtype not in (torch.float32, torch.float64):
        raise ValueError("nonempty FP32/FP64 score vector required")
    n = scores.numel()
    if not all(math.isfinite(x) for x in (budget, alpha, floor)) or not 0 < alpha < 1:
        raise ValueError("finite configuration and 0 < alpha < 1 required")
    if not 0 < budget <= n or not 0 < floor < budget / n:
        raise ValueError("require 0 < floor < budget/N <= 1")
    if not bool(torch.isfinite(scores).all()) or bool((scores < 0).any()):
        raise ValueError("finite nonnegative scores required")
    with torch.no_grad():
        if budget == n:
            return torch.ones_like(scores)
        positive = scores > 0
        count = int(positive.sum())
        zeros = n - count
        result = torch.full_like(scores, floor)
        if budget >= count + zeros * floor:
            result[positive] = 1.
            if zeros:
                result[~positive] = (budget - count) / zeros
            return result
        active = scores[positive]
        target = budget - zeros * floor
        # Take logs BEFORE multiplication: subnormal FP32 scores may underflow
        # at alpha*score even though both logarithms are finite separately.
        log_a = active.log() + math.log(alpha)
        lo = log_a.min() - 1
        hi = log_a.max() - (1 - alpha) * math.log(floor) + 1
        for _ in range(80):
            middle = (lo + hi) / 2
            candidate = ((log_a - middle) / (1 - alpha)).clamp(math.log(floor), 0).exp().clamp(floor, 1.)
            if float(candidate.sum()) > target:
                lo = middle
            else:
                hi = middle
        result[positive] = ((log_a - (lo + hi) / 2) / (1 - alpha)).clamp(math.log(floor), 0).exp().clamp(floor, 1.)
        return result


def weighted_oracle(incoming: torch.Tensor, outgoing: torch.Tensor,
                    allocation: torch.Tensor, alpha: float = .5) -> tuple[torch.Tensor, torch.Tensor]:
    """Eq.5/Algorithm1: D^alpha Polar(D^alpha M1), Polar(M2 D^alpha) D^alpha."""
    if incoming.ndim != 2 or outgoing.ndim != 2 or incoming.shape[0] != outgoing.shape[1]:
        raise ValueError("paired incoming [channel,input], outgoing [output,channel] required")
    if allocation.shape != (incoming.shape[0],) or allocation.device != incoming.device:
        raise ValueError("one same-device allocation per hidden channel required")
    if outgoing.device != incoming.device or incoming.dtype != outgoing.dtype or allocation.dtype != incoming.dtype:
        raise ValueError("matrix/allocation device and dtype must match")
    if not math.isfinite(alpha) or not 0 < alpha < 1 or not bool(torch.isfinite(allocation).all()):
        raise ValueError("finite exponent/allocation required")
    if not bool(((allocation > 0) & (allocation <= 1)).all()):
        raise ValueError("allocations must be in (0,1]")
    scale = allocation.pow(alpha)
    return scale[:, None] * polar(scale[:, None] * incoming), polar(outgoing * scale[None]) * scale[None]


class BudgetMuon(torch.optim.Optimizer):
    """Paired-MLP optimizer with global allocation competition and Nesterov momentum.

    Missing gradients are rejected: silently skipping one half would change the
    channel-coupled oracle and global budget. FP16/BF16 are explicitly unsupported.
    """

    def __init__(self, blocks: Iterable[tuple[torch.Tensor, torch.Tensor]], *, budget: float,
                 lr: float = .01, momentum: float = .95, alpha: float = .5,
                 floor: float = 1e-6, allocation_period: int = 5, weight_decay: float = 0.):
        self.blocks = tuple(blocks)
        if not self.blocks:
            raise ValueError("at least one paired MLP block required")
        params = [p for pair in self.blocks for p in pair]
        if len({id(p) for p in params}) != len(params):
            raise ValueError("each parameter must belong to exactly one pair")
        sample = params[0]
        for left, right in self.blocks:
            if left.ndim != 2 or right.ndim != 2 or min(*left.shape, *right.shape) < 1 or left.shape[0] != right.shape[1]:
                raise ValueError("compatible nonempty paired MLP matrices required")
            if left.dtype not in (torch.float32, torch.float64) or right.dtype != left.dtype:
                raise ValueError("FP32/FP64 parameters required")
            if left.device != sample.device or right.device != sample.device or left.dtype != sample.dtype:
                raise ValueError("all blocks must share dtype and device")
        n = sum(left.shape[0] for left, _ in self.blocks)
        allocate_budget(sample.new_ones(n), budget, alpha=alpha, floor=floor)
        if not all(math.isfinite(x) for x in (lr, momentum, weight_decay)) or lr <= 0 or not 0 <= momentum < 1 or weight_decay < 0:
            raise ValueError("valid learning rate, momentum and weight decay required")
        if isinstance(allocation_period, bool) or not isinstance(allocation_period, int) or allocation_period < 1:
            raise ValueError("positive integer allocation period required")
        self.budget, self.alpha, self.floor = float(budget), alpha, floor
        self.allocation_period = allocation_period
        super().__init__(params, dict(lr=lr, momentum=momentum, weight_decay=weight_decay))
        for left, _ in self.blocks:
            self.state[left]["allocation"] = sample.new_full((left.shape[0],), budget / n)
        self.state[self.blocks[0][0]]["global_step"] = 0

    @property
    def steps(self) -> int:
        return int(self.state[self.blocks[0][0]]["global_step"])

    @property
    def allocations(self) -> tuple[torch.Tensor, ...]:
        return tuple(self.state[left]["allocation"].detach().clone() for left, _ in self.blocks)

    @torch.no_grad()
    def step(self, closure=None):
        loss = None
        if closure is not None:
            with torch.enable_grad():
                loss = closure()
        group = self.param_groups[0]
        for parameter in group["params"]:
            if parameter.grad is None or parameter.grad.is_sparse or not bool(torch.isfinite(parameter.grad).all()):
                raise ValueError("finite dense gradients required for every paired parameter")
        momenta = []
        for left, right in self.blocks:
            pair = []
            for parameter in (left, right):
                state = self.state[parameter]
                buffer = state.setdefault("momentum_buffer", torch.zeros_like(parameter))
                buffer.mul_(group["momentum"]).add_(parameter.grad)
                pair.append(parameter.grad + group["momentum"] * buffer)
            momenta.append(tuple(pair))
        if self.steps % self.allocation_period == 0:
            scores = []
            for (left, _), (m1, m2) in zip(self.blocks, momenta, strict=True):
                scale = self.state[left]["allocation"].pow(self.alpha)
                p1, p2 = polar(scale[:, None] * m1), polar(m2 * scale[None])
                scores.append(((m1 * p1).sum(1) + (m2 * p2).sum(0)).clamp_min(0))
            allocation = allocate_budget(torch.cat(scores), self.budget, alpha=self.alpha, floor=self.floor)
            offset = 0
            for left, _ in self.blocks:
                self.state[left]["allocation"].copy_(allocation[offset:offset + left.shape[0]])
                offset += left.shape[0]
        for (left, right), (m1, m2) in zip(self.blocks, momenta, strict=True):
            directions = weighted_oracle(m1, m2, self.state[left]["allocation"], self.alpha)
            for parameter, direction in zip((left, right), directions, strict=True):
                parameter.mul_(1 - group["lr"] * group["weight_decay"]).add_(direction, alpha=-group["lr"])
        self.state[self.blocks[0][0]]["global_step"] += 1
        return loss
