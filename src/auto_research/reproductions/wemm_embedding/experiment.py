from __future__ import annotations

from pathlib import Path

from ..recent_20260728_common import load_recent_movielens, relative
from .model import align_views, paired_views, refine_with_cross_scale_teacher, retrieval_metrics


def reproduce_wemm_embedding(dataset_dir: Path, seed: int = 42) -> dict:
    data = load_recent_movielens(dataset_dir, maximum_users=320, maximum_items=360)
    content, collaborative = paired_views(data)
    stage1 = align_views(content, collaborative, dimension=16)
    stage2 = refine_with_cross_scale_teacher(*stage1)
    baseline = retrieval_metrics(*stage1)
    method = retrieval_metrics(*stage2)
    matryoshka = {
        str(dim): retrieval_metrics(stage2[0][:, :dim], stage2[1][:, :dim])
        for dim in (4, 8, 16)
    }
    return {
        "paper": {"arxiv_id": "2608.24053", "title": "WeMM-Embedding"},
        "dataset": {"name": "MovieLens-1M paired content/collaborative views", "items": data.item_count},
        "setup": {"seed": seed, "alignment_stages": 2, "embedding_dimension": 16},
        "variants": {"stage-1 multimodal alignment": baseline, "WeMM refinement": method},
        "matryoshka": matryoshka,
        "relative": relative(method, baseline),
        "paper_results": {"mmeb_v2_9b": 80.6, "online_ab_tests": 14, "production_rollout": True},
        "scope": "在 MovieLens-1M 公开内容特征与协同共现视图上真实执行两阶段跨模态对齐、细粒度 relevance refinement、cross-scale teacher transfer 和 Matryoshka 截断评测；未加载 WeMM 2B/4B/9B checkpoint、数亿私有样本或微信线上索引。",
    }
