"""EvalAlloc calibration/MAP and paired-selection numerical SUBCOMPONENTS.

No LLM/scaffold search, benchmark executor, warm-up MIRT fitting or two-fold
MIRT refitting is implemented. Item model/prior and cross-fitted predictions
are external fixed inputs. APIs consume sparse SEARCH observations only;
DEV/TEST outcomes and a full hidden score matrix are never accepted.
"""
from __future__ import annotations

from dataclasses import dataclass
import math

import numpy as np
from scipy.optimize import minimize
from scipy.special import expit

REQUIRES_GPU_VALIDATION = False


def _array(value, ndim):
    a = np.asarray(value, dtype=np.float64)
    if a.ndim != ndim or not a.size or not np.isfinite(a).all():
        raise ValueError("nonempty finite numerical array required")
    return a


def _counts(value):
    # Validate integer magnitudes BEFORE conversion: Python/int64 2**53+1
    # must not silently round down to an apparently valid float64 count.
    raw = np.asarray(value)
    if raw.ndim != 1 or not raw.size or raw.dtype.kind not in "iuf" or not np.isfinite(raw).all() or np.any(raw < 0) or np.any(raw > 2**53):
        raise ValueError("finite nonnegative exactly representable count <=2**53 required")
    result = raw.astype(np.float64)
    if np.any(result != np.floor(result)):
        raise ValueError("integer observation count required")
    return result


def informativeness(full_credit_counts, observation_counts, *, z=2.):
    """Eqs.2--3: closed Beta moments of p(1-p), not Bernoulli variance alone.

    Only outcomes exactly equal to1 increment a_i; fractional credit counts
    as a failure for acquisition, but remains fractional in response fitting.
    Negative lower-confidence scores are retained, not clipped to zero.
    """
    a, n = _counts(full_credit_counts), _counts(observation_counts)
    if a.shape != n.shape or np.any(a < 0) or np.any(n < a) or np.any(a != np.floor(a)) or np.any(n != np.floor(n)):
        raise ValueError("aligned integer 0 <= successes <= observations required")
    if isinstance(z, bool) or not math.isfinite(z) or z < 0:
        raise ValueError("nonnegative finite uncertainty multiplier required")
    alpha, beta = a + 1, n - a + 1
    total = alpha + beta
    mean = alpha * beta / (total * (total + 1))
    second = alpha * (alpha + 1) * beta * (beta + 1) / (total * (total + 1) * (total + 2) * (total + 3))
    variance = np.maximum(second - mean * mean, 0.)
    with np.errstate(over="ignore", invalid="ignore"):
        result = 4 * (mean - z * np.sqrt(variance))
    if not np.isfinite(result).all():
        raise ValueError("information posterior moments are not representable")
    return result


def shared_core(scores, *, size: int):
    values = _array(scores, 1)
    if type(size) is not int or not 0 <= size <= len(values):
        raise ValueError("core size within item population required")
    return tuple(np.lexsort((np.arange(len(values)), -values))[:size].tolist())


def acquire(scores, core: tuple[int, ...], *, total: int, temperature=.001, seed: int):
    """Eq.5: unchanged common core plus Gumbel-top-k without replacement."""
    values = _array(scores, 1)
    if len(set(core)) != len(core) or any(type(i) is not int or not 0 <= i < len(values) for i in core):
        raise ValueError("distinct SEARCH item indices required")
    if type(total) is not int or not len(core) <= total <= len(values) or type(seed) is not int:
        raise ValueError("total sparse budget and integer seed required")
    if isinstance(temperature, bool) or not math.isfinite(temperature) or temperature <= 0:
        raise ValueError("positive finite Gumbel temperature required")
    remaining = np.array([i for i in range(len(values)) if i not in core], dtype=int)
    logits = values[remaining] / temperature
    if not np.isfinite(logits).all():
        raise ValueError("acquisition logits must be representable")
    random = np.random.default_rng(seed).gumbel(size=len(remaining))
    order = np.lexsort((remaining, -(logits + random)))
    return tuple(core) + tuple(remaining[order[:total - len(core)]].tolist())


