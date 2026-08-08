from ..base import OnlineABEvidence, PaperMetadata, ReproductionAdapter, ReproductionFidelity
from ..registry import register
from .experiment import reproduce_dme
from .report import render

ADAPTER = register(ReproductionAdapter(
    key="dme",
    paper=PaperMetadata(
        arxiv_id="2608.02148", title="Douyin Multimodal Embedding Model Technical Report",
        url="https://arxiv.org/abs/2608.02148", track="recommendation",
        organization="ByteDance / Douyin", published="2026-08-03",
        topics=("content-understanding", "multimodal-retrieval", "embedding", "llm-recommendation"),
        online_ab=(OnlineABEvidence("Douyin Search", "Lifetime", 0.1, "online A/B test"),),
    ),
    run=reproduce_dme, render=render, fidelity=ReproductionFidelity.CORE_MECHANISM,
    omitted_core_components=("2B/9B multimodal backbone", "Douyin private multimodal corpus and billion-scale vector index"),
))
