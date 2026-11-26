"""CPU-only RAP Eq. (11)-(12), arXiv:2611.34298v1.

This is a hyperbolic compression component, not a vision-language model.
The canonical Lorentz origin is used; no embedding training or downloads occur.
"""
from __future__ import annotations

import math
import numpy as np

REQUIRES_GPU_VALIDATION = False


def _curvature(c: float) -> float:
    if not math.isfinite(c) or c <= 0:
        raise ValueError("curvature magnitude must be positive and finite")
    return math.sqrt(c)


def polar_to_lorentz(radii, directions, *, curvature: float = 1.0):
    root = _curvature(curvature)
    r, u = np.asarray(radii, dtype=np.float64), np.asarray(directions, dtype=np.float64)
    if r.ndim != 1 or u.ndim != 2 or len(r) != len(u) or u.shape[1] < 1:
        raise ValueError("one radius and direction per point required")
    if not np.isfinite(r).all() or not np.isfinite(u).all() or (r < 0).any():
        raise ValueError("finite nonnegative radii and finite directions required")
    if not np.allclose(np.linalg.norm(u, axis=1), 1, atol=1e-10, rtol=1e-10):
        raise ValueError("directions must be unit vectors, including at the origin")
    with np.errstate(over="ignore"):
        result = np.column_stack((np.cosh(root * r), np.sinh(root * r)[:, None] * u)) / root
    if not np.isfinite(result).all():
        raise ValueError("radii exceed the numerical range")
    return result


def lorentz_to_polar(points, *, curvature: float = 1.0):
    root = _curvature(curvature)
    x = np.asarray(points, dtype=np.float64)
    if x.ndim != 2 or x.shape[1] < 2 or not np.isfinite(x).all():
        raise ValueError("finite Lorentz points required")
    norm = np.linalg.norm(x[:, 1:], axis=1)
    expected_time = np.hypot(1 / root, norm)
    if not np.allclose(x[:, 0], expected_time, atol=1e-10, rtol=1e-10):
        raise ValueError("points must lie on the upper hyperboloid")
    # asinh(spatial norm) is more stable at the origin than acosh(time).
    r = np.arcsinh(root * norm) / root
    u = np.zeros_like(x[:, 1:])
    nonzero = norm > 0
    u[nonzero] = x[nonzero, 1:] / norm[nonzero, None]
    u[~nonzero, 0] = 1
    return r, u


def _projection(points, matrix, curvature):
    r, u = lorentz_to_polar(points, curvature=curvature)
    p = np.asarray(matrix, dtype=np.float64)
    if p.ndim != 2 or p.shape[1] != u.shape[1] or not p.shape[0] or not np.isfinite(p).all():
        raise ValueError("finite target-by-source projection matrix required")
    return r, u, p


def project_rap(points, matrix, *, curvature: float = 1.0):
    """Keep radius exactly; normalize the Gaussian-sketched angular direction."""
    r, u, p = _projection(points, matrix, curvature)
    angular = u @ p.T
    norm = np.linalg.norm(angular, axis=1)
    if ((norm == 0) & (r > 0)).any():
        raise ValueError("RAP is undefined for a non-anchor direction in the projection kernel")
    origin = r == 0
    angular[origin] = 0
    angular[origin, 0] = 1
    norm[origin] = 1
    return polar_to_lorentz(r, angular / norm[:, None], curvature=curvature)


def project_tangent(points, matrix, *, curvature: float = 1.0):
    """Canonical-origin log -> Gaussian sketch -> exp comparator, Eq. (7)."""
    r, u, p = _projection(points, matrix, curvature)
    tangent = (r[:, None] * u) @ p.T
    radius = np.linalg.norm(tangent, axis=1)
    directions = np.zeros_like(tangent)
    nonzero = radius > 0
    directions[nonzero] = tangent[nonzero] / radius[nonzero, None]
    directions[~nonzero, 0] = 1
    return polar_to_lorentz(radius, directions, curvature=curvature)


def project_spatial(points, matrix, *, curvature: float = 1.0):
    """Spatial sketch and recomputed time coordinate, Eq. (9)."""
    _, _, p = _projection(points, matrix, curvature)
    spatial = np.asarray(points)[:, 1:] @ p.T
    return np.column_stack((np.sqrt(1 / curvature + np.square(spatial).sum(axis=1)), spatial))


def pairwise_distance(points, *, curvature: float = 1.0):
    """Hyperbolic law of cosines with a stable radial-difference expression."""
    root = _curvature(curvature)
    r, u = lorentz_to_polar(points, curvature=curvature)
    angle_loss = np.clip(1 - u @ u.T, 0, 2)
    a = root * r
    argument = np.cosh(a[:, None] - a[None, :]) + np.outer(np.sinh(a), np.sinh(a)) * angle_loss
    result = np.arccosh(np.maximum(argument, 1)) / root
    np.fill_diagonal(result, 0)
    return result


def diagnostic(seed: int, device: str = "cpu") -> dict:
    if type(seed) is not int or device != "cpu":
        raise ValueError("integer seed and CPU-only execution required")
    rng = np.random.default_rng(seed)
    u = rng.normal(size=(128, 32))
    u /= np.linalg.norm(u, axis=1, keepdims=True)
    r = rng.uniform(0.1, 2, len(u))
    r[0] = 0
    x = polar_to_lorentz(r, u)
    p = rng.normal(size=(8, 32)) / math.sqrt(8)
    y = project_rap(x, p)
    yr, _ = lorentz_to_polar(y)
    original = pairwise_distance(x)
    mask = np.triu(original > 1e-10, 1)
    distortion = lambda z: float(np.abs(pairwise_distance(z)[mask] / original[mask] - 1).mean())
    ray = polar_to_lorentz(np.array([0.2, 1.1, 1.9]), np.tile(u[1], (3, 1)))
    ray_error = float(np.max(np.abs(pairwise_distance(project_rap(ray, p)) - pairwise_distance(ray))))
    manifold_error = float(np.max(np.abs(-y[:, 0] ** 2 + (y[:, 1:] ** 2).sum(axis=1) + 1)))
    return {"seed": seed, "device": device, "evaluation_tier": "l1_mechanism", "diagnostic_only": True,
            "checks": {"exact_radius": bool(np.max(np.abs(yr-r)) < 1e-12),
                       "target_hyperboloid": bool(manifold_error < 1e-12),
                       "same_ray_distance": bool(ray_error < 1e-7),
                       "anchor_is_preserved": bool(np.array_equal(y[0], np.array([1.] + [0.]*8)))},
            "metrics": {"radial_max_abs_error": float(np.max(np.abs(yr-r))),
                        "hyperboloid_max_abs_error": manifold_error, "same_ray_max_abs_error": ray_error,
                        "rap_mean_relative_distortion": distortion(y),
                        "tangent_mean_relative_distortion": distortion(project_tangent(x,p)),
                        "spatial_mean_relative_distortion": distortion(project_spatial(x,p)),
                        "points": len(x), "source_dimension": 32, "target_dimension": 8}}
