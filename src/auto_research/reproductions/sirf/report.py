def render(result):
    return "\n".join([
        f"# {result['paper']['title']}", "",
        "| 对照 | Precision | Black Recall | Accuracy |", "|---|---:|---:|---:|",
        f"| {result['baseline']['name']} | {result['baseline']['precision']:.4f} | {result['baseline']['black_recall']:.4f} | {result['baseline']['accuracy']:.4f} |",
        f"| {result['method']['name']} | {result['method']['precision']:.4f} | {result['method']['black_recall']:.4f} | {result['method']['accuracy']:.4f} |", "",
        f"P95 下 Black Recall 变化：{result['relative']['black_recall_at_p95_points']:+.2f} pp。", "",
        "## 复现边界", "", result["scope"], "",
    ])
