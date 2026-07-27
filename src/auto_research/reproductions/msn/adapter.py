from ..base import OnlineABEvidence, PaperMetadata, ReproductionAdapter, ReproductionFidelity
from ..registry import register
from ..industrial_2026 import render_standard
from .experiment import reproduce_msn

ADAPTER = register(ReproductionAdapter(
    key="msn", paper=PaperMetadata(
        arxiv_id="2602.07526", title="MSN: A Memory-based Sparse Activation Scaling Framework for Large-scale Industrial Recommendation",
        url="https://arxiv.org/abs/2602.07526", track="recommendation",
        organization="ByteDance / Douyin Search", published="2026-02-07",
        topics=("search-ranking", "sparse-memory", "product-key-memory"),
        online_ab=(
            OnlineABEvidence("Douyin Search", "Watch time", 0.2958, "online A/B"),
            OnlineABEvidence("Douyin Search", "Finish rate", 0.2071, "online A/B"),
        ),
    ), run=reproduce_msn, render=render_standard,
    fidelity=ReproductionFidelity.CORE_MECHANISM,
    omitted_core_components=("private search logs", "production sparse-memory kernel"),
))
