from typing import Any


def render(result: dict[str, Any]) -> str:
    lines = [f"# {result['paper']['title']}", "", f"arXiv `{result['paper']['arxiv_id']}` · {result['dataset']}", "", "## Local public-data result", "", "| Workflow | Hit@10 | NDCG@10 |", "|---|---:|---:|"]
    for name, row in result["results"].items():
        lines.append(f"| {name} | {row['hit_at_10']:.4f} ± {row['hit_at_10_std']:.4f} | {row['ndcg_at_10']:.4f} ± {row['ndcg_at_10_std']:.4f} |")
    ab = result["paper_online_ab"]
    lines += ["", f"Promoted candidates by seed: `{result['setup']['promoted_candidates']}`. Local NDCG@10 change: **{result['ndcg_gain_percent']:+.2f}%**.", "", "## Paper's production A/B evidence", "", f"Google reports statistically significant YouTube/surface lifts for RMSProp (**+{ab['rmsprop_youtube_percent']:.2f}%/+{ab['rmsprop_surface_percent']:.2f}%**), GLU (**+{ab['glu_youtube_percent']:.2f}%/+{ab['glu_surface_percent']:.2f}%**), and synthesized reward (**+{ab['reward_youtube_percent']:.2f}%/+{ab['reward_surface_percent']:.2f}%**).", "", "## Reproduction boundary", "", result["scope"], ""]
    return "\n".join(lines)
