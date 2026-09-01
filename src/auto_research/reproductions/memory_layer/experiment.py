from pathlib import Path

from ..industrial_2026 import evaluate, load_industrial_data, summary_result
from .model import (
    build_memory_layer,
    memory_diagnostics,
    score_external_snapshot,
    score_memory_layer,
)


def reproduce_memory_layer(dataset_dir: Path, seed: int = 42) -> dict:
    del seed  # The eta=1 writeback path is intentionally deterministic.
    data = load_industrial_data(dataset_dir)
    state = build_memory_layer(data)
    baseline = evaluate(data, lambda history: score_external_snapshot(data, state, history))
    method = evaluate(data, lambda history: score_memory_layer(data, state, history))
    return summary_result(
        key="memory-layer",
        paper={
            "arxiv_id": "2607.25110",
            "title": "Memory Layer: Train the In-Model Cache for Recommendation Models",
            "url": "https://arxiv.org/abs/2607.25110",
            "organization": "Meta",
        },
        data=data,
        baseline_name="external frozen item cache",
        method_name="co-trained writeback memory + always-on embedding",
        baseline=baseline,
        proposed=method,
        stages=memory_diagnostics(state),
        paper_results={
            "coverage_before_percent": 96,
            "coverage_after_percent": 100,
            "freshness_before_seconds": 300,
            "freshness_after_seconds": 20,
            "training_serving_ne_gap_reduction_percent": 86,
            "cold_start_engagement_lift_percent": [5, 6],
            "training_publish_cost_reduction_percent": 30,
        },
        scope=(
            "实际执行训练内 eta=1 cache writeback、冻结外部快照对照、cache miss 与 "
            "always-on 属性表征；未复刻 MPZCH/FBGEMM 分布式存储、15 秒流式发布和 Instagram 私有日志。"
        ),
    )
