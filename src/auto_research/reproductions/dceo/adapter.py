from ..base import EvaluationTier, OnlineABEvidence, PaperMetadata, ReproductionAdapter, ReproductionFidelity
from ..registry import register
from .experiment import reproduce_dceo
from .report import render


ADAPTER = register(ReproductionAdapter(
    key="dceo",
    paper=PaperMetadata(
        arxiv_id="2608.25635",
        title="DCEO: Direct Causal Effect Optimization for Long-Term User Value Modeling in E-commerce Search",
        url="https://arxiv.org/abs/2608.25635",
        track="recommendation",
        organization="Taobao & Tmall Group, Alibaba",
        published="2026-08-26",
        topics=("search-ranking", "long-term-value", "causal-optimization", "multi-objective-ranking"),
        online_ab=(OnlineABEvidence(
            "Alibaba e-commerce search", "GMV", 0.36,
            "41-day production A/B test",
            source_url="https://arxiv.org/html/2608.25635v1#S5.SS7",
            source_location="Section 5.7", experiment_duration="41 days",
            retrieved_at="2026-08-28",
        ),),
    ),
    run=reproduce_dceo,
    render=render,
    fidelity=ReproductionFidelity.CORE_MECHANISM,
    omitted_core_components=("Alibaba private search logs", "production long-term GMV critic", "online serving stack"),
    evaluation_tier=EvaluationTier.PUBLIC_DATASET,
    datasets=("MovieLens-1M",),
    baseline="fixed multi-objective log fusion over the same four proxy scores",
    metrics=("Hit@10", "NDCG@10", "head share@10", "estimated relative causal effect"),
    device_capabilities=("cpu",), infer_device_capabilities=False,
))