@dataclass(frozen=True)
class FrozenItemModel:
    """Eq.4 fixed item reference and externally fitted Gaussian candidate prior."""
    item_intercepts: np.ndarray
    item_loadings: np.ndarray
    prior_mean: np.ndarray
    prior_covariance: np.ndarray
    fit_candidates: frozenset[str]

    def __post_init__(self):
        intercept = _array(self.item_intercepts, 1)
        loadings, mean, covariance = _array(self.item_loadings, 2), _array(self.prior_mean, 1), _array(self.prior_covariance, 2)
        if loadings.shape[0] != len(intercept) or len(mean) != loadings.shape[1] + 1 or covariance.shape != (len(mean), len(mean)):
            raise ValueError("aligned fixed items and [bias,latent] prior required")
        if not np.allclose(covariance, covariance.T, rtol=0, atol=1e-12):
            raise ValueError("symmetric positive definite prior covariance required")
        try:
            np.linalg.cholesky(covariance)
        except np.linalg.LinAlgError as error:
            raise ValueError("positive definite prior covariance required") from error
        if not self.fit_candidates or any(not isinstance(c, str) or not c for c in self.fit_candidates):
            raise ValueError("external training-candidate provenance required")
        object.__setattr__(self, "fit_candidates", frozenset(self.fit_candidates))
        for key, value in (("item_intercepts", intercept), ("item_loadings", loadings), ("prior_mean", mean), ("prior_covariance", covariance)):
            frozen = value.copy()
            frozen.flags.writeable = False
            object.__setattr__(self, key, frozen)


def infer_candidate(model: FrozenItemModel, candidate: str, observations: dict[int, float]):
    """Sec5.1 MAP: optimize candidate parameters only under frozen reference.

    item_intercepts includes global mu+eta_i. Local L-BFGS tolerance/iteration
    cap is numerical configuration, not a recovered author implementation.
    """
    if not isinstance(candidate, str) or not candidate or candidate in model.fit_candidates:
        raise ValueError("a new candidate, not an external item-model training candidate, required")
    if not observations or any(type(i) is not int or not 0 <= i < len(model.item_intercepts) for i in observations):
        raise ValueError("sparse observed SEARCH indices required")
    indices = np.array(list(observations), dtype=int)
    y = _array(list(observations.values()), 1)
    if np.any((y < 0) | (y > 1)):
        raise ValueError("observed fractional outcomes in [0,1] required")
    design = np.column_stack((np.ones(len(indices)), model.item_loadings[indices]))
    precision = np.linalg.inv(model.prior_covariance)
    if not np.isfinite(precision).all():
        raise ValueError("prior precision is not representable")

    def objective(theta):
        with np.errstate(over="ignore", invalid="ignore"):
            logit = model.item_intercepts[indices] + design @ theta
            delta = theta - model.prior_mean
        if not np.isfinite(logit).all() or not np.isfinite(delta).all():
            raise ValueError("MAP logits/parameter displacement are not representable")
        with np.errstate(over="ignore", invalid="ignore"):
            loss = np.logaddexp(0, logit).sum() - y @ logit + .5 * delta @ precision @ delta
            gradient = design.T @ (expit(logit) - y) + precision @ delta
        if not math.isfinite(loss) or not np.isfinite(gradient).all():
            raise ValueError("MAP objective/gradient are not representable")
        return loss, gradient

    result = minimize(objective, model.prior_mean.copy(), jac=True, method="L-BFGS-B", options={"maxiter": 200, "ftol": 1e-12, "gtol": 1e-8})
    if not result.success or not np.isfinite(result.x).all():
        raise ValueError("MAP optimization did not converge; no fallback score")
    all_design = np.column_stack((np.ones(len(model.item_intercepts)), model.item_loadings))
    with np.errstate(over="ignore", invalid="ignore"):
        logits = model.item_intercepts + all_design @ result.x
    if not np.isfinite(logits).all():
        raise ValueError("prediction logits are not representable; sigmoid(inf) is not validation")
    predictions = expit(logits)
    return predictions, result.x


