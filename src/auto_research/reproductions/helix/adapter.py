"""Register the public HELIX architecture mechanism."""

from __future__ import annotations

from ..base import EvaluationTier, OnlineABEvidence, PaperMetadata, ReproductionAdapter, ReproductionFidelity
from ..registry import register
from .experiment import reproduce


def render(result: dict) -> str:
    metrics = result["metrics"]
    return (
        "# HELIX 架构诊断\n\n"
        f"- 候选条件分支差异：{metrics['candidate_conditioned_delta']:.6f}\n"
        f"- 用户缓存保持不变：{metrics['user_cache_unchanged']}\n\n"
        f"> {result['scope']}\n"
    )


ADAPTER = register(ReproductionAdapter(
    key="helix",
    paper=PaperMetadata(
        arxiv_id="2609.37183",
        title="HELIX: Purified and Unified - Rethinking Feature Interaction and Sequence Modeling for Large-Scale Recommendation",
        url="https://arxiv.org/abs/2609.37183",
        track="recommendation",
        organization="TikTok / ByteDance",
        published="2026-09-29",
        publication_label="arXiv v1",
        topics=("ranking", "feature-interaction", "sequence-modeling"),
        online_ab=(OnlineABEvidence(
            "TikTok e-commerce video recommendation", "e-commerce video GMV per user", 5.4624,
            "randomized full-traffic online A/B", source_url="https://arxiv.org/html/2609.37183",
            source_location="Section 3.5, Tables 4-5", retrieved_at="2026-09-30",
        ),),
    ),
    run=reproduce,
    render=render,
    fidelity=ReproductionFidelity.CONCEPT_DEMO,
    omitted_core_components=(
        "private TikTok feature schema, multitask labels and production training data",
        "pyramidal encoder, GQA kernels, M-FALCON serving and full-traffic validation",
    ),
    evaluation_tier=EvaluationTier.MECHANISM,
    datasets=("deterministic tensor mini-suite",),
    baseline="same user cache evaluated with two candidate-conditioned sequence streams",
    metrics=("metrics.candidate_conditioned_delta", "metrics.user_cache_unchanged"),
    default_seeds=(42, 43, 44),
    budget="two candidates, one reusable user cache, one HELIX core block per seed",
    device_capabilities=("cpu", "cuda"),
    infer_device_capabilities=False,
))
