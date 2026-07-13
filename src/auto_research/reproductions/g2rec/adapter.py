from ..base import PaperMetadata, ReproductionAdapter, ReproductionFidelity
from ..registry import register
from .experiment import reproduce_g2rec
from .report import render

ADAPTER = register(
    ReproductionAdapter(
        key="g2rec",
        paper=PaperMetadata(
            arxiv_id="2606.20554",
            title="Structuring and Tokenizing Distributed User Interest Context for Generative Recommendation",
            url="https://arxiv.org/abs/2606.20554",
            track="recommendation",
        ),
        run=reproduce_g2rec,
        render=render,
        fidelity=ReproductionFidelity.CONCEPT_DEMO,
        omitted_core_components=("generative decoder", "autoregressive interest-token training"),
    )
)
