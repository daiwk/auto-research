from pathlib import Path

from ..industrial_2026 import evaluate, load_industrial_data, summary_result
from .model import build_snaplgr, score_baseline_sid, score_snaplgr, snaplgr_diagnostics


def reproduce_snaplgr(dataset_dir: Path, seed: int = 42) -> dict:
    data = load_industrial_data(dataset_dir)
    state = build_snaplgr(data, seed)
    baseline = evaluate(data, lambda history: score_baseline_sid(data, state, history))
    method = evaluate(data, lambda history: score_snaplgr(data, state, history))
    return summary_result(
        key="snaplgr",
        paper={
            "arxiv_id": "2607.28895",
            "title": "LLM-Based Generative Retrieval for Snapchat Content Recommendation",
            "url": "https://arxiv.org/abs/2607.28895",
            "organization": "Snap Inc.",
        },
        data=data,
        baseline_name="vanilla RQ semantic IDs",
        method_name="PPR co-engagement SID + token grounding + SID transition SFT",
        baseline=baseline,
        proposed=method,
        stages=snaplgr_diagnostics(state),
        paper_results={
            "view_time_lift_percent": 0.37,
            "time_spent_lift_percent": 0.09,
            "deep_sessions_lift_percent": 0.18,
            "experiment_days": 7,
            "serving_throughput_multiplier": 45.7,
        },
        scope=(
            "实际执行 co-engagement 图传播、残差量化 SID、code token 语义 grounding 和 code-level"
            " next-token transition；未加载预训练 LLM/Qwen3-VL，也未复刻 TensorRT-LLM 与 64×A100 服务。"
        ),
    )
