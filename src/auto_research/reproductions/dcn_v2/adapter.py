from ..base import PaperMetadata, ReproductionAdapter, ReproductionFidelity
from ..registry import register
from .experiment import reproduce
from .report import render

ADAPTER = register(ReproductionAdapter(
    key="dcn-v2",
    paper=PaperMetadata(
        arxiv_id="2008.13535", title="DCN V2: Improved Deep & Cross Network and Practical Lessons for Web-scale Learning to Rank Systems",
        url="https://arxiv.org/abs/2008.13535", track="recommendation",
        organization="Google", published="2020-08-19",
        topics=("ranking", "classic", "feature-interaction"),
        selection_exception="用户明确要求补齐经典搜广推论文；原文确认 Google 线上业务指标显著提升但未披露具体 lift。",
    ),
    run=reproduce, render=render, fidelity=ReproductionFidelity.CORE_MECHANISM,
    omitted_core_components=("Google private ranking datasets", "production-scale low-rank expert tuning"),
))
