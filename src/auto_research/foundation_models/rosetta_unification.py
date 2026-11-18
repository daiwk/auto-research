"""Similarity-block arithmetic for the Rosetta unification probe (2508.11017 §5).

The caller supplies fact-grouped representations and the same-language baseline.
This does not invent a hidden-state extractor or reproduce the 110-run study.
"""
from __future__ import annotations

import numpy as np

REQUIRES_GPU_VALIDATION = False


def average_cosine(left: np.ndarray, right: np.ndarray) -> float:
    a, b = np.asarray(left, dtype=float), np.asarray(right, dtype=float)
    if a.ndim != 2 or b.ndim != 2 or not a.shape[0] or not b.shape[0] or a.shape[1] != b.shape[1] or not a.shape[1] or not np.isfinite(a).all() or not np.isfinite(b).all():
        raise ValueError("nonempty finite compatible representation sets required")
    an, bn = np.linalg.norm(a, axis=1), np.linalg.norm(b, axis=1)
    if np.any(an == 0) or np.any(bn == 0):
        raise ValueError("cosine is undefined for zero representations")
    return float(((a / an[:, None]) @ (b / bn[:, None]).T).mean())


def unification_score(groups: list[tuple[np.ndarray, np.ndarray, np.ndarray]]) -> float:
    """Mean of per-group ratios, not ratio of global means.

    Each tuple is (X,Y,baseline_X): semantic equivalents across languages X/Y
    and externally specified same-language comparison points baseline_X.
    Ambiguous fact/baseline construction is not silently guessed from labels.
    The original notation sim(X,X) names a same-language set baseline, not
    merely self-cosine of a single representation (which would always be one).
    """
    if not groups:
        raise ValueError("at least one explicitly grouped comparison required")
    ratios = []
    for x, y, baseline in groups:
        denominator = average_cosine(x, baseline)
        if abs(denominator) < 1e-12:
            raise ValueError("unification denominator is zero or numerically unstable")
        ratios.append(average_cosine(x, y) / denominator)
    return float(np.mean(ratios))


def diagnostic(seed: int = 42, device: str = "cpu") -> dict:
    if device != "cpu":
        raise ValueError("CPU statistical component only")
    rng = np.random.default_rng(seed)
    x = rng.normal(size=(4, 6)); y = x + .01 * rng.normal(size=x.shape)
    baseline = x + .5 * rng.normal(size=x.shape)
    score = unification_score([(x, y, baseline)])
    return {"seed": seed, "device": device, "metrics": {"unification_ratio": score, "cross_language_cosine": average_cosine(x, y)},
            "checks": {"finite_ratio": bool(np.isfinite(score)), "cosine_scale_invariant": bool(np.isclose(average_cosine(x, y), average_cosine(3*x, 2*y))), "self_set_mean_is_not_diagonal_one": average_cosine(x, x) < .999},
            "diagnostic_only": True, "evaluation_tier": "l1_mechanism"}
