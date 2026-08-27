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
    omitted_core_components=("generative MLLM teacher checkpoint", "vision compositionality benchmarks", "full CLIP pretraining"),
    evaluation_tier=EvaluationTier.MECHANISM,
    datasets=("MovieLens-1M public content/collaborative proxy",),
    baseline="same student features without attention selection or CKA projection",
    metrics=("Recall@10", "linear CKA", "attention selected fraction"),
    device_capabilities=("cpu",), infer_device_capabilities=False,
))
