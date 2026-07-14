def render(result):
    rows = result["results"]
    ab = result["paper_online_ab"]
    return "\n".join([
        f"# {result['paper']['title']}", "", f"arXiv `{result['paper']['arxiv_id']}` · {result['dataset']}", "",
        "## Local public-data result", "", "| Model | Hit@10 | NDCG@10 | Head share@10 |", "|---|---:|---:|---:|",
        f"| SASRec | {rows['sasrec']['hit_at_10']:.4f} ± {rows['sasrec']['hit_at_10_std']:.4f} | {rows['sasrec']['ndcg_at_10']:.4f} ± {rows['sasrec']['ndcg_at_10_std']:.4f} | {rows['sasrec']['head_share_at_10']:.4f} |",
        f"| HSTU | {rows['hstu']['hit_at_10']:.4f} ± {rows['hstu']['hit_at_10_std']:.4f} | {rows['hstu']['ndcg_at_10']:.4f} ± {rows['hstu']['ndcg_at_10_std']:.4f} | {rows['hstu']['head_share_at_10']:.4f} |",
        "", f"HSTU NDCG@10 change vs matched SASRec: **{result['ndcg_gain_percent']:+.2f}%**.",
        "", "## Paper's production A/B evidence", "", f"The production GR ranking A/B reports engagement **+{ab['ranking_engagement_percent']:.1f}%** and consumption **+{ab['ranking_consumption_percent']:.1f}%**.",
        "", "## Reproduction boundary", "", result["scope"], "",
    ])
