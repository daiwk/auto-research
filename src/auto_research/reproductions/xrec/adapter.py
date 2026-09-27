from ..base import (
    EvaluationTier,
    OnlineABEvidence,
    PaperMetadata,
    ReproductionAdapter,
    ReproductionFidelity,
)
from ..registry import register
from .experiment import reproduce_xrec
from .report import render


ADAPTER = register(ReproductionAdapter(
    key="xrec",
    paper=PaperMetadata(
        arxiv_id="2609.29180",
        title="X-Rec Technical Report",
        url="https://arxiv.org/abs/2609.29180",
        track="recommendation",
        organization="TikTok (ByteDance)",
        published="2026-09-24",
        topics=("retrieval", "generative-recommendation", "flow-matching"),
        online_ab=(
            OnlineABEvidence(
                product="TikTok vertical-content recommendation",
                metric="vertical engagement",
                lift_percent=4.1484,
                traffic="two consecutive production launches (V1 then V2); paper does not disclose bucket share",
                source_url="https://arxiv.org/html/2609.29180v1",
                source_location="Section 5, Table 3",
                retrieved_at="2026-09-27",
            ),
        ),
    ),
    run=reproduce_xrec,
    render=render,
    fidelity=ReproductionFidelity.CORE_MECHANISM,
    omitted_core_components=(
        "TikTok private multi-attribute sequence features and streaming benchmark",
        "production-scale contrastive item embeddings, ANN index and cached serving",
        "online A/B deployment",
    ),
    evaluation_tier=EvaluationTier.PUBLIC_DATASET,
    datasets=("MovieLens 1M",),
    baseline="same-data two-layer U2I and trained residual-SID autoregressive decoder",
    metrics=("hit_at_10", "ndcg_at_10", "recall_at_20", "generation_requests_per_second_cpu"),
    default_seeds=(42, 43, 44),
    budget="160 shared item-vector + 200 model updates (X-Rec 160+40, SID-AR 200, U2I 200); updates matched, not FLOPs",
    device_capabilities=("cpu",),
    infer_device_capabilities=False,
))
