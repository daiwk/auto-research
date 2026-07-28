from ..base import OnlineABEvidence, PaperMetadata, ReproductionAdapter, ReproductionFidelity
from ..registry import register
from .experiment import reproduce_core_relevance
from .report import render


ADAPTER = register(
    ReproductionAdapter(
        key="core-relevance",
        paper=PaperMetadata(
            arxiv_id="2607.24417",
            title="CORE: A Unified Cascaded Ordinal Relevance Estimation Framework for E-commerce Search",
            url="https://arxiv.org/abs/2607.24417",
            track="recommendation",
            organization="Meituan / Beijing Institute of Technology",
            published="2026-07-27",
            topics=(
                "search-ranking",
                "ordinal-relevance",
                "step-grpo",
                "llm-distillation",
            ),
            online_ab=(
                OnlineABEvidence("Meituan e-commerce search", "NDCG@5", 0.20, "production A/B"),
                OnlineABEvidence("Meituan e-commerce search", "Badcase@5 reduction", 15.9, "production A/B"),
            ),
        ),
        run=reproduce_core_relevance,
        render=render,
        fidelity=ReproductionFidelity.CORE_MECHANISM,
        omitted_core_components=(
            "Meituan private 90K query-item relevance labels",
            "Qwen3-14B reasoning traces",
            "production BERT encoder and online thresholds",
        ),
    )
)
