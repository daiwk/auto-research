from ..base import OnlineABEvidence, PaperMetadata, ReproductionAdapter, ReproductionFidelity
from ..registry import register
from .experiment import reproduce_lwgr
from .report import render


ADAPTER = register(
    ReproductionAdapter(
        key="lwgr",
        paper=PaperMetadata(
            arxiv_id="2605.18771",
            title="LWGR: Lagrangian-Constrained Personalized World Knowledge for Generative Recommendation",
            url="https://arxiv.org/abs/2605.18771",
            track="recommendation",
            organization="Alibaba International / CAS",
            published="2026-05",
            topics=("generative-recommendation", "soft-prompt", "world-knowledge", "lagrangian"),
            online_ab=(
                OnlineABEvidence("Southeast Asia Ads", "Revenue", 1.35, "15% users, 2025-12-19 to 2025-12-30"),
                OnlineABEvidence("Southeast Asia Ads", "CTR", 1.17, "p<0.05"),
            ),
        ),
        run=reproduce_lwgr,
        render=render,
        fidelity=ReproductionFidelity.FULL_PIPELINE,
        omitted_core_components=(
            "Qwen3-4B/8B scale and full Amazon Beauty/Toys preprocessing",
            "2.95B-interaction industrial data and 20.1M-item inventory",
            "nearline vector repository and production online request forwarding",
        ),
    )
)
