from ..base import PaperMetadata, ReproductionAdapter, ReproductionFidelity
from ..registry import register
from .experiment import reproduce_rankmixer
from .report import render


ADAPTER = register(
    ReproductionAdapter(
        key="rankmixer",
        paper=PaperMetadata(
            arxiv_id="2507.15551",
            title="RankMixer: Scaling Up Ranking Models in Industrial Recommenders",
            url="https://arxiv.org/abs/2507.15551",
            track="recommendation",
        ),
        run=reproduce_rankmixer,
        render=render,
        fidelity=ReproductionFidelity.FULL_PIPELINE,
    )
)
