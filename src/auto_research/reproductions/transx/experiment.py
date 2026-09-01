from pathlib import Path

from ..industrial_2026 import evaluate, load_industrial_data, summary_result
from .model import score_monolithic, score_transx, transx_diagnostics


def reproduce_transx(dataset_dir: Path, seed: int = 42) -> dict:
    del seed
    data = load_industrial_data(dataset_dir)
    baseline = evaluate(data, lambda history: score_monolithic(data, history))
    method = evaluate(data, lambda history: score_transx(data, history))
    return summary_result(
        key="transx",
        paper={
            "arxiv_id": "2607.28940",
            "title": "TransX: Scaling Transformer-based Recommendation via Behavioral and Serving Stream Crossings",
            "url": "https://arxiv.org/abs/2607.28940",
            "organization": "LinkedIn",
        },
        data=data,
        baseline_name="monolithic recent-sequence scorer",
        method_name="cached behavior encoder + serving-stream cross attention",
        baseline=baseline,
        proposed=method,
        stages=transx_diagnostics(data, data.sequences.train[0]),
        paper_results={
            "ctr_lift_percent": 6.0,
            "conversion_lift_percent": 4.4,
            "online_compute_reduction_percent": 80,
        },
        scope=(
            "实际拆分 nearline 行为流和实时 serving 流，构造 global-local cache 并执行 candidate-to-cache"
            " cross attention；未复刻 LinkedIn Kafka、KV 服务、TTL/version 管理和生产候选特征。"
        ),
    )
