from ..base import OnlineABEvidence, PaperMetadata, ReproductionAdapter, ReproductionFidelity
from ..registry import register
from .experiment import reproduce_kunlun
from .report import render

ADAPTER = register(ReproductionAdapter(key="kunlun", paper=PaperMetadata(arxiv_id="2602.10016", title="Kunlun: Establishing Scaling Laws for Massive-Scale Recommendation Systems through Unified Architecture Design", url="https://arxiv.org/abs/2602.10016", track="recommendation", organization="Meta", published="2026-02-10", topics=("ranking", "scaling-law", "long-sequence", "mixture-of-experts", "serving"), online_ab=(OnlineABEvidence("Meta Ads", "topline", 1.2, "deployed across major Ads models", source_url="https://arxiv.org/html/2602.10016v3#S5.SS5", source_location="Section 5.5", retrieved_at="2026-08-09"),)), run=reproduce_kunlun, render=render, fidelity=ReproductionFidelity.CORE_MECHANISM, omitted_core_components=("Meta private ads data and massive scale", "expert-parallel accelerator implementation")))

