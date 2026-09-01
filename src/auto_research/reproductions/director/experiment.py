from pathlib import Path

from ..industrial_2026 import evaluate, load_industrial_data, summary_result
from .model import director_diagnostics, score_director, score_independent_indices


def reproduce_director(dataset_dir: Path, seed: int = 42) -> dict:
    del seed
    data = load_industrial_data(dataset_dir)
    baseline = evaluate(data, lambda history: score_independent_indices(data, history))
    method = evaluate(data, lambda history: score_director(data, history))
    return summary_result(
        key="director",
        paper={
            "arxiv_id": "2607.26418",
            "title": "DIRECTOR: Dynamic Index-based Recommendation with Transport-Optimized Retrieval",
            "url": "https://arxiv.org/abs/2607.26418",
            "organization": "University of Science and Technology of China",
        },
        data=data,
        baseline_name="independent position-wise dynamic indices",
        method_name="Sinkhorn coordinated indices + duplicate-free global matching",
        baseline=baseline,
        proposed=method,
        stages=director_diagnostics(data, data.sequences.train[0]),
        paper_results={
            "valid_view_lift_percent": 0.519,
            "comment_lift_percent": 0.695,
            "like_lift_percent": 0.330,
            "cpu_reduction_percent": 66.7,
            "service_availability_percent": 99,
        },
        scope=(
            "实际执行 request-conditioned 连续索引、熵正则 Sinkhorn capacity coupling、并行 position"
            " logits 和无重复 hard matching；未复刻论文 CVAE/DIFF generator、私有 evaluator 与 20K QPS 服务。"
        ),
    )
