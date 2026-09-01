from ..base import EvaluationTier, OnlineABEvidence, PaperMetadata, ReproductionAdapter, ReproductionFidelity
from ..registry import register
from .experiment import reproduce_elise
from .report import render

ADAPTER = register(ReproductionAdapter(
    key='elise',
    paper=PaperMetadata(
        arxiv_id='2607.10239', title='Multilingual Semantic Retrieval for Apple Music Search', url="https://arxiv.org/abs/2607.10239",
        track="recommendation", organization='Apple', published='2026-07-11', topics=('search', 'multilingual-retrieval', 'score-calibration'),
        online_ab=(OnlineABEvidence('Apple Music worldwide search', 'Conversion Rate', 2.28, '18-day test; 10% treatment and 10% control',
            source_url="https://arxiv.org/html/2607.10239v1", source_location='Section 7.2, Table 8', retrieved_at="2026-09-02"),),
    ),
    run=reproduce_elise, render=render, fidelity=ReproductionFidelity.CORE_MECHANISM,
    omitted_core_components=('GTE multilingual checkpoint fine-tuning', 'Apple catalog annotations', 'global storefront serving'), evaluation_tier=EvaluationTier.PUBLIC_DATASET,
    datasets=("MovieLens 100K",), baseline='lexical/token-index retrieval', metrics=('hit_at_10', 'ndcg_at_10', 'retrieval_sources', 'quantile_matched'),
    evolve_operators=('context:quantile-fusion',), default_seeds=(42, 43, 44),
    budget="220 users / 360 items; validation-only blend selection", device_capabilities=("cpu",), infer_device_capabilities=False,
))
