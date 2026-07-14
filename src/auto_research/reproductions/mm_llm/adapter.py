from ..base import OnlineABEvidence, PaperMetadata, ReproductionAdapter, ReproductionFidelity
from ..registry import register
from .experiment import reproduce_mm_llm
from .report import render


ADAPTER = register(ReproductionAdapter(key="mm-llm", paper=PaperMetadata(arxiv_id="2605.09338", title="A General Framework for Multimodal LLM-Based Multimedia Understanding in Large-Scale Recommendation Systems", url="https://arxiv.org/abs/2605.09338", track="recommendation", organization="Meta", published="2026-05", topics=("multimodal", "llm-recommendation", "ranking"), online_ab=(OnlineABEvidence(product="Meta recommendation", metric="engagement", lift_percent=0.02, traffic="large-scale online A/B"),)), run=reproduce_mm_llm, render=render, fidelity=ReproductionFidelity.CORE_MECHANISM, omitted_core_components=("raw private multimedia and BLIP-2/LLaMA2-1.5B scale",)))
