from ..base import EvaluationTier, OnlineABEvidence, PaperMetadata, ReproductionAdapter, ReproductionFidelity
from ..registry import register
from .experiment import reproduce_piano
from .report import render

ADAPTER = register(ReproductionAdapter(
    key='piano',
    paper=PaperMetadata(
        arxiv_id='2606.16641', title='PIANO: Personalized Reranking via Information Aggregation Node for Music Search Optimization', url="https://arxiv.org/abs/2606.16641",
        track="recommendation", organization='NetEase Cloud Music', published='2026-06-15', topics=('search', 'reranking', 'listwise'),
        online_ab=(OnlineABEvidence('NetEase Cloud Music search', 'CVR', 4.45, 'multi-week stable-bucket experiment',
            source_url="https://arxiv.org/html/2606.16641v1", source_location='Section 5.1, Table 6', retrieved_at="2026-09-02"),),
    ),
    run=reproduce_piano, render=render, fidelity=ReproductionFidelity.CORE_MECHANISM,
    omitted_core_components=('music-query logs', 'production multimodal encoders', '95%-traffic serving deployment'), evaluation_tier=EvaluationTier.PUBLIC_DATASET,
    datasets=("MovieLens 100K",), baseline='pointwise personalized reranker', metrics=('hit_at_10', 'ndcg_at_10', 'interest_refiner', 'information_nodes'),
    evolve_operators=('head:listwise-node',), default_seeds=(42, 43, 44),
    budget="220 users / 360 items; validation-only blend selection", device_capabilities=("cpu",), infer_device_capabilities=False,
))
