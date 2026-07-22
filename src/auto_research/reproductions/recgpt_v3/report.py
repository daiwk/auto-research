def render(result: dict) -> str:
    base, method, diag = result["baseline"], result["method"], result["diagnostics"]
    return "\n".join([
        "# RecGPT-V3", "", f"公开数据：MovieLens 1M（{result['dataset']['users']} users / {result['dataset']['items']} items）。", "",
        "| Variant | Hit@10 | NDCG@10 | Head share@10 |", "|---|---:|---:|---:|",
        f"| {base['name']} | {base['hit_at_10']:.4f} | {base['ndcg_at_10']:.4f} | {base['head_share_at_10']:.4f} |",
        f"| {method['name']} | {method['hit_at_10']:.4f} | {method['ndcg_at_10']:.4f} | {method['head_share_at_10']:.4f} |", "",
        f"NDCG@10 {result['relative']['ndcg_at_10_percent']:+.2f}%；memory 输入 token -{diag['memory_token_reduction_percent']:.2f}%；latent reasoning slots -{diag['reasoning_slot_reduction_percent']:.2f}%。", "",
        "## 复现边界", "", result["scope"], "",
    ])
