from ..base import (
    OnlineABEvidence,
    PaperMetadata,
    ReproductionAdapter,
    ReproductionFidelity,
)
from ..registry import register
from .experiment import reproduce_recgpt_v2
from .report import render

ADAPTER = register(
    ReproductionAdapter(
        key="recgpt-v2",
        paper=PaperMetadata(
            arxiv_id="2512.14503",
            title="RecGPT-V2 Technical Report",
            url="https://arxiv.org/abs/2512.14503",
            track="recommendation",
            organization="Alibaba / Taobao",
            published="2025-12-16",
            topics=(
                "llm-recommendation",
                "multi-agent",
                "reinforcement-learning",
                "ranking",
            ),
            online_ab=(
                OnlineABEvidence("Taobao", "CTR", 2.98, "online A/B"),
                OnlineABEvidence("Taobao", "IPV", 3.71, "online A/B"),
                OnlineABEvidence("Taobao", "NER", 11.46, "online A/B"),
            ),
        ),
        run=reproduce_recgpt_v2,
        render=render,
        fidelity=ReproductionFidelity.CORE_MECHANISM,
        omitted_core_components=(
            "Taobao proprietary LLM",
            "production Agent-as-a-Judge labels",
        ),
    )
)
