from typing import Any


def render(result: dict[str, Any]) -> str:
    lines = [f"# {result['paper']['title']}", "", f"arXiv `{result['paper']['arxiv_id']}` · {result['dataset']}", "", "## Local public-data result", "", "Mean ± standard deviation across three seeds.", "", "| Architecture | Hit@10 | NDCG@10 |", "|---|---:|---:|"]
    for name, row in result["results"].items():
        lines.append(f"| {name} | {row['hit_at_10']:.4f} ± {row['hit_at_10_std']:.4f} | {row['ndcg_at_10']:.4f} ± {row['ndcg_at_10_std']:.4f} |")
    ab = result["paper_online_ab"]
    lines += ["", f"LLaTTE local NDCG@10 change: **{result['ndcg_gain_percent']:+.2f}%**. Validation-selected target-aware/upstream weights: `{result['setup']['validation_selected_weights']}`.", "", "## Paper's production A/B evidence", "", f"Meta reports **+{ab['conversion_lift_percent']:.1f}% conversion** and **-{ab['normalized_entropy_reduction_percent']:.2f}% normalized entropy** across multiple large-scale A/B tests.", "", "## Reproduction boundary", "", result["scope"], ""]
    return "\n".join(lines)
