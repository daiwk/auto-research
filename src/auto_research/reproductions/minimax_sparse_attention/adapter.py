from ..base import PaperMetadata, ReproductionAdapter, ReproductionFidelity
from ..registry import register
from .experiment import reproduce_minimax_sparse_attention
from .report import render

ADAPTER = register(ReproductionAdapter(
    key="minimax-sparse-attention", paper=PaperMetadata(
        arxiv_id="2606.13392", title="MiniMax Sparse Attention",
        url="https://arxiv.org/abs/2606.13392", track="llm",
        code_url="https://github.com/MiniMax-AI/MSA",
        organization="MiniMax", published="2026-06-11",
        topics=("llm", "sparse-attention", "gqa", "long-context"),
    ), run=reproduce_minimax_sparse_attention, render=render,
    fidelity=ReproductionFidelity.CORE_MECHANISM,
    omitted_core_components=("109B pretraining", "official fused H800 kernel"),
))
