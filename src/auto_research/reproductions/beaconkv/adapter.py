from ..base import EvaluationTier, PaperMetadata, ReproductionAdapter, ReproductionFidelity
from ..registry import register
from .experiment import render, reproduce


ADAPTER = register(ReproductionAdapter(
    key="beaconkv",
    paper=PaperMetadata(
        arxiv_id="2609.04971", title="BeaconKV: Key-Value Cache Compression Guided by Beacon Queries for Efficient Large Reasoning Model Inference",
        url="https://arxiv.org/abs/2609.04971", track="llm", organization="Hanyang University",
        published="2026-09-04", topics=("kv-cache", "long-context", "reasoning", "inference-serving"),
    ),
    run=reproduce, render=render, fidelity=ReproductionFidelity.CORE_MECHANISM,
    omitted_core_components=("four-model reasoning benchmark matrix", "vLLM throughput integration"),
    evaluation_tier=EvaluationTier.PUBLIC_DATASET, datasets=("public-domain long-context probe",),
    baseline="equal-budget recent-token KV retention", metrics=("attention-output cosine", "retained tokens", "peak GPU memory"),
    evolve_operators=("attention:beacon-query-kv",), device_capabilities=("cuda",), infer_device_capabilities=False,
    requires_gpu_validation=True, gpu_validation_artifact="docs/gpu-validations/beaconkv-a100-20260907.json",
))
