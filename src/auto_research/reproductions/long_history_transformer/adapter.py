from ..base import OnlineABEvidence, PaperMetadata, ReproductionAdapter, ReproductionFidelity
from ..registry import register
from .experiment import reproduce_long_history_transformer
from .report import render


ADAPTER = register(ReproductionAdapter(
    key="long-history-transformer",
    paper=PaperMetadata(
        arxiv_id="2607.14331",
        title="Long-History User Transformers for Real-Time Ad Ranking",
        url="https://arxiv.org/abs/2607.14331",
        track="recommendation",
        organization="Yandex",
        published="2026-07-15",
        topics=("advertising", "long-sequence", "cached-user-representation", "serving"),
        online_ab=(
            OnlineABEvidence("Yandex Search Ads", "Primary ranking metric", 2.77, "production A/B; p<0.05"),
            OnlineABEvidence("Yandex Search Ads", "Revenue", 2.26, "production A/B; p<0.05"),
            OnlineABEvidence("Yandex Advertising Network", "Primary ranking metric", 2.10, "production A/B; p<0.05"),
        ),
    ),
    run=reproduce_long_history_transformer,
    render=render,
    fidelity=ReproductionFidelity.CORE_MECHANISM,
    omitted_core_components=("private Yandex cross-surface logs", "production CatBoost ranker and feature-store refresh stack"),
))
