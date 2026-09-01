from ..base import EvaluationTier, OnlineABEvidence, PaperMetadata, ReproductionAdapter, ReproductionFidelity
from ..registry import register
from .experiment import reproduce_poem
from .report import render

ADAPTER = register(ReproductionAdapter(
    key='poem',
    paper=PaperMetadata(
        arxiv_id='2606.29946', title='POEM: Partial-Order Enhanced Real-Time Sequential Modeling for Recommendation', url="https://arxiv.org/abs/2606.29946",
        track="recommendation", organization='Kuaishou', published='2026-06-29', topics=('sequential-recommendation', 'partial-order', 'real-time'),
        online_ab=(OnlineABEvidence('Kuaishou main page', 'Usage Time per User', 0.249, 'seven-day test; 5% treatment and 5% control',
            source_url="https://arxiv.org/html/2606.29946v1", source_location='Section 4.2.3, Table 5', retrieved_at="2026-09-02"),),
    ),
    run=reproduce_poem, render=render, fidelity=ReproductionFidelity.CORE_MECHANISM,
    omitted_core_components=('real-time production ranker scores', 'Kuaiformer stack', 'short-video logs'), evaluation_tier=EvaluationTier.PUBLIC_DATASET,
    datasets=("MovieLens 100K",), baseline='chronological sequential ranking', metrics=('hit_at_10', 'ndcg_at_10', 'ranking_signals', 'partial_order_pairs'),
    evolve_operators=('context:partial-order',), default_seeds=(42, 43, 44),
    budget="220 users / 360 items; validation-only blend selection", device_capabilities=("cpu",), infer_device_capabilities=False,
))
