from ..base import EvaluationTier, OnlineABEvidence, PaperMetadata, ReproductionAdapter, ReproductionFidelity
from ..registry import register
from .experiment import reproduce_transx
from .report import render


ADAPTER = register(
    ReproductionAdapter(
        key="transx",
        paper=PaperMetadata(
            arxiv_id="2607.28940",
            title="TransX: Scaling Transformer-based Recommendation via Behavioral and Serving Stream Crossings",
            url="https://arxiv.org/abs/2607.28940",
            track="recommendation",
            organization="LinkedIn",
            published="2026-07-31",
            publication_label="TheWebConf 2027 / arXiv 2607.28940",
            topics=("ranking", "long-sequence", "cross-attention", "serving"),
            online_ab=(
                OnlineABEvidence(
                    "LinkedIn recommender systems",
                    "CTR",
                    6.0,
                    "large-scale online A/B test",
                    source_url="https://arxiv.org/html/2607.28940v1",
                    source_location="Abstract and Section 6",
                    significance="statistically significant for users with eligible history",
                    retrieved_at="2026-09-01",
                ),
            ),
        ),
        run=reproduce_transx,
        render=render,
        fidelity=ReproductionFidelity.CORE_MECHANISM,
        omitted_core_components=("LinkedIn nearline Kafka pipeline", "distributed KV cache", "production candidate tower"),
        evaluation_tier=EvaluationTier.PUBLIC_DATASET,
        datasets=("MovieLens 100K",),
        baseline="monolithic recent-sequence scorer",
        metrics=("hit_at_10", "ndcg_at_10", "attention_pair_reduction"),
        evolve_operators=("context:transx-cross-stream",),
        default_seeds=(42, 43, 44),
        budget="220 users / 360 items; global token plus 8 cached local tokens",
        device_capabilities=("cpu",),
    )
)
