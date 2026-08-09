from ..base import OnlineABEvidence, PaperMetadata, ReproductionAdapter, ReproductionFidelity
from ..registry import register
from ..latest_20260809_common import reproduce_kgd, render_latest

ADAPTER = register(ReproductionAdapter(
    key="kgd", paper=PaperMetadata(
        arxiv_id="2608.02738", title="Knowledge–Geometry Decoupling: Refreshable Pretrained Transfer for Streaming Recommendation",
        url="https://arxiv.org/abs/2608.02738", track="recommendation",
        code_url="https://github.com/FuCongResearchSquad/KGD4REC",
        organization="Xiamen University / Shopee", published="2026-08-03",
        topics=("sequential-recommendation", "pretraining", "streaming", "transfer"),
        online_ab=(
            OnlineABEvidence("Shopee Homepage Search", "GMV per user", 1.75, "live A/B; fully deployed"),
            OnlineABEvidence("Shopee Homepage Search", "advertising revenue", 1.53, "live A/B; fully deployed"),
        )), run=reproduce_kgd, render=render_latest,
    fidelity=ReproductionFidelity.CORE_MECHANISM,
    omitted_core_components=("Shopee private 90-day stream", "production continual refresh service"),
))
