from ..base import (
    OnlineABEvidence,
    PaperMetadata,
    ReproductionAdapter,
    ReproductionFidelity,
)
from ..registry import register
from .experiment import reproduce_mim
from .report import render

ADAPTER = register(
    ReproductionAdapter(
        key="mim",
        paper=PaperMetadata(
            arxiv_id="2502.00321",
            title="MIM: Multi-modal Content Interest Modeling Paradigm for User Behavior Modeling",
            url="https://arxiv.org/abs/2502.00321",
            track="recommendation",
            code_url="https://pan.quark.cn/s/8fc8ec3e74f3",
            organization="Alibaba / Taobao",
            published="2025-02-01",
            topics=(
                "multimodal-recommendation",
                "user-modeling",
                "pretraining",
                "ranking",
            ),
            online_ab=(
                OnlineABEvidence("Taobao", "CTR", 14.14, "production A/B"),
                OnlineABEvidence("Taobao", "RPM", 4.12, "production A/B"),
            ),
        ),
        run=reproduce_mim,
        render=render,
        fidelity=ReproductionFidelity.CORE_MECHANISM,
        omitted_core_components=(
            "Taobao private multimodal corpus",
            "production CiUBM serving",
        ),
    )
)
