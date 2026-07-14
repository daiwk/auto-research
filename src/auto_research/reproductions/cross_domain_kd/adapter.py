from ..base import OnlineABEvidence, PaperMetadata, ReproductionAdapter, ReproductionFidelity
from ..registry import register
from .experiment import reproduce_cross_domain_kd
from .report import render


ADAPTER = register(ReproductionAdapter(
    key="cross-domain-kd",
    paper=PaperMetadata(arxiv_id="2603.28994", title="Zero-shot Cross-domain Knowledge Distillation: A Case study on YouTube Music", url="https://arxiv.org/abs/2603.28994", track="recommendation", organization="Google / YouTube", published="2026-03", topics=("distillation", "cross-domain", "ranking"), online_ab=(OnlineABEvidence(product="YouTube Music", metric="discovery", lift_percent=1.12, traffic="two-week live experiments"),)),
    run=reproduce_cross_domain_kd, render=render, fidelity=ReproductionFidelity.CORE_MECHANISM,
    omitted_core_components=("private YouTube teacher and YouTube Music feature/task schemas",),
))
