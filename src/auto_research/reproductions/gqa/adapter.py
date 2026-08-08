from ..base import PaperMetadata, ReproductionAdapter, ReproductionFidelity
from ..registry import register
from .experiment import reproduce
from .report import render
ADAPTER = register(ReproductionAdapter(key="gqa", paper=PaperMetadata(arxiv_id="2305.13245", title="GQA: Training Generalized Multi-Query Transformer Models from Multi-Head Checkpoints", url="https://arxiv.org/abs/2305.13245", track="llm", organization="Google Research", published="2023-05-22", topics=("attention", "kv-cache", "serving", "architecture")), run=reproduce, render=render, fidelity=ReproductionFidelity.CORE_MECHANISM, omitted_core_components=("T5-XXL checkpoint uptraining", "production decode benchmark")))
