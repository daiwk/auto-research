from ..base import EvaluationTier, PaperMetadata, ReproductionAdapter, ReproductionFidelity
from ..registry import register
from .experiment import render, reproduce_random_attention


ADAPTER = register(ReproductionAdapter(
    key="random-attention",
    paper=PaperMetadata(
        arxiv_id="2609.03430",
        title="Random Attention: Rethinking KV Cache Eviction for Efficient Reasoning",
        url="https://arxiv.org/abs/2609.03430",
        code_url="https://github.com/SalesforceAIResearch/Random-Attention",
        track="llm",
        organization="Salesforce AI Research / University of Illinois Urbana-Champaign",
        published="2026-09-03",
        publication_label="Salesforce AI Research preprint",
        topics=("kv-cache", "reasoning", "inference-serving", "compression"),
    ),
    run=reproduce_random_attention,
    render=render,
    fidelity=ReproductionFidelity.CORE_MECHANISM,
    omitted_core_components=("full six-task reasoning matrix", "official vLLM serving integration"),
    evaluation_tier=EvaluationTier.PUBLIC_DATASET,
    datasets=("WikiText-2 real-checkpoint subset",),
    baseline="prompt-protected recent-token eviction at equal budget",
    metrics=("attention-output cosine", "selection latency", "KV bytes", "peak GPU memory"),
    evolve_operators=("attention:prompt-protected-random-eviction",),
    device_capabilities=("cuda",), infer_device_capabilities=False,
    requires_gpu_validation=True,
    gpu_validation_artifact="docs/gpu-validations/random-attention-a100-20260906.json",
))
