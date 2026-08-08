from ..base import PaperMetadata, ReproductionAdapter, ReproductionFidelity
from ..registry import register
from .experiment import reproduce
from .report import render
ADAPTER = register(ReproductionAdapter(key="doremi", paper=PaperMetadata(arxiv_id="2305.10429", title="DoReMi: Optimizing Data Mixtures Speeds Up Language Model Pretraining", url="https://arxiv.org/abs/2305.10429", code_url="https://github.com/sangmichaelxie/doremi", track="llm", organization="Stanford University / Google Research", published="2023-05-17", topics=("pretraining-data", "data-mixture", "group-dro")), run=reproduce, render=render, fidelity=ReproductionFidelity.CORE_MECHANISM, omitted_core_components=("The Pile", "280M proxy and 8B target models")))
