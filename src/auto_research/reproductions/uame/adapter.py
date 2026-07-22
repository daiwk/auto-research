from ..base import OnlineABEvidence, PaperMetadata, ReproductionAdapter, ReproductionFidelity
from ..industrial_2026 import render_standard
from ..registry import register
from .experiment import reproduce_uame


ADAPTER = register(ReproductionAdapter(
    key="uame",
    paper=PaperMetadata(
        arxiv_id="2607.17092", title="Uncertainty as Remedy: Mitigating Satisfaction Label Bias in Short Video Multi-Objective Ensemble Ranking",
        url="https://arxiv.org/abs/2607.17092", track="recommendation", organization="Kuaishou Technology", published="2026-07-19",
        topics=("multi-objective-ranking", "uncertainty", "loss-design"),
        online_ab=(
            OnlineABEvidence("Kuaishou short-video feed vs EMER", "LongView", 1.614, "7 days; 5% traffic; p<0.005"),
            OnlineABEvidence("Kuaishou short-video feed vs EASQ", "Forward", 1.598, "7 days; 5% traffic; p<0.005"),
        ),
    ),
    run=reproduce_uame, render=render_standard,
    fidelity=ReproductionFidelity.CORE_MECHANISM,
    omitted_core_components=("private eight-pxtr logs", "EMER/EASQ production backbones", "questionnaire satisfaction labels"),
))
