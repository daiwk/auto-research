from __future__ import annotations

import numpy as np

from ..industrial_2026 import base_scores


def pair_scores(data, history) -> np.ndarray:
    first = base_scores(data, history)
    continuation = data.transition
    order_affinity = 0.65 * continuation + 0.35 * data.cosine
    scores = first[:, None] + 0.55 * order_affinity
    np.fill_diagonal(scores, -np.inf)
    return scores


def score_item_space(data, history) -> np.ndarray:
    return base_scores(data, history)


def score_pair_space(data, history) -> np.ndarray:
    scores = pair_scores(data, history)
    # Marginalize each first item over its strongest valid ordered partner.
    return np.max(scores, axis=1)


def decode_pairs(data, history, slate_length: int = 6) -> tuple[list[tuple[int, int]], list[int]]:
    scores = pair_scores(data, history).copy()
    used: set[int] = set(history)
    pairs: list[tuple[int, int]] = []
    while len(pairs) * 2 < slate_length:
        if used:
            index = np.asarray(sorted(used), dtype=np.int64)
            scores[index, :] = -np.inf
            scores[:, index] = -np.inf
        flat = int(np.argmax(scores))
        left, right = np.unravel_index(flat, scores.shape)
        if not np.isfinite(scores[left, right]):
            break
        pairs.append((int(left), int(right)))
        used.update((int(left), int(right)))
    return pairs, [item for pair in pairs for item in pair][:slate_length]


def psg_diagnostics(data, history, slate_length: int = 6) -> dict[str, float]:
    pairs, slate = decode_pairs(data, history, slate_length)
    return {
        "item_space_steps": int(slate_length),
        "pair_space_steps": int(len(pairs)),
        "decode_step_reduction": float(1 - len(pairs) / slate_length),
        "request_pair_vocabulary": int(data.item_count * (data.item_count - 1)),
        "generated_items": int(len(slate)),
        "duplicate_items": int(len(slate) - len(set(slate))),
    }
