from ..base import OnlineABEvidence, PaperMetadata, ReproductionAdapter, ReproductionFidelity
from ..registry import register
from .experiment import reproduce_tokenmixer_large
from .report import render

ADAPTER = register(ReproductionAdapter(
    key="tokenmixer-large", paper=PaperMetadata(
        arxiv_id="2602.06563", title="TokenMixer-Large: Scaling Up Large Ranking Models in Industrial Recommenders",
        url="https://arxiv.org/abs/2602.06563", track="recommendation",
        organization="ByteDance", published="2026-02-06",
        topics=("ranking", "token-mixing", "scaling"),
        online_ab=(
            OnlineABEvidence("ByteDance e-commerce", "Orders", 1.66, "online A/B"),
            OnlineABEvidence("ByteDance e-commerce", "Per-capita payment GMV", 2.98, "online A/B"),
            OnlineABEvidence("ByteDance ads", "ADSS", 2.0, "online A/B"),
        ),
    ), run=reproduce_tokenmixer_large, render=render,
    fidelity=ReproductionFidelity.FULL_PIPELINE,
    omitted_core_components=("private trillion-scale training data", "production fused kernels"),
))
