from ..base import OnlineABEvidence, PaperMetadata, ReproductionAdapter, ReproductionFidelity
from ..registry import register
from .experiment import reproduce_sort_gen
from .report import render


ADAPTER = register(ReproductionAdapter(
    key="sort-gen",
    paper=PaperMetadata(
        arxiv_id="2505.07197",
        title="A Generative Re-ranking Model for List-level Multi-objective Optimization at Taobao",
        url="https://arxiv.org/abs/2505.07197",
        track="recommendation",
        organization="Alibaba / Taobao & Tmall",
        published="2025-05-12",
        topics=("reranking", "multi-objective", "ordered-regression", "diversity"),
        online_ab=(
            OnlineABEvidence("Taobao Baiyibutie", "CLICK", 4.13, "two-week A/B vs deployed FFT context model + fastDPP"),
            OnlineABEvidence("Taobao Baiyibutie", "GMV", 8.10, "two-week A/B vs deployed FFT context model + fastDPP"),
        ),
    ),
    run=reproduce_sort_gen,
    render=render,
    fidelity=ReproductionFidelity.CORE_MECHANISM,
    omitted_core_components=("private Taobao exposures and CTR/CVR priors", "production multimodal embeddings", "online 19 ms tensor engine"),
))
