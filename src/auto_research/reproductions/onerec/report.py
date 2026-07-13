from typing import Any


def render(result: dict[str, Any]) -> str:
    lines = [f"# {result['paper']['title']}", "", f"arXiv `{result['paper']['arxiv_id']}` · {result['dataset']}", "", "## Local public-data result", "", "| Method | Hit@10 | NDCG@10 | Head share@10 |", "|---|---:|---:|---:|"]
    for name, row in result["results"].items():
        lines.append(f"| {name} | {row['hit_at_10']:.4f} | {row['ndcg_at_10']:.4f} | {row['head_share_at_10']:.4f} |")
    ab = result["paper_online_ab"]
    dpo = result["training"]["dpo"]
    lines += ["", f"OneRec local NDCG@10 change after DPO: **{result['ndcg_gain_percent']:+.2f}%** from **{dpo['pairs']}** self-sampled preference pairs.", "", "## Paper's production A/B evidence", "", f"On **{ab['traffic_percent']:.0f}%** Kuaishou main traffic, total watch time improved **+{ab['total_watch_time_percent']:.2f}%** and average view duration **+{ab['average_view_duration_percent']:.2f}%**.", "", "## Reproduction boundary", "", result["scope"], ""]
    return "\n".join(lines)
