from ..base import PaperMetadata, ReproductionAdapter, ReproductionFidelity
from ..llm_evolve_2026_common import render
from ..registry import register
from .experiment import reproduce

ADAPTER = register(ReproductionAdapter(
    key="switch-attention",
    paper=PaperMetadata(
        arxiv_id="2603.26380", title="Switch Attention: Towards Dynamic and Fine-grained Hybrid Transformers",
        url="https://arxiv.org/abs/2603.26380", track="llm",
        organization="Peking University / Huawei Technologies",
        published="2026-03-27", topics=("llm-architecture", "efficient-attention", "long-context"),
    ),
    run=reproduce, render=render, fidelity=ReproductionFidelity.CORE_MECHANISM,
    omitted_core_components=("32K continual pretraining", "branch-selective fused decode kernel"),
))
