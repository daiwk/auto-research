from ..base import EvaluationTier, PaperMetadata, ReproductionAdapter, ReproductionFidelity
from ..registry import register
from .experiment import reproduce_sas_attention
from .report import render


ADAPTER = register(ReproductionAdapter(
    key="sas-attention",
    paper=PaperMetadata(
        arxiv_id="2609.13141",
        title="SAS: Simple Attention Sparsification via End-to-End Optimization of Context Ranking",
        url="https://arxiv.org/abs/2609.13141",
        code_url="https://github.com/Tencent-Hunyuan/Simple-Attention-Sparsification",
        track="llm",
        organization="Tencent HY LLM Frontier / HKUST (Guangzhou) / HKUST",
        published="2026-09-11",
        publication_label="arXiv v1",
        topics=("sparse-attention", "long-context", "post-training", "context-ranking"),
    ),
    run=reproduce_sas_attention,
    render=render,
    fidelity=ReproductionFidelity.CORE_MECHANISM,
    omitted_core_components=(
        "Qwen3-4B/8B/14B and OLMo3-7B checkpoints",
        "OpenR1-Math-220k, LongBench, BFCL and VitaBench paper-scale runs",
        "Triton/FlashAttention kernel and SGLang decode benchmark",
    ),
    evaluation_tier=EvaluationTier.PUBLIC_DATASET,
    datasets=("WikiText-2",),
    baseline="same trained tiny decoder with full causal attention",
    metrics=(
        "test.sas.perplexity",
        "test.dense.perplexity",
        "routing.retained_attention_fraction",
        "selector_training.selector_gradient_norm_mean",
    ),
    default_seeds=(42, 43, 44),
    device_capabilities=("cpu",),
    infer_device_capabilities=False,
))
