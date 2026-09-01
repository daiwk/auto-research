from ..base import EvaluationTier, OnlineABEvidence, PaperMetadata, ReproductionAdapter, ReproductionFidelity
from ..registry import register
from .experiment import reproduce_psg
from .report import render


ADAPTER = register(
    ReproductionAdapter(
        key="psg",
        paper=PaperMetadata(
            arxiv_id="2607.26427",
            title="PSG: Pair-Space Generation for Efficient Generative Reranking",
            url="https://arxiv.org/abs/2607.26427",
            track="recommendation",
            organization="Kuaishou Technology",
            published="2026-07-29",
            topics=("reranking", "generative-recommendation", "pair-token", "serving"),
            online_ab=(
                OnlineABEvidence(
                    "Kuaishou single-column feed",
                    "Stay Time per user",
                    0.178,
                    "7-day test; two disjoint 10% traffic buckets",
                    source_url="https://arxiv.org/html/2607.26427v1",
                    source_location="Section 5 online A/B test, Table 8",
                    retrieved_at="2026-09-01",
                ),
            ),
        ),
        run=reproduce_psg,
        render=render,
        fidelity=ReproductionFidelity.CORE_MECHANISM,
        omitted_core_components=("pretrained pair-token module on exposure logs", "GoalRank evaluator", "production beam service"),
        evaluation_tier=EvaluationTier.PUBLIC_DATASET,
        datasets=("MovieLens 100K",),
        baseline="item-space autoregressive scorer",
        metrics=("hit_at_10", "ndcg_at_10", "decode_step_reduction", "duplicate_items"),
        evolve_operators=("head:pair-space",),
        default_seeds=(42, 43, 44),
        budget="220 users / 360 items; six-item slate",
        device_capabilities=("cpu",),
    )
)
