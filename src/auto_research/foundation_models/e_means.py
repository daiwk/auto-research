"""Bounded dense CPU reference for e-means v1 Algorithm 1."""

from __future__ import annotations

from dataclasses import dataclass
import math

import numpy as np
from numpy.typing import NDArray

REQUIRES_GPU_VALIDATION = False
_INITIAL_COUNT = 1e-10
_BF16_EPSILON = 2.0**-7


@dataclass(frozen=True)
class EMeansFit:
    centers: NDArray[np.float64]
    ema_centers: NDArray[np.float64]
    last_assignments: NDArray[np.intp]
    revival_count: int
    steps: int


def cosine_step(index: int, updates: int, alpha0: float) -> float:
    """Equation 5's zero-based schedule; the nominal floor is at index M."""
    if not 0 <= index < updates or not 0 < alpha0 <= 1:
        raise ValueError("expected 0 <= index < updates and 0 < alpha0 <= 1")
    return alpha0 * (0.1 + 0.45 * (1.0 + math.cos(math.pi * index / updates)))


def _assign(rows: NDArray, centers: NDArray) -> NDArray[np.intp]:
    # Small reference inputs use direct L2 and deterministic lowest-ID tie break.
    delta = rows[:, None, :] - centers[None, :, :]
    return np.einsum("ijk,ijk->ij", delta, delta).argmin(axis=1)


def _stats(rows: NDArray, labels: NDArray, k: int) -> tuple[NDArray, NDArray]:
    counts = np.bincount(labels, minlength=k)
    sums = np.zeros((k, rows.shape[1]), dtype=np.float64)
    np.add.at(sums, labels, rows)
    return counts, sums


def _centers(counts: NDArray, sums: NDArray, previous: NDArray) -> NDArray:
    return np.divide(sums, counts[:, None], out=previous.copy(), where=counts[:, None] > 0)


def _revive(counts: NDArray, sums: NDArray, rng: np.random.Generator) -> int:
    """Appendix H: split live donors once each and overwrite weak slots."""
    threshold = 0.1 * float(counts.mean())
    weak = np.flatnonzero(counts < threshold)
    donors = np.flatnonzero((counts >= threshold) & (counts > 0))
    n = min(len(weak), len(donors))
    if not n:
        return 0
    # If too few unique live donors exist, defer remaining weak slots to the next check.
    selected = rng.choice(donors, size=n, replace=False, p=counts[donors] / counts[donors].sum())
    weak = weak[:n]
    center = sums[selected] / counts[selected, None]
    half = counts[selected] / 2.0
    offset = _BF16_EPSILON * np.where(np.arange(sums.shape[1]) % 2 == 0, 1, -1)
    counts[weak] = counts[selected] = half
    sums[weak] = center * (1.0 + offset) * half[:, None]
    sums[selected] = center * (1.0 - offset) * half[:, None]
    return n


