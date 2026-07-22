from ..base import PaperMetadata, ReproductionAdapter, ReproductionFidelity
from ..registry import register
from .experiment import reproduce_slimper
from .report import render


ADAPTER = register(ReproductionAdapter(
    key="slimper",
    paper=PaperMetadata(
        arxiv_id="2607.12281", title="SlimPer: Make Personalization Model Slim and Smart",
        url="https://arxiv.org/abs/2607.12281", track="recommendation", organization="Meta Platforms, Inc.", published="2026-07-14",
        topics=("ranking", "long-sequence", "serving-efficiency"),
        selection_exception="User explicitly accepts the paper's statistically significant full-traffic Instagram launch as online evidence although exact lift percentages are undisclosed.",
    ),
    run=reproduce_slimper, render=render,
    fidelity=ReproductionFidelity.CORE_MECHANISM,
    omitted_core_components=("Instagram private multimodal data", "1k–10k+ history and production kernels", "multi-task Shampoo training"),
))
