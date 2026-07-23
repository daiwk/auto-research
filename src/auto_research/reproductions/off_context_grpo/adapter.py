from ..base import PaperMetadata, ReproductionAdapter, ReproductionFidelity
from ..registry import register
from .experiment import reproduce_off_context_grpo
from .report import render


ADAPTER = register(ReproductionAdapter(
    key="off-context-grpo",
    paper=PaperMetadata(
        arxiv_id="2607.19313",
        title="Off-Context GRPO: Learning to Reason on Hard Problems using Privileged Information",
        url="https://arxiv.org/abs/2607.19313",
        code_url="https://github.com/AgPriyank/OC-GRPO",
        track="llm",
        organization="Meta AI / Columbia University",
        published="2026-07-21",
        topics=("rlvr", "grpo", "reasoning", "privileged-information"),
    ),
    run=reproduce_off_context_grpo,
    render=render,
    fidelity=ReproductionFidelity.CORE_MECHANISM,
    omitted_core_components=("Qwen2.5 1.5B/3B/7B token-level rollouts", "multi-GPU veRL training stack"),
))
