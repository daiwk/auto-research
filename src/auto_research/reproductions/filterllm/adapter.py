from ..base import (
    OnlineABEvidence,
    PaperMetadata,
    ReproductionAdapter,
    ReproductionFidelity,
)
from ..registry import register
from .experiment import reproduce_filterllm
from .report import render

ADAPTER = register(
    ReproductionAdapter(
        key="filterllm",
        paper=PaperMetadata(
            arxiv_id="2502.16924",
            title="FilterLLM: Text-To-Distribution LLM for Billion-Scale Cold-Start Recommendation",
            url="https://arxiv.org/abs/2502.16924",
            track="recommendation",
            organization="Alibaba",
            published="2025-02-24",
            topics=(
                "llm-recommendation",
                "cold-start",
                "retrieval",
                "text-to-distribution",
            ),
            online_ab=(
                OnlineABEvidence(
                    "Alibaba cold-start", "Cold-PV", 5.13, "two-month A/B"
                ),
                OnlineABEvidence("Alibaba cold-start", "GMV", 10.86, "two-month A/B"),
            ),
        ),
        run=reproduce_filterllm,
        render=render,
        fidelity=ReproductionFidelity.CORE_MECHANISM,
        omitted_core_components=(
            "billion-user vocabulary",
            "proprietary LLM and cold-start traffic",
        ),
    )
)
