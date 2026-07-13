from typing import Any


def render(result: dict[str, Any]) -> str:
    lines = [
        f"# {result['paper']['title']}", "",
        f"arXiv `{result['paper']['arxiv_id']}` · {result['dataset']}", "",
        "## Local public-data result", "",
        "Mean ± standard deviation across three seeds.", "",
        "| Sampler | Hit@10 | NDCG@10 | Head share@10 |",
        "|---|---:|---:|---:|",
    ]
    for name, row in result["results"].items():
        lines.append(f"| {name} | {row['hit_at_10']:.4f} ± {row['hit_at_10_std']:.4f} | {row['ndcg_at_10']:.4f} ± {row['ndcg_at_10_std']:.4f} | {row['head_share_at_10']:.4f} ± {row['head_share_at_10_std']:.4f} |")
    ab = result["paper_online_ab"]
    lines += [
        "", f"Cluster GOOBS local NDCG@10 change: **{result['ndcg_gain_percent']:+.2f}%**; head-item share change: **{result['head_share_change_percent']:+.2f}%**.",
        "", "## Paper's production A/B evidence", "",
        f"The paper reports **+{ab['ctr_lift_percent']:.0f}% CTR** and a top-100 impression-share reduction from **{ab['top_100_impression_share_control_percent']:.0f}% to {ab['top_100_impression_share_treatment_percent']:.0f}%**.",
        "", "## Reproduction boundary", "", result["scope"], "",
    ]
    return "\n".join(lines)
