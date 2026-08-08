from ..base import PaperMetadata, ReproductionAdapter, ReproductionFidelity
from ..registry import register
from .experiment import reproduce
from .report import render
ADAPTER = register(ReproductionAdapter(key="moba", paper=PaperMetadata(arxiv_id="2502.13189", title="MoBA: Mixture of Block Attention for Long-Context LLMs", url="https://arxiv.org/abs/2502.13189", code_url="https://github.com/MoonshotAI/MoBA", track="llm", organization="Moonshot AI", published="2025-02-18", topics=("sparse-attention", "long-context", "block-routing")), run=reproduce, render=render, fidelity=ReproductionFidelity.CORE_MECHANISM, omitted_core_components=("million-token training", "fused sparse kernel")))
