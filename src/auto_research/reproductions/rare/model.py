from __future__ import annotations

import numpy as np


def rowspace_basis(router: np.ndarray) -> np.ndarray:
    """Return an orthonormal basis of the router row space."""
    _u, singular, vh = np.linalg.svd(router, full_matrices=False)
    rank = int(np.sum(singular > singular.max() * 1e-8))
    return vh[:rank].T


def nullspace_projector(router: np.ndarray) -> np.ndarray:
    basis = rowspace_basis(router)
    return np.eye(router.shape[1]) - basis @ basis.T


def route(router: np.ndarray, states: np.ndarray) -> np.ndarray:
    return np.argmax(states @ router.T, axis=1)


def rare_edit(router: np.ndarray, direction: np.ndarray) -> np.ndarray:
    projected = nullspace_projector(router) @ direction
    return projected / max(float(np.linalg.norm(projected)), 1e-12)
