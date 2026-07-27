from ..base import OnlineABEvidence, PaperMetadata, ReproductionAdapter, ReproductionFidelity
from ..industrial_2026 import render_standard
from ..registry import register
from .experiment import reproduce_pinclip


ADAPTER = register(ReproductionAdapter(
    key="pinclip",
    paper=PaperMetadata(
        arxiv_id="2603.03544",
        title="PinCLIP: Large-scale Foundational Multimodal Representation at Pinterest",
        url="https://arxiv.org/abs/2603.03544", track="recommendation",
        organization="Pinterest", published="2026-03-03",
        topics=("multimodal", "contrastive-learning", "cold-start"),
        online_ab=(
            OnlineABEvidence("Pinterest organic fresh content", "Repin", 15.0, "online A/B"),
            OnlineABEvidence("Pinterest new Ads", "clicks", 8.7, "online A/B"),
        ),
    ),
    run=reproduce_pinclip, render=render_standard,
    fidelity=ReproductionFidelity.CORE_MECHANISM,
    omitted_core_components=("VLM backbone and image pixels", "Pinterest Pin-Board production graph"),
))
