from ..base import OnlineABEvidence, PaperMetadata, ReproductionAdapter, ReproductionFidelity
from ..registry import register
from .experiment import reproduce_open_web_ufm
from .report import render


ADAPTER = register(ReproductionAdapter(
    key="open-web-ufm",
    paper=PaperMetadata(
        arxiv_id="2607.28019", title="Building a User Foundation Model for the Open Web",
        url="https://arxiv.org/abs/2607.28019", track="recommendation",
        organization="Teads", published="2026-07-30",
        topics=("advertising", "user-foundation-model", "self-supervised-learning", "llm-optimizer"),
        online_ab=(
            OnlineABEvidence("Teads click-optimized RTB", "CTR", 2.13, "full traffic, 50/50 user-level split, 7 days"),
            OnlineABEvidence("Teads visit-optimized RTB", "visit rate", 2.37, "full traffic, 50/50 user-level split, 7 days"),
        ),
    ),
    run=reproduce_open_web_ufm, render=render,
    fidelity=ReproductionFidelity.CORE_MECHANISM,
    omitted_core_components=("Teads private RTB logs", "Claude Opus lifter search", "production GDCN adapter"),
))
