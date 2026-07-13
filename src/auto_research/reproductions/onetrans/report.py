from typing import Any


def render(result: dict[str, Any]) -> str:
    lines = [f"# {result['paper']['title']}", "", f"arXiv `{result['paper']['arxiv_id']}` · {result['dataset']}", "", "## Local public-data result", "", "| Architecture | Hit@10 | NDCG@10 |", "|---|---:|---:|"]
    for name, row in result["results"].items():
        lines.append(f"| {name} | {row['hit_at_10']:.4f} ± {row['hit_at_10_std']:.4f} | {row['ndcg_at_10']:.4f} ± {row['ndcg_at_10_std']:.4f} |")
    ab = result["paper_online_ab"]
    lines += ["", f"OneTrans local NDCG@10 change: **{result['ndcg_gain_percent']:+.2f}%**.", "", "## Paper's production A/B evidence", "", f"Feeds order/GMV per user **+{ab['feeds_order_percent']:.4f}%/+{ab['feeds_gmv_percent']:.4f}%** with p99 latency **{ab['feeds_latency_percent']:.2f}%**; Mall order/GMV **+{ab['mall_order_percent']:.4f}%/+{ab['mall_gmv_percent']:.4f}%**.", "", "## Reproduction boundary", "", result["scope"], ""]
    return "\n".join(lines)
