from ..base import OnlineABEvidence, PaperMetadata, ReproductionAdapter, ReproductionFidelity
from ..registry import register
from .experiment import reproduce_steps
from .report import render

ADAPTER = register(ReproductionAdapter(
    key="steps",
    paper=PaperMetadata(
        arxiv_id="2608.01949", title="A Self-Triggered Agentic Push Recommendation System",
        url="https://arxiv.org/abs/2608.01949", track="recommendation",
        organization="ByteDance / Douyin", published="2026-08-03",
        topics=("push-recommendation", "agentic-recommendation", "decision-transformer", "serving"),
        online_ab=(
            OnlineABEvidence("Douyin Push", "Active days", 0.2843, "fully deployed; online A/B"),
            OnlineABEvidence("Douyin Push", "Push permission disablement", -1.9089, "fully deployed; online A/B"),
        ),
    ),
    run=reproduce_steps, render=render, fidelity=ReproductionFidelity.CORE_MECHANISM,
    omitted_core_components=("Douyin billion-user push trajectories", "production trigger scheduler and notification serving"),
))
