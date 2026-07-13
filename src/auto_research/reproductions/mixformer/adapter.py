from ..base import PaperMetadata, ReproductionAdapter, ReproductionFidelity
from ..registry import register
from .experiment import reproduce_mixformer
from .report import render

ADAPTER = register(
    ReproductionAdapter(
        key="mixformer",
        paper=PaperMetadata(
            arxiv_id="2602.14110",
            title="MixFormer: Co-Scaling Up Dense and Sequence in Industrial Recommenders",
            url="https://arxiv.org/abs/2602.14110",
            track="recommendation",
        ),
        run=reproduce_mixformer,
        render=render,
        fidelity=ReproductionFidelity.CONCEPT_DEMO,
        omitted_core_components=("trainable MixFormer blocks", "decoupled serving path"),
    )
)
