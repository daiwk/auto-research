from ..base import PaperMetadata, ReproductionAdapter, ReproductionFidelity
from ..registry import register
from .experiment import reproduce_rd_attnres
from .report import render


ADAPTER = register(ReproductionAdapter(
    key="rd-attnres",
    paper=PaperMetadata(
        arxiv_id="2608.01075",
        title="Role-Decoupled Attention Residuals",
        url="https://arxiv.org/abs/2608.01075",
        track="llm",
        organization="Kehan Wang（论文未列机构）",
        published="2026-08-03",
        topics=("foundation-model", "attention", "residual-routing"),
    ),
    run=reproduce_rd_attnres,
    render=render,
    fidelity=ReproductionFidelity.CORE_MECHANISM,
    omitted_core_components=("120M/343M pretraining scale", "paper training corpus"),
))
