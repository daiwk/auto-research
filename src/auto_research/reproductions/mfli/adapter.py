from ..base import OnlineABEvidence, PaperMetadata, ReproductionAdapter, ReproductionFidelity
from ..registry import register
from .experiment import reproduce_mfli
from .report import render

ADAPTER = register(ReproductionAdapter(key="mfli", paper=PaperMetadata(arxiv_id="2602.16124", title="Rethinking ANN-based Retrieval: Multifaceted Learnable Index for Large-scale Recommendation System", url="https://arxiv.org/abs/2602.16124", track="recommendation", organization="Meta", published="2026-02-18", topics=("retrieval", "learnable-index", "fresh-content", "diversity", "serving"), online_ab=(OnlineABEvidence("Meta recommendation", "low-view exposure", 279.0, "7-day online A/B", source_url="https://arxiv.org/html/2602.16124v1#S4.SS6", source_location="Section 4.6", experiment_duration="7 days", retrieved_at="2026-08-09"), OnlineABEvidence("Meta recommendation", "diversity", 0.30, "7-day online A/B", source_url="https://arxiv.org/html/2602.16124v1#S4.SS6", source_location="Section 4.6", experiment_duration="7 days", retrieved_at="2026-08-09"))), run=reproduce_mfli, render=render, fidelity=ReproductionFidelity.CORE_MECHANISM, omitted_core_components=("Meta private corpus", "distributed real-time indexing and production QPS stack")))

