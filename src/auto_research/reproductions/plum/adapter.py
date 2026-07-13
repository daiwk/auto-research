from ..base import PaperMetadata, ReproductionAdapter, ReproductionFidelity
from ..registry import register
from .experiment import reproduce_plum
from .report import render

ADAPTER = register(
    ReproductionAdapter(
        key="plum",
        paper=PaperMetadata(
            arxiv_id="2510.07784",
            title="PLUM: Adapting Pre-trained Language Models for Industrial-scale Generative Recommendations",
            url="https://arxiv.org/abs/2510.07784",
            track="recommendation",
        ),
        run=reproduce_plum,
        render=render,
        fidelity=ReproductionFidelity.FULL_PIPELINE,
    )
)
