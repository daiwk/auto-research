"""Extracted unchanged from auto_research.foundation_latest_20260914; stable mechanism boundary."""
from __future__ import annotations

import numpy as np

def similarity_contracting_windows(turns: list[str], embeddings: np.ndarray, *, minimum_similarity: float = 0.25) -> list[list[str]]:
    """SWRouter segmentation: extend a window only while similarity contracts."""
    embeddings = np.asarray(embeddings, dtype=np.float64)
    if len(turns) != len(embeddings):
        raise ValueError("turns and embeddings must have equal length")
    windows: list[list[str]] = []
    for turn, vector in zip(turns, embeddings):
        if not windows:
            windows.append([turn])
            continue
        previous_index = sum(len(window) for window in windows) - 1
        previous = embeddings[previous_index]
        similarity = float(previous @ vector / (np.linalg.norm(previous) * np.linalg.norm(vector) + 1e-12))
        if similarity >= minimum_similarity:
            windows[-1].append(turn)
        else:
            windows.append([turn])
    return windows
