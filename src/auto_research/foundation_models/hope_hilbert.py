"""HOPE (2607.21366v1): CPU-only Hilbert kernel and pruning subcomponents.

This is NOT the HOPE encoder: MERGE, EVICT, parent synthesis, convolutional
padding, full curricula, DEFT and ImageNet evaluation are deliberately absent.
Statistics and effective weights must be supplied from a caller's frozen model.
The Gaussian surrogate is the paper's modeling assumption, not real-data truth.
Formulas were independently implemented; no upstream implementation is vendored.
"""
from __future__ import annotations

from dataclasses import dataclass
import hashlib
import math

import numpy as np

REQUIRES_GPU_VALIDATION = False
GPU_VALIDATION_ARTIFACT = None


def _scalar(value: float, name: str) -> float:
    if isinstance(value, (bool, np.bool_)) or not np.isscalar(value):
        raise ValueError(f"{name}: finite real scalar required")
    try:
        result = float(value)
    except (TypeError, ValueError, OverflowError) as error:
        raise ValueError(f"{name}: finite real scalar required") from error
    if not math.isfinite(result) or abs(result) > 1e8:
        raise ValueError(f"{name}: bounded finite real scalar required")
    return result


def _array(value, name: str, *, ndim: int) -> np.ndarray:
    raw = np.asarray(value)
    if (raw.ndim != ndim or raw.size == 0 or raw.size > 65_536
            or not np.issubdtype(raw.dtype, np.floating)
            or not np.isfinite(raw).all() or np.max(np.abs(raw)) > 1e8):
        raise ValueError(f"{name}: nonempty bounded finite floating array required")
    return raw.astype(np.float64, copy=True)


def _phi(x: float) -> float:
    return math.exp(-0.5 * x * x) / math.sqrt(2.0 * math.pi)


def _cdf(x: float) -> float:
    return 0.5 * math.erfc(-x / math.sqrt(2.0))


def relu_moments(beta: float, gamma: float) -> tuple[float, float, float]:
    """E[ReLU(Y)], E[ReLU(Y)^2], Var[ReLU(Y)], Y~N(beta,gamma²).

    Eq.3 / Appendix E.2. gamma may be negative (a signed BN scale); its
    marginal standard deviation is abs(gamma). Zero variance is deterministic.
    """
    beta, gamma = _scalar(beta, "beta"), _scalar(gamma, "gamma")
    sigma = abs(gamma)
    if sigma == 0:
        mean = max(beta, 0.0)
        return mean, mean * mean, 0.0
    c = beta / sigma
    density, probability = _phi(c), _cdf(c)
    mean = sigma * density + beta * probability
    second = (sigma * sigma + beta * beta) * probability + beta * sigma * density
    if c >= 0:
        # Algebraically second-mean², without subtracting two beta²-sized
        # numbers. Positive-tail representation preserves variance at beta=1e8.
        # Beyond 38 standard deviations the tail terms round away in float64;
        # avoiding c²*0 also handles an overflowed positive beta/sigma ratio.
        if c > 38:
            variance = sigma * sigma
        else:
            tail = _cdf(-c)
            delta = density - c * tail
            variance = sigma * sigma * (1 + (c*c - 1)*tail - c*density - delta*delta)
    else:
        variance = second - mean * mean
    tolerance = 1e-12 * max(1.0, second)
    if min(mean, second, variance) < -tolerance:
        raise ValueError("nonrepresentable Gaussian ReLU moments")
    return max(0.0, mean), max(0.0, second), max(0.0, variance)


