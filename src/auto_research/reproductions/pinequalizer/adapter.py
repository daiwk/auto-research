from ..base import OnlineABEvidence, PaperMetadata, ReproductionAdapter, ReproductionFidelity
from ..registry import register
from .experiment import reproduce_pinequalizer
from .report import render


ADAPTER = register(ReproductionAdapter(
    key="pinequalizer",
    paper=PaperMetadata(
        arxiv_id="2607.22518",
        title="PinEqualizer: Full Funnel Content Exploration and Debiasing System at Pinterest",
        url="https://arxiv.org/abs/2607.22518",
        track="recommendation",
        organization="Pinterest",
        published="2026-07-23",
        topics=("cold-start", "exploration", "debiasing", "ranking", "retrieval"),
        online_ab=(
            OnlineABEvidence(
                "Related Pins",
                "fresh-content engagement volume, ranking architecture",
                8.63,
                "component-level user A/B",
            ),
            OnlineABEvidence(
                "Related Pins",
                "underexplored-content engagement volume, ranking architecture",
                6.57,
                "component-level user A/B",
            ),
        ),
    ),
    run=reproduce_pinequalizer,
    render=render,
    fidelity=ReproductionFidelity.CORE_MECHANISM,
    omitted_core_components=(
        "Pinterest private Pin, provider, PinCLIP, Semantic-ID and off-platform data",
        "Homefeed/Search/Related Pins production retrieval and ranking stacks",
        "multi-year content holdout, live traffic and near-real-time Flink features",
    ),
))
