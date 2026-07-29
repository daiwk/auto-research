from ..base import PaperMetadata, ReproductionAdapter, ReproductionFidelity
from ..llm_evolve_2026_common import render
from ..registry import register
from .experiment import reproduce_penelope


ADAPTER = register(ReproductionAdapter(
    key="penelope",
    paper=PaperMetadata(
        arxiv_id="2607.25915",
        title="Penelope: Localized Latent Recurrence for Efficient Structured Reasoning",
        url="https://arxiv.org/abs/2607.25915",
        track="llm",
        organization="Academic author team",
        published="2026-07-28",
        topics=("llm-architecture", "latent-reasoning", "recurrence", "efficiency"),
    ),
    run=reproduce_penelope,
    render=render,
    fidelity=ReproductionFidelity.CORE_MECHANISM,
    omitted_core_components=("pretrained decoder checkpoint", "progressive CoT-to-latent curriculum at paper scale"),
))
