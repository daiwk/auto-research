def render(result: dict) -> str:
    lines = [
        "# Netflix GenRec local reproduction",
        "",
        f"Dataset: {result['dataset']['name']} ({result['dataset']['users']} users / "
        f"{result['dataset']['items']} items).",
        "",
        "| Variant | Hit@10 | NDCG@10 | MRR | Head share@10 |",
        "|---|---:|---:|---:|---:|",
    ]
    for name, row in result["variants"].items():
        lines.append(
            f"| {name} | {row['hit_at_10']:.5f} | {row['ndcg_at_10']:.5f} | "
            f"{row['mrr']:.5f} | {row['head_share_at_10']:.5f} |"
        )
    lines.extend(("", "## Scope", "", result["scope"], ""))
    return "\n".join(lines)
