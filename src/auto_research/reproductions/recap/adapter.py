from ..base import OnlineABEvidence, PaperMetadata, ReproductionAdapter, ReproductionFidelity
from ..industrial_2026 import render_standard
from ..registry import register
from .experiment import reproduce_recap


ADAPTER = register(ReproductionAdapter(
    key="recap",
    paper=PaperMetadata(
        arxiv_id="2607.15730", title="RECAP: Feedback-Driven Streaming Semantic User Profiles for Short-Video Recommendation",
        url="https://arxiv.org/abs/2607.15730", track="recommendation", organization="Kuaishou Technology / USTC", published="2026-07-17",
        topics=("llm-recommendation", "semantic-profile", "grpo"),
        online_ab=(OnlineABEvidence("Kuaishou short-video recommendation", "average application usage time per user", 0.139, "7-day online A/B; statistically significant"),),
    ),
    run=reproduce_recap, render=render_standard,
    fidelity=ReproductionFidelity.CORE_MECHANISM,
    omitted_core_components=("production natural-language profiles", "industrial LLM judge and generator scale", "private short-video logs"),
))
