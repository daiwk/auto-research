from ..base import OnlineABEvidence, PaperMetadata, ReproductionAdapter, ReproductionFidelity
from ..registry import register
from ..industrial_2026 import render_standard
from .experiment import reproduce_idproxy

ADAPTER = register(ReproductionAdapter(
    key="idproxy", paper=PaperMetadata(
        arxiv_id="2603.01590", title="IDProxy: Cold-Start CTR Prediction for Ads and Recommendation at Xiaohongshu with Multimodal LLMs",
        url="https://arxiv.org/abs/2603.01590", track="recommendation",
        organization="Xiaohongshu / Shanghai Jiao Tong University / Fudan University", published="2026-03-02",
        topics=("multimodal-llm", "id-alignment", "ranking"),
        online_ab=(
            OnlineABEvidence("Xiaohongshu content feed", "Engagement", 0.50, "online A/B"),
            OnlineABEvidence("Xiaohongshu ads", "ADVV", 1.93, "online A/B"),
        ),
    ), run=reproduce_idproxy, render=render_standard,
    fidelity=ReproductionFidelity.CORE_MECHANISM,
    omitted_core_components=("InternVL checkpoint", "private image/text and advertising features"),
))
