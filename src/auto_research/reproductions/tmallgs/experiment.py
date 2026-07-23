from pathlib import Path

from ..july_2026_common import (
    JulyRankingConfig,
    build_late_fusion_baseline,
    evaluate_catalog,
    ranking_data,
    standard_result,
    train_catalog_model,
)
from .model import build_tmallgs, progressive_loss


def reproduce_tmallgs(dataset_dir: Path, seed: int = 42) -> dict:
    data = ranking_data(dataset_dir)
    config = JulyRankingConfig.from_env("TMALLGS")
    baseline_model, baseline_training = train_catalog_model(
        build_late_fusion_baseline(data, config), data, config, seed
    )
    method_model, method_training = train_catalog_model(
        build_tmallgs(data, config), data, config, seed, loss_builder=progressive_loss
    )
    baseline = evaluate_catalog(baseline_model, data, config)
    method = evaluate_catalog(method_model, data, config)
    return standard_result(
        key="tmallgs",
        title="TMallGS: Scaling Unified Feature and Sequence Modeling for Generative E-commerce Search",
        organization="Taobao & Tmall Group of Alibaba",
        data=data,
        config=config,
        seed=seed,
        baseline_name="DIN/RankMixer-style late fusion Transformer",
        method_name="TMallGS field-adaptive gated Transformer",
        baseline=baseline,
        method=method,
        training={"late_fusion": baseline_training, "tmallgs": method_training},
        stages={
            "distribution_calibrated_saliency": True,
            "per_field_qkv": True,
            "noise_adaptive_gate": True,
            "film_late_fusion": True,
            "context_bias_net": True,
            "error_aware_progressive_loss": True,
        },
        paper_results={
            "pv_auc_percent": 0.79,
            "imp_gauc_percent": 0.34,
            "uctcvr_percent": 1.38,
            "gmv_percent": 1.52,
            "latency_ms": 6,
            "ab_duration_days": 30,
        },
        scope="实际训练 field-wise Q/K/V、噪声自适应门控、显式内容 FiLM late fusion、context-aware bias 与按中间层误差动态加权的 progressive loss；同切分 late-fusion Transformer 为基线。MovieLens 类型和序列字段替代天猫 query/UIH/UQH/重交叉特征。",
    )
