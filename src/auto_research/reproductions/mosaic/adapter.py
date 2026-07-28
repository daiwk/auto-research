from ..base import OnlineABEvidence, PaperMetadata, ReproductionAdapter, ReproductionFidelity
from ..registry import register
from .experiment import reproduce_mosaic
from .report import render


ADAPTER = register(
    ReproductionAdapter(
        key="mosaic",
        paper=PaperMetadata(
            arxiv_id="2607.24015",
            title="Mosaic: A Fleet of User Embedding Specialists for Recommendation at Meta",
            url="https://arxiv.org/abs/2607.24015",
            track="recommendation",
            organization="Meta",
            published="2026-07-27",
            topics=(
                "user-embedding",
                "multi-task-learning",
                "sequential-recommendation",
                "mixture-of-experts",
            ),
            online_ab=(
                OnlineABEvidence("Meta Surface 1", "topline engagement", 0.10, "production A/B"),
                OnlineABEvidence("Meta Surface 2", "topline engagement", 0.15, "production A/B"),
                OnlineABEvidence("Meta Surface 3", "topline engagement", 0.28, "production A/B"),
            ),
        ),
        run=reproduce_mosaic,
        render=render,
        fidelity=ReproductionFidelity.CORE_MECHANISM,
        omitted_core_components=(
            "Meta private multi-surface features and labels",
            "HSTU-2048 specialists and production-scale CoTrain",
            "CoEval, zero-out evaluation, AOTI and hybrid serving",
        ),
    )
)
