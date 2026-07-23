from ..base import OnlineABEvidence, PaperMetadata, ReproductionAdapter, ReproductionFidelity
from ..registry import register
from .experiment import reproduce_downstream_rewards
from .report import render


ADAPTER = register(ReproductionAdapter(
    key="downstream-rewards",
    paper=PaperMetadata(
        arxiv_id="2607.14192",
        title="Long-term User Engagement Optimization through Model-agnostic Downstream Rewards Learning",
        url="https://arxiv.org/abs/2607.14192",
        track="recommendation",
        organization="Pinterest",
        published="2026-07-15",
        topics=("long-term-value", "reward-design", "multi-surface", "retention"),
        online_ab=(
            OnlineABEvidence("Pinterest Homefeed", "Successful Sessions", 0.36, "online A/B"),
            OnlineABEvidence("Pinterest Search", "Search Fulfillment Rate", 0.25, "online A/B"),
            OnlineABEvidence("Pinterest Related Pins", "Successful Sessions", 0.15, "online A/B"),
        ),
    ),
    run=reproduce_downstream_rewards,
    render=render,
    fidelity=ReproductionFidelity.CORE_MECHANISM,
    omitted_core_components=("billions of private Pinterest cross-surface events", "production Pinnability and TransAct rankers"),
))
