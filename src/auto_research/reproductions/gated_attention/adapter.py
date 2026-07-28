from ..base import PaperMetadata, ReproductionAdapter, ReproductionFidelity
from ..llm_evolve_2026_common import render
from ..registry import register
from .experiment import reproduce


ADAPTER = register(ReproductionAdapter(
    key="gated-attention",
    paper=PaperMetadata(
        arxiv_id="2505.06708",
        title="Gated Attention for Large Language Models: Non-linearity, Sparsity, and Attention-Sink-Free",
        url="https://arxiv.org/abs/2505.06708",
        track="llm",
        code_url="https://github.com/qiuzh20/gated_attention",
        organization="Qwen / Alibaba",
        published="2025-05-10",
        topics=("llm-architecture", "attention-gating", "long-context"),
    ),
    run=reproduce,
    render=render,
    fidelity=ReproductionFidelity.CORE_MECHANISM,
    omitted_core_components=(
        "15B-parameter scaling experiments",
        "large-scale learning-rate stability sweep",
        "full long-context benchmark matrix",
    ),
))
