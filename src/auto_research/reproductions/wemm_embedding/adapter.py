from ..base import EvaluationTier, PaperMetadata, ReproductionAdapter, ReproductionFidelity
from ..registry import register
from .experiment import reproduce_wemm_embedding
from .report import render


ADAPTER = register(ReproductionAdapter(
    key="wemm-embedding",
    paper=PaperMetadata(
        arxiv_id="2608.24053",
        title="WeMM-Embedding: WeChat Multi-Modal Embedding Technical Report",
        url="https://arxiv.org/abs/2608.24053",
        track="llm",
        code_url="https://github.com/Tencent/WeMM-Embedding",
        organization="WeChat Vision, Tencent",
        published="2026-08-25",
        topics=("multimodal-foundation-model", "embedding", "retrieval", "matryoshka-representation"),
    ),
    run=reproduce_wemm_embedding,
    render=render,
    fidelity=ReproductionFidelity.CORE_MECHANISM,
    omitted_core_components=("2B/4B/9B released checkpoints", "hundreds of millions of private pairs", "WeChat production indexes"),
    evaluation_tier=EvaluationTier.PUBLIC_DATASET,
    datasets=("MovieLens-1M paired content/collaborative views",),
    baseline="stage-1 multimodal alignment without refinement",
    metrics=("Recall@1", "Recall@10", "MRR"),
    device_capabilities=("cpu",),
    infer_device_capabilities=False,
))
