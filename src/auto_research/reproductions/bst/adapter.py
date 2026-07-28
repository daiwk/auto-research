from ..base import OnlineABEvidence, PaperMetadata, ReproductionAdapter, ReproductionFidelity
from ..registry import register
from .experiment import reproduce
from .report import render

ADAPTER = register(ReproductionAdapter(
    key="bst",
    paper=PaperMetadata(
        arxiv_id="1905.06874", title="Behavior Sequence Transformer for E-commerce Recommendation in Alibaba",
        url="https://arxiv.org/abs/1905.06874", track="recommendation",
        organization="Alibaba", published="2019-05-15",
        topics=("ranking", "classic", "sequence-modeling"),
        online_ab=(OnlineABEvidence("Taobao recommendation", "CTR", 7.57, "online A/B vs WDL control"),),
    ),
    run=reproduce, render=render, fidelity=ReproductionFidelity.CORE_MECHANISM,
    omitted_core_components=("Taobao private user/context features", "production inference stack"),
))
