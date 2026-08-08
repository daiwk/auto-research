from ..base import PaperMetadata, ReproductionAdapter, ReproductionFidelity
from ..registry import register
from .experiment import reproduce
from .report import render
ADAPTER = register(ReproductionAdapter(key="alibi", paper=PaperMetadata(arxiv_id="2108.12409", title="Train Short, Test Long: Attention with Linear Biases Enables Input Length Extrapolation", url="https://arxiv.org/abs/2108.12409", code_url="https://github.com/ofirpress/attention_with_linear_biases", track="llm", organization="University of Washington / Meta AI", published="2021-08-27", topics=("position-encoding", "length-extrapolation", "attention")), run=reproduce, render=render, fidelity=ReproductionFidelity.CORE_MECHANISM, omitted_core_components=("WikiText-103 scale",)))
