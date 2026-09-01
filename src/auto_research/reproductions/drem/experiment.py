from pathlib import Path

from ..industrial_2026 import evaluate, load_industrial_data, summary_result
from .model import build_drem, robustness_diagnostics, score_drem, score_naive


def reproduce_drem(dataset_dir: Path, seed: int = 42) -> dict:
    data = load_industrial_data(dataset_dir)
    state = build_drem(data, seed)
    baseline = evaluate(data, lambda history: score_naive(data, history))
    method = evaluate(data, lambda history: score_drem(data, state, history))
    return summary_result(
        key="drem",
        paper={
            "arxiv_id": "2608.12778",
            "title": "DrEM: Dual-Side Robust Ensemble Ranking from Noisy User Preference Predictions in Video Recommendation",
            "url": "https://arxiv.org/abs/2608.12778",
            "organization": "Shenzhen University",
        },
        data=data,
        baseline_name="naive pxtr ensemble",
        method_name="dual-side risk correction + preference-preserving consistency",
        baseline=baseline,
        proposed=method,
        stages=robustness_diagnostics(data, state, data.sequences.train[0]),
        paper_results={
            "traffic_percent_per_group": 5.1,
            "experiment_days": 7,
            "emer_comment_lift_percent": 1.388,
            "emer_follow_lift_percent": 1.197,
            "all_p_values_below": 0.005,
        },
        scope=(
            "实际执行 logit-space pxtr 扰动、偏好保持筛选、pair-label flip 风险反演和一致性融合；"
            "公开数据以转移、内容和热度三路代理 pxtr，未复刻生产 EMER/EASQ 与私有短视频日志。"
        ),
    )
