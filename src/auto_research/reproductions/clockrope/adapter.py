from ..base import EvaluationTier, OnlineABEvidence, PaperMetadata, ReproductionAdapter, ReproductionFidelity
from ..registry import register
from .experiment import reproduce_clockrope
from .report import render


ADAPTER = register(ReproductionAdapter(
    key="clockrope",
    paper=PaperMetadata(
        arxiv_id="2607.26369", title="ClockRoPE: Random Fourier Rotations for Temporal Routine Modeling",
        url="https://arxiv.org/abs/2607.26369", track="recommendation",
        organization="YouTube / Google DeepMind", published="2026-07-29",
        topics=("generative-retrieval", "temporal-modeling", "rope", "long-sequence"),
        online_ab=(
            OnlineABEvidence("major video platform", "engagement", 0.08, "14-day A/B; 1% traffic per variant", source_url="https://arxiv.org/html/2607.26369v2#S4.SS2", source_location="Section 4.2 Table 6", experiment_duration="14 days", retrieved_at="2026-08-24"),
            OnlineABEvidence("major video platform", "valued engagement", 0.08, "14-day A/B; 1% traffic per variant", source_url="https://arxiv.org/html/2607.26369v2#S4.SS2", source_location="Section 4.2 Table 6", experiment_duration="14 days", retrieved_at="2026-08-24"),
        ),
    ),
    run=reproduce_clockrope, render=render, fidelity=ReproductionFidelity.CORE_MECHANISM,
    omitted_core_components=("YouTube private timestamped logs", "production generative retrieval stack"),
    evaluation_tier=EvaluationTier.PUBLIC_DATASET, datasets=("MovieLens-100K",),
    baseline="RoPE-style recency ranker", metrics=("Hit@10", "NDCG@10"),
    device_capabilities=("cpu",), infer_device_capabilities=False,
))