def warped_correlation(effective_i, effective_j, gamma_i: float, gamma_j: float) -> float:
    """Appendix E.3 / Eq.4 pairwise max-entropy correlation, not raw cosine.

    This is a pairwise surrogate. Repeating it for many pairs does NOT prove
    that all entries come from one globally consistent covariance matrix.
    """
    a, b = _array(effective_i, "effective_i", ndim=1), _array(effective_j, "effective_j", ndim=1)
    si, sj = abs(_scalar(gamma_i, "gamma_i")), abs(_scalar(gamma_j, "gamma_j"))
    if a.shape != b.shape or min(np.linalg.norm(a), np.linalg.norm(b), si, sj) == 0:
        raise ValueError("matching nonzero effective weights and nonzero gamma required")
    na, nb = float(np.linalg.norm(a)), float(np.linalg.norm(b))
    normalized_a, normalized_b = a / na, b / nb
    # Detect exact coincident directions without turning a genuinely near-unit
    # correlation into a singular one. A self dot can round below one.
    if np.array_equal(normalized_a, normalized_b):
        return 1.0
    if np.array_equal(normalized_a, -normalized_b):
        return -1.0
    rho = float(np.clip(normalized_a @ normalized_b, -1.0, 1.0))
    if abs(rho) == 1:
        return rho
    kappa = (rho / (1.0 - rho * rho)) * (si / na) * (sj / nb)
    if not math.isfinite(kappa):
        raise ValueError("nonrepresentable warped-correlation scale")
    # Algebraically Eq.4, using hypot to avoid squaring a large kappa.
    return 2.0 * kappa / (1.0 + math.hypot(1.0, 2.0 * kappa))


def _interval_moments(lower: float, upper: float) -> tuple[float, float, float]:
    probability = _cdf(upper) - _cdf(lower)
    first = _phi(lower) - _phi(upper)
    lower_term = 0.0 if not math.isfinite(lower) else lower * _phi(lower)
    upper_term = 0.0 if not math.isfinite(upper) else upper * _phi(upper)
    return probability, first, probability + lower_term - upper_term


def relu_cross_kernel(beta_i: float, gamma_i: float, beta_j: float,
                      gamma_j: float, correlation: float) -> float:
    """Exact biased ReLU moment of Eq.83, to deterministic quadrature tolerance.

    Φ₂ is evaluated by a deterministic 1D Gaussian integral (SciPy extra), not
    Monte Carlo or the paper's separate zero-bias Eq.85 approximation. Perfect
    correlation and deterministic marginals use exact limiting expressions.
    """
    bi, bj = _scalar(beta_i, "beta_i"), _scalar(beta_j, "beta_j")
    si, sj = abs(_scalar(gamma_i, "gamma_i")), abs(_scalar(gamma_j, "gamma_j"))
    rho = _scalar(correlation, "correlation")
    if not -1 <= rho <= 1:
        raise ValueError("correlation must be in[-1,1]")
    mi, qi, _ = relu_moments(bi, si)
    mj, qj, _ = relu_moments(bj, sj)
    if si == 0 or sj == 0 or rho == 0:
        return mi * mj
    ci, cj = bi / si, bj / sj
    if rho == 1:
        p, m1, m2 = _interval_moments(max(-ci, -cj), math.inf)
        result = bi * bj * p + (bi * sj + bj * si) * m1 + si * sj * m2
    elif rho == -1:
        lower, upper = -ci, cj
        if lower >= upper:
            return 0.0
        p, m1, m2 = _interval_moments(lower, upper)
        result = bi * bj * p + (si * bj - bi * sj) * m1 - si * sj * m2
    elif 1.0 - abs(rho) < 1e-7:
        # Eq.83's several terms become ill-conditioned near singularity.
        # Evaluate the SAME Gaussian moment via conditional integration rather
        # than silently rounding a genuinely non-unit correlation to ±1.
        from scipy.integrate import quad

        conditional_sigma = sj * math.sqrt(1 - rho * rho)
        # Infinite/huge integration intervals may cause QUADPACK to miss the
        # normal density around zero and falsely report zero error. At ±38σ
        # the omitted Gaussian polynomial tails are below float64 tolerance.
        lower, upper, pivot = max(-ci, -38.0), 38.0, -cj / rho
        points = [lower, pivot, upper] if lower < pivot < upper else [lower, upper]
        result = 0.0
        for left, right in zip(points, points[1:]) if lower < upper else []:
            value, error = quad(
                lambda z: (bi + si * z) * relu_moments(bj + sj * rho * z, conditional_sigma)[0] * _phi(z),
                left, right, epsabs=2e-13, epsrel=2e-13, limit=200,
            )
            if error > 1e-10:
                raise ValueError("near-singular Gaussian moment did not meet fixed tolerance")
            result += value
    else:
        from scipy.integrate import quad

        scale = math.sqrt(1.0 - rho * rho)
        if ci <= -38:
            p2, error = 0.0, 0.0
        else:
            p2, error = quad(lambda z: _phi(z) * _cdf((cj - rho * z) / scale),
                             -38.0, min(ci, 38.0), epsabs=2e-13, epsrel=2e-13, limit=200)
        if error > 1e-10:
            raise ValueError("bivariate CDF quadrature did not meet the fixed tolerance")
        density2 = math.exp(-(ci * ci - 2 * rho * ci * cj + cj * cj)
                            / (2 * scale * scale)) / (2 * math.pi * scale)
        result = si * sj * ((ci * cj + rho) * p2
                            + ci * _phi(cj) * _cdf((ci - rho * cj) / scale)
                            + cj * _phi(ci) * _cdf((cj - rho * ci) / scale)
                            + scale * scale * density2)
    bound = math.sqrt(qi * qj)
    if result < -1e-10 * max(1.0, bound) or result > bound + 1e-10 * max(1.0, bound):
        raise ValueError("kernel violates nonnegativity/Cauchy-Schwarz beyond round-off")
    return min(bound, max(0.0, result))


