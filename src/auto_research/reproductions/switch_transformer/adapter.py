from ..base import PaperMetadata, ReproductionAdapter, ReproductionFidelity
from ..llm_evolve_2026_common import render
from ..registry import register
from .experiment import reproduce

ADAPTER = register(ReproductionAdapter(
    key="switch-transformer",
    paper=PaperMetadata(
        arxiv_id="2101.03961", title="Switch Transformers: Scaling to Trillion Parameter Models with Simple and Efficient Sparsity",
        url="https://arxiv.org/abs/2101.03961", track="llm",
        code_url="https://github.com/tensorflow/mesh",
        organization="Google Brain", published="2021-01-11",
        topics=("llm-architecture", "mixture-of-experts", "classic"),
    ),
    run=reproduce, render=render, fidelity=ReproductionFidelity.CORE_MECHANISM,
    omitted_core_components=("trillion-parameter distributed training", "expert capacity overflow/all-to-all communication"),
))
