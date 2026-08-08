from ..base import PaperMetadata, ReproductionAdapter, ReproductionFidelity
from ..registry import register
from .experiment import reproduce
from .report import render

ADAPTER = register(ReproductionAdapter(
    key="open-language-model",
    paper=PaperMetadata(
        arxiv_id="2607.16669",
        title="OpenLanguageModel: Readable and Composable Small-Language-Model Pretraining for Education and Research",
        url="https://arxiv.org/abs/2607.16669",
        track="llm",
        code_url="https://github.com/openlanguagemodel/openlanguagemodel",
        organization="Indian Institute of Technology Madras",
        published="2026-07-18",
        topics=("pretraining-infrastructure", "composable-architecture", "small-language-model", "evolve"),
    ),
    run=reproduce, render=render, fidelity=ReproductionFidelity.CORE_MECHANISM,
    omitted_core_components=("complete upstream 27-preset package", "348M four-GPU weak-scaling experiment"),
))
