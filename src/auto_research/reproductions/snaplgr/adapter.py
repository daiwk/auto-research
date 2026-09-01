from ..base import EvaluationTier, OnlineABEvidence, PaperMetadata, ReproductionAdapter, ReproductionFidelity
from ..registry import register
from .experiment import reproduce_snaplgr
from .report import render


ADAPTER = register(
    ReproductionAdapter(
        key="snaplgr",
        paper=PaperMetadata(
            arxiv_id="2607.28895",
            title="LLM-Based Generative Retrieval for Snapchat Content Recommendation",
            url="https://arxiv.org/abs/2607.28895",
            track="recommendation",
            organization="Snap Inc.",
            published="2026-07-30",
            topics=("retrieval", "generative-recommendation", "semantic-id", "llm", "multimodal"),
            online_ab=(
                OnlineABEvidence(
                    "Snapchat content recommendation",
                    "View Time",
                    0.37,
                    "7-day production A/B test",
                    source_url="https://arxiv.org/html/2607.28895v1",
                    source_location="Section 4.5, Table 8",
                    significance="p = 0.007",
                    retrieved_at="2026-09-01",
                ),
            ),
        ),
        run=reproduce_snaplgr,
        render=render,
        fidelity=ReproductionFidelity.CORE_MECHANISM,
        omitted_core_components=("pretrained LLM and Qwen3-VL", "TensorRT-LLM CUDA beam search", "64-A100 worker loop"),
        evaluation_tier=EvaluationTier.PUBLIC_DATASET,
        datasets=("MovieLens 100K content/co-engagement proxy",),
        baseline="vanilla residual-quantized semantic IDs",
        metrics=("hit_at_10", "ndcg_at_10", "sid_utilization", "sid_collision_rate"),
        evolve_operators=("head:snaplgr-sid",),
        default_seeds=(42, 43, 44),
        budget="220 users / 360 items; 3-level width-8 SID",
        device_capabilities=("cpu",),
    )
)
