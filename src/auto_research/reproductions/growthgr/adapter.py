from ..base import OnlineABEvidence, PaperMetadata, ReproductionAdapter, ReproductionFidelity
from ..registry import register
from .experiment import reproduce_growthgr
from .report import render

ADAPTER = register(ReproductionAdapter(key="growthgr", paper=PaperMetadata(arxiv_id="2605.17994", title="Towards Sustainable Growth: A Multi-Value-Aware Retrieval Framework for E-Commerce Search", url="https://arxiv.org/abs/2605.17994", track="recommendation", organization="Alibaba Group / Taobao & Tmall", published="2026-05-18", topics=("generative-recommendation", "reinforcement-learning", "new-items"), online_ab=(OnlineABEvidence("Taobao/Tmall Search", "new-item GMV", 5.3, "online A/B test"), OnlineABEvidence("Taobao/Tmall Search", "overall search GMV", 0.3, "online A/B test"))), run=reproduce_growthgr, render=render, fidelity=ReproductionFidelity.CORE_MECHANISM, omitted_core_components=("private order funnel and foundation-model multimodal embeddings",)))
