from ..base import OnlineABEvidence, PaperMetadata, ReproductionAdapter, ReproductionFidelity
from ..registry import register
from .experiment import reproduce_dual_sid
from .report import render

ADAPTER = register(ReproductionAdapter(key="dual-sid", paper=PaperMetadata(arxiv_id="2607.24865", title="Tokens are All You Need: Dual-purpose Semantic IDs for Achieving LLM-Level I/O Efficiency in Recommendation Systems", url="https://arxiv.org/abs/2607.24865", track="recommendation", organization="Google DeepMind / YouTube", published="2026-07-26", topics=("semantic-id", "retrieval", "ranking", "content-understanding", "serving"), online_ab=(OnlineABEvidence("YouTube Watchpage ranking", "sitewide objective", 0.09, "production online experiment", source_url="https://arxiv.org/html/2607.24865v1#S4.SS2", source_location="Section 4.2 Table 1", retrieved_at="2026-08-09"), OnlineABEvidence("YouTube retrieval", "homepage objective", 0.13, "production online experiment", source_url="https://arxiv.org/html/2607.24865v1#S4.SS2", source_location="Section 4.2 Table 1", retrieved_at="2026-08-09"))), run=reproduce_dual_sid, render=render, fidelity=ReproductionFidelity.CORE_MECHANISM, omitted_core_components=("YouTube-scale codebooks and private logs", "production embedding reconstruction service")))

