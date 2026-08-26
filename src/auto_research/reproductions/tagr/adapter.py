from ..base import EvaluationTier, OnlineABEvidence, PaperMetadata, ReproductionAdapter, ReproductionFidelity
from ..registry import register
from .experiment import reproduce_tagr
from .report import render


ADAPTER = register(ReproductionAdapter(
    key="tagr",
    paper=PaperMetadata(
        arxiv_id="2608.24034",
        title="TAGR: Temporally Adaptive Generative Recommendation for Industrial Live-Streaming Advertising",
        url="https://arxiv.org/abs/2608.24034",
        track="recommendation",
        organization="Kuaishou Technology",
        published="2026-08-25",
        topics=("generative-recommendation", "live-streaming-advertising", "semantic-id", "online-rl"),
        online_ab=(
            OnlineABEvidence("Kuaishou live-stream advertising", "live-room entry rate", 8.5, "production A/B under the same downstream stack", source_url="https://arxiv.org/html/2608.24034v1#S4.SS3", source_location="Section 4.3 / Table 1", retrieved_at="2026-08-26"),
            OnlineABEvidence("Kuaishou live-stream advertising", "shopping-cart click rate", 7.4, "production A/B under the same downstream stack", source_url="https://arxiv.org/html/2608.24034v1#S4.SS3", source_location="Section 4.3 / Table 1", retrieved_at="2026-08-26"),
            OnlineABEvidence("Kuaishou live-stream advertising", "revenue", 16.1, "multi-week production experiment", source_url="https://arxiv.org/html/2608.24034v1#S4.SS3", source_location="Section 4.3 / Table 1", retrieved_at="2026-08-26"),
        ),
    ),
    run=reproduce_tagr,
    render=render,
    fidelity=ReproductionFidelity.CORE_MECHANISM,
    omitted_core_components=("Kuaishou private live-ad logs", "online reward model and GRPO training", "real-time LSID and serving engine"),
    evaluation_tier=EvaluationTier.PUBLIC_DATASET,
    datasets=("MovieLens-1M",),
    baseline="production-style first-order transition recommender",
    metrics=("Hit@10", "NDCG@10", "head share@10"),
    device_capabilities=("cpu",),
    infer_device_capabilities=False,
))
