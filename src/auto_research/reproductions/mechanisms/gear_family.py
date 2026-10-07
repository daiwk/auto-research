"""Extracted unchanged from auto_research.reproductions.latest_20261002; stable mechanism boundary."""
from __future__ import annotations

from auto_research.paper_specs.runtime import adapter_from_spec
from pathlib import Path
import torch
from auto_research.mechanisms.basis_vq import basis_vq
from auto_research.mechanisms.effective_training_time import effective_training_time
from auto_research.mechanisms.gear_collision_rerank import gear_collision_rerank
from auto_research.mechanisms.gris_hierarchical_ids import gris_hierarchical_ids
from auto_research.mechanisms.repair_preference_state import repair_preference_state
from auto_research.reproductions.base import EvaluationTier, OnlineABEvidence, PaperMetadata, ReproductionAdapter, ReproductionFidelity

PAPERS = {
    "gear": {
        "arxiv_id": "2609.39327",
        "title": "Generative End-to-end Ad Retrieval at Douyin",
        "organization": "ByteDance",
        "published": "2026-09-30",
        "topics": ("ad-retrieval", "generative-retrieval", "semantic-id"),
        "omitted": (
            "Douyin Ads private logs",
            "streaming parameter server and minute-level index",
            "production traffic",
        ),
    },
    "effective-training-time": {
        "arxiv_id": "2610.02057",
        "title": "Optimizing Effective Training Time for Large-Scale Recommendation Systems",
        "organization": "Meta Platforms, Inc.",
        "published": "2026-10-01",
        "topics": ("training-systems", "effective-training-time", "gpu-fleet"),
        "omitted": ("Meta production trainers", "fleet telemetry", "deployment control plane"),
        "selection_exception": (
            "用户于 2026-10-02 明确批准的生产训练基础设施例外；"
            "部署指标是 ETT，不作为推荐模型效果或线上 A/B 收益。"
        ),
    },
    "gris": {
        "arxiv_id": "2610.01533",
        "title": "Neither Black nor White: Balancing Semantic and Collaborative Signals with Graph-Informed Semantic IDs (GrIS)",
        "organization": "Huawei Ireland Research Centre",
        "published": "2026-10-01",
        "topics": ("generative-recommendation", "semantic-id", "graph-partition"),
        "code_url": "https://github.com/hirc-airecs/graph-informed-sids",
        "omitted": ("full benchmark training", "production interaction graph", "generative decoder"),
        "selection_exception": (
            "用户于 2026-10-02 明确批准的学术/Evolve 机制例外；"
            "论文没有量化线上 A/B，不进入工业证据结论。"
        ),
    },
    "repair-state": {
        "arxiv_id": "2610.01270",
        "title": "Not All Is Lost: Repairing Lossy User Preference States of Personalization Encoders",
        "organization": "原文首页未列第一作者机构",
        "published": "2026-10-01",
        "topics": ("personalization", "state-repair", "sequential-recommendation"),
        "omitted": ("twelve pretrained host recommenders", "large public benchmarks", "generation heads"),
        "selection_exception": (
            "用户于 2026-10-02 明确批准的学术/Evolve 机制例外；"
            "论文没有量化线上 A/B，不进入工业证据结论。"
        ),
    },
}

def reproduce(key: str, dataset_dir: Path, seed: int = 42) -> dict:
    """Execute the defining mechanism without pretending to use private data."""
    del dataset_dir
    torch.manual_seed(seed)
    if key == "gear":
        basis, _ = torch.linalg.qr(torch.randn(5, 5))
        quantized, codes = basis_vq(torch.randn(12, 5), basis, torch.randn(8, 5))
        order, scores = gear_collision_rerank(
            torch.randn(5), quantized[:4], [(0,), (0,), (1,), (1,)]
        )
        metrics = {
            "used_codes": int(codes.unique().numel()),
            "reranked_items": len(order),
            "score_std": float(scores.std()),
        }
    elif key == "effective-training-time":
        ett, losses = effective_training_time(
            {"training": 80, "compile": 8, "checkpoint": 7, "recovery": 5}
        )
        metrics = {"ett": ett, "loss_fraction": sum(losses.values())}
    elif key == "gris":
        features = torch.randn(10, 4)
        adjacency = torch.eye(10)
        adjacency[:-1, 1:] += torch.eye(9)
        ids = gris_hierarchical_ids(features, adjacency, levels=3)
        metrics = {
            "unique_ids": int(ids.unique(dim=0).shape[0]),
            "levels": ids.shape[1],
        }
    elif key == "repair-state":
        repaired, audit = repair_preference_state(
            torch.randn(6), torch.randn(12, 6), torch.randn(6), top_k=3
        )
        metrics = {
            "state_norm": float(repaired.norm()),
            "selected_timesteps": len(audit["selected_timesteps"]),
        }
    else:
        raise KeyError(key)
    row = PAPERS[key]
    return {
        "manifest_ref": f"reproduction:{key}",
        "paper": {
            "arxiv_id": row["arxiv_id"],
            "title": row["title"],
            "url": f"https://arxiv.org/abs/{row['arxiv_id']}",
            "track": "recommendation",
        },
        "dataset": "deterministic public mechanism mini-suite",
        "setup": {"seed": seed, "diagnostic_only": True},
        "results": metrics,
        "scope": "L1 核心机制诊断；不复刻私有数据、生产系统或论文规模训练。",
    }

def render(result: dict) -> str:
    import json

    return "# 机制诊断结果\n\n```json\n" + json.dumps(
        result, ensure_ascii=False, indent=2
    ) + "\n```\n"

def make_adapter(key: str) -> ReproductionAdapter:
    row = PAPERS[key]
    online_ab = ()
    if key == "gear":
        source = "https://arxiv.org/html/2609.39327v1"
        online_ab = (
            OnlineABEvidence(
                "Douyin Ads",
                "ADSS",
                0.563,
                "seven-day online A/B; 5% traffic in each group",
                source_url=source,
                source_location="Section 6.4, Table 6",
                experiment_duration="7 days",
                retrieved_at="2026-10-02",
            ),
            OnlineABEvidence(
                "Douyin Ads",
                "ADVV",
                0.658,
                "seven-day online A/B; 5% traffic in each group",
                source_url=source,
                source_location="Section 6.4, Table 6",
                experiment_duration="7 days",
                retrieved_at="2026-10-02",
            ),
        )
    return adapter_from_spec(key=key, run=lambda dataset_dir, seed=42: reproduce(key, dataset_dir, seed), render=render)
