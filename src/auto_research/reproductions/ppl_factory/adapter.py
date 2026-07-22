from ..base import PaperMetadata, ReproductionAdapter, ReproductionFidelity
from ..registry import register
from .experiment import reproduce_ppl_factory
from .report import render


ADAPTER = register(ReproductionAdapter(
    key="ppl-factory",
    paper=PaperMetadata(
        arxiv_id="2607.18199", title="PPL-Factory: Task-Aware and Budget-Aware Data Selection from Language Modeling to Reasoning",
        url="https://arxiv.org/abs/2607.18199", track="llm",
        organization="McGill University", published="2026-07-20",
        topics=("llm-training", "data-selection", "efficient-finetuning"),
    ),
    run=reproduce_ppl_factory, render=render,
    fidelity=ReproductionFidelity.CORE_MECHANISM,
    omitted_core_components=("Qwen2.5-7B reasoning SFT", "GSM8K and MATH answer accuracy"),
))
