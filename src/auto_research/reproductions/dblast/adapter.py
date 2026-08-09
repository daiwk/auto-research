from ..base import PaperMetadata, ReproductionAdapter, ReproductionFidelity
from ..registry import register
from ..latest_20260809_common import reproduce_dblast, render_latest

ADAPTER = register(ReproductionAdapter(
    key="dblast", paper=PaperMetadata(arxiv_id="2608.05448", title="DBLast: Dependent Block Drafting for Stochastic Speculative Decoding",
        url="https://arxiv.org/abs/2608.05448", track="llm", organization="Huawei Technologies Canada",
        published="2026-08-05", topics=("speculative-decoding", "inference-efficiency", "stochastic-decoding")),
    run=reproduce_dblast, render=render_latest, fidelity=ReproductionFidelity.CORE_MECHANISM,
    omitted_core_components=("Qwen3 checkpoints", "GPU block-drafter kernels"),
))
