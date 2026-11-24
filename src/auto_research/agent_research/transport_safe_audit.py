"""Transport-safe evaluation CPU formulas, arXiv:2611.30742v1.

This is evaluator-side arithmetic, not an evaluated agent. Unaudited labels
are represented by None and cannot enter AIPW/e-process updates. Predictions
and audit probabilities are committed before any current label is accepted.
No LLM judge, human-label collection, nuisance learner or live ranking runs.
"""
from __future__ import annotations

from dataclasses import dataclass
import math
import random

REQUIRES_GPU_VALIDATION = False


def _real(value):
    if type(value) not in (int, float) or not math.isfinite(value):
        raise ValueError("finite real scalar required")
    return float(value)


def _probability(value):
    result = _real(value)
    if not 0 <= result <= 1:
        raise ValueError("probability in [0,1] required")
    return result


def transport_bias(theta, sensitivity, specificity, target_sensitivity, target_specificity):
    q, s0, t0, sa, ta = map(_probability, (theta, sensitivity, specificity, target_sensitivity, target_specificity))
    index = s0+t0-1
    if index == 0:
        raise ValueError("uninformative scalar judge correction")
    return _real((q*(sa-s0)+(1-q)*(t0-ta))/index)


@dataclass(frozen=True)
class CrossFitPrediction:
    value: float
    held_out_fold: str
    training_folds: frozenset[str]

    def __post_init__(self):
        _probability(self.value)
        if (not isinstance(self.held_out_fold, str) or not self.held_out_fold
                or not isinstance(self.training_folds, frozenset)
                or any(not isinstance(fold, str) or not fold for fold in self.training_folds)
                or self.held_out_fold in self.training_folds):
            raise ValueError("explicit out-of-fold prediction provenance required")


def aipw_estimate(predictions, propensities, observed_labels, *, positivity_floor):
    """Cross-fitted AIPW summands; do not clip design-unbiased estimates.

    Provenance declarations are checked structurally, not a proof that an
    external learner really used only those folds. Folds/design must be fixed
    independently before auditing under the paper's stated assumptions.
    """
    floor = _probability(positivity_floor)
    if (floor <= 0 or not isinstance(predictions, (list, tuple)) or not predictions
            or len(predictions) != len(propensities) or len(predictions) != len(observed_labels)):
        raise ValueError("aligned nonempty records and positive floor required")
    terms = []
    for prediction, probability, label in zip(predictions, propensities, observed_labels, strict=True):
        if not isinstance(prediction, CrossFitPrediction):
            raise ValueError("typed cross-fit predictions required")
        phi = _probability(probability)
        if phi < floor:
            raise ValueError("audit probability violates positivity floor")
        if label is None:
            term = prediction.value
        elif type(label) is int and label in (0, 1):
            term = prediction.value+(label-prediction.value)/phi
        else:
            raise ValueError("only audited binary labels or None are accepted")
        terms.append(_real(term))
    return _real(math.fsum(terms)/len(terms))


def bounded_allocation(predicted_success, weights, *, mean_budget, positivity_floor):
    """KKT phi=min(1,max(floor,lambda*sqrt(m(1-m)))); finite strata only."""
    floor, budget = _probability(positivity_floor), _probability(mean_budget)
    if (floor <= 0 or not isinstance(predicted_success, (list, tuple)) or not predicted_success
            or len(predicted_success) != len(weights)):
        raise ValueError("positive floor and aligned nonempty finite strata required")
    m = tuple(_probability(value) for value in predicted_success)
    w = tuple(_probability(value) for value in weights)
    if not math.isclose(math.fsum(w), 1., rel_tol=1e-12, abs_tol=1e-12):
        raise ValueError("stratum weights must sum to one")
    sigma = tuple(math.sqrt(value*(1-value)) for value in m)
    maximum = floor+(1-floor)*math.fsum(weight for sd, weight in zip(sigma, w, strict=True) if sd > 0)
    if not floor <= budget <= maximum+1e-12:
        raise ValueError("budget outside the paper's attainable KKT range")

    def allocation(multiplier):
        return tuple(min(1., max(floor, multiplier*sd)) for sd in sigma)

    if math.isclose(budget, maximum, rel_tol=0., abs_tol=1e-12):
        return tuple(1. if sd > 0 else floor for sd in sigma)
    if budget == floor:
        return (floor,)*len(m)
    low, high = 0., 1.
    while math.fsum(p*weight for p, weight in zip(allocation(high), w, strict=True)) < budget:
        high = _real(2*high)
    for _ in range(100):
        mid = low+(high-low)/2
        cost = math.fsum(p*weight for p, weight in zip(allocation(mid), w, strict=True))
        if cost < budget:
            low = mid
        else:
            high = mid
    return allocation(high)


