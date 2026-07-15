from ..base import OnlineABEvidence, PaperMetadata, ReproductionAdapter, ReproductionFidelity
from ..registry import register
from .experiment import reproduce_sigma
from .report import render


ADAPTER = register(
    ReproductionAdapter(
        key="sigma",
        paper=PaperMetadata(
            arxiv_id="2602.22913",
            title="SIGMA: A Semantic-Grounded Instruction-Driven Generative Multi-Task Recommender at AliExpress",
            url="https://arxiv.org/abs/2602.22913",
            track="recommendation",
            organization="Alibaba / AliExpress",
            published="2026-02",
            topics=("generative-recommendation", "multi-task-sft", "hybrid-token", "semantic-grounding"),
            online_ab=(
                OnlineABEvidence("AliExpress", "Order Volume", 2.80, "5% traffic, 2 weeks"),
                OnlineABEvidence("AliExpress", "GMV", 7.84, "5% traffic, 2 weeks"),
            ),
        ),
        run=reproduce_sigma,
        render=render,
        fidelity=ReproductionFidelity.FULL_PIPELINE,
        omitted_core_components=(
            "Qwen3-0.6B/4B scale and 280M private grounding/SFT pairs",
            "AliExpress query, image, festival, trend, demographic and online ranking features",
            "minute-level KV-cache inference and production U2I index serving",
        ),
    )
)
