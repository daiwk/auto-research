from ..base import PaperMetadata, ReproductionAdapter, ReproductionFidelity
from ..registry import register
from .experiment import reproduce
from .report import render
ADAPTER = register(ReproductionAdapter(key="rope", paper=PaperMetadata(arxiv_id="2104.09864", title="RoFormer: Enhanced Transformer with Rotary Position Embedding", url="https://arxiv.org/abs/2104.09864", code_url="https://github.com/ZhuiyiTechnology/roformer", track="llm", organization="Zhuiyi Technology", published="2021-04-20", topics=("position-encoding", "long-context", "architecture")), run=reproduce, render=render, fidelity=ReproductionFidelity.CORE_MECHANISM, omitted_core_components=("large-scale Chinese pretraining",)))
