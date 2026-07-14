def render(result):
    rows = result["results"]
    return "\n".join([
        f"# {result['paper']['title']}", "",
        f"arXiv `{result['paper']['arxiv_id']}` · {result['dataset']}", "",
        "## Local public-data result", "",
        "| Model | Hit@10 | NDCG@10 | Head share@10 |", "|---|---:|---:|---:|",
        f"| TransAct | {rows['transact']['hit_at_10']:.4f} ± {rows['transact']['hit_at_10_std']:.4f} | {rows['transact']['ndcg_at_10']:.4f} ± {rows['transact']['ndcg_at_10_std']:.4f} | {rows['transact']['head_share_at_10']:.4f} |",
        f"| TransAct V2 | {rows['transact_v2']['hit_at_10']:.4f} ± {rows['transact_v2']['hit_at_10_std']:.4f} | {rows['transact_v2']['ndcg_at_10']:.4f} ± {rows['transact_v2']['ndcg_at_10_std']:.4f} | {rows['transact_v2']['head_share_at_10']:.4f} |",
        "", f"TransAct V2 NDCG@10 change: **{result['ndcg_gain_percent']:+.2f}%**.",
        "", "## Paper's production A/B evidence", "",
        "Pinterest Homefeed: Repin Volume +6.35%, Hide Volume -12.80%, Impression Diversity +0.45%, Time Spent +1.41%; each arm served 1.5% traffic.",
        "", "## Reproduction boundary", "", result["scope"], "",
    ])
