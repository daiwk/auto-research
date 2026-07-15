from ..base import OnlineABEvidence, PaperMetadata, ReproductionAdapter, ReproductionFidelity
from ..registry import register
from .experiment import reproduce_pinterest_ads_llm
from .report import render


ADAPTER = register(
    ReproductionAdapter(
        key="pinterest-ads-llm",
        paper=PaperMetadata(
            arxiv_id="2605.27856",
            title="Fine-Tuned LLM as a Complementary Predictor Improving Ads System",
            url="https://arxiv.org/abs/2605.27856",
            track="recommendation",
            organization="Pinterest",
            published="2026-05",
            topics=("advertising", "llm-sft", "grpo", "candidate-generation"),
            online_ab=(
                OnlineABEvidence("US Shopping Ads", "RoAS", 4.94, "p=0.021"),
                OnlineABEvidence("Opt-in US Shopping Ads", "RoAS", 6.69, "p=0.029"),
            ),
        ),
        run=reproduce_pinterest_ads_llm,
        render=render,
        fidelity=ReproductionFidelity.FULL_PIPELINE,
        omitted_core_components=(
            "Pinterest private conversion, URL, advertiser-spend and PinCLIP SID data",
            "4B full-scale training and distributed vLLM/Ray daily serving",
            "live ctcvr/vtcvr and production candidate-blending traffic",
        ),
    )
)
