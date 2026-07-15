from __future__ import annotations


def render(result: dict) -> str:
    lines = [
        "# SIGMA", "", "| Variant | HR@1 | HR@5 | HR@10 | HR@20 | NDCG@10 |",
        "|---|---:|---:|---:|---:|---:|",
    ]
    for name, values in result["test"].items():
        lines.append(
            f"| {name} | {values['hr_at_1']:.4f} | {values['hr_at_5']:.4f} | "
            f"{values['hr_at_10']:.4f} | {values['hr_at_20']:.4f} | {values['ndcg_at_10']:.4f} |"
        )
    lines.extend(
        [
            "", f"Validation selected `{result['setup']['selected_variant']}`.", "",
            "## Reproduction boundary", "", result["scope"],
        ]
    )
    return "\n".join(lines)
