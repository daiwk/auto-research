from ..base import OnlineABEvidence, PaperMetadata, ReproductionAdapter, ReproductionFidelity
from ..industrial_2026 import render_standard
from ..registry import register
from .experiment import reproduce_podcast_mtl


ADAPTER = register(ReproductionAdapter(
    key="podcast-mtl",
    paper=PaperMetadata(
        arxiv_id="2601.02306",
        title="Cold-Starting Podcast Ads and Promotions with Multi-Task Learning on Spotify",
        url="https://arxiv.org/abs/2601.02306", track="recommendation",
        organization="Spotify", published="2026-01-05",
        topics=("cold-start", "multi-task", "ads"),
        online_ab=(
            OnlineABEvidence("Spotify podcast ads", "effective cost per stream", -22.0, "online A/B"),
            OnlineABEvidence("Spotify podcast promotions", "stream rate", 24.0, "online A/B, upper reported lift"),
        ),
    ),
    run=reproduce_podcast_mtl, render=render_standard,
    fidelity=ReproductionFidelity.CORE_MECHANISM,
    omitted_core_components=("private Spotify ad/promotion logs", "production imbalance and gradient-balancing stack"),
))
