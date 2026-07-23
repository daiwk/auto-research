from ..base import OnlineABEvidence, PaperMetadata, ReproductionAdapter, ReproductionFidelity
from ..registry import register
from .experiment import reproduce_whale
from .report import render


ADAPTER = register(ReproductionAdapter(
    key="whale",
    paper=PaperMetadata(
        arxiv_id="2607.17017",
        title="WHALE: A Scalable Unified Model for Recommendation with Wukong-HSTU Architecture",
        url="https://arxiv.org/abs/2607.17017",
        track="recommendation",
        organization="Meta Platforms, Inc.",
        published="2026-07-19",
        topics=("ranking", "hstu", "feature-interaction", "scaling"),
        online_ab=(
            OnlineABEvidence("Meta social recommendation surface", "Primary metric", 0.113, "14 days; production baseline"),
            OnlineABEvidence("Meta social recommendation surface", "Metric 1", 0.824, "14 days; production baseline"),
        ),
    ),
    run=reproduce_whale,
    render=render,
    fidelity=ReproductionFidelity.CORE_MECHANISM,
    omitted_core_components=("private Meta ranking features and labels", "production Triton and AOTInductor kernels"),
))
