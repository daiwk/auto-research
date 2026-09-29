"""ActKV Algorithm 2 confidence monitor and adaptive KV budget.

This is the model-independent budget policy. It does not calculate attention
from paged KV or perform CUDA compaction, so it is not an end-to-end ActKV run.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import ceil

import numpy as np


@dataclass(frozen=True)
class BudgetDecision:
    budget: int
    confidence_slope: float
    trace_confidence: tuple[float, ...]


def confidence_budget(
    token_probabilities: np.ndarray,
    *,
    budget: int,
    budget_upper: int,
    scale_up: float = 1.5,
    top_k: int = 5,
    window: int = 8,
    stride: int = 2,
    bottom_fraction: float = 0.5,
) -> BudgetDecision:
    """Raise the budget when low-confidence regions trend downward.

    Each row contains the model's full next-token probability distribution.
    The paper writes token *surprisal* as ``-mean(log(top-k P))`` but also says
    a negative slope denotes falling confidence. We negate that surprisal
    before fitting, so a negative slope has the stated operational meaning.
    Insufficient observations leave the budget unchanged.
    """
    probabilities = np.asarray(token_probabilities, dtype=np.float64)
    if probabilities.ndim != 2 or not all(probabilities.shape):
        raise ValueError("expected nonempty [tokens, vocabulary] probabilities")
    if not np.isfinite(probabilities).all() or (probabilities < 0).any():
        raise ValueError("probabilities must be finite and nonnegative")
    if not np.allclose(probabilities.sum(axis=1), 1.0, rtol=1e-5, atol=1e-6):
        raise ValueError("each token distribution must sum to one")
    if not 1 <= top_k <= probabilities.shape[1]:
        raise ValueError("top_k exceeds the vocabulary")
    if not 1 <= budget <= budget_upper or scale_up < 1 or window < 1 or stride < 1:
        raise ValueError("invalid budget or window configuration")
    if not 0 < bottom_fraction <= 1:
        raise ValueError("bottom_fraction must be in (0, 1]")

    top = np.partition(probabilities, -top_k, axis=1)[:, -top_k:]
    # The sign is confidence (higher is better), not the paper's surprisal.
    token_confidence = np.log(np.clip(top, np.finfo(float).tiny, 1)).mean(axis=1)
    pooled = np.array([
        token_confidence[start:start + window].min()
        for start in range(0, len(token_confidence) - window + 1, stride)
    ])
    if len(pooled) < 2:
        return BudgetDecision(budget, 0.0, tuple(float(value) for value in pooled))
    threshold = np.quantile(pooled, bottom_fraction)
    trace = pooled[pooled <= threshold]
    if len(trace) < 2:
        return BudgetDecision(budget, 0.0, tuple(float(value) for value in trace))
    slope = float(np.polyfit(np.arange(len(trace)), trace, 1)[0])
    allocated = min(budget_upper, ceil(budget * scale_up)) if slope < 0 else budget
    return BudgetDecision(allocated, slope, tuple(float(value) for value in trace))
