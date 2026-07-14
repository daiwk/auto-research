from ..base import OnlineABEvidence, PaperMetadata, ReproductionAdapter, ReproductionFidelity
from ..registry import register
from .experiment import reproduce_onerec_v2
from .report import render

ADAPTER = register(ReproductionAdapter(
    key="onerec-v2",
    paper=PaperMetadata(
        arxiv_id="2508.20900", title="OneRec-V2 Technical Report",
        url="https://arxiv.org/abs/2508.20900", track="recommendation",
        organization="Kuaishou", published="2025-08",
        topics=("llm-recommendation", "generative-retrieval", "reinforcement-learning"),
        online_ab=(
            OnlineABEvidence("Kuaishou", "app stay time", 0.467, "5% traffic, one week"),
            OnlineABEvidence("Kuaishou Lite", "app stay time", 0.741, "5% traffic, one week"),
        ),
    ),
    run=reproduce_onerec_v2, render=render,
    fidelity=ReproductionFidelity.FULL_PIPELINE,
))
