def render(result: dict) -> str:
    baseline, method = result["baseline"], result["method"]
    return "\n".join((
        "# ConnectionMind", "",
        f"公开数据：{result['dataset']['name']}（{result['dataset']['users']} users / {result['dataset']['items']} items）。", "",
        "| Variant | Recall@10 | Precision@10 | NDCG@10 |",
        "|---|---:|---:|---:|",
        f"| {baseline['name']} | {baseline['recall_at_10']:.4f} | {baseline['precision_at_10']:.4f} | {baseline['ndcg_at_10']:.4f} |",
        f"| {method['name']} | {method['recall_at_10']:.4f} | {method['precision_at_10']:.4f} | {method['ndcg_at_10']:.4f} |", "",
        f"相对同图同候选基线：Recall@10 {result['relative']['recall_at_10_percent']:+.2f}%，NDCG@10 {result['relative']['ndcg_at_10_percent']:+.2f}%。", "",
        "## 复现边界", "", result["scope"], "",
    ))
