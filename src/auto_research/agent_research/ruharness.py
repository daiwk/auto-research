"""RuHarness: outcome-blind assessment statistics and conservative frontier.

Consumes external behavioral labels and measured outcomes. No judge, LLM
harness mutation, benchmark execution or unified Evolve integration is faked.
"""
from __future__ import annotations

import math
import numpy as np

REQUIRES_GPU_VALIDATION = False
VIOLATED, SATISFIED, NOT_APPLICABLE = 0, 1, 2


def _inputs(labels, outcomes):
    labels = np.asarray(labels)
    outcomes = np.asarray(outcomes)
    if labels.ndim != 2 or not min(labels.shape) or labels.dtype.kind not in "iu" or not np.isin(labels, [0, 1, 2]).all():
        raise ValueError("nonempty [criterion, trajectory] integer assessment labels 0/1/2 required")
    if outcomes.shape != (labels.shape[1],) or outcomes.dtype != np.bool_:
        raise ValueError("aligned Boolean external task outcomes required")
    return labels, outcomes


def contingency(labels, outcomes):
    """Return [criterion, pass/fail, violated/satisfied/N/A] counts."""
    labels, outcomes = _inputs(labels, outcomes)
    return np.array([[[np.count_nonzero((row == k) & group) for k in range(3)]
                      for group in (outcomes, ~outcomes)] for row in labels], dtype=np.int64)


def set_statistics(labels, outcomes):
    """Eq.15 unique failure coverage and Eq.16 max violation-set Jaccard.

    Empty violation unions have overlap zero (explicit local convention).
    At least one failed trajectory is required to define failure novelty.
    """
    labels, outcomes = _inputs(labels, outcomes)
    if outcomes.all():
        raise ValueError("at least one failure required for novelty")
    violated = labels == VIOLATED
    unique = violated & (violated.sum(0) == 1)[None, :] & (~outcomes)[None, :]
    novelty = unique.sum(1) / (~outcomes).sum()
    redundancy = np.zeros(len(labels), dtype=np.float64)
    for i in range(len(labels)):
        for j in range(len(labels)):
            if i != j:
                union = np.count_nonzero(violated[i] | violated[j])
                overlap = np.count_nonzero(violated[i] & violated[j]) / union if union else 0.
                redundancy[i] = max(redundancy[i], overlap)
    return novelty, redundancy


def dcp(joint):
    """Eqs.11--14, supporting posterior probability arrays [...,2,3].

    Undefined observed-count denominators are rejected, not silently smoothed.
    Posterior draws are strictly positive almost surely under Jeffreys prior.
    """
    joint = np.asarray(joint, dtype=np.float64)
    if joint.ndim < 2 or joint.shape[-2:] != (2, 3) or not np.isfinite(joint).all() or (joint < 0).any():
        raise ValueError("finite nonnegative [...,2,3] joint counts/probabilities required")
    vp, sp, _ = np.moveaxis(joint[..., 0, :], -1, 0)
    vf, sf, nf = np.moveaxis(joint[..., 1, :], -1, 0)
    denominators = (vf + sf, vp + sp, vf + sf + nf, vf + vp, vp + sp + vf + sf)
    if any((value <= 0).any() for value in denominators):
        raise ValueError("diagnostic rates undefined without applicable outcome groups / violations")
    discrimination = vf / (vf + sf) - vp / (vp + sp)
    coverage = vf / (vf + sf + nf)
    predictive = vf / (vf + vp) - (vf + sf) / (vp + sp + vf + sf)
    return discrimination, coverage, predictive


