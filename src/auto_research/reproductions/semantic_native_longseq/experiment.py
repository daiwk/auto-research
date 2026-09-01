from pathlib import Path

from ..industrial_2026 import evaluate, load_industrial_data, summary_result
from .model import build_semantic_native, score_semantic_long, score_vanilla_short


def reproduce_semantic_native_longseq(dataset_dir: Path, seed: int = 42) -> dict:
    data = load_industrial_data(dataset_dir)
    state = build_semantic_native(data, seed)
    baseline = evaluate(data, lambda history: score_vanilla_short(data, state, history))
    method = evaluate(data, lambda history: score_semantic_long(data, state, history)[0])
    _, trace = score_semantic_long(data, state, data.sequences.train[0])
    return summary_result(
        key="semantic-native-longseq",
        paper={
            "arxiv_id": "2606.07546",
            "title": "Beyond Item IDs: Scaling Short-Form-Video Recommendation via Semantic-Native Long Sequence Modeling",
            "url": "https://arxiv.org/abs/2606.07546",
            "organization": "Google",
        },
        data=data,
        baseline_name="short Video-ID-like vanilla attention",
        method_name="SID + global-aware temporal folding",
        baseline=baseline,
        proposed=method,
        stages={
            **trace,
            "sid_levels": 3,
            "depth_truncated_bigram_vocabulary": int(len(set(state["bigrams"].tolist()))),
        },
        paper_results={
            "freshness_satisfied_views_percent": 6.81,
            "step_time_reduction_percent": 83.9,
            "peak_hbm_reduction_percent": 92.2,
            "actively_engaged_users_percent": 0.52,
            "satisfied_watch_time_percent": 1.42,
            "satisfied_views_percent": 1.08,
        },
        scope=(
            "实际执行 residual-quantized SID、depth-truncated bigram、parameter-free temporal folding、双 global query "
            "和统一 global-local pooling；48-event MovieLens 历史替代生产 2,000 视频序列，未复刻 Google RQ-VAE 训练和异步服务图。"
        ),
    )
