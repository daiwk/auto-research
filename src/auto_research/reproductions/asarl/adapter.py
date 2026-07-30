from ..base import OnlineABEvidence, PaperMetadata, ReproductionAdapter, ReproductionFidelity
from ..registry import register
from .experiment import reproduce_asarl
from .report import render


ADAPTER = register(
    ReproductionAdapter(
        key="asarl",
        paper=PaperMetadata(
            arxiv_id="2607.26593",
            title="ASARL: Autonomous Social-Aware Relevance Learning for QQ Search",
            url="https://arxiv.org/abs/2607.26593",
            track="recommendation",
            organization="Tencent PCG",
            published="2026-07-29",
            topics=("search-relevance", "multi-agent-data-curation", "knowledge-distillation"),
            online_ab=(
                OnlineABEvidence("QQ channel search", "CTR", 2.69, "20% treatment / 20% control, >=7 days"),
                OnlineABEvidence("QQ group search", "GSB", 16.66, "20% treatment / 20% control, >=7 days"),
            ),
        ),
        run=reproduce_asarl,
        render=render,
        fidelity=ReproductionFidelity.CORE_MECHANISM,
        omitted_core_components=(
            "QQ private social-search logs",
            "production LLM annotation agents",
            "online RoBERTa deployment",
        ),
    )
)
