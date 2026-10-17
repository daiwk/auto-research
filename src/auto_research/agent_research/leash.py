"""CPU reference-bank LDA gates and bounded Shadow oversight from LEASH.

Representations must be supplied by the caller. Synthetic vectors verify the
statistics only; no GUI agent, hidden-state extractor or remote model is run.
"""
from __future__ import annotations

from dataclasses import dataclass
import math

import numpy as np


def _matrix(x):
    a = np.asarray(x, float)
    if a.ndim != 2 or not a.size or not np.isfinite(a).all():
        raise ValueError("nonempty finite feature matrix required")
    return a


def _labels(y, n):
    a = np.asarray(y)
    if a.shape != (n,) or not np.isin(a, [0, 1]).all():
        raise ValueError("one reference outcome (0 fail / 1 pass) per vector required")
    return a.astype(int)


@dataclass(frozen=True)
class PooledLDA:
    mean: np.ndarray
    scale: np.ndarray
    pass_mean: np.ndarray
    fail_mean: np.ndarray
    precision: np.ndarray
    ridge: float

    def score(self, features):
        x = _matrix(features)
        if x.shape[1] != len(self.mean):
            raise ValueError("feature dimension mismatch")
        z = (x - self.mean) / self.scale
        dp, df = z - self.pass_mean, z - self.fail_mean
        # Eq.3: distance to pass minus distance to fail; high means uncertain.
        result = np.einsum("nd,df,nf->n", dp, self.precision, dp)
        result -= np.einsum("nd,df,nf->n", df, self.precision, df)
        return result


def fit_lda(features, outcomes, *, ridge=.1):
    x = _matrix(features)
    y = _labels(outcomes, len(x))
    if not math.isfinite(ridge) or ridge <= 0 or len(np.unique(y)) != 2:
        raise ValueError("positive ridge and both outcome classes required")
    mean, scale = x.mean(0), x.std(0)
    scale = np.where(scale < 1e-12, 1., scale)
    z = (x - mean) / scale
    p, f = z[y == 1].mean(0), z[y == 0].mean(0)
    residuals = z - np.where((y == 1)[:, None], p, f)
    covariance = residuals.T @ residuals / max(1, len(z) - 2)
    # SVD avoids treating an unobserved feature direction as zero uncertainty.
    u, singular, vt = np.linalg.svd(covariance, hermitian=True)
    precision = (vt.T * (1 / (singular + ridge))) @ u.T
    return PooledLDA(mean, scale, p, f, precision, float(ridge))


def auroc(outcomes, scores):
    s = np.asarray(scores, float)
    y = _labels(outcomes, len(s))
    if s.ndim != 1 or not np.isfinite(s).all() or len(np.unique(y)) != 2:
        raise ValueError("finite scores and both reference outcomes required")
    failure, passing = s[y == 0], s[y == 1]
    return float(np.mean((failure[:, None] > passing) + .5 * (failure[:, None] == passing)))


@dataclass(frozen=True)
class CrossfitResult:
    estimator: PooledLDA
    scores: np.ndarray
    task_folds: dict[str, int]
    fold_training_tasks: tuple[tuple[str, ...], ...]
    selected_ridge: float
    oof_auroc: float


def crossfit_reference(features, outcomes, task_ids, *, seed=42, folds=5,
                       ridge_grid=(.01, .1, 1.), split="reference", excluded_task_ids=()):
    """Task-grouped OOF scores and reference-only ridge selection.

    All steps from a task stay in one fold. Evaluation tasks must not occur in
    this bank; held-out outcomes are never passed to an inference score call.
    """
    x = _matrix(features)
    y = _labels(outcomes, len(x))
    groups = tuple(str(t) for t in task_ids)
    unique = sorted(set(groups))
    if (split != "reference" or len(groups) != len(x) or any(not g for g in groups)
            or set(unique) & set(excluded_task_ids) or not 2 <= folds <= len(unique)):
        raise ValueError("disjoint reference tasks and bounded grouped folds required")
    if not ridge_grid or any(not math.isfinite(r) or r <= 0 for r in ridge_grid):
        raise ValueError("positive finite ridge candidates required")
    shuffled = np.random.default_rng(seed).permutation(unique)
    task_folds = {str(task): i % folds for i, task in enumerate(shuffled)}
    assignment = np.asarray([task_folds[g] for g in groups])
    training = tuple(tuple(t for t in unique if task_folds[t] != f) for f in range(folds))
    candidates = []
    for ridge in ridge_grid:
        scores = np.empty(len(x))
        for f in range(folds):
            fit, held = assignment != f, assignment == f
            model = fit_lda(x[fit], y[fit], ridge=ridge)
            scores[held] = model.score(x[held])
        candidates.append((auroc(y, scores), float(ridge), scores))
    metric, ridge, scores = max(candidates, key=lambda c: (c[0], -c[1]))
    return CrossfitResult(fit_lda(x, y, ridge=ridge), scores.copy(), task_folds,
                          training, ridge, metric)


