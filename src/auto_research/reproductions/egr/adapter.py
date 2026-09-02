from ..base import EvaluationTier, OnlineABEvidence, PaperMetadata, ReproductionAdapter, ReproductionFidelity
from ..registry import register
from .experiment import reproduce_egr
from .report import render

ADAPTER = register(ReproductionAdapter(
    key='egr',
    paper=PaperMetadata(
        arxiv_id='2607.23038', title='EGR: Embedding-Native Generative Retrieval with a Shared LLM', url="https://arxiv.org/abs/2607.23038",
        track="recommendation", organization='Snap Inc.', published='2026-07-25', topics=('retrieval', 'generative-retrieval', 'shared-encoder'),
        online_ab=(OnlineABEvidence('Snap DPA', 'CVR', 2.91, 'two-week test; 10%/10% traffic split',
            source_url="https://arxiv.org/html/2607.23038v1", source_location='Section 4.5, Table 6', retrieved_at="2026-09-02"),),
    ),
    run=reproduce_egr, render=render, fidelity=ReproductionFidelity.CORE_MECHANISM,
    omitted_core_components=('shared production LLM', 'daily embedding pipeline', 'ANN serving'), evaluation_tier=EvaluationTier.PUBLIC_DATASET,
    datasets=("MovieLens 100K",), baseline='separate transition/content retrieval', metrics=('hit_at_10', 'ndcg_at_10', 'shared_encoder_passes', 'indexed_items'),
    evolve_operators=('head:embedding-native',), default_seeds=(42, 43, 44),
    budget="220 users / 360 items; validation-only blend selection", device_capabilities=("cpu",), infer_device_capabilities=False,
))
