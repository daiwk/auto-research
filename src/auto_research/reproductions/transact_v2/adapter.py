from ..base import PaperMetadata, ReproductionAdapter, ReproductionFidelity
from ..registry import register
from .experiment import reproduce_transact_v2
from .report import render


ADAPTER = register(ReproductionAdapter(
    key="transact-v2",
    paper=PaperMetadata(
        arxiv_id="2506.02267",
        title="TransAct V2: Lifelong User Action Sequence Modeling on Pinterest Recommendation",
        url="https://arxiv.org/abs/2506.02267",
        track="recommendation",
    ),
    run=reproduce_transact_v2,
    render=render,
    fidelity=ReproductionFidelity.CORE_MECHANISM,
    omitted_core_components=(
        "Pinterest action and surface features",
        "impression-log negative samples",
        "SKUT and production serving kernels",
    ),
))
