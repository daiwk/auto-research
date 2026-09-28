"""DeltaS state-drift KV selection (arXiv:2609.27470, Eq. 3 / Algorithm 1).

The input states must come from an actual gated-linear-attention model. This
module does not manufacture them from video embeddings or inspect a question.
"""

from __future__ import annotations

from dataclasses import dataclass
import math

import numpy as np


def state_drift(before, after, *, epsilon: float = 1e-12) -> float:
    """Mean layer-wise relative Frobenius change across recurrent states."""
    if len(before) != len(after) or not before or epsilon <= 0:
        raise ValueError("matching nonempty state sequences and positive epsilon required")
    terms = []
    for left, right in zip(before, after):
        left = np.asarray(left, dtype=np.float64)
        right = np.asarray(right, dtype=np.float64)
        if left.shape != right.shape or not np.isfinite(left).all() or not np.isfinite(right).all():
            raise ValueError("state shape or finiteness mismatch")
        terms.append(float(np.linalg.norm(right - left) / max(np.linalg.norm(left), epsilon)))
    return float(np.mean(terms))


@dataclass(frozen=True)
class TokenScore:
    position: int
    chunk: int
    score: float


def retain_positions(
    tokens: tuple[TokenScore, ...], *, budget: int, sinks: int, window: int,
    spans: int,
) -> tuple[int, ...]:
    """Choose bounded cache positions, retaining original positional IDs.

    Partition uses the *original chunk arrival time*, not indices in the
    current surviving cache. Underfull spans donate spare slots to the
    globally highest-scored remaining candidates.
    """
    if budget < 1 or sinks < 0 or window < 0 or spans < 1 or sinks + window > budget:
        raise ValueError("invalid cache reservation")
    if any(not math.isfinite(item.score) or item.chunk < 0 or item.position < 0 for item in tokens):
        raise ValueError("invalid token metadata")
    positions = [item.position for item in tokens]
    if positions != sorted(set(positions)):
        raise ValueError("positions must be unique and sorted")
    if len(tokens) <= budget:
        return tuple(positions)
    protected = set(positions[:sinks]) | set(positions[-window:] if window else ())
    candidates = [item for item in tokens if item.position not in protected]
    capacity = budget - len(protected)
    if not capacity:
        return tuple(sorted(protected))
    minimum = min(item.chunk for item in candidates)
    maximum = max(item.chunk for item in candidates)
    buckets: list[list[TokenScore]] = [[] for _ in range(spans)]
    for item in candidates:
        index = min(spans - 1, (item.chunk - minimum) * spans // (maximum - minimum + 1))
        buckets[index].append(item)
    quota, extra = divmod(capacity, spans)
    selected: set[int] = set()
    for index, bucket in enumerate(buckets):
        bucket.sort(key=lambda item: (-item.score, item.position))
        selected.update(item.position for item in bucket[:quota + (index < extra)])
    if len(selected) < capacity:
        remaining = sorted((item for item in candidates if item.position not in selected),
                           key=lambda item: (-item.score, item.position))
        selected.update(item.position for item in remaining[:capacity - len(selected)])
    return tuple(sorted(protected | selected))


def append_chunk(
    cache: tuple[TokenScore, ...], *, positions: tuple[int, ...], chunk: int,
    before, after, budget: int, sinks: int, window: int, spans: int,
) -> tuple[TokenScore, ...]:
    """Assign one state-drift score to all new tokens and return kept metadata."""
    if positions != tuple(sorted(set(positions))) or (cache and positions and positions[0] <= cache[-1].position):
        raise ValueError("new positions must increase strictly")
    score = state_drift(before, after)
    combined = cache + tuple(TokenScore(position, chunk, score) for position in positions)
    kept = set(retain_positions(combined, budget=budget, sinks=sinks, window=window, spans=spans))
    return tuple(item for item in combined if item.position in kept)
