"""LocaLeJEPA's local uniform-ball regularizer (arXiv:2610.28458).

Independent implementation of Sec. 4 and the authors' pure-torch fallback at
771361c18d37e65df3dc188761ffb26751ce4e37. No encoder or capability benchmark is
provided here. Neighborhood assignment is detached; residuals remain trainable.
"""
from __future__ import annotations

import math

import numpy as np
import torch
from torch import Tensor
import torch.nn.functional as F


def _projections(value: Tensor) -> Tensor:
    if value.ndim != 3 or min(value.shape) < 1 or not value.is_floating_point():
        raise ValueError("projections must be nonempty floating (views, samples, dim)")
    if not bool(torch.isfinite(value).all()):
        raise ValueError("projections must be finite")
    return value.float()


def uniform_ball_cf(frequencies: Tensor, dimension: int, *,
                    radius: float | None = None, quadrature_nodes: int = 64) -> Tensor:
    """Characteristic function of a unit-direction projection of Unif(B_R^d).

    The projected density is proportional to (1-s^2)^((d-1)/2), s in [-1,1].
    Gauss-Legendre quadrature follows the official implementation. This is NOT
    the isotropic Gaussian characteristic function used by LeJEPA.
    """
    radius = math.sqrt(dimension + 2) if radius is None else float(radius)
    if dimension < 1 or quadrature_nodes < 2 or not math.isfinite(radius) or radius <= 0:
        raise ValueError("positive dimension/radius and at least two quadrature nodes required")
    nodes, weights = np.polynomial.legendre.leggauss(quadrature_nodes)
    nodes_t = torch.as_tensor(nodes, device=frequencies.device, dtype=torch.float32)
    weight_t = torch.as_tensor(weights, device=frequencies.device, dtype=torch.float32)
    density_weight = (1 - nodes_t.square()).clamp_min(0).pow((dimension - 1) / 2) * weight_t
    return (torch.cos(frequencies.float()[..., None] * radius * nodes_t)
            * density_weight).sum(-1) / density_weight.sum()


def ballreg_loss(projections: Tensor, *, knots: int = 17, num_slices: int = 256,
                 t_max: float = 3.0, radius: float | None = None,
                 generator: torch.Generator | None = None) -> Tensor:
    """Centered per-view sketched Epps-Pulley statistic against a uniform ball.

    Integrate on [-t_max,t_max] via symmetry, with the Gaussian *window* and the
    uniform-ball *target*. N multiplies each cluster's statistic before averaging
    views and random projection directions, exactly as in the source statistic.
    """
    z = _projections(projections)
    if knots < 2 or num_slices < 1 or not math.isfinite(t_max) or t_max <= 0:
        raise ValueError("knots>=2, num_slices>=1 and finite positive t_max required")
    z = z - z.mean(dim=1, keepdim=True)
    frequencies = torch.linspace(0, t_max, knots, device=z.device)
    dt = t_max / (knots - 1)
    weights = torch.full((knots,), 2 * dt, device=z.device)
    weights[[0, -1]] = dt
    weights = weights * torch.exp(-frequencies.square() / 2)
    directions = torch.randn(z.shape[-1], num_slices, device=z.device, generator=generator)
    directions = F.normalize(directions, dim=0)
    projected = (z @ directions).unsqueeze(-1) * frequencies
    target = uniform_ball_cf(frequencies, z.shape[-1], radius=radius)
    discrepancy = ((projected.cos().mean(dim=1) - target).square()
                   + projected.sin().mean(dim=1).square())
    return (discrepancy @ weights).mean() * z.shape[1]


@torch.no_grad()
def torch_kmeans_labels(points: Tensor, num_clusters: int, *, iterations: int = 10,
                        generator: torch.Generator | None = None) -> Tensor:
    """Cosine-like Lloyd assignment used by the authors' pure-torch backend.

    Requested clusters are clipped to sample count. Empty clusters keep their
    previous centers; assignments are shared across views of the same sample.
    """
    if points.ndim != 2 or min(points.shape) < 1 or num_clusters < 1 or iterations < 1:
        raise ValueError("nonempty (samples, dim), positive clusters/iterations required")
    if not bool(torch.isfinite(points).all()):
        raise ValueError("cluster points must be finite")
    x = F.normalize(points.detach().float(), dim=-1)
    count = min(num_clusters, len(x))
    centers = x[torch.randperm(len(x), device=x.device, generator=generator)[:count]].clone()
    for _ in range(iterations):
        labels = torch.cdist(x, centers).argmin(-1)
        sums = torch.zeros_like(centers).index_add_(0, labels, x)
        sizes = torch.bincount(labels, minlength=count)
        nonempty = sizes > 0
        updated = centers.clone()
        updated[nonempty] = sums[nonempty] / sizes[nonempty, None]
        centers = F.normalize(updated, dim=-1)
    return labels


def local_ballreg_loss(projections: Tensor, *, num_clusters: int = 4,
                       min_cluster_size: int = 4, kmeans_iterations: int = 10,
                       num_global: int | None = None, knots: int = 17,
                       num_slices: int = 256, t_max: float = 3.0,
                       generator: torch.Generator | None = None,
                       stats: dict[str, float] | None = None) -> Tensor:
    """Equal-weight cluster/view LocaLeReg; whole-batch fallback is observable.

    The clustering uses the detached mean across reference views. Surviving
    neighborhoods are centered separately per view and tested against B_sqrt(d+2).
    If every neighborhood has fewer than min_cluster_size points, the centered
    whole-batch test runs rather than returning zero. No global Gaussian target.
    """
    z = _projections(projections)
    if num_clusters < 1 or min_cluster_size < 1:
        raise ValueError("positive num_clusters/min_cluster_size required")
    if num_global is not None and not 1 <= num_global <= z.shape[0]:
        raise ValueError("num_global must select at least one existing view")
    reference = z if num_global is None else z[:num_global]
    labels = torch_kmeans_labels(reference.mean(0).detach(), num_clusters,
                                 iterations=kmeans_iterations, generator=generator)
    sizes = torch.bincount(labels, minlength=min(num_clusters, z.shape[1])).tolist()
    kept = [index for index, size in enumerate(sizes) if size >= min_cluster_size]
    if stats is not None:
        stats.update(configured_clusters=float(num_clusters), effective_clusters=float(len(kept)),
                     kept_fraction=sum(sizes[index] for index in kept) / z.shape[1],
                     fallback=float(not kept))
    arguments = dict(knots=knots, num_slices=num_slices, t_max=t_max, generator=generator)
    if not kept:
        return ballreg_loss(z, **arguments)
    return torch.stack([ballreg_loss(z[:, labels == index], **arguments) for index in kept]).mean()


def locale_jepa_loss(projections: Tensor, *, regularization_weight: float = 0.1,
                     num_global: int | None = None, **kwargs) -> dict[str, Tensor]:
    """Prediction Eq. 4 plus LocaLeReg, without EMA teacher or stop-gradient."""
    if not 0 <= regularization_weight <= 1:
        raise ValueError("regularization_weight must be in [0, 1]")
    z = _projections(projections)
    if num_global is not None and not 1 <= num_global <= z.shape[0]:
        raise ValueError("num_global must select at least one existing view")
    reference = z if num_global is None else z[:num_global]
    prediction = (z - reference.mean(0, keepdim=True)).square().mean()
    regularizer = local_ballreg_loss(z, num_global=num_global, **kwargs)
    total = (1 - regularization_weight) * prediction + regularization_weight * regularizer
    return {"loss": total, "prediction": prediction, "regularizer": regularizer}