def operator_pair_gram(effective_weights, output_weights, beta, gamma,
                       *, centered: bool = True) -> np.ndarray:
    """2×2 Hilbert Gram: activation (co)moment times outgoing-vector dot product.

    The centered option explicitly uses C=K-mmᵀ, matching the Oct27 released
    implementation. centered=False is the uncentered Sec.5/Eq.3–6 formulation.
    Bias mean removal is not silently interchangeable with the uncentered norm.
    """
    w, out = _array(effective_weights, "effective_weights", ndim=2), _array(output_weights, "output_weights", ndim=2)
    beta, gamma = _array(beta, "beta", ndim=1), _array(gamma, "gamma", ndim=1)
    if w.shape[0] != 2 or out.shape[0] != 2 or beta.shape != (2,) or gamma.shape != (2,):
        raise ValueError("exactly two neurons with matched beta/gamma required")
    if not isinstance(centered, bool):
        raise ValueError("centered must be bool")
    moments = [relu_moments(b, g) for b, g in zip(beta, gamma)]
    if np.all(gamma != 0) and np.all(np.linalg.norm(w, axis=1) > 0):
        rho = warped_correlation(w[0], w[1], gamma[0], gamma[1])
    else:
        # A deterministic marginal has zero covariance and does not need rho.
        if np.any((gamma != 0) & (np.linalg.norm(w, axis=1) == 0)):
            raise ValueError("active marginal requires nonzero effective weights")
        rho = 0.0
    cross = relu_cross_kernel(beta[0], gamma[0], beta[1], gamma[1], rho)
    kernel = np.array([[moments[0][1], cross], [cross, moments[1][1]]])
    if centered:
        means = np.array([x[0] for x in moments])
        variances = np.array([x[2] for x in moments])
        if rho == 0 or np.any(gamma == 0):
            # Independent (or deterministic) marginals have exact zero
            # covariance, even when K and the product of means are huge.
            covariance = 0.0
        elif rho == 1 and beta[0] == beta[1] and abs(gamma[0]) == abs(gamma[1]):
            covariance = float(variances[0])
        else:
            product = means[0] * means[1]
            covariance = cross - product
            # A valid uncentered moment need not support accurate centering.
            # Fail closed rather than turn catastrophic cancellation into a
            # dead feature, zero covariance, or an artificially repaired PSD.
            roundoff_bound = 8 * np.finfo(np.float64).eps * (abs(cross) + abs(product))
            covariance_bound = math.sqrt(variances[0] * variances[1])
            if roundoff_bound > 1e-10 * max(1.0, covariance_bound):
                raise ValueError("centered covariance unsupported at this mean scale: cancellation exceeds tolerance")
            if abs(covariance) > covariance_bound + 1e-10 * max(1.0, covariance_bound):
                raise ValueError("centered covariance violates its variance bound")
        kernel = np.array([[variances[0], covariance], [covariance, variances[1]]])
    return kernel * (out @ out.T)


