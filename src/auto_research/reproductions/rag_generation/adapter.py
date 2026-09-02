from ..base import EvaluationTier, OnlineABEvidence, PaperMetadata, ReproductionAdapter, ReproductionFidelity
from ..registry import register
from .experiment import reproduce_rag_generation
from .report import render

ADAPTER = register(ReproductionAdapter(
    key='rag-generation',
    paper=PaperMetadata(
        arxiv_id='2606.25496', title='Recommendation as Generation: Unifying Personalized Video Generation and Recommendation at Industrial Scale', url="https://arxiv.org/abs/2606.25496",
        track="recommendation", organization='Kuaishou / Beihang University', published='2026-06-24', topics=('generative-recommendation', 'semantic-id', 'video-generation'),
        online_ab=(OnlineABEvidence('Kuaishou advertising', 'Ad Revenue vs GRM', 1.87, 'large-scale production A/B test',
            source_url="https://arxiv.org/html/2606.25496v1", source_location='Section 4.1, Table 1', retrieved_at="2026-09-02"),),
    ),
    run=reproduce_rag_generation, render=render, fidelity=ReproductionFidelity.CORE_MECHANISM,
    omitted_core_components=('video generation agents', 'instruction model', 'cross-domain reward service'), evaluation_tier=EvaluationTier.PUBLIC_DATASET,
    datasets=("MovieLens 100K",), baseline='fixed-catalog generative recommendation', metrics=('hit_at_10', 'ndcg_at_10', 'sid_levels', 'sid_width'),
    evolve_operators=('head:disentangled-sid',), default_seeds=(42, 43, 44),
    budget="220 users / 360 items; validation-only blend selection", device_capabilities=("cpu",), infer_device_capabilities=False,
))
