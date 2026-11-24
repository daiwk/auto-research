"""CPU-only Weight Coding edit/search kernels, fixed arXiv:2611.29613v1 §3.

Not the paper's LLM agent, production cached evaluator or full recommendation
model. Callers supply development/search and validation objectives; there is
deliberately no held-out/test callback in the search interface.
"""

from dataclasses import dataclass
from collections.abc import Callable

import numpy as np

REQUIRES_GPU_VALIDATION = False


def _array(value):
    out = np.asarray(value, dtype=np.float64)
    if not out.size or not np.isfinite(out).all():
        raise ValueError("nonempty finite weights required")
    return out.copy()


def edit(weights, operation, *, coefficient=1.0, reference=None):
    """Functional Table1 subset; remove means selected output projection only."""
    w = _array(weights)
    if not np.isfinite(coefficient):
        raise ValueError("finite edit coefficient required")
    if operation == "rescale":
        out = coefficient * w
    elif operation == "remove":
        out = np.zeros_like(w)
    elif operation in {"reset", "interpolate", "steer"}:
        other = _array(reference)
        if other.shape != w.shape:
            raise ValueError("edit shape mismatch")
        if operation == "reset":
            out = other
        elif operation == "interpolate":
            if not 0 <= coefficient <= 1:
                raise ValueError("interpolation coefficient outside [0,1]")
            out = (1 - coefficient) * w + coefficient * other
        else:
            out = w + coefficient * other
    else:
        raise ValueError("unsupported primitive; compression is not implemented")
    return _array(out)


def concept_direction(positive_embeddings, negative_embeddings):
    """§3.2: normalized difference of mean item embeddings, not gold answers."""
    a, b = _array(positive_embeddings), _array(negative_embeddings)
    if a.ndim != 2 or b.ndim != 2 or a.shape[1] != b.shape[1]:
        raise ValueError("compatible embedding matrices required")
    u = a.mean(axis=0) - b.mean(axis=0)
    norm = np.linalg.norm(u)
    if not np.isfinite(norm) or norm == 0:
        raise ValueError("concept means do not define a finite nonzero direction")
    return u / norm


def centered_ranks(scores):
    """Average tied ranks; a constant evaluator must produce zero update."""
    values = _array(scores)
    if values.ndim != 1 or len(values) < 2:
        raise ValueError("at least two scalar scores required")
    ranks = np.empty_like(values)
    order = np.argsort(values, kind="stable")
    start = 0
    while start < len(values):
        end = start + 1
        while end < len(values) and values[order[end]] == values[order[start]]:
            end += 1
        ranks[order[start:end]] = (start + end - 1) / 2
        start = end
    return ranks / (len(values) - 1) - 0.5


@dataclass(frozen=True)
class SearchResult:
    weights: np.ndarray
    validation_score: float
    selected_step: int
    objective_calls: int
    validation_calls: int


