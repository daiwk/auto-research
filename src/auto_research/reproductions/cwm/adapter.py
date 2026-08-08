from ..base import OnlineABEvidence, PaperMetadata, ReproductionAdapter, ReproductionFidelity
from ..registry import register
from .experiment import reproduce
from .report import render

ADAPTER = register(ReproductionAdapter(
    key="cwm", paper=PaperMetadata(
        arxiv_id="2406.07932", title="Counteracting Duration Bias in Video Recommendation via Counterfactual Watch Time",
        url="https://arxiv.org/abs/2406.07932", code_url="https://github.com/hyz20/CWM",
        track="recommendation", organization="Kuaishou Technology / Renmin University of China",
        published="2024-06-12", topics=("ranking", "counterfactual-learning", "watch-time", "bias"),
        online_ab=(OnlineABEvidence("Kuaishou", "Mean Watch Time", 2.9, "online A/B"),),
    ), run=reproduce, render=render, fidelity=ReproductionFidelity.CORE_MECHANISM,
    omitted_core_components=("true video duration/watch-time censoring logs", "production survival model"),
))
