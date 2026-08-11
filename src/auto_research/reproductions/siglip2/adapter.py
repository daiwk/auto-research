from ..base import EvaluationTier, PaperMetadata, ReproductionAdapter, ReproductionFidelity
from ..registry import register
from .experiment import reproduce
from .report import render


ADAPTER = register(ReproductionAdapter(
    key="siglip2",
    paper=PaperMetadata(
        arxiv_id="2502.14786",
        title="SigLIP 2: Multilingual Vision-Language Encoders with Improved Semantic Understanding, Localization, and Dense Features",
        url="https://arxiv.org/abs/2502.14786",
        code_url="https://github.com/google-research/big_vision",
        track="llm",
        organization="Google DeepMind",
        published="2025-02-20",
        topics=("multimodal", "sigmoid-contrastive", "self-distillation"),
    ),
    run=reproduce,
    render=render,
    fidelity=ReproductionFidelity.CORE_MECHANISM,
    omitted_core_components=("multilingual web-scale mixture", "caption decoder", "dense localization heads"),
    evaluation_tier=EvaluationTier.PUBLIC_DATASET,
    datasets=("Fashion-MNIST image-text pairs",),
    baseline="uniform label retrieval",
    metrics=("test_accuracy", "visual_dependency_delta"),
    device_capabilities=("cpu", "mps", "cuda"),
))
