from ..base import PaperMetadata, ReproductionAdapter, ReproductionFidelity
from ..registry import register
from .experiment import reproduce_naju
from .report import render


ADAPTER = register(ReproductionAdapter(
    key="naju",
    paper=PaperMetadata(
        arxiv_id="2607.21000",
        title="Naju: A Native Discrete State-Space Model with Independent Retention and Writing for Long-Sequence Memory",
        url="https://arxiv.org/abs/2607.21000",
        track="llm",
        organization="Independent researchers",
        published="2026-07-23",
        topics=("llm-architecture", "state-space-model", "long-context"),
    ),
    run=reproduce_naju,
    render=render,
    fidelity=ReproductionFidelity.CORE_MECHANISM,
    omitted_core_components=(
        "official fused parallel scan kernel",
        "1.2B-token WikiText-103 training",
        "Mamba/Mamba-2/xLSTM/LRA full benchmark matrix",
    ),
))
