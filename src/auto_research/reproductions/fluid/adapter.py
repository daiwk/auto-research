from ..base import OnlineABEvidence, PaperMetadata, ReproductionAdapter, ReproductionFidelity
from ..registry import register
from .experiment import reproduce_fluid
from .report import render


ADAPTER = register(ReproductionAdapter(
    key="fluid",
    paper=PaperMetadata(
        arxiv_id="2605.21832",
        title="FLUID: From Ephemeral IDs to Multimodal Semantic Codes for Industrial-Scale Livestreaming Recommendation",
        url="https://arxiv.org/abs/2605.21832",
        track="recommendation",
        organization="TikTok / ByteDance",
        published="2026-05-20",
        topics=("llm-recommendation", "multimodal", "semantic-id", "cold-start", "ranking"),
        online_ab=(
            OnlineABEvidence("TikTok / ByteDance livestreaming", "Quality Watch Duration", 0.55, "production online A/B test"),
            OnlineABEvidence("TikTok / ByteDance livestreaming", "Cold-Start Room Views", 2.05, "production online A/B test"),
        ),
    ),
    run=reproduce_fluid,
    render=render,
    fidelity=ReproductionFidelity.CORE_MECHANISM,
    omitted_core_components=("private livestream slices and user traffic", "SigLIP2 + Qwen3-Embedding-0.6B encoder", "production incremental training"),
))
