from ..base import PaperMetadata, ReproductionAdapter, ReproductionFidelity
from ..registry import register
from .experiment import reproduce_cmsl
from .report import render

ADAPTER = register(
    ReproductionAdapter(
        key="cmsl",
        paper=PaperMetadata(
            arxiv_id="2606.28533",
            title="CMSL: Constructive Multi-Sequence Learning for Recommendation Systems",
            url="https://arxiv.org/abs/2606.28533",
            track="recommendation",
        ),
        run=reproduce_cmsl,
        render=render,
        fidelity=ReproductionFidelity.CONCEPT_DEMO,
        omitted_core_components=("learned contextual lenses", "trainable HSTU backbone"),
    )
)
