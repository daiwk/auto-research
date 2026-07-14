from ..base import OnlineABEvidence, PaperMetadata, ReproductionAdapter, ReproductionFidelity
from ..registry import register
from .experiment import reproduce_pinrec
from .report import render

ADAPTER = register(ReproductionAdapter(
    key="pinrec",
    paper=PaperMetadata(
        arxiv_id="2504.10507", title="PinRec: Outcome-Conditioned, Multi-Token Generative Retrieval for Industry-Scale Recommendation Systems",
        url="https://arxiv.org/abs/2504.10507", track="recommendation",
        organization="Pinterest", published="2025-04",
        topics=("generative-retrieval", "outcome-conditioning", "multi-token"),
        online_ab=(OnlineABEvidence("Pinterest Homefeed", "grid clicks", 4.01, "global traffic, CUPED adjusted"),),
    ),
    run=reproduce_pinrec, render=render,
    fidelity=ReproductionFidelity.FULL_PIPELINE,
))
