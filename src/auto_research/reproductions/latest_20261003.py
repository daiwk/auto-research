"""Executable recommendation adapters from the 2026-10-03 intake."""

from __future__ import annotations

from pathlib import Path

import torch

from ..recommendation_latest_20261003 import agent_web_evidence, rptune_curate
from .base import EvaluationTier, PaperMetadata, ReproductionAdapter, ReproductionFidelity


PAPERS = {
    "rptune": {
        "arxiv_id": "2610.00964",
        "title": "RPTune: Learned Context Curation for LLM Catalog Search",
        "organization": "Google",
        "published": "2026-10-01",
        "topics": ("search", "llm-recommendation", "context-curation"),
        "omitted": ("seven merchant catalogs", "Gemma-4 post-training", "frontier LLM feedback"),
        "selection_exception": (
            "Google 高优先全文复核后的学术/Evolve 机制收录；论文报告真实商家实验，"
            "但没有量化线上 A/B，不进入工业搜广推线上证据结论。"
        ),
    },
    "agent-web-rec": {
        "arxiv_id": "2610.01705",
        "title": "AgentWebRec: Compact Evidence Fusion over the Agent Web for Personalized Recommendation",
        "organization": "Beihang University",
        "published": "2026-10-01",
        "topics": ("agent-recommendation", "private-memory", "evidence-fusion"),
        "omitted": ("LLM query generation", "InstructRec full benchmark", "deployed agent web"),
        "selection_exception": (
            "近期学术/Evolve 机制例外；论文没有量化线上 A/B，"
            "不进入工业搜广推证据结论。"
        ),
    },
}


def reproduce(key: str, dataset_dir: Path, seed: int = 42) -> dict:
    del dataset_dir
    torch.manual_seed(seed)
    if key == "rptune":
        order, scores = rptune_curate(
            torch.randn(8), torch.randn(12, 8), torch.randn(12) * .1, prune_rate=.5
        )
        metrics = {
            "retained_items": len(order),
            "highest_priority_last": int(order[-1]) == int(scores.argmax()),
            "score_std": float(scores.std()),
        }
    elif key == "agent-web-rec":
        chosen, patterns, audit = agent_web_evidence(
            torch.rand(8), torch.arange(8.0), semantic_weight=.7,
            memory_budget=3, confidence=.4, confidence_threshold=.7,
            collaborator_patterns=("prefers durable items", "avoids subscriptions"),
        )
        metrics = {"retrieved_memories": len(chosen), "patterns": len(patterns), **audit}
    else:
        raise KeyError(key)
    row = PAPERS[key]
    return {
        "manifest_ref": f"reproduction:{key}",
        "paper": {"arxiv_id": row["arxiv_id"], "title": row["title"], "url": f"https://arxiv.org/abs/{row['arxiv_id']}", "track": "recommendation"},
        "dataset": "deterministic public mechanism mini-suite",
        "setup": {"seed": seed, "diagnostic_only": True},
        "results": metrics,
        "scope": "L1 核心机制诊断；不复刻私有数据、模型服务或论文规模训练。",
    }


def render(result: dict) -> str:
    import json
    return "# 机制诊断结果\n\n```json\n" + json.dumps(result, ensure_ascii=False, indent=2) + "\n```\n"


def make_adapter(key: str) -> ReproductionAdapter:
    row = PAPERS[key]
    return ReproductionAdapter(
        key=key,
        paper=PaperMetadata(
            arxiv_id=row["arxiv_id"], title=row["title"],
            url=f"https://arxiv.org/abs/{row['arxiv_id']}", track="recommendation",
            organization=row["organization"], published=row["published"],
            publication_label="arXiv v1", topics=row["topics"],
            selection_exception=row.get("selection_exception"),
        ),
        run=lambda dataset_dir, seed=42: reproduce(key, dataset_dir, seed),
        render=render,
        fidelity=ReproductionFidelity.CORE_MECHANISM,
        omitted_core_components=row["omitted"],
        evaluation_tier=EvaluationTier.MECHANISM,
        datasets=("deterministic public mechanism mini-suite",),
        baseline="mechanism disabled or default state",
        metrics=tuple(reproduce(key, Path("."), 42)["results"]),
        default_seeds=(42, 43, 44),
        budget="deterministic L1 mechanism fixture",
        device_capabilities=("cpu",),
        infer_device_capabilities=False,
    )