def completed_fitness(predictions, observations: dict[int, float]):
    """Eq.6: observed cells replace predictions, never predict over known data."""
    q = _array(predictions, 1)
    if np.any((q < 0) | (q > 1)) or not observations or any(type(i) is not int or not 0 <= i < len(q) for i in observations):
        raise ValueError("valid SEARCH predictions and sparse observations required")
    values = _array(list(observations.values()), 1)
    if np.any((values < 0) | (values > 1)):
        raise ValueError("fractional observed scores in [0,1] required")
    return float((q.sum() + sum(value - q[i] for i, value in observations.items())) / len(q))


def regression_adjusted_scores(outcomes: dict[str, dict[int, float]], predictions: dict[str, np.ndarray],
                               trained_on: dict[str, frozenset[str]], *, first_round: bool):
    """Eqs.7--9: union-mean first, clipped pooled slope on later rounds.

    Predictions must be externally cross-fitted: candidate c must not train
    the item model used for c. This provenance check is not proof that an
    arbitrary external provider actually fitted the declared folds.
    """
    if not outcomes or set(outcomes) != set(predictions) or set(outcomes) != set(trained_on) or type(first_round) is not bool:
        raise ValueError("same nonempty survivors and explicit round type required")
    numerator, denominator, rows = 0., 0., {}
    size = None
    for candidate, observations in outcomes.items():
        q = _array(predictions[candidate], 1)
        if size is None:
            size = len(q)
        if len(q) != size or (candidate in trained_on[candidate] and len(observations) < size) or not trained_on[candidate]:
            raise ValueError("aligned external cross-fitted item predictions required")
        completed_fitness(q, observations)  # validates indices/ranges
        y = np.asarray(list(observations.values()), dtype=float)
        observed_q = q[list(observations)]
        numerator += float((y - y.mean()) @ (observed_q - observed_q.mean()))
        denominator += float((observed_q - observed_q.mean()) @ (observed_q - observed_q.mean()))
        rows[candidate] = (float(y.mean()), float(q.mean() - observed_q.mean()))
    if not math.isfinite(numerator) or not math.isfinite(denominator):
        raise ValueError("pooled regression moments are not representable")
    raw_slope = 0. if first_round or denominator == 0 else numerator / denominator
    if not math.isfinite(raw_slope):
        raise ValueError("pooled slope is not representable")
    slope = float(np.clip(raw_slope, 0, 1.5))
    scores = {candidate: mean + slope * correction for candidate, (mean, correction) in rows.items()}
    if not all(math.isfinite(value) for value in scores.values()):
        raise ValueError("regression-adjusted fitness is not representable")
    return scores, slope


def missing_cells(cached: dict[str, dict[int, float]], shared_prefix: tuple[int, ...], *, n_items: int):
    """Sec5.3 union: retain search observations; execute ONLY missing prefix cells.

    One paired round's allocation, not a complete SH/search controller. The
    caller must preflight this count against remaining execution budget.
    """
    if type(n_items) is not int or n_items < 1 or len(set(shared_prefix)) != len(shared_prefix) or any(
        type(i) is not int or not 0 <= i < n_items for i in shared_prefix
    ):
        raise ValueError("valid common SEARCH prefix required")
    if not cached or any(not isinstance(c, str) or not c for c in cached):
        raise ValueError("nonempty candidate cache required")
    for observations in cached.values():
        if any(type(i) is not int or not 0 <= i < n_items or not math.isfinite(y) or not 0 <= y <= 1 for i, y in observations.items()):
            raise ValueError("valid sparse SEARCH cache required")
    return tuple((candidate, item) for candidate in sorted(cached) for item in shared_prefix if item not in cached[candidate])


