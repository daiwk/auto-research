from ..base import OnlineABEvidence, PaperMetadata, ReproductionAdapter, ReproductionFidelity
from ..registry import register
from .experiment import reproduce_proximity_features
from .report import render

ADAPTER = register(ReproductionAdapter(key="proximity-features", paper=PaperMetadata(arxiv_id="2607.12246", title="Proximity Features: Privacy-Compliant Cold-Start Personalization at Airbnb", url="https://arxiv.org/abs/2607.12246", track="recommendation", organization="Airbnb", published="2026-07-14", topics=("cold-start", "privacy", "features"), online_ab=(OnlineABEvidence("Airbnb marketing landing", "first-time bookers", 2.0, "experiments 2024-12 to 2026-03"), OnlineABEvidence("Airbnb AutoSuggest", "global bookings", 0.16, "experiments 2024-12 to 2026-03"))), run=reproduce_proximity_features, render=render, fidelity=ReproductionFidelity.CORE_MECHANISM, omitted_core_components=("commercial geo-IP database, consent platform and distributed KV serving",)))
