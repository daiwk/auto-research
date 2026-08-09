from pathlib import Path

from ..industrial_2026 import base_scores, evaluate, load_industrial_data, summary_result, tune_blend
from .model import score_ultra_hstu


def reproduce_ultra_hstu(dataset_dir: Path, seed: int = 42) -> dict:
    data = load_industrial_data(dataset_dir)
    method_only = lambda h: score_ultra_hstu(data, h)[0]
    baseline = evaluate(data, lambda h: base_scores(data, h))
    alpha, scorer, validation = tune_blend(data, lambda h: base_scores(data, h), method_only)
    method = evaluate(data, scorer)
    _, trace = score_ultra_hstu(data, data.sequences.train[0])
    return summary_result(key="ultra-hstu", paper={"arxiv_id": "2602.16986", "title": "Bending the Scaling Law Curve in Large-Scale Recommendation Systems", "url": "https://arxiv.org/abs/2602.16986", "organization": "Meta"}, data=data, baseline_name="short-history transition-content ranker", method_name="ULTRA-HSTU compact core", baseline=baseline, proposed=method, stages={"semi_local_layers": 6, "local_window": 8, "lbsl": True, "mixture_of_transducers": trace, "selected_blend": alpha, "validation": validation}, paper_results={"consumption_percent": 4.11, "engagement_percent_range": [2, 8], "training_scaling_x": 5, "inference_scaling_x": 21}, scope="实际执行半局部 attention、逐层扩大的 LBSL 感受野和 Mixture of Transducers；48-event 公共序列替代 16k 历史，未复刻 18 层生产规模、动态 topology 与定制 kernel。")
