from ..base import EvaluationTier, OnlineABEvidence, PaperMetadata, ReproductionAdapter, ReproductionFidelity
from ..registry import register
from .experiment import reproduce_reward_guided_decoding
from .report import render


ADAPTER = register(
    ReproductionAdapter(
        key="reward-guided-decoding",
        paper=PaperMetadata(
            arxiv_id="2607.25344",
            title="Reward Guided Decoding for Generative Recommendation",
            url="https://arxiv.org/abs/2607.25344",
            track="recommendation",
            organization="Institute of Information Engineering, Chinese Academy of Sciences",
            published="2026-07-28",
            topics=("generative-recommendation", "decoding", "reward", "business-alignment"),
            online_ab=(
                OnlineABEvidence(
                    "Kuaishou live-streaming recommendation",
                    "watch time",
                    0.689,
                    "two-week online A/B test",
                    source_url="https://arxiv.org/html/2607.25344v1",
                    source_location="Section 5.4 online A/B test",
                    retrieved_at="2026-09-01",
                ),
            ),
        ),
        run=reproduce_reward_guided_decoding,
        render=render,
        fidelity=ReproductionFidelity.CORE_MECHANISM,
        omitted_core_components=("Kuaishou SID generator", "shared-decoder reward model", "production beam search"),
        evaluation_tier=EvaluationTier.PUBLIC_DATASET,
        datasets=("MovieLens 100K",),
        baseline="generator likelihood decoding",
        metrics=("hit_at_10", "ndcg_at_10", "guided_expected_reward", "kl_from_generator"),
        evolve_operators=("reward:reward-guided",),
        default_seeds=(42, 43, 44),
        budget="220 users / 360 items; beta=0.55",
        device_capabilities=("cpu",),
    )
)
