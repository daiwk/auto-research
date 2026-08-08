from ..base import OnlineABEvidence, PaperMetadata, ReproductionAdapter, ReproductionFidelity
from ..registry import register
from .experiment import reproduce
from .report import render

ADAPTER = register(ReproductionAdapter(
    key="glorank", paper=PaperMetadata(
        arxiv_id="2604.25291", title="From Local Indices to Global Identifiers: Generative Reranking via Global Action Space",
        url="https://arxiv.org/abs/2604.25291", track="recommendation",
        organization="City University of Hong Kong / Kuaishou / UC San Diego", published="2026-04-28",
        topics=("reranking", "generative-recommendation", "semantic-id", "reinforcement-learning"),
        online_ab=(OnlineABEvidence("Kuaishou", "Watch Time", 0.095, "7.8% traffic, 14 days"),),
    ), run=reproduce, render=render, fidelity=ReproductionFidelity.CORE_MECHANISM,
    omitted_core_components=("Kuaishou private traffic", "production LLM and constrained decoder"),
))
