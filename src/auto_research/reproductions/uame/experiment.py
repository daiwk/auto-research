from __future__ import annotations

from pathlib import Path

from ..industrial_2026 import evaluate, gain, load_industrial_data
from ..llm_training import require_torch
from .model import scorer, train_ranker


def reproduce_uame(dataset_dir: Path, seed: int = 42) -> dict:
    torch = require_torch(); data = load_industrial_data(dataset_dir)
    base_model, base_training = train_ranker(data, False, seed, torch)
    method_model, method_training = train_ranker(data, True, seed, torch)
    baseline = evaluate(data, lambda history: scorer(base_model, data, history, torch))
    method = evaluate(data, lambda history: scorer(method_model, data, history, torch))
    return {
        "paper": {"arxiv_id": "2607.17092", "title": "Uncertainty as Remedy: Mitigating Satisfaction Label Bias in Short Video Multi-Objective Ensemble Ranking", "url": "https://arxiv.org/abs/2607.17092", "organization": "Kuaishou"},
        "dataset": {"name": "MovieLens 100K", "users": len(data.sequences.train), "items": data.item_count},
        "setup": {"seed": seed, "same_pairs_features_and_backbone": True, "proxy_objectives": ["transition", "content similarity", "popularity"]},
        "baseline": {"name": "deterministic multi-objective pairwise ranker", **baseline},
        "method": {"name": "UAME", **method}, "relative": gain(method, baseline),
        "training": {"baseline": base_training, "uame": method_training},
        "stages": {"gaussian_score": True, "probabilistic_pairwise_cdf": True, "uncertainty_regularization_alpha": 0.02, "conflict_auxiliary_beta": 0.1, "adaptive_weight_gamma": 2.0, "mean_only_serving": True},
        "paper_results": {"vs_EMER_LongView_percent": 1.614, "vs_EASQ_LongView_percent": 1.126, "vs_EMER_Forward_percent": 1.325, "vs_EASQ_Forward_percent": 1.598},
        "scope": "实际用共享 backbone 的 mean/variance 双头、Gaussian CDF pair probability、三路 proxy 联合 PPR、方差正则、冲突辅助约束和 uncertainty min-max weighting 训练；推理只读 mean，零额外排序路径。MovieLens proxy 替代快手八路 pxtr、EMER/EASQ 与问卷满意度。",
    }
