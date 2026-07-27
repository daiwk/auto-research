def render(result):
    base, method = result["baseline"], result["method"]
    return "\n".join([
        f"# {result['paper']['title']}", "",
        "| Variant | Hit@10 | NDCG@10 |", "|---|---:|---:|",
        f"| {base['name']} | {base['hit_at_10']:.4f} | {base['ndcg_at_10']:.4f} |",
        f"| {method['name']} | {method['hit_at_10']:.4f} | {method['ndcg_at_10']:.4f} |", "",
        f"相对同协议基线：NDCG@10 {result['relative']['ndcg_at_10_percent']:+.2f}%。", "",
        "## 复现边界", "", result["scope"], "",
    ])
