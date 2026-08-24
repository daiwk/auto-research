def render(result):
    lines = ["# NEXT", "", "| Variant | Hit@10 | NDCG@10 |", "|---|---:|---:|"]
    for name, row in result["variants"].items():
        lines.append(f"| {name} | {row['hit_at_10']:.4f} | {row['ndcg_at_10']:.4f} |")
    lines += ["", "## 复现边界", "", result["scope"], ""]
    return "\n".join(lines)
