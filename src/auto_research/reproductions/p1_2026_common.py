from __future__ import annotations

from pathlib import Path

from .p0_2026_common import run_scoring_reproduction


PAPERS = {
    "onemall": {
        "arxiv_id": "2601.21770",
        "title": "OneMall: One Model, More Scenarios -- End-to-End Generative Recommender Family at Kuaishou E-Commerce",
        "url": "https://arxiv.org/abs/2601.21770",
        "organization": "Kuaishou",
    },
    "dos": {
        "arxiv_id": "2602.04460",
        "title": "DOS: Dual-Flow Orthogonal Semantic IDs for Recommendation in Meituan",
        "url": "https://arxiv.org/abs/2602.04460",
        "organization": "Meituan",
    },
    "mdl": {
        "arxiv_id": "2602.07520",
        "title": "MDL: A Unified Multi-Distribution Learner in Large-scale Industrial Recommendation through Tokenization",
        "url": "https://arxiv.org/abs/2602.07520",
        "organization": "ByteDance / Douyin",
    },
    "hisac": {
        "arxiv_id": "2602.21009",
        "title": "HiSAC: Hierarchical Sparse Activation Compression for Ultra-long Sequence Modeling in Recommenders",
        "url": "https://arxiv.org/abs/2602.21009",
        "organization": "Alibaba / Taobao",
    },
    "pinclip": {
        "arxiv_id": "2603.03544",
        "title": "PinCLIP: Large-scale Foundational Multimodal Representation at Pinterest",
        "url": "https://arxiv.org/abs/2603.03544",
        "organization": "Pinterest",
    },
    "pin-scale": {
        "arxiv_id": "sigir2026-pin-scale",
        "title": "Pin-SCALE: Semantic Cascading and Alignment Learning for Engagement-Aware IDs in Cold-Start Recommendations",
        "url": "https://sigir2026.org/SIGIR2026_program.pdf",
        "organization": "Pinterest",
    },
    "causal-retrieval": {
        "arxiv_id": "2607.14161",
        "title": "Deep-learning Causal Retrieval Optimization for Efficient e-commerce Distribution in Pinterest",
        "url": "https://arxiv.org/abs/2607.14161",
        "organization": "Pinterest",
    },
    "podcast-mtl": {
        "arxiv_id": "2601.02306",
        "title": "Cold-Starting Podcast Ads and Promotions with Multi-Task Learning on Spotify",
        "url": "https://arxiv.org/abs/2601.02306",
        "organization": "Spotify",
    },
}


def run_p1(
    *,
    key: str,
    dataset_dir: Path,
    build_method,
    baseline_name: str,
    method_name: str,
    paper_results: dict,
    scope: str,
):
    return run_scoring_reproduction(
        key=key,
        paper=PAPERS[key],
        dataset_dir=dataset_dir,
        build_method=build_method,
        baseline_name=baseline_name,
        method_name=method_name,
        paper_results=paper_results,
        scope=scope,
    )
