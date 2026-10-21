"""Spatial ad externality grouped pseudo-disk LP/rounding core (§2.2).

This is NOT the full ad-matching reduction, payment mechanism, or 2D PTAS.
SciPy is an optional CPU LP dependency; never replaced by a greedy pseudo-LP.
"""
from __future__ import annotations

from dataclasses import dataclass
import numpy as np


@dataclass(frozen=True)
class Disk:
    center: int
    radius: float
    weight: float
    group: int


def constraints(distances, disks):
    d = np.asarray(distances, dtype=float)
    if (d.ndim != 2 or not d.shape[0] or d.shape[0] != d.shape[1]
            or not np.isfinite(d).all() or (d < 0).any() or (d > 1+1e-12).any()
            or not np.allclose(d, d.T) or not np.allclose(np.diag(d), 0)):
        raise ValueError("finite symmetric metric of diameter <= 1 required")
    if not disks or len(disks) > 256:
        raise ValueError("bounded nonempty <=256 disk core required")
    if any(not isinstance(v.center, int) or not 0 <= v.center < len(d)
           or not np.isfinite([v.radius, v.weight]).all() or not 0 <= v.radius <= 1
           or v.weight < 0 for v in disks):
        raise ValueError("valid center/radius/nonnegative weight required")
    for k in range(len(d)):
        if (d > d[:, [k]]+d[[k], :]+1e-10).any():
            raise ValueError("triangle inequality violated")
    cover = np.array([[d[c, disk.center] < disk.radius for disk in disks]
                      for c in range(len(d))], dtype=float)
    groups = sorted({v.group for v in disks})
    group_rows = np.array([[v.group == g for v in disks] for g in groups], dtype=float)
    return d, np.concatenate([cover, group_rows])


def solve_relaxation(distances, disks):
    from scipy.optimize import linprog
    _, matrix = constraints(distances, disks)
    result = linprog(-np.array([v.weight for v in disks]), A_ub=matrix,
                     b_ub=np.ones(len(matrix)), bounds=(0, 1), method="highs")
    if not result.success:
        raise RuntimeError(f"LP failed: {result.message}")
    solution = np.clip(result.x, 0, 1)
    if (matrix@solution > 1+1e-7).any():
        raise RuntimeError("solver returned infeasible point")
    return solution, float(-result.fun)


def round_solution(distances, disks, solution, *, seed):
    """Algorithm1: independent x/3, isolate against ALL sampled, thin Eq2."""
    d, matrix = constraints(distances, disks)
    x = np.asarray(solution, dtype=float)
    if (x.shape != (len(disks),) or not np.isfinite(x).all() or (x < 0).any()
            or (x > 1).any() or (matrix@x > 1+1e-7).any()):
        raise ValueError("feasible fractional LP point required")
    rng = np.random.default_rng(seed)
    sampled = rng.random(len(disks)) < x/3
    selected = []
    for i, disk in enumerate(disks):
        conflicts = np.array([j != i and (disk.group == other.group
            or d[disk.center, other.center] < other.radius) for j, other in enumerate(disks)])
        if not sampled[i] or (sampled & conflicts).any():
            continue
        probability = 1/(3*float(np.prod(1-x[conflicts]/3)))
        if probability > 1+1e-7:
            raise RuntimeError("rounding probability infeasible; no silent algorithm change")
        if rng.random() < min(1, probability):
            selected.append(i)
    return selected


def feasible_ii(distances, disks, selected):
    d, _ = constraints(distances, disks)
    if len(set(selected)) != len(selected) or any(not 0 <= i < len(disks) for i in selected):
        return False
    if len({disks[i].group for i in selected}) != len(selected):
        return False
    return all(d[disks[i].center, disks[j].center] >= disks[j].radius
               for i in selected for j in selected if i != j)
