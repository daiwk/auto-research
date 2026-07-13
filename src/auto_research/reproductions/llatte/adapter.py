from ..base import PaperMetadata, ReproductionAdapter
from ..registry import register
from .experiment import reproduce_llatte
from .report import render

ADAPTER = register(
    ReproductionAdapter(
        key="llatte",
        paper=PaperMetadata(
            arxiv_id="2601.20083",
            title="LLaTTE: Scaling Laws for Multi-Stage Sequence Modeling in Large-Scale Ads Recommendation",
            url="https://arxiv.org/abs/2601.20083",
            track="recommendation",
        ),
        run=reproduce_llatte,
        render=render,
    )
)
