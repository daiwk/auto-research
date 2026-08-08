from ..base import PaperMetadata, ReproductionAdapter, ReproductionFidelity
from ..registry import register
from .experiment import reproduce
from .report import render
ADAPTER = register(ReproductionAdapter(key="awq", paper=PaperMetadata(arxiv_id="2306.00978", title="AWQ: Activation-aware Weight Quantization for LLM Compression and Acceleration", url="https://arxiv.org/abs/2306.00978", code_url="https://github.com/mit-han-lab/llm-awq", track="llm", organization="MIT / NVIDIA / Harvard / SJTU", published="2023-06-01", publication_label="MLSys 2024 Best Paper", topics=("inference-serving", "quantization")), run=reproduce, render=render, fidelity=ReproductionFidelity.CORE_MECHANISM, omitted_core_components=("70B model", "TinyChat kernels")))
