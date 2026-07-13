from __future__ import annotations

from ..base import PaperMetadata, ReproductionAdapter, ReproductionFidelity
from ..registry import register
from .experiment import reproduce_mdcns
from .report import render

ADAPTER = register(
    ReproductionAdapter(
        key="mdcns",
        paper=PaperMetadata(
            arxiv_id="2605.19651",
            title="Divergence Meets Consensus: A Multi-Source Negative Sampling Framework for Sequential Recommendation",
            url="https://arxiv.org/abs/2605.19651",
            track="recommendation",
            code_url="https://github.com/Lyz103/SIGIR26-MDCNS",
        ),
        run=reproduce_mdcns,
        render=render,
        fidelity=ReproductionFidelity.CORE_MECHANISM,
    )
)
