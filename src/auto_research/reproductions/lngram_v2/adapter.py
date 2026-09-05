from ..base import EvaluationTier, PaperMetadata, ReproductionAdapter, ReproductionFidelity
from ..registry import register
from .experiment import render, reproduce_lngram_v2


ADAPTER=register(ReproductionAdapter(
    key="lngram-v2",paper=PaperMetadata(arxiv_id="2609.03426",title="Lngram v2: Latent N-Gram Memory with Interpretable Discrete Representations",url="https://arxiv.org/abs/2609.03426",track="llm",organization="Beijing University of Posts and Telecommunications / Kuaishou Technology",published="2026-09-03",publication_label="ICLR 2027",topics=("multimodal-foundation-model","conditional-memory","discrete-routing","model-architecture")),
    run=reproduce_lngram_v2,render=render,fidelity=ReproductionFidelity.CORE_MECHANISM,
    omitted_core_components=("Keye 2B/30B pretraining","paper-scale multimodal corpus"),evaluation_tier=EvaluationTier.PUBLIC_DATASET,
    datasets=("Qwen2.5-VL-3B-Instruct checkpoint + deterministic RGB geometry probe",),baseline="same checkpoint without latent memory branch",metrics=("finite output","route diversity","sink selectivity","activation memory"),
    evolve_operators=("memory:latent-ngram-gqa",),device_capabilities=("cuda",),infer_device_capabilities=False,requires_gpu_validation=True,gpu_validation_artifact="docs/gpu-validations/lngram-v2-a100-20260906.json",
))
