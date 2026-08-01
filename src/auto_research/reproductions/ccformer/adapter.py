from ..base import OnlineABEvidence, PaperMetadata, ReproductionAdapter, ReproductionFidelity
from ..registry import register
from .experiment import reproduce_ccformer
from .report import render


ADAPTER = register(ReproductionAdapter(
    key="ccformer",
    paper=PaperMetadata(
        arxiv_id="2607.28070", title="CCFormer: Efficient Cross-Field Interaction and Hierarchical Sequence Compression for Industrial Recommendation at Tencent",
        url="https://arxiv.org/abs/2607.28070", track="recommendation",
        organization="Tencent Platform and Content Group", published="2026-07-30",
        topics=("ranking", "long-sequence", "sequence-compression", "token-mixing"),
        online_ab=(
            OnlineABEvidence("Tencent video recommendation", "CTR", 3.57, "over one million exposed users/day, two weeks; fully deployed"),
            OnlineABEvidence("Tencent advertising ranking", "advertising revenue", 1.71, "over one million exposed users/day, two weeks; fully deployed"),
        ),
    ),
    run=reproduce_ccformer, render=render,
    fidelity=ReproductionFidelity.CORE_MECHANISM,
    omitted_core_components=("Tencent four-billion-sample private dataset", "parallel multi-target serving kernel"),
))
