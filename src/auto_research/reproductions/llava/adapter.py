from ..base import PaperMetadata, ReproductionAdapter, ReproductionFidelity
from ..registry import register
from .experiment import reproduce
from .report import render
ADAPTER = register(ReproductionAdapter(key="llava", paper=PaperMetadata(arxiv_id="2304.08485", title="Visual Instruction Tuning", url="https://arxiv.org/abs/2304.08485", code_url="https://github.com/haotian-liu/LLaVA", track="llm", organization="University of Wisconsin-Madison / Microsoft Research / Columbia University", published="2023-04-17", publication_label="NeurIPS 2023 Oral", topics=("multimodal", "instruction-tuning")), run=reproduce, render=render, fidelity=ReproductionFidelity.CORE_MECHANISM, omitted_core_components=("GPT-4 generated instructions", "LLaMA-scale decoder")))
