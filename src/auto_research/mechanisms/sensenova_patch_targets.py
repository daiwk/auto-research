"""Extracted unchanged from auto_research.foundation_latest_20260914; stable mechanism boundary."""
from __future__ import annotations

import numpy as np

def sensenova_patch_targets(patches: np.ndarray, mask: np.ndarray) -> np.ndarray:
    """Spatial patch-reconstruction targets without a tokenizer or VAE."""
    patches = np.asarray(patches, dtype=np.float64)
    mask = np.asarray(mask, dtype=bool)
    if patches.ndim != 3 or mask.shape != patches.shape[:2]:
        raise ValueError("patches must be [batch, tokens, dim] and mask [batch, tokens]")
    reconstructed = patches.copy()
    for row in range(len(patches)):
        visible = patches[row, ~mask[row]]
        fill = visible.mean(0) if len(visible) else np.zeros(patches.shape[-1])
        reconstructed[row, mask[row]] = fill
    return reconstructed
