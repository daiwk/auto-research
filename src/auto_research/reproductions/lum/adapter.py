from ..base import OnlineABEvidence, PaperMetadata, ReproductionAdapter, ReproductionFidelity
from ..registry import register
from .experiment import reproduce_lum
from .report import render_report


register(ReproductionAdapter(
    key="lum",
    paper=PaperMetadata(
        arxiv_id="2502.08309", title="Unlocking Scaling Law in Industrial Recommendation Systems with a Three-step Paradigm based Large User Model",
        url="https://arxiv.org/abs/2502.08309", track="recommendation", organization="Alibaba", published="2025-02",
        topics=("large user model", "generative pretraining", "knowledge querying", "CTR"),
        online_ab=(
            OnlineABEvidence("Taobao sponsored search", "CTR", 2.9, "production A/B"),
            OnlineABEvidence("Taobao sponsored search", "RPM", 1.2, "production A/B"),
        ),
    ), run=reproduce_lum, render=render_report,
    fidelity=ReproductionFidelity.FULL_PIPELINE,
    omitted_core_components=("7B scaling study", "Taobao scenario/search conditions", "production pre-trigger service"),
))
