from pathlib import Path

from ..industrial_2026 import base_scores, evaluate, load_industrial_data, summary_result, tune_blend
from .model import build_mfli, score_mfli


def reproduce_mfli(dataset_dir: Path, seed: int = 42) -> dict:
    data = load_industrial_data(dataset_dir)
    state = build_mfli(data)
    baseline = evaluate(data, lambda h: base_scores(data, h))
    alpha, scorer, validation = tune_blend(data, lambda h: base_scores(data, h), lambda h: score_mfli(data, state, h))
    method = evaluate(data, scorer)
    return summary_result(key="mfli", paper={"arxiv_id": "2602.16124", "title": "Rethinking ANN-based Retrieval: Multifaceted Learnable Index for Large-scale Recommendation System", "url": "https://arxiv.org/abs/2602.16124", "organization": "Meta"}, data=data, baseline_name="single-space ANN proxy", method_name="MFLI", baseline=baseline, proposed=method, stages={"facets": ["genre", "semantic-coarse", "semantic-fine", "freshness"], "learned_facet_transitions": 4, "selected_blend": alpha, "validation": validation}, paper_results={"low_vv_exposure_percent": 279, "ultra_fresh_exposure_percent": 221, "diversity_percent": 0.30, "qps_percent": 60}, scope="实际构建四个可学习 facet 索引、分层语义 code、facet 转移与 query-dependent allocation；全目录评分用于公平评测，未冒充 Meta 分布式实时索引。")
