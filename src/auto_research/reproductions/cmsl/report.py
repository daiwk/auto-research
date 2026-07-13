from typing import Any


def render(result: dict[str, Any]) -> str:
    lines = [f"# {result['paper']['title']}", "", f"arXiv `{result['paper']['arxiv_id']}` · {result['dataset']}", "", "## Local public-data result", "", "| Model | Hit@10 | NDCG@10 |", "|---|---:|---:|"]
    for name, row in result["results"].items():
        lines.append(f"| {name} | {row['hit_at_10']:.4f} ± {row['hit_at_10_std']:.4f} | {row['ndcg_at_10']:.4f} ± {row['ndcg_at_10_std']:.4f} |")
    ab = result["paper_online_ab"]
    lines += ["", f"CMSL local NDCG@10 change: **{result['ndcg_gain_percent']:+.2f}%**. Validation-selected mixture weights by seed: `{result['setup']['validation_selected_alpha']}`.", "", "## Paper's production A/B evidence", "", f"Meta reports statistically significant retrieval lifts of **+{ab['metric_1']:.3f}%**, **+{ab['metric_2']:.3f}%**, **+{ab['metric_3']:.3f}%**, and **+{ab['metric_4']:.3f}%** on four engagement metrics.", "", "## Reproduction boundary", "", result["scope"], ""]
    return "\n".join(lines)
