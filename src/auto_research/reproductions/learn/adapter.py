from ..base import OnlineABEvidence, PaperMetadata, ReproductionAdapter, ReproductionFidelity
from ..registry import register
from .experiment import reproduce_learn
from .report import render

ADAPTER = register(ReproductionAdapter(
    key="learn",
    paper=PaperMetadata(
        arxiv_id="2405.03988", title="Knowledge Adaptation from Large Language Model to Recommendation for Practical Industrial Application",
        url="https://arxiv.org/abs/2405.03988", track="recommendation",
        organization="Kuaishou", published="2024-05",
        topics=("llm-recommendation", "knowledge-adaptation", "cold-start"),
        online_ab=(OnlineABEvidence("Kuaishou e-commerce ads", "cold-start item revenue", 8.77, "20% traffic, 9 days"),),
    ),
    run=reproduce_learn, render=render,
    fidelity=ReproductionFidelity.FULL_PIPELINE,
))
