from ..base import PaperMetadata, ReproductionAdapter, ReproductionFidelity
from ..registry import register
from .experiment import reproduce_adadsf
from .report import render


ADAPTER = register(ReproductionAdapter(
    key="adadsf",
    paper=PaperMetadata(
        arxiv_id="2607.21291",
        title="Adaptive Depth Sparse Framework: Similarity-Driven Resource Allocation for Pre-Trained LLMs",
        url="https://arxiv.org/abs/2607.21291",
        track="llm",
        organization="Huawei ACS Lab / Southern University of Science and Technology",
        published="2026-07-23",
        topics=("llm-architecture", "efficient-inference", "token-routing"),
    ),
    run=reproduce_adadsf,
    render=render,
    fidelity=ReproductionFidelity.CORE_MECHANISM,
    omitted_core_components=(
        "GPT-NeoX-130M and Qwen2.5-0.5B/1.5B checkpoints",
        "WikiText-103 and six full commonsense benchmarks",
        "hardware-level FLOP profiling",
    ),
))
