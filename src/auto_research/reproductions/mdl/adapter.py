from ..base import OnlineABEvidence, PaperMetadata, ReproductionAdapter, ReproductionFidelity
from ..industrial_2026 import render_standard
from ..registry import register
from .experiment import reproduce_mdl


ADAPTER = register(ReproductionAdapter(
    key="mdl",
    paper=PaperMetadata(
        arxiv_id="2602.07520",
        title="MDL: A Unified Multi-Distribution Learner in Large-scale Industrial Recommendation through Tokenization",
        url="https://arxiv.org/abs/2602.07520", track="recommendation",
        organization="ByteDance / Douyin", published="2026-02-07",
        topics=("ranking", "multi-scenario", "multi-task", "tokenization"),
        online_ab=(
            OnlineABEvidence("Douyin search", "LT30", 0.0626, "online A/B"),
            OnlineABEvidence("Douyin search", "query rewrite rate", -0.3267, "online A/B"),
        ),
    ),
    run=reproduce_mdl, render=render_standard,
    fidelity=ReproductionFidelity.CORE_MECHANISM,
    omitted_core_components=("hundreds-of-millions-user production model", "private scenario/task labels"),
))
