"""VOPD v1: detached group projection and full-vocabulary CPU loss gradients.

These are small equation-level components, not an on-policy language-model
trainer. A hypothetical next-token expectation is conditional on a fixed
observed group; it is not an unbiased full trajectory/verifier gradient.
"""

from dataclasses import dataclass
import math

import numpy as np

REQUIRES_GPU_VALIDATION = False


def _array(value, ndim):
    result = np.asarray(value, dtype=np.float64)
    if result.ndim != ndim or not result.size or not np.isfinite(result).all():
        raise ValueError("nonempty finite array of the required rank expected")
    return result


def _real(value):
    if type(value) not in (int, float) or not math.isfinite(value):
        raise ValueError("finite real number required")
    return float(value)


def _log_softmax(logits):
    z = _array(logits, 1)
    with np.errstate(over="raise", invalid="raise", divide="raise"):
        try:
            shifted = z-z.max()
            result = shifted-math.log(float(np.exp(shifted).sum()))
        except FloatingPointError as exc:
            raise ValueError("log-softmax intermediate overflow") from exc
    return result


def cumulative_teacher_rewards(teacher_sampled_logp, reference_sampled_logp, *, mask):
    """Eq.6 SUMS sampled-token log ratios, not a response-length mean.

    Mask positions must refer to the same response tokens and causal prefixes.
    Neither ground-truth answers nor a verifier are consumed by this function.
    """
    teacher, reference = _array(teacher_sampled_logp, 2), _array(reference_sampled_logp, 2)
    valid = np.asarray(mask)
    if (teacher.shape != reference.shape or valid.dtype != np.bool_ or valid.shape != teacher.shape
            or not valid.any(axis=1).all() or np.any(teacher > 0) or np.any(reference > 0)):
        raise ValueError("aligned nonpositive log probabilities and nonempty boolean response masks required")
    try:
        with np.errstate(over="raise", invalid="raise"):
            result = np.where(valid, teacher-reference, 0.).sum(axis=1)
    except FloatingPointError as exc:
        raise ValueError("cumulative implicit reward overflow") from exc
    if not np.isfinite(result).all():
        raise ValueError("cumulative implicit reward overflow")
    return result


@dataclass(frozen=True)
class GroupProjection:
    correlation: float | None
    strength: float
    used_fixed_fallback: bool


def group_projection(verifier_rewards, cumulative_rewards, *, weight=.25, fallback_strength=.25):
    """Eqs.7--12/zero-variance paragraph, using population normalization.

    Returned scalars are detached inputs to local_loss_gradient. The explicit
    fixed fallback is the extrapolation strength, not weight times correlation.
    The paper only specifies a zero-VERIFIER-variance fallback. A zero teacher
    variance with varying verifier outcomes is rejected, not silently invented.
    """
    v, d = _array(verifier_rewards, 1), _array(cumulative_rewards, 1)
    lam, fallback = _real(weight), _real(fallback_strength)
    if v.shape != d.shape or len(v) < 2 or not np.isin(v, (0., 1.)).all() or lam < 0 or fallback < 0:
        raise ValueError("at least two binary verifier outcomes, matched rewards and nonnegative strengths required")
    if np.all(v == v[0]):
        return GroupProjection(None, fallback, True)
    if np.all(d == d[0]):
        raise ValueError("zero teacher variance with varying verifier outcomes is unspecified in fixed v1")

    def centered_unit(values):
        # Independent positive scaling leaves Pearson correlation unchanged.
        scale = float(np.max(np.abs(values)))
        scaled = values/scale if scale else values
        centered = scaled-scaled.mean()
        norm = float(np.linalg.norm(centered))
        if norm == 0:
            raise ValueError("variance is numerically unresolved")
        return centered/norm

    correlation = float(np.dot(centered_unit(v), centered_unit(d)))
    correlation = max(-1., min(1., correlation))  # only roundoff outside [-1,1]
    strength = lam*correlation
    if not math.isfinite(strength):
        raise ValueError("extrapolation strength overflow")
    return GroupProjection(correlation, strength, False)


