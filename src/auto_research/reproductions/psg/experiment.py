from pathlib import Path

from ..industrial_2026 import evaluate, load_industrial_data, summary_result
from .model import psg_diagnostics, score_item_space, score_pair_space


def reproduce_psg(dataset_dir: Path, seed: int = 42) -> dict:
    del seed
    data = load_industrial_data(dataset_dir)
    baseline = evaluate(data, lambda history: score_item_space(data, history))
    method = evaluate(data, lambda history: score_pair_space(data, history))
    return summary_result(
        key="psg",
        paper={
            "arxiv_id": "2607.26427",
            "title": "PSG: Pair-Space Generation for Efficient Generative Reranking",
            "url": "https://arxiv.org/abs/2607.26427",
            "organization": "Kuaishou Technology",
        },
        data=data,
        baseline_name="item-space autoregressive next-item scoring",
        method_name="ordered pair-token generation and unfolding",
        baseline=baseline,
        proposed=method,
        stages=psg_diagnostics(data, data.sequences.train[0]),
        paper_results={
            "stay_time_lift_percent": 0.178,
            "industrial_speedup": 1.83,
            "traffic_percent_per_bucket": 10,
            "experiment_days": 7,
        },
        scope=(
            "实际构造 request-specific n(n-1) 有序 pair space、pair token 打分、半长度解码与无重复展开；"
            "未复刻 Kuaishou GoalRank evaluator、曝光日志和线上 50-list beam serving。"
        ),
    )
