from ..base import OnlineABEvidence, PaperMetadata, ReproductionAdapter, ReproductionFidelity
from ..registry import register
from .experiment import reproduce_precise
from .report import render_report


register(ReproductionAdapter(
    key="precise",
    paper=PaperMetadata(
        arxiv_id="2412.06308",
        title="PRECISE: Pre-training Sequential Recommenders with Collaborative and Semantic Information",
        url="https://arxiv.org/abs/2412.06308",
        track="recommendation",
        organization="Tencent / WeChat",
        published="2024-12",
        topics=("LLM semantic embedding", "sequential pre-training", "MoE", "targeted training"),
        online_ab=(
            OnlineABEvidence("WeChat article ranking", "Clicks", 1.961, "180M participants"),
            OnlineABEvidence("WeChat article ranking", "Shares", 1.433, "180M participants"),
            OnlineABEvidence("WeChat share U2I recall", "Shares", 2.560, "26M participants"),
        ),
    ),
    run=reproduce_precise,
    render=render_report,
    fidelity=ReproductionFidelity.FULL_PIPELINE,
    omitted_core_components=(
        "Qwen2-1.5B is scaled to SmolLM2-135M for local initialization",
        "WeChat private cross-scene logs and production embedding/ANN servers",
        "daily periodic warm-start deployment schedule",
    ),
))
