from ..base import PaperMetadata, ReproductionAdapter
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
    )
)
