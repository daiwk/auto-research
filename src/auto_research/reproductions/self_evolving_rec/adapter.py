from ..base import PaperMetadata, ReproductionAdapter
from ..registry import register
from .experiment import reproduce_self_evolving_rec
from .report import render

ADAPTER = register(
    ReproductionAdapter(
        key="self-evolving-rec",
        paper=PaperMetadata(
            arxiv_id="2602.10226",
            title="Self-Evolving Recommendation System: End-To-End Autonomous Model Optimization With LLM Agents",
            url="https://arxiv.org/abs/2602.10226",
            track="recommendation",
        ),
        run=reproduce_self_evolving_rec,
        render=render,
    )
)
