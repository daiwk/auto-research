from ..base import OnlineABEvidence, PaperMetadata, ReproductionAdapter, ReproductionFidelity
from ..registry import register
from ..industrial_2026 import render_standard
from .experiment import reproduce_rankgraph2

ADAPTER = register(ReproductionAdapter(
    key="rankgraph2", paper=PaperMetadata(
        arxiv_id="2606.18379", title="RankGraph-2: Lifecycle Co-Design for Billion-Node Graph Learning in Recommendation",
        url="https://arxiv.org/abs/2606.18379", track="recommendation",
        organization="Meta", published="2026-06-16",
        topics=("graph-retrieval", "ppr", "residual-quantization"),
        online_ab=(
            OnlineABEvidence("Meta recommendation products", "CTR", 0.96, "20+ production launches"),
            OnlineABEvidence("Meta recommendation products", "CVR", 2.75, "20+ production launches"),
        ),
    ), run=reproduce_rankgraph2, render=render_standard,
    fidelity=ReproductionFidelity.CORE_MECHANISM,
    omitted_core_components=("Meta-scale graph", "distributed PPR and ANN serving"),
))
