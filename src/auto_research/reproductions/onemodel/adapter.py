from ..base import EvaluationTier, OnlineABEvidence, PaperMetadata, ReproductionAdapter, ReproductionFidelity
from ..registry import register
from .experiment import reproduce_onemodel
from .report import render


ADAPTER = register(ReproductionAdapter(
    key="onemodel",
    paper=PaperMetadata(
        arxiv_id="2608.18606", title="OneModel: A Unified Foundation for Platform-Scale Multi-Scenario Ranking",
        url="https://arxiv.org/abs/2608.18606", track="recommendation",
        organization="Xiaohongshu", published="2026-08-19",
        topics=("ranking", "multi-scenario", "foundation-model", "long-sequence"),
        online_ab=(
            OnlineABEvidence("Xiaohongshu Explore Feed", "time spent", 0.33, "production A/B", source_url="https://arxiv.org/html/2608.18606v1#S5.SS3", source_location="Section 5.3 Table 4", retrieved_at="2026-08-24"),
            OnlineABEvidence("Xiaohongshu Feed Ads", "advertising value", 3.43, "production A/B", source_url="https://arxiv.org/html/2608.18606v1#S5.SS3", source_location="Section 5.3 Table 4", retrieved_at="2026-08-24"),
            OnlineABEvidence("Xiaohongshu Merchant Recommendation", "DGMV", 1.1867, "production A/B", source_url="https://arxiv.org/html/2608.18606v1#S5.SS3", source_location="Section 5.3 Table 4", retrieved_at="2026-08-24"),
        ),
    ),
    run=reproduce_onemodel, render=render, fidelity=ReproductionFidelity.CORE_MECHANISM,
    omitted_core_components=("Xiaohongshu private multi-stream logs", "production unified decoder and serving stack"),
    evaluation_tier=EvaluationTier.PUBLIC_DATASET, datasets=("MovieLens-1M",),
    baseline="shared global sequential ranker", metrics=("Hit@10", "NDCG@10", "head share@10"),
    device_capabilities=("cpu",), infer_device_capabilities=False,
))