def _threshold(scores, fraction):
    x = np.asarray(scores, float)
    if x.ndim != 1 or not x.size or not np.isfinite(x).all():
        raise ValueError("finite reference scores required")
    if not math.isfinite(fraction) or not 0 <= fraction <= 1:
        raise ValueError("budget fraction must be in [0,1]")
    cap = math.floor(fraction * len(x) + 1e-12)
    if cap == 0:
        return math.inf
    if cap == len(x):
        return -math.inf
    # A strict gate conservatively underfills ties instead of using test ranks.
    return float(np.sort(x)[::-1][cap])


@dataclass(frozen=True)
class EscalationCalibration:
    query_threshold: float
    runtime_threshold: float
    initial_target: float
    overall_target: float
    reference_tasks: int
    initial_routed: int
    overall_routed: int

    def initial(self, scores):
        return np.asarray(scores, float) > self.query_threshold

    def runtime(self, scores):
        return np.asarray(scores, float) > self.runtime_threshold


def calibrate_escalation(query_scores, runtime_scores, *, initial_target=.25,
                         overall_target=.5, split="reference"):
    """Eq.4: maxima per task, conditional runtime budget, no test calibration."""
    q = np.asarray(query_scores, float)
    if (split != "reference" or q.ndim != 1 or len(runtime_scores) != len(q)
            or not q.size or not np.isfinite(q).all()
            or not (0 <= initial_target <= overall_target <= 1)):
        raise ValueError("matched reference tasks and nested budgets required")
    maxima = []
    for trajectory in runtime_scores:
        a = np.asarray(trajectory, float)
        if a.ndim != 1 or not a.size or not np.isfinite(a).all():
            raise ValueError("retain a finite runtime score sequence for every reference task")
        maxima.append(float(a.max()))
    maximum = np.asarray(maxima)
    tq = _threshold(q, initial_target)
    initial = q > tq
    conditional = 0. if initial_target == 1 else (
        (overall_target - initial_target) / (1 - initial_target))
    ta = math.inf if initial.all() else _threshold(maximum[~initial], conditional)
    overall = initial | (maximum > ta)
    return EscalationCalibration(tq, ta, initial_target, overall_target,
                                 len(q), int(initial.sum()), int(overall.sum()))


def calibrate_shadow(reference_action_scores, *, split="reference", quantile=.9):
    """Paper Shadow gate uses the 90th percentile of per-step reference scores."""
    x = np.asarray(reference_action_scores, float)
    if (split != "reference" or x.ndim != 1 or not x.size or not np.isfinite(x).all()
            or not math.isfinite(quantile) or not 0 <= quantile <= 1):
        raise ValueError("finite reference-only Shadow calibration required")
    return float(np.quantile(x, quantile, method="linear"))


class ShadowOversight:
    """Schedule inert weak probes after handoff; never execute their actions."""

    def __init__(self, threshold, *, every=3, max_interventions=6, max_changes=2):
        if (not math.isfinite(threshold) or every < 1
                or not 1 <= max_interventions <= 6 or not 1 <= max_changes <= 2):
            raise ValueError("bounded Shadow configuration required")
        self.threshold, self.every = float(threshold), int(every)
        self.max_interventions, self.max_changes = max_interventions, max_changes
        self.interventions, self.changed_actions, self.probes, self.last_step = 0, 0, 0, 0

    def monitor(self, strong_step, *, probe_score: callable, intervene: callable):
        if not isinstance(strong_step, int) or strong_step <= self.last_step:
            raise ValueError("strictly increasing strong-agent step required")
        self.last_step = strong_step
        if ((strong_step - 1) % self.every or self.interventions >= self.max_interventions
                or self.changed_actions >= self.max_changes):
            return False
        score = float(probe_score())
        if not math.isfinite(score):
            raise ValueError("finite weak representation score required")
        self.probes += 1
        if score <= self.threshold:
            return False
        # Intervene replaces the pending strong action; the probe action is not supplied.
        changed = intervene()
        if not isinstance(changed, bool):
            raise ValueError("intervention callback must report whether strong action changed")
        self.interventions += 1
        self.changed_actions += int(changed)
        return True
