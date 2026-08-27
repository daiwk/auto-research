from ..base import EvaluationTier, PaperMetadata, ReproductionAdapter, ReproductionFidelity
from ..registry import register
from .experiment import reproduce_vbvr_pro
from .report import render


ADAPTER = register(ReproductionAdapter(
    key="vbvr-pro",
    paper=PaperMetadata(
        arxiv_id="2608.26105", title="VBVR-Pro: A Scalable and Verifiable Suite for Native Visual Reasoning",
        url="https://arxiv.org/abs/2608.26105", track="llm",
        code_url="https://www.video-reason.com/?v=pro",
        organization="Nanyang Technological University / VBVR Community",
        published="2026-08-26",
        topics=("multimodal-foundation-model", "native-visual-reasoning", "verifiable-reward", "benchmark"),
    ),
    run=reproduce_vbvr_pro, render=render,
    fidelity=ReproductionFidelity.CORE_MECHANISM,
    omitted_core_components=("released large video/image generators", "seven external transfer benchmarks", "large-scale multi-task RL"),
    evaluation_tier=EvaluationTier.MECHANISM,
    datasets=("VBVR-Pro procedural task specification",),
    baseline="scalar VLM-as-a-judge analogue on the same 300 generated tasks",
    metrics=("reward mean", "reward standard deviation", "deterministic verifier agreement"),
    device_capabilities=("cpu",), infer_device_capabilities=False,
))
