from ..base import OnlineABEvidence, PaperMetadata, ReproductionAdapter, ReproductionFidelity
from ..registry import register
from .experiment import reproduce_barge
from .report import render


ADAPTER = register(ReproductionAdapter(
    key="barge",
    paper=PaperMetadata(
        arxiv_id="2607.21028",
        title="Bridging the Structural Gap: Adapting Autoregressive Generation for Recommendation",
        url="https://arxiv.org/abs/2607.21028",
        track="recommendation",
        organization="Tencent",
        published="2026-07-23",
        topics=("generative-recommendation", "semantic-id", "reranking"),
        online_ab=(
            OnlineABEvidence("Tencent commercial media platform", "CTR", 0.60, "online A/B"),
            OnlineABEvidence("Tencent commercial media platform", "click UV", 1.34, "online A/B"),
            OnlineABEvidence("Tencent commercial media platform", "total reading time", 1.70, "online A/B"),
        ),
    ),
    run=reproduce_barge,
    render=render,
    fidelity=ReproductionFidelity.CORE_MECHANISM,
    omitted_core_components=(
        "private Tencent item embeddings and behavior logs",
        "production beam-search kernels and impressed-but-unclicked negatives",
        "full-scale learned OSQ-VAE and serving stack",
    ),
))
