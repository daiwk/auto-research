def render(result: dict) -> str:
    baseline, method = result["baseline"], result["method"]
    return "\n".join(
        [
            "# Mosaic",
            "",
            f"公开数据：MovieLens-1M（{result['dataset']['users']} users / {result['dataset']['items']} items）。",
            "",
            "| Variant | Hit@10 | NDCG@10 | Head share@10 |",
            "|---|---:|---:|---:|",
            f"| {baseline['name']} | {baseline['hit_at_10']:.4f} | {baseline['ndcg_at_10']:.4f} | {baseline['head_share_at_10']:.4f} |",
            f"| {method['name']} | {method['hit_at_10']:.4f} | {method['ndcg_at_10']:.4f} | {method['head_share_at_10']:.4f} |",
            "",
            f"相对同协议单 specialist 基线：NDCG@10 {result['relative']['ndcg_at_10_percent']:+.2f}%。",
            "",
            "## 复现边界",
            "",
            result["scope"],
            "",
        ]
    )
