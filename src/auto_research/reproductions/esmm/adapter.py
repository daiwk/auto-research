from ..base import PaperMetadata, ReproductionAdapter, ReproductionFidelity
from ..registry import register
from .experiment import reproduce
from .report import render

ADAPTER = register(ReproductionAdapter(
    key="esmm",
    paper=PaperMetadata(
        arxiv_id="1804.07931",
        title="Entire Space Multi-Task Model: An Effective Approach for Estimating Post-Click Conversion Rate",
        url="https://arxiv.org/abs/1804.07931",
        track="recommendation",
        organization="Alibaba",
        published="2018-04-21",
        topics=("ranking", "classic", "multi-task", "conversion"),
        selection_exception="用户明确批准 ESMM 为经典例外；原文工业部署不满足当前新论文的量化线上证据格式。",
    ),
    run=reproduce,
    render=render,
    fidelity=ReproductionFidelity.CORE_MECHANISM,
    omitted_core_components=("Taobao private exposure/click/conversion logs",),
))
