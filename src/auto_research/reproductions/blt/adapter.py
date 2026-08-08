from ..base import PaperMetadata, ReproductionAdapter, ReproductionFidelity
from ..registry import register
from .experiment import reproduce
from .report import render
ADAPTER = register(ReproductionAdapter(key="blt", paper=PaperMetadata(arxiv_id="2412.09871", title="Byte Latent Transformer: Patches Scale Better Than Tokens", url="https://arxiv.org/abs/2412.09871", code_url="https://github.com/facebookresearch/blt", track="llm", organization="Meta FAIR", published="2024-12-13", topics=("tokenizer-free", "byte-model", "dynamic-patching", "architecture")), run=reproduce, render=render, fidelity=ReproductionFidelity.CORE_MECHANISM, omitted_core_components=("raw-byte 8B pretraining", "full local byte encoder/decoder")))