def pruning_rates(capacities, initial_parameter_footprints) -> tuple[np.ndarray, int]:
    """Eq.6/23 pruning-only candidates: N*capacity/(Ea-capacity)/ΔP_init.

    N counts supplied live neurons (including zero-capacity ones). Infinite
    cost is retained for capacity-depleting actions; no arbitrary epsilon makes
    the last positive-capacity neuron appear safely removable. Footprints must
    refer to the INITIAL model, not the shrinking live shape.
    """
    c = _array(capacities, "capacities", ndim=1)
    p = _array(initial_parameter_footprints, "initial_parameter_footprints", ndim=1)
    if c.shape != p.shape or np.any(c < 0) or np.any(p <= 0) or not np.any(c > 0):
        raise ValueError("nonnegative live capacities, some positive; matching positive initial footprints")
    remaining = c.sum() - c
    rates = np.full(c.shape, np.inf)
    good = remaining > 0
    rates[good] = len(c) * c[good] / remaining[good] / p[good]
    if not np.isfinite(rates).any():
        raise ValueError("no admissible pruning-only action remains")
    return rates, int(np.argmin(rates))


def _digest(weights: np.ndarray, mean: np.ndarray) -> str:
    result = hashlib.sha256()
    for x in (weights, mean):
        result.update(str(x.shape).encode())
        result.update(x.tobytes())
    return result.hexdigest()


@dataclass(frozen=True)
class PrunePacket:
    """Single-step undo record, not a portable/full-model HOPE curriculum."""
    index: int
    original_row: tuple[float, ...]
    original_mean: tuple[float, ...]
    expected_post_sha256: str


def prune_dense_neuron(output_weights, consumer_mean, index: int, activation_mean: float):
    """Zero one outgoing row and compensate a DENSE consumer's BN running mean.

    μ_consumer <- μ_consumer - E[ReLU(Y_i)]*W_out[i]. Shapes stay fixed;
    there is no advertised hardware sparsity speedup or 3×3 padding support.
    Returns NEW arrays. Inputs are neither mutated nor used as calibration data.
    """
    weights, mean = _array(output_weights, "output_weights", ndim=2), _array(consumer_mean, "consumer_mean", ndim=1)
    activation_mean = _scalar(activation_mean, "activation_mean")
    if (mean.shape != weights.shape[1:] or isinstance(index, (bool, np.bool_))
            or not isinstance(index, (int, np.integer)) or not 0 <= index < weights.shape[0]
            or activation_mean < 0):
        raise ValueError("valid neuron index, matching consumer mean, nonnegative activation mean required")
    old_row, old_mean = tuple(weights[index]), tuple(mean)
    mean -= activation_mean * weights[index]
    weights[index] = 0.0
    if not np.isfinite(mean).all():
        raise ValueError("nonrepresentable BN compensation; no state changed")
    packet = PrunePacket(int(index), old_row, old_mean, _digest(weights, mean))
    return weights, mean, packet


def restore_dense_neuron(output_weights, consumer_mean, packet: PrunePacket):
    """Undo only the exact post-prune state; stale/wrong-state packets fail closed."""
    weights, mean = _array(output_weights, "output_weights", ndim=2), _array(consumer_mean, "consumer_mean", ndim=1)
    if (not isinstance(packet, PrunePacket) or mean.shape != weights.shape[1:]
            or len(packet.original_row) != weights.shape[1]
            or not 0 <= packet.index < weights.shape[0]
            or _digest(weights, mean) != packet.expected_post_sha256):
        raise ValueError("undo packet is incompatible with or stale for this state")
    weights[packet.index] = packet.original_row
    return weights, np.asarray(packet.original_mean, dtype=np.float64)


