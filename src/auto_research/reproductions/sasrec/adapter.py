from ..base import PaperMetadata, ReproductionAdapter, ReproductionFidelity
from ..registry import register
from .experiment import reproduce_sasrec
from .report import render


ADAPTER = register(ReproductionAdapter(
    key="sasrec",
    paper=PaperMetadata(arxiv_id="1808.09781", title="Self-Attentive Sequential Recommendation", url="https://arxiv.org/abs/1808.09781", track="recommendation", code_url="https://github.com/kang205/SASRec"),
    run=reproduce_sasrec,
    render=render,
    fidelity=ReproductionFidelity.FULL_PIPELINE,
))
