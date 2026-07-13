from ..base import PaperMetadata, ReproductionAdapter, ReproductionFidelity
from ..registry import register
from .experiment import reproduce_hyformer
from .report import render


ADAPTER = register(
    ReproductionAdapter(
        key="hyformer",
        paper=PaperMetadata(
            arxiv_id="2601.12681",
            title="HyFormer: Revisiting the Roles of Sequence Modeling and Feature Interaction in CTR Prediction",
            url="https://arxiv.org/abs/2601.12681",
            track="recommendation",
        ),
        run=reproduce_hyformer,
        render=render,
        fidelity=ReproductionFidelity.FULL_PIPELINE,
    )
)
