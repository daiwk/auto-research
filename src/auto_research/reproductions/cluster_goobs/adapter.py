from ..base import PaperMetadata, ReproductionAdapter, ReproductionFidelity
from ..registry import register
from .experiment import reproduce_cluster_goobs
from .report import render

ADAPTER = register(
    ReproductionAdapter(
        key="cluster-goobs",
        paper=PaperMetadata(
            arxiv_id="2607.00448",
            title="Real-Time Hard Negative Sampling via LLM-based Clustering for Large-Scale Two-Tower Retrieval",
            url="https://arxiv.org/abs/2607.00448",
            track="recommendation",
        ),
        run=reproduce_cluster_goobs,
        render=render,
        fidelity=ReproductionFidelity.CORE_MECHANISM,
    )
)
