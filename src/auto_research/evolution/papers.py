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

FALLBACK_PAPERS = (
    Paper("RankMixer: Scaling Up Ranking Models in Industrial Recommenders", "Parameter-free token mixing and per-token feed-forward networks for industrial ranking.", [], "2025-07-21", "https://arxiv.org/abs/2507.15551", "2507.15551"),
    Paper("TokenMixer-Large: Scaling Up Large Ranking Models in Industrial Recommenders", "Mixing and reverting, interval residuals, auxiliary losses and sparse per-token MoE.", [], "2026-02-06", "https://arxiv.org/abs/2602.06563", "2602.06563"),
    Paper("Zenith: Scaling up Ranking Models for Billion-scale Livestreaming Recommendation", "Prime Tokens, Token Fusion and Token Boost for scalable ranking.", [], "2026-01-29", "https://arxiv.org/abs/2601.21285", "2601.21285"),
    Paper("MOI-Mixer: Improving MLP-Mixer with Multi Order Interactions in Sequential Recommendation", "Explicit multi-order interactions in mixer channel layers.", [], "2021-08-17", "https://arxiv.org/abs/2108.07505", "2108.07505"),
    Paper("LONGER: Scaling Up Long Sequence Modeling in Industrial Recommenders", "Token merge, global tokens and hybrid attention for ultra-long user sequences.", [], "2025-05-07", "https://arxiv.org/abs/2505.04421", "2505.04421"),
    Paper("UniMixer: A Unified Architecture for Scaling Laws in Recommendation Systems", "Learnable parameterized token mixing for heterogeneous feature interaction.", [], "2026-04-01", "https://arxiv.org/abs/2604.00590", "2604.00590"),
)


def discover_papers(query: str, limit: int, allow_network: bool) -> list[PaperInspiration]:
    papers: list[Paper] = []
    source = "installed evidence"
    if allow_network:
        try:
            papers = ArxivClient().search(query, limit, ("cs.IR", "cs.LG"))
            source = "live arXiv search"
        except Exception:
            papers = []
    by_id = {paper.arxiv_id.split("v")[0]: paper for paper in papers}
    # Installed, reviewed mutations remain available even when broad search misses them.
    for paper in FALLBACK_PAPERS:
        by_id.setdefault(paper.arxiv_id, paper)
    ranked = sorted(by_id.values(), key=lambda paper: (paper.arxiv_id not in INSTALLED_MUTATIONS, paper.published), reverse=False)
    result = []
    for paper in ranked[: max(limit, len(FALLBACK_PAPERS))]:
        paper_id = paper.arxiv_id.split("v")[0]
        architecture, method = INSTALLED_MUTATIONS.get(paper_id, (None, "检索到相关论文，但尚无经过测试的安全结构算子映射"))
        result.append(PaperInspiration(paper_id, paper.title, paper.url, paper.published[:10], architecture, method, source if paper_id in {p.arxiv_id.split('v')[0] for p in papers} else "installed evidence"))
    return result
