from ..base import OnlineABEvidence, PaperMetadata, ReproductionAdapter, ReproductionFidelity
from ..registry import register
from .experiment import reproduce_mbgr
from .report import render

ADAPTER = register(ReproductionAdapter(key="mbgr", paper=PaperMetadata(arxiv_id="2604.02684", title="MBGR: Multi-Business Generative Recommendation", url="https://arxiv.org/abs/2604.02684", track="recommendation", organization="Meituan", published="2026-04-03", topics=("generative-recommendation", "multi-domain", "semantic-id"), online_ab=(OnlineABEvidence("Meituan multi-business recommendation", "CTCVR", 3.98, "online A/B test"),)), run=reproduce_mbgr, render=render, fidelity=ReproductionFidelity.CORE_MECHANISM, omitted_core_components=("private multi-business logs and production Transformer scale",)))
