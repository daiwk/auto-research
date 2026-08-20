from ..base import EvaluationTier, OnlineABEvidence, PaperMetadata, ReproductionAdapter, ReproductionFidelity
from ..registry import register
from .experiment import reproduce_dream
from .report import render


ADAPTER = register(ReproductionAdapter(
    key="dream",
    paper=PaperMetadata(
        arxiv_id="2608.09408", title="DREAM: A Dual-Loop Recommendation Evolution Framework Powered by Large Language Models", url="https://arxiv.org/abs/2608.09408", track="recommendation",
        organization="Taobao & Tmall Group / Alibaba", published="2026-08-10",
        topics=("llm-recommendation", "ranking", "reranking", "intent-understanding", "online-policy", "serving"),
        online_ab=(
            OnlineABEvidence("Taobao homepage recommendation", "IPV", 2.71, "platform-scale online deployment of fine-rank + rerank", source_url="https://arxiv.org/pdf/2608.09408", source_location="Section 5.3.1 Table 7", retrieved_at="2026-08-20"),
            OnlineABEvidence("Taobao homepage recommendation", "Core IPV", 3.06, "platform-scale online deployment of fine-rank + rerank", source_url="https://arxiv.org/pdf/2608.09408", source_location="Section 5.3.1 Table 7", retrieved_at="2026-08-20"),
            OnlineABEvidence("Taobao homepage recommendation", "GMV", 1.31, "platform-scale online deployment of fine-rank + rerank", source_url="https://arxiv.org/pdf/2608.09408", source_location="Section 5.3.1 Table 7", retrieved_at="2026-08-20"),
        ),
    ),
    run=reproduce_dream, render=render,
    fidelity=ReproductionFidelity.CORE_MECHANISM,
    omitted_core_components=("Taobao private multi-source signals and production traffic", "Qwen3 Meta Engine and online conclusion feedback"),
    evaluation_tier=EvaluationTier.PUBLIC_DATASET,
    datasets=("MovieLens-1M",), baseline="retrieval/ranking backbone without DREAM overlay",
    metrics=("Hit@10", "NDCG@10", "Fresh Hit@10", "Head share@10"),
    budget="3 offline replay generations", device_capabilities=("cpu",),
))
