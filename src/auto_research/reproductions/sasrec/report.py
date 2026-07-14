def render(result):
    rows = result["results"]
    return "\n".join([
        f"# {result['paper']['title']}", "",
        f"arXiv `{result['paper']['arxiv_id']}` · {result['dataset']}", "",
        "## Local public-data result", "",
        "| Model | Hit@10 | NDCG@10 | Head share@10 |", "|---|---:|---:|---:|",
        f"| Popularity | {rows['popularity']['hit_at_10']:.4f} | {rows['popularity']['ndcg_at_10']:.4f} | {rows['popularity']['head_share_at_10']:.4f} |",
        f"| SASRec | {rows['sasrec']['hit_at_10']:.4f} ± {rows['sasrec']['hit_at_10_std']:.4f} | {rows['sasrec']['ndcg_at_10']:.4f} ± {rows['sasrec']['ndcg_at_10_std']:.4f} | {rows['sasrec']['head_share_at_10']:.4f} |",
        "", f"SASRec NDCG@10 change vs popularity: **{result['ndcg_gain_percent']:+.2f}%**.",
        "", "## Paper's production A/B evidence", "", "The paper reports no production online A/B test; this adapter is a user-requested classic-baseline exception.",
        "", "## Reproduction boundary", "", result["scope"], "",
    ])