def support_outer_set(identified_contribution, unsupported_mass):
    contribution, mass = _probability(identified_contribution), _probability(unsupported_mass)
    if contribution+mass > 1+1e-12:
        raise ValueError("contribution plus unsupported mass exceeds one")
    return contribution, min(1., contribution+mass)


def robust_rank_sets(intervals):
    """Strict identification-robust ordering; no midpoint ranking substitute."""
    if not isinstance(intervals, dict) or not intervals:
        raise ValueError("named simultaneous outer intervals required")
    checked = {}
    for name, bounds in intervals.items():
        if not isinstance(name, str) or not name or not isinstance(bounds, (list, tuple)) or len(bounds) != 2:
            raise ValueError("nonempty names and interval pairs required")
        lower, upper = map(_probability, bounds)
        if lower > upper:
            raise ValueError("reversed interval")
        checked[name] = (lower, upper)
    count = len(checked)
    return {name: (1+sum(other[0] > current[1] for key, other in checked.items() if key != name),
                   count-sum(current[0] > other[1] for key, other in checked.items() if key != name))
            for name, current in checked.items()}


@dataclass(frozen=True)
class FrozenTarget:
    identity: str
    agent_frozen: bool = True
    independently_drawn_tasks: bool = True

    def __post_init__(self):
        if (not isinstance(self.identity, str) or not self.identity
                or self.agent_frozen is not True or self.independently_drawn_tasks is not True):
            raise ValueError("one frozen agent with independently drawn stable-target tasks required")


class HedgedAuditProcess:
    """Log-space e-process for a predeclared finite grid of theta hypotheses.

    `accepted_grid` is a grid inversion, NOT continuous confidence-interval
    endpoints or coverage for a truth absent from the grid. The paper's
    continuous inversion is outside this small numerical slice. Target/design
    declarations cannot prove semantic independence of external task streams.
    """

    def __init__(self, target, theta_grid, lambda_grid, *, positivity_floor, alpha=.05, seed=42):
        if not isinstance(target, FrozenTarget) or type(seed) is not int or seed < 0:
            raise ValueError("frozen stable target and nonnegative seed required")
        self.target = target
        self.floor, self.alpha = _probability(positivity_floor), _probability(alpha)
        if self.floor <= 0 or not 0 < self.alpha < 1:
            raise ValueError("positive floor and alpha in (0,1) required")
        if (not isinstance(theta_grid, tuple) or not theta_grid or not isinstance(lambda_grid, tuple)
                or not lambda_grid or len(theta_grid) > 1001 or len(lambda_grid) > 64):
            raise ValueError("bounded predeclared immutable theta/lambda grids required")
        self.theta = tuple(_probability(theta) for theta in theta_grid)
        self.lambdas = tuple(_real(lam) for lam in lambda_grid)
        if (len(set(self.theta)) != len(self.theta) or len(set(self.lambdas)) != len(self.lambdas)
                or min(self.lambdas) <= 0 or max(self.lambdas) >= self.floor):
            raise ValueError("unique hypotheses and lambda strictly in (0,floor) required")
        self._plus = [[0.]*len(self.lambdas) for _ in self.theta]
        self._minus = [[0.]*len(self.lambdas) for _ in self.theta]
        self._pending = None
        self._rng = random.Random(seed)
        self.count = 0

    def plan(self, prediction, propensity, *, target_identity):
        """Commit current prediction and audit probability before seeing Y_t."""
        if self._pending is not None or target_identity != self.target.identity:
            raise ValueError("no pending episode and unchanged target required")
        prediction, propensity = _probability(prediction), _probability(propensity)
        if propensity < self.floor:
            raise ValueError("audit probability below declared floor")
        audited = self._rng.random() < propensity
        self._pending = (prediction, propensity, audited)
        return audited

    def observe(self, label):
        if self._pending is None:
            raise ValueError("commit predictable inputs before accepting a label")
        m, phi, audited = self._pending
        if ((audited and (type(label) is not int or label not in (0, 1)))
                or (not audited and label is not None)):
            raise ValueError("audited episode needs binary label; unaudited episode must be None")
        corrected = _real(m+(label-m)/phi) if audited else m
        # All validation precedes mutation, preserving retryable pending state.
        plus = [row.copy() for row in self._plus]
        minus = [row.copy() for row in self._minus]
        for index, theta in enumerate(self.theta):
            w = _real(corrected-theta)
            for j, lam in enumerate(self.lambdas):
                increment = _real(lam*w)
                if not -1 < increment < 1:
                    raise ValueError("e-factor nonpositivity or violated audit bounds")
                plus[index][j] = _real(plus[index][j]+math.log1p(increment))
                minus[index][j] = _real(minus[index][j]+math.log1p(-increment))
        self._plus, self._minus = plus, minus
        self.count += 1
        self._pending = None

    def log_evalues(self):
        result = []
        for positive, negative in zip(self._plus, self._minus, strict=True):
            logs = positive+negative
            maximum = max(logs)
            result.append(maximum+math.log(math.fsum(math.exp(x-maximum) for x in logs))-math.log(len(logs)))
        return tuple(result)

    def accepted_grid(self):
        threshold = -math.log(self.alpha)
        return tuple(theta for theta, log_e in zip(self.theta, self.log_evalues(), strict=True) if log_e < threshold)


