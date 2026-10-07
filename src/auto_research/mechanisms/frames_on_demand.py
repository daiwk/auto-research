"""Extracted unchanged from auto_research.foundation_latest_20260914; stable mechanism boundary."""
from __future__ import annotations

import numpy as np

def frames_on_demand(
    caption_embedding: np.ndarray,
    query_embedding: np.ndarray,
    frame_embeddings: np.ndarray,
    *,
    maximum_frames: int,
    threshold: float = 0.35,
) -> tuple[np.ndarray, dict[str, float]]:
    """Caption-first visual-need routing with a bounded frame budget."""
    caption = np.asarray(caption_embedding, dtype=np.float64)
    query = np.asarray(query_embedding, dtype=np.float64)
    frames = np.asarray(frame_embeddings, dtype=np.float64)
    cosine = float(caption @ query / (np.linalg.norm(caption) * np.linalg.norm(query) + 1e-12))
    need_visual = cosine < threshold
    if not need_visual or maximum_frames <= 0:
        chosen = np.asarray([], dtype=np.int64)
    else:
        scores = frames @ query / (np.linalg.norm(frames, axis=1) * np.linalg.norm(query) + 1e-12)
        chosen = np.argsort(-scores)[: min(maximum_frames, len(frames))]
    return chosen, {"caption_query_similarity": cosine, "visual_need": float(need_visual), "selected_frames": float(len(chosen))}
