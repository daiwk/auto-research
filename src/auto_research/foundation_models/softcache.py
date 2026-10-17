"""SoftCache headroom-controlled off-grid sampling, equations 6--12.

The probe is explicitly supplied by the caller; this is not SeaCache's spectral
filter or a FLUX/Wan integration.  Cached states are local to each sample call.
"""
from __future__ import annotations

from dataclasses import dataclass
import math
from typing import Callable

import torch
from torch import Tensor


@dataclass(frozen=True)
class CacheTrace:
    time: float
    step: float
    fresh: bool
    accumulator: float
    probe_change: float


def residual_extrapolation(current: Tensor, previous: Tensor | None, time: float,
                           anchor_time: float, previous_time: float | None, beta: float) -> Tensor:
    if previous is None:
        return current
    if previous_time is None or anchor_time <= previous_time:
        raise ValueError("strictly ordered anchors required")
    return current + beta * (time - anchor_time) / (anchor_time - previous_time) * (current - previous)


def cached_step(time: float, scheduled: float, accumulator: float, threshold: float,
                max_jump: float, probe_change: float) -> float:
    if (not all(math.isfinite(x) for x in (time, scheduled, accumulator, threshold, max_jump, probe_change))
            or not 0 <= time < 1 or scheduled <= 0 or accumulator < 0 or threshold <= 0
            or max_jump < 1 or probe_change < 0):
        raise ValueError("invalid finite cache step parameters")
    if accumulator >= threshold or time < .1 or probe_change > .18:
        return min(scheduled, 1 - time)
    return min(1 - time, scheduled * (1 + (max_jump - 1) * (1 - accumulator / threshold)))


class SoftCacheSampler:
    def __init__(self, threshold: float = .5, max_jump: float = 3., beta: float = 1.):
        if not all(math.isfinite(x) for x in (threshold, max_jump, beta)) or threshold <= 0 or max_jump < 1 or not 0 <= beta <= 1:
            raise ValueError("positive threshold, jump >= 1, beta in [0,1] required")
        self.threshold, self.max_jump, self.beta = threshold, max_jump, beta

    def sample(self, initial: Tensor, nodes: list[float], residual: Callable[[Tensor, float], Tensor],
               readout: Callable[[Tensor, Tensor, float], Tensor],
               probe: Callable[[Tensor, float], Tensor]) -> tuple[Tensor, tuple[CacheTrace, ...]]:
        if (len(nodes) < 2 or nodes[0] != 0 or nodes[-1] != 1
                or any(not math.isfinite(t) for t in nodes)
                or any(b <= a for a, b in zip(nodes[:-1], nodes[1:], strict=True))):
            raise ValueError("strictly increasing finite 0..1 schedule required")
        x, grid, trace = initial, list(nodes), []
        previous_probe, anchor, previous_anchor = None, None, None
        anchor_time, previous_time, accumulator = 0., None, 0.
        while len(grid) > 1:
            time, scheduled = grid[0], grid[1] - grid[0]
            current_probe = probe(x, time)
            if not bool(torch.isfinite(current_probe).all()):
                raise ValueError("nonfinite probe")
            rho = (0. if previous_probe is None else float((current_probe - previous_probe).abs().sum().detach()
                   / previous_probe.abs().sum().detach().clamp_min(1e-12)))
            accumulator += rho
            fresh = anchor is None or accumulator >= self.threshold
            if fresh:
                previous_anchor, previous_time = anchor, (anchor_time if anchor is not None else None)
                anchor, anchor_time = residual(x, time), time
                accumulator, step, prediction = 0., scheduled, anchor
            else:
                prediction = residual_extrapolation(anchor, previous_anchor, time, anchor_time, previous_time, self.beta)
                step = cached_step(time, scheduled, accumulator, self.threshold, self.max_jump, rho)
            x = x + step * readout(x, prediction, time)
            if not bool(torch.isfinite(x).all()):
                raise ValueError("nonfinite sample")
            trace.append(CacheTrace(time, step, fresh, accumulator, rho))
            previous_probe = current_probe
            landing = min(1., time + step)
            tail = [value for value in grid[1:] if value > landing + 1e-12]
            if landing >= 1 - 1e-12:
                grid = [1.]
            elif step > scheduled * (1 + 1e-12) and len(tail) >= 2:
                grid = [landing + (1 - landing) * k / (len(tail) - 1) for k in range(len(tail))]
            else:
                grid = [landing] + tail
        return x, tuple(trace)
