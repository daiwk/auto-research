"""ELPSD fixed-prefix CPU kernels (v1 Eqs.3--5), not a looped LM trainer."""

from dataclasses import dataclass
import math

import numpy as np

REQUIRES_GPU_VALIDATION = False


def _logsoftmax(value):
    x = np.asarray(value, dtype=np.float64)
    if x.ndim != 3 or min(x.shape) < 1 or not np.isfinite(x).all():
        raise ValueError("finite nonempty [response,position,vocabulary] logits required")
    with np.errstate(over="raise", invalid="raise", divide="raise"):
        try:
            z = x-x.max(axis=-1, keepdims=True)
            return z-np.log(np.exp(z).sum(axis=-1, keepdims=True))
        except FloatingPointError as exc:
            raise ValueError("unrepresentable log-softmax") from exc


@dataclass(frozen=True)
class FrozenTeacher:
    logp: np.ndarray
    early_logp: np.ndarray
    last_logp: np.ndarray
    log_normalizer: np.ndarray
    weight: float


def extrapolated_teacher(early_logits, last_logits, *, weight=.5):
    """Freeze Eq.3's base-model loop1/last readouts; temperature1, no truncation."""
    if isinstance(weight, (bool, np.bool_)) or not np.isscalar(weight):
        raise ValueError("finite nonnegative extrapolation weight required")
    weight = float(weight)
    if not math.isfinite(weight) or weight < 0:
        raise ValueError("finite nonnegative extrapolation weight required")
    early, last = _logsoftmax(early_logits), _logsoftmax(last_logits)
    if early.shape != last.shape:
        raise ValueError("aligned first/last-loop readouts required")
    with np.errstate(over="raise", invalid="raise"):
        try:
            z = (1+weight)*last-weight*early
            lp = _logsoftmax(z)
            normalizer = z[:, :, 0]-lp[:, :, 0]
        except FloatingPointError as exc:
            raise ValueError("unrepresentable extrapolated teacher") from exc
    for value in (lp, early, last, normalizer):
        value.setflags(write=False)
    return FrozenTeacher(lp, early, last, normalizer, weight)


def loss_gradient(student_logits, teacher, *, mask=None):
    """Exact reverse KL; token mean per response THEN response mean (Eq.4).

    The provided prefixes are fixed. The derivative does not backpropagate
    through sampled prefix distribution or the frozen teacher.
    """
    if not isinstance(teacher, FrozenTeacher):
        raise ValueError("frozen extrapolated teacher required")
    lp = _logsoftmax(student_logits)
    if lp.shape != teacher.logp.shape:
        raise ValueError("student and teacher readouts must align")
    valid = np.ones(lp.shape[:2], dtype=bool) if mask is None else np.asarray(mask)
    if valid.shape != lp.shape[:2] or valid.dtype != np.bool_ or not valid.any(axis=1).all():
        raise ValueError("boolean mask and at least one visited prefix per response required")
    p = np.exp(lp)
    residual = lp-teacher.logp
    per_prefix = np.sum(p*residual, axis=-1)
    weights = valid/(valid.sum(axis=1, keepdims=True)*len(valid))
    gradient = weights[:, :, None]*p*(residual-per_prefix[:, :, None])
    kl_last = np.sum(p*(lp-teacher.last_logp), axis=-1)
    kl_early = np.sum(p*(lp-teacher.early_logp), axis=-1)
    decomposition = (1+teacher.weight)*kl_last-teacher.weight*kl_early+teacher.log_normalizer
    if not np.isfinite(gradient).all() or not np.isfinite(per_prefix).all():
        raise ValueError("nonfinite reverse-KL output")
    return {"loss": float(np.sum(weights*per_prefix)), "gradient": gradient,
            "per_prefix_kl": per_prefix, "decomposition": decomposition}


def refreshed_rounds(early_logits, initial_last_logits, *, weight=.5, rounds=4):
    """Proposition2's idealized exact-fit map, not actual model optimization."""
    if type(rounds) is not int or rounds < 0 or rounds > 32:
        raise ValueError("bounded nonnegative integer round count required")
    current = _logsoftmax(initial_last_logits)
    outputs = [current.copy()]
    for _ in range(rounds):
        current = extrapolated_teacher(early_logits, current, weight=weight).logp.copy()
        outputs.append(current)
    return outputs


def diagnostic(seed=42, device="cpu"):
    if type(seed) is not int or seed < 0 or device != "cpu":
        raise ValueError("nonnegative integer seed and CPU-only device required")
    rng = np.random.default_rng(seed)
    early, last, student = rng.normal(size=(3, 2, 3, 5))
    teacher = extrapolated_teacher(early, last)
    mask = np.array([[True, True, False], [True, False, False]])
    result = loss_gradient(student, teacher, mask=mask)
    numerical = np.zeros_like(student)
    for index in np.ndindex(student.shape):
        delta = np.zeros_like(student); delta[index] = 1e-6
        numerical[index] = (loss_gradient(student+delta, teacher, mask=mask)["loss"]-
                            loss_gradient(student-delta, teacher, mask=mask)["loss"])/(2e-6)
    error = float(np.max(np.abs(numerical-result["gradient"])))
    zero = loss_gradient(last, extrapolated_teacher(early, last, weight=0.))
    exact = loss_gradient(teacher.logp, teacher)
    path = refreshed_rounds(early, last, rounds=3)
    initial_gap = path[0]-_logsoftmax(early)
    final_gap = path[-1]-_logsoftmax(early)
    recurrence_error = float(np.max(np.abs((final_gap-final_gap[:, :, :1])-1.5**3*(initial_gap-initial_gap[:, :, :1]))))
    checks = {"analytic_gradient_matches_finite_difference": error < 1e-8,
              "contrastive_decomposition_exact": bool(np.allclose(result["per_prefix_kl"], result["decomposition"], atol=1e-12)),
              "zero_extrapolation_degenerate_at_initialization": abs(zero["loss"]) < 1e-12 and bool(np.allclose(zero["gradient"], 0., atol=1e-12)),
              "frozen_target_is_stationary": abs(exact["loss"]) < 1e-12 and bool(np.allclose(exact["gradient"], 0., atol=1e-12)),
              "padding_gradient_zero": bool(np.all(result["gradient"][~mask] == 0)),
              "teacher_arrays_are_frozen": not teacher.logp.flags.writeable,
              "moving_teacher_compounds_log_odds": recurrence_error < 1e-11}
    return {"seed": seed, "device": device, "evaluation_tier": "l1_mechanism", "diagnostic_only": True,
            "training_executed": False, "checks": checks, "metrics": {"finite_difference_max_abs_error": error,
            "contrastive_decomposition_max_abs_error": float(np.max(np.abs(result["per_prefix_kl"]-result["decomposition"]))),
            "moving_teacher_log_odds_max_abs_error": recurrence_error, "responses": 2, "vocabulary": 5}}
