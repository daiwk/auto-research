from ..base import OnlineABEvidence, PaperMetadata, ReproductionAdapter, ReproductionFidelity
from ..registry import register
from .experiment import reproduce_recgpt_mobile
from .report import render


ADAPTER = register(ReproductionAdapter(
    key="recgpt-mobile",
    paper=PaperMetadata(
        arxiv_id="2605.04726",
        title="RecGPT-Mobile: On-Device Large Language Models for User Intent Understanding in Taobao Feed Recommendation",
        url="https://arxiv.org/abs/2605.04726",
        track="recommendation",
        organization="Alibaba / Taobao",
        published="2026-05-06",
        topics=("llm-recommendation", "on-device", "intent-understanding", "serving-efficiency"),
        online_ab=(
            OnlineABEvidence("Mobile Taobao feed", "CLICK", 1.8, "one-month test across four scenarios"),
            OnlineABEvidence("Mobile Taobao feed", "PAY", 2.7, "one-month test across four scenarios"),
            OnlineABEvidence("Mobile Taobao feed", "GMV", 2.5, "one-month test across four scenarios"),
        ),
    ),
    run=reproduce_recgpt_mobile,
    render=render,
    fidelity=ReproductionFidelity.CORE_MECHANISM,
    omitted_core_components=(
        "Qwen3-0.6B proprietary intent data and human annotations",
        "GPT rewriting and production item retrieval",
        "real mobile runtime, device fleet and operating-system integration",
    ),
))
