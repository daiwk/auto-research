from ..base import OnlineABEvidence, PaperMetadata, ReproductionAdapter, ReproductionFidelity
from ..registry import register
from .experiment import reproduce_recgpt_v3
from .report import render


ADAPTER = register(ReproductionAdapter(
    key="recgpt-v3",
    paper=PaperMetadata(
        arxiv_id="2607.15591",
        title="RecGPT-V3 Technical Report",
        url="https://arxiv.org/abs/2607.15591",
        track="recommendation",
        organization="Alibaba / Taobao",
        published="2026-07-17",
        topics=("generative-recommendation", "semantic-id", "user-memory", "latent-reasoning"),
        online_ab=(
            OnlineABEvidence("Taobao Guess What You Like (feed)", "IPV", 1.28, "1% treatment vs 1% RecGPT-V2 control"),
            OnlineABEvidence("Taobao Guess What You Like (feed)", "CTR", 1.00, "1% treatment vs 1% RecGPT-V2 control"),
            OnlineABEvidence("Taobao Guess What You Like (feed)", "GMV", 3.97, "1% treatment vs 1% RecGPT-V2 control"),
        ),
    ),
    run=reproduce_recgpt_v3,
    render=render,
    fidelity=ReproductionFidelity.CORE_MECHANISM,
    omitted_core_components=(
        "Qwen3-14B continual pre-training and general-domain mixture",
        "CN-CLIP/Q-Former image tower and private Taobao behavior",
        "DeepSeek-V3.2 teacher and production CTR ranker",
        "online GRPO and production serving stack",
    ),
))
