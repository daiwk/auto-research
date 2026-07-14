from ..base import OnlineABEvidence, PaperMetadata, ReproductionAdapter, ReproductionFidelity
from ..registry import register
from .experiment import reproduce_seral
from .report import render
ADAPTER = register(ReproductionAdapter(key="seral", paper=PaperMetadata(arxiv_id="2502.13539", title="Bursting Filter Bubble: Enhancing Serendipity Recommendations with Aligned Large Language Models", url="https://arxiv.org/abs/2502.13539", track="recommendation", organization="Alibaba / Taobao", published="2025-02", topics=("llm-recommendation", "preference-alignment", "serendipity"), online_ab=(OnlineABEvidence(product="Taobao Guess What You Like", metric="serendipity clicks", lift_percent=29.56, traffic="fully deployed online experiment"),)), run=reproduce_seral, render=render, fidelity=ReproductionFidelity.FULL_PIPELINE, omitted_core_components=("private Taobao profiles and GPT-4/human CDI annotations",)))
