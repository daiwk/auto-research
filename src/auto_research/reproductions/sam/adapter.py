from ..base import OnlineABEvidence, PaperMetadata, ReproductionAdapter, ReproductionFidelity
from ..registry import register
from .experiment import reproduce_sam
from .report import render

ADAPTER = register(ReproductionAdapter(key="sam", paper=PaperMetadata(arxiv_id="2607.12714", title="Learning to Forget: Satiation-Aware Long-Sequence Transducers for Mitigating Post-Purchase Redundancy", url="https://arxiv.org/abs/2607.12714", track="recommendation", organization="Alibaba Group", published="2026-07-14", topics=("ranking", "long-sequence", "satiation"), online_ab=(OnlineABEvidence("Alibaba recommendation", "CTR", 1.1, "1% traffic"), OnlineABEvidence("Alibaba recommendation", "GMV", 0.9, "1% traffic"))), run=reproduce_sam, render=render, fidelity=ReproductionFidelity.CORE_MECHANISM, omitted_core_components=("private click/purchase logs and production long-sequence transducer",)))
