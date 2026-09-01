from pathlib import Path

from ..industrial_2026 import evaluate, load_industrial_data, summary_result
from .model import rgd_diagnostics, score_generator, score_reward_guided


def reproduce_reward_guided_decoding(dataset_dir: Path, seed: int = 42) -> dict:
    del seed
    data = load_industrial_data(dataset_dir)
    baseline = evaluate(data, lambda history: score_generator(data, history))
    method = evaluate(data, lambda history: score_reward_guided(data, history))
    return summary_result(
        key="reward-guided-decoding",
        paper={
            "arxiv_id": "2607.25344",
            "title": "Reward Guided Decoding for Generative Recommendation",
            "url": "https://arxiv.org/abs/2607.25344",
            "organization": "Institute of Information Engineering, Chinese Academy of Sciences",
        },
        data=data,
        baseline_name="generator likelihood decoding",
        method_name="closed-form KL-regularized reward-guided decoding",
        baseline=baseline,
        proposed=method,
        stages=rgd_diagnostics(data, data.sequences.train[0]),
        paper_results={
            "page_ctr_lift_percent": 0.392,
            "watch_time_lift_percent": 0.689,
            "watch_count_lift_percent": 0.349,
            "experiment_weeks": 2,
        },
        scope=(
            "实际执行 Q*(j) ∝ P(j) exp(R(j)/beta) 的闭式重加权、KL 距离和 reward 控制；"
            "公开 reward 使用内容相关性与新颖度代理，未复刻 Kuaishou SID generator、共享 decoder reward model 和线上 beam search。"
        ),
    )
