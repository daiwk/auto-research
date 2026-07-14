from ..base import PaperMetadata, ReproductionAdapter, ReproductionFidelity
from ..registry import register
from .experiment import reproduce_pinfm
from .report import render


ADAPTER = register(ReproductionAdapter(
    key="pinfm",
    paper=PaperMetadata(
        arxiv_id="2507.12704",
        title="PinFM: Foundation Model for User Activity Sequences at a Billion-scale Visual Discovery Platform",
        url="https://arxiv.org/abs/2507.12704",
        track="recommendation",
    ),
    run=reproduce_pinfm,
    render=render,
    fidelity=ReproductionFidelity.CORE_MECHANISM,
    omitted_core_components=(
        "Pinterest multi-action and multi-surface pretraining corpus",
        "fresh-item age-dependent dropout",
        "int4 embedding and Triton DCAT serving kernels",
    ),
))
