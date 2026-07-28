from ..base import (
    OnlineABEvidence,
    PaperMetadata,
    ReproductionAdapter,
    ReproductionFidelity,
)
from ..registry import register
from .experiment import reproduce_adaf2m2
from .report import render

ADAPTER = register(
    ReproductionAdapter(
        key="adaf2m2",
        paper=PaperMetadata(
            arxiv_id="2501.15816",
            title="AdaF²M²: Comprehensive Learning and Responsive Leveraging Features in Recommendation System",
            url="https://arxiv.org/abs/2501.15816",
            track="recommendation",
            organization="ByteDance / Douyin",
            published="2025-01-27",
            topics=(
                "ranking",
                "feature-masking",
                "state-aware-adapter",
                "multi-forward",
            ),
            online_ab=(
                OnlineABEvidence(
                    "Douyin", "cumulative active days", 1.37, "production A/B"
                ),
                OnlineABEvidence("Douyin", "app duration", 1.89, "production A/B"),
            ),
        ),
        run=reproduce_adaf2m2,
        render=render,
        fidelity=ReproductionFidelity.CORE_MECHANISM,
        omitted_core_components=(
            "Douyin private features",
            "production retrieval/ranking/cold-start stack",
        ),
    )
)
