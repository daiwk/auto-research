from ..base import EvaluationTier, OnlineABEvidence, PaperMetadata, ReproductionAdapter, ReproductionFidelity
from ..registry import register
from .experiment import reproduce_uniformer
from .report import render

ADAPTER = register(ReproductionAdapter(
    key='uniformer',
    paper=PaperMetadata(
        arxiv_id='2606.27058', title='UniFormer: Efficient and Unified Model-Centric Scaling for Industrial Recommendation', url="https://arxiv.org/abs/2606.27058",
        track="recommendation", organization='Kuaishou', published='2026-06-25', topics=('ranking', 'feature-tokenization', 'multi-task'),
        online_ab=(OnlineABEvidence('Kuaishou Lite', 'Watch Time', 1.113, 'seven-day test; 5% production traffic',
            source_url="https://arxiv.org/html/2606.27058v1", source_location='Section 5.6, Table 2', retrieved_at="2026-09-02"),),
    ),
    run=reproduce_uniformer, render=render, fidelity=ReproductionFidelity.CORE_MECHANISM,
    omitted_core_components=('512-candidate production scorer', 'industrial feature schema', 'distributed serving'), evaluation_tier=EvaluationTier.PUBLIC_DATASET,
    datasets=("MovieLens 100K",), baseline='single-space feature interaction', metrics=('hit_at_10', 'ndcg_at_10', 'feature_spaces', 'task_tokens'),
    evolve_operators=('context:unified-token',), default_seeds=(42, 43, 44),
    budget="220 users / 360 items; validation-only blend selection", device_capabilities=("cpu",), infer_device_capabilities=False,
))
