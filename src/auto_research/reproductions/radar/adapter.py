from ..base import OnlineABEvidence, PaperMetadata, ReproductionAdapter, ReproductionFidelity
from ..registry import register
from .experiment import reproduce
from .report import render

ADAPTER = register(ReproductionAdapter(
    key="radar", paper=PaperMetadata(
        arxiv_id="2506.07261", title="RADAR: Recall Augmentation through Deferred Asynchronous Retrieval",
        url="https://arxiv.org/abs/2506.07261", track="recommendation", organization="Meta",
        published="2025-06-08", topics=("retrieval", "asynchronous-serving", "ranking"),
        online_ab=(OnlineABEvidence("Meta recommendation product", "Engagement", 0.8, "online A/B"),),
    ), run=reproduce, render=render, fidelity=ReproductionFidelity.CORE_MECHANISM,
    omitted_core_components=("billion-item catalog", "production deferred compute and KV store"),
))
