from ..base import OnlineABEvidence, PaperMetadata, ReproductionAdapter, ReproductionFidelity
from ..registry import register
from ..industrial_2026 import render_standard
from .experiment import reproduce_solaris

ADAPTER = register(ReproductionAdapter(
    key="solaris", paper=PaperMetadata(
        arxiv_id="2604.12110", title="SOLARIS: Speculative Offloading of Latent-bAsed Representation for Inference Scaling",
        url="https://arxiv.org/abs/2604.12110", track="recommendation",
        organization="Meta", published="2026-04-13",
        topics=("foundation-model", "serving", "latent-cache"),
        online_ab=(OnlineABEvidence("Meta recommendation", "Top-line revenue", 0.67, "fully deployed"),),
    ), run=reproduce_solaris, render=render_standard,
    fidelity=ReproductionFidelity.CORE_MECHANISM,
    omitted_core_components=("Meta foundation-model weights", "production cache infrastructure"),
))
