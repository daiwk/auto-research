from ..base import (
    EvaluationTier,
    OnlineABEvidence,
    PaperMetadata,
    ReproductionAdapter,
    ReproductionFidelity,
)
from ..registry import register
from .experiment import reproduce_scalr
from .report import render


ADAPTER = register(
    ReproductionAdapter(
        key="scalr",
        paper=PaperMetadata(
            arxiv_id="2606.00282",
            title="Synthetic Data from Cross-Domain Events for Large-Scale Recommendation Systems",
            url="https://arxiv.org/abs/2606.00282",
            track="recommendation",
            organization="Meta",
            published="2026-05-29",
            topics=(
                "cross-domain",
                "synthetic-data",
                "sampling",
                "conversion",
                "data-augmentation",
            ),
            online_ab=(
                OnlineABEvidence(
                    "Meta industrial recommendation platform",
                    "conversion rate",
                    0.14,
                    "live traffic over multiple weeks; paper reports a consistent +0.14% to +0.24% range",
                    source_url="https://arxiv.org/html/2606.00282v1#S5.SS2",
                    source_location="Section 5.2",
                    experiment_duration="multiple weeks",
                    significance="statistically significant",
                    retrieved_at="2026-09-01",
                ),
            ),
        ),
        run=reproduce_scalr,
        render=render,
        fidelity=ReproductionFidelity.CORE_MECHANISM,
        omitted_core_components=(
            "Meta cross-product logs",
            "production conversion model",
            "multi-source generation service",
        ),
        evaluation_tier=EvaluationTier.PUBLIC_DATASET,
        datasets=("MovieLens 100K (220 users / 360 items; genre-derived domains)",),
        baseline="deterministic top-k translation under the identical source events and candidate catalog",
        metrics=("hit_at_10", "ndcg_at_10", "head_share_at_10", "synthetic_catalog_coverage"),
        evolve_operators=("data:scalr",),
        default_seeds=(42, 43, 44),
        budget="two synthetic targets per source event",
        device_capabilities=("cpu", "mps", "cuda"),
    )
)
