"""StepRefine entropy/soft-embedding/KL/budget primitives, not a multimodal denoiser."""
from __future__ import annotations

import numpy as np

from auto_research.foundation_models.b3 import entropy

REQUIRES_GPU_VALIDATION = False


def spike(current_change: float, preceding_changes: np.ndarray) -> bool:
    history = np.asarray(preceding_changes, dtype=float)
    if history.ndim != 1 or not len(history) or not np.isfinite(history).all() or not np.isfinite(current_change):
        raise ValueError("a finite completed history window and current entropy change are required")
    return bool(current_change > history.mean() + history.std(ddof=0))


def mask_entropy(probabilities: np.ndarray, mask: np.ndarray) -> float:
    values = entropy(probabilities)
    selected = np.asarray(mask)
    if selected.dtype != np.bool_ or selected.shape != values.shape or not selected.any():
        raise ValueError("a nonempty boolean mask aligned to positions is required")
    return float(values[selected].mean())


def soft_embeddings(probabilities: np.ndarray, embeddings: np.ndarray,
                    current_embeddings: np.ndarray, mask: np.ndarray) -> np.ndarray:
    mask_entropy(probabilities, mask)
    p, table, current = map(lambda x: np.asarray(x, dtype=float),
                            (probabilities, embeddings, current_embeddings))
    if (table.ndim != 2 or table.shape[0] != p.shape[1]
            or current.shape != (p.shape[0], table.shape[1])
            or not np.isfinite(table).all() or not np.isfinite(current).all()):
        raise ValueError("finite vocabulary embedding table and aligned current embeddings required")
    result = current.copy()
    result[mask] = p[mask] @ table
    return result


def refinement_kl(new: np.ndarray, previous: np.ndarray, mask: np.ndarray) -> float:
    mask_entropy(new, mask)
    mask_entropy(previous, mask)
    if np.shape(new) != np.shape(previous):
        raise ValueError("consecutive distributions must align")
    p, q = np.asarray(new)[mask], np.asarray(previous)[mask]
    active = p > 0
    if np.any(active & (q == 0)):
        return float("inf")
    terms = np.zeros_like(p, dtype=float)
    terms[active] = p[active] * np.log(p[active] / q[active])
    return float(terms.sum(-1).mean())


def next_denoising_index(current: int, refinement_passes: int) -> int:
    """Algorithm 1 charges the standard pass AND k additional passes: t <- t-1-k."""
    if (type(current) is not int or type(refinement_passes) is not int
            or current < 1 or not 0 <= refinement_passes < current):
        raise ValueError("refinement must fit the remaining forward-pass budget")
    return current - 1 - refinement_passes


def diagnostic(seed: int, device: str = "cpu") -> dict:
    if device != "cpu":
        raise ValueError("StepRefine numerical reference is CPU-only; no CUDA backbone is supplied")
    rng = np.random.default_rng(seed)
    old = rng.dirichlet(np.ones(9), 6)
    new = 0.999 * old + 0.001 / 9
    table = rng.normal(size=(9, 5))
    current = rng.normal(size=(6, 5))
    mask = np.array([False, True, True, False, True, True])
    replaced = soft_embeddings(old, table, current, mask)
    kl = refinement_kl(new, old, mask)
    return {"seed": seed, "diagnostic_only": True, "evaluation_tier": "l1_mechanism",
            "metrics": {"mean_mask_entropy": mask_entropy(old, mask), "refinement_forward_kl": kl,
                        "masked_positions": int(mask.sum()), "next_index_after_two_refinements": next_denoising_index(16, 2)},
            "checks": {"spike_detected_against_prior_window": spike(0.5, np.array([-0.1, -0.2, -0.15])),
                       "strict_spike_boundary": not spike(0.0, np.zeros(4)),
                       "unmasked_embeddings_preserved": bool(np.array_equal(replaced[~mask], current[~mask])),
                       "weighted_embeddings_exact": bool(np.allclose(replaced[mask], old[mask] @ table)),
                       "stable_refinement_can_stop": 0 <= kl < 0.01,
                       "refinement_charged_to_original_budget": next_denoising_index(3, 2) == 0}}
