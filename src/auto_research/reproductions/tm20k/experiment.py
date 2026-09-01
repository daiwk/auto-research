from pathlib import Path

from ..industrial_2026 import evaluate, load_industrial_data, summary_result
from .model import score_merged_student, score_tm20k, tm20k_diagnostics


def reproduce_tm20k(dataset_dir: Path, seed: int = 42) -> dict:
    del seed
    data = load_industrial_data(dataset_dir)
    baseline = evaluate(data, lambda history: score_merged_student(data, history))
    method = evaluate(data, lambda history: score_tm20k(data, history))
    return summary_result(
        key="tm20k",
        paper={
            "arxiv_id": "2608.07055",
            "title": "Teacher Retains Full Tokens, Student Merges Efficiently: TM20K for E-Commerce Sequence Modeling in Ad Recommendation",
            "url": "https://arxiv.org/abs/2608.07055",
            "organization": "ByteDance",
        },
        data=data,
        baseline_name="merged-token full-attention student without KD",
        method_name="sum-merge student distilled from full-token teacher",
        baseline=baseline,
        proposed=method,
        stages=tm20k_diagnostics(data, data.sequences.train[0]),
        paper_results={
            "sequence_length": 20000,
            "adss_lift_percent": 1.036,
            "advv_lift_percent": 0.780,
            "serving_latency_increase_percent": 5.6,
            "experiment_days": 5,
        },
        scope=(
            "实际执行全 token teacher、连续分组 sum/sqrt(n) token merge、全注意力 student 和"
            "teacher-logit 蒸馏；公开序列远短于 20K，未复刻 M-Falcon、广告私有特征或线上 GPU 集群。"
        ),
    )