def conservative_frontier(labels, outcomes, *, active, budget: int = 10, seed: int = 42,
                          samples: int = 2000, quantile: float = .2):
    """Appendix A.4 Jeffreys-Dirichlet lower utility quantile, active only.

    Novelty and redundancy remain fixed per measured trajectory sets. NumPy's
    linear sample-quantile convention and stable index tie-break are local
    numerical choices; no outcome is passed to a behavioral judge here.
    """
    labels, outcomes = _inputs(labels, outcomes)
    active = np.asarray(active)
    if active.shape != (len(labels),) or active.dtype != np.bool_:
        raise ValueError("explicit Boolean lifecycle-active flags required")
    if type(budget) is not int or budget < 0 or type(samples) is not int or samples < 1 or type(seed) is not int:
        raise ValueError("nonnegative budget, positive sample count and integer seed required")
    if isinstance(quantile, bool) or not math.isfinite(quantile) or not 0 < quantile < 1:
        raise ValueError("quantile strictly between zero and one required")
    counts = contingency(labels, outcomes)
    novelty, redundancy = set_statistics(labels, outcomes)
    rng = np.random.default_rng(seed)
    scores = np.empty(len(labels), dtype=np.float64)
    for i, table in enumerate(counts):
        draws = rng.dirichlet(table.ravel() + .5, size=samples).reshape(samples, 2, 3)
        discrimination, coverage, predictive = dcp(draws)
        utilities = discrimination + .5 * coverage + predictive + .5 * novelty[i] - .5 * redundancy[i]
        scores[i] = np.quantile(utilities, quantile, method="linear")
    eligible = np.flatnonzero(active)
    order = eligible[np.argsort(-scores[eligible], kind="stable")][:budget]
    return {"indices": order, "scores": scores, "novelty": novelty,
            "redundancy": redundancy, "counts": counts}


def validation_update(current_score: float, candidate_scores: list[float], *, verified: list[bool],
                      epsilon: float = .05) -> int | None:
    """Eq.9--10: choose verified max and commit only at strict improvement.

    Scores must come from the same separate validation set. This function does
    not certify split isolation or perform the lightweight candidate verifier.
    """
    values = [current_score, *candidate_scores]
    if any(isinstance(x, bool) or not isinstance(x, (int, float)) or not math.isfinite(x) or not 0 <= x <= 1 for x in values):
        raise ValueError("finite validation scores in [0,1] required")
    if len(verified) != len(candidate_scores) or any(type(x) is not bool for x in verified):
        raise ValueError("aligned explicit external verifier decisions required")
    if isinstance(epsilon, bool) or not math.isfinite(epsilon) or not 0 <= epsilon < 1:
        raise ValueError("finite nonnegative acceptance threshold required")
    eligible = [i for i, flag in enumerate(verified) if flag]
    if not eligible:
        return None
    best = max(eligible, key=lambda i: candidate_scores[i])
    return best if candidate_scores[best] - current_score > epsilon else None


def diagnostic(seed: int = 42, device: str = "cpu") -> dict:
    if device != "cpu":
        raise ValueError("pure CPU statistical diagnostic; no GPU/model execution")
    labels = np.array([[1, 1, 1, 1, 0, 0, 0, 0],
                       [0, 0, 1, 1, 0, 0, 1, 1],
                       [1, 1, 1, 1, 0, 0, 0, 0],
                       [2, 2, 1, 1, 2, 2, 1, 1]])
    outcomes = np.array([True] * 4 + [False] * 4)
    result = conservative_frontier(labels, outcomes, active=[True, True, False, True], seed=seed)
    repeated = conservative_frontier(labels, outcomes, active=[True, True, False, True], seed=seed)
    d, c, p = dcp(result["counts"][0])
    return {"seed": seed, "diagnostic_only": True, "component": "ruharness_conservative_rubric_frontier",
            "metrics": {"reference_discrimination": float(d), "reference_failure_coverage": float(c),
                        "reference_predictive_validity": float(p), "frontier_size": len(result["indices"]),
                        "best_lower_quantile": float(result["scores"][result["indices"][0]]),
                        "duplicate_criterion_redundancy": float(result["redundancy"][0]),
                        "posterior_samples_per_criterion": 2000},
            "checks": {"formula_reference_counts": float(d) == 1 and float(c) == 1 and float(p) == .5,
                       "duplicate_sets_have_unit_jaccard": bool(result["redundancy"][0] == result["redundancy"][2] == 1),
                       "inactive_not_selected": 2 not in result["indices"],
                       "fixed_seed_reproducible": np.array_equal(result["scores"], repeated["scores"]),
                       "finite_conservative_scores": bool(np.isfinite(result["scores"]).all()),
                       "unverified_candidate_excluded": validation_update(.4, [.9, .5], verified=[False, True]) == 1,
                       "strict_epsilon_boundary": validation_update(0., [.05], verified=[True]) is None,
                       "no_candidate_preserves_incumbent": validation_update(.4, [], verified=[]) is None}}
