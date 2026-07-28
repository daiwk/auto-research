from ..base import PaperMetadata, ReproductionAdapter, ReproductionFidelity
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
        fidelity=ReproductionFidelity.CORE_MECHANISM,
        omitted_core_components=("private Meta ads features", "asynchronous production serving"),
    )
)
