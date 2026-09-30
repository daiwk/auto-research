from __future__ import annotations

import json
from pathlib import Path

import numpy as np

from auto_research.recommendation_latest_20260930_closure import (
    promptshift_metrics,
    promptshift_rerank,
)


def reproduce(_dataset_dir: Path, seed: int = 42) -> dict:
    """Run identity-cue drift diagnostics and adaptive popularity mitigation."""
    rng = np.random.default_rng(seed)
    items = np.arange(10)
    relevance = np.linspace(1.0, 0.1, 10) + rng.normal(0.0, 0.005, 10)
    popularity = np.linspace(0.9, 0.05, 10)
    reference = items[np.argsort(-relevance, kind="stable")]
    identity_cued = reference.copy()
    identity_cued[[2, 7]] = identity_cued[[7, 2]]
    before = promptshift_metrics(
        reference, identity_cued, popularity, relevant={0, 1, 6, 7}, k=10
    )
    reranked, _ = promptshift_rerank(
        identity_cued, relevance[identity_cued], popularity, mainstreamness=0.35
    )
    after = promptshift_metrics(
        reference, reranked, popularity, relevant={0, 1, 6, 7}, k=10
    )
    return {
        "paper": {
            "arxiv_id": "2609.34229",
            "url": "https://arxiv.org/abs/2609.34229",
        },
        "dataset": "deterministic public identity-slice fixture",
        "setup": {"seed": seed, "items": len(items), "mainstreamness": 0.35},
        "baseline": {"name": "identity-cued ranking", **before},
        "method": {"name": "PromptShift adaptive reranker", **after},
        "scope": (
            "执行 Drift、SliceShift、difficulty-weighted hit 与后处理 reranker；"
            "身份 slice 和相关性由公开 fixture 给出，不生成真实用户画像。"
        ),
    }


def render(result: dict) -> str:
    return "# PromptShift\n\n```json\n" + json.dumps(
        result, ensure_ascii=False, indent=2
    ) + "\n```\n"
