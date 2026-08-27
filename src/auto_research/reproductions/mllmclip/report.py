def render(result: dict) -> str:
    lines = ["# MLLMCLIP", "", "| Variant | Recall@10 | Linear CKA |", "|---|---:|---:|"]
    for name, row in result["variants"].items():
        lines.append(f"| {name} | {row['recall_at_10']:.4f} | {row['linear_cka']:.4f} |")
    lines += ["", "## 复现边界", "", result["scope"], ""]
    return "\n".join(lines)
