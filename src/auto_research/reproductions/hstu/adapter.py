from ..base import PaperMetadata, ReproductionAdapter, ReproductionFidelity
from ..registry import register
from .experiment import reproduce_hstu
from .report import render


ADAPTER = register(ReproductionAdapter(
    key="hstu",
    paper=PaperMetadata(arxiv_id="2402.17152", title="Actions Speak Louder than Words: Trillion-Parameter Sequential Transducers for Generative Recommendations", url="https://arxiv.org/abs/2402.17152", track="recommendation", code_url="https://github.com/meta-recsys/generative-recommenders"),
    run=reproduce_hstu,
    render=render,
    fidelity=ReproductionFidelity.CORE_MECHANISM,
    omitted_core_components=("heterogeneous action tokens", "stochastic-length training", "M-FALCON serving"),
))
