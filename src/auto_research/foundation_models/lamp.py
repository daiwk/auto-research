"""Support-calibrated LAMP and exact LAMP-F response (arXiv:2610.22182).

The encoder is deliberately outside this feature-level component. No query/test
labels enter calibration, fitting, prediction or prototype training.
"""
from __future__ import annotations

from dataclasses import dataclass
import math
from typing import Sequence

import torch
from torch.nn import functional as F


def vit_regions(tokens: torch.Tensor) -> torch.Tensor:
    """Eq.4: token LN -> token L2 -> 2x2 mean -> regional L2."""
    if tokens.ndim != 4 or min(tokens.shape) < 1 or min(tokens.shape[1:3]) < 2:
        raise ValueError("[batch,height>=2,width>=2,channels] patch tokens required")
    normalized = F.normalize(F.layer_norm(tokens, (tokens.shape[-1],)), dim=-1)
    pooled = F.adaptive_avg_pool2d(normalized.permute(0, 3, 1, 2), (2, 2))
    return F.normalize(pooled.flatten(2).transpose(1, 2), dim=-1)


def resnet_regions(activations: torch.Tensor) -> torch.Tensor:
    """Eq.5: nonnegative C3/C4/C5 GeM(p=3) -> regional L2."""
    if activations.ndim != 4 or min(activations.shape) < 1 or min(activations.shape[2:]) < 2:
        raise ValueError("[batch,channels,height>=2,width>=2] activations required")
    if not bool(torch.isfinite(activations).all()) or bool((activations < 0).any()):
        raise ValueError("finite post-ReLU activations required")
    pooled = F.adaptive_avg_pool2d(activations.pow(3), (2, 2)).clamp_min(0).pow(1 / 3)
    return F.normalize(pooled.flatten(2).transpose(1, 2), dim=-1)


@dataclass(frozen=True)
class FeatureBatch:
    global_features: torch.Tensor
    regional_features: tuple[torch.Tensor, ...]
    sample_ids: tuple[str, ...]

    def validate(self) -> None:
        n = self.global_features.shape[0] if self.global_features.ndim == 2 else 0
        if n < 1 or self.global_features.shape[1] < 1 or len(self.regional_features) != 3:
            raise ValueError("nonempty global descriptors and three native-layer regional branches required")
        if len(self.sample_ids) != n or len(set(self.sample_ids)) != n or any(not s for s in self.sample_ids):
            raise ValueError("one unique nonempty identity per feature view required")
        if any(t.ndim != 3 or t.shape[0] != n or t.shape[1] != 4 or t.shape[2] < 1 for t in self.regional_features):
            raise ValueError("each regional branch must have shape [views,4,native_width]")
        for tensor in (self.global_features, *self.regional_features):
            if not tensor.is_floating_point() or tensor.dtype != self.global_features.dtype or tensor.device != self.global_features.device:
                raise ValueError("features must share floating dtype/device")
            if not bool(torch.isfinite(tensor).all()):
                raise ValueError("finite features required")
            if not bool(torch.allclose(tensor.norm(dim=-1), torch.ones_like(tensor[..., 0]), atol=1e-5, rtol=1e-5)):
                raise ValueError("unit descriptors required")


@dataclass(frozen=True)
class Mixture:
    rho: float
    weights: tuple[float, float, float]

    def coefficients(self) -> tuple[float, float, float, float]:
        if not math.isfinite(self.rho) or not 0 <= self.rho <= 1:
            raise ValueError("rho must be in [0,1]")
        if len(self.weights) != 3 or any(not math.isfinite(x) or x < 0 for x in self.weights) or not math.isclose(sum(self.weights), 1., abs_tol=1e-8):
            raise ValueError("three finite nonnegative regional weights summing to one required")
        return (1 - self.rho, *(self.rho * w for w in self.weights))


@dataclass(frozen=True)
class CachedResponse:
    base_scores: torch.Tensor
    prototype_response: torch.Tensor
    text_prototypes: torch.Tensor

    def predict(self, prototypes: torch.Tensor) -> torch.Tensor:
        if prototypes.shape != self.text_prototypes.shape or not bool(torch.isfinite(prototypes).all()):
            raise ValueError("finite prototypes of the original shape required")
        gamma = F.normalize(prototypes, dim=-1) - self.text_prototypes
        return self.base_scores + self.prototype_response @ gamma.T


def _global_kernel(left: torch.Tensor, right: torch.Tensor, beta: float) -> torch.Tensor:
    return torch.exp(-beta * (1 - left @ right.T))


