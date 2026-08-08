from ..base import PaperMetadata, ReproductionAdapter, ReproductionFidelity
from ..registry import register
from .experiment import reproduce
from .report import render
ADAPTER = register(ReproductionAdapter(key="clip", paper=PaperMetadata(arxiv_id="2103.00020", title="Learning Transferable Visual Models From Natural Language Supervision", url="https://arxiv.org/abs/2103.00020", code_url="https://github.com/openai/CLIP", track="llm", organization="OpenAI", published="2021-02-26", topics=("multimodal", "contrastive-pretraining")), run=reproduce, render=render, fidelity=ReproductionFidelity.CORE_MECHANISM, omitted_core_components=("400M image-text pairs", "large vision encoder")))
