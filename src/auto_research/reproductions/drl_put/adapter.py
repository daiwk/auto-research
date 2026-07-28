from ..base import OnlineABEvidence, PaperMetadata, ReproductionAdapter, ReproductionFidelity
from ..registry import register
from .experiment import reproduce_drl_put
from .report import render


ADAPTER = register(ReproductionAdapter(
    key="drl-put",
    paper=PaperMetadata(
        arxiv_id="2509.05292",
        title="Deep Reinforcement Learning for Ranking Utility Tuning in the Ad Recommender System at Pinterest",
        url="https://arxiv.org/abs/2509.05292",
        track="recommendation",
        organization="Pinterest",
        published="2025-09-05",
        topics=("ads-ranking", "reinforcement-learning", "utility-tuning", "off-policy"),
        online_ab=(
            OnlineABEvidence("Pinterest ads", "platform revenue", 0.27, "production A/B"),
            OnlineABEvidence("Pinterest ads", "CTR", 1.62, "production A/B"),
        ),
    ),
    run=reproduce_drl_put,
    render=render,
    fidelity=ReproductionFidelity.CORE_MECHANISM,
    omitted_core_components=("Pinterest auction and revenue labels", "production counterfactual calibration"),
))
