from ..base import EvaluationTier, OnlineABEvidence, PaperMetadata, ReproductionAdapter, ReproductionFidelity
from ..registry import register
from .experiment import reproduce_zorro
from .report import render

ADAPTER = register(ReproductionAdapter(
    key='zorro',
    paper=PaperMetadata(
        arxiv_id='2607.10910', title='ZoRRO: A Zero-Weight Personalized Recommender System for Scalable News Recommendation', url="https://arxiv.org/abs/2607.10910",
        track="recommendation", organization='Technical University of Denmark', published='2026-07-12', topics=('news-recommendation', 'training-free', 'recency'),
        online_ab=(OnlineABEvidence('Ekstra Bladet', 'CTR', 4.19, 'six-day live test; 45% treatment traffic',
            source_url="https://arxiv.org/html/2607.10910v1", source_location='Section 4.3, Table 7', retrieved_at="2026-09-02"),),
    ),
    run=reproduce_zorro, render=render, fidelity=ReproductionFidelity.CORE_MECHANISM,
    omitted_core_components=('Ekstra Bladet live candidate service', 'publisher embeddings', 'AWS Fargate stack'), evaluation_tier=EvaluationTier.PUBLIC_DATASET,
    datasets=("MovieLens 100K",), baseline='most-popular/content-transition ranker', metrics=('hit_at_10', 'ndcg_at_10', 'trainable_parameters', 'history_items'),
    evolve_operators=('context:zero-weight',), default_seeds=(42, 43, 44),
    budget="220 users / 360 items; validation-only blend selection", device_capabilities=("cpu",), infer_device_capabilities=False,
))
