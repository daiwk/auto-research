from ..base import EvaluationTier, PaperMetadata, ReproductionAdapter, ReproductionFidelity
from ..registry import register
from .experiment import render, reproduce_pace_vlm


ADAPTER = register(ReproductionAdapter(
    key="pace-vlm",
    paper=PaperMetadata(
        arxiv_id="2608.27206",
        title="PACE: A Unified Condense-and-Extract Paradigm for Fast VLM Inference",
        url="https://arxiv.org/abs/2608.27206",
        code_url="https://github.com/jjL357/PACE",
        track="llm",
        organization="Sun Yat-sen University",
        published="2026-08-27",
        topics=("multimodal-foundation-model", "visual-token-compression", "inference-serving"),
    ),
    run=reproduce_pace_vlm,
    render=render,
    fidelity=ReproductionFidelity.CORE_MECHANISM,
    omitted_core_components=("paper-scale benchmark suite", "custom fused serving kernels"),
    evaluation_tier=EvaluationTier.PUBLIC_DATASET,
    datasets=("RealWorldQA checkpoint subset",),
    baseline="Qwen2.5-VL at the original visual-token budget",
    metrics=("answer accuracy", "visual tokens", "latency", "peak GPU memory"),
    device_capabilities=("cuda",),
    infer_device_capabilities=False,
    requires_gpu_validation=True,
    gpu_validation_artifact="docs/gpu-validations/pace-vlm-a100-20260829.json",
))
