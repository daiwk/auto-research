from pathlib import Path

from ..july_2026_common import (
    JulyRankingConfig,
    evaluate_catalog,
    ranking_data,
    standard_result,
    train_catalog_model,
)
from .model import build_privacy_ranker, ramp_loss


def reproduce_ramp(dataset_dir: Path, seed: int = 42) -> dict:
    data = ranking_data(dataset_dir)
    config = JulyRankingConfig.from_env("RAMP")
    baseline_model, baseline_training = train_catalog_model(
        build_privacy_ranker(data, config, ramp=False), data, config, seed
    )
    method_model, method_training = train_catalog_model(
        build_privacy_ranker(data, config, ramp=True), data, config, seed,
        loss_builder=ramp_loss,
    )
    baseline = evaluate_catalog(baseline_model, data, config, mode="non_personalized")
    method = evaluate_catalog(method_model, data, config, mode="non_personalized")
    personalized = evaluate_catalog(method_model, data, config, mode="personalized")
    return standard_result(
        key="ramp",
        title="RAMP: Robust Ad Recommendation Under Limited Personalized-Feature Availability via Masking and Alignment Pathways",
        organization="Huawei Ireland Research Center / University College Dublin",
        data=data,
        config=config,
        seed=seed,
        baseline_name="shared CTR tower with missing personalized features",
        method_name="RAMP masked dual tower + alignment pathway",
        baseline=baseline,
        method=method,
        training={"shared_tower": baseline_training, "ramp": method_training},
        stages={
            "personalized_pathway": True,
            "feature_availability_output_mask": True,
            "nonpersonalized_pathway": True,
            "distillation_prediction_alignment": True,
            "nonpersonalized_traffic_share": 0.20,
            "personalized_test_metrics": personalized,
        },
        paper_results={
            "industrial_total_advertiser_value_percent": 3.0,
            "public_auc_gain_range_percent": [0.10, 0.87],
            "significance": "p<0.001 offline",
        },
        scope="实际训练 consent-aware personalized/non-personalized 双塔、输出 masking、仅公共字段的独立 pathway，以及由富特征 teacher 到受限路径的 prediction-alignment KL；本地结果专门在无个性化字段流量上比较。MovieLens 行为向量/类型字段分别代理受限个性化和公共广告特征。",
    )
