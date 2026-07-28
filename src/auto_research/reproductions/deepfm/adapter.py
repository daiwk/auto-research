from ..base import PaperMetadata, ReproductionAdapter, ReproductionFidelity
from ..registry import register
from .experiment import reproduce
from .report import render

ADAPTER = register(ReproductionAdapter(
    key="deepfm",
    paper=PaperMetadata(
        arxiv_id="1703.04247",
        title="DeepFM: A Factorization-Machine based Neural Network for CTR Prediction",
        url="https://arxiv.org/abs/1703.04247",
        track="recommendation",
        organization="Huawei Noah's Ark Lab",
        published="2017-03-13",
        topics=("ranking", "classic", "feature-interaction"),
        selection_exception="用户明确批准 DeepFM 为经典例外；不以该例外放宽新工业论文的量化线上证据门槛。",
    ),
    run=reproduce,
    render=render,
    fidelity=ReproductionFidelity.CORE_MECHANISM,
    omitted_core_components=("Huawei private App Market CTR features and production traffic",),
))
