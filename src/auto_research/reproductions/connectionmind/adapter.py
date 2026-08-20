from ..base import EvaluationTier, OnlineABEvidence, PaperMetadata, ReproductionAdapter, ReproductionFidelity
from ..registry import register
from .experiment import reproduce_connectionmind
from .report import render


ADAPTER = register(ReproductionAdapter(
    key="connectionmind",
    paper=PaperMetadata(
        arxiv_id="2608.10187", title="ConnectionMind: A General Social-Personalized Recommendation System with LLM Reasoning", url="https://arxiv.org/abs/2608.10187", track="recommendation",
        organization="Michigan State University / Meta Platforms, Inc.", published="2026-08-10",
        topics=("social-recommendation", "llm-recommendation", "graph-reasoning", "reinforcement-learning", "distillation"),
        online_ab=(
            OnlineABEvidence("Meta short-video recommendation", "exposure", 0.33, "multi-week test over tens of millions of users", source_url="https://arxiv.org/pdf/2608.10187", source_location="Section 5.4 Table 2", experiment_duration="multiple weeks", significance="±0.08%", retrieved_at="2026-08-20"),
            OnlineABEvidence("Meta short-video recommendation", "watch time", 0.43, "multi-week test over tens of millions of users", source_url="https://arxiv.org/pdf/2608.10187", source_location="Section 5.4 Table 2", experiment_duration="multiple weeks", significance="±0.14%", retrieved_at="2026-08-20"),
            OnlineABEvidence("Meta short-video recommendation", "video sessions", 0.22, "multi-week test over tens of millions of users", source_url="https://arxiv.org/pdf/2608.10187", source_location="Section 5.4 Table 2", experiment_duration="multiple weeks", significance="±0.13%", retrieved_at="2026-08-20"),
        ),
    ),
    run=reproduce_connectionmind, render=render,
    fidelity=ReproductionFidelity.CORE_MECHANISM,
    omitted_core_components=("Meta private short-video graph and production serving", "Llama-3.1 3B/8B policies and production-scale GNN student"),
    evaluation_tier=EvaluationTier.PUBLIC_DATASET,
    datasets=("HetRec 2011 Delicious-2K",), baseline="fixed heterogeneous graph aggregation",
    metrics=("Recall@10", "Precision@10", "NDCG@10"), budget="3 SFT epochs + 180 GRPO groups",
    device_capabilities=("cpu",),
))
