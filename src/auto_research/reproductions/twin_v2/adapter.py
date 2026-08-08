from ..base import OnlineABEvidence, PaperMetadata, ReproductionAdapter, ReproductionFidelity
from ..registry import register
from .experiment import reproduce
from .report import render
ADAPTER = register(ReproductionAdapter(key="twin-v2", paper=PaperMetadata(arxiv_id="2407.16357", title="TWIN V2: Scaling Ultra-Long User Behavior Sequence Modeling for Enhanced CTR Prediction at Kuaishou", url="https://arxiv.org/abs/2407.16357", track="recommendation", organization="Kuaishou", published="2024-07-23", publication_label="CIKM 2024", topics=("ranking", "long-sequence", "training-serving"), online_ab=(OnlineABEvidence("Kuaishou Featured-Video", "watch time", 0.672, "main traffic"), OnlineABEvidence("Kuaishou Discovery", "watch time", 0.800, "main traffic"))), run=reproduce, render=render, fidelity=ReproductionFidelity.CORE_MECHANISM, omitted_core_components=("billion-scale private logs", "nearline production clustering")))
