from ..base import OnlineABEvidence, PaperMetadata, ReproductionAdapter, ReproductionFidelity
from ..registry import register
from .experiment import reproduce_rocs
from .report import render


ADAPTER = register(ReproductionAdapter(
    key="rocs",
    paper=PaperMetadata(
        arxiv_id="2607.27744", title="ROCS: Request-Oriented Compute Sharing for Efficient Large-Scale Recommendation",
        url="https://arxiv.org/abs/2607.27744", track="recommendation",
        code_url="https://github.com/pytorch/FBGEMM/tree/main/fbgemm_gpu/experimental/ikbo",
        organization="Meta AI", published="2026-07-30",
        topics=("retrieval", "ranking", "serving", "compute-sharing"),
        online_ab=(
            OnlineABEvidence("Meta retrieval systems", "QPS", 200.0, "deployed across ads and organic surfaces"),
            OnlineABEvidence("Meta short-form video ranking", "QPS", 50.0, "production deployment; LogLoss -0.5%"),
        ),
    ),
    run=reproduce_rocs, render=render,
    fidelity=ReproductionFidelity.CORE_MECHANISM,
    omitted_core_components=("production GLM masking stack", "IKBO GPU kernel benchmark", "Meta private logs"),
))
