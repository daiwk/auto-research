from ..base import OnlineABEvidence, PaperMetadata, ReproductionAdapter, ReproductionFidelity
from ..registry import register
from .experiment import reproduce_mesh
from .report import render

ADAPTER = register(ReproductionAdapter(key="mesh", paper=PaperMetadata(arxiv_id="2607.12392", title="MESH: Scaling Up Retrieval with Heterogeneous Content Unification", url="https://arxiv.org/abs/2607.12392", track="recommendation", organization="Pinterest", published="2026-07-14", topics=("retrieval", "fresh-content", "serving"), online_ab=(OnlineABEvidence("Pinterest", "fresh-item repins", 5.5, "online A/B test"), OnlineABEvidence("Pinterest", "retention", 0.46, "online A/B test"))), run=reproduce_mesh, render=render, fidelity=ReproductionFidelity.CORE_MECHANISM, omitted_core_components=("production DHEN operators, TorchScript GPU parallel serving and Pinterest logs",)))
