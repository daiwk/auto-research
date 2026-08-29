from ..base import EvaluationTier, PaperMetadata, ReproductionAdapter, ReproductionFidelity
from ..registry import register
from .experiment import render, reproduce_twinkv


ADAPTER = register(ReproductionAdapter(
    key="twinkv",
    paper=PaperMetadata(
        arxiv_id="2608.27128",
        title="TwinKV: A Composable Repair Pass for KV Cache Eviction via Pairwise Key Redundancy",
        url="https://arxiv.org/abs/2608.27128",
        track="llm",
        organization="The Hong Kong University of Science and Technology (Guangzhou)",
        published="2026-08-27",
        topics=("kv-cache", "long-context", "inference-serving", "compression"),
    ),
    run=reproduce_twinkv,
    render=render,
    fidelity=ReproductionFidelity.CORE_MECHANISM,
    omitted_core_components=("full LongBench/LooGLE/RULER matrix", "production KV-cache kernels"),
    evaluation_tier=EvaluationTier.PUBLIC_DATASET,
    datasets=("WikiText-2 long-context checkpoint subset",),
    baseline="StreamingLLM sink + recent eviction at the same KV budget",
    metrics=("attention-output cosine", "repair latency", "KV bytes", "peak GPU memory"),
    device_capabilities=("cuda",),
    infer_device_capabilities=False,
    requires_gpu_validation=True,
    gpu_validation_artifact="docs/gpu-validations/twinkv-a100-20260829.json",
))
