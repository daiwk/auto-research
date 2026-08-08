from ..base import OnlineABEvidence, PaperMetadata, ReproductionAdapter, ReproductionFidelity
from ..registry import register
from .experiment import reproduce
from .report import render

ADAPTER = register(ReproductionAdapter(
    key="mpformer", paper=PaperMetadata(
        arxiv_id="2508.20400", title="MPFormer: Adaptive Framework for Industrial Multi-Task Personalized Sequential Retriever",
        url="https://arxiv.org/abs/2508.20400", track="recommendation", organization="Kuaishou Technology",
        published="2025-08-28", topics=("retrieval", "multi-task", "sequence", "serving"),
        online_ab=(OnlineABEvidence("Kuaishou", "Watch Time", 0.426, "online A/B"),),
    ), run=reproduce, render=render, fidelity=ReproductionFidelity.CORE_MECHANISM,
    omitted_core_components=("400M-DAU traffic", "1.2M-QPS serving stack"),
))
