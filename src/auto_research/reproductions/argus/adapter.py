from ..base import OnlineABEvidence, PaperMetadata, ReproductionAdapter, ReproductionFidelity
from ..registry import register
from .experiment import reproduce_argus
from .report import render


ADAPTER = register(ReproductionAdapter(key="argus", paper=PaperMetadata(arxiv_id="2507.15994", title="Scaling Recommender Transformers to One Billion Parameters", url="https://arxiv.org/abs/2507.15994", track="recommendation", organization="Yandex", published="2025-07", topics=("long-sequence", "transformer", "multi-task"), online_ab=(OnlineABEvidence(product="Yandex Music", metric="total listening time", lift_percent=2.26, traffic="large-scale online experiment"), OnlineABEvidence(product="Yandex Music", metric="likes", lift_percent=6.37, traffic="large-scale online experiment"))), run=reproduce_argus, render=render, fidelity=ReproductionFidelity.CORE_MECHANISM, omitted_core_components=("private music feedback schema and billion-parameter scaling",)))
