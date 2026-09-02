from ..base import EvaluationTier, OnlineABEvidence, PaperMetadata, ReproductionAdapter, ReproductionFidelity
from ..registry import register
from .experiment import reproduce_onerank
from .report import render

ADAPTER = register(ReproductionAdapter(
    key='onerank',
    paper=PaperMetadata(
        arxiv_id='2606.16838', title='OneRank: Unified Transformer-Native Ranking Architecture for Multi-Task Recommendation', url="https://arxiv.org/abs/2606.16838",
        track="recommendation", organization='Renmin University of China', published='2026-06-15', topics=('ranking', 'multi-task', 'transformer'),
        online_ab=(OnlineABEvidence('Shopee personalized ranking', 'GMV per user', 1.01, 'seven-day test; 10% treatment and 10% control',
            source_url="https://arxiv.org/html/2606.16838v1", source_location='Section 4.5, Table 3', retrieved_at="2026-09-02"),),
    ),
    run=reproduce_onerank, render=render, fidelity=ReproductionFidelity.CORE_MECHANISM,
    omitted_core_components=('Shopee feature schema', 'production multi-stage score fusion', 'large-scale training'), evaluation_tier=EvaluationTier.PUBLIC_DATASET,
    datasets=("MovieLens 100K",), baseline='Transformer encoder plus separate task predictor', metrics=('hit_at_10', 'ndcg_at_10', 'task_private_channels', 'gradient_detach_boundaries'),
    evolve_operators=('head:unified-ranker',), default_seeds=(42, 43, 44),
    budget="220 users / 360 items; validation-only blend selection", device_capabilities=("cpu",), infer_device_capabilities=False,
))
