def render(result):
    rows = result["results"]
    return "\n".join([
        f"# {result['paper']['title']}", "",
        f"arXiv `{result['paper']['arxiv_id']}` · {result['dataset']}", "",
        "## Local public-data result", "",
        "| Model | Hit@10 | NDCG@10 | Head share@10 |", "|---|---:|---:|---:|",
        f"| Scratch DCAT | {rows['scratch_dcat']['hit_at_10']:.4f} ± {rows['scratch_dcat']['hit_at_10_std']:.4f} | {rows['scratch_dcat']['ndcg_at_10']:.4f} ± {rows['scratch_dcat']['ndcg_at_10_std']:.4f} | {rows['scratch_dcat']['head_share_at_10']:.4f} |",
        f"| PinFM | {rows['pinfm']['hit_at_10']:.4f} ± {rows['pinfm']['hit_at_10_std']:.4f} | {rows['pinfm']['ndcg_at_10']:.4f} ± {rows['pinfm']['ndcg_at_10_std']:.4f} | {rows['pinfm']['head_share_at_10']:.4f} |",
        "", f"PinFM NDCG@10 change vs scratch DCAT: **{result['ndcg_gain_percent']:+.2f}%**.",
        "", "## Paper's production A/B evidence", "",
        "Pinterest Homefeed: sitewide Saves +1.20%, surface Saves +2.60%, fresh Saves +5.70%; I2I: sitewide Saves +0.72%, surface Saves +2.09%.",
        "", "## Reproduction boundary", "", result["scope"], "",
    ])
