from ..base import OnlineABEvidence, PaperMetadata, ReproductionAdapter, ReproductionFidelity
from ..registry import register
from .experiment import reproduce
from .report import render
ADAPTER = register(ReproductionAdapter(key="crsd", paper=PaperMetadata(arxiv_id="2510.11056", title="From Reasoning LLMs to BERT: A Two-Stage Distillation Framework for Search Relevance", url="https://arxiv.org/abs/2510.11056", track="recommendation", organization="Meituan", published="2025-10-13", publication_label="TheWebConf 2026 Industry", topics=("search", "content-understanding", "llm-distillation"), online_ab=(OnlineABEvidence("Meituan search advertising", "AdCTR", 0.91, "30% traffic"), OnlineABEvidence("Meituan search advertising", "AdCVR", 1.06, "30% traffic"))), run=reproduce, render=render, fidelity=ReproductionFidelity.CORE_MECHANISM, omitted_core_components=("domain CPT/SFT teacher LLM", "private search-ad logs")))
