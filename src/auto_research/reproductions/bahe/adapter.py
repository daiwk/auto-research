from ..base import OnlineABEvidence, PaperMetadata, ReproductionAdapter, ReproductionFidelity
from ..registry import register
from .experiment import reproduce_bahe
from .report import render

ADAPTER = register(ReproductionAdapter(
    key="bahe",
    paper=PaperMetadata(
        arxiv_id="2403.19347", title="Breaking the Length Barrier: LLM-Enhanced CTR Prediction in Long Textual User Behaviors",
        url="https://arxiv.org/abs/2403.19347", track="recommendation",
        organization="Ant Group", published="2024-03",
        topics=("llm-recommendation", "ctr-ranking", "long-sequence", "efficiency"),
        online_ab=(OnlineABEvidence("e-commerce ads", "CTR", 9.65, "two-week A/B test"),),
    ),
    run=reproduce_bahe, render=render,
    fidelity=ReproductionFidelity.FULL_PIPELINE,
))
