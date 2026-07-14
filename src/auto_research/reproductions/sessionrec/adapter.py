from ..base import OnlineABEvidence, PaperMetadata, ReproductionAdapter, ReproductionFidelity
from ..registry import register
from .experiment import reproduce_sessionrec
from .report import render_report


register(ReproductionAdapter(
    key="sessionrec",
    paper=PaperMetadata(
        arxiv_id="2502.10157",
        title="SessionRec: Next Session Prediction Paradigm For Generative Sequential Recommendation",
        url="https://arxiv.org/abs/2502.10157",
        track="recommendation",
        organization="Meituan",
        published="2025-02",
        topics=("session recommendation", "generative retrieval"),
        online_ab=(
            OnlineABEvidence("Meituan homepage", "Pay PV", 0.603, "7 days"),
            OnlineABEvidence("Meituan homepage", "PVCTCVR", 0.564, "7 days"),
        ),
    ),
    run=reproduce_sessionrec,
    render=render_report,
    fidelity=ReproductionFidelity.CORE_MECHANISM,
    omitted_core_components=("Meituan production features", "ANN serving"),
))
