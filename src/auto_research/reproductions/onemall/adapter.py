from ..base import OnlineABEvidence, PaperMetadata, ReproductionAdapter, ReproductionFidelity
from ..industrial_2026 import render_standard
from ..registry import register
from .experiment import reproduce_onemall


ADAPTER = register(ReproductionAdapter(
    key="onemall",
    paper=PaperMetadata(
        arxiv_id="2601.21770",
        title="OneMall: One Model, More Scenarios -- End-to-End Generative Recommender Family at Kuaishou E-Commerce",
        url="https://arxiv.org/abs/2601.21770", track="recommendation",
        organization="Kuaishou", published="2026-01-29",
        topics=("generative-recommendation", "multi-scenario", "semantic-id"),
        online_ab=(
            OnlineABEvidence("Kuaishou product-card", "GMV", 13.01, "online A/B"),
            OnlineABEvidence("Kuaishou short-video", "orders", 15.32, "online A/B"),
            OnlineABEvidence("Kuaishou live", "orders", 2.78, "online A/B"),
        ),
    ),
    run=reproduce_onemall, render=render_standard,
    fidelity=ReproductionFidelity.CORE_MECHANISM,
    omitted_core_components=("production Sparse MoE and Query-Former", "private e-commerce data and RL alignment"),
))
