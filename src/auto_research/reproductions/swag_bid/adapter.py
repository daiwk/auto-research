from ..base import OnlineABEvidence, PaperMetadata, ReproductionAdapter, ReproductionFidelity
from ..industrial_2026 import render_standard
from ..latest_20260729_common import reproduce_swag_bid
from ..registry import register


ADAPTER = register(ReproductionAdapter(
    key="swag-bid",
    paper=PaperMetadata(
        arxiv_id="2607.25233",
        title="Beyond Single-Episode Optimization: Sliding-Window Aware Generative Auto-Bidding for Long-Term Advertising Effectiveness",
        url="https://arxiv.org/abs/2607.25233",
        track="recommendation",
        organization="Alibaba International Digital Commerce / Dalian University of Technology",
        published="2026-07-28",
        topics=("advertising", "generative-model", "decision-transformer", "long-horizon"),
        online_ab=(
            OnlineABEvidence("AliExpress advertising", "GMV", 3.42, "21-day campaign-randomized online A/B"),
            OnlineABEvidence("AliExpress advertising", "ROAS", 5.65, "21-day campaign-randomized online A/B"),
        ),
    ),
    run=reproduce_swag_bid,
    render=render_standard,
    fidelity=ReproductionFidelity.CORE_MECHANISM,
    omitted_core_components=("AliExpress private campaign logs", "production Decision Transformer checkpoint"),
))
