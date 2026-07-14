from typing import Any


def render(result: dict[str, Any]) -> str:
    rows = result["results"]
    return "\n".join([
        f"# {result['paper']['title']}", "", f"arXiv `{result['paper']['arxiv_id']}` · {result['dataset']}", "",
        "| Model | Hit@10 | NDCG@10 |", "|---|---:|---:|",
        *[f"| {name} | {value['hit_at_10']:.4f} ± {value['hit_at_10_std']:.4f} | {value['ndcg_at_10']:.4f} ± {value['ndcg_at_10_std']:.4f} |" for name, value in rows.items()],
        "", f"NDCG@10 change: **{result['ndcg_gain_percent']:+.2f}%**.", "", "## Reproduction boundary", "", result["scope"], "",
    ])

