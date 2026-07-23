from ..base import OnlineABEvidence, PaperMetadata, ReproductionAdapter, ReproductionFidelity
from ..registry import register
from .experiment import reproduce_tsgr
from .report import render


ADAPTER = register(ReproductionAdapter(
    key="tsgr",
    paper=PaperMetadata(
        arxiv_id="2607.18796",
        title="TSGR: Taobao Search Generative Retrieval",
        url="https://arxiv.org/abs/2607.18796",
        track="recommendation",
        organization="Taobao & Tmall Group of Alibaba / Zhejiang University",
        published="2026-07-21",
        topics=("generative-retrieval", "semantic-id", "search", "pre-ranking"),
        online_ab=(
            OnlineABEvidence("Taobao Search", "IPV", 0.43, "1% traffic; 38 days; statistically significant"),
            OnlineABEvidence("Taobao Search", "Transaction Count", 1.12, "1% traffic; 38 days; statistically significant"),
            OnlineABEvidence("Taobao Search", "GMV", 1.64, "1% traffic; 38 days; statistically significant"),
        ),
    ),
    run=reproduce_tsgr,
    render=render,
    fidelity=ReproductionFidelity.CORE_MECHANISM,
    omitted_core_components=("private Taobao queries and 200M interactions", "H20 constrained beam-search serving stack"),
))