def _regional_kernel(left: torch.Tensor, right: torch.Tensor, beta: float) -> torch.Tensor:
    # Mean all 4x4 regional pair affinities, independent of spatial ordering.
    def self_affinity(x):
        return torch.exp(-beta * (1 - torch.einsum("njd,nkd->njk", x, x))).mean((1, 2))
    affinity = torch.exp(-beta * (1 - torch.einsum("ajd,bkd->abjk", left, right))).mean((-1, -2))
    return affinity / torch.sqrt(self_affinity(left)[:, None] * self_affinity(right)[None])


class LampPredictor:
    """Frozen feature bank with support-only calibration and residual fitting."""

    def __init__(self, support: FeatureBatch, labels: torch.Tensor, text_prototypes: torch.Tensor, *,
                 regularization: float = 1., global_bandwidth: float = 1., regional_ratio: float = 1.,
                 support_image_ids: Sequence[str] | None = None):
        support.validate()
        if any(not math.isfinite(x) or x <= 0 for x in (regularization, global_bandwidth, regional_ratio)):
            raise ValueError("positive finite regularization and bandwidths required")
        if text_prototypes.ndim != 2 or text_prototypes.shape[1] != support.global_features.shape[1] or text_prototypes.shape[0] < 2:
            raise ValueError("[classes,global_width] text prototypes required")
        if text_prototypes.device != support.global_features.device or text_prototypes.dtype != support.global_features.dtype:
            raise ValueError("text and visual descriptors must share dtype/device")
        if not bool(torch.isfinite(text_prototypes).all()) or not torch.allclose(text_prototypes.norm(dim=-1), torch.ones_like(text_prototypes[:, 0]), atol=1e-5, rtol=1e-5):
            raise ValueError("finite unit text prototypes required")
        self.support = FeatureBatch(support.global_features.detach().clone(),
                                    tuple(t.detach().clone() for t in support.regional_features), support.sample_ids)
        self.text = text_prototypes.detach().clone()
        self._labels(labels, len(support.sample_ids))
        if set(labels.tolist()) != set(range(self.text.shape[0])):
            raise ValueError("support must represent every class")
        self.labels = labels.detach().clone()
        self.regularization, self.beta = regularization, global_bandwidth
        self.regional_beta = global_bandwidth * regional_ratio
        self.one_hot = F.one_hot(self.labels, self.text.shape[0]).to(self.text.dtype)
        self.support_means: list[torch.Tensor] = []
        self.support_variances: list[torch.Tensor] = []
        self.grand_means: list[torch.Tensor] = []
        matrices = [_global_kernel(self.support.global_features, self.support.global_features, self.beta)]
        for regional in self.support.regional_features:
            kernel = _regional_kernel(regional, regional, self.regional_beta)
            mean, grand = kernel.mean(1), kernel.mean()
            variance = (1 - 2 * mean + grand).clamp_min(1e-10)
            matrices.append((kernel - mean[:, None] - mean[None] + grand) / torch.sqrt(variance[:, None] * variance[None]))
            self.support_means.append(mean)
            self.support_variances.append(variance)
            self.grand_means.append(grand)
        identity = torch.eye(len(self.labels), dtype=self.text.dtype, device=self.text.device)
        self.systems = tuple(identity + kernel / self.regularization for kernel in matrices)
        residual = self.one_hot - self.support.global_features @ self.text.T
        self.alphas = tuple(torch.linalg.solve(system, residual) for system in self.systems)
        self.responses = tuple(torch.linalg.solve(system, self.support.global_features) for system in self.systems)
        image_ids = tuple(support_image_ids) if support_image_ids is not None else support.sample_ids
        if len(image_ids) != len(self.labels) or any(not value for value in image_ids):
            raise ValueError("one nonempty source-image identity per support view required")
        self.image_groups = tuple(tuple(i for i, value in enumerate(image_ids) if value == key) for key in dict.fromkeys(image_ids))
        if any(len(set(self.labels[list(indices)].tolist())) != 1 for indices in self.image_groups):
            raise ValueError("views of a source image must have one class label")

    def _labels(self, labels: torch.Tensor, size: int) -> None:
        if labels.shape != (size,) or labels.dtype != torch.int64 or labels.device != self.text.device:
            raise ValueError("one same-device int64 label per sample required")
        if bool(((labels < 0) | (labels >= self.text.shape[0])).any()):
            raise ValueError("label outside class range")

    def query_kernels(self, batch: FeatureBatch) -> tuple[torch.Tensor, ...]:
        batch.validate()
        if batch.global_features.shape[1] != self.text.shape[1] or any(q.shape[-1] != s.shape[-1] for q, s in zip(batch.regional_features, self.support.regional_features, strict=True)):
            raise ValueError("query feature widths differ from fitted support widths")
        if batch.global_features.device != self.text.device or batch.global_features.dtype != self.text.dtype:
            raise ValueError("query and support dtype/device differ")
        kernels = [_global_kernel(batch.global_features.detach(), self.support.global_features, self.beta)]
        for index, regional in enumerate(batch.regional_features):
            raw = _regional_kernel(regional.detach(), self.support.regional_features[index], self.regional_beta)
            mean, grand = raw.mean(1), self.grand_means[index]
            variance = (1 - 2 * mean + grand).clamp_min(1e-10)
            kernels.append((raw - mean[:, None] - self.support_means[index][None] + grand)
                           / torch.sqrt(variance[:, None] * self.support_variances[index][None]))
        return tuple(kernels)

    def predict(self, batch: FeatureBatch, mixture: Mixture, prototypes: torch.Tensor | None = None) -> torch.Tensor:
        weights = mixture.coefficients()
        proto = self.text if prototypes is None else F.normalize(prototypes, dim=-1)
        if proto.shape != self.text.shape or not bool(torch.isfinite(proto).all()):
            raise ValueError("finite prototypes of the original shape required")
        residual = self.one_hot - self.support.global_features @ proto.T
        kernels = self.query_kernels(batch)
        # Deliberately fresh solves: an independent path for testing Eq.14.
        correction = sum(w * (kernel @ torch.linalg.solve(system, residual))
                         for w, kernel, system in zip(weights, kernels, self.systems, strict=True))
        return batch.global_features.detach() @ proto.T + correction

    def cache(self, batch: FeatureBatch, mixture: Mixture) -> CachedResponse:
        weights = mixture.coefficients()
        kernels = self.query_kernels(batch)
        base = batch.global_features.detach() @ self.text.T + sum(w * h @ alpha for w, h, alpha in zip(weights, kernels, self.alphas, strict=True))
        response = batch.global_features.detach() - sum(w * h @ b for w, h, b in zip(weights, kernels, self.responses, strict=True))
        return CachedResponse(base, response, self.text)

    def prototype_loss(self, prototypes: torch.Tensor) -> torch.Tensor:
        """Eq.12 uses support images only, averaging views without renormalizing."""
        if prototypes.shape != self.text.shape or not bool(torch.isfinite(prototypes).all()):
            raise ValueError("finite prototypes of the original shape required")
        means = torch.stack([self.support.global_features[list(group)].mean(0) for group in self.image_groups])
        labels = torch.stack([self.labels[group[0]] for group in self.image_groups])
        logits = self.support.global_features @ self.text.T
        confidence = logits.softmax(-1).gather(1, self.labels[:, None]).squeeze(1)
        anchors = torch.stack([confidence[self.labels == c].mean() for c in range(self.text.shape[0])])
        return F.cross_entropy(100 * means @ F.normalize(prototypes, dim=-1).T, labels) + (
            anchors * (prototypes - self.text).square().sum(-1)).mean()


