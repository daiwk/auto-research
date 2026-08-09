from ..base import OnlineABEvidence, PaperMetadata, ReproductionAdapter, ReproductionFidelity
from ..registry import register
from .experiment import reproduce_ha_moe
from .report import render

ADAPTER = register(ReproductionAdapter(key="ha-moe", paper=PaperMetadata(arxiv_id="2607.27577", title="Heterogeneous Ranking in Industrial-Scale Recommender Systems: A Case Study", url="https://arxiv.org/abs/2607.27577", track="recommendation", organization="Google / Discover", published="2026-07-30", topics=("ranking", "mixture-of-experts", "heterogeneity", "diversity"), online_ab=(OnlineABEvidence("Google Discover", "DAU", 0.22, "7-day 1% live-traffic A/B", source_url="https://arxiv.org/html/2607.27577v1#S4.SS4", source_location="Section 4.4 Table 4", experiment_duration="7 days", significance="±0.11%", retrieved_at="2026-08-09"), OnlineABEvidence("Google Discover", "Diverse Engagement Rate", 0.54, "7-day 1% live-traffic A/B", source_url="https://arxiv.org/html/2607.27577v1#S4.SS4", source_location="Section 4.4 Table 4", experiment_duration="7 days", significance="±0.07%", retrieved_at="2026-08-09"))), run=reproduce_ha_moe, render=render, fidelity=ReproductionFidelity.CORE_MECHANISM, omitted_core_components=("Google Discover private logs", "LENS observability and production DL-AUC")))

