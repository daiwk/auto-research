"""Cheap Signals v1 §3: CP/ordinal kernels and frozen-human calibration.

New official November16 code release, historical March paper. Supplied ratings
are not generated here. This implements component likelihood/gradient/conditional
interval arithmetic, not the complete Adam/BFGS fitting or population inference.
"""

from __future__ import annotations

from statistics import NormalDist
import math
import torch
from torch import Tensor

REQUIRES_GPU_VALIDATION = True


def capability_tensor(models: Tensor, prompts: Tensor, raters: Tensor) -> Tensor:
    if (
        any(
            x.ndim != 2 or not x.numel() or not torch.isfinite(x).all()
            for x in (models, prompts, raters)
        )
        or len({x.shape[1] for x in (models, prompts, raters)}) != 1
    ):
        raise ValueError("finite model/prompt/rater factors of shared rank required")
    return torch.einsum("ir,jr,kr->ijk", models, prompts, raters)


def ordinal_probabilities(delta: Tensor, cutoffs: Tensor) -> Tensor:
    """Eq3.1; rater-specific strict cutoffs, not a binary sigmoid shortcut."""
    if (
        cutoffs.ndim != 1
        or not cutoffs.numel()
        or not torch.isfinite(cutoffs).all()
        or not torch.isfinite(delta).all()
        or (cutoffs[1:] <= cutoffs[:-1]).any()
    ):
        raise ValueError("finite advantages and strictly ordered finite cutoffs required")
    cdf = (cutoffs - delta[..., None]).sigmoid()
    return torch.cat((cdf[..., :1], cdf[..., 1:] - cdf[..., :-1], 1 - cdf[..., -1:]), dim=-1)


def frozen_human_nll(
    models: Tensor,
    prompts: Tensor,
    human: Tensor,
    cutoffs: Tensor,
    model_indices: Tensor,
    prompt_indices: Tensor,
    labels: Tensor,
    *,
    opponents: Tensor | None = None,
) -> Tensor:
    """Stage2: only human factors/cutoffs receive gradients; no autorater refit.

    Optional opponents creates pairwise capability differences, preserving ties
    through the same ordinal likelihood. Model IDs are not human labels.
    """
    if (
        model_indices.ndim != 1
        or not model_indices.numel()
        or prompt_indices.shape != model_indices.shape
        or labels.shape != model_indices.shape
        or model_indices.dtype != torch.long
        or prompt_indices.dtype != torch.long
        or labels.dtype != torch.long
        or (model_indices < 0).any()
        or (model_indices >= len(models)).any()
        or (prompt_indices < 0).any()
        or (prompt_indices >= len(prompts)).any()
        or (labels < 0).any()
        or (labels > len(cutoffs)).any()
    ):
        raise ValueError("nonempty aligned valid categorical observation indices required")
    features = models.detach()[model_indices] * prompts.detach()[prompt_indices]
    if opponents is not None:
        if (
            opponents.shape != model_indices.shape
            or opponents.dtype != torch.long
            or (opponents < 0).any()
            or (opponents >= len(models)).any()
        ):
            raise ValueError("valid paired opponent indices required")
        features = features - models.detach()[opponents] * prompts.detach()[prompt_indices]
    if human.shape != models.shape[1:] or models.shape[1:] != prompts.shape[1:]:
        raise ValueError("shared latent rank required")
    p = ordinal_probabilities(features @ human, cutoffs)
    likelihood = p.gather(-1, labels[:, None]).squeeze(-1)
    if (likelihood <= 0).any():
        raise ValueError("likelihood underflow; no silent clipping of statistical objective")
    return -likelihood.log().mean()


def conditional_wald(
    feature: Tensor,
    human: Tensor,
    covariance: Tensor,
    samples: int,
    *,
    confidence: float = 0.95,
    comparisons: int = 1,
):
    """§3.3 conditional CI with optional Bonferroni; upstream factor error omitted.

    covariance is the asymptotic Sigma, not already-divided estimator covariance.
    No claim of validity after optional all-parameter human fine-tuning.
    """
    r = human.numel()
    if (
        feature.shape != human.shape
        or covariance.shape != (r, r)
        or type(samples) is not int
        or samples < 1
        or type(comparisons) is not int
        or comparisons < 1
        or not 0 < confidence < 1
        or not torch.isfinite(feature).all()
        or not torch.isfinite(human).all()
        or not torch.isfinite(covariance).all()
        or not torch.allclose(covariance, covariance.T)
        or torch.linalg.eigvalsh(covariance).min() < -1e-10
    ):
        raise ValueError(
            "finite feature/head, symmetric PSD covariance and positive sample count required"
        )
    z = NormalDist().inv_cdf(1 - (1 - confidence) / (2 * comparisons))
    center = feature @ human
    radius = z * (feature @ covariance @ feature / samples).clamp_min(0).sqrt()
    return center - radius, center + radius


def diagnostic(seed: int, device: str = "cpu") -> dict:
    if type(seed) is not int or device not in {"cpu", "cuda"}:
        raise ValueError("integer seed and explicit cpu/cuda device required")
    torch.manual_seed(seed)
    models = torch.randn(4, 3, device=device, dtype=torch.float64, requires_grad=True)
    prompts = torch.randn(6, 3, device=device, dtype=torch.float64, requires_grad=True)
    raters = torch.randn(2, 3, device=device, dtype=torch.float64)
    tensor = capability_tensor(models, prompts, raters)
    human = torch.zeros(3, device=device, dtype=torch.float64, requires_grad=True)
    cutoffs = torch.tensor([-1.0, 0.3], device=device, dtype=torch.float64, requires_grad=True)
    indices = torch.tensor([0, 1, 2, 3], device=device)
    loss = frozen_human_nll(models, prompts, human, cutoffs, indices, indices, indices % 3)
    loss.backward()
    p = ordinal_probabilities(tensor[0, :, 0], cutoffs.detach())
    feature = torch.ones(3, device=device, dtype=torch.float64)
    cov = torch.eye(3, device=device, dtype=torch.float64)
    ordinary = conditional_wald(feature, human.detach(), cov, 20)
    simultaneous = conditional_wald(feature, human.detach(), cov, 20, comparisons=24)
    return {
        "seed": seed,
        "diagnostic_only": True,
        "evaluation_tier": "l1_mechanism",
        "checks": {
            "cp_matches_scalar_sum": bool(
                torch.allclose(tensor[1, 2, 0], (models[1] * prompts[2] * raters[0]).sum())
            ),
            "ordinal_probability_simplex": bool(
                torch.allclose(p.sum(-1), torch.ones(6, device=device, dtype=torch.float64))
            ),
            "human_fit_freezes_shared_factors": models.grad is None and prompts.grad is None,
            "human_head_has_real_gradient": bool(human.grad.abs().sum() > 0),
            "multiple_comparison_interval_wider": bool(
                simultaneous[1] - simultaneous[0] > ordinary[1] - ordinary[0]
            ),
        },
        "metrics": {
            "human_calibration_nll": float(loss.detach()),
            "conditional_interval_width": float(ordinary[1] - ordinary[0]),
            "simultaneous_interval_width": float(simultaneous[1] - simultaneous[0]),
        },
    }
