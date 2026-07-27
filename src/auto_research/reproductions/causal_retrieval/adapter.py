from ..base import OnlineABEvidence, PaperMetadata, ReproductionAdapter, ReproductionFidelity
from ..industrial_2026 import render_standard
from ..registry import register
from .experiment import reproduce_causal_retrieval


ADAPTER = register(ReproductionAdapter(
    key="causal-retrieval",
    paper=PaperMetadata(
        arxiv_id="2607.14161",
        title="Deep-learning Causal Retrieval Optimization for Efficient e-commerce Distribution in Pinterest",
        url="https://arxiv.org/abs/2607.14161", track="recommendation",
        organization="Pinterest", published="2026-07-14",
        topics=("causal-retrieval", "uplift", "candidate-generation"),
        online_ab=(
            OnlineABEvidence("Pinterest shopping retrieval", "total sessions", 0.26, "online A/B"),
            OnlineABEvidence("Pinterest shopping retrieval", "Pin saves", 1.10, "online A/B"),
        ),
    ),
    run=reproduce_causal_retrieval, render=render_standard,
    fidelity=ReproductionFidelity.CORE_MECHANISM,
    omitted_core_components=("Pinterest randomized traffic logs", "production retrieval RPC and replay system"),
))
