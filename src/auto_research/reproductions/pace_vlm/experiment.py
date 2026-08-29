from __future__ import annotations

from pathlib import Path

import numpy as np

from .model import apc_scores, dual_attention_saliency, target_resolution


def reproduce_pace_vlm(dataset_dir: Path, seed: int = 42):
    """Deterministic mechanism check; checkpoint evidence lives in checkpoint.py."""
    import torch

    generator = torch.Generator().manual_seed(seed)
    smooth = torch.ones(196, 32) + 0.02 * torch.randn(196, 32, generator=generator)
    detailed = torch.randn(196, 32, generator=generator)
    smooth_budget, _, _ = apc_scores(smooth)
    detailed_budget, density, detail = apc_scores(detailed)
    height, width, actual = target_resolution(
        672, 672, retention=detailed_budget, patch_size=28,
    )
    llm = torch.softmax(torch.randn(196, generator=generator), 0)
    vit = torch.softmax(torch.randn(196, generator=generator) * 1.8, 0)
    fused, weights = dual_attention_saliency(llm, vit)
    return {
        "paper": {"arxiv_id": "2608.27206", "title": "PACE"},
        "dataset": {"name": "deterministic visual-token mechanism mini-suite"},
        "setup": {"seed": seed, "tokens": 196, "dimensions": 32},
        "baseline": {"name": "fixed visual-token budget", "retention": 1.0},
        "method": {
            "name": "PACE APC + DDAE", "smooth_retention": smooth_budget,
            "detailed_retention": detailed_budget, "global_density": density,
            "local_detail": detail, "target_height": height, "target_width": width,
            "actual_retention": actual, "llm_weight": float(weights[0]),
            "vision_weight": float(weights[1]), "saliency_std": float(fused.std()),
        },
        "relative": {
            "token_reduction_percent": 100.0 * (1.0 - actual),
            "detail_vs_smooth_retention_points": 100.0 * (detailed_budget - smooth_budget),
        },
        "diagnostic_only": True,
        "scope": "公式级 APC/DDAE 验证；真实 Qwen2.5-VL 与 RealWorldQA 结果见 GPU receipt。",
    }


def render(result):
    return (
        f"# PACE\n\nAPC token reduction: "
        f"{result['relative']['token_reduction_percent']:.2f}%.\n"
    )
