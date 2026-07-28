from pathlib import Path
from ..p0_2026_common import run_scoring_reproduction
from .model import build_cq_sid

def reproduce(dataset_dir: Path, seed: int = 42):
    return run_scoring_reproduction(
        key="cq-sid",
        paper={"arxiv_id": "2605.14434", "title": "Efficient Generative Retrieval for E-commerce Search with Semantic Cluster IDs and Expert-Guided RL", "url": "https://arxiv.org/abs/2605.14434", "organization": "Alibaba Taobao & Tmall"},
        dataset_dir=dataset_dir,
        build_method=lambda data: build_cq_sid(data, seed),
        baseline_name="transition + content recall",
        method_name="CQ-SID + progressive translation + EG-GRPO reward",
        paper_results={"semantic_click_hitrate_relative_percent": 26.76, "personalized_click_hitrate_relative_percent": 11.11, "online_gmv_percent": 1.15, "online_uctcvr_percent": 0.40, "purchase_contribution_percent": 72.63},
        scope="实际构造 category-constrained 首级 code、两级 residual semantic cluster、四类 progressive translation 特征，并执行 240 次 ground-truth 强制入组的 group-relative policy update。MovieLens genre/history 替代自然语言 query，未训练论文的 64-GPU 生成 LLM。",
    )
