from pathlib import Path

from ..industrial_2026 import base_scores, evaluate, load_industrial_data, summary_result, tune_blend
from .model import score_growthgr, train_growthgr


def reproduce_growthgr(dataset_dir: Path, seed: int = 42) -> dict:
    data = load_industrial_data(dataset_dir)
    _, uplift, policy, stages = train_growthgr(data, seed)
    baseline = evaluate(data, lambda h: base_scores(data, h))
    alpha, scorer, validation = tune_blend(data, lambda h: base_scores(data, h), lambda h: score_growthgr(data, uplift, policy, h))
    stages.update({"selected_blend": alpha, "validation": validation})
    method = evaluate(data, scorer)
    return summary_result(key="growthgr", paper={"arxiv_id": "2605.17994", "title": "Towards Sustainable Growth: A Multi-Value-Aware Retrieval Framework for E-Commerce Search", "url": "https://arxiv.org/abs/2605.17994", "organization": "Alibaba Group / Taobao & Tmall"}, data=data, baseline_name="NTP-retrieval", method_name="GrowthGR", baseline=baseline, proposed=method, stages=stages, paper_results={"new-item GMV": 5.3, "overall search GMV": 0.3}, scope="实际训练 ItemLTV base/uplift 两塔、三层 residual SID、NTP transition policy，并执行带 clipped inverse propensity、group advantage、PPO clip 的 MoPO 更新和有效 SID 约束。MovieLens 未来正反馈频次代理 7 日订单。")
