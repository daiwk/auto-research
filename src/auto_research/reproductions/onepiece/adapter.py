from ..base import OnlineABEvidence, PaperMetadata, ReproductionAdapter, ReproductionFidelity
from ..registry import register
from .experiment import reproduce
from .report import render

ADAPTER = register(ReproductionAdapter(
    key="onepiece", paper=PaperMetadata(
        arxiv_id="2509.18091", title="OnePiece: Bringing Context Engineering and Reasoning to Industrial Cascade Ranking",
        url="https://arxiv.org/abs/2509.18091", track="recommendation", organization="Shopee",
        published="2025-09-22", topics=("ranking", "retrieval", "latent-reasoning", "multi-task"),
        online_ab=(OnlineABEvidence("Shopee", "Advertising Revenue", 2.90, "production A/B"),),
    ), run=reproduce, render=render, fidelity=ReproductionFidelity.CORE_MECHANISM,
    omitted_core_components=("Shopee private user feedback chains", "production cascade"),
))
