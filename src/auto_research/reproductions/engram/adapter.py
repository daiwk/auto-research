from ..base import PaperMetadata, ReproductionAdapter, ReproductionFidelity
from ..llm_evolve_2026_common import render
from ..registry import register
from .experiment import reproduce_engram


ADAPTER = register(ReproductionAdapter(
    key="engram",
    paper=PaperMetadata(
        arxiv_id="2601.07372",
        title="Conditional Memory via Scalable Lookup: A New Axis of Sparsity for Large Language Models",
        url="https://arxiv.org/abs/2601.07372", track="llm",
        code_url="https://github.com/deepseek-ai/Engram",
        organization="DeepSeek", published="2026-01-12",
        topics=("llm-architecture", "conditional-memory", "sparsity"),
    ),
    run=reproduce_engram, render=render,
    fidelity=ReproductionFidelity.CORE_MECHANISM,
    omitted_core_components=("27B-scale pretraining", "distributed memory prefetch infrastructure"),
))
