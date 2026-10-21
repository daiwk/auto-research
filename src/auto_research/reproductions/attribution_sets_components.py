"""Attribution-set risk estimator, arXiv:2602.06276v1 §3–4 (NumPy only).

The learner receives window predictions, never conversion identities. Population
moments/prior are explicit inputs. The printed v1 coefficients fail a finite-n
mass identity for k>1; preserve this negative result rather than silently repair
the paper and advertise an unbiased estimator. See the per-paper documentation.
"""
from __future__ import annotations

import math
import numpy as np


def binomial_tail(n: int, p: float, threshold: int) -> float:
    if n < 0 or not 0 < p < 1:
        raise ValueError("n >= 0 and 0 < p < 1 required")
    if threshold <= 0:
        return 1.0
    if threshold > n:
        return 0.0
    logs = np.array([math.lgamma(n+1)-math.lgamma(i+1)-math.lgamma(n-i+1)
                     + i*math.log(p)+(n-i)*math.log1p(-p)
                     for i in range(threshold, n+1)])
    maximum = float(logs.max())
    return min(1.0, math.exp(maximum)*float(np.exp(logs-maximum).sum()))


def unbiased_cell(f2_value: float, *, n: int, p: float, j: int,
                  prior: np.ndarray, position: int, mean_f1: float,
                  mean_f2: float) -> float:
    """Literal printed Eq2, NOT a verified unbiased guarantee for k>1.

    One-indexed j/position. Caller applies 1{j <= M-k}.
    """
    pi = np.asarray(prior, dtype=float)
    k = pi.size
    if (pi.ndim != 1 or not k or not np.isfinite(pi).all() or (pi < 0).any()
            or not np.isclose(pi.sum(), 1) or not k <= j <= n
            or not 1 <= position <= k):
        raise ValueError("valid prior and one-indexed interior position required")
    if not np.isfinite([f2_value, mean_f1, mean_f2]).all():
        raise ValueError("finite loss moments required")
    b = binomial_tail(n, p, j+k)
    b_minus = binomial_tail(n-1, p, j+k-1)
    probability = pi[position-1]
    beta0 = (1-p*b_minus)/(1-p)*(1-probability)
    beta1 = probability*b/p + (b_minus-(1-p*b_minus)/(1-p))*(1-probability)
    if b <= 1e-14 or abs(beta1) <= 1e-12:
        raise ValueError("unidentifiable/numerically singular estimator; no clipping fallback")
    return float(f2_value/beta1 + mean_f1/b-beta0*mean_f2/(beta1*b))


def squared_risk(window_predictions, *, n: int, p: float, prior,
                 mean_prediction: float, mean_squared_prediction: float) -> float:
    """Literal Eq6 for squared loss; known moments, fixed denominator.

    Empty sums return zero as the indicator estimator requires; they are not
    normalized by the observed conversion count. np/2 must be integral here.
    """
    pi = np.asarray(prior, dtype=float)
    windows = np.asarray(window_predictions, dtype=float)
    k = pi.size
    if windows.size == 0:
        windows = np.empty((0, k))
    if (windows.ndim != 2 or windows.shape[1] != k or not np.isfinite(windows).all()
            or ((windows < 0) | (windows > 1)).any()):
        raise ValueError("M by k window probabilities required")
    half = n*p/2
    if not math.isclose(half, round(half)) or half < 2*k:
        raise ValueError("bounded Eq6 implementation requires integral np/2 >= 2k")
    weights = pi*pi/float(pi@pi)
    upper = min(round(half)-k, len(windows)-k)
    total = 0.0
    for j in range(k, upper+1):
        for i, weight in enumerate(weights, 1):
            if weight:
                total += weight*unbiased_cell(1-2*windows[j-1, i-1], n=n, p=p,
                    j=j, prior=pi, position=i, mean_f1=mean_squared_prediction,
                    mean_f2=1-2*mean_prediction)
    return float(total/(half-2*k+1))


def finite_erm(hypothesis_windows, parameters):
    """Select a finite hypothesis from observed weak signals, not hidden labels."""
    values = [squared_risk(windows, **parameters) for windows, parameters in
              zip(hypothesis_windows, parameters, strict=True)]
    if not values:
        raise ValueError("nonempty hypothesis set required")
    return int(np.argmin(values)), values
