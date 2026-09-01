from ..base import (
    EvaluationTier,
    OnlineABEvidence,
    PaperMetadata,
    ReproductionAdapter,
    ReproductionFidelity,
)
from ..registry import register
from .experiment import reproduce_incrementality
from .report import render


ADAPTER = register(
    ReproductionAdapter(
        key="incrementality",
        paper=PaperMetadata(
            arxiv_id="2608.10182",
            title="From Prediction to Incrementality: Causal Optimization for Large-Scale Targeting and Recommendation",
            url="https://arxiv.org/abs/2608.10182",
            track="recommendation",
            organization="LinkedIn",
            published="2026-08-10",
            topics=("causal-recommendation", "uplift", "bandit", "constrained-allocation"),
            online_ab=(
                OnlineABEvidence(
                    "LinkedIn Feed marketing traffic",
                    "primary long-term-value KPI",
                    7.20,
                    "online A/B test",
                    source_url="https://arxiv.org/html/2608.10182v1",
                    source_location="Section 4 online evaluation",
                    significance="p = 0.041",
                    retrieved_at="2026-09-01",
                ),
            ),
        ),
        run=reproduce_incrementality,
        render=render,
        fidelity=ReproductionFidelity.CORE_MECHANISM,
        omitted_core_components=("production Transformer DragonNet", "neural bandit service", "large-scale LP solver"),
        evaluation_tier=EvaluationTier.PUBLIC_DATASET,
        datasets=("MovieLens 100K causal targeting simulation",),
        baseline="predictive treated-outcome targeting at the same budget",
        metrics=("policy_value", "total_incremental_value", "uplift_rank_correlation"),
        evolve_operators=("reward:incrementality",),
        default_seeds=(42, 43, 44),
        budget="220 users; 30% treatment budget",
        device_capabilities=("cpu",),
    )
)
