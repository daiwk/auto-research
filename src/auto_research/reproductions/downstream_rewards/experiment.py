from pathlib import Path

from ..industrial_2026 import base_scores, evaluate, load_industrial_data, summary_result, tune_blend
from .model import learn_downstream_rewards, score_with_rewards


def reproduce_downstream_rewards(dataset_dir: Path, seed: int = 42) -> dict:
    data = load_industrial_data(dataset_dir, maximum_users=420, maximum_items=620)
    coefficients, stages = learn_downstream_rewards(data)
    baseline = evaluate(data, lambda history: base_scores(data, history))
    raw = lambda history: score_with_rewards(data, coefficients, history)
    alpha, scorer, validation = tune_blend(
        data, lambda history: base_scores(data, history), raw
    )
    stages.update({
        "reward_coefficients": coefficients.tolist(),
        "selected_validation_blend": alpha,
        "validation": validation,
        "cross_surface_shared_definition": True,
    })
    method = evaluate(data, scorer)
    return summary_result(
        key="downstream-rewards",
        paper={
            "arxiv_id": "2607.14192",
            "title": "Long-term User Engagement Optimization through Model-agnostic Downstream Rewards Learning",
            "url": "https://arxiv.org/abs/2607.14192",
            "organization": "Pinterest",
        },
        data=data,
        baseline_name="immediate next-item engagement ranker",
        method_name="immediate engagement + screened downstream reward heads",
        baseline=baseline,
        proposed=method,
        stages=stages,
        paper_results={
            "homefeed_successful_sessions_percent": 0.36,
            "homefeed_total_time_percent": 0.35,
            "search_fulfillment_percent": 0.25,
            "related_pins_successful_sessions_percent": 0.15,
            "notifications_successful_sessions_percent": 0.14,
            "notifications_wau_percent": 0.11,
        },
        scope="实际从多个 session-level 候选信号出发，用未来行为域覆盖代理 retention 做离线相关性筛选，训练可插拔 reward heads，并与即时排序目标联合打分；validation 独立选择权重。MovieLens 连续行为/类型多样性替代 Pinterest P2P、save、download 与跨 surface 日志。",
    )
