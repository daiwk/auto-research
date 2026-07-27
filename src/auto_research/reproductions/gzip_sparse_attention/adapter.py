from ..base import PaperMetadata, ReproductionAdapter, ReproductionFidelity
from ..registry import register
from .experiment import reproduce_gzip_sparse_attention
from .report import render


ADAPTER = register(ReproductionAdapter(
    key="gzip-sparse-attention",
    paper=PaperMetadata(
        arxiv_id="2607.21752",
        title="Parameter-free Adaptive Sparse Attention via Compression-Based Content Selection",
        url="https://arxiv.org/abs/2607.21752",
        track="llm",
        organization="Pennsylvania State University",
        published="2026-07-23",
        topics=("llm", "sparse-attention", "long-context", "compression"),
    ),
    run=reproduce_gzip_sparse_attention,
    render=render,
    fidelity=ReproductionFidelity.CORE_MECHANISM,
    omitted_core_components=(
        "92M-parameter 12-layer ByteLM and 20K-step multi-H100 training",
        "PG-19 full 8K-byte training corpus",
        "true block-sparse attention kernel",
    ),
))
