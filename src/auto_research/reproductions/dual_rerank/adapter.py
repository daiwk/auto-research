from ..base import OnlineABEvidence, PaperMetadata, ReproductionAdapter, ReproductionFidelity
from ..registry import register
from .experiment import reproduce
from .report import render

ADAPTER = register(ReproductionAdapter(
    key="dual-rerank", paper=PaperMetadata(
        arxiv_id="2604.07420", title="Dual-Rerank: Fusing Sequential Dependencies and Utility for Generative Reranking",
        url="https://arxiv.org/abs/2604.07420", track="recommendation", organization="Kuaishou Technology",
        published="2026-04-08", topics=("reranking", "knowledge-distillation", "listwise-rl", "serving"),
        online_ab=(OnlineABEvidence("Kuaishou Search", "Long View", 1.107, "5% traffic, one month"),),
    ), run=reproduce, render=render, fidelity=ReproductionFidelity.CORE_MECHANISM,
    omitted_core_components=("production AR teacher", "high-throughput NAR inference kernel"),
))
