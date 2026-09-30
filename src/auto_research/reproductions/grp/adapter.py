"""Register the public Snap GRP v0.1 mechanisms."""

from __future__ import annotations

from ..base import EvaluationTier, OnlineABEvidence, PaperMetadata, ReproductionAdapter, ReproductionFidelity
from ..registry import register
from .experiment import reproduce


def render(result: dict) -> str:
    metrics = result["metrics"]
    return "# GRP v0.1 机制诊断\n\n" + "\n".join(f"- {key}: {value}" for key, value in metrics.items()) + f"\n\n> {result['scope']}\n"


ADAPTER = register(ReproductionAdapter(
    key="grp",
    paper=PaperMetadata(
        arxiv_id="2609.36688", title="GRP v0.1 Technical Report",
        url="https://arxiv.org/abs/2609.36688", track="recommendation",
        organization="Snap Inc.", published="2026-09-29", publication_label="arXiv v1",
        topics=("generative-recommendation", "ranking", "rl-alignment"),
        online_ab=(
            OnlineABEvidence("Snap short-video recommendation", "view time", 0.46, "retrieval-only online A/B", source_url="https://arxiv.org/html/2609.36688", source_location="Section 6.2", retrieved_at="2026-09-30"),
            OnlineABEvidence("Snap short-video recommendation", "shares", 2.56, "bypass plus source-replacement online A/B", source_url="https://arxiv.org/html/2609.36688", source_location="Section 6.4", retrieved_at="2026-09-30"),
        ),
    ),
    run=reproduce, render=render,
    fidelity=ReproductionFidelity.CONCEPT_DEMO,
    omitted_core_components=(
        "private Snap user/item data, Qwen3-VL semantic-ID tokenizer and production objectives",
        "full encoder-decoder training, CUDA-graph serving, reverse catalog and online traffic",
    ),
    evaluation_tier=EvaluationTier.MECHANISM,
    datasets=("deterministic tensor mini-suite",),
    baseline="GRPO surrogate without the active one-sided logged-target guard",
    metrics=("metrics.independent_blocks", "metrics.ranker_candidate_variance", "metrics.recall_guard"),
    default_seeds=(42, 43, 44),
    budget="two item blocks, three candidate scores and one mGRPO group per seed",
    device_capabilities=("cpu",), infer_device_capabilities=False,
))
