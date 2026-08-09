from pathlib import Path

from ..industrial_2026 import base_scores, evaluate, load_industrial_data, summary_result, tune_blend
from .model import score_dual_sid, train_dual_sid


def reproduce_dual_sid(dataset_dir: Path, seed: int = 42) -> dict:
    data = load_industrial_data(dataset_dir)
    state = train_dual_sid(data)
    baseline = evaluate(data, lambda h: base_scores(data, h))
    alpha, scorer, validation = tune_blend(data, lambda h: base_scores(data, h), lambda h: score_dual_sid(data, state, h))
    method = evaluate(data, scorer)
    reconstruction_mse = float(((state["reconstructed"] - data.sequences.features) ** 2).mean())
    return summary_result(key="dual-sid", paper={"arxiv_id": "2607.24865", "title": "Tokens are All You Need: Dual-purpose Semantic IDs for Achieving LLM-Level I/O Efficiency in Recommendation Systems", "url": "https://arxiv.org/abs/2607.24865", "organization": "Google DeepMind / YouTube"}, data=data, baseline_name="dense transition-content retrieval", method_name="Dual-purpose SID", baseline=baseline, proposed=method, stages={"hierarchical_levels": 3, "codebook_width": 8, "semantic_decoder_mse": reconstruction_mse, "selected_blend": alpha, "validation": validation}, paper_results={"watchpage_ranking_percent": 0.09, "homepage_ranking_percent": 0.08, "retrieval_sitewide_percent": 0.06}, scope="实际训练三层协同 SID、逐层 SID 转移和从 SID one-hot 重建内容的 Semantic Decoder；genre 替代 YouTube 多模态内容，未复刻生产 embedding reconstruction 服务。")
