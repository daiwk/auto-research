from ..base import OnlineABEvidence, PaperMetadata, ReproductionAdapter, ReproductionFidelity
from ..registry import register
from .experiment import reproduce_danet
from .report import render

ADAPTER = register(ReproductionAdapter(key="danet", paper=PaperMetadata(arxiv_id="2607.12578", title="Cheaper is Better: A Discount-Aware Network for Conversion Rate Prediction in E-commerce Recommendation System", url="https://arxiv.org/abs/2607.12578", track="recommendation", code_url="https://github.com/tangrc/DANet", organization="Alibaba Group / Tmall", published="2026-07-14", topics=("ranking", "cvr", "discount"), online_ab=(OnlineABEvidence("Tmall", "pCVR", 3.63, "online A/B test"), OnlineABEvidence("Tmall", "GMV", 2.23, "online A/B test"))), run=reproduce_danet, render=render, fidelity=ReproductionFidelity.CORE_MECHANISM, omitted_core_components=("private 400-day discount series and production feature platform",)))
