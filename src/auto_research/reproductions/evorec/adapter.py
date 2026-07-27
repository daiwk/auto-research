from ..base import OnlineABEvidence, PaperMetadata, ReproductionAdapter, ReproductionFidelity
from ..registry import register
from ..industrial_2026 import render_standard
from .experiment import reproduce_evorec

ADAPTER = register(ReproductionAdapter(
    key="evorec", paper=PaperMetadata(
        arxiv_id="2606.28368", title="EvoRec: Self-Evolving Agentic Recommender Systems",
        url="https://arxiv.org/abs/2606.28368", track="recommendation",
        organization="Alibaba International Digital Commerce Group", published="2026-06-15",
        topics=("auto-research", "agent", "skill-evolution"),
        online_ab=(
            OnlineABEvidence("Alibaba international recommendation", "Revenue", 1.85, "online A/B"),
            OnlineABEvidence("Alibaba international recommendation", "CTR", 1.02, "online A/B"),
        ),
    ), run=reproduce_evorec, render=render_standard,
    fidelity=ReproductionFidelity.CORE_MECHANISM,
    omitted_core_components=("production multi-agent toolchain", "private industrial dataset"),
))
