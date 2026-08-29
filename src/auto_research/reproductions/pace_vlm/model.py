"""Training-free PACE operators from arXiv:2608.27206.

The real checkpoint path uses the authors' Qwen2.5-VL integration.  These
small functions keep the paper-defining APC and DDAE equations independently
testable and available to Evolve without copying the upstream 2,000-line model
fork into this repository.
"""

from __future__ import annotations

import math


def apc_scores(
    features,
    *,
    global_weight: float = 0.6,
    detail_fraction: float = 0.1,
    detail_scale: float = 1.5,
    minimum_retention: float = 0.05,
):
    """Return ``(retention, global_density, local_detail)`` for ViT tokens."""
    import torch

    if features.ndim != 2 or len(features) == 0:
        raise ValueError("features must have shape [tokens, dimensions]")
    if not 0 <= global_weight <= 1:
        raise ValueError("global_weight must be in [0, 1]")
    if not 0 < detail_fraction <= 1 or detail_scale <= 0:
        raise ValueError("detail_fraction and detail_scale must be positive")
    normalized = torch.nn.functional.normalize(
        torch.nan_to_num(features.float()), dim=-1, eps=1e-12
    )
    count = len(normalized)
    if count == 1:
        return minimum_retention, 0.0, 0.0
    feature_sum = normalized.sum(0)
    off_diagonal = (
        torch.dot(feature_sum, feature_sum) - normalized.square().sum()
    ) / (count * (count - 1))
    global_density = (1 - off_diagonal).clamp(0, 1)
    background = torch.nn.functional.normalize(
        (feature_sum / count).unsqueeze(0), dim=-1, eps=1e-12
    )
    distances = torch.linalg.vector_norm(normalized - background, dim=-1)
    detail_count = min(count, max(1, math.ceil(count * detail_fraction)))
    local_detail = (distances.topk(detail_count).values.mean() / detail_scale).clamp(0, 1)
    retention = (
        global_weight * global_density + (1 - global_weight) * local_detail
    ).clamp(minimum_retention, 1)
    return float(retention), float(global_density), float(local_detail)


def target_resolution(
    height: int,
    width: int,
    *,
    retention: float,
    patch_size: int = 28,
) -> tuple[int, int, float]:
    """Choose a patch-aligned resolution closest to the APC token budget."""
    if height < 1 or width < 1 or patch_size < 1 or not 0 < retention <= 1:
        raise ValueError("invalid image shape, patch size, or retention")
    old_h = math.ceil(height / patch_size)
    old_w = math.ceil(width / patch_size)
    target = max(1, round(old_h * old_w * retention))
    aspect = height / width
    ideal_w = math.sqrt(target / aspect)
    ideal_h = ideal_w * aspect
    candidates = (
        (max(1, math.floor(ideal_h)), max(1, math.floor(ideal_w))),
        (max(1, math.floor(ideal_h)), max(1, math.ceil(ideal_w))),
        (max(1, math.ceil(ideal_h)), max(1, math.floor(ideal_w))),
        (max(1, math.ceil(ideal_h)), max(1, math.ceil(ideal_w))),
    )
    new_h, new_w = min(
        candidates,
        key=lambda shape: (
            abs(shape[0] * shape[1] - target),
            abs(shape[0] / shape[1] - aspect),
        ),
    )
    actual = new_h * new_w / (old_h * old_w)
    return new_h * patch_size, new_w * patch_size, actual


def dual_attention_saliency(
    llm_attention,
    vision_attention,
    *,
    temperature: float = 0.5,
):
    """Fuse normalized LLM/Vision maps with DDAE confidence weights."""
    import torch

    if llm_attention.shape != vision_attention.shape or llm_attention.ndim != 1:
        raise ValueError("attention maps must be one-dimensional with equal shape")
    if temperature <= 0:
        raise ValueError("temperature must be positive")

    def normalize(values):
        values = values.float()
        span = values.max() - values.min()
        return (values - values.min()) / span.clamp_min(1e-12)

    llm = normalize(llm_attention)
    vision = normalize(vision_attention)
    weights = torch.softmax(
        torch.stack((llm.std(unbiased=False), vision.std(unbiased=False))) / temperature,
        dim=0,
    )
    return weights[0] * llm + weights[1] * vision, weights
