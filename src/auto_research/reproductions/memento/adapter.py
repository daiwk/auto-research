from ..base import PaperMetadata, ReproductionAdapter
from ..registry import register
from .experiment import reproduce_memento
from .report import render

ADAPTER = register(
    ReproductionAdapter(
        key="memento",
        paper=PaperMetadata(
            arxiv_id="2605.24051",
            title="Memento: Personalized RAG-Style Long-Retention Data Scaling for Online Ads Recommendation",
            url="https://arxiv.org/abs/2605.24051",
            track="recommendation",
        ),
        run=reproduce_memento,
        render=render,
    )
)
