from ..base import OnlineABEvidence, PaperMetadata, ReproductionAdapter, ReproductionFidelity
from ..industrial_2026 import render_standard
from ..latest_20260729_common import reproduce_youtube_freshness
from ..registry import register


ADAPTER = register(ReproductionAdapter(
    key="youtube-freshness",
    paper=PaperMetadata(
        arxiv_id="2607.23749",
        title="Breaking the Loop: An Empirical Comparison of Strategies for Novelty and Freshness in YouTube Music",
        url="https://arxiv.org/abs/2607.23749",
        track="recommendation",
        organization="YouTube Music / Google",
        published="2026-07-26",
        topics=("ranking", "feedback-loop", "freshness", "exploration"),
        online_ab=(
            OnlineABEvidence("YouTube Music homepage", "1-day new-release engagement", 4.33, "two-week A/B; millions of daily users per arm"),
        ),
    ),
    run=reproduce_youtube_freshness,
    render=render_standard,
    fidelity=ReproductionFidelity.CORE_MECHANISM,
    omitted_core_components=("continuous YouTube training loop", "production SNGP ranker"),
))