def plan_paired_round(cached, shared_prefix, *, n_items: int, remaining_budget: int):
    """Preflight exact additional cell cost; never silently exceed a budget."""
    if type(remaining_budget) is not int or remaining_budget < 0:
        raise ValueError("nonnegative integer remaining cell budget required")
    planned = missing_cells(cached, shared_prefix, n_items=n_items)
    if len(planned) > remaining_budget:
        raise ValueError("insufficient budget for complete paired round; execute nothing")
    return planned


def accept_round_results(cached, planned, results):
    """Only actually requested SEARCH results enter a copied immutable-round cache."""
    if len(set(planned)) != len(planned) or set(results) != set(planned):
        raise ValueError("one measured result per planned cell, no hidden extra cells")
    updated = {candidate: dict(values) for candidate, values in cached.items()}
    for candidate, item in planned:
        value = results[candidate, item]
        if candidate not in updated or item in updated[candidate] or isinstance(value, bool) or not math.isfinite(value) or not 0 <= value <= 1:
            raise ValueError("new finite measured result in [0,1] required")
        updated[candidate][item] = float(value)
    return updated


def diagnostic(seed: int = 42, device: str = "cpu"):
    if type(seed) is not int or device != "cpu":
        raise ValueError("pure CPU numerical/control component")
    counts, totals = [1, 5, 10, 0, 8, 2], [10] * 6
    info = informativeness(counts, totals)
    core = shared_core(info, size=2)
    acquired = acquire(info, core, total=4, seed=seed)
    model = FrozenItemModel(np.linspace(-1, 1, 6), np.array([[1, 0], [0, 1], [1, 1], [-1, 0], [0, -1], [-1, -1.]]), np.zeros(3), np.eye(3), frozenset({"warmup"}))
    before = model.item_intercepts.copy()
    observed = {0: 1., 2: .5}
    pred, parameters = infer_candidate(model, "new", observed)
    cached = {"a": {0: .1, 4: .5}, "b": {0: .8, 2: 1.}}
    missing = missing_cells(cached, (0, 1, 2), n_items=6)
    q = {"a": pred, "b": 1 - pred}
    training = {"a": frozenset({"warmup", "b"}), "b": frozenset({"warmup", "a"})}
    scores, slope = regression_adjusted_scores(cached, q, training, first_round=False)
    complete = {"a": {i: float(i / 5) for i in range(6)}, "b": {i: float(1 - i / 5) for i in range(6)}}
    full_scores, _ = regression_adjusted_scores(complete, q, training, first_round=False)
    rejected = 0
    for operation in (
        lambda: plan_paired_round(cached, (0, 1, 2), n_items=6, remaining_budget=len(missing) - 1),
        lambda: regression_adjusted_scores(cached, q, {"a": frozenset({"a"}), "b": frozenset({"a"})}, first_round=False),
        lambda: accept_round_results(cached, missing, {**{cell: .5 for cell in missing}, ("a", 999): 1.}),
    ):
        try:
            operation()
        except ValueError:
            rejected += 1
    return {"seed": seed, "diagnostic_only": True,
        "metrics": {"information_score_max": float(info.max()), "completed_fitness": completed_fitness(pred, observed),
                    "map_parameter_norm": float(np.linalg.norm(parameters)), "missing_execution_cells": len(missing),
                    "regression_slope": slope, "adjusted_score_a": scores["a"], "rejected_negative_controls": rejected},
        "checks": {"common_core_preserved": acquired[:2] == core,
                   "acquisition_without_replacement": len(set(acquired)) == 4,
                   "item_parameters_frozen_during_MAP": bool(np.array_equal(before, model.item_intercepts)),
                   "MAP_predictions_finite": bool(np.isfinite(pred).all()),
                   "cached_cells_not_reexecuted": all(i not in cached[c] for c, i in missing),
                   "search_union_cache_preserved": 4 in cached["a"],
                   "pooled_slope_clipped": 0 <= slope <= 1.5,
                   "full_observation_correction_zero": abs(full_scores["a"] - .5) < 1e-12 and abs(full_scores["b"] - .5) < 1e-12,
                   "budget_self_fit_and_hidden_cells_refused": rejected == 3}}
