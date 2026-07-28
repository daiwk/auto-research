from ..base import OnlineABEvidence, PaperMetadata, ReproductionAdapter, ReproductionFidelity
from ..registry import register
from .experiment import reproduce
from .report import render

ADAPTER = register(ReproductionAdapter(
    key="cq-sid",
    paper=PaperMetadata(
        arxiv_id="2605.14434", title="Efficient Generative Retrieval for E-commerce Search with Semantic Cluster IDs and Expert-Guided RL",
        url="https://arxiv.org/abs/2605.14434", track="recommendation",
        organization="Alibaba Taobao & Tmall Group", published="2026-05-14",
        topics=("generative-retrieval", "semantic-id", "reinforcement-learning"),
        online_ab=(
            OnlineABEvidence("TmallAPP Search", "GMV", 1.15, "two-week online A/B"),
            OnlineABEvidence("TmallAPP Search", "UCTCVR", 0.40, "two-week online A/B"),
        ),
    ),
    run=reproduce, render=render, fidelity=ReproductionFidelity.CORE_MECHANISM,
    omitted_core_components=("64-GPU progressive LLM training", "Tmall private query logs and production beam service"),
))
