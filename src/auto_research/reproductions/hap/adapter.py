from ..base import OnlineABEvidence, PaperMetadata, ReproductionAdapter, ReproductionFidelity
from ..registry import register
from .experiment import reproduce
from .report import render

ADAPTER = register(ReproductionAdapter(
    key="hap", paper=PaperMetadata(
        arxiv_id="2603.03770", title="Not All Candidates are Created Equal: Heterogeneity-Aware Pre-ranking",
        url="https://arxiv.org/abs/2603.03770", code_url="https://github.com/Toutiao-Rec/HAP",
        track="recommendation", organization="ByteDance / Toutiao", published="2026-03-04",
        topics=("pre-ranking", "contrastive-learning", "dynamic-routing"),
        online_ab=(OnlineABEvidence("Toutiao", "App Usage Duration", 0.4, "nine-month deployment"),),
    ), run=reproduce, render=render, fidelity=ReproductionFidelity.CORE_MECHANISM,
    omitted_core_components=("Toutiao private candidates", "heterogeneous production model fleet"),
))
