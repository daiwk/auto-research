"""Paper equations 6–10; detached population targets, not VICReg substitutes."""
from __future__ import annotations

from dataclasses import dataclass
import math

import torch
from torch import Tensor
from torch.nn import functional as F


def _matrix(value: Tensor, name: str) -> None:
    if value.ndim != 2 or min(value.shape) < 1 or not value.is_floating_point():
        raise ValueError(f"{name} must be a nonempty floating-point matrix")
    if not torch.isfinite(value).all():
        raise ValueError(f"{name} must be finite")


def gaussian_quantile_targets(projected: Tensor) -> Tensor:
    """Assign each projection's rank to Phi^-1((rank+.5)/N), Eq. 6."""
    _matrix(projected, "projected")
    value = projected.detach()
    n = len(value)
    ranks = value.argsort(dim=0, stable=True).argsort(dim=0, stable=True)
    probability = (ranks.to(torch.float64) + 0.5) / n
    return (math.sqrt(2) * torch.erfinv(2 * probability - 1)).to(value.dtype)


def unit_projections(width: int, count: int, *, seed: int, dtype=torch.float32) -> Tensor:
    if not (1 <= width <= 4096 and 1 <= count <= 4096):
        raise ValueError("projection dimensions must be in 1..4096")
    generator = torch.Generator().manual_seed(seed)
    return F.normalize(torch.randn(width, count, generator=generator, dtype=dtype), dim=0)


@dataclass(frozen=True)
class GaussianAnchors:
    """CPU-owned fixed projection directions and sample-indexed quantiles."""

    directions: Tensor
    targets: Tensor
    refresh_step: int

    @classmethod
    def build(cls, representations: Tensor, directions: Tensor, *, step: int = 0):
        _matrix(representations, "representations")
        _matrix(directions, "directions")
        if representations.shape[1] != directions.shape[0] or step < 0:
            raise ValueError("projection width or refresh step is invalid")
        if not torch.allclose(directions.norm(dim=0), torch.ones(directions.shape[1], device=directions.device,
                                                               dtype=directions.dtype), atol=1e-5):
            raise ValueError("projection directions must have unit norm")
        fixed = directions.detach().cpu().clone()
        targets = gaussian_quantile_targets(representations.detach().cpu() @ fixed)
        return cls(fixed, targets.clone(), step)

    def loss(self, representations: Tensor, sample_indices: Tensor) -> Tensor:
        _matrix(representations, "representations")
        indices = validate_indices(sample_indices, len(self.targets), len(representations))
        directions = self.directions.to(device=representations.device, dtype=representations.dtype)
        targets = self.targets[indices].to(device=representations.device, dtype=representations.dtype)
        return F.mse_loss(representations @ directions, targets)


def validate_indices(indices: Tensor, population: int, batch: int) -> Tensor:
    if indices.ndim != 1 or len(indices) != batch or indices.dtype not in (torch.int32, torch.int64):
        raise ValueError("sample indices must be one integer per representation")
    indices = indices.detach().cpu().long()
    if ((indices < 0) | (indices >= population)).any():
        raise ValueError("sample index outside cached training population")
    return indices


def spherical_objective(anchors: Tensor, source: Tensor, *, tau: float = 2.0,
                        fidelity: float = 0.1) -> Tensor:
    """Eq. 8–9, off-diagonal log-mean-exp repulsion plus source attraction."""
    _matrix(anchors, "anchors")
    _matrix(source, "source")
    if anchors.shape != source.shape or len(anchors) < 2:
        raise ValueError("spherical optimization requires >=2 matched rows")
    if not (math.isfinite(tau) and tau > 0 and math.isfinite(fidelity) and fidelity >= 0):
        raise ValueError("invalid spherical hyperparameters")
    a = F.normalize(anchors, dim=1)
    z = F.normalize(source.detach(), dim=1)
    distances = (a[:, None] - a[None, :]).square().sum(-1)
    mask = ~torch.eye(len(a), dtype=torch.bool, device=a.device)
    repulsion = torch.logsumexp(-tau * distances[mask], dim=0) - math.log(mask.sum().item())
    return repulsion + fidelity * (1 - (a * z).sum(-1)).mean()


@dataclass(frozen=True)
class SphericalAnchors:
    targets: Tensor
    refresh_step: int
    optimization_steps: int

    @classmethod
    def build(cls, representations: Tensor, *, step: int = 0, seed: int = 0,
              previous: SphericalAnchors | None = None, steps: int = 20,
              subset_size: int = 256, lr: float = 0.05):
        _matrix(representations, "representations")
        if len(representations) < 2 or not (1 <= steps <= 100 and 2 <= subset_size <= 256):
            raise ValueError("bounded spherical optimization requires >=2 rows, 1..100 steps")
        if step < 0 or not (math.isfinite(lr) and lr > 0):
            raise ValueError("invalid refresh step or learning rate")
        source = F.normalize(representations.detach().cpu(), dim=1)
        generator = torch.Generator().manual_seed(seed)
        if previous is None:
            start = source + 0.01 * torch.randn(source.shape, generator=generator, dtype=source.dtype)
        else:
            if previous.targets.shape != source.shape:
                raise ValueError("previous cache does not match population")
            start = 0.5 * source + 0.5 * previous.targets
        parameter = torch.nn.Parameter(F.normalize(start, dim=1))
        optimizer = torch.optim.Adam([parameter], lr=lr)
        for _ in range(steps):
            chosen = torch.randperm(len(source), generator=generator)[:subset_size]
            optimizer.zero_grad(set_to_none=True)
            loss = spherical_objective(parameter[chosen], source[chosen])
            loss.backward()
            optimizer.step()
            with torch.no_grad():
                parameter.copy_(F.normalize(parameter, dim=1))
        return cls(parameter.detach().cpu().clone(), step, steps)

    def loss(self, representations: Tensor, sample_indices: Tensor) -> Tensor:
        _matrix(representations, "representations")
        indices = validate_indices(sample_indices, len(self.targets), len(representations))
        targets = self.targets[indices].to(device=representations.device, dtype=representations.dtype)
        return (1 - (F.normalize(representations, dim=1) * targets).sum(-1)).mean()


def in_batch_gaussian_loss(representations: Tensor, directions: Tensor) -> Tensor:
    projected = representations @ directions.to(representations)
    return F.mse_loss(projected, gaussian_quantile_targets(projected))


def alignment_loss(first: Tensor, second: Tensor) -> Tensor:
    if first.shape != second.shape:
        raise ValueError("augmented views must have matching shapes")
    return (1 - F.cosine_similarity(first, second, dim=-1)).mean()


def simclr_loss(first: Tensor, second: Tensor, *, temperature: float = 0.5) -> Tensor:
    if first.ndim != 2 or first.shape != second.shape or len(first) < 2:
        raise ValueError("SimCLR requires >=2 matched view pairs")
    if not math.isfinite(temperature) or temperature <= 0:
        raise ValueError("temperature must be positive")
    z = F.normalize(torch.cat((first, second)), dim=1)
    logits = z @ z.T / temperature
    logits = logits.masked_fill(torch.eye(len(z), dtype=torch.bool, device=z.device), -torch.inf)
    labels = (torch.arange(len(z), device=z.device) + len(first)) % len(z)
    return F.cross_entropy(logits, labels)
