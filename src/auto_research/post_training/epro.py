"""EPRO v1 equation-level CPU kernels, not an execution-engine RL trainer.

The importance multiplier and SSC gate are frozen for differentiation (Eq.11).
Head-tail mode reconstructs Appendix B's rescaled old-training tail; it does
not pretend that unrecorded execution probabilities have been measured.
"""

from dataclasses import dataclass
import math

import numpy as np

REQUIRES_GPU_VALIDATION = False


def _matrix(value):
    x = np.asarray(value, dtype=np.float64)
    if x.ndim != 2 or min(x.shape) < 1 or not np.isfinite(x).all():
        raise ValueError("nonempty finite prefix-by-vocabulary matrix required")
    return x


def _logsoftmax(value):
    z = _matrix(value)
    with np.errstate(over="raise", invalid="raise", divide="raise"):
        try:
            shifted = z-z.max(axis=-1, keepdims=True)
            lp = shifted-np.log(np.exp(shifted).sum(axis=-1, keepdims=True))
        except FloatingPointError as exc:
            raise ValueError("log-softmax overflow") from exc
    return lp


def _scalar(value, *, positive=False):
    if type(value) not in (int, float) or not math.isfinite(value) or (positive and value <= 0):
        raise ValueError("finite scalar (strictly positive where required) expected")
    return float(value)


def _transport(logp, logq, logu):
    with np.errstate(over="raise", invalid="raise", divide="raise"):
        try:
            z = logq+logu-logp
            maximum = z.max(axis=-1, keepdims=True)
            logz = maximum+np.log(np.exp(z-maximum).sum(axis=-1, keepdims=True))
            result = z-logz
        except FloatingPointError as exc:
            raise ValueError("transport normalization overflow") from exc
    return result, logz[:, 0]


@dataclass(frozen=True)
class FrozenUpdate:
    old_training_logp: np.ndarray
    execution_anchor_logp: np.ndarray
    actions: np.ndarray
    coefficients: np.ndarray
    mask: np.ndarray
    policy_shift: np.ndarray
    attenuation: np.ndarray
    importance: np.ndarray
    head_indices: np.ndarray | None


def prepare_update(old_training_logits, old_execution_logits, current_logits, actions, advantages,
                   *, mask=None, cap=2., threshold=.125, scale=.0625, head_size=None):
    """Freeze Eq.11 multipliers at this forward pass.

    No head_size means exact full-vocabulary Eqs.2/8. A smaller head_size
    selects the old execution top-K and uses Appendix B Eqs.35--39. Inputs
    are ordinary finite distributions; numerically unresolved tails fail.
    """
    logp, logq, logu = map(_logsoftmax, (old_training_logits, old_execution_logits, current_logits))
    if logp.shape != logq.shape or logp.shape != logu.shape:
        raise ValueError("aligned vocabulary and prefixes required")
    n, vocabulary = logp.shape
    a = np.asarray(actions)
    adv = np.asarray(advantages, dtype=np.float64)
    valid = np.ones(n, dtype=bool) if mask is None else np.asarray(mask)
    if (a.shape != (n,) or a.dtype.kind not in "iu" or np.any(a < 0) or np.any(a >= vocabulary)
            or adv.shape != (n,) or not np.isfinite(adv).all() or valid.shape != (n,)
            or valid.dtype != np.bool_ or not valid.any()):
        raise ValueError("valid actions, finite advantages and a nonempty boolean mask required")
    cap, threshold, scale = _scalar(cap, positive=True), _scalar(threshold), _scalar(scale, positive=True)
    if threshold < 0:
        raise ValueError("nonnegative SSC threshold required")
    p, q, u = map(np.exp, (logp, logq, logu))
    head = None
    if head_size is not None:
        if type(head_size) is not int or not 1 <= head_size <= vocabulary:
            raise ValueError("head_size must be an integer in [1, vocabulary]")
        if head_size < vocabulary:
            # Stable order resolves equal old-execution probabilities locally.
            head = np.argsort(-q, axis=1, kind="stable")[:, :head_size]
            ph, qh, uh = (np.take_along_axis(x, head, axis=1) for x in (p, q, u))
            pt, qt, ut = (1-x.sum(axis=1, keepdims=True) for x in (ph, qh, uh))
            if min(float(x.min()) for x in (pt, qt, ut)) <= 1e-12:
                raise ValueError("head-tail probability mass is numerically unresolved")
            q_approx = (qt/pt)*p
            np.put_along_axis(q_approx, head, qh, axis=1)
            logq = np.log(q_approx)
            bucket_p = np.concatenate((ph, pt), axis=1)
            bucket_u = np.concatenate((uh, ut), axis=1)
            displacement = np.log(bucket_u/bucket_p)
        else:
            bucket_p, displacement = p, logu-logp
    else:
        bucket_p, displacement = p, logu-logp
    mean = np.sum(bucket_p*displacement, axis=1, keepdims=True)
    shift = np.sqrt(np.sum(bucket_p*(displacement-mean)**2, axis=1))
    _, logz = _transport(logp, logq, logu)
    logratio = (logu-logp)[np.arange(n), a]
    importance = np.exp(np.minimum(logratio-logz, math.log(cap)))
    outward = adv*logratio > 0
    attenuation = np.where(outward, np.exp(-np.maximum(shift-threshold, 0)/scale), 1.)
    coefficients = adv*importance*attenuation
    values = [logp, logq, a.copy(), coefficients, valid.copy(), shift, attenuation, importance, head]
    for value in values:
        if value is not None:
            if not np.isfinite(value).all():
                raise ValueError("EPRO intermediate is nonfinite")
            value.setflags(write=False)
    return FrozenUpdate(*values)


