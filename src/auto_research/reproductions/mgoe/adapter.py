from ..base import OnlineABEvidence, PaperMetadata, ReproductionAdapter, ReproductionFidelity
from ..registry import register
from .experiment import reproduce_mgoe
from .report import render


ADAPTER = register(ReproductionAdapter(
    key="mgoe",
    paper=PaperMetadata(
        arxiv_id="2506.10520",
        title="Macro Graph of Experts for Billion-Scale Multi-Task Recommendation",
        url="https://arxiv.org/abs/2506.10520",
        track="recommendation",
        code_url="https://github.com/RainmannnnN/MGOE",
        organization="Alibaba",
        published="2025-06-12",
        publication_label="KDD 2026",
        topics=("multi-task-learning", "mixture-of-experts", "graph-neural-network", "ranking"),
        online_ab=(
            OnlineABEvidence("Alibaba", "PCTR", 2.16, "production A/B vs MMoE"),
            OnlineABEvidence("Alibaba", "GMV", 16.46, "production A/B vs MMoE"),
        ),
    ),
    run=reproduce_mgoe,
    render=render,
    fidelity=ReproductionFidelity.CORE_MECHANISM,
    omitted_core_components=("Alibaba billion-scale sparse features", "distributed production training"),
))
