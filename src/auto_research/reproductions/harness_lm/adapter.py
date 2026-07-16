from ..base import OnlineABEvidence, PaperMetadata, ReproductionAdapter, ReproductionFidelity
from ..registry import register
from .experiment import reproduce_harness_lm
from .report import render

ADAPTER = register(ReproductionAdapter(key="harness-lm", paper=PaperMetadata(arxiv_id="2605.23572", title="HARNESS-LM: A Three-Phase Training Recipe for Harnessing SLMs in Sponsored Search Retrieval", url="https://arxiv.org/abs/2605.23572", track="recommendation", organization="Microsoft AI / Bing Ads", published="2026-05-22", topics=("llm-recommendation", "retrieval", "distillation"), online_ab=(OnlineABEvidence("Bing Ads", "Revenue", 1.0, "production deployment"), OnlineABEvidence("Bing Ads", "Clicks", 0.4, "production deployment"))), run=reproduce_harness_lm, render=render, fidelity=ReproductionFidelity.CORE_MECHANISM, omitted_core_components=("Qwen3-Embedding 4B/0.6B scale and proprietary GPT expansions", "structured layer/FFN pruning hardware study")))