def diagnostic(seed=42, device="cpu"):
    if device != "cpu":
        raise ValueError("CPU-only evaluator arithmetic")
    predictions = (CrossFitPrediction(.2, "a", frozenset({"b"})),
                   CrossFitPrediction(.8, "b", frozenset({"a"})))
    # Exact two-episode Bernoulli audit-design enumeration; no live agent.
    expectation = 0.
    for r0 in (0, 1):
        for r1 in (0, 1):
            expectation += .25*aipw_estimate(predictions, (.5, .5), (0 if r0 else None, 1 if r1 else None), positivity_floor=.1)
    allocation = bounded_allocation((.1, .5, .9), (.2, .5, .3), mean_budget=.3, positivity_floor=.05)
    process = HedgedAuditProcess(FrozenTarget("frozen-synthetic"), (0., .5, 1.), (.01, .05), positivity_floor=.1, seed=seed)
    evaluator = random.Random(seed+1000)
    for _ in range(40):
        audited = process.plan(.4, .5, target_identity="frozen-synthetic")
        process.observe(int(evaluator.random() < .5) if audited else None)
    ranks = robust_rank_sets({"high": (.7, .8), "mid": (.4, .6), "tie": (.4, .6)})
    checks = {"exact_design_unbiased_with_wrong_imputation": math.isclose(expectation, .5, abs_tol=1e-12),
              "allocation_meets_budget": math.isclose(math.fsum(x*w for x, w in zip(allocation, (.2, .5, .3), strict=True)), .3, abs_tol=1e-12),
              "allocation_respects_positivity": min(allocation) >= .05 and max(allocation) <= 1,
              "support_failure_reports_outer_set": support_outer_set(.445, .2) == (.445, .645),
              "rank_sets_preserve_unresolved_tie": ranks == {"high": (1, 1), "mid": (2, 3), "tie": (2, 3)},
              "log_eprocess_finite": all(math.isfinite(x) for x in process.log_evalues()),
              "all_episodes_update_even_if_unaudited": process.count == 40,
              "no_pending_label_after_update": process._pending is None}
    return {"seed": seed, "device": "cpu", "evaluation_tier": "l1_mechanism", "diagnostic_only": True,
            "checks": checks, "metrics": {"exact_design_mean": expectation, "episodes": process.count,
                                           "accepted_grid_points": len(process.accepted_grid()),
                                           "log_evalue_at_half": process.log_evalues()[1]},
            "live_judge_evaluation_executed": False, "continuous_confidence_interval_implemented": False}
