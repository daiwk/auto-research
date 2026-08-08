from ..base import PaperMetadata, ReproductionAdapter, ReproductionFidelity
from ..registry import register
from .experiment import reproduce
from .report import render
ADAPTER = register(ReproductionAdapter(key="data-mixing-laws", paper=PaperMetadata(arxiv_id="2403.16952", title="Data Mixing Laws: Optimizing Data Mixtures by Predicting Language Modeling Performance", url="https://arxiv.org/abs/2403.16952", code_url="https://github.com/yegcjs/mixinglaws", track="llm", organization="University of Cambridge / Shanghai AI Laboratory", published="2024-03-25", topics=("pretraining-data", "scaling-law", "data-mixture")), run=reproduce, render=render, fidelity=ReproductionFidelity.CORE_MECHANISM, omitted_core_components=("RedPajama multi-scale training", "large-model extrapolation")))
