from ..base import OnlineABEvidence, PaperMetadata, ReproductionAdapter, ReproductionFidelity
from ..registry import register
from .experiment import reproduce
from .report import render

ADAPTER = register(ReproductionAdapter(
    key="wide-deep",
    paper=PaperMetadata(
        arxiv_id="1606.07792", title="Wide & Deep Learning for Recommender Systems",
        url="https://arxiv.org/abs/1606.07792", track="recommendation",
        code_url="https://github.com/tensorflow/models/tree/master/official/r1/wide_deep",
        organization="Google", published="2016-06-24",
        topics=("ranking", "classic", "feature-interaction"),
        online_ab=(OnlineABEvidence("Google Play", "app acquisition", 3.9, "1% treatment vs 1% control, three weeks"),),
    ),
    run=reproduce, render=render, fidelity=ReproductionFidelity.CORE_MECHANISM,
    omitted_core_components=("Google Play sparse IDs and production crosses", "distributed serving stack"),
))
