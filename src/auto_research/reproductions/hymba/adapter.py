from ..base import PaperMetadata, ReproductionAdapter, ReproductionFidelity
from ..registry import register
from .experiment import reproduce
from .report import render
ADAPTER = register(ReproductionAdapter(key="hymba", paper=PaperMetadata(arxiv_id="2411.13676", title="Hymba: A Hybrid-head Architecture for Small Language Models", url="https://arxiv.org/abs/2411.13676", code_url="https://github.com/NVlabs/hymba", track="llm", organization="NVIDIA", published="2024-11-20", topics=("hybrid-attention-ssm", "small-language-model", "architecture")), run=reproduce, render=render, fidelity=ReproductionFidelity.CORE_MECHANISM, omitted_core_components=("1.5B pretraining", "learnable meta tokens and fused kernels")))
