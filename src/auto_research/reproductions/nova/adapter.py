from ..base import OnlineABEvidence, PaperMetadata, ReproductionAdapter, ReproductionFidelity
from ..registry import register
from ..industrial_2026 import render_standard
from .experiment import reproduce_nova

ADAPTER = register(ReproductionAdapter(
    key="nova", paper=PaperMetadata(
        arxiv_id="2606.27243", title="NOVA: A Verification-Aware Agent Harness for Architecture Evolution in Industrial Recommender Systems",
        url="https://arxiv.org/abs/2606.27243", track="recommendation",
        organization="Tencent", published="2026-06-25",
        topics=("auto-research", "architecture-evolution", "verification"),
        online_ab=(
            OnlineABEvidence("Tencent advertising", "GMV objective 1", 1.25, "online A/B"),
            OnlineABEvidence("Tencent advertising", "GMV objective 2", 1.70, "online A/B"),
            OnlineABEvidence("Tencent advertising", "GMV objective 3", 2.02, "online A/B"),
        ),
    ), run=reproduce_nova, render=render_standard,
    fidelity=ReproductionFidelity.CORE_MECHANISM,
    omitted_core_components=("Tencent production code agents and advertising features", "L4 online deployment control"),
))
