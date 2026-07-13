from typing import Any


def render(result: dict[str, Any]) -> str:
    lines = [f"# {result['paper']['title']}", "", f"arXiv `{result['paper']['arxiv_id']}` · {result['dataset']}", "", "## Local public-data result", "", "| Architecture | Hit@10 | NDCG@10 |", "|---|---:|---:|"]
    for name, row in result["results"].items():
        lines.append(f"| {name} | {row['hit_at_10']:.4f} ± {row['hit_at_10_std']:.4f} | {row['ndcg_at_10']:.4f} ± {row['ndcg_at_10_std']:.4f} |")
    ab = result["paper_online_ab"]
    lines += ["", f"MixFormer local NDCG@10 change: **{result['ndcg_gain_percent']:+.2f}%**.", "", "## Paper's production A/B evidence", "", f"Douyin/Douyin Lite duration: **+{ab['douyin_duration_percent']:.4f}% / +{ab['douyin_lite_duration_percent']:.4f}%**; comments: **+{ab['douyin_comment_percent']:.4f}% / +{ab['douyin_lite_comment_percent']:.4f}%**.", "", "## Reproduction boundary", "", result["scope"], ""]
    return "\n".join(lines)
