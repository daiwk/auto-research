from pathlib import Path

from ..industrial_2026 import base_scores, evaluate, load_industrial_data, summary_result, tune_blend
from .model import score_sam, train_sam


def reproduce_sam(dataset_dir: Path, seed: int = 42) -> dict:
    data = load_industrial_data(dataset_dir)
    cycles, stages = train_sam(data)
    baseline = evaluate(data, lambda h: base_scores(data, h))
    alpha, scorer, validation = tune_blend(data, lambda h: base_scores(data, h), lambda h: score_sam(data, cycles, h))
    stages.update({"selected_blend": alpha, "validation": validation})
    method = evaluate(data, scorer)
    return summary_result(key="sam", paper={"arxiv_id": "2607.12714", "title": "Learning to Forget: Satiation-Aware Long-Sequence Transducers for Mitigating Post-Purchase Redundancy", "url": "https://arxiv.org/abs/2607.12714", "organization": "Alibaba Group"}, data=data, baseline_name="DIN-like-interest", method_name="SAM", baseline=baseline, proposed=method, stages=stages, paper_results={"CTR": 1.1, "GMV": 0.9, "bad-case reduction": 74.5}, scope="实际估计 category replenishment cycle、执行 pointwise intent localization、ASGU recovery mask 与 log-mask attention intervention；MovieLens 高分 genre 重复间隔代理购买与复购节奏。")
