from ..base import OnlineABEvidence, PaperMetadata, ReproductionAdapter, ReproductionFidelity
from ..registry import register
from .experiment import reproduce_gryphon_v2
from .report import render


ADAPTER = register(ReproductionAdapter(
    key="gryphon-v2",
    paper=PaperMetadata(
        arxiv_id="2608.06213",
        title="Gryphon-v2: One Model in Place of a Cascade — Generate-and-Rank Recommender with Rollout Distillation",
        url="https://arxiv.org/abs/2608.06213",
        track="recommendation",
        organization="Yandex",
        published="2026-08-06",
        topics=("generative-recommendation", "retrieval", "ranking", "rollout-distillation"),
        online_ab=(
            OnlineABEvidence(
                "Yandex Music large-scale recommendation surface",
                "active users",
                1.41,
                "single model replaces 15+ candidate generators, pre-ranking and final ranking at comparable latency",
            ),
        ),
    ),
    run=reproduce_gryphon_v2,
    render=render,
    fidelity=ReproductionFidelity.CORE_MECHANISM,
    omitted_core_components=(
        "Yandex private music interaction logs and multimodal semantic IDs",
        "8,000-event teacher history and ten-minute online refresh",
        "production Triton serving stack",
    ),
))
