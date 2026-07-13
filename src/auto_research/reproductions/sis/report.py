from __future__ import annotations

from typing import Any


def render(result: dict[str, Any]) -> str:
    paper = result["paper"]
    lines = [
        f"# {paper['title']}",
        "",
        f"arXiv `{paper['arxiv_id']}` · dataset: {result['dataset']}",
        "",
        "| Method | Weight variance | Mean |log ratio| | ESS | Accept rate |",
        "|---|---:|---:|---:|---:|",
    ]
    for key in ("baseline", "method"):
        row = result[key]
        lines.append(
            f"| {row['method']} | {row['weight_variance']:.6f} | "
            f"{row['mean_abs_log_ratio']:.6f} | {row['effective_sample_size']:.1f} | "
            f"{row['acceptance_rate']:.2%} |"
        )
    lines.extend(
        [
            "",
            f"SIS reduced importance-weight variance by **{result['variance_reduction_percent']:.2f}%**.",
            "",
            "## Scope",
            "",
            "Mechanism-level Mac reproduction; this does not claim to reproduce the paper's Qwen/GRPO accuracy numbers.",
            "",
        ]
    )
    return "\n".join(lines)
