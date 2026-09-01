from ..base import (
    EvaluationTier,
    OnlineABEvidence,
    PaperMetadata,
    ReproductionAdapter,
    ReproductionFidelity,
)
from ..registry import register
from .experiment import reproduce_memory_layer
from .report import render


ADAPTER = register(
    ReproductionAdapter(
        key="memory-layer",
        paper=PaperMetadata(
            arxiv_id="2607.25110",
            title="Memory Layer: Train the In-Model Cache for Recommendation Models",
            url="https://arxiv.org/abs/2607.25110",
            track="recommendation",
            organization="Meta / Instagram Reels",
            published="2026-07-27",
            topics=("ranking", "training-serving-consistency", "cold-start", "cache", "serving"),
            online_ab=(
                OnlineABEvidence(
                    "Instagram Reels early-stage ranking",
                    "cold-start reshare rate",
                    5.0,
                    "post-launch A/B backtest; paper reports a statistically significant +5% to +6% range",
                    source_url="https://arxiv.org/html/2607.25110v1#S6.SS3",
                    source_location="Section 6.3, Table 1",
                    significance="all Table 1 A/B improvements statistically significant",
                    retrieved_at="2026-09-01",
                ),
                OnlineABEvidence(
                    "Instagram Reels early-stage ranking",
                    "video views for media younger than one hour",
                    6.0,
                    "post-launch A/B backtest; paper reports a +6% to +7% range",
                    source_url="https://arxiv.org/html/2607.25110v1#S6.SS3",
                    source_location="Section 6.3, Table 1",
                    significance="statistically significant",
                    retrieved_at="2026-09-01",
                ),
            ),
        ),
        run=reproduce_memory_layer,
        render=render,
        fidelity=ReproductionFidelity.CORE_MECHANISM,
        omitted_core_components=(
            "Meta MPZCH distributed storage",
            "raw embedding streaming",
            "Instagram private logs",
        ),
        evaluation_tier=EvaluationTier.PUBLIC_DATASET,
        datasets=("MovieLens 100K (220 users / 360 items)",),
        baseline="same item tower with an external early frozen cache and no always-on miss path",
        metrics=(
            "hit_at_10",
            "ndcg_at_10",
            "head_share_at_10",
            "snapshot_coverage",
            "memory_coverage",
        ),
        evolve_operators=("rankmixer_memory_layer",),
        default_seeds=(42, 43, 44),
        budget="220 users / 360 items; one chronological writeback pass",
        device_capabilities=("cpu", "mps", "cuda"),
    )
)
