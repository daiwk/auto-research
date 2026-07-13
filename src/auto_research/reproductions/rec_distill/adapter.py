from ..base import PaperMetadata, ReproductionAdapter, ReproductionFidelity
from ..registry import register
from .experiment import reproduce_rec_distill
from .report import render


ADAPTER = register(
    ReproductionAdapter(
        key="rec-distill",
        paper=PaperMetadata(
            arxiv_id="2605.29755",
            title="Rec-Distill: An Industrial Distillation Pipeline for Large-Scale Recommendation Models",
            url="https://arxiv.org/abs/2605.29755",
            track="recommendation",
        ),
        run=reproduce_rec_distill,
        render=render,
        fidelity=ReproductionFidelity.FULL_PIPELINE,
    )
)