def search(weights, objective: Callable, validation: Callable, *, seed=42,
           steps=20, pairs=16, sigma=None, learning_rate=0.03,
           mode="values", validation_every=10):
    """§3.4 antithetic Gaussian ES, centered ranks and ascent Adam.

    `values` uses fixed initial tensor RMS and sigma=.05; `row_log_scales`
    searches log row multipliers with sigma=.1. Adam uses explicit conventional
    betas (.9,.999) and epsilon1e-8: details not specified by this paper are
    local reference choices, not a recovered private implementation. Zero-RMS
    value blocks are rejected rather than inventing a perturbation floor.
    """
    base = _array(weights)
    integers = (steps, pairs, validation_every)
    if any(isinstance(n, bool) or not isinstance(n, int) or n <= 0 for n in integers):
        raise ValueError("positive integer search budgets required")
    if mode not in {"values", "row_log_scales"}:
        raise ValueError("unknown search parameterization")
    if mode == "row_log_scales" and base.ndim != 2:
        raise ValueError("row log scales require a matrix")
    sigma = (0.05 if mode == "values" else 0.1) if sigma is None else sigma
    if not np.isfinite([sigma, learning_rate]).all() or sigma <= 0 or learning_rate <= 0:
        raise ValueError("positive finite sigma and learning rate required")
    rms = np.sqrt(np.mean(base * base)) if mode == "values" else 1.0
    if not np.isfinite(rms) or rms == 0:
        raise ValueError("zero/nonfinite RMS cannot define value perturbations")
    theta = base / rms if mode == "values" else np.zeros(base.shape[0])
    def decode(state):
        with np.errstate(over="ignore", under="ignore", invalid="ignore"):
            if mode == "values":
                return _array(state * rms)
            scales = np.exp(state)
            if not np.isfinite(scales).all() or np.any(scales == 0):
                raise ValueError("row log-scale underflow or overflow")
            result = _array(base * scales[:, None])
            if np.any((base != 0) & (result == 0)):
                raise ValueError("row-scaled weights underflowed to zero")
            return result
    def score(callback, candidate):
        result = float(callback(candidate.copy()))
        if not np.isfinite(result):
            raise ValueError("nonfinite evaluator score")
        return result
    rng = np.random.default_rng(seed)
    best, best_score, selected = base.copy(), score(validation, base), 0
    val_calls, calls = 1, 0
    m, v = np.zeros_like(theta), np.zeros_like(theta)
    for step in range(1, steps + 1):
        noise = rng.normal(size=(pairs,) + theta.shape)
        positive = [score(objective, decode(theta + sigma * e)) for e in noise]
        negative = [score(objective, decode(theta - sigma * e)) for e in noise]
        ranks = centered_ranks(positive + negative)
        gradient = np.tensordot(ranks[:pairs] - ranks[pairs:], noise, axes=1) / (2 * pairs * sigma)
        m = .9 * m + .1 * gradient
        v = .999 * v + .001 * gradient ** 2
        theta += learning_rate * (m / (1 - .9 ** step)) / (np.sqrt(v / (1 - .999 ** step)) + 1e-8)
        calls += 2 * pairs
        if step % validation_every == 0 or step == steps:
            candidate = decode(theta)
            current = score(validation, candidate)
            val_calls += 1
            if current > best_score:
                best, best_score, selected = candidate, current, step
    return SearchResult(best, best_score, selected, calls, val_calls)


def diagnostic(seed=42, device="cpu"):
    if device != "cpu":
        raise ValueError("Weight Coding reference kernel is CPU-only")
    rng = np.random.default_rng(seed)
    weights = rng.normal(size=(3, 4))
    original = weights.copy()
    target = .5 * weights
    objective = lambda w: -float(np.mean((w - target) ** 2))
    result = search(weights, objective, objective, seed=seed)
    tied = search(weights, lambda _: 1., lambda _: 1., seed=seed, steps=2)
    blocked = search(weights, objective, lambda w: -float(np.mean((w-original)**2)), seed=seed, steps=2)
    direction = concept_direction([[2., 1.], [3., 1.]], [[0., 1.]])
    return {"seed": seed, "diagnostic_only": True, "evaluation_tier": "l1_mechanism",
            "checks": {"immutable_original": bool(np.array_equal(weights, original)),
                       "quadratic_objective_improves": bool(result.validation_score > objective(weights)),
                       "ties_do_not_move": bool(np.array_equal(tied.weights, weights)),
                       "validation_can_retain_initial": blocked.selected_step == 0,
                       "rescale_identity": bool(np.array_equal(edit(weights, "rescale"), weights)),
                       "direction_normalized": bool(np.isclose(np.linalg.norm(direction), 1))},
            "metrics": {"synthetic_initial_score": objective(weights),
                        "synthetic_selected_score": result.validation_score,
                        "selected_step": result.selected_step,
                        "objective_calls": result.objective_calls,
                        "validation_calls": result.validation_calls}}
