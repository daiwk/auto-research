from ..base import OnlineABEvidence, PaperMetadata, ReproductionAdapter, ReproductionFidelity
from ..registry import register
from .experiment import reproduce_notellm
from .report import render

ADAPTER = register(ReproductionAdapter(
    key="notellm",
    paper=PaperMetadata(
        arxiv_id="2403.01744", title="NoteLLM: A Retrievable Large Language Model for Note Recommendation",
        url="https://arxiv.org/abs/2403.01744", track="recommendation",
        organization="Xiaohongshu", published="2024-03",
        topics=("llm-recommendation", "contrastive-learning", "i2i-retrieval"),
        online_ab=(OnlineABEvidence("Xiaohongshu I2I", "CTR", 16.20, "week-long online experiment"),),
    ),
    run=reproduce_notellm, render=render,
    fidelity=ReproductionFidelity.FULL_PIPELINE,
))
