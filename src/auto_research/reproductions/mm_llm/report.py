from typing import Any


def render(result: dict[str, Any]) -> str:
    rows = result["results"]
    return "\n".join([f"# {result['paper']['title']}", "", f"arXiv `{result['paper']['arxiv_id']}` · {result['dataset']}", "", "| Model | Hit@10 | NDCG@10 |", "|---|---:|---:|", *[f"| {n} | {v['hit_at_10']:.4f} ± {v['hit_at_10_std']:.4f} | {v['ndcg_at_10']:.4f} ± {v['ndcg_at_10_std']:.4f} |" for n, v in rows.items()], "", f"NDCG@10 change: **{result['ndcg_gain_percent']:+.2f}%**.", "", "## Reproduction boundary", "", result["scope"], ""])

