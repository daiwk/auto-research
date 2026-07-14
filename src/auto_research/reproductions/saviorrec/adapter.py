from ..base import OnlineABEvidence, PaperMetadata, ReproductionAdapter, ReproductionFidelity
from ..registry import register
from .experiment import reproduce_saviorrec
from .report import render_report


register(ReproductionAdapter(
    key="saviorrec",
    paper=PaperMetadata(
        arxiv_id="2508.01375", title="SaviorRec: Semantic-Behavior Alignment for Cold-Start Recommendation",
        url="https://arxiv.org/abs/2508.01375", track="recommendation", organization="Alibaba",
        published="2025-08", topics=("cold start", "semantic ID", "multimodal recommendation"),
        online_ab=(
            OnlineABEvidence("Taobao Guess You Like cold-start", "Clicks", 13.31, "production A/B"),
            OnlineABEvidence("Taobao Guess You Like cold-start", "Orders", 13.44, "production A/B"),
            OnlineABEvidence("Taobao Guess You Like cold-start", "CTR", 12.80, "production A/B"),
        ),
    ), run=reproduce_saviorrec, render=render_report,
    fidelity=ReproductionFidelity.CORE_MECHANISM,
    omitted_core_components=("proprietary image/text encoders", "Taobao production features"),
))
