from __future__ import annotations

import numpy as np

from ..industrial_2026 import hierarchical_codes


def build_dos_scorer(data):
    """Collaborative/semantic dual flow followed by orthogonal RQ."""
    content = data.sequences.features.astype(float)
    collaborative = data.transition + data.transition.T
    u, _, _ = np.linalg.svd(collaborative, full_matrices=False)
    collaborative = u[:, : content.shape[1]]
    cross = content.T @ collaborative
    left, _, right = np.linalg.svd(cross, full_matrices=False)
    rotation = left @ right
    aligned = content @ rotation
    codes = hierarchical_codes(aligned, levels=3, width=8)
    code_similarity = (codes[:, None] == codes[None]).mean(-1)
    orthogonality_error = float(
        np.linalg.norm(rotation.T @ rotation - np.eye(rotation.shape[1]))
    )

    def scorer(history):
        recent = np.asarray(history[-10:])
        semantic_flow = code_similarity[recent].mean(0)
        collaborative_flow = data.transition[recent].mean(0)
        return 0.50 * semantic_flow + 0.50 * collaborative_flow

    return scorer, {
        "flows": ("semantic", "collaborative"),
        "orq_levels": 3,
        "rotation_orthogonality_error": orthogonality_error,
    }
