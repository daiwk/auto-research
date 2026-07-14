from ..base import OnlineABEvidence, PaperMetadata, ReproductionAdapter, ReproductionFidelity
from ..registry import register
from .experiment import reproduce_genrank
from .report import render

ADAPTER = register(ReproductionAdapter(
    key="genrank",
    paper=PaperMetadata(
        arxiv_id="2505.04180", title="Towards Large-scale Generative Ranking",
        url="https://arxiv.org/abs/2505.04180", track="recommendation",
        organization="Xiaohongshu", published="2025-05",
        topics=("generative-ranking", "action-modeling", "efficiency"),
        online_ab=(OnlineABEvidence("Explore Feed", "engagements", 1.2474, "10% treatment/control, 15 days"),),
    ),
    run=reproduce_genrank, render=render,
    fidelity=ReproductionFidelity.FULL_PIPELINE,
))
