from ..base import PaperMetadata, ReproductionAdapter, ReproductionFidelity
from ..registry import register
from ..latest_20260809_common import reproduce_hilp, render_latest

ADAPTER = register(ReproductionAdapter(
    key="hilp", paper=PaperMetadata(arxiv_id="2608.05806", title="Hierarchical Latent Prediction for Language Models",
        url="https://arxiv.org/abs/2608.05806", track="llm", organization="University of Texas at Austin",
        published="2026-08-06", topics=("pretraining", "latent-prediction", "multi-token-prediction", "speculative-decoding")),
    run=reproduce_hilp, render=render_latest, fidelity=ReproductionFidelity.CORE_MECHANISM,
    omitted_core_components=("large-scale language model pretraining", "paper speculative decoder"),
))
