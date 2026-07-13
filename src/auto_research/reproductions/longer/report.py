from typing import Any


def render(result: dict[str, Any]) -> str:
    lines = [f"# {result['paper']['title']}", "", f"arXiv `{result['paper']['arxiv_id']}` · {result['dataset']}", "", "## Local public-data result", "", "| Architecture | Hit@10 | NDCG@10 |", "|---|---:|---:|"]
    for name, row in result["results"].items():
        lines.append(f"| {name} | {row['hit_at_10']:.4f} ± {row['hit_at_10_std']:.4f} | {row['ndcg_at_10']:.4f} ± {row['ndcg_at_10_std']:.4f} |")
    ads = result["paper_online_ab"]["douyin_ads_adss_range_percent"]
    orders = result["paper_online_ab"]["douyin_ecommerce_order_per_user_range_percent"]
    lines += ["", f"LONGER local NDCG@10 change: **{result['ndcg_gain_percent']:+.2f}%**.", "", "## Paper's production A/B evidence", "", f"Douyin Ads ADSS: **+{ads[0]:.3f}% to +{ads[1]:.3f}%**; Douyin E-commerce Order/U: **+{orders[0]:.4f}% to +{orders[1]:.4f}%**.", "", "## Reproduction boundary", "", result["scope"], ""]
    return "\n".join(lines)
