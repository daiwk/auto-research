from ..base import OnlineABEvidence, PaperMetadata, ReproductionAdapter, ReproductionFidelity
from ..registry import register
from .experiment import reproduce_m6rec
from .report import render

ADAPTER = register(ReproductionAdapter(
    key="m6rec",
    paper=PaperMetadata(
        arxiv_id="2205.08084",
        title="M6-Rec: Generative Pretrained Language Models are Open-Ended Recommender Systems",
        url="https://arxiv.org/abs/2205.08084", track="recommendation",
        organization="Alibaba", published="2022-05",
        topics=("llm-recommendation", "foundation-model", "parameter-efficient-tuning"),
        online_ab=(OnlineABEvidence("Alipay", "mini-app retrieval CTR", 1.0, "live replacement; fully deployed"),),
    ),
    run=reproduce_m6rec, render=render,
    fidelity=ReproductionFidelity.CORE_MECHANISM,
))
