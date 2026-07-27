from ..base import OnlineABEvidence, PaperMetadata, ReproductionAdapter, ReproductionFidelity
from ..industrial_2026 import render_standard
from ..registry import register
from .experiment import reproduce_dos


ADAPTER = register(ReproductionAdapter(
    key="dos",
    paper=PaperMetadata(
        arxiv_id="2602.04460",
        title="DOS: Dual-Flow Orthogonal Semantic IDs for Recommendation in Meituan",
        url="https://arxiv.org/abs/2602.04460", track="recommendation",
        organization="Meituan", published="2026-02-04",
        topics=("generative-recommendation", "semantic-id", "orthogonal-quantization"),
        online_ab=(OnlineABEvidence("Meituan app", "revenue", 1.15, "30% traffic, one week"),),
    ),
    run=reproduce_dos, render=render_standard,
    fidelity=ReproductionFidelity.CORE_MECHANISM,
    omitted_core_components=("private Meituan features and LLM embeddings", "production generator"),
))
