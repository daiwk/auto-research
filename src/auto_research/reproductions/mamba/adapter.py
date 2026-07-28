from ..base import PaperMetadata, ReproductionAdapter, ReproductionFidelity
from ..llm_evolve_2026_common import render
from ..registry import register
from .experiment import reproduce

ADAPTER = register(ReproductionAdapter(
    key="mamba",
    paper=PaperMetadata(
        arxiv_id="2312.00752", title="Mamba: Linear-Time Sequence Modeling with Selective State Spaces",
        url="https://arxiv.org/abs/2312.00752", track="llm",
        code_url="https://github.com/state-spaces/mamba",
        organization="Carnegie Mellon University / Princeton University",
        published="2023-12-01", topics=("llm-architecture", "state-space-model", "classic"),
    ),
    run=reproduce, render=render, fidelity=ReproductionFidelity.CORE_MECHANISM,
    omitted_core_components=("fused parallel selective-scan CUDA kernel", "2.8B-scale pretraining"),
))
