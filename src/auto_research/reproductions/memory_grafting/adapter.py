from ..base import PaperMetadata, ReproductionAdapter, ReproductionFidelity
from ..registry import register
from .experiment import reproduce_memory_grafting
from .report import render


ADAPTER = register(ReproductionAdapter(
    key="memory-grafting",
    paper=PaperMetadata(
        arxiv_id="2605.20948",
        title="Memory Grafting: Scaling Language Model Pre-training via Offline Conditional Memory",
        url="https://arxiv.org/abs/2605.20948",
        track="llm",
        organization="Tsinghua University / Microsoft Research Asia",
        published="2026-05-20",
        topics=("llm-pretraining", "conditional-memory", "offline-knowledge-transfer"),
    ),
    run=reproduce_memory_grafting,
    render=render,
    fidelity=ReproductionFidelity.CORE_MECHANISM,
    omitted_core_components=("0.92B/2.8B MoE recipients", "Qwen3.5/DeepSeek teacher and 3M-entry memory bank"),
))
