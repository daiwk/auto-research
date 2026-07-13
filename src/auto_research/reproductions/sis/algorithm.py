from __future__ import annotations

from dataclasses import dataclass

import numpy as np


@dataclass(frozen=True)
class SISResult:
    method: str
    samples: int
    top_k: int
    acceptance_rate: float
    weight_variance: float
    mean_abs_log_ratio: float
    effective_sample_size: float


def sis_topk_weight(
    target: np.ndarray,
    behavior: np.ndarray,
    token: int,
    top_k: int,
    rng: np.random.Generator,
) -> tuple[float, bool]:
    """Algorithm 1 of arXiv:2607.04728 for one token position."""
    ratio = float(target[token] / behavior[token])
    size = min(top_k, len(behavior))
    top = np.argpartition(behavior, -size)[-size:]
    if token not in top:
        return ratio, False
    envelope = float(np.max(target[top] / behavior[top]))
    accepted = bool(rng.random() < min(1.0, ratio / envelope))
    return (1.0 if accepted else ratio), accepted


def weight_stats(
    method: str, weights: list[float], acceptance: float, samples: int, top_k: int
) -> SISResult:
    values = np.asarray(weights, dtype=np.float64)
    ess = float(values.sum() ** 2 / np.square(values).sum())
    return SISResult(
        method=method,
        samples=samples,
        top_k=top_k,
        acceptance_rate=acceptance,
        weight_variance=float(values.var()),
        mean_abs_log_ratio=float(np.abs(np.log(np.maximum(values, 1e-12))).mean()),
        effective_sample_size=ess,
    )
