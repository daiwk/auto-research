from pathlib import Path

from ..industrial_2026 import base_scores, evaluate, load_industrial_data, summary_result, tune_blend
from .model import score_mbgr, train_mbgr


def reproduce_mbgr(dataset_dir: Path, seed: int = 42) -> dict:
    data = load_industrial_data(dataset_dir)
    codes, routed, distribution, stages = train_mbgr(data, seed)
    baseline = evaluate(data, lambda h: base_scores(data, h))
    alpha, scorer, validation = tune_blend(data, lambda h: base_scores(data, h), lambda h: score_mbgr(data, routed, distribution, codes, h))
    stages.update({"selected_blend": alpha, "validation": validation})
    method = evaluate(data, scorer)
    return summary_result(key="mbgr", paper={"arxiv_id": "2604.02684", "title": "MBGR: Multi-Business Generative Recommendation", "url": "https://arxiv.org/abs/2604.02684", "organization": "Meituan"}, data=data, baseline_name="shared-next-item", method_name="MBGR", baseline=baseline, proposed=method, stages=stages, paper_results={"CTCVR": 3.98}, scope="实际执行 business-aware residual SID、共享的 domain-conditioned reconstruction/prediction table、multi-business experts 聚合，以及为每个业务寻找最近未来交互的 LDR；MovieLens genre 作为公开业务域代理。")
