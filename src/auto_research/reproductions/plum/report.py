from typing import Any


def render(result: dict[str, Any]) -> str:
    lines = [f"# {result['paper']['title']}", "", f"arXiv `{result['paper']['arxiv_id']}` · {result['dataset']}", "", "## Local public-data result", "", "| Retrieval | Hit@10 | NDCG@10 |", "|---|---:|---:|"]
    for name, row in result["results"].items():
        lines.append(f"| {name} | {row['hit_at_10']:.4f} | {row['ndcg_at_10']:.4f} |")
    ab = result["paper_online_ab"]
    lines += ["", f"PLUM local NDCG@10 change: **{result['ndcg_gain_percent']:+.2f}%**.", "", "## Paper's production A/B evidence", "", f"YouTube LFV engaged users/panel CTR: **+{ab['lfv_engaged_users_percent']:.2f}% / +{ab['lfv_panel_ctr_percent']:.2f}%**; Shorts: **+{ab['shorts_engaged_users_percent']:.2f}% / +{ab['shorts_panel_ctr_percent']:.2f}%**.", "", "## Reproduction boundary", "", result["scope"], ""]
    return "\n".join(lines)
