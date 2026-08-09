from ..base import PaperMetadata, ReproductionAdapter, ReproductionFidelity
from ..registry import register
from ..latest_20260809_common import reproduce_bakron, render_latest

ADAPTER = register(ReproductionAdapter(
    key="bakron", paper=PaperMetadata(arxiv_id="2608.06291", title="BaKron: Efficient Quantization with Kronecker-Factored Hessians",
        url="https://arxiv.org/abs/2608.06291", track="llm", organization="University of California, San Diego",
        published="2026-08-06", topics=("quantization", "hessian", "inference-efficiency")),
    run=reproduce_bakron, render=render_latest, fidelity=ReproductionFidelity.CORE_MECHANISM,
    omitted_core_components=("anti-diagonal GPU solver", "full pretrained model quantization sweep"),
))
