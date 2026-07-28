from ..base import OnlineABEvidence, PaperMetadata, ReproductionAdapter, ReproductionFidelity
from ..registry import register
from .experiment import reproduce_click_a_buy_b
from .report import render


ADAPTER = register(ReproductionAdapter(
    key="click-a-buy-b",
    paper=PaperMetadata(
        arxiv_id="2507.15113",
        title="Click A, Buy B: Rethinking Conversion Attribution in E-Commerce Recommendations",
        url="https://arxiv.org/abs/2507.15113",
        track="recommendation",
        organization="Pinterest",
        published="2025-07-20",
        topics=("conversion-attribution", "multi-task-learning", "taxonomy", "ads-ranking"),
        online_ab=(
            OnlineABEvidence("Pinterest shopping", "primary business metric", 0.25, "production A/B"),
        ),
    ),
    run=reproduce_click_a_buy_b,
    render=render,
    fidelity=ReproductionFidelity.CORE_MECHANISM,
    omitted_core_components=("Pinterest conversion windows", "private purchase and ad exposure labels"),
))
