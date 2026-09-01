from ..base import EvaluationTier, OnlineABEvidence, PaperMetadata, ReproductionAdapter, ReproductionFidelity
from ..registry import register
from .experiment import reproduce_specformer
from .report import render

ADAPTER = register(ReproductionAdapter(
    key='specformer',
    paper=PaperMetadata(
        arxiv_id='2607.24025', title='SpecFormer: Mitigating Embedding and Attention Collapse via Spectral-Aware Transformer for Recommendation', url="https://arxiv.org/abs/2607.24025",
        track="recommendation", organization='Zhejiang University', published='2026-07-27', topics=('ranking', 'transformer', 'spectral-softening'),
        online_ab=(OnlineABEvidence('Alibaba e-commerce advertising', 'CTR', 1.34, '10-day test; 10% production traffic',
            source_url="https://arxiv.org/html/2607.24025v1", source_location='Section V-F, Table V', retrieved_at="2026-09-02"),),
    ),
    run=reproduce_specformer, render=render, fidelity=ReproductionFidelity.CORE_MECHANISM,
    omitted_core_components=('97M production stack', 'distributed dynamic embeddings', 'FlashAttention serving'), evaluation_tier=EvaluationTier.PUBLIC_DATASET,
    datasets=("MovieLens 100K",), baseline='standard Transformer/DLRM-style interaction', metrics=('hit_at_10', 'ndcg_at_10', 'spectral_condition_before', 'softened_rank'),
    evolve_operators=('context:spectral-soften',), default_seeds=(42, 43, 44),
    budget="220 users / 360 items; validation-only blend selection", device_capabilities=("cpu",), infer_device_capabilities=False,
))
