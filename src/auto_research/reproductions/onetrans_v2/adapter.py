from ..base import EvaluationTier, OnlineABEvidence, PaperMetadata, ReproductionAdapter, ReproductionFidelity
from ..registry import register
from .experiment import reproduce_onetrans_v2
from .report import render


ADAPTER = register(ReproductionAdapter(
    key="onetrans-v2",
    paper=PaperMetadata(
        arxiv_id="2609.28589",
        title="OneTrans-V2: Unifying Retrieval, Pre-rank, and Fine-rank with One Transformer in Industrial Recommender",
        url="https://arxiv.org/abs/2609.28589",
        track="recommendation",
        organization="ByteDance",
        published="2026-09-23",
        topics=("multi-stage-ranking", "generative-retrieval", "cross-stage-distillation"),
        online_ab=(OnlineABEvidence(
            product="industrial recommendation cascade", metric="GMV per user", lift_percent=9.74,
            traffic="user-level 50/50 randomized A/B", source_url="https://arxiv.org/html/2609.28589v1",
            source_location="Section 6.3", retrieved_at="2026-09-27",
        ),),
    ),
    run=reproduce_onetrans_v2,
    render=render,
    fidelity=ReproductionFidelity.CONCEPT_DEMO,
    omitted_core_components=(
        "real purchase, spend and sponsored-supply decision labels (MovieLens proxies only)",
        "production exposure streams, SNT amortization and online serving stack",
        "sparse MoE and production-scale item encoder",
    ),
    evaluation_tier=EvaluationTier.PUBLIC_DATASET,
    datasets=("MovieLens 1M",),
    baseline="shared three-stage mechanism; no production cascade baseline available",
    metrics=("pre_rating_ge_3_auc", "fine_rating_ge_3_auc", "sid_exact_accuracy"),
    default_seeds=(42, 43, 44),
    budget="200 shared-backbone updates, batch 64, three seeds",
    device_capabilities=("cpu",),
    infer_device_capabilities=False,
))
