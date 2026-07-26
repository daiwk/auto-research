from ..base import PaperMetadata, ReproductionAdapter, ReproductionFidelity
from ..registry import register
from .experiment import reproduce_windowed_mtp
from .report import render


ADAPTER = register(ReproductionAdapter(
    key="windowed-mtp",
    paper=PaperMetadata(
        arxiv_id="2607.21535",
        title="Windowed-MTP: Removing the Full-Context Draft-KV Tax at Million-Token Context",
        url="https://arxiv.org/abs/2607.21535",
        code_url="https://github.com/avalliappan-nvidia/windowed-mtp-b200",
        track="llm",
        organization="NVIDIA",
        published="2026-07-23",
        topics=("llm-serving", "speculative-decoding", "kv-cache", "long-context"),
    ),
    run=reproduce_windowed_mtp,
    render=render,
    fidelity=ReproductionFidelity.CORE_MECHANISM,
    omitted_core_components=(
        "Qwen3.6-35B/122B and Nemotron-3-120B checkpoints",
        "one-million-token contexts on B200/H100",
        "SGLang paged-KV ring-buffer kernel and continuous batching",
    ),
))
