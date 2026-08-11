from ..base import EvaluationTier, PaperMetadata, ReproductionAdapter, ReproductionFidelity
from ..registry import register
from .experiment import reproduce
from .report import render


ADAPTER = register(ReproductionAdapter(
    key="smolvlm",
    paper=PaperMetadata(
        arxiv_id="2504.05299",
        title="SmolVLM: Redefining small and efficient multimodal models",
        url="https://arxiv.org/abs/2504.05299",
        code_url="https://github.com/huggingface/smollm",
        track="llm",
        organization="Hugging Face",
        published="2025-04-07",
        topics=("multimodal", "efficient-vlm", "visual-token-compression"),
    ),
    run=reproduce,
    render=render,
    fidelity=ReproductionFidelity.CORE_MECHANISM,
    omitted_core_components=("256M-2.2B language decoder", "large multimodal data recipe", "video training"),
    evaluation_tier=EvaluationTier.PUBLIC_DATASET,
    datasets=("Fashion-MNIST object QA",),
    baseline="linear mean-pooled connector",
    metrics=("test_accuracy", "visual_dependency_delta", "visual_tokens"),
    device_capabilities=("cpu", "mps", "cuda"),
))
