from ..base import (
    EvaluationTier,
    OnlineABEvidence,
    PaperMetadata,
    ReproductionAdapter,
    ReproductionFidelity,
)
from ..registry import register
from .experiment import reproduce_semantic_native_longseq
from .report import render


ADAPTER = register(
    ReproductionAdapter(
        key="semantic-native-longseq",
        paper=PaperMetadata(
            arxiv_id="2606.07546",
            title="Beyond Item IDs: Scaling Short-Form-Video Recommendation via Semantic-Native Long Sequence Modeling",
            url="https://arxiv.org/abs/2606.07546",
            track="recommendation",
            organization="Google",
            published="2026-05-04",
            publication_label="SIGIR 2026 / arXiv 2606.07546",
            topics=(
                "long-sequence",
                "semantic-id",
                "rq-vae",
                "efficient-transformer",
                "cold-start",
            ),
            online_ab=(
                OnlineABEvidence(
                    "Google global short-video platform",
                    "actively engaged users",
                    0.52,
                    "large-scale online A/B; full SID + compressed-transformer system versus L=800 Video-ID baseline",
                    source_url="https://arxiv.org/html/2606.07546v1#S3.SS5",
                    source_location="Section 3.5, Table 4",
                    significance="p < 0.05",
                    retrieved_at="2026-09-01",
                ),
                OnlineABEvidence(
                    "Google global short-video platform",
                    "satisfied watch time",
                    1.42,
                    "large-scale online A/B; full SID + compressed-transformer system",
                    source_url="https://arxiv.org/html/2606.07546v1#S3.SS5",
                    source_location="Section 3.5, Table 4",
                    significance="p < 0.05",
                    retrieved_at="2026-09-01",
                ),
            ),
        ),
        run=reproduce_semantic_native_longseq,
        render=render,
        fidelity=ReproductionFidelity.CORE_MECHANISM,
        omitted_core_components=(
            "Google production RQ-VAE",
            "2,000-event private video histories",
            "hybrid asynchronous serving stack",
        ),
        evaluation_tier=EvaluationTier.PUBLIC_DATASET,
        datasets=("MovieLens 100K (220 users / 360 items)",),
        baseline="12-event item-ID feature attention under the same public split and full catalog",
        metrics=("hit_at_10", "ndcg_at_10", "head_share_at_10", "attention_pair_reduction"),
        evolve_operators=("rankmixer_semantic_native_longseq",),
        default_seeds=(42, 43, 44),
        budget="48 events folded by 4 into 12 local tokens plus two global queries",
        device_capabilities=("cpu", "mps", "cuda"),
    )
)
