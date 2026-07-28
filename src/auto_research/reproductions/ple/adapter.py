from ..base import PaperMetadata, ReproductionAdapter, ReproductionFidelity
from ..registry import register
from .experiment import reproduce
from .report import render

ADAPTER = register(ReproductionAdapter(
    key="ple",
    paper=PaperMetadata(
        arxiv_id="recsys2020-ple",
        title="Progressive Layered Extraction (PLE): A Novel Multi-Task Learning Model for Personalized Recommendations",
        url="https://doi.org/10.1145/3383313.3412236",
        track="recommendation",
        organization="Tencent",
        published="2020-09-22",
        publication_label="RecSys 2020 paper",
        publication_source="ACM RecSys 2020",
        topics=("ranking", "classic", "multi-task", "mixture-of-experts"),
        selection_exception="用户明确批准 PLE 为经典例外；原文腾讯视频部署证据不按当前新论文的量化线上门槛计入。",
    ),
    run=reproduce,
    render=render,
    fidelity=ReproductionFidelity.CORE_MECHANISM,
    omitted_core_components=("Tencent Video private watch/interaction tasks", "production progressive tower depth"),
))
