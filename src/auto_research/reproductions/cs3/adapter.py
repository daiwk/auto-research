from ..base import OnlineABEvidence, PaperMetadata, ReproductionAdapter, ReproductionFidelity
from ..registry import register
from .experiment import reproduce
from .report import render

ADAPTER = register(ReproductionAdapter(
    key="cs3",
    paper=PaperMetadata(
        arxiv_id="2604.19269", title="CS3: Efficient Online Capability Synergy for Two-Tower Recommendation",
        url="https://arxiv.org/abs/2604.19269", track="recommendation",
        code_url="https://github.com/lixiangwang/CS3Rec",
        organization="Kuaishou Technology", published="2026-04-21",
        topics=("retrieval", "two-tower", "online-learning"),
        online_ab=(OnlineABEvidence("Kuaishou advertising", "Revenue", 8.356, "Scenario A; three production scenarios"),),
    ),
    run=reproduce, render=render, fidelity=ReproductionFidelity.CORE_MECHANISM,
    omitted_core_components=("400M-DAU online feature cache", "production EMA cross vectors and QPS stack"),
))
