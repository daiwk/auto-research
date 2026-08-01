from ..base import PaperMetadata, ReproductionAdapter, ReproductionFidelity
from ..llm_evolve_2026_common import render
from ..registry import register
from .experiment import reproduce_wide


ADAPTER = register(ReproductionAdapter(
    key="wide",
    paper=PaperMetadata(
        arxiv_id="2607.28418", title="WIDE: Boosting Adaptive LLM Inference via Token-level Dynamic Width Pruning",
        url="https://arxiv.org/abs/2607.28418", track="llm",
        code_url="https://github.com/EIT-NLP/LLM-Pruning/tree/main/WIDE",
        organization="EIT-NLP / LMU Munich", published="2026-07-30",
        topics=("llm-architecture", "dynamic-pruning", "inference-efficiency"),
    ),
    run=reproduce_wide, render=render,
    fidelity=ReproductionFidelity.CORE_MECHANISM,
    omitted_core_components=("custom CUDA kernels", "billion-parameter two-stage calibration"),
))
