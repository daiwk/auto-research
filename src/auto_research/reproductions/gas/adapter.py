from ..base import EvaluationTier, PaperMetadata, ReproductionAdapter, ReproductionFidelity
from ..registry import register
from .experiment import reproduce
from .report import render


ADAPTER = register(ReproductionAdapter(
    key="gas",
    paper=PaperMetadata(
        arxiv_id="2608.12209",
        title=(
            "Generation as Auxiliary Supervision: Enhancing Visual Understanding "
            "at Zero Inference Overhead via Decoupled Embedding Prediction"
        ),
        url="https://arxiv.org/abs/2608.12209",
        track="llm",
        organization="ByteDance",
        published="2026-08-12",
        topics=("multimodal", "generation-guided-training", "next-embedding-prediction"),
    ),
    run=reproduce,
    render=render,
    fidelity=ReproductionFidelity.CORE_MECHANISM,
    omitted_core_components=(
        "Qwen3-VL 2B/4B backbones", "10M generation corpus", "two-stage 32-GPU training",
    ),
    evaluation_tier=EvaluationTier.PUBLIC_DATASET,
    datasets=("Fashion-MNIST object QA",),
    baseline="understanding-only matched trunk",
    metrics=("test_accuracy", "visual_dependency_delta", "deployed_parameter_overhead_percent"),
    device_capabilities=("cpu", "mps", "cuda"),
))
