def render(result: dict) -> str:
    lines = ["# WeMM-Embedding", "", "| Variant | Recall@1 | Recall@10 | MRR |", "|---|---:|---:|---:|"]
    for name, row in result["variants"].items():
        lines.append(f"| {name} | {row['recall_at_1']:.4f} | {row['recall_at_10']:.4f} | {row['mrr']:.4f} |")
    lines += ["", "## 复现边界", "", result["scope"], ""]
    return "\n".join(lines)
