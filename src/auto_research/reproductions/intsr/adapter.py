from ..base import OnlineABEvidence, PaperMetadata, ReproductionAdapter, ReproductionFidelity
from ..registry import register
from .experiment import reproduce
from .report import render

ADAPTER = register(ReproductionAdapter(
    key="intsr", paper=PaperMetadata(
        arxiv_id="2509.21179", title="IntSR: An Integrated Generative Framework for Search and Recommendation",
        url="https://arxiv.org/abs/2509.21179", track="recommendation", organization="Alibaba / Amap",
        published="2025-09-25", topics=("search", "recommendation", "generative-retrieval", "content-understanding"),
        online_ab=(OnlineABEvidence("Amap", "GMV", 9.34, "online A/B"),),
    ), run=reproduce, render=render, fidelity=ReproductionFidelity.CORE_MECHANISM,
    omitted_core_components=("Amap private POI/query logs", "production autoregressive decoder"),
))
