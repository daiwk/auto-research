from ..base import EvaluationTier, OnlineABEvidence, PaperMetadata, ReproductionAdapter, ReproductionFidelity
from ..registry import register
from .experiment import reproduce_next
from .report import render


ADAPTER = register(ReproductionAdapter(
    key="next-vlm",
    paper=PaperMetadata(
        arxiv_id="2607.24789", title="NEXT: Reasoning-Driven Video Recommendation via a Vision-Language Model",
        url="https://arxiv.org/abs/2607.24789", track="recommendation",
        organization="Meta", published="2026-06-27",
        topics=("multimodal", "reasoning", "retrieval", "knowledge-graph", "vlm"),
        online_ab=(
            OnlineABEvidence("commercial short-form video platform", "watch time", 0.53, "multi-week A/B at approximately 100M users", source_url="https://arxiv.org/html/2607.24789v1#S5.SS2", source_location="Section 5.2 Table 5", experiment_duration="multiple weeks", retrieved_at="2026-08-24"),
            OnlineABEvidence("commercial short-form video platform", "distinct video exposure", 0.51, "multi-week A/B at approximately 100M users", source_url="https://arxiv.org/html/2607.24789v1#S5.SS2", source_location="Section 5.2 Table 5", experiment_duration="multiple weeks", retrieved_at="2026-08-24"),
        ),
    ),
    run=reproduce_next, render=render, fidelity=ReproductionFidelity.CORE_MECHANISM,
    omitted_core_components=("NEXT-8B VLM post-training", "Meta private short-video corpus and production injection service"),
    evaluation_tier=EvaluationTier.PUBLIC_DATASET, datasets=("MovieLens-1M",),
    baseline="multi-path transition/semantic ranker", metrics=("Hit@10", "NDCG@10"),
    device_capabilities=("cpu",), infer_device_capabilities=False,
))
