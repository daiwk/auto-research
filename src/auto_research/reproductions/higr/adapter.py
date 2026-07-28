from ..base import OnlineABEvidence, PaperMetadata, ReproductionAdapter, ReproductionFidelity
from ..registry import register
from .experiment import reproduce_higr
from .report import render


ADAPTER = register(ReproductionAdapter(
    key="higr",
    paper=PaperMetadata(
        arxiv_id="2512.24787",
        title="HiGR: Industrial-Scale Hierarchical Generative Slate Recommendation Framework in Tencent",
        url="https://arxiv.org/abs/2512.24787",
        track="recommendation",
        organization="Tencent",
        published="2025-12-31",
        topics=("generative-recommendation", "slate-recommendation", "semantic-id", "preference-optimization"),
        online_ab=(
            OnlineABEvidence("Tencent video", "stay time", 1.03, "5% traffic"),
            OnlineABEvidence("Tencent video", "video views", 1.73, "5% traffic"),
        ),
    ),
    run=reproduce_higr,
    render=render,
    fidelity=ReproductionFidelity.CORE_MECHANISM,
    omitted_core_components=("Tencent private video data", "production PCRQ-VAE and beam serving"),
))
