from __future__ import annotations


def render(result: dict) -> str:
    lines = [
        "# LWGR", "", "| Variant | Recall@5 | NDCG@5 | Recall@10 | NDCG@10 |",
        "|---|---:|---:|---:|---:|",
    ]
    for name, metrics in result["test"].items():
        lines.append(
            f"| {name} | {metrics['recall_at_5']:.4f} | {metrics['ndcg_at_5']:.4f} | "
            f"{metrics['recall_at_10']:.4f} | {metrics['ndcg_at_10']:.4f} |"
        )
    lines.extend(
        [
            "", f"Validation selected `{result['setup']['selected_variant']}`.", "",
            "## Reproduction boundary", "", result["scope"],
        ]
    )
    return "\n".join(lines)
