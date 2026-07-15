from ..base import OnlineABEvidence, PaperMetadata, ReproductionAdapter, ReproductionFidelity
from ..registry import register
from .experiment import reproduce_s_grec
from .report import render


ADAPTER = register(
    ReproductionAdapter(
        key="s-grec",
        paper=PaperMetadata(
            arxiv_id="2602.10606",
            title="S-GRec: Personalized Semantic-Aware Generative Recommendation with Asymmetric Advantage",
            url="https://arxiv.org/abs/2602.10606",
            track="recommendation",
            organization="Tencent / WeChat Channels",
            published="2026-02",
            topics=("generative-recommendation", "llm-as-judge", "grpo", "a2po"),
            online_ab=(
                OnlineABEvidence("WeChat Channels", "GMV", 1.19, "20% advertising traffic"),
                OnlineABEvidence("WeChat Channels", "CTR", 1.16, "20% advertising traffic"),
            ),
        ),
        run=reproduce_s_grec,
        render=render,
        fidelity=ReproductionFidelity.FULL_PIPELINE,
        omitted_core_components=(
            "Qwen3-4B judge, Qwen2.5-1.5B MiniOneRec backbone and production-scale training",
            "20k human-verified point-wise and 40k pairwise proprietary ad annotations",
            "WeChat eCPM reward model, ad inventory and online sample server",
        ),
    )
)
