from ..base import OnlineABEvidence, PaperMetadata, ReproductionAdapter, ReproductionFidelity
from ..registry import register
from .experiment import reproduce
from .report import render

ADAPTER = register(ReproductionAdapter(
    key="cdm", paper=PaperMetadata(
        arxiv_id="2406.09021", title="Contextual Distillation Model for Diversified Recommendation",
        url="https://arxiv.org/abs/2406.09021", track="recommendation", organization="Kuaishou Technology",
        published="2024-06-13", topics=("reranking", "diversity", "knowledge-distillation"),
        online_ab=(OnlineABEvidence("Kuaishou", "Watch Time", 0.406, "main-app A/B"),),
    ), run=reproduce, render=render, fidelity=ReproductionFidelity.CORE_MECHANISM,
    omitted_core_components=("private short-video features", "production MMR teacher traffic"),
))
