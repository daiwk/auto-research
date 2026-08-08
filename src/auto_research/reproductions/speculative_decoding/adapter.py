from ..base import PaperMetadata, ReproductionAdapter, ReproductionFidelity
from ..registry import register
from .experiment import reproduce
from .report import render
ADAPTER = register(ReproductionAdapter(key="speculative-decoding", paper=PaperMetadata(arxiv_id="2211.17192", title="Fast Inference from Transformers via Speculative Decoding", url="https://arxiv.org/abs/2211.17192", code_url="https://github.com/google-research/google-research/tree/master/speculative_decoding", track="llm", organization="Google Research", published="2022-11-30", publication_label="ICML 2023 Oral", topics=("inference-serving", "decoding")), run=reproduce, render=render, fidelity=ReproductionFidelity.CORE_MECHANISM, omitted_core_components=("T5-XXL", "accelerator kernels")))
