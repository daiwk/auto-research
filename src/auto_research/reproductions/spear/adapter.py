from ..base import OnlineABEvidence, PaperMetadata, ReproductionAdapter, ReproductionFidelity
from ..registry import register
from .experiment import reproduce_spear
from .report import render

ADAPTER = register(ReproductionAdapter(
    key="spear",
    paper=PaperMetadata(
        arxiv_id="2608.01738", title="SPEAR: Selection-aware Personalized End-to-end Adaptive Rewriting and Retrieval for Community Search",
        url="https://arxiv.org/abs/2608.01738", track="recommendation",
        code_url="https://github.com/mallocagi1-cell/spear",
        organization="Dewu", published="2026-08-03",
        topics=("search", "query-rewriting", "retrieval", "personalization"),
        online_ab=(
            OnlineABEvidence("Dewu community search", "Query-view CTR", 0.259, "online A/B; fully deployed"),
            OnlineABEvidence("Dewu community search", "Average reading depth", 0.733, "online A/B; fully deployed"),
        ),
    ),
    run=reproduce_spear, render=render, fidelity=ReproductionFidelity.CORE_MECHANISM,
    omitted_core_components=("Dewu private query/rewrite/item logs", "production request-level feature schema and serving stack"),
))
