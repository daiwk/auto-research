from pathlib import Path

from ..industrial_2026 import base_scores, evaluate, load_industrial_data, summary_result, tune_blend
from .model import score_grc, train_grc


def reproduce_grc(dataset_dir: Path, seed: int = 42) -> dict:
    data = load_industrial_data(dataset_dir)
    codes, location, semantic, corrected, stages = train_grc(data, seed)
    baseline = evaluate(data, lambda h: base_scores(data, h))
    alpha, scorer, validation = tune_blend(data, lambda h: base_scores(data, h), lambda h: score_grc(data, codes, location, semantic, corrected, h))
    stages.update({"selected_blend": alpha, "validation": validation})
    method = evaluate(data, scorer)
    return summary_result(key="grc", paper={"arxiv_id": "2602.23639", "title": "Learning to Reflect and Correct: Towards Better Decoding Trajectories for Large-Scale Generative Recommendation", "url": "https://arxiv.org/abs/2602.23639", "organization": "Alibaba International / Wuhan University"}, data=data, baseline_name="GR-backbone", method_name="GRC", baseline=baseline, proposed=method, stages=stages, paper_results={"Revenue": 1.79, "CTR": 2.11, "GMV": 2.04}, scope="实际构造 draft/reflection/correction 单序列 SFT 标签，学习首错位置和语义一致性，执行完整 trajectory 的 group-relative clipped update，并以 reflection entropy 在固定 beam budget 内调度 correction。")
