from pathlib import Path

from ..industrial_2026 import evaluate, load_industrial_data, summary_result, tune_blend
from .model import build_ha_moe, score_baseline, score_ha_moe


def reproduce_ha_moe(dataset_dir: Path, seed: int = 42) -> dict:
    data = load_industrial_data(dataset_dir)
    state = build_ha_moe(data)
    baseline = evaluate(data, lambda h: score_baseline(data, h))
    alpha, scorer, validation = tune_blend(data, lambda h: score_baseline(data, h), lambda h: score_ha_moe(data, state, h))
    method = evaluate(data, scorer)
    return summary_result(key="ha-moe", paper={"arxiv_id": "2607.27577", "title": "Heterogeneous Ranking in Industrial-Scale Recommender Systems: A Case Study", "url": "https://arxiv.org/abs/2607.27577", "organization": "Google / Discover"}, data=data, baseline_name="homogeneous transition-content ranker", method_name="HA-MoE", baseline=baseline, proposed=method, stages={"experts": ["domain", "transition", "content", "freshness"], "heterogeneity_gate": True, "selected_blend": alpha, "validation": validation}, paper_results={"DAU_percent": 0.22, "viewed_impressions_percent": 0.48, "diverse_engagement_rate_percent": 0.54}, scope="实际执行按 session 领域熵计算的异构门控、四个专长 expert 与验证集选强度；MovieLens genre 代理 Discover 内容异构性，未复刻 Google 私有 LENS/DL-AUC 管线。")
