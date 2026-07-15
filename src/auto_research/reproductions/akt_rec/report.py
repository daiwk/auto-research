def render(result):
    rows = result["test"]
    lines = [
        f"# {result['paper']['title']}",
        "",
        f"arXiv `{result['paper']['arxiv_id']}` · {result['dataset']['name']}",
        "",
        "## Local public-data result",
        "",
        "| Variant | AUC | GAUC | Tail AUC |",
        "|---|---:|---:|---:|",
    ]
    for name in ("online_base", "akt_rec"):
        row = rows[name]
        lines.append(
            f"| {name} | {row['auc']:.4f} ± {row['auc_std']:.4f} | "
            f"{row['gauc']:.4f} ± {row['gauc_std']:.4f} | "
            f"{row['tail_auc']:.4f} ± {row['tail_auc_std']:.4f} |"
        )
    lines += [
        "",
        f"AKT-Rec relative to the same sampled-CTR online-base model: AUC "
        f"**{result['relative']['auc_percent']:+.2f}%**, GAUC "
        f"**{result['relative']['gauc_percent']:+.2f}%**, tail AUC "
        f"**{result['relative']['tail_auc_percent']:+.2f}%**.",
        "",
        "## Reproduction boundary",
        "",
        result["scope"],
        "",
    ]
    return "\n".join(lines)