def select_mixture(model: LampPredictor, validation: FeatureBatch, validation_labels: torch.Tensor,
                   candidates: Sequence[Mixture]) -> tuple[Mixture, float]:
    """Validation-only selection. Test batches/labels are absent from this API."""
    if set(validation.sample_ids) & set(model.support.sample_ids):
        raise ValueError("support/validation identities overlap")
    model._labels(validation_labels, len(validation.sample_ids))
    if not candidates:
        raise ValueError("at least one mixture candidate required")
    with torch.no_grad():
        cache = [model.cache(validation, candidate).base_scores for candidate in candidates]
        scores = [float((logits.argmax(-1) == validation_labels).double().mean()) for logits in cache]
    index = max(range(len(scores)), key=scores.__getitem__)
    return candidates[index], scores[index]


def evaluate_test(model: LampPredictor, test: FeatureBatch, test_labels: torch.Tensor,
                  mixture: Mixture, *, validation_ids: Sequence[str]) -> dict[str, float]:
    """Final report only; no fitted state or mixture is changed by test labels."""
    if set(test.sample_ids) & (set(model.support.sample_ids) | set(validation_ids)):
        raise ValueError("test identities overlap support/validation")
    model._labels(test_labels, len(test.sample_ids))
    with torch.no_grad():
        return {"accuracy": float((model.predict(test, mixture).argmax(-1) == test_labels).double().mean()),
                "examples": len(test.sample_ids)}
