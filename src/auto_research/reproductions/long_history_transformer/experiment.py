from pathlib import Path

from ..july_2026_common import (
    JulyRankingConfig,
    build_late_fusion_baseline,
    evaluate_catalog,
    ranking_data,
    standard_result,
    train_catalog_model,
)
from .model import build_long_history_model, dual_objective_loss


def reproduce_long_history_transformer(dataset_dir: Path, seed: int = 42) -> dict:
    data = ranking_data(dataset_dir)
    config = JulyRankingConfig.from_env("LONG_HISTORY", sequence_length=24)
    baseline_model, baseline_training = train_catalog_model(
        build_late_fusion_baseline(data, config, history_limit=4), data, config, seed
    )
    method_model, method_training = train_catalog_model(
        build_long_history_model(data, config), data, config, seed,
        loss_builder=dual_objective_loss,
    )
    baseline = evaluate_catalog(baseline_model, data, config)
    method = evaluate_catalog(method_model, data, config)
    return standard_result(
        key="long-history-transformer",
        title="Long-History User Transformers for Real-Time Ad Ranking",
        organization="Yandex",
        data=data,
        config=config,
        seed=seed,
        baseline_name="request-time recent-history Transformer (4 events)",
        method_name="cached full-history encoder + lightweight runtime Transformer",
        baseline=baseline,
        method=method,
        training={"recent_runtime": baseline_training, "split_long_history": method_training},
        stages={
            "asynchronous_offline_encoder": True,
            "compact_cached_representation_dimensions": config.dimensions,
            "runtime_recent_events": 4,
            "autoregressive_next_item_pretraining": True,
            "feedback_prediction_pretraining": True,
            "target_surface_finetuning": True,
        },
        paper_results={
            "search_primary_percent": 2.77,
            "search_clicks_percent": 2.87,
            "search_revenue_percent": 2.26,
            "yan_primary_percent": 2.10,
            "yan_clicks_percent": 2.59,
            "yan_revenue_percent": 0.43,
            "serving_latency_change_ms": 0,
        },
        scope="实际训练异步长历史 Transformer、固定维度缓存状态、近期事件 runtime Transformer，以及 feedback/next-item 双预训练目标后联合 CTR 式排序微调；本地近期历史模型为直接对照。MovieLens 跨类型行为替代 Yandex 多广告 surface 日志，未复刻 CatBoost 和线上 feature store。",
    )
