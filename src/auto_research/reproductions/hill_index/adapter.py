from ..base import (
    EvaluationTier,
    OnlineABEvidence,
    PaperMetadata,
    ReproductionAdapter,
    ReproductionFidelity,
)
from ..registry import register
from .experiment import reproduce_hill_index
from .report import render


ADAPTER = register(
    ReproductionAdapter(
        key="hill-index",
        paper=PaperMetadata(
            arxiv_id="2604.12965",
            title="Efficient Retrieval Scaling with Hierarchical Indexing for Large Scale Recommendation",
            url="https://arxiv.org/abs/2604.12965",
            track="recommendation",
            organization="Meta / Facebook and Instagram Ads",
            published="2026-04-14",
            publication_label="EDBT 2026 / arXiv 2604.12965",
            topics=(
                "retrieval",
                "hierarchical-index",
                "residual-quantization",
                "test-time-training",
                "serving",
            ),
            online_ab=(
                OnlineABEvidence(
                    "Meta Ads Retrieval",
                    "online ads metric",
                    2.57,
                    "production online A/B: 2-layer MoNN Large/Small versus MoNN Small",
                    source_url="https://arxiv.org/html/2604.12965v1#S4.SS5",
                    source_location="Section 4.5, Table 8",
                    retrieved_at="2026-09-01",
                ),
            ),
        ),
        run=reproduce_hill_index,
        render=render,
        fidelity=ReproductionFidelity.CORE_MECHANISM,
        omitted_core_components=(
            "Meta MoNN production model",
            "distributed FAISS EM",
            "Facebook and Instagram Ads logs",
        ),
        evaluation_tier=EvaluationTier.PUBLIC_DATASET,
        datasets=("MovieLens 100K (220 users / 360 items)",),
        baseline="one-layer learned index with the same public item features and retrieval protocol",
        metrics=("hit_at_10", "ndcg_at_10", "head_share_at_10", "mean_scored_items"),
        evolve_operators=("rankmixer_hill_index",),
        default_seeds=(42, 43, 44),
        budget="6 coarse nodes; up to 6 residual child nodes per parent",
        device_capabilities=("cpu", "mps", "cuda"),
    )
)