def fit(
    rows: NDArray, *, k: int, epochs: int, batch_size: int, alpha0: float, seed: int,
    initial_indices: NDArray | None = None,
) -> EMeansFit:
    """Run a bounded exact-L2 reference on fully covered mini-batches."""
    data = np.asarray(rows, dtype=np.float64)
    if data.ndim != 2 or not data.shape[1] or not np.isfinite(data).all():
        raise ValueError("expected a finite rank-two vector matrix with positive dimension")
    n, d = data.shape
    if not all(type(value) is int for value in (k, epochs, batch_size)):
        raise ValueError("k, epochs and batch_size must be integers")
    if not 1 <= k <= n or not 1 <= batch_size <= n or n % batch_size or epochs < 1:
        raise ValueError("positive sizes required, with k <= n and batch_size dividing n")
    if batch_size * k * d > 2_000_000 or epochs * n * k * d > 50_000_000:
        raise ValueError("input exceeds bounded CPU reference budget")
    if not 0 < alpha0 <= 1:
        raise ValueError("alpha0 must be in (0, 1]")
    rng = np.random.default_rng(seed)
    if initial_indices is None:
        indices = rng.choice(n, size=k, replace=False)
    else:
        indices = np.asarray(initial_indices)
        if (indices.shape != (k,) or not np.issubdtype(indices.dtype, np.integer)
                or np.any((indices < 0) | (indices >= n)) or np.unique(indices).size != k):
            raise ValueError("initial_indices must be k distinct training row indices")
    centers = data[indices].copy()
    counts = np.full(k, _INITIAL_COUNT)
    sums = counts[:, None] * centers
    labels = np.empty(n, dtype=np.intp)
    updates = epochs * (n // batch_size)
    step = revivals = 0
    for epoch in range(epochs):
        order = rng.permutation(n)
        for ids in order.reshape(-1, batch_size):
            batch = data[ids]
            assigned = _assign(batch, centers)
            if epoch == epochs - 1:
                labels[ids] = assigned
            batch_counts, batch_sums = _stats(batch, assigned, k)
            alpha = cosine_step(step, updates, alpha0)
            counts = (1.0 - alpha) * counts + alpha * batch_counts
            sums = (1.0 - alpha) * sums + alpha * batch_sums
            step += 1
            if step % 5 == 0:
                revivals += _revive(counts, sums, rng)
            # With alpha=1, an unassigned center can have exactly zero mass.
            centers = _centers(counts, sums, centers)
    last_counts, last_sums = _stats(data, labels, k)
    return EMeansFit(_centers(last_counts, last_sums, centers), centers, labels, revivals, step)


def diagnostic(seed: int, device: str = "cpu") -> dict:
    """Check exact arithmetic, weak-donor split and fixed-label closing mean."""
    if device != "cpu":
        raise ValueError("e-means diagnostic is CPU-only")
    rng = np.random.default_rng(seed)
    locations = rng.normal(size=(8, 12)) * 2.0
    train = locations[np.arange(256) % 8] + rng.normal(0, 0.4, size=(256, 12))
    holdout = locations[np.arange(64) % 8] + rng.normal(0, 0.4, size=(64, 12))
    init = rng.choice(len(train), size=16, replace=False)
    fit_result = fit(train, k=16, epochs=4, batch_size=32, alpha0=0.24, seed=seed, initial_indices=init)
    labels = fit_result.last_assignments
    closing_mse = float(np.square(train - fit_result.centers[labels]).sum(axis=1).mean())
    ema_mse = float(np.square(train - fit_result.ema_centers[labels]).sum(axis=1).mean())
    lloyd = train[init].copy()
    for _ in range(4):
        counts, sums = _stats(train, _assign(train, lloyd), len(lloyd))
        lloyd = _centers(counts, sums, lloyd)

    def holdout_mse(centers: NDArray) -> float:
        return float(np.square(holdout - centers[_assign(holdout, centers)]).sum(axis=1).mean())

    counts = np.array([8.0, 0.1])
    sums = np.array([[16.0, 32.0], [0.0, 0.0]])
    split = _revive(counts, sums, rng)
    return {
        "seed": seed,
        "diagnostic_only": True,
        "evaluation_tier": "l1_mechanism",
        "metrics": {
            "vectors": len(train), "heldout_vectors": len(holdout), "dimension": train.shape[1],
            "centers": len(lloyd), "ema_updates": fit_result.steps, "revivals": fit_result.revival_count,
            "closing_fixed_label_mse": closing_mse, "ema_fixed_label_mse": ema_mse,
            "e_means_heldout_mse": holdout_mse(fit_result.centers), "lloyd_heldout_mse": holdout_mse(lloyd),
        },
        "checks": {
            "closing_mean_minimizes_fixed_label_mse": closing_mse <= ema_mse + 1e-12,
            "cosine_schedule_anneals": cosine_step(0, 32, 0.24) > cosine_step(31, 32, 0.24),
            "revival_splits_live_mass_and_sum": bool(
                split == 1 and np.array_equal(counts, [4.0, 4.0])
                and np.allclose(sums.sum(axis=0), [16.0, 32.0]) and not np.array_equal(sums[0], sums[1])
            ),
            "nearest_assignment_has_stable_ties": bool(_assign(np.array([[0.0]]), np.array([[-1.0], [1.0]]))[0] == 0),
            "all_training_points_accounted_for": len(labels) == len(train) and fit_result.steps == 32,
        },
    }
