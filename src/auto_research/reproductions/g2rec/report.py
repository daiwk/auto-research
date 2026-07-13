from typing import Any


def render(result: dict[str, Any]) -> str:
    lines = [f"# {result['paper']['title']}", "", f"arXiv `{result['paper']['arxiv_id']}` · {result['dataset']}", "", "## Local public-data result", "", "| Tokenization | Hit@10 | NDCG@10 | Head share@10 |", "|---|---:|---:|---:|"]
    for name, row in result["results"].items():
        lines.append(f"| {name} | {row['hit_at_10']:.4f} | {row['ndcg_at_10']:.4f} | {row['head_share_at_10']:.4f} |")
    low, high = result["paper_online_ab"]["engagement_lift_range_percent"]
    lines += ["", f"G2Rec local NDCG@10 change: **{result['ndcg_gain_percent']:+.2f}%**; validation-selected graph-token weight: **{result['setup']['validation_selected_beta']:.2f}**.", "", "## Paper's production A/B evidence", "", f"The paper reports more than **+{result['paper_online_ab']['in_session_lift_lower_bound_percent']:.2f}%** in-session improvement and **+{low:.2f}% to +{high:.2f}%** across engagement metrics including time spent, likes, and shares.", "", "## Reproduction boundary", "", result["scope"], ""]
    return "\n".join(lines)
