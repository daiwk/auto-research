from ..base import OnlineABEvidence, PaperMetadata, ReproductionAdapter, ReproductionFidelity
from ..registry import register
from ..latest_20260809_common import reproduce_twitch_mor, render_latest

ADAPTER = register(ReproductionAdapter(
    key="twitch-mor", paper=PaperMetadata(
        arxiv_id="2608.04455", title="Multi-Objective Ranking for Live-Streaming: Balancing Fresh and Delayed Signals with Segment-Aware Targeting",
        url="https://arxiv.org/abs/2608.04455", track="recommendation",
        organization="Twitch", published="2026-08-05",
        topics=("ranking", "multi-task-learning", "mmoe", "live-streaming"),
        online_ab=(
            OnlineABEvidence("Twitch live recommendation", "daily active viewers", .09, "14-day A/B", significance="p<0.01"),
            OnlineABEvidence("Twitch engaged viewers", "capped ARPU", .56, "14-day A/B", significance="p<0.05"),
            OnlineABEvidence("Twitch mobile livefeed", "positive interactions", 1.12, "14-day A/B", significance="p<0.001"),
        )), run=reproduce_twitch_mor, render=render_latest,
    fidelity=ReproductionFidelity.CORE_MECHANISM,
    omitted_core_components=("Twitch private engagement and revenue labels", "production p99 serving stack"),
))
