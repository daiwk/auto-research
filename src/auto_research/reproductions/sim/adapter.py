from ..base import OnlineABEvidence, PaperMetadata, ReproductionAdapter, ReproductionFidelity
from ..registry import register
from .experiment import reproduce
from .report import render
ADAPTER = register(ReproductionAdapter(key="sim", paper=PaperMetadata(arxiv_id="2006.05639", title="Search-based User Interest Modeling with Lifelong Sequential Behavior Data for CTR Prediction", url="https://arxiv.org/abs/2006.05639", track="recommendation", organization="Alibaba", published="2020-06-10", publication_label="CIKM 2020", topics=("ranking", "long-sequence", "training-serving"), online_ab=(OnlineABEvidence("Alibaba display advertising", "CTR", 7.1, "main traffic"), OnlineABEvidence("Alibaba display advertising", "RPM", 4.4, "main traffic"))), run=reproduce, render=render, fidelity=ReproductionFidelity.CORE_MECHANISM, omitted_core_components=("54k production behavior service", "Alibaba private logs")))
