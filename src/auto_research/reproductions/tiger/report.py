def render(result):
    rows = result["results"]
    return "\n".join([
        f"# {result['paper']['title']}", "", f"arXiv `{result['paper']['arxiv_id']}` · {result['dataset']}", "",
        "## Local public-data result", "", "| Identifier | Hit@10 | NDCG@10 | Head share@10 |", "|---|---:|---:|---:|",
        f"| Random ID | {rows['random_id']['hit_at_10']:.4f} ± {rows['random_id']['hit_at_10_std']:.4f} | {rows['random_id']['ndcg_at_10']:.4f} ± {rows['random_id']['ndcg_at_10_std']:.4f} | {rows['random_id']['head_share_at_10']:.4f} |",
        f"| RQ-VAE Semantic ID | {rows['tiger']['hit_at_10']:.4f} ± {rows['tiger']['hit_at_10_std']:.4f} | {rows['tiger']['ndcg_at_10']:.4f} ± {rows['tiger']['ndcg_at_10_std']:.4f} | {rows['tiger']['head_share_at_10']:.4f} |",
        "", f"TIGER NDCG@10 change vs random IDs: **{result['ndcg_gain_percent']:+.2f}%**.",
        "", "## Paper's production A/B evidence", "", "The paper reports no production online A/B test; this adapter is a user-requested classic-paper exception.",
        "", "## Reproduction boundary", "", result["scope"], "",
    ])
