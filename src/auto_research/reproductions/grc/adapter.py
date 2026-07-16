from ..base import OnlineABEvidence, PaperMetadata, ReproductionAdapter, ReproductionFidelity
from ..registry import register
from .experiment import reproduce_grc
from .report import render

ADAPTER = register(ReproductionAdapter(key="grc", paper=PaperMetadata(arxiv_id="2602.23639", title="Learning to Reflect and Correct: Towards Better Decoding Trajectories for Large-Scale Generative Recommendation", url="https://arxiv.org/abs/2602.23639", track="recommendation", organization="Alibaba International / Wuhan University", published="2026-02-27", topics=("generative-recommendation", "reinforcement-learning", "self-correction"), online_ab=(OnlineABEvidence("Alibaba International", "Revenue", 1.79, "2026-01-02 to 2026-01-12, 15%/15%"), OnlineABEvidence("Alibaba International", "CTR", 2.11, "2026-01-02 to 2026-01-12, 15%/15%"))), run=reproduce_grc, render=render, fidelity=ReproductionFidelity.CORE_MECHANISM, omitted_core_components=("industrial LLM backbone and private seller/brand attributes",)))
