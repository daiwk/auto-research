from ..base import PaperMetadata, ReproductionAdapter, ReproductionFidelity
from ..llm_evolve_2026_common import render
from ..registry import register
from .experiment import reproduce


ADAPTER = register(ReproductionAdapter(
    key="native-sparse-attention",
    paper=PaperMetadata(
        arxiv_id="2502.11089",
        title="Native Sparse Attention: Hardware-Aligned and Natively Trainable Sparse Attention",
        url="https://arxiv.org/abs/2502.11089",
        track="llm",
        organization="DeepSeek",
        published="2025-02-16",
        topics=("llm-architecture", "sparse-attention", "long-context"),
    ),
    run=reproduce,
    render=render,
    fidelity=ReproductionFidelity.CORE_MECHANISM,
    omitted_core_components=(
        "custom Triton kernels and hardware speed claims",
        "27B-parameter continued pretraining",
        "64K-context benchmark matrix",
    ),
))
