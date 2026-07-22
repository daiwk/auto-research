from ..base import PaperMetadata, ReproductionAdapter, ReproductionFidelity
from ..registry import register
from .experiment import reproduce_conv_llm
from .report import render


ADAPTER = register(ReproductionAdapter(
    key="conv-llm",
    paper=PaperMetadata(
        arxiv_id="2607.18413",
        title="Convolution for Large Language Models",
        url="https://arxiv.org/abs/2607.18413",
        track="llm",
        organization="Huawei / Peking University / Tsinghua University",
        published="2026-07-20",
        topics=("llm-architecture", "attention", "depthwise-convolution"),
    ),
    run=reproduce_conv_llm,
    render=render,
    fidelity=ReproductionFidelity.CORE_MECHANISM,
    omitted_core_components=("Qwen3 0.6B–4B full pre-training", "seven downstream benchmark suite"),
))
