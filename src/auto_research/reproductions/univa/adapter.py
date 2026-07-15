from ..base import OnlineABEvidence, PaperMetadata, ReproductionAdapter, ReproductionFidelity
from ..registry import register
from .experiment import reproduce_univa
from .report import render


ADAPTER = register(
    ReproductionAdapter(
        key="univa",
        paper=PaperMetadata(
            arxiv_id="2605.05803",
            title="Unified Value Alignment for Generative Recommendation in Industrial Advertising",
            url="https://arxiv.org/abs/2605.05803",
            track="recommendation",
            organization="Tencent / WeChat Channels",
            published="2026-05",
            topics=("generative-advertising", "commercial-sid", "ppo", "value-aware-serving"),
            online_ab=(
                OnlineABEvidence(
                    "WeChat Channels Ads",
                    "GMV",
                    1.50,
                    "5% traffic, 2026-03-07 to 2026-03-11",
                ),
                OnlineABEvidence(
                    "WeChat Channels Ads",
                    "GMV(normal)",
                    1.42,
                    "5% traffic, 2026-03-07 to 2026-03-11",
                ),
            ),
        ),
        run=reproduce_univa,
        render=render,
        fidelity=ReproductionFidelity.FULL_PIPELINE,
        omitted_core_components=(
            "Tencent private multimodal ads, optimization goal, ROI, industry, and bid fields",
            "production pCTR/pCVR simulator snapshots and MCTS sampler",
            "80M decoder, 2048-token histories, production inventory and live serving",
        ),
    )
)
