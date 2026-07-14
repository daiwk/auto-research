from ..base import PaperMetadata, ReproductionAdapter, ReproductionFidelity
from ..registry import register
from .experiment import reproduce_tiger
from .report import render


ADAPTER = register(ReproductionAdapter(
    key="tiger",
    paper=PaperMetadata(arxiv_id="2305.05065", title="Recommender Systems with Generative Retrieval", url="https://arxiv.org/abs/2305.05065", track="recommendation"),
    run=reproduce_tiger,
    render=render,
    fidelity=ReproductionFidelity.CORE_MECHANISM,
    omitted_core_components=("Sentence-T5 item encoder", "hashed user token", "cold-start epsilon mixing"),
))
