from ..base import OnlineABEvidence, PaperMetadata, ReproductionAdapter, ReproductionFidelity
from ..industrial_2026 import render_standard
from ..registry import register
from .experiment import reproduce_hisac


ADAPTER = register(ReproductionAdapter(
    key="hisac",
    paper=PaperMetadata(
        arxiv_id="2602.21009",
        title="HiSAC: Hierarchical Sparse Activation Compression for Ultra-long Sequence Modeling in Recommenders",
        url="https://arxiv.org/abs/2602.21009", track="recommendation",
        organization="Alibaba / Taobao", published="2026-02-24",
        topics=("long-sequence", "sparse-activation", "semantic-id"),
        online_ab=(OnlineABEvidence("Taobao recommendation", "CTR", 1.65, "online A/B"),),
    ),
    run=reproduce_hisac, render=render_standard,
    fidelity=ReproductionFidelity.CORE_MECHANISM,
    omitted_core_components=("private multimodal embeddings", "production ultra-long sequence serving"),
))
