def render(result):
    rows = result["results"]
    lines = [
        f"# {result['paper']['title']}",
        "",
        f"arXiv `{result['paper']['arxiv_id']}` · {result['dataset']}",
        "",
        "## Local public-data result",
        "",
        "| Variant | Hit@10 | NDCG@10 | Head share@10 |",
        "|---|---:|---:|---:|",
    ]
    for name in ("ntp", "tcl", "tdl", "nontp"):
        row = rows[name]
        lines.append(
            f"| {name.upper()} | {row['hit_at_10']:.4f} ± {row['hit_at_10_std']:.4f} | "
            f"{row['ndcg_at_10']:.4f} ± {row['ndcg_at_10_std']:.4f} | {row['head_share_at_10']:.4f} |"
        )
    lines += [
        "",
        f"NONTP relative to the same-backbone NTP baseline: Hit@10 "
        f"**{result['relative']['hit_at_10_percent']:+.2f}%**, NDCG@10 "
        f"**{result['relative']['ndcg_at_10_percent']:+.2f}%**.",
        "",
        "## Reproduction boundary",
        "",
        result["scope"],
        "",
    ]
    return "\n".join(lines)
