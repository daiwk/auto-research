from ..base import OnlineABEvidence, PaperMetadata, ReproductionAdapter, ReproductionFidelity
from ..registry import register
from .experiment import reproduce_cobra
from .report import render


ADAPTER = register(ReproductionAdapter(key="cobra", paper=PaperMetadata(arxiv_id="2503.02453", title="Sparse Meets Dense: Unified Generative Recommendations with Cascaded Sparse-Dense Representations", url="https://arxiv.org/abs/2503.02453", track="recommendation", organization="Baidu", published="2025-03", topics=("generative-retrieval", "semantic-id", "dense-retrieval"), online_ab=(OnlineABEvidence(product="Baidu advertising", metric="conversion", lift_percent=3.60, traffic="production online A/B"), OnlineABEvidence(product="Baidu advertising", metric="ARPU", lift_percent=4.15, traffic="production online A/B"))), run=reproduce_cobra, render=render, fidelity=ReproductionFidelity.FULL_PIPELINE, omitted_core_components=("private ad data and production ANN/BeamFusion serving",)))
