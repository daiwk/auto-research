from ..base import PaperMetadata, ReproductionAdapter, ReproductionFidelity
from ..registry import register
from .experiment import reproduce
from .report import render

ADAPTER = register(ReproductionAdapter(
    key="mmoe",
    paper=PaperMetadata(
        arxiv_id="kdd2018-mmoe",
        title="Modeling Task Relationships in Multi-task Learning with Multi-gate Mixture-of-Experts",
        url="https://research.google/pubs/modeling-task-relationships-in-multi-task-learning-with-multi-gate-mixture-of-experts/",
        track="recommendation",
        organization="Google",
        published="2018-08-19",
        publication_label="KDD 2018 paper",
        publication_source="ACM KDD 2018",
        topics=("ranking", "classic", "multi-task", "mixture-of-experts"),
        selection_exception="用户明确批准 MMoE 为经典例外；原文生产任务未披露当前门槛要求的量化线上 A/B lift。",
    ),
    run=reproduce,
    render=render,
    fidelity=ReproductionFidelity.CORE_MECHANISM,
    omitted_core_components=("Google private recommendation tasks and production features",),
))
