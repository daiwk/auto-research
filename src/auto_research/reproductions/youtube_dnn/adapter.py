from ..base import PaperMetadata, ReproductionAdapter, ReproductionFidelity
from ..registry import register
from .experiment import reproduce
from .report import render

ADAPTER = register(ReproductionAdapter(
    key="youtube-dnn",
    paper=PaperMetadata(
        arxiv_id="recsys2016-youtube-dnn",
        title="Deep Neural Networks for YouTube Recommendations",
        url="https://research.google/pubs/deep-neural-networks-for-youtube-recommendations/",
        track="recommendation",
        organization="Google / YouTube",
        published="2016-09-15",
        publication_label="RecSys 2016 paper",
        publication_source="ACM RecSys 2016",
        topics=("retrieval", "ranking", "classic", "two-stage"),
        selection_exception="用户明确批准 YouTube DNN 为经典例外；论文描述线上服务系统但未披露可核验的量化 lift。",
    ),
    run=reproduce,
    render=render,
    fidelity=ReproductionFidelity.CORE_MECHANISM,
    omitted_core_components=("YouTube private watch corpus", "sampled-softmax candidate generation and production ranker"),
))
