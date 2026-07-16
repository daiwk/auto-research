from pathlib import Path

from ..industrial_2026 import evaluate, load_industrial_data, base_scores, summary_result, tune_blend
from .model import score_degre, train_degre


def reproduce_degre(dataset_dir: Path, seed: int = 42) -> dict:
    data = load_industrial_data(dataset_dir)
    _, dense, stages = train_degre(data, seed)
    baseline = evaluate(data, lambda history: base_scores(data, history))
    alpha, scorer, validation = tune_blend(data, lambda h: base_scores(data, h), lambda h: score_degre(data, dense, h))
    stages.update({"selected_blend": alpha, "validation": validation})
    proposed = evaluate(data, scorer)
    return summary_result(key="degre", paper={"arxiv_id": "2605.25749", "title": "DeGRe: Listwise Generative Reranking with Offline Lookahead Distillation", "url": "https://arxiv.org/abs/2605.25749", "organization": "Alibaba Group / Zhejiang University"}, data=data, baseline_name="pointwise-generator", method_name="DeGRe", baseline=baseline, proposed=proposed, stages=stages, paper_results={"Taobao Flash CTR": 2.85, "Taobao Flash orders": 2.14, "Taobao Flash GMV": 3.75}, scope="实际训练累计价值 evaluator、执行 lookahead beam mining、构造逐前缀 dense soft label 与 beam 权重，再蒸馏到单次在线 scorer；MovieLens 正反馈、diversity 与 novelty 代理私有交易价值。")
