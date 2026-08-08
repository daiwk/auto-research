from ..base import OnlineABEvidence, PaperMetadata, ReproductionAdapter, ReproductionFidelity
from ..registry import register
from .experiment import reproduce_degr
from .report import render


ADAPTER = register(ReproductionAdapter(
    key="degr",
    paper=PaperMetadata(
        arxiv_id="2608.04809",
        title="DEGR: Dual Exploration-Driven Generative Re-Ranking for Adaptive Cross-Request Context Bridging",
        url="https://arxiv.org/abs/2608.04809",
        track="recommendation",
        organization="JD.com",
        published="2026-08-05",
        topics=("reranking", "slate-optimization", "exploration", "preference-optimization"),
        online_ab=(
            OnlineABEvidence("JD homepage recommendation", "UCTR", 1.22, "online A/B test"),
            OnlineABEvidence("JD homepage recommendation", "PV", 0.20, "online A/B test"),
        ),
    ),
    run=reproduce_degr,
    render=render,
    fidelity=ReproductionFidelity.CORE_MECHANISM,
    omitted_core_components=(
        "JD one-billion-request private dataset",
        "industrial exploratory reward model",
        "cross-request exposure trajectories",
    ),
))
