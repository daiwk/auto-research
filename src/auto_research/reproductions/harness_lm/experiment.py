from pathlib import Path

from ..industrial_2026 import evaluate, load_industrial_data, summary_result, tune_blend
from .model import score_harness, score_small, train_harness


def reproduce_harness_lm(dataset_dir: Path, seed: int = 42) -> dict:
    data = load_industrial_data(dataset_dir)
    docs, student, stages = train_harness(data, seed)
    baseline = evaluate(data, lambda h: score_small(data, h))
    alpha, scorer, validation = tune_blend(data, lambda h: score_small(data, h), lambda h: score_harness(data, docs, student, h))
    stages.update({"selected_blend": alpha, "validation": validation})
    method = evaluate(data, scorer)
    return summary_result(key="harness-lm", paper={"arxiv_id": "2605.23572", "title": "HARNESS-LM: A Three-Phase Training Recipe for Harnessing SLMs in Sponsored Search Retrieval", "url": "https://arxiv.org/abs/2605.23572", "organization": "Microsoft AI / Bing Ads"}, data=data, baseline_name="small-symmetric-retriever", method_name="HARNESS-LM", baseline=baseline, proposed=method, stages=stages, paper_results={"Revenue": 1.0, "Impressions": 0.6, "Clicks": 0.4}, scope="实际执行强 teacher、无标签 L2 query-space alignment、冻结 teacher document index 后的监督 InfoNCE refinement。公开实验以协同 SVD+内容构造离线强 teacher；没有宣称达到 Qwen3-Embedding 4B/0.6B 的规模与 Bing 延迟。")
