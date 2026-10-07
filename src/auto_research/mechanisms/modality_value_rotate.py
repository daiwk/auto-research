"""Extracted unchanged from auto_research.foundation_latest_20260914; stable mechanism boundary."""
from __future__ import annotations

import numpy as np

def modality_value_rotate(values: np.ndarray, modalities: np.ndarray) -> tuple[np.ndarray, dict[int, np.ndarray]]:
    """Center and independently rotate each modality's value geometry."""
    values = np.asarray(values, dtype=np.float64)
    modalities = np.asarray(modalities)
    if len(values) != len(modalities):
        raise ValueError("values and modalities must have matching token counts")
    rotated = np.empty_like(values)
    rotations = {}
    for modality in np.unique(modalities):
        mask = modalities == modality
        group = values[mask]
        _, _, vh = np.linalg.svd(group - group.mean(0), full_matrices=False)
        rotation = vh.T
        if rotation.shape != (values.shape[1], values.shape[1]):
            rotation = np.eye(values.shape[1])
        rotated[mask] = group @ rotation
        rotations[int(modality)] = rotation
    return rotated, rotations
