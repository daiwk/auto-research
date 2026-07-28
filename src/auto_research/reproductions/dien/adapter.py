from ..base import OnlineABEvidence, PaperMetadata, ReproductionAdapter, ReproductionFidelity
from ..registry import register
from .experiment import reproduce
from .report import render

ADAPTER = register(ReproductionAdapter(
    key="dien",
    paper=PaperMetadata(
        arxiv_id="1809.03672", title="Deep Interest Evolution Network for Click-Through Rate Prediction",
        url="https://arxiv.org/abs/1809.03672", track="recommendation",
        code_url="https://github.com/mouna99/dien", organization="Alibaba",
        published="2018-09-11", topics=("ranking", "classic", "sequence-modeling"),
        online_ab=(OnlineABEvidence("Taobao display advertising", "CTR", 20.7, "2018-06-07 to 2018-07-12"),),
    ),
    run=reproduce, render=render, fidelity=ReproductionFidelity.CORE_MECHANISM,
    omitted_core_components=("Taobao private ads features", "fused production AUGRU kernels"),
))
