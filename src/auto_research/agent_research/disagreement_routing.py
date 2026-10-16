"""Label-free corrected-disagreement operators and tiny CPU probe training.

No checkpoint or generation backend is provided. Caller-supplied weak-model
representations and offline model responses remain distinct from gold answers.
"""
from __future__ import annotations

from dataclasses import dataclass
import math

import numpy as np


def _array(value, ndim):
    out = np.asarray(value, dtype=np.float64)
    if out.ndim != ndim or not out.size or not np.isfinite(out).all():
        raise ValueError(f"nonempty finite {ndim}-dimensional array required")
    return out


def empirical_targets(weak_responses, strong_responses, disagrees=None) -> tuple[np.ndarray, float]:
    """Equations 9/10; self-pairs excluded, no correctness/gold input exists."""
    weak, strong = tuple(weak_responses), tuple(strong_responses)
    if not weak or len(strong) < 2:
        raise ValueError("nonempty weak responses and >= 2 independent strong draws required")
    compare = disagrees or (lambda a, b: a != b)
    def indicator(a, b):
        result = compare(a, b)
        if result not in (0, 1, False, True):
            raise ValueError("disagreement function must return a binary indicator")
        return int(result)
    d = np.array([sum(indicator(w, s) for s in strong) / len(strong) for w in weak])
    total = sum(indicator(a, b) for i, a in enumerate(strong) for j, b in enumerate(strong) if i != j)
    return d, total / (len(strong) * (len(strong) - 1))


def corrected_score(weak_strong, strong_self):
    """Equation 11: min_i f_d - f_g, deliberately retaining negative scores."""
    d = np.asarray(weak_strong, dtype=np.float64)
    g = np.asarray(strong_self, dtype=np.float64)
    if d.ndim < 1 or not d.size or not np.isfinite(d).all() or not np.isfinite(g).all():
        raise ValueError("nonempty finite probability inputs required")
    if ((d < 0) | (d > 1)).any() or ((g < 0) | (g > 1)).any():
        raise ValueError("probe probabilities must lie in [0, 1]")
    if g.shape != d.shape[:-1]:
        raise ValueError("one self-disagreement value per candidate set required")
    return np.min(d, axis=-1) - g


def _sigmoid(value):
    return np.exp(-np.logaddexp(0., -value))


@dataclass(frozen=True)
class ProbabilityProbe:
    weights: np.ndarray
    mean: np.ndarray
    scale: np.ndarray
    initial_loss: float
    final_loss: float
    parameter_delta_l2: float

    def predict(self, features):
        x = _array(features, 2)
        if x.shape[1] != len(self.mean):
            raise ValueError("probe feature dimension mismatch")
        design = np.column_stack(((x - self.mean) / self.scale, np.ones(len(x))))
        return _sigmoid(design @ self.weights)


def fit_probability_probe(features, targets, *, seed=42, steps=200, learning_rate=.05, l2=1e-3):
    """Real soft-target BCE/Adam fit; standardizer sees training features only."""
    x, y = _array(features, 2), _array(targets, 1)
    if len(x) != len(y) or ((y < 0) | (y > 1)).any():
        raise ValueError("matched probability targets required")
    if not 1 <= steps <= 1000 or learning_rate <= 0 or not math.isfinite(learning_rate) or not math.isfinite(l2) or l2 < 0:
        raise ValueError("bounded valid optimization settings required")
    mean, scale = x.mean(0), x.std(0)
    scale = np.where(scale < 1e-12, 1., scale)
    design = np.column_stack(((x - mean) / scale, np.ones(len(x))))
    weights = np.random.default_rng(seed).normal(0, .01, design.shape[1])
    original = weights.copy()
    def objective(w):
        logits = design @ w
        return float(np.mean(np.logaddexp(0., logits) - y * logits) + l2 * np.square(w[:-1]).sum())
    initial = objective(weights)
    m, v = np.zeros_like(weights), np.zeros_like(weights)
    for step in range(1, steps + 1):
        gradient = design.T @ (_sigmoid(design @ weights) - y) / len(y)
        gradient[:-1] += 2 * l2 * weights[:-1]
        m, v = .9 * m + .1 * gradient, .999 * v + .001 * gradient**2
        weights -= learning_rate * (m / (1 - .9**step)) / (np.sqrt(v / (1 - .999**step)) + 1e-8)
    return ProbabilityProbe(weights.copy(), mean, scale, initial, objective(weights),
                            float(np.linalg.norm(weights - original)))


@dataclass(frozen=True)
class DisagreementRouter:
    response_probe: ProbabilityProbe
    prompt_probe: ProbabilityProbe

    def scores(self, prompt_features, response_features):
        prompts, responses = _array(prompt_features, 2), _array(response_features, 3)
        if len(prompts) != len(responses):
            raise ValueError("matched prompt/candidate representations required")
        predicted_d = self.response_probe.predict(responses.reshape(-1, responses.shape[-1])).reshape(responses.shape[:2])
        predicted_g = self.prompt_probe.predict(prompts)
        return corrected_score(predicted_d, predicted_g)


def fit_router(prompt_features, response_features, weak_responses, strong_responses, *, seed=42, steps=200):
    prompts, responses = _array(prompt_features, 2), _array(response_features, 3)
    if not (len(prompts) == len(responses) == len(weak_responses) == len(strong_responses)):
        raise ValueError("matched training prompts and offline response sets required")
    targets = [empirical_targets(w, s) for w, s in zip(weak_responses, strong_responses, strict=True)]
    d = np.stack([item[0] for item in targets])
    if d.shape != responses.shape[:2]:
        raise ValueError("candidate features must match every weak response")
    response_probe = fit_probability_probe(responses.reshape(-1, responses.shape[-1]), d.ravel(), seed=seed, steps=steps)
    prompt_probe = fit_probability_probe(prompts, [item[1] for item in targets], seed=seed + 1, steps=steps)
    return DisagreementRouter(response_probe, prompt_probe)


@dataclass(frozen=True)
class BudgetCalibration:
    threshold: float
    requested_budget: float
    validation_count: int
    validation_routed: int

    def route(self, scores):
        values = _array(scores, 1)
        return values > self.threshold


def calibrate_budget(validation_scores, budget, *, split="validation") -> BudgetCalibration:
    """Conservative strict threshold; ties cannot exceed held-out budget.

    Test distribution drift can change its realized rate. It is not an exact
    top-k quota on test data, and test scores are never used for calibration.
    """
    values = _array(validation_scores, 1)
    if split != "validation" or not math.isfinite(budget) or not 0 <= budget <= 1:
        raise ValueError("budget must be in [0,1], calibration split must be validation")
    positive = np.sort(values[values > 0])[::-1]
    cap = math.floor(budget * len(values) + 1e-12)
    threshold = math.inf if cap == 0 else 0. if cap >= len(positive) else float(positive[cap])
    return BudgetCalibration(threshold, float(budget), len(values), int((values > threshold).sum()))
