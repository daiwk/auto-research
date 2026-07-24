from ..base import PaperMetadata, ReproductionAdapter, ReproductionFidelity
from ..registry import register
from .experiment import reproduce_mobius_rope
from .report import render


ADAPTER = register(ReproductionAdapter(
    key="mobius-rope",
    paper=PaperMetadata(
        arxiv_id="2607.21405",
        title="Anti-Periodic Positional Encoding: Möbius Boundary Conditions Make In-Context Retrieval Reliable",
        url="https://arxiv.org/abs/2607.21405",
        track="llm",
        organization="Independent researcher",
        published="2026-07-23",
        topics=("llm-architecture", "positional-encoding", "long-context"),
    ),
    run=reproduce_mobius_rope,
    render=render,
    fidelity=ReproductionFidelity.CORE_MECHANISM,
    omitted_core_components=(
        "48 runs at 160M/410M parameters",
        "2B FineWeb-Edu tokens per run",
        "six-seed variance significance study",
    ),
))
