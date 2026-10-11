"""OnTrack UFGW numerical core (2610.12375), not a complete monitor yet.

Exact objective, clipped online linearization, and surrogate diagnostic are
separate. No aggregate diagnostic threshold constitutes a safety decision.
"""
from __future__ import annotations

from dataclasses import dataclass

import numpy as np


def _matrix(value):
    x = np.asarray(value, dtype=np.float64)
    if x.ndim != 2 or not np.isfinite(x).all() or (x < 0).any():
        raise ValueError("finite nonnegative matrix required")
    return x


def graph_distances(parents):
    """Unsigned normalized shortest dependency hops, disconnected distance 1."""
    n = len(parents)
    if not n:
        raise ValueError("nonempty graph required")
    d = np.full((n, n), np.inf)
    np.fill_diagonal(d, 0.)
    for child, ancestors in enumerate(parents):
        for parent in ancestors:
            if not 0 <= parent < child:
                raise ValueError("chronological DAG parent required")
            d[parent, child] = d[child, parent] = 1.
    for k in range(n):
        d = np.minimum(d, d[:, k, None] + d[None, k, :])
    return np.where(np.isfinite(d), d / max(n - 1, 1), 1.)


def frontier_marginal(parents, previous, *, kappa=.3, lookahead=.3, inactive=.01):
    n = len(parents)
    if not n or not 0 < kappa <= 1 or not 0 < inactive <= lookahead <= 1:
        raise ValueError("valid frontier parameters required")
    previous = _matrix(previous)
    if previous.shape[1] != n:
        raise ValueError("reference columns must match graph")
    nominal = np.full(n, 1. / n)
    satisfied = previous.sum(0) / nominal >= kappa
    active = np.array([all(satisfied[p] for p in ps) for ps in parents])
    look = np.zeros(n, dtype=bool)
    for child, ps in enumerate(parents):
        if not active[child] and any(active[p] for p in ps):
            look[child] = True
    factors = np.where(active | satisfied, 1., np.where(look, lookahead, inactive))
    return nominal * factors, active, satisfied


def gw_gradient(coupling, prefix_distances, reference_distances):
    t = _matrix(coupling)
    a, b = _matrix(prefix_distances), _matrix(reference_distances)
    if a.shape != (len(t), len(t)) or b.shape != (t.shape[1], t.shape[1]):
        raise ValueError("distance matrices must match coupling")
    if not np.allclose(a, a.T) or not np.allclose(b, b.T):
        raise ValueError("symmetric unsigned distances required")
    p, q = t.sum(1), t.sum(0)
    return (a * a @ p)[:, None] + (b * b @ q)[None, :] - 2 * a @ t @ b.T


def _kl(a, b):
    a, b = np.asarray(a), np.asarray(b)
    if a.shape != b.shape or (b <= 0).any():
        raise ValueError("positive aligned nominal mass required")
    return float(np.sum(np.where(a > 0, a * np.log(np.maximum(a, 1e-300) / b), 0.) - a + b))


def objective(cost, coupling, prefix_distances, reference_distances, mu, nu, *, theta=.35, relaxation=.1, entropy=.05):
    c, t = _matrix(cost), _matrix(coupling)
    if c.shape != t.shape:
        raise ValueError("aligned costs and coupling required")
    g = gw_gradient(t, prefix_distances, reference_distances)
    h = float(np.sum(t * (np.log(np.maximum(t, 1e-300)) - 1)))
    return float((1 - theta) * np.sum(c * t) + theta / 2 * np.sum(g * t)
                 + relaxation * (_kl(t.sum(1), mu) + _kl(t.sum(0), nu)) + entropy * h)


def _logsumexp(value, axis):
    maximum = value.max(axis=axis, keepdims=True)
    return (maximum + np.log(np.exp(value - maximum).sum(axis=axis, keepdims=True))).squeeze(axis)


@dataclass
class CouplingState:
    coupling: np.ndarray
    log_u: np.ndarray
    log_v: np.ndarray


def sinkhorn(cost, mu, nu, *, relaxation=.1, entropy=.05, inner=5, state=None, tolerance=1e-8):
    c = _matrix(cost)
    mu, nu = np.asarray(mu, dtype=float), np.asarray(nu, dtype=float)
    if (mu.shape != (c.shape[0],) or nu.shape != (c.shape[1],) or (mu <= 0).any() or (nu <= 0).any()
            or not np.isfinite(mu).all() or not np.isfinite(nu).all() or min(relaxation, entropy, inner) <= 0):
        raise ValueError("positive finite aligned marginals and solver budget required")
    u, v = np.zeros(len(mu)), np.zeros(len(nu))
    if state is not None:
        count = len(state.log_u)
        if count > len(mu) or state.log_v.shape != v.shape:
            raise ValueError("warm state cannot shrink or change reference support")
        u[:count], v[:] = state.log_u, state.log_v
        if count:
            u[count:] = np.median(state.log_u)
    log_kernel = -c / entropy
    eta = relaxation / (relaxation + entropy)
    for _ in range(int(inner)):
        old_u, old_v = u.copy(), v.copy()
        u = eta * (np.log(mu) - _logsumexp(log_kernel + v[None, :], 1))
        v = eta * (np.log(nu) - _logsumexp(log_kernel + u[:, None], 0))
        if max(np.max(np.abs(old_u - u)), np.max(np.abs(old_v - v))) < tolerance:
            break
    t = np.exp(u[:, None] + log_kernel + v[None, :])
    if not np.isfinite(t).all():
        raise ValueError("nonfinite transport iterate")
    return CouplingState(t, u, v)


def solve(cost, prefix_distances, reference_distances, mu, nu, *, state=None, ages=None,
          outer=1, inner=5, gamma=.7, theta=.35, relaxation=.1, entropy=.05):
    c = _matrix(cost)
    if outer < 1 or not 0 < gamma <= 1 or not 0 <= theta <= 1:
        raise ValueError("valid conditional-gradient parameters required")
    t = np.zeros_like(c)
    if state is not None:
        if state.coupling.shape[1] != c.shape[1] or len(state.coupling) > len(c):
            raise ValueError("only row-growing warm support allowed")
        t[:len(state.coupling)] = state.coupling
    weights = np.ones(len(c)) if ages is None else np.asarray(ages, dtype=float)
    if weights.shape != (len(c),) or not np.isfinite(weights).all() or (weights < 0).any() or (weights > 1).any():
        raise ValueError("aligned structural age weights in [0,1] required")
    for _ in range(outer):
        g = np.maximum(gw_gradient(t, prefix_distances, reference_distances), 0.) * weights[:, None]
        linear = (1 - theta) * c + theta * g
        state = sinkhorn(linear, mu, nu, relaxation=relaxation, entropy=entropy, inner=inner, state=state)
        t = (1 - gamma) * t + gamma * state.coupling
        state = CouplingState(t, state.log_u, state.log_v)
    return state


def diagnostic(cost, coupling, prefix_distances, reference_distances, mu, nu, *, theta=.35, relaxation=.1, entropy=.05):
    """Paper's implemented mass-L1 surrogate, NOT the exact KL objective."""
    c, t = _matrix(cost), _matrix(coupling)
    g = gw_gradient(t, prefix_distances, reference_distances)
    h = float(np.sum(t * (np.log(np.maximum(t, 1e-300)) - 1)))
    total = float(t.sum())
    return float((1 - theta) * np.sum(c * t) + theta / 2 * max(float(np.sum(g * t)), 0.)
                 + relaxation * (abs(total - np.sum(mu)) + abs(total - np.sum(nu))) + entropy * h)
