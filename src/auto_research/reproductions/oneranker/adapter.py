from ..base import OnlineABEvidence, PaperMetadata, ReproductionAdapter, ReproductionFidelity
from ..registry import register
from .experiment import reproduce
from .report import render

ADAPTER = register(ReproductionAdapter(
    key="oneranker", paper=PaperMetadata(
        arxiv_id="2603.02999", title="OneRanker: Unified Generation and Ranking with One Model in Industrial Advertising Recommendation",
        url="https://arxiv.org/abs/2603.02999", track="recommendation", organization="Tencent",
        published="2026-03-03", topics=("advertising", "generative-recommendation", "ranking", "multi-task"),
        online_ab=(OnlineABEvidence("Weixin Channels Ads", "GMV", 1.34, "full deployment"),),
    ), run=reproduce, render=render, fidelity=ReproductionFidelity.CORE_MECHANISM,
    omitted_core_components=("Weixin private ad logs", "production generative backbone"),
))
