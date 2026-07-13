from __future__ import annotations

from typing import Any


def render(result: dict[str, Any]) -> str:
    paper = result["paper"]
    lines = [
        f"# {paper['title']}",
        "",
        f"arXiv `{paper['arxiv_id']}` · dataset: {result['dataset']}",
        "",
        "| Sampler | Hit@10 | NDCG@10 |",
        "|---|---:|---:|",
    ]
    for method, row in result["results"].items():
        lines.append(
            f"| {method} | {row['hit_at_10']:.6f} | {row['ndcg_at_10']:.6f} |"
        )
    lines.extend(
        [
            "",
            f"MDCNS NDCG@10 change versus Uniform: **{result['ndcg10_gain_vs_uniform_percent']:.2f}%**.",
            "",
            "## Scope",
            "",
            "Mac-scale reproduction of the paper-specific sampler and distillation path; this does not claim to reproduce all six datasets and neural backbones.",
            "",
        ]
    )
    return "\n".join(lines)
