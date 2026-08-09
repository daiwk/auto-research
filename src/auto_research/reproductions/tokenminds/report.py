def render(result: dict) -> str:
    baseline, method = result["baseline"], result["method"]
    return "\n".join(
        [
            "# TokenMinds",
            "",
            f"公开数据：MovieLens-1M（{result['dataset']['users']} users / {result['dataset']['items']} items）。",
            "",
            "| Variant | Hit@10 | NDCG@10 | Head share@10 |",
            "|---|---:|---:|---:|",
            f"| {baseline['name']} | {baseline['hit_at_10']:.4f} | {baseline['ndcg_at_10']:.4f} | {baseline['head_share_at_10']:.4f} |",
            f"| {method['name']} | {method['hit_at_10']:.4f} | {method['ndcg_at_10']:.4f} | {method['head_share_at_10']:.4f} |",
            "",
            f"相对 dense-only 公平基线：NDCG@10 {result['relative']['ndcg_at_10_percent']:+.2f}%。",
            "",
            "## 复现边界",
            "",
            result["scope"],
            "",
        ]
    )
