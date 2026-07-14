from ..base import OnlineABEvidence, PaperMetadata, ReproductionAdapter, ReproductionFidelity
from ..registry import register
from .experiment import reproduce_kar
from .report import render

ADAPTER = register(ReproductionAdapter(
    key="kar",
    paper=PaperMetadata(
        arxiv_id="2306.10933", title="Towards Open-World Recommendation with Knowledge Augmentation from Large Language Models",
        url="https://arxiv.org/abs/2306.10933", track="recommendation",
        organization="Huawei", published="2023-06",
        topics=("llm-recommendation", "knowledge-augmentation", "ctr-ranking"),
        online_ab=(
            OnlineABEvidence("Huawei News", "recall", 7.0, "online A/B test"),
            OnlineABEvidence("Huawei Music", "song play count", 1.7, "10% treatment/control, 7 days"),
        ),
    ),
    run=reproduce_kar, render=render,
    fidelity=ReproductionFidelity.FULL_PIPELINE,
))
