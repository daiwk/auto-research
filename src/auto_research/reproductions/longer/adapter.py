from ..base import PaperMetadata, ReproductionAdapter, ReproductionFidelity
from ..registry import register
from .experiment import reproduce_longer
from .report import render

ADAPTER = register(
    ReproductionAdapter(
        key="longer",
        paper=PaperMetadata(
            arxiv_id="2505.04421",
            title="LONGER: Scaling Up Long Sequence Modeling in Industrial Recommenders",
            url="https://arxiv.org/abs/2505.04421",
            track="recommendation",
        ),
        run=reproduce_longer,
        render=render,
        fidelity=ReproductionFidelity.CONCEPT_DEMO,
        omitted_core_components=("trainable hybrid attention", "InnerTrans module"),
    )
)
