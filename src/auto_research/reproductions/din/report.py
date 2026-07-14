def render(result):
    rows, ab = result["results"], result["paper_online_ab"]
    return "\n".join([
        f"# {result['paper']['title']}", "", f"arXiv `{result['paper']['arxiv_id']}` · {result['dataset']}", "",
        "## Local public-data result", "", "| Model | Hit@10 | NDCG@10 | Head share@10 |", "|---|---:|---:|---:|",
        f"| Mean pooling DNN | {rows['mean_pool']['hit_at_10']:.4f} ± {rows['mean_pool']['hit_at_10_std']:.4f} | {rows['mean_pool']['ndcg_at_10']:.4f} ± {rows['mean_pool']['ndcg_at_10_std']:.4f} | {rows['mean_pool']['head_share_at_10']:.4f} |",
        f"| DIN | {rows['din']['hit_at_10']:.4f} ± {rows['din']['hit_at_10_std']:.4f} | {rows['din']['ndcg_at_10']:.4f} ± {rows['din']['ndcg_at_10_std']:.4f} | {rows['din']['head_share_at_10']:.4f} |",
        "", f"DIN NDCG@10 change vs mean pooling: **{result['ndcg_gain_percent']:+.2f}%**.",
        "", "## Paper's production A/B evidence", "", f"Alibaba's month-long A/B test ({ab['period']}) reports CTR **+{ab['ctr_percent']:.1f}%** and RPM **+{ab['rpm_percent']:.1f}%**.",
        "", "## Reproduction boundary", "", result["scope"], "",
    ])
