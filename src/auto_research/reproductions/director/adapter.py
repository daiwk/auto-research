from ..base import EvaluationTier, OnlineABEvidence, PaperMetadata, ReproductionAdapter, ReproductionFidelity
from ..registry import register
from .experiment import reproduce_director
from .report import render


ADAPTER = register(
    ReproductionAdapter(
        key="director",
        paper=PaperMetadata(
            arxiv_id="2607.26418",
            title="DIRECTOR: Dynamic Index-based Recommendation with Transport-Optimized Retrieval",
            url="https://arxiv.org/abs/2607.26418",
            track="recommendation",
            organization="University of Science and Technology of China",
            published="2026-07-29",
            topics=("reranking", "dynamic-index", "optimal-transport", "non-autoregressive"),
            online_ab=(
                OnlineABEvidence(
                    "Kuaishou main application",
                    "Valid View",
                    0.519,
                    "7-day test; two mutually exclusive 10% buckets",
                    source_url="https://arxiv.org/html/2607.26418v1",
                    source_location="Section 6.2 and Appendix online protocol, Table 4",
                    significance="p < 0.05; 95% CI [0.45%, 0.59%]",
                    retrieved_at="2026-09-01",
                ),
            ),
        ),
        run=reproduce_director,
        render=render,
        fidelity=ReproductionFidelity.CORE_MECHANISM,
        omitted_core_components=("CVAE/DIFF production generators", "opaque listwise evaluator", "20K-QPS serving stack"),
        evaluation_tier=EvaluationTier.PUBLIC_DATASET,
        datasets=("MovieLens 100K",),
        baseline="independent position-wise dynamic-index retrieval",
        metrics=("hit_at_10", "ndcg_at_10", "matched_duplicate_count", "transport_row_error"),
        evolve_operators=("head:transport-index",),
        default_seeds=(42, 43, 44),
        budget="220 users / 360 items; six parallel positions",
        device_capabilities=("cpu",),
    )
)
