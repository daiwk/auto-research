from ..base import PaperMetadata, ReproductionAdapter, ReproductionFidelity
from ..registry import register
from .experiment import reproduce_din
from .report import render


ADAPTER = register(ReproductionAdapter(
    key="din",
    paper=PaperMetadata(arxiv_id="1706.06978", title="Deep Interest Network for Click-Through Rate Prediction", url="https://arxiv.org/abs/1706.06978", track="recommendation", code_url="https://github.com/zhougr1993/DeepInterestNetwork"),
    run=reproduce_din,
    render=render,
    fidelity=ReproductionFidelity.CORE_MECHANISM,
    omitted_core_components=("mini-batch-aware regularization", "Alibaba production sparse features"),
))