def loss_gradient(current_logits, frozen):
    """Eq.11 value/gradient with frozen weight and gate, exact in its anchor.

    In head-tail mode the anchor is Appendix B's reconstructed distribution.
    The returned derivative is with respect to all current TRAINING logits.
    """
    if not isinstance(frozen, FrozenUpdate):
        raise ValueError("prepare_update result required")
    logu = _logsoftmax(current_logits)
    if logu.shape != frozen.old_training_logp.shape:
        raise ValueError("same prefix/vocabulary shape required")
    logmu, _ = _transport(frozen.old_training_logp, frozen.execution_anchor_logp, logu)
    mu = np.exp(logmu)
    norm = int(frozen.mask.sum())
    scale = np.where(frozen.mask, frozen.coefficients, 0.)/norm
    sampled = logmu[np.arange(len(mu)), frozen.actions]
    gradient = scale[:, None]*mu
    gradient[np.arange(len(mu)), frozen.actions] -= scale
    return {"loss": float(-np.dot(scale, sampled)), "gradient": gradient,
            "transported_probabilities": mu}


def diagnostic(seed=42, device="cpu"):
    if type(seed) is not int or seed < 0 or device != "cpu":
        raise ValueError("nonnegative integer seed and CPU-only device required")
    rng = np.random.default_rng(seed)
    old, execution, current = rng.normal(size=(3, 4, 7))
    current = old+.05*current  # Small learner movement, not a saturated SSC-only check.
    actions, advantages = [0, 2, 4, 6], [1., -.5, .3, -1.]
    frozen = prepare_update(old, execution, current, actions, advantages)
    result = loss_gradient(current, frozen)
    numerical = np.zeros_like(current)
    step = 1e-6
    for coordinate in np.ndindex(current.shape):
        change = np.zeros_like(current)
        change[coordinate] = step
        numerical[coordinate] = (loss_gradient(current+change, frozen)["loss"]-
                                 loss_gradient(current-change, frozen)["loss"])/(2*step)
    err = float(np.max(np.abs(numerical-result["gradient"])))
    anchor = prepare_update(old, execution, old, actions, advantages)
    at_anchor = loss_gradient(old, anchor)["transported_probabilities"]
    head = prepare_update(old, execution, current, actions, advantages, head_size=3)
    full_head = prepare_update(old, execution, current, actions, advantages, head_size=7)
    same_engine = prepare_update(old, old, current, actions, advantages)
    checks = {
        "frozen_multiplier_gradient_matches_finite_difference": err < 1e-8,
        "transport_recovers_execution_anchor_at_rollout": bool(np.allclose(at_anchor, np.exp(_logsoftmax(execution)))),
        "matched_engines_transport_to_current_training_policy": bool(np.allclose(
            loss_gradient(current, same_engine)["transported_probabilities"], np.exp(_logsoftmax(current)))),
        "full_head_reduces_to_full_vocabulary": bool(np.allclose(loss_gradient(current, full_head)["gradient"], result["gradient"])),
        "head_tail_uses_a_normalized_reconstructed_anchor": bool(np.allclose(np.exp(head.execution_anchor_logp).sum(axis=1), 1.)),
        "score_centering_logit_gradient_sums_to_zero": bool(np.allclose(result["gradient"].sum(axis=1), 0.)),
        "importance_is_capped": bool(np.all(frozen.importance <= 2.)),
        "zero_policy_shift_at_rollout": bool(np.allclose(anchor.policy_shift, 0.))}
    return {"seed": seed, "device": device, "evaluation_tier": "l1_mechanism", "diagnostic_only": True,
            "checks": checks, "metrics": {"finite_difference_max_abs_error": err,
            "head_tail_gradient_difference": float(np.max(np.abs(loss_gradient(current, head)["gradient"]-result["gradient"]))),
            "prefixes": 4, "vocabulary": 7}, "training_executed": False}
