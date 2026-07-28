from ..base import OnlineABEvidence, PaperMetadata, ReproductionAdapter, ReproductionFidelity
from ..registry import register
from .experiment import reproduce_unir2
from .report import render


ADAPTER = register(
    ReproductionAdapter(
        key="unir2",
        paper=PaperMetadata(
            arxiv_id="2607.24439",
            title="Unifying Generative Recall and Multi-Objective Ranking in a Single Decoder-Only Sequence",
            url="https://arxiv.org/abs/2607.24439",
            track="recommendation",
            organization="Kuaishou / IIE, CAS / UCAS",
            published="2026-07-27",
            topics=(
                "generative-recommendation",
                "unified-recall-ranking",
                "multi-objective-ranking",
                "lora",
            ),
            online_ab=(
                OnlineABEvidence("Kuaishou App", "play volume", 1.177, "5% traffic, two weeks"),
                OnlineABEvidence("Kuaishou App", "like rate", 2.560, "5% traffic, two weeks"),
                OnlineABEvidence("Kuaishou Lite", "total gifting amount", 2.569, "5% traffic, two weeks"),
            ),
        ),
        run=reproduce_unir2,
        render=render,
        fidelity=ReproductionFidelity.CORE_MECHANISM,
        omitted_core_components=(
            "Kuaishou private full-stream multi-objective samples",
            "three-level 8129-way SID and production beam search",
            "3-layer 640-d online service and pipeline parallelism",
        ),
    )
)
