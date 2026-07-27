from ..base import PaperMetadata, ReproductionAdapter, ReproductionFidelity
from ..llm_evolve_2026_common import render
from ..registry import register
from .experiment import reproduce_looped_latent_attention


ADAPTER = register(ReproductionAdapter(
    key="looped-latent-attention",
    paper=PaperMetadata(
        arxiv_id="2607.15456",
        title="Looped Latent Attention: Cross-Loop KV Compression for Looped Transformers",
        url="https://arxiv.org/abs/2607.15456", track="llm",
        organization="University of Maryland / Meta AI", published="2026-07-16",
        topics=("llm-architecture", "kv-cache", "looped-transformer"),
    ),
    run=reproduce_looped_latent_attention, render=render,
    fidelity=ReproductionFidelity.CORE_MECHANISM,
    omitted_core_components=("large looped checkpoint post-training", "fused inference codec"),
))
