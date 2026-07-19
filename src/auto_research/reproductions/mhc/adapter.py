from ..base import PaperMetadata, ReproductionAdapter, ReproductionFidelity
from ..registry import register
from .experiment import reproduce_mhc
from .report import render


ADAPTER = register(ReproductionAdapter(
    key="mhc",
    paper=PaperMetadata(
        arxiv_id="2512.24880",
        title="mHC: Manifold-Constrained Hyper-Connections",
        url="https://arxiv.org/abs/2512.24880",
        track="llm",
        organization="DeepSeek-AI",
        published="2025-12-31",
        topics=("llm-architecture", "hyper-connections", "training-stability"),
    ),
    run=reproduce_mhc,
    render=render,
    fidelity=ReproductionFidelity.CORE_MECHANISM,
    omitted_core_components=("3B/9B/27B private pre-training", "TileLang kernels, recomputation and DualPipe"),
))
