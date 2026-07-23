from pathlib import Path

from ..july_2026_common import (
    JulyRankingConfig,
    build_late_fusion_baseline,
    evaluate_catalog,
    ranking_data,
    standard_result,
    train_catalog_model,
)
from .model import build_whale


def reproduce_whale(dataset_dir: Path, seed: int = 42) -> dict:
    data = ranking_data(dataset_dir)
    config = JulyRankingConfig.from_env("WHALE")
    baseline_model, baseline_training = train_catalog_model(
        build_late_fusion_baseline(data, config), data, config, seed
    )
    method_model, method_training = train_catalog_model(build_whale(data, config), data, config, seed)
    baseline = evaluate_catalog(baseline_model, data, config)
    method = evaluate_catalog(method_model, data, config)
    return standard_result(
        key="whale",
        title="WHALE: A Scalable Unified Model for Recommendation with Wukong-HSTU Architecture",
        organization="Meta",
        data=data,
        config=config,
        seed=seed,
        baseline_name="separate Transformer branches with late fusion",
        method_name="WHALE progressive Wukong-HSTU exchange",
        baseline=baseline,
        method=method,
        training={"late_fusion": baseline_training, "whale": method_training},
        stages={
            "recursive_wukong_blocks": config.layers,
            "recursive_hstu_blocks": config.layers,
            "attention_cross_branch_exchange": True,
            "gated_hstu_updates": True,
        },
        paper_results={
            "primary_metric_percent": 0.113,
            "metric_1_percent": 0.824,
            "metric_2_percent": 1.820,
            "inference_qps_percent": -5.0,
            "ab_duration_days": 14,
        },
        scope="实际训练逐层 Wukong 乘性交叉、HSTU 式门控因果注意力及由特征交互分支查询行为序列的 cross-attention；同容量 late-fusion Transformer 为本地基线。MovieLens 类型特征替代 Meta 私有稀疏特征，未复刻生产 Triton/AOTInductor 内核。",
    )
