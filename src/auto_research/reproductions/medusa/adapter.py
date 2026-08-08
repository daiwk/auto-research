from ..base import PaperMetadata, ReproductionAdapter, ReproductionFidelity
from ..registry import register
from .experiment import reproduce
from .report import render
ADAPTER = register(ReproductionAdapter(key="medusa", paper=PaperMetadata(arxiv_id="2401.10774", title="Medusa: Simple LLM Inference Acceleration Framework with Multiple Decoding Heads", url="https://arxiv.org/abs/2401.10774", code_url="https://github.com/FasterDecoding/Medusa", track="llm", organization="Together AI / Princeton University / University of Illinois Urbana-Champaign", published="2024-01-19", topics=("inference-serving", "decoding")), run=reproduce, render=render, fidelity=ReproductionFidelity.CORE_MECHANISM, omitted_core_components=("multi-billion-parameter backbone", "GPU tree-attention kernel")))
