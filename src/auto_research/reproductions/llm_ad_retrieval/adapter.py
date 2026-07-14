from ..base import OnlineABEvidence, PaperMetadata, ReproductionAdapter, ReproductionFidelity
from ..registry import register
from .experiment import reproduce_llm_ad_retrieval
from .report import render


ADAPTER = register(
    ReproductionAdapter(
        key="llm-ad-retrieval",
        paper=PaperMetadata(
            arxiv_id="2605.21969",
            title="LLM Retrieval for Stable and Predictable Ad Recommendations",
            url="https://arxiv.org/abs/2605.21969",
            track="recommendation",
            organization="Meta",
            published="2026-05",
            topics=("llm-recommendation", "retrieval", "stability"),
            online_ab=(
                OnlineABEvidence(
                    product="Meta Ads",
                    metric="top-line performance",
                    lift_percent=0.45,
                    traffic="large-scale industrial online A/B",
                ),
            ),
        ),
        run=reproduce_llm_ad_retrieval,
        render=render,
        fidelity=ReproductionFidelity.CORE_MECHANISM,
        omitted_core_components=(
            "Llama-3-8B and private ads fine-tuning data",
            "Meta distributed inference and online serving stack",
            "conversion/revenue-weighted live A/A' shadow-ad framework",
        ),
    )
)
