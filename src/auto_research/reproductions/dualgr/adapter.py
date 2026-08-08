from ..base import OnlineABEvidence, PaperMetadata, ReproductionAdapter, ReproductionFidelity
from ..registry import register
from .experiment import reproduce
from .report import render

ADAPTER = register(ReproductionAdapter(
    key="dualgr", paper=PaperMetadata(
        arxiv_id="2511.12518", title="DualGR: Generative Retrieval with Long and Short-Term Interests Modeling",
        url="https://arxiv.org/abs/2511.12518", track="recommendation",
        organization="USTC / Kuaishou Technology", published="2025-11-16",
        topics=("retrieval", "generative-recommendation", "semantic-id", "long-short-interest"),
        online_ab=(OnlineABEvidence("Kuaishou", "Video Views", 0.527, "online A/B"),),
    ), run=reproduce, render=render, fidelity=ReproductionFidelity.CORE_MECHANISM,
    omitted_core_components=("Kuaishou private exposure logs", "production constrained decoder"),
))
