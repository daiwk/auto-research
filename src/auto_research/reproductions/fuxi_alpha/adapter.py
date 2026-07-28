from ..base import OnlineABEvidence, PaperMetadata, ReproductionAdapter, ReproductionFidelity
from ..registry import register
from .experiment import reproduce_fuxi_alpha
from .report import render


ADAPTER = register(ReproductionAdapter(
    key="fuxi-alpha",
    paper=PaperMetadata(
        arxiv_id="2502.03036",
        title="FuXi-α: Scaling Recommendation Model with Feature Interaction Enhanced Transformer",
        url="https://arxiv.org/abs/2502.03036",
        track="recommendation",
        code_url="https://github.com/USTC-StarTeam/FuXi-alpha",
        organization="Huawei / USTC",
        published="2025-02-05",
        topics=("ranking", "transformer", "feature-interaction", "scaling"),
        online_ab=(
            OnlineABEvidence("Huawei Music", "songs played", 4.67, "30% traffic, 7 days"),
            OnlineABEvidence("Huawei Music", "listening duration", 5.10, "30% traffic, 7 days"),
        ),
    ),
    run=reproduce_fuxi_alpha,
    render=render,
    fidelity=ReproductionFidelity.CORE_MECHANISM,
    omitted_core_components=("Huawei private features", "billion-parameter distributed training"),
))
