from ..base import OnlineABEvidence, PaperMetadata, ReproductionAdapter, ReproductionFidelity
from ..registry import register
from .experiment import reproduce_akt_rec
from .report import render


ADAPTER = register(
    ReproductionAdapter(
        key="akt-rec",
        paper=PaperMetadata(
            arxiv_id="2605.23310",
            title="From Head to Tail: Asymmetric Knowledge Transfer in Long-tail Recommendation with Generative Semantic IDs",
            url="https://arxiv.org/abs/2605.23310",
            track="recommendation",
            organization="Alibaba Group / Peking University",
            published="2026-05-22",
            topics=("llm-recommendation", "semantic-id", "long-tail", "ctr-ranking"),
            online_ab=(
                OnlineABEvidence("Tmall", "CTR", 2.76, "10% control / 10% treatment, two weeks"),
                OnlineABEvidence("Tmall", "GMV", 3.47, "10% control / 10% treatment, two weeks"),
            ),
        ),
        run=reproduce_akt_rec,
        render=render,
        fidelity=ReproductionFidelity.CORE_MECHANISM,
        omitted_core_components=(
            "GME-Qwen2-VL-7B images/statistics and Qwen3-30B-A3B scale",
            "36M-user/300M-item Tmall data and production cluster-feature store",
        ),
    )
)
