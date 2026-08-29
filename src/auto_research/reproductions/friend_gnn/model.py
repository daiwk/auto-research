from __future__ import annotations

import bisect
import numpy as np


def multi_hash_embedding(identifier: int, table: np.ndarray, hashes: int = 3) -> np.ndarray:
    """Concatenate independent shared-table rows and mean-project them."""
    rows = [((identifier + 1) * prime + 17 * slot) % len(table)
            for slot, prime in enumerate((2654435761, 2246822519, 3266489917)[:hashes])]
    return np.concatenate([table[row] for row in rows])


def temporal_prefix(neighbors: list[tuple[int, int]], cutoff: int) -> list[int]:
    """Timestamp-sorted CSR analogue using a binary-search cutoff."""
    times = [timestamp for timestamp, _ in neighbors]
    boundary = bisect.bisect_left(times, cutoff)
    return [node for _, node in neighbors[:boundary]]


def build_item_graph(train) -> tuple[dict[int, list[tuple[int, int]]], dict[int, set[int]]]:
    temporal: dict[int, list[tuple[int, int]]] = {}
    plain: dict[int, set[int]] = {}
    for history in train:
        for timestamp, (left, right) in enumerate(zip(history[:-1], history[1:]), 1):
            temporal.setdefault(left, []).append((timestamp, right))
            temporal.setdefault(right, []).append((timestamp, left))
            plain.setdefault(left, set()).add(right)
            plain.setdefault(right, set()).add(left)
    for values in temporal.values():
        values.sort()
    return temporal, plain


def score_candidates(data, history, *, use_temporal_hash: bool) -> np.ndarray:
    item_count = data.item_count
    popularity = np.bincount(
        [item for values in data.train for item in values], minlength=item_count,
    ).astype(float)
    if not use_temporal_hash:
        return np.log1p(popularity)
    temporal, plain = build_item_graph(data.train)
    cutoff = max(2, len(history) + 1)
    seed = history[-1]
    visible = set(temporal_prefix(temporal.get(seed, []), cutoff))
    table = np.random.default_rng(7).normal(0, 0.2, size=(max(32, item_count // 4), 8))
    seed_vector = multi_hash_embedding(seed, table)
    scores = np.log1p(popularity) * 0.08
    for candidate in range(item_count):
        overlap = len(plain.get(candidate, set()) & visible)
        hash_similarity = float(np.dot(seed_vector, multi_hash_embedding(candidate, table)))
        scores[candidate] += 1.8 * (candidate in visible) + 0.55 * overlap + 0.02 * hash_similarity
    return scores
