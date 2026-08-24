from ..base import EvaluationTier, OnlineABEvidence, PaperMetadata, ReproductionAdapter, ReproductionFidelity
from ..registry import register
from .experiment import reproduce_oneshot
from .report import render


ADAPTER = register(ReproductionAdapter(
    key="oneshot-index",
    paper=PaperMetadata(
        arxiv_id="2607.27475", title="OneShot: Index-in-Ranking with Neural Scoring for Large-Scale Retrieval",
        url="https://arxiv.org/abs/2607.27475", track="recommendation",
        organization="Meta / Instagram", published="2026-07-29",
        topics=("retrieval", "learnable-index", "neural-scoring", "serving"),
        online_ab=(
            OnlineABEvidence("Instagram short video", "daily sessions", 0.035, "fully deployed to global traffic", source_url="https://arxiv.org/html/2607.27475v2#S5.SS1.SSS2", source_location="Section 5.1.2 Table 3", retrieved_at="2026-08-24"),
            OnlineABEvidence("Instagram short video", "watch time", 0.136, "fully deployed to global traffic", source_url="https://arxiv.org/html/2607.27475v2#S5.SS1.SSS2", source_location="Section 5.1.2 Table 3", retrieved_at="2026-08-24"),
        ),
    ),
    run=reproduce_oneshot, render=render, fidelity=ReproductionFidelity.CORE_MECHANISM,
    omitted_core_components=("Instagram billion-item corpus", "stochastic compositional balancing and distributed serving"),
    evaluation_tier=EvaluationTier.PUBLIC_DATASET, datasets=("MovieLens-100K",),
    baseline="two-tower dot-product retrieval", metrics=("Hit@10", "NDCG@10"),
    device_capabilities=("cpu",), infer_device_capabilities=False,
))
