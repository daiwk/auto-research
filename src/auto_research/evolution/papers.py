from __future__ import annotations

from ..models import Paper
from ..papers import ArxivClient
from .models import PaperInspiration


INSTALLED_MUTATIONS = {
    "2507.15551": ("rankmixer_smoe", "RankMixer per-token FFN 与 dense-training/sparse-serving ReLU MoE"),
    "2602.06563": ("tokenmixer_large", "Mixing-Reverting、per-token SwiGLU、interval residual 与辅助头"),
    "2601.21285": ("zenith", "Prime Token Fusion 与 tokenwise SwiGLU Token Boost"),
    "2108.07505": ("moi_mixer", "显式一阶与二阶 Multi-Order Interaction channel mixing"),
    "2505.04421": ("longer", "LONGER 的分块 token merge、全局兴趣与 recent token 保留"),
    "2604.00590": ("unimixer", "UniMixer 的可学习参数化 token mixing，解除固定 head-token 对齐"),
}

LLM_MUTATIONS = {
    "2204.02311": ("parallel_block", "PaLM 的 parallel attention/FFN block 与 SwiGLU 路径"),
    "2302.13971": ("llama_modern", "LLaMA 风格 RMSNorm、RoPE、SwiGLU 与 pre-normalization"),
    "2305.13245": ("gqa", "Grouped-Query Attention：多 query heads 共享更少的 key/value heads"),
    "2305.10429": ("data_mixture", "DoReMi 的数据域混合与动态配比思想，本地使用可审计的固定/课程配比"),
    "2310.05914": ("neftune", "NEFTune 在 instruction tuning 时向 embedding 注入缩放均匀噪声"),
    "2401.02385": ("small_llm", "TinyLlama 展示 LLaMA 架构的小模型预训练与 staged data mixture"),
    "2512.24880": ("mhc", "mHC 的多 residual streams、动态映射与 Sinkhorn 双随机流形约束"),
}

FALLBACK_PAPERS = (
    Paper("RankMixer: Scaling Up Ranking Models in Industrial Recommenders", "Parameter-free token mixing and per-token feed-forward networks for industrial ranking.", [], "2025-07-21", "https://arxiv.org/abs/2507.15551", "2507.15551"),
    Paper("TokenMixer-Large: Scaling Up Large Ranking Models in Industrial Recommenders", "Mixing and reverting, interval residuals, auxiliary losses and sparse per-token MoE.", [], "2026-02-06", "https://arxiv.org/abs/2602.06563", "2602.06563"),
    Paper("Zenith: Scaling up Ranking Models for Billion-scale Livestreaming Recommendation", "Prime Tokens, Token Fusion and Token Boost for scalable ranking.", [], "2026-01-29", "https://arxiv.org/abs/2601.21285", "2601.21285"),
    Paper("MOI-Mixer: Improving MLP-Mixer with Multi Order Interactions in Sequential Recommendation", "Explicit multi-order interactions in mixer channel layers.", [], "2021-08-17", "https://arxiv.org/abs/2108.07505", "2108.07505"),
    Paper("LONGER: Scaling Up Long Sequence Modeling in Industrial Recommenders", "Token merge, global tokens and hybrid attention for ultra-long user sequences.", [], "2025-05-07", "https://arxiv.org/abs/2505.04421", "2505.04421"),
    Paper("UniMixer: A Unified Architecture for Scaling Laws in Recommendation Systems", "Learnable parameterized token mixing for heterogeneous feature interaction.", [], "2026-04-01", "https://arxiv.org/abs/2604.00590", "2604.00590"),
)

LLM_FALLBACK_PAPERS = (
    Paper("PaLM: Scaling Language Modeling with Pathways", "Parallel Transformer layers and SwiGLU in a decoder-only language model.", [], "2022-04-05", "https://arxiv.org/abs/2204.02311", "2204.02311"),
    Paper("LLaMA: Open and Efficient Foundation Language Models", "Pre-normalization with RMSNorm, SwiGLU and rotary positional embeddings.", [], "2023-02-27", "https://arxiv.org/abs/2302.13971", "2302.13971"),
    Paper("GQA: Training Generalized Multi-Query Transformer Models from Multi-Head Checkpoints", "Grouped-query attention shares key/value heads for efficient decoding.", [], "2023-05-22", "https://arxiv.org/abs/2305.13245", "2305.13245"),
    Paper("DoReMi: Optimizing Data Mixtures Speeds Up Language Model Pretraining", "Optimizes domain weights for language-model pretraining data mixtures.", [], "2023-05-17", "https://arxiv.org/abs/2305.10429", "2305.10429"),
    Paper("NEFTune: Noisy Embeddings Improve Instruction Finetuning", "Adds scaled uniform noise to token embeddings during instruction tuning.", [], "2023-10-09", "https://arxiv.org/abs/2310.05914", "2310.05914"),
    Paper("TinyLlama: An Open-Source Small Language Model", "A compact LLaMA-style model trained with staged data mixtures.", [], "2024-01-04", "https://arxiv.org/abs/2401.02385", "2401.02385"),
    Paper("mHC: Manifold-Constrained Hyper-Connections", "Doubly stochastic residual mixing stabilizes multi-stream Hyper-Connections.", [], "2025-12-31", "https://arxiv.org/abs/2512.24880", "2512.24880"),
)


def discover_papers(query: str, limit: int, allow_network: bool, track: str = "recommendation") -> list[PaperInspiration]:
    mutations = LLM_MUTATIONS if track == "llm" else INSTALLED_MUTATIONS
    fallback = LLM_FALLBACK_PAPERS if track == "llm" else FALLBACK_PAPERS
    categories = ("cs.CL", "cs.LG") if track == "llm" else ("cs.IR", "cs.LG")
    papers: list[Paper] = []
    source = "installed evidence"
    if allow_network:
        try:
            papers = ArxivClient().search(query, limit, categories)
            source = "live arXiv search"
        except Exception:
            papers = []
    by_id = {paper.arxiv_id.split("v")[0]: paper for paper in papers}
    # Installed, reviewed mutations remain available even when broad search misses them.
    for paper in fallback:
        by_id.setdefault(paper.arxiv_id, paper)
    ranked = sorted(by_id.values(), key=lambda paper: (paper.arxiv_id not in mutations, paper.published), reverse=False)
    result = []
    for paper in ranked[: max(limit, len(fallback))]:
        paper_id = paper.arxiv_id.split("v")[0]
        architecture, method = mutations.get(paper_id, (None, "检索到相关论文，但尚无经过测试的安全结构算子映射"))
        result.append(PaperInspiration(paper_id, paper.title, paper.url, paper.published[:10], architecture, method, source if paper_id in {p.arxiv_id.split('v')[0] for p in papers} else "installed evidence"))
    return result
