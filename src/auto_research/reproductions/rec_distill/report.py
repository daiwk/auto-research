from typing import Any


def render(result: dict[str, Any]) -> str:
    lines = [f"# {result['paper']['title']}", "", f"arXiv `{result['paper']['arxiv_id']}` · {result['dataset']}", "", "## Local public-data result", "", "| Model | Hit@10 | NDCG@10 |", "|---|---:|---:|"]
    for name, row in result["results"].items():
        lines.append(f"| {name} | {row['hit_at_10']:.4f} | {row['ndcg_at_10']:.4f} |")
    ab = result["paper_online_ab"]
    transferability = result["transferability"]
    transfer_text = "undefined because the local teacher did not beat the raw student" if transferability is None else f"**{100 * transferability:.2f}%**"
    lines += ["", f"Local distillation transferability: {transfer_text}.", "", "## Paper's production A/B evidence", "", f"Ads ADVV **+{ab['ads_advv_percent']:.2f}%**, recommendation Finish/U **+{ab['recommendation_finish_per_user_percent']:.4f}%**, live gift revenue **+{ab['live_gift_revenue_percent']:.2f}%**.", "", "## Reproduction boundary", "", result["scope"], ""]
    return "\n".join(lines)
