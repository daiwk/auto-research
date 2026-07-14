from ..base import OnlineABEvidence, PaperMetadata, ReproductionAdapter, ReproductionFidelity
from ..registry import register
from .experiment import reproduce_beque
from .report import render

ADAPTER = register(ReproductionAdapter(
    key="beque",
    paper=PaperMetadata(
        arxiv_id="2311.03758", title="Large Language Model based Long-tail Query Rewriting in Taobao Search",
        url="https://arxiv.org/abs/2311.03758", track="recommendation",
        organization="Alibaba", published="2023-11",
        topics=("llm-recommendation", "query-rewriting", "preference-optimization", "search"),
        online_ab=(OnlineABEvidence("Mobile Taobao Search", "GMV", 0.40, "14-day online test"),),
    ),
    run=reproduce_beque, render=render,
    fidelity=ReproductionFidelity.FULL_PIPELINE,
))
