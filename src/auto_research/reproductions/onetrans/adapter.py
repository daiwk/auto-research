from ..base import PaperMetadata, ReproductionAdapter, ReproductionFidelity
from ..registry import register
from .experiment import reproduce_onetrans
from .report import render


ADAPTER = register(
    ReproductionAdapter(
        key="onetrans",
        paper=PaperMetadata(
            arxiv_id="2510.26104",
            title="OneTrans: Unified Feature Interaction and Sequence Modeling with One Transformer in Industrial Recommender",
            url="https://arxiv.org/abs/2510.26104",
            track="recommendation",
        ),
        run=reproduce_onetrans,
        render=render,
        fidelity=ReproductionFidelity.FULL_PIPELINE,
    )
)
