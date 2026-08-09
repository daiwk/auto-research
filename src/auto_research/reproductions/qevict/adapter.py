from ..base import PaperMetadata, ReproductionAdapter, ReproductionFidelity
from ..registry import register
from ..latest_20260809_common import reproduce_qevict, render_latest

ADAPTER = register(ReproductionAdapter(
    key="qevict", paper=PaperMetadata(arxiv_id="2608.05326", title="QEvict: Recoverable Quantized KV Eviction for Attention-Drift-Robust Long-Context Decoding",
        url="https://arxiv.org/abs/2608.05326", track="llm", organization="Indian Institute of Technology Roorkee",
        published="2026-08-05", topics=("long-context", "kv-cache", "quantization", "serving")),
    run=reproduce_qevict, render=render_latest, fidelity=ReproductionFidelity.CORE_MECHANISM,
    omitted_core_components=("transformer KV kernels", "full long-context benchmark"),
))
