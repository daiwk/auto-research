from ..base import OnlineABEvidence, PaperMetadata, ReproductionAdapter, ReproductionFidelity
from ..registry import register
from .experiment import reproduce_nontp
from .report import render


ADAPTER = register(
    ReproductionAdapter(
        key="nontp",
        paper=PaperMetadata(
            arxiv_id="2607.12277",
            title="Not Only NTP: Extending Training Signal Coverage for Generative Recommendation",
            url="https://arxiv.org/abs/2607.12277",
            track="recommendation",
            organization="Meituan",
            published="2026-07-14",
            topics=("generative-recommendation", "contrastive-learning", "multi-domain"),
            online_ab=(
                OnlineABEvidence("Meituan DSP recall", "CTR", 1.8, "5% traffic each, 14 days, p<0.01"),
                OnlineABEvidence("Meituan DSP recall", "GMV", 2.1, "5% traffic each, 14 days, p<0.01"),
            ),
        ),
        run=reproduce_nontp,
        render=render,
        fidelity=ReproductionFidelity.CORE_MECHANISM,
        omitted_core_components=(
            "HSTU backbone and 3.2M-item Amazon Movie-Book-CDs preprocessing",
            "38.3M-user Meituan multi-business logs and full-ranking serving stack",
        ),
    )
)
