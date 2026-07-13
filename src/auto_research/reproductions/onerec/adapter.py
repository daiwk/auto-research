from ..base import PaperMetadata, ReproductionAdapter, ReproductionFidelity
from ..registry import register
from .experiment import reproduce_onerec
from .report import render

ADAPTER = register(
    ReproductionAdapter(
        key="onerec",
        paper=PaperMetadata(
            arxiv_id="2502.18965",
            title="OneRec: Unifying Retrieve and Rank with Generative Recommender and Iterative Preference Alignment",
            url="https://arxiv.org/abs/2502.18965",
            track="recommendation",
        ),
        run=reproduce_onerec,
        render=render,
        fidelity=ReproductionFidelity.FULL_PIPELINE,
    )
)
