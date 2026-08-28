from ..base import EvaluationTier, PaperMetadata, ReproductionAdapter, ReproductionFidelity
from ..registry import register
from .experiment import reproduce_mllmclip
from .report import render


ADAPTER = register(ReproductionAdapter(
    key="mllmclip",
    paper=PaperMetadata(
        arxiv_id="2608.25575", title="MLLMCLIP: Feature-Level Distillation of MLLM for Robust Vision-Language Representations",
        url="https://arxiv.org/abs/2608.25575", track="llm",
        organization="KAIST / Sony AI", published="2026-08-26",
        topics=("multimodal-foundation-model", "feature-distillation", "compositionality", "cka"),
    ),
    run=reproduce_mllmclip, render=render,
    fidelity=ReproductionFidelity.CORE_MECHANISM,
    omitted_core_components=("paper-scale vision compositionality suite", "full CLIP pretraining"),
    evaluation_tier=EvaluationTier.PUBLIC_DATASET,
    datasets=("CIFAR-10 public checkpoint subset", "MovieLens-1M diagnostic proxy"),
    baseline="frozen CLIP features with an untrained matched projection",
    metrics=("linear CKA", "1-NN accuracy", "training loss", "peak GPU memory"),
    device_capabilities=("cuda",), infer_device_capabilities=False,
    requires_gpu_validation=True,
    gpu_validation_artifact="docs/gpu-validations/mllmclip-a100-20260828.json",
))
