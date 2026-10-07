"""Extracted unchanged from auto_research.foundation_latest_20260914; stable mechanism boundary."""
from __future__ import annotations

import numpy as np

def soft_musec_update(momentum: np.ndarray, *, clip: float = 1.0, softness: float = 0.2) -> tuple[np.ndarray, dict[str, float]]:
    """Smooth spectral clipping for a Muon-style matrix update."""
    matrix = np.asarray(momentum, dtype=np.float64)
    u, singular, vh = np.linalg.svd(matrix, full_matrices=False)
    clipped = clip * np.tanh(singular / max(clip * softness, 1e-12))
    update = (u * clipped) @ vh
    return update, {
        "spectral_norm_before": float(singular.max(initial=0.0)),
        "spectral_norm_after": float(clipped.max(initial=0.0)),
        "clipped_singular_values": float(np.count_nonzero(singular > clip)),
    }
