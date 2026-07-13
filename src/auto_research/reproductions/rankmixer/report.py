from typing import Any


def render(result: dict[str, Any]) -> str:
    lines = [f"# {result['paper']['title']}", "", f"arXiv `{result['paper']['arxiv_id']}` · {result['dataset']}", "", "## Local public-data result", "", "| Architecture | Hit@10 | NDCG@10 | Head share@10 |", "|---|---:|---:|---:|"]
    for name, row in result["results"].items():
        lines.append(f"| {name} | {row['hit_at_10']:.4f} | {row['ndcg_at_10']:.4f} | {row['head_share_at_10']:.4f} |")
    ab = result["paper_online_ab"]
    lines += ["", f"Sparse RankMixer local NDCG@10 change vs shared FFN: **{result['ndcg_gain_percent']:+.2f}%**.", "", "## Paper's production A/B evidence", "", f"Full-traffic Douyin deployment reports Active Days **+{ab['active_days_percent']:.2f}%** and app duration **+{ab['duration_percent']:.2f}%**.", "", "## Reproduction boundary", "", result["scope"], ""]
    return "\n".join(lines)
