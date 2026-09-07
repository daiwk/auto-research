from ..base import EvaluationTier, PaperMetadata, ReproductionAdapter, ReproductionFidelity
from ..registry import register
from .experiment import render, reproduce


ADAPTER = register(ReproductionAdapter(
    key="kvmem",
    paper=PaperMetadata(
        arxiv_id="2609.04852", title="KVMem: Virtualizing Million-Token Agent Workspaces on a Consumer GPU",
        url="https://arxiv.org/abs/2609.04852", code_url="https://github.com/kvmem/kvmem-qw3", track="llm",
        organization="Shanghai University of Finance and Economics", published="2026-09-04",
        topics=("agent-memory", "kv-cache", "long-context", "inference-serving"),
    ),
    run=reproduce, render=render, fidelity=ReproductionFidelity.CORE_MECHANISM,
    omitted_core_components=("NVMe asynchronous paging engine", "QW3 production inference integration", "million-token benchmark matrix"),
    evaluation_tier=EvaluationTier.PUBLIC_DATASET, datasets=("public-domain long-context probe",),
    baseline="equal-budget recent-context compaction", metrics=("attention-output cosine", "materialized blocks", "peak GPU memory"),
    evolve_operators=("memory:query-conditioned-paged-kv",), device_capabilities=("cuda",), infer_device_capabilities=False,
    requires_gpu_validation=True, gpu_validation_artifact="docs/gpu-validations/kvmem-a100-20260907.json",
))
