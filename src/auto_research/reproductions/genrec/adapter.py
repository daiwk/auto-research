from ..base import OnlineABEvidence, PaperMetadata, ReproductionAdapter, ReproductionFidelity
from ..registry import register
from ..industrial_2026 import render_standard
from .experiment import reproduce_genrec

ADAPTER = register(ReproductionAdapter(
    key="genrec", paper=PaperMetadata(
        arxiv_id="2604.14878", title="GenRec: A Preference-Oriented Generative Framework for Large-Scale Recommendation",
        url="https://arxiv.org/abs/2604.14878", track="recommendation",
        organization="JD.com", published="2026-04-16",
        topics=("generative-recommendation", "grpo", "page-wise"),
        online_ab=(
            OnlineABEvidence("JD recommendation", "Clicks", 9.5, "online A/B"),
            OnlineABEvidence("JD recommendation", "Transactions", 8.7, "online A/B"),
        ),
    ), run=reproduce_genrec, render=render_standard,
    fidelity=ReproductionFidelity.CORE_MECHANISM,
    omitted_core_components=("JD private page logs", "production LLM and online RL stack"),
))
