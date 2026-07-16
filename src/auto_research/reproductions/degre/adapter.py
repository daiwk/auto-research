from ..base import OnlineABEvidence, PaperMetadata, ReproductionAdapter, ReproductionFidelity
from ..registry import register
from .experiment import reproduce_degre
from .report import render

ADAPTER = register(ReproductionAdapter(key="degre", paper=PaperMetadata(arxiv_id="2605.25749", title="DeGRe: Listwise Generative Reranking with Offline Lookahead Distillation", url="https://arxiv.org/abs/2605.25749", track="recommendation", organization="Alibaba Group / Zhejiang University", published="2026-05-25", topics=("generative-recommendation", "reranking", "distillation"), online_ab=(OnlineABEvidence("Taobao Flash Shopping", "CTR", 2.85, "8 days, 2% traffic"), OnlineABEvidence("Taobao Flash Shopping", "GMV", 3.75, "8 days, 2% traffic"))), run=reproduce_degre, render=render, fidelity=ReproductionFidelity.CORE_MECHANISM, omitted_core_components=("private transaction labels and production Transformer scale",)))
