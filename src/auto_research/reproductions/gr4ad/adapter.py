from ..base import OnlineABEvidence, PaperMetadata, ReproductionAdapter, ReproductionFidelity
from ..registry import register
from .experiment import reproduce_gr4ad
from .report import render


ADAPTER = register(ReproductionAdapter(key="gr4ad", paper=PaperMetadata(arxiv_id="2602.22732", title="Generative Recommendation for Large-Scale Advertising", url="https://arxiv.org/abs/2602.22732", track="recommendation", organization="Kuaishou", published="2026-02", topics=("generative-retrieval", "advertising", "reinforcement-learning", "serving"), online_ab=(OnlineABEvidence(product="Kuaishou Ads", metric="ad revenue", lift_percent=4.2, traffic="large-scale online A/B"),)), run=reproduce_gr4ad, render=render, fidelity=ReproductionFidelity.CORE_MECHANISM, omitted_core_components=("multimodal ad corpus, eCPM rewards, continual online learning, and dynamic beam service",)))
