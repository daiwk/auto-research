from ..base import OnlineABEvidence, PaperMetadata, ReproductionAdapter, ReproductionFidelity
from ..registry import register
from .experiment import reproduce_tmallgs
from .report import render


ADAPTER = register(ReproductionAdapter(
    key="tmallgs",
    paper=PaperMetadata(
        arxiv_id="2607.13398",
        title="TMallGS: Scaling Unified Feature and Sequence Modeling for Generative E-commerce Search",
        url="https://arxiv.org/abs/2607.13398",
        track="recommendation",
        organization="Taobao & Tmall Group of Alibaba",
        published="2026-07-15",
        topics=("search-ranking", "transformer", "scaling", "feature-interaction"),
        online_ab=(
            OnlineABEvidence("Tmall Search", "UCTCVR", 1.38, "30 days; p<0.05"),
            OnlineABEvidence("Tmall Search", "GMV", 1.52, "30 days; p<0.05"),
        ),
    ),
    run=reproduce_tmallgs,
    render=render,
    fidelity=ReproductionFidelity.CORE_MECHANISM,
    omitted_core_components=("private Tmall search features and labels", "0.05B online model and production GPU serving"),
))
