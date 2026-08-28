from ..base import EvaluationTier, OnlineABEvidence, PaperMetadata, ReproductionAdapter, ReproductionFidelity
from ..registry import register
from .experiment import reproduce_friend_gnn
from .report import render


ADAPTER = register(ReproductionAdapter(
    key="friend-gnn",
    paper=PaperMetadata(
        arxiv_id="2608.27413",
        title="Scaling Graph Neural Networks for Friend Recommendation: Multi-Hash User Embeddings and Temporal Neighbor Sampling",
        url="https://arxiv.org/abs/2608.27413",
        track="recommendation",
        organization="AI VK",
        published="2026-08-27",
        code_url="https://github.com/makut/VK-GNN",
        topics=("friend-recommendation", "graph-ranking", "multi-hash-embedding", "temporal-sampling"),
        online_ab=(
            OnlineABEvidence("VK friend recommendation", "friend additions", 16.0, "production A/B test", source_url="https://arxiv.org/html/2608.27413v1#S6.SS6", source_location="Section 6.6", retrieved_at="2026-08-29"),
            OnlineABEvidence("VK friend recommendation", "unique friend adders", 11.5, "production A/B test", source_url="https://arxiv.org/html/2608.27413v1#S6.SS6", source_location="Section 6.6", retrieved_at="2026-08-29"),
        ),
    ),
    run=reproduce_friend_gnn,
    render=render,
    fidelity=ReproductionFidelity.CORE_MECHANISM,
    omitted_core_components=("VK private 194M-user graph", "distributed GATv2 training", "production ranker"),
    evaluation_tier=EvaluationTier.PUBLIC_DATASET,
    datasets=("MovieLens-1M",),
    baseline="popularity ranker on the identical full candidate catalog",
    metrics=("Hit@10", "NDCG@10", "hash table compression", "temporal sampling complexity"),
    device_capabilities=("cpu",), infer_device_capabilities=False,
))
