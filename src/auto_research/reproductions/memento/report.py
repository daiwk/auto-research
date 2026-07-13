from typing import Any


def render(result: dict[str, Any]) -> str:
    lines = [f"# {result['paper']['title']}", "", f"arXiv `{result['paper']['arxiv_id']}` · {result['dataset']}", "", "## Local public-data result", "", "| History method | Hit@10 | NDCG@10 | Head share@10 |", "|---|---:|---:|---:|"]
    for name, row in result["results"].items():
        lines.append(f"| {name} | {row['hit_at_10']:.4f} | {row['ndcg_at_10']:.4f} | {row['head_share_at_10']:.4f} |")
    ab = result["paper_online_ab"]
    lines += ["", f"Memento local NDCG@10 change: **{result['ndcg_gain_percent']:+.2f}%**; validation-selected relevance weight: **{result['setup']['validation_selected_relevance_weight']:.2f}**.", "", "## Paper's production A/B evidence", "", f"Meta reports **+{ab['ctr_lift_percent']:.1f}% CTR** and **+{ab['cvr_lift_percent']:.1f}% CVR** after several rounds of large-scale A/B testing.", "", "## Reproduction boundary", "", result["scope"], ""]
    return "\n".join(lines)
