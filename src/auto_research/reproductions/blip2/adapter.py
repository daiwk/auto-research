from ..base import EvaluationTier, PaperMetadata, ReproductionAdapter, ReproductionFidelity
from ..registry import register
from .experiment import reproduce
from .report import render


ADAPTER = register(ReproductionAdapter(
    key="blip2",
    paper=PaperMetadata(
        arxiv_id="2301.12597",
        title="BLIP-2: Bootstrapping Language-Image Pre-training with Frozen Image Encoders and Large Language Models",
        url="https://arxiv.org/abs/2301.12597",
        code_url="https://github.com/salesforce/LAVIS",
        track="llm",
        organization="Salesforce Research",
        published="2023-01-30",
        publication_label="ICML 2023",
        topics=("multimodal", "q-former", "frozen-encoders"),
    ),
    run=reproduce,
    render=render,
    fidelity=ReproductionFidelity.CORE_MECHANISM,
    omitted_core_components=("frozen ViT-g and OPT/FlanT5", "two-stage web-scale pretraining"),
    evaluation_tier=EvaluationTier.PUBLIC_DATASET,
    datasets=("Fashion-MNIST object QA",),
    baseline="linear mean-pooled connector",
    metrics=("test_accuracy", "visual_dependency_delta", "visual_tokens"),
    device_capabilities=("cpu", "mps", "cuda"),
))