def diagnostic(seed: int, device: str = "cpu") -> dict:
    """Seeded exact-formula/undo contracts, not ImageNet accuracy or DEFT retention."""
    if device != "cpu":
        raise ValueError("hope-hilbert is CPU-only; no advertised CUDA path or fallback")
    if isinstance(seed, bool) or not isinstance(seed, int) or seed < 0:
        raise ValueError("nonnegative integer seed required")
    from scipy.integrate import quad

    rng = np.random.default_rng(seed)
    w, out = rng.normal(size=(2, 4)), rng.normal(size=(2, 3))
    beta, gamma = rng.uniform(-0.7, 0.7, 2), rng.uniform(0.5, 1.4, 2)
    rho = warped_correlation(w[0], w[1], gamma[0], gamma[1])
    cross = relu_cross_kernel(*[beta[0], gamma[0], beta[1], gamma[1], rho])
    conditional_sigma = gamma[1] * math.sqrt(1 - rho * rho)
    reference, _ = quad(lambda z: max(0.0, beta[0] + gamma[0] * z)
                         * relu_moments(beta[1] + gamma[1] * rho * z, conditional_sigma)[0]
                         * _phi(z), -beta[0] / gamma[0], math.inf, epsabs=1e-11, epsrel=1e-11)
    gram = operator_pair_gram(w, out, beta, gamma)
    scaled_w, scaled_out = w.copy(), out.copy()
    scaled_b, scaled_g = beta.copy(), gamma.copy()
    factor = 7.0
    scaled_w[0] *= factor
    scaled_out[0] /= factor
    scaled_b[0] *= factor
    scaled_g[0] *= factor
    scaled_gram = operator_pair_gram(scaled_w, scaled_out, scaled_b, scaled_g)
    capacities = np.array([0.25, 0.8, 1.2]) * rng.uniform(0.9, 1.1)
    footprints = np.array([3.0, 35.0, 5.0])
    rates, chosen = pruning_rates(capacities, footprints)
    wrong_choice = int(np.argmin(capacities))
    weights, mean = rng.normal(size=(3, 2)), rng.normal(size=2)
    activation_means = rng.uniform(0.1, 1.1, 3)
    pruned, adjusted, packet = prune_dense_neuron(weights, mean, chosen, activation_means[chosen])
    restored, restored_mean = restore_dense_neuron(pruned, adjusted, packet)
    before = activation_means @ weights - mean
    after_means = activation_means.copy()
    after_means[chosen] = 0
    after = after_means @ pruned - adjusted
    measures = {
        "cross_kernel_reference_error": abs(cross - reference),
        "scale_invariance_error": float(np.max(np.abs(gram - scaled_gram))),
        "gram_min_eigenvalue": float(np.linalg.eigvalsh(gram).min()),
        "bn_mean_compensation_error": float(np.max(np.abs(before - after))),
        "restore_error": float(max(np.max(np.abs(restored - weights)), np.max(np.abs(restored_mean - mean)))),
        "selected_rate": float(rates[chosen]),
        "capacity_only_negative_control_rate_gap": float(rates[wrong_choice] - rates[chosen]),
        "mean_removal_negative_control_gap": float(abs(operator_pair_gram(w, out, beta, gamma, centered=False)[0, 0] - gram[0, 0])),
    }
    checks = {
        "biased_cross_matches_conditional_integral": measures["cross_kernel_reference_error"] < 1e-10,
        "positive_neuron_gauge_invariant": measures["scale_invariance_error"] < 1e-10,
        "two_neuron_gram_psd": measures["gram_min_eigenvalue"] >= -1e-10,
        "dense_bn_mean_compensated": measures["bn_mean_compensation_error"] < 1e-12,
        "single_step_undo_exact": measures["restore_error"] == 0,
        "static_footprint_changes_selection": measures["capacity_only_negative_control_rate_gap"] > 0,
        "centering_is_not_silently_dropped": measures["mean_removal_negative_control_gap"] > 0,
    }
    return {"seed": seed, "metrics": measures, "checks": checks}
