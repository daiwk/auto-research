from ..base import PaperMetadata, ReproductionAdapter, ReproductionFidelity
from ..llm_evolve_2026_common import render
from ..registry import register
from .experiment import reproduce


ADAPTER = register(ReproductionAdapter(
    key="muon",
    paper=PaperMetadata(
        arxiv_id="2502.16982",
        title="Muon is Scalable for LLM Training",
        url="https://arxiv.org/abs/2502.16982",
        track="llm",
        code_url="https://github.com/MoonshotAI/Moonlight",
        organization="Moonshot AI / UCLA",
        published="2025-02-24",
        topics=("llm-training", "optimizer", "training-efficiency"),
    ),
    run=reproduce,
    render=render,
    fidelity=ReproductionFidelity.CORE_MECHANISM,
    omitted_core_components=(
        "distributed optimizer state and communication implementation",
        "3B/16B MoE models and 5.7T-token training",
        "large-scale compute-optimal frontier",
    ),
))