def local_loss_gradient(student_logits, teacher_logits, reference_logits, *, strength):
    """Eq.17 and analytic logit gradient; group/prefix/teacher/reference fixed.

    This executes the theoretical FULL-vocabulary objective. The paper's
    top-16 training approximation is not guessed from an unreleased trainer.
    """
    logp, logt, logr = (_log_softmax(x) for x in (student_logits, teacher_logits, reference_logits))
    if logp.shape != logt.shape or logp.shape != logr.shape:
        raise ValueError("shared vocabulary required")
    w = _real(strength)
    p = np.exp(logp)
    try:
        with np.errstate(over="raise", invalid="raise"):
            reward = logt-logr
            integrand = logp-logt-w*reward
            loss = float(np.dot(p, integrand))
            gradient = p*(integrand-float(np.dot(p, integrand)))
            target_logits = (1+w)*logt-w*logr
    except FloatingPointError as exc:
        raise ValueError("VOPD objective intermediate overflow") from exc
    if not math.isfinite(loss) or not np.isfinite(gradient).all():
        raise ValueError("VOPD objective overflow")
    return {"loss": loss, "gradient": gradient, "student_probabilities": p,
            "implicit_reward": reward, "target_log_probabilities": _log_softmax(target_logits)}


def conditional_reward_gradient(student_probabilities, implicit_reward, *, correlation, baseline=0.):
    """Eq.13--15: enumerate a FRESH next token after fixing observed group.

    Returns conditional mean and second central moment of c*(d-b)*score.
    Rao--Blackwellizing gives this mean without the next-token variance; it
    does not integrate the observed group or future trajectory randomness.
    """
    p, d = _array(student_probabilities, 1), _array(implicit_reward, 1)
    c, b = _real(correlation), _real(baseline)
    if p.shape != d.shape or np.any(p < 0) or not math.isclose(float(p.sum()), 1., rel_tol=1e-12, abs_tol=1e-12) or not -1 <= c <= 1:
        raise ValueError("normalized probability vector, matched reward and correlation in [-1,1] required")
    with np.errstate(over="raise", invalid="raise"):
        try:
            samples = c*(d-b)[:, None]*(np.eye(len(p))-p[None, :])
            mean = p@samples
            variance = float(np.sum(p[:, None]*(samples-mean)**2))
        except FloatingPointError as exc:
            raise ValueError("conditional gradient moment overflow") from exc
    if not np.isfinite(mean).all() or not math.isfinite(variance):
        raise ValueError("conditional gradient moment overflow")
    return mean, variance


def diagnostic(seed=42, device="cpu"):
    if type(seed) is not int or seed < 0 or device != "cpu":
        raise ValueError("nonnegative integer seed and CPU-only device required")
    rng = np.random.default_rng(seed)
    projection = group_projection([0, 0, 1, 1], [-2., -1., 1., 2.])
    z, teacher, reference = rng.normal(size=(3, 5))
    local = local_loss_gradient(z, teacher, reference, strength=projection.strength)
    expected, variance = conditional_reward_gradient(local["student_probabilities"], local["implicit_reward"],
                                                     correlation=projection.correlation, baseline=2.)
    centered = projection.correlation*local["student_probabilities"]*(local["implicit_reward"]-
                np.dot(local["student_probabilities"], local["implicit_reward"]))
    no_baseline, _ = conditional_reward_gradient(local["student_probabilities"], local["implicit_reward"],
                                                correlation=projection.correlation, baseline=0.)
    step = 1e-6
    numerical = []
    for i in range(5):
        delta = np.eye(5)[i]*step
        numerical.append((local_loss_gradient(z+delta, teacher, reference, strength=projection.strength)["loss"]-
                          local_loss_gradient(z-delta, teacher, reference, strength=projection.strength)["loss"])/(2*step))
    error = float(np.max(np.abs(local["gradient"]-numerical)))
    checks = {"analytic_loss_gradient_matches_finite_difference": error < 1e-8,
              "conditional_sample_mean_matches_dense_gradient": bool(np.allclose(expected, centered, atol=1e-12)),
              "fixed_baseline_cancels_in_fresh_token_expectation": bool(np.allclose(expected, no_baseline, atol=1e-12)),
              "sampled_estimator_has_variance_dense_conditional_mean_does_not": variance > 0,
              "verifier_zero_variance_uses_fixed_extrapolation": group_projection([1, 1], [0., 2.], weight=2.).strength == .25,
              "negative_agreement_opposes_teacher_direction": group_projection([1, 1, 0, 0], [-2., -1., 1., 2.]).strength < 0,
              "all_vocab_logit_gradient_has_zero_sum": abs(float(local["gradient"].sum())) < 1e-12}
    return {"seed": seed, "device": device, "evaluation_tier": "l1_mechanism", "diagnostic_only": True,
            "checks": checks, "metrics": {"finite_difference_max_abs_error": error,
            "conditional_gradient_max_abs_error": float(np.max(np.abs(expected-centered))),
            "sampled_next_token_variance_trace": variance, "correlation": projection.correlation,
            "strength": projection.strength, "vocabulary": 5}, "training_executed": False}
