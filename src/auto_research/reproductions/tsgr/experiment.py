from pathlib import Path

from ..industrial_2026 import (
    base_scores,
    evaluate,
    load_industrial_data,
    summary_result,
    tune_blend,
)
from .model import construct_qp_sid, train_vrm, tsgr_score


def reproduce_tsgr(dataset_dir: Path, seed: int = 42) -> dict:
    data = load_industrial_data(dataset_dir, maximum_users=420, maximum_items=620)
    semantic, prefixes, global_order, query_order = construct_qp_sid(data, seed)
    coefficients, training = train_vrm(data, prefixes, global_order, query_order, seed)
    baseline = evaluate(data, lambda history: base_scores(data, history))
    raw = lambda history: tsgr_score(
        data, prefixes, global_order, query_order, coefficients, history
    )
    alpha, scorer, validation = tune_blend(
        data, lambda history: base_scores(data, history), raw
    )
    method = evaluate(data, scorer)
    stages = {
        **training,
        "rq_semantic_levels": semantic.shape[1],
        "parallel_value_code": True,
        "query_conditioned_codebooks": query_order.shape[0],
        "joint_value_aware_ranking_module": True,
        "selected_validation_blend": alpha,
        "validation": validation,
    }
    return summary_result(
        key="tsgr",
        paper={
            "arxiv_id": "2607.18796",
            "title": "TSGR: Taobao Search Generative Retrieval",
            "url": "https://arxiv.org/abs/2607.18796",
            "organization": "Taobao & Tmall Group of Alibaba",
        },
        data=data,
        baseline_name="semantic retrieval + conventional pre-ranking proxy",
        method_name="QP-SID + jointly optimized value-aware ranking module",
        baseline=baseline,
        proposed=method,
        stages=stages,
        paper_results={
            "offline_hr_at_1000_percent": 9.16,
            "online_ipv_percent": 0.43,
            "online_transaction_count_percent": 1.12,
            "online_gmv_percent": 1.64,
            "traffic_percent": 1.0,
            "ab_duration_days": 38,
            "fully_deployed": True,
        },
        scope="实际构建两级 residual-quantized semantic prefix、prefix 内全局价值码和 query-domain 条件并行码本；以加权多正例/负例训练联合 VRM，融合 backbone user representation、item side-info 和价值分数，并只在 validation 选择融合强度。MovieLens genre/popularity/transition 替代淘宝 query-item 统计和商业标签；论文未采用的 RL 同样不进入本地部署路径。",
    )
