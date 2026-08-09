from pathlib import Path

from ..industrial_2026 import base_scores, evaluate, load_industrial_data, summary_result, tune_blend
from .model import score_kunlun


def reproduce_kunlun(dataset_dir: Path, seed: int = 42) -> dict:
    data = load_industrial_data(dataset_dir)
    method_only = lambda h: score_kunlun(data, h)[0]
    baseline = evaluate(data, lambda h: base_scores(data, h))
    alpha, scorer, validation = tune_blend(data, lambda h: base_scores(data, h), method_only)
    method = evaluate(data, scorer)
    _, trace = score_kunlun(data, data.sequences.train[0])
    return summary_result(key="kunlun", paper={"arxiv_id": "2602.10016", "title": "Kunlun: Establishing Scaling Laws for Massive-Scale Recommendation Systems through Unified Architecture Design", "url": "https://arxiv.org/abs/2602.10016", "organization": "Meta"}, data=data, baseline_name="shallow transition-content ranker", method_name="Kunlun compact core", baseline=baseline, proposed=method, stages={"gdpa_layers": 4, "hierarchical_seed_widths": [2, 4, 8], "compskip": True, "moe_routes_example": trace, "selected_blend": alpha, "validation": validation}, paper_results={"topline_percent": 1.2, "mfu_before_percent": 17, "mfu_after_percent": 37, "scaling_efficiency_x": 2}, scope="实际执行 GDPA、2/4/8 层级 seed pooling、三 expert routing 与 CompSkip；小型 NumPy 前向验证结构，不复刻 Meta Ads 万亿参数、expert parallel 和硬件 MFU。")
