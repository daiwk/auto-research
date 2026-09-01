from ..base import (
    EvaluationTier,
    OnlineABEvidence,
    PaperMetadata,
    ReproductionAdapter,
    ReproductionFidelity,
)
from ..registry import register
from .experiment import reproduce_drem
from .report import render


ADAPTER = register(
    ReproductionAdapter(
        key="drem",
        paper=PaperMetadata(
            arxiv_id="2608.12778",
            title="DrEM: Dual-Side Robust Ensemble Ranking from Noisy User Preference Predictions in Video Recommendation",
            url="https://arxiv.org/abs/2608.12778",
            track="recommendation",
            organization="Shenzhen University",
            published="2026-08-13",
            topics=("ranking", "multi-objective", "robust-learning", "video-recommendation"),
            online_ab=(
                OnlineABEvidence(
                    "industrial video recommendation",
                    "Comment",
                    1.388,
                    "7-day experiment; 5.1% main traffic per group",
                    source_url="https://arxiv.org/html/2608.12778v1",
                    source_location="Section 5.4, Table 2",
                    significance="p < 0.005",
                    retrieved_at="2026-09-01",
                ),
            ),
        ),
        run=reproduce_drem,
        render=render,
        fidelity=ReproductionFidelity.CORE_MECHANISM,
        omitted_core_components=("EMER/EASQ production backbones", "private pxtr logs"),
        evaluation_tier=EvaluationTier.PUBLIC_DATASET,
        datasets=("MovieLens 100K (proxy multi-objective channels)",),
        baseline="naive weighted pxtr fusion under the same perturbations",
        metrics=("hit_at_10", "ndcg_at_10", "naive_mean_absolute_drift", "robust_mean_absolute_drift"),
        evolve_operators=("reward:robust-preference",),
        default_seeds=(42, 43, 44),
        budget="220 users / 360 items; 24 fixed logit perturbations",
        device_capabilities=("cpu",),
    )
)
